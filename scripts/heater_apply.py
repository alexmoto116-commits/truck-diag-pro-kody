# -*- coding: utf-8 -*-
"""
Заводские таблицы кодов отопителей (Eberspächer, Webasto, Планар).

Две команды, запускать из корня репозитория:

  python -X utf8 -I scripts/heater_apply.py sources
      Собирает scripts/heater_sources.json (в git: общедоступные сведения из
      заводских руководств, с документом и страницей по каждому коду) из
      сверенных выписок в _мозг/дело/отопители-источники/ (eberspacher.json,
      webasto.json, telestart.json если есть, planar.json).

  python -X utf8 -I scripts/heater_apply.py apply
      Заменяет в pcode-source/pcode.json таблицы eberspacher, webasto, planar
      на сверенные (старый файл копируется в pcode-source/_архив-выгрузок-до-2026-10-20/).
      Тексты для поиска и KV собираются из heater_sources.json. pcode.json в git
      не попадает (закрытая база), остальные марки не трогаются.

Страницы кодов берут подробности (модель, источник, заводская рекомендация)
прямо из heater_sources.json (scripts/build_heater_pages.py).
"""
import io, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_мозг', 'дело', 'отопители-источники')
OUT = os.path.join(ROOT, 'scripts', 'heater_sources.json')
PCODE = os.path.join(ROOT, 'pcode-source', 'pcode.json')
ARCH = os.path.join(ROOT, 'pcode-source', '_архив-выгрузок-до-2026-10-20')


def load(*parts):
    return json.loads(io.open(os.path.join(SRC, *parts), encoding='utf-8').read())


def src_list(sources):
    """Только публичные сведения: документ, адрес, страница."""
    out = []
    for s in sources or []:
        out.append({k: s.get(k) for k in ('doc', 'url', 'page') if s.get(k)})
    return out


def cmd_sources():
    eb = load('eberspacher', 'eberspacher.json')
    wa = load('webasto', 'webasto.json')
    pl = load('planar', 'planar.json')
    res = {'about': u'Сверено по заводским руководствам 28.10.2026. Собрано scripts/heater_apply.py sources.'}

    # --- Eberspächer
    e = {}
    for c in eb['codes']:
        e[c['code']] = {
            'kind': 'airtronic', 'title': c['ru_title'], 'ru': c['ru'], 'en': c['en'],
            'model': c['model'], 'hydronic_note': c.get('hydronic_note') or '',
            'remedy': c.get('remedy_ru') or '', 'level': c.get('remedy_level') or '',
            'confidence': c.get('confidence') or '', 'sources': src_list(c['sources'])}
    for c in eb['hydronic_only']:
        e[c['code']] = {
            'kind': 'hydronic', 'title': c['ru'], 'ru': c['ru'], 'en': c['en'],
            'model': c['model'], 'hydronic_note': '', 'remedy': c.get('remedy_ru') or '',
            'level': c.get('remedy_level') or '', 'note': c.get('note') or '',
            'confidence': c.get('confidence') or '', 'sources': src_list(c['sources'])}
    res['eberspacher'] = e
    res['eberspacher_removed'] = list(eb['remove'])

    # --- Webasto
    pc = {}
    for c in wa['pc_codes']:
        pc[c['code']] = {
            'title': c['ru_title'], 'ru': c['ru'], 'en': c['en'], 'f': c['f_on_timer'],
            'confidence': c.get('confidence') or '', 'sources': src_list(c['sources'])}
    f = {}
    for model, rows in wa['f_codes'].items():
        for r in rows:
            f.setdefault(r['code'], []).append({
                'model': model, 'title': r['ru_title'], 'ru': r['ru'], 'en': r['en'],
                'pc': r['pc'], 'remedy': r.get('remedy_ru') or '', 'note': r.get('note') or '',
                'confidence': r.get('confidence') or '', 'sources': src_list(r['sources'])})
    disp = []
    for d in wa['display']:
        if not d.get('how') or d['how'].startswith('НЕ ПОДТВЕРЖДЕНО'):
            continue
        how = d['how']
        if d['control'].startswith('WTT'):
            # В выписке стоит пометка про прежние ошибки сайта - на страницу она не нужна.
            how = (u'Показывает шестнадцатеричные ПК-коды (00...FF, например 03, 84, 9A). '
                   u'Один F-код таймера объединяет несколько ПК-кодов.')
        disp.append({'control': d['control'], 'how': how, 'source': d.get('source') or ''})
    tpath = os.path.join(SRC, 'webasto', 'telestart', 'telestart.json')
    if os.path.isfile(tpath):
        for d in load('webasto', 'telestart', 'telestart.json')['display']:
            if d.get('shows_f_number') is False:
                disp.append({'control': d['control'], 'how': d['how_ru'], 'no_f': True,
                             'source': u'; '.join(s['doc'] for s in d.get('sources', []))})
    res['webasto'] = {'pc': pc, 'f': f, 'display': disp}

    # --- Планар
    p = {}
    for c in pl['codes']:
        p[c['code']] = {
            'title': c['ru_title'], 'ru': c['ru'], 'en': c['en'], 'system': c['system'],
            'equivalent': c['equivalent'], 'remedy': c.get('remedy_ru') or '',
            'confidence': c.get('confidence') or '', 'sources': src_list(c['sources'])}
    res['planar'] = p

    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True))
    print(u'записано %s: eberspacher %d (удалить %d), webasto пк %d, F %d, planar %d'
          % (OUT, len(e), len(res['eberspacher_removed']), len(pc), len(f), len(p)))


# ------------------------------------------------------------ тексты для поиска

def _f_summary(fmap, lang):
    """«F03» или «F06 (Air Top 2000 ST, Thermo Top Evo), F10 (…)»."""
    groups = {}
    for model, fv in fmap.items():
        if fv:
            groups.setdefault(fv, []).append(model)
    if not groups:
        return u''
    if len(groups) == 1:
        return list(groups)[0]
    return u', '.join(u'%s (%s)' % (fv, u', '.join(ms)) for fv, ms in sorted(groups.items()))


def _planar_short(c, lang):
    t = c['title'] if lang == 'ru' else c['en']
    if lang == 'ru' and u': ' in t:
        t = t.split(u': ', 1)[1]
        t = t[:1].upper() + t[1:]
    sysm = c['system']
    if lang == 'ru':
        if u'совпадают' in sysm:
            lab = u''
        elif sysm.startswith(u'ПУ-5'):
            lab = u' (число миганий пульта ПУ-5)'
        else:
            lab = u' (код таблицы ремонта)'
    else:
        if u'совпадают' in sysm:
            lab = u''
        elif sysm.startswith(u'ПУ-5'):
            lab = u' (PU-5 remote blink count)'
        else:
            lab = u' (repair-table code)'
    out = t.rstrip(u'.') + lab
    if u'два разных смысла' in sysm:
        # Один номер означает разное в двух системах - второй смысл в тот же ответ поиска.
        last = (c['ru'] if lang == 'ru' else c['en']).rstrip(u'.').split(u'. ')[-1]
        out += u'. ' + last
    return out


def _hydronic_text(note):
    """Примечание про Hydronic одной фразой: без повторов «Hydronic: В Hydronic ...»."""
    n = note.strip()
    for pre in (u'Тот же смысл; ', u'В Hydronic тот же номер: '):
        if n.startswith(pre):
            n = n[len(pre):]
    if n.startswith(u'в Hydronic '):
        n = n[len(u'в '):]
    elif n.startswith(u'В Hydronic '):
        n = n[len(u'В '):]
    if n.startswith(u'Hydronic'):
        return n[:1].upper() + n[1:]
    return u'Hydronic: ' + n


def compose(src):
    out = {'eberspacher': {}, 'webasto': {}, 'planar': {}}
    for code, c in src['eberspacher'].items():
        ru = u'%s (%s)' % (c['title'], c['model'])
        en = u'%s (%s)' % (c['en'], c['model'])
        note = c.get('hydronic_note') or u''
        if c['kind'] == 'airtronic' and note and not note.startswith((u'Тот же смысл.', u'В Hydronic нет')):
            ru += u'. ' + _hydronic_text(note)
        out['eberspacher'][code] = {'ru': ru, 'en': en}
    w = src['webasto']
    for code, c in w['pc'].items():
        fs = _f_summary(c['f'], 'ru')
        if fs:
            ru = u'%s (служебный ПК-код Webasto Thermo Test; на таймере: %s)' % (c['title'], fs)
            en = u'%s (PC diagnostic code, Webasto Thermo Test; on the timer: %s)' % (c['en'], fs)
        else:
            ru = u'%s (служебный ПК-код Webasto Thermo Test; на таймере F-кода нет)' % c['title']
            en = u'%s (PC diagnostic code, Webasto Thermo Test; no F-code on the timer)' % c['en']
        out['webasto'][code] = {'ru': ru, 'en': en}
    for fcode, rows in w['f'].items():
        gru, gen = {}, {}
        for r in rows:
            gru.setdefault(r['title'], []).append(r['model'])
            gen.setdefault(r['en'], []).append(r['model'])
        pcs = []
        for r in rows:
            for x in r['pc']:
                if x not in pcs:
                    pcs.append(x)
        if len(gru) == 1:
            ru = u'%s (таймер, F-код; ПК-коды: %s)' % (list(gru)[0], u', '.join(sorted(pcs)))
        else:
            ru = u'; '.join(u'%s (%s)' % (t, u', '.join(ms)) for t, ms in gru.items()) + \
                u' (таймер, F-код; ПК-коды: %s)' % u', '.join(sorted(pcs))
        if len(gen) == 1:
            en = u'%s (timer F-code; PC codes: %s)' % (list(gen)[0], u', '.join(sorted(pcs)))
        else:
            en = u'; '.join(u'%s (%s)' % (t, u', '.join(ms)) for t, ms in gen.items()) + \
                u' (timer F-code; PC codes: %s)' % u', '.join(sorted(pcs))
        out['webasto'][fcode] = {'ru': ru, 'en': en}
    for code, c in src['planar'].items():
        out['planar'][code] = {'ru': _planar_short(c, 'ru'), 'en': _planar_short(c, 'en')}
    return out


def cmd_apply():
    src = json.loads(io.open(OUT, encoding='utf-8').read())
    pcode = json.loads(io.open(PCODE, encoding='utf-8').read())
    if not os.path.isdir(ARCH):
        os.makedirs(ARCH)
    bak = os.path.join(ARCH, 'pcode.до-исправления-отопителей-2026-10-28.json')
    if not os.path.exists(bak):
        shutil.copyfile(PCODE, bak)
        print(u'копия старого pcode.json: %s' % bak)
    new = compose(src)
    for b, tbl in new.items():
        old = pcode.get(b, {})
        added = sorted(set(tbl) - set(old))
        gone = sorted(set(old) - set(tbl))
        changed = sorted(k for k in set(tbl) & set(old) if old[k] != tbl[k])
        print(u'%s: было %d, стало %d; новых %d, убрано %d, изменено %d'
              % (b, len(old), len(tbl), len(added), len(gone), len(changed)))
        pcode[b] = tbl
    io.open(PCODE, 'w', encoding='utf-8').write(
        json.dumps(pcode, ensure_ascii=False, indent=1, sort_keys=True))
    print(u'записано', PCODE)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'sources':
        cmd_sources()
    elif cmd == 'apply':
        cmd_apply()
    else:
        print(__doc__)
        sys.exit(1)
