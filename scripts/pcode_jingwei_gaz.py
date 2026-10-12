# -*- coding: utf-8 -*-
"""Две дилерские таблицы, 27.09.2026: отопитель Jingwei (штатный у SITRAK) и
ГАЗон Next.

Какие коды бывают — по списку lorrytruck.ru; текст наш. У Jingwei код E00…E32
вместе с двоичной записью, которую отопитель мигает светодиодом. У ГАЗон Next
это стандартные коды OBD-II (SAE J2012) — смысл задан стандартом; заводские
P1601 и P1602 не берём: проверить их не по чему.

    python scripts/pcode_jingwei_gaz.py   # дописать в pcode-source/pcode.json
    python scripts/build_pcode.py         # потом, как всегда
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Тексты кодов хранятся вне git: pcode-source/jingwei_gaz_data.json
# (формат: {"jingwei": {код: {"ru": ..., "en": ...}}, "gaz": {...}}).
DATA_PATH = os.path.join(ROOT, 'pcode-source', 'jingwei_gaz_data.json')


def load_tables():
    try:
        with io.open(DATA_PATH, encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        sys.exit('Нет файла с текстами кодов: ' + DATA_PATH + '\n'
                 'Он лежит в pcode-source/, который не попадает в git. '
                 'Положите jingwei_gaz_data.json туда и запустите скрипт снова.')
    jingwei = {k: (v['ru'], v['en']) for k, v in data['jingwei'].items()}
    gaz = {k: (v['ru'], v['en']) for k, v in data['gaz'].items()}
    return jingwei, gaz


if __name__ == '__main__':
    JINGWEI, GAZ = load_tables()
    путь = os.path.join(ROOT, 'pcode-source', 'pcode.json')
    p = json.load(io.open(путь, encoding='utf-8'))
    for марка, таблица in (('jingwei', JINGWEI), ('gaz', GAZ)):
        p.setdefault(марка, {})
        for к, (ру, en) in таблица.items():
            p[марка][к] = {'ru': ру, 'en': en}
        print(марка, len(p[марка]))
    io.open(путь, 'w', encoding='utf-8').write(json.dumps(p, ensure_ascii=False, indent=1))
