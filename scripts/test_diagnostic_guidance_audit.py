#!/usr/bin/env python3
"""Unit tests for diagnostic audit matching and exclusion of hidden JSON-LD."""
import tempfile
import unittest
from pathlib import Path
from audit_diagnostic_guidance import audit_page, inventory, markdown


def sample_page(visible, js=""):
    return ('<!doctype html><html lang="ru"><head>'
            '<title>SPN test</title><meta name="description" content="Test">'
            '<script type="application/ld+json">' + js + '</script></head>'
            '<body><main><h1>Test</h1><section><h2>Можно ли ехать</h2>'
            '<p>' + visible + '</p></section></main></body></html>')


class DiagnosticGuidanceAuditTest(unittest.TestCase):
    def test_find_brake_safety_assumption_in_visible_copy(self):
        issues = audit_page(sample_page("АБС неисправна, обычные тормоза работают."),
                            "kody/spn-789.html")
        self.assertIn("brake_operation_assumed", {x["rule"] for x in issues})

    def test_jsonld_does_not_duplicate_visible_matches(self):
        issues = audit_page(sample_page("Проверьте FMI.",
                                         '{"description":"обычные тормоза работают"}'),
                            "kody/spn-789.html")
        self.assertNotIn("brake_operation_assumed", {x["rule"] for x in issues})

    def test_detect_generic_permission_to_drive(self):
        issues = audit_page(sample_page("Обычно ехать можно."),
                            "kody/spn-555.html")
        self.assertIn("generic_drive_clearance", {x["rule"] for x in issues})

    def test_charge_scenario_only_on_diagonal_relay(self):
        text = sample_page("Бортовая сеть не держит напряжение.")
        target = audit_page(text, "kody/spn-802.html")
        other = audit_page(text, "kody/spn-168.html")
        self.assertIn("charging_scenario_on_abs_relay", {x["rule"] for x in target})
        self.assertNotIn("charging_scenario_on_abs_relay", {x["rule"] for x in other})

    def test_only_public_spn_files_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "kody").mkdir()
            (root / "kody/spn-789.html").write_text(sample_page("обычные тормоза работают"), encoding="utf-8")
            (root / "kody/index.html").write_text(sample_page("Обычно ехать можно"), encoding="utf-8")
            result = inventory(root)
            self.assertEqual(result["pages_scanned"], 1)
            self.assertEqual(result["pages_flagged"], 1)
            self.assertEqual(result["counts_by_rule"]["brake_operation_assumed"], 1)
            self.assertIn("kody/spn-789.html", markdown(result))


if __name__ == "__main__":
    unittest.main()
