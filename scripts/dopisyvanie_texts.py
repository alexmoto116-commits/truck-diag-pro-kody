# -*- coding: utf-8 -*-
"""Дописанные тексты страниц (механизм от 09.11.2026).

Где что лежит:
  dopis_codes_ru.py  - страницы кодов ru,   ключ 'code:<SPN>'
  dopis_codes_en.py  - страницы кодов en,   ключ 'code-en:<SPN>'
  dopis_brands.py    - марки: ru 'brand:<марка>+' (добавка к прежним блокам), en 'brand-en:<марка>'
Всё сливается в EXTRA_BLOCKS (marki_problemy_texts.py, в самом конце файла).
Ключ с '+' в конце читается extra_html() ПОСЛЕ ключа без '+' - так можно
дописать страницу, у которой блоки уже есть, не трогая их.
Элемент раздела: строка - абзац; список - маркеры; кортеж (вопрос, ответ) - FAQ
(кортежи уходят и в разметку FAQPage через extra_faq()). **x** - жирный не
поддерживается в extra_html, поэтому в build_pages он снимается/заменяется там же.
Новая страница в механизме: добавить ключ в один из файлов; сборка подхватит сама.
"""
import dopis_codes_ru, dopis_codes_en, dopis_brands

ALL = {}
for _m in (dopis_codes_ru, dopis_codes_en, dopis_brands):
    ALL.update(_m.BLOCKS)
