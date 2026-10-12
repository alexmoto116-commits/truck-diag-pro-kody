# -*- coding: utf-8 -*-
"""English twin of own_checks.py: where the node is, what to measure, the figures,
common causes. Key = SPN. The same fields as the Russian data:
  узел    - what it is and where it sits;
  нормы   - [(what, value)] - the figures table;
  шаги    - check order, simple to complex; "FMI 3, 4: ..." at the start of a
            line means the step is for those FMI only;
  причины - common causes, most to least common.
Keys match own_checks.CHECKS one to one (checked in the build).
Numbers, units, FMI values and make names are the same as in the Russian data.
"""

CHECKS = {
    100: {
        'узел': 'The oil pressure sensor sits on the cylinder block by the oil filter or on '
                'the main oil gallery. Most engines use a three-wire unit: 5 V reference, '
                'ground and signal. Some engines have a single-wire low oil pressure switch '
                'fitted instead of it or alongside it.',
        'нормы': [
            ('Reference voltage at the connector, ignition on', '5.0 V ± 0.25'),
            ('Sensor signal in the working range', '0.5…4.5 V'),
            ('Pressure at hot idle', 'usually not below 0.8…1.0 bar — check against the factory data'),
            ('Pressure at mid and high revs', 'usually 3…5 bar'),
        ],
        'шаги': [
            'Oil level by the dipstick — on level ground, a few minutes after stopping the engine.',
            'FMI 1, 17, 18 (pressure low): do not trust the sensor until you have checked the '
            'pressure with a mechanical gauge. Fit a mechanical gauge in place of the sensor and '
            'compare with the dash reading. If the gauge shows normal — the fault is in the sensor '
            'or the wiring. If it does not — stop the engine and look for the cause in the engine.',
            'FMI 3, 4 (voltage above or below normal): unplug the connector and inspect the '
            'contacts for corrosion and oil inside the connector. Switch the ignition on and '
            'measure the reference voltage between the supply and ground at the connector.',
            'No reference voltage — check the wires back to the ECU for continuity. If codes for '
            'other 5 V sensors are active at the same time, the shared sensor supply line is the '
            'suspect: one shorted sensor pulls it down for all of them.',
            'FMI 2 (signal unreliable): wiggle the harness with the engine running and watch the '
            'value in diagnostics. If it jumps — poor contact.',
        ],
        'причины': [
            'Connector: corrosion, oil in the connector after a leak at the sensor thread.',
            'The sensor itself.',
            'Low oil level or diluted oil: fuel or coolant in the sump.',
            'Clogged oil pickup screen, worn oil pump.',
            'Worn bearings — pressure drops specifically at hot idle.',
        ],
    },

    168: {
        'узел': 'The ECU measures the voltage at its own power input. This code means the ECU '
                'sees the wrong voltage: the cause is in the batteries, the alternator, or the '
                'wires and grounds between them and the ECU.',
        'нормы': [
            ('Two charged 12 V batteries, engine off', '25.2…25.6 V'),
            ('Engine running, alternator charging', '27.5…28.8 V'),
            ('During cranking', 'not below 18 V'),
            ('Difference between the battery terminals and the ECU input under load', 'not more than 0.5 V'),
        ],
        'шаги': [
            'Measure at the battery terminals with the engine off, then with it running.',
            'Above 29.5 V with the engine running — alternator regulator. Below 27 V — alternator, '
            'belt, or the wire from the alternator.',
            'Battery voltage is normal but the ECU sees less: measure at the ECU power connector '
            'with a load on (headlights, heater fan). A difference of more than 0.5 V means poor '
            'contact: the battery terminals, the ECU ground, the engine-to-frame ground, the power fuse.',
            'The code appears only when cranking — check the batteries with a load tester or meter: '
            'a sagging battery drops the voltage and the ECU restarts.',
            'If several ECUs have this code at once, the cause is common: batteries, alternator or '
            'the main ground, not the ECU.',
        ],
        'причины': [
            'Corroded or loosely tightened battery terminals.',
            'Engine-to-frame ground or ECU ground.',
            'Worn or discharged batteries.',
            'Alternator regulator, brushes, belt.',
            'ECU power fuse or relay with burnt contacts.',
        ],
    },

    639: {
        'узел': 'The main CAN bus, over which the vehicle\'s ECUs exchange data: engine, gearbox, '
                'brakes, dash, tachograph. This code means an ECU cannot hear its neighbours on '
                'the bus, or the bus itself is faulty. The bus is two twisted wires, CAN-H and '
                'CAN-L, with a 120 Ω resistor at each end.',
        'нормы': [
            ('Resistance between CAN-H and CAN-L, power off', 'about 60 Ω'),
            ('If it reads about 120 Ω', 'one resistor or a section of the bus is open'),
            ('If it reads about 40 Ω or less', 'an extra resistor or a short circuit'),
            ('Voltage of CAN-H to ground, ignition on', 'about 2.5…3.5 V'),
            ('Voltage of CAN-L to ground', 'about 1.5…2.5 V'),
        ],
        'шаги': [
            'Read the codes of all ECUs: which one does not answer. If one is silent — check its '
            'power, ground and connector. If codes are coming from all of them — check the bus itself.',
            'Switch the power off and measure the resistance between CAN-H and CAN-L at the '
            'diagnostic connector. On the 9-pin truck connector these are pins C and D; on the '
            '16-pin one it depends on the make — on many it is pins 3 and 11 or 6 and 14.',
            'Ignition on, measure the CAN-H and CAN-L voltages to ground. If one of them is at zero '
            'or at plus — a wire is shorted.',
            'Disconnect the ECUs one at a time and see whether the short goes away: a faulty ECU '
            'can pull the whole bus down.',
            'Inspect the harness at the bends: at the cab, at the frame, at added equipment. '
            'Third-party taps into CAN (alarm, tracker) are a common cause.',
        ],
        'причины': [
            'A tap into the bus by added equipment: tracker, alarm, fuel sensor.',
            'Corroded connector or water in the connector.',
            'Chafed bus wire.',
            'Loss of power or ground at one of the ECUs.',
            'A faulty ECU that shorts the bus.',
        ],
    },

    157: {
        'узел': 'The fuel pressure sensor sits on the end of the common rail. Three-wire: 5 V '
                'reference, ground and signal. The ECU regulates the pressure from it, so this '
                'code almost always comes with loss of power or the engine stopping.',
        'нормы': [
            ('Reference voltage at the connector', '5.0 V ± 0.25'),
            ('Signal with the engine off', 'about 0.5 V'),
            ('Pressure for starting', 'usually not less than 200…300 bar — check against the factory data'),
        ],
        'шаги': [
            'FMI 3, 4 (electrical): unplug the connector, inspect the contacts, and with the ignition '
            'on measure the 5 V reference. With the engine off the sensor should show close to zero '
            'pressure: if it shows hundreds of bar — the sensor is at fault.',
            'FMI 1, 17, 18 (pressure low): fuel first — level, coarse and fine filters, transfer pump. '
            'Air in the clear hose or bubbles in the sedimenter — an air leak on the suction side.',
            'Check the leak-off from the injectors: disconnect the returns and compare how much each '
            'one returns on cranking or at idle. If one returns noticeably more than the others — '
            'that injector is pulling the rail pressure down.',
            'Check the pressure regulating valve on the high-pressure pump and the rail\'s pressure '
            'relief valve (the rail has a drain pipe): a leak from the relief valve with the engine '
            'running — it has opened or is faulty.',
            'FMI 0, 16 (pressure high): pressure regulating valve on the high-pressure pump, clogged '
            'drain from the rail.',
        ],
        'причины': [
            'Clogged fuel filters, air leak on the suction side.',
            'Worn injector with excessive leak-off.',
            'Pressure regulating valve on the high-pressure pump.',
            'Rail pressure relief valve.',
            'Connector or the pressure sensor itself.',
            'Worn high-pressure pump.',
        ],
    },
}


# the other batches: engine, fuel, electrics, brakes, second hundred
from own_checks_en_motor import CHECKS as _motor
from own_checks_en_fuel import CHECKS as _fuel
from own_checks_en_elec import CHECKS as _elec
from own_checks_en_brake import CHECKS as _brake
from own_checks_en_more import CHECKS as _more
from own_checks_en_3 import CHECKS as _third
from own_checks_en_4 import CHECKS as _fourth
for _c in (_motor, _fuel, _elec, _brake, _more, _third, _fourth):
    for _k, _v in _c.items():
        assert _k not in CHECKS, _k
        CHECKS[_k] = _v
