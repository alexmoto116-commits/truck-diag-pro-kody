#!/usr/bin/env python3
"""Read-only inventory of potentially unsafe/generic guidance on public SPN pages.

No network, no dependencies, no private code database. Flagged copy is a review
candidate, not a medical/mechanical verdict or a Google indexing diagnosis.

Usage: python3 scripts/audit_diagnostic_guidance.py
       python3 scripts/audit_diagnostic_guidance.py --json diagnostic-audit.json --markdown diagnostic-audit.md
"""
import argparse
from collections import Counter
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SPN = re.compile(r"spn-(\d+)\.html$")
MAX_EXAMPLES = 30

RULES = (
    ("brake_operation_assumed", "high", re.compile(
        r"обычные тормоза (?:работают|при этом действуют)", re.I),
     "Brake function asserted without independent check"),
    ("electrical_fault_drive_clearance", "high", re.compile(
        r"(?:Код электрический|код электрический|Само давление, скорее всего, в норме)[^.]{0,400}(?:Ехать можно|ехать можно)", re.I | re.S),
     "Sensor circuit fault interpreted as proof it is safe to drive"),
    ("certain_reach_base", "medium", re.compile(
        r"Хватит доехать до базы|До места, где есть помощь, лучше доехать", re.I),
     "Unverified promise about reaching a destination"),
    ("generic_drive_clearance", "review", re.compile(
        r"Обычно ехать можно|Ехать можно осторожно", re.I),
     "Generic positive driving advice; verify FMI and symptoms"),
    ("definite_engine_continuation", "high", re.compile(
        r"Посреди трассы машина не заглохнет", re.I),
     "Unsupported categorical prediction of engine behavior"),
    ("charging_scenario_on_abs_relay", "high", re.compile(
        r"Бортовая сеть не держит напряжение", re.I),
     "Charging-system scenario in ABS relay context"),
)


class Sections(HTMLParser):
    """Extract only page text, not scripts/JSON-LD, styles or source comments."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.parts = []
        self.description = ""
        self.in_section = 0
        self.section_buffer = []
        self.sections = []
        self.in_heading = 0
        self.heading_buffer = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ("script", "style", "noscript"):
            self.hidden += 1
        if tag == "meta" and d.get("name", "").lower() == "description":
            self.description = d.get("content", "")
        if self.hidden:
            return
        if tag == "section":
            self.in_section += 1
            if self.in_section == 1:
                self.section_buffer = []
        if tag == "h2":
            self.in_heading += 1
            self.heading_buffer = []

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self.hidden = max(0, self.hidden - 1)
            return
        if self.hidden:
            return
        if tag == "h2" and self.in_heading:
            self.in_heading -= 1
        if tag == "section" and self.in_section:
            self.in_section -= 1
            if self.in_section == 0:
                self.sections.append(" ".join(self.section_buffer))
                self.section_buffer = []

    def handle_data(self, data):
        if self.hidden:
            return
        s = " ".join(unescape(data).split())
        if s:
            self.parts.append(s)
            if self.in_section:
                self.section_buffer.append(s)
            if self.in_heading:
                self.heading_buffer.append(s)


def audit_page(content, path):
    page = Sections()
    page.feed(content)
    # Search user-visible copy and avoid repeating findings from JSON-LD.
    visible = " ".join(page.parts)
    context = visible + " " + page.description
    findings = []
    for rule_id, severity, pattern, rationale in RULES:
        found = pattern.search(context)
        if found:
            findings.append({
                "rule": rule_id, "severity": severity, "path": path,
                "matched": found.group(0)[:200], "why_review": rationale,
            })
    # Separate from risk claims: page is a review candidate when its
    # diagnostic topic and explanation about charging are incompatible.
    if SPN.search(path) and "spn-802.html" not in path:
        findings = [x for x in findings if x["rule"] != "charging_scenario_on_abs_relay"]
    # Flag template claims in sections rather than hard-failing the whole build.
    # Authors must verify FMI/vehicle-specific applicability before modifying.
    return findings


def inventory(root):
    findings = []
    files = sorted((root / "kody").glob("spn-*.html"))
    for file in files:
        if not SPN.fullmatch(file.name):
            continue
        rel = file.relative_to(root).as_posix()
        findings.extend(audit_page(file.read_text(encoding="utf-8"), rel))
    counts = dict(sorted(Counter(x["rule"] for x in findings).items()))
    severities = dict(sorted(Counter(x["severity"] for x in findings).items()))
    return {
        "scope": "public kody/spn-*.html only",
        "pages_scanned": len(files),
        "pages_flagged": len({x["path"] for x in findings}),
        "finding_count": len(findings),
        "counts_by_rule": counts,
        "counts_by_severity": severities,
        "findings": findings,
        "disclaimer": "Potential content problems for editorial review; not verified faults or ranking causes.",
    }


def markdown(report):
    lines = [
        "# CodeTruck diagnostic guidance inventory",
        "",
        f"Public SPN pages scanned: **{report['pages_scanned']}**.",
        f"Pages requiring editorial review: **{report['pages_flagged']}**.",
        f"Total findings: **{report['finding_count']}**.",
        "",
        "These are automated text matches, not independently verified diagnoses.",
        "They do not establish why Google indexes or does not index a page.",
        "",
        "## Findings by rule",
        "",
        "| Rule | Count |",
        "|---|---:|",
    ]
    lines.extend(f"| {rule} | {count} |" for rule, count in report["counts_by_rule"].items())
    lines.extend(["", "## Prioritized examples (up to 30)", ""])
    order = {"high": 0, "medium": 1, "review": 2}
    ranked = sorted(report["findings"], key=lambda x: (order[x["severity"]], x["rule"], x["path"]))
    for x in ranked[:MAX_EXAMPLES]:
        lines.append(f"- **{x['severity']}** — `{x['path']}` / `{x['rule']}`: {x['matched']}")
    if not ranked:
        lines.append("No matching patterns.")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json_out")
    parser.add_argument("--markdown", dest="markdown_out")
    args = parser.parse_args()
    report = inventory(ROOT)
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown_out:
        Path(args.markdown_out).write_text(markdown(report), encoding="utf-8")
    print(f"SPN files scanned: {report['pages_scanned']}; pages flagged: {report['pages_flagged']}; findings: {report['finding_count']}")
    for rule, count in report["counts_by_rule"].items():
        print(f"  {rule}: {count}")
    print("REPORT ONLY: No content, index policy, sitemaps or private data changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
