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
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JINGWEI = {
    'E00': ('Обрыв цепи датчика пламени (двоичный код 00000). Проверить разъём датчика и сам датчик.',
            'Flame sensor open circuit (binary 00000). Check the sensor connector and the sensor.'),
    'E01': ('Слишком большой ток нагрузки (00001): замыкание в моторе вентилятора, свече или топливном насосе.',
            'Load current too high (00001): short in the fan motor, glow plug or fuel pump.'),
    'E02': ('Напряжение питания слишком высокое при запуске (00010), выше 30 В. Проверить регулятор генератора.',
            'Supply voltage too high at start (00010), above 30 V. Check the alternator regulator.'),
    'E03': ('Напряжение питания слишком низкое (00011), ниже 18 В на клеммах отопителя. АКБ, провода, клеммы.',
            'Supply voltage too low (00011), below 18 V at the heater terminals. Check batteries, wiring, terminals.'),
    'E04': ('Замыкание датчика пламени (00100). Проверить провод датчика на замыкание, затем датчик.',
            'Flame sensor short circuit (00100). Check the sensor wire for a short, then the sensor.'),
    'E05': ('Обрыв цепи датчика перегрева (00101). Разъём, провода, датчик.',
            'Overheat sensor open circuit (00101). Check connector, wiring, sensor.'),
    'E06': ('Замыкание датчика перегрева (00110). Провода, датчик.',
            'Overheat sensor short circuit (00110). Check wiring and sensor.'),
    'E08': ('Слишком большой ток топливного насоса при проверке на запуске (01000). Разъём, насос.',
            'Fuel pump current too high during start self-test (01000). Check connector and pump.'),
    'E13': ('Отопитель не разжигается (01101): нет топлива, воздух в топливопроводе, насос, свеча, загустевшее на морозе топливо.',
            'Heater fails to ignite (01101): no fuel, air in the fuel line, pump, glow plug, fuel gelled in the cold.'),
    'E14': ('Пламя гаснет во время работы (01110): топливо, подсос воздуха, датчик пламени, забитый выхлоп.',
            'Flame goes out during operation (01110): fuel, air leak, flame sensor, blocked exhaust.'),
    'E18': ('Обрыв цепи свечи (10010): свеча перегорела или отошёл разъём.',
            'Glow plug open circuit (10010): plug burnt out or connector loose.'),
    'E19': ('Слишком большой ток свечи (10011): замыкание свечи.',
            'Glow plug current too high (10011): glow plug short circuit.'),
    'E21': ('Слишком большой ток мотора вентилятора (10101): мотор заклинило или крыльчатка задевает.',
            'Fan motor current too high (10101): motor seized or impeller rubbing.'),
    'E25': ('Давление воздуха слишком низкое (11001): датчик давления воздуха в блоке. Разъём, блок управления.',
            'Air pressure too low (11001): air pressure sensor in the control unit. Check connector, control unit.'),
    'E26': ('Давление воздуха слишком высокое (11010): датчик давления воздуха в блоке. Разъём, блок управления.',
            'Air pressure too high (11010): air pressure sensor in the control unit. Check connector, control unit.'),
    'E27': ('Перегрев отопителя (11011): закрыт вход или выход тёплого воздуха, забит воздуховод.',
            'Heater overheat (11011): warm air inlet or outlet blocked, duct clogged.'),
    'E29': ('Мотор вентилятора не вращается — нет сигнала датчика Холла (11101). Мотор, его разъём, блок.',
            'Fan motor not turning — no Hall sensor signal (11101). Check motor, connector, control unit.'),
    'E32': ('Нет обратного сигнала (11111): неисправен жгут между пультом и блоком.',
            'No feedback signal (11111): harness between control panel and unit faulty.'),
}

GAZ = {
    'P0016': ('Положение коленвала и распредвала не согласовано: фазы газораспределения, датчики.',
              'Crankshaft/camshaft position correlation: valve timing or sensors.'),
    'P003A': ('Привод турбокомпрессора: не выходит на заданное положение.',
              'Turbocharger boost control position exceeded learning limit: actuator not reaching position.'),
    'P0087': ('Давление топлива в рампе слишком низкое.',
              'Fuel rail pressure too low.'),
    'P0106': ('Датчик абсолютного давления во впускном коллекторе (MAP): сигнал вне диапазона или недостоверен.',
              'Manifold absolute pressure (MAP) sensor: range/performance.'),
    'P0116': ('Датчик температуры охлаждающей жидкости: сигнал вне диапазона или недостоверен.',
              'Engine coolant temperature sensor: range/performance.'),
    'P0193': ('Датчик давления топлива в рампе: высокий уровень сигнала.',
              'Fuel rail pressure sensor: circuit high.'),
    'P0217': ('Перегрев двигателя.',
              'Engine coolant over-temperature.'),
    'P0299': ('Давление наддува ниже нормы.',
              'Turbocharger underboost.'),
    'P0300': ('Пропуски воспламенения в нескольких цилиндрах.',
              'Random/multiple cylinder misfire.'),
    'P0404': ('Клапан рециркуляции выхлопных газов (EGR): сигнал вне диапазона или недостоверен.',
              'EGR control circuit: range/performance.'),
    'P0405': ('Датчик положения клапана EGR: низкий уровень сигнала.',
              'EGR sensor A: circuit low.'),
    'P0500': ('Датчик скорости автомобиля.',
              'Vehicle speed sensor.'),
    'P0641': ('Опорное напряжение датчиков, линия A: обрыв цепи.',
              'Sensor reference voltage A: circuit open.'),
    'P226C': ('Турбокомпрессор: давление наддува растёт слишком медленно — заедает геометрия или привод.',
              'Turbocharger boost control slow response: variable geometry or actuator sticking.'),
    'U0001': ('Шина CAN: нет связи между блоками.',
              'High-speed CAN communication bus fault.'),
}

if __name__ == '__main__':
    путь = os.path.join(ROOT, 'pcode-source', 'pcode.json')
    p = json.load(io.open(путь, encoding='utf-8'))
    for марка, таблица in (('jingwei', JINGWEI), ('gaz', GAZ)):
        p.setdefault(марка, {})
        for к, (ру, en) in таблица.items():
            p[марка][к] = {'ru': ру, 'en': en}
        print(марка, len(p[марка]))
    io.open(путь, 'w', encoding='utf-8').write(json.dumps(p, ensure_ascii=False, indent=1))
