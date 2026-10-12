# -*- coding: utf-8 -*-
"""English twin of own_checks_3.py: 100 more codes, the same fields and the same keys.
Key = SPN. Numbers, units, FMI values and make names are the same as in the Russian data.
"""

CHECKS = {
    38: {
        'узел': 'The fuel level sensor in the second tank. The ECU gets its signal as a voltage or over the CAN bus '
                'and shows the level on the dash. If it fails, the readings for the second tank are wrong, and the '
                'site data shows power limited at FMI 3 and 4.',
        'нормы': [
            ('Level readings with a known fuel volume in the tank', 'match the actual volume — check by refuelling'),
            ('Sensor voltage at the connector, ignition on', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3, 4 (voltage above or below the limit): unplug the sensor connector and inspect the contacts for '
            'corrosion and water. Switch the ignition on and measure the sensor supply and the signal against ground.',
            'FMI 3 (voltage above the limit): check the signal wire for a short to plus. Unplug the sensor: if the '
            'signal at the ECU disappears, the fault is in the wiring; if it stays, it is the sensor.',
            'FMI 4 (voltage below the limit): the signal wire may be shorted to ground or open. Check its continuity '
            'from the sensor connector to the ECU.',
            'FMI 19 (sensor signal lost on the CAN bus): check the power and ground of the sensor unit and the bus '
            'for chafing.',
            'Compare the second-tank reading with the first tank and with the actual refuelling volume: if only the '
            'second tank is off, the cause is its sensor or wiring, not the ECU.',
        ],
        'причины': [
            'Corroded sensor connector, water in the connector.',
            'Chafed signal or ground wire near the frame.',
            'Float or resistive sensor stuck in one position.',
            'The ECU input that reads the sensor.',
        ],
    },

    59: {
        'узел': 'The sensor that tells the ECU which position the gearbox shift finger is in. The signal comes from a '
                'sensor in the gearbox or from the gearbox unit over the CAN bus. The brand rows refer to different '
                'parts: for one brand it is the PTO, for another the reverse switch. Check first the part that is fitted in your vehicle.',
        'нормы': [
            ('Reverse switch signal with reverse engaged and not engaged', 'changes — check by diagnostics'),
            ('PTO solenoid valve (Renault row)', 'resistance 40…50 Ω — per the site data'),
        ],
        'шаги': [
            'Read the codes of the gearbox and the PTO unit, if any: if there are bus codes nearby, check the bus first.',
            'FMI 2 (reverse switch signal unreliable): select and deselect reverse at a standstill and watch the value in '
            'diagnostics. Check the switch contacts by resistance when pressed.',
            'FMI 8 (PTO signal present while the PTO control is not active): check the PTO solenoid valve and its sensor '
            'by resistance, then the connections to the ECU.',
            'FMI 19 (gear position signal lost on the CAN bus): check the power and ground of the gearbox unit and the CAN bus for chafing.',
        ],
        'причины': [
            'Corroded connector of the switch or sensor in the gearbox.',
            'Open or shorted wires between the gearbox and the ECU.',
            'PTO solenoid valve.',
            'A faulty gearbox unit that sends the signal.',
        ],
    },

    77: {
        'узел': 'Oil temperature sensor in the front drive axle of the rear bogie. The ECU uses it to warn when the axle '
                'overheats. Axle heating is usually linked to load, oil level and brakes, not to the sensor itself.',
        'нормы': [
            ('Axle oil temperature after warm-up on a flat road', 'per the manufacturer\'s manual'),
            ('Sensor reading on a cold axle', 'close to the outside air temperature — check by diagnostics'),
        ],
        'шаги': [
            'FMI 0 (reading above normal): compare with the temperature of the next axle and the gearbox oil. If the '
            'axle is hot on a flat road — look at the cause in the axle: oil level and condition, brakes, load.',
            'FMI 1 (reading below normal): check the sensor connector and the signal wire to the ECU. An open or '
            'grounded wire gives low readings.',
            'Inspect the sensor connector for corrosion and oil; check the sensor mounting in the axle.',
        ],
        'причины': [
            'Low oil level or old oil in the axle.',
            'Axle brake dragging or slipping.',
            'Temperature sensor or its connector.',
            'Sensor wire pinched in the area of the propshaft.',
        ],
    },

    78: {
        'узел': 'Oil temperature sensor in the rear drive axle of the rear bogie. The ECU uses it to warn about axle '
                'overheating. Overheating is usually linked to load, oil level and brakes.',
        'нормы': [
            ('Axle oil temperature after warm-up on a flat road', 'per the manufacturer\'s manual'),
            ('Sensor reading on a cold axle', 'close to the outside air temperature — check by diagnostics'),
        ],
        'шаги': [
            'FMI 0 (reading above normal): compare with the front axle of the bogie. If the axle is hot on a flat road — '
            'oil level and condition, brakes, load.',
            'FMI 1 (reading below normal): check the sensor connector and the signal wire to the ECU. An open or '
            'grounded wire gives low readings.',
            'Inspect the sensor connector for corrosion and oil; check the sensor mounting in the axle.',
        ],
        'причины': [
            'Low oil level or old oil in the axle.',
            'Axle brake dragging or slipping.',
            'Temperature sensor or its connector.',
            'Sensor wire pinched or chafed near the frame.',
        ],
    },

    101: {
        'узел': 'Crankcase gas pressure sensor, mounted on the crankcase or on the oil separator. The ECU uses it to check '
                'whether the crankcase pressure is rising. High pressure points to a blocked breather or gas blow-by; '
                'low pressure points to a leak or a hose that has come off the intake.',
        'нормы': [
            ('Reference voltage at the connector (three-wire sensor), ignition on', '5.0 V ± 0.25'),
            ('Crankcase pressure with the engine running', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'Inspect the hose from the crankcase to the intake manifold and the oil separator: a hose that has come off '
            'or been pinched is a common cause (FMI 2, per the site data).',
            'FMI 0, 1 (sensor voltage above or below the limit): unplug the connector and check the contacts. With the '
            'ignition on, measure the 5 V reference and the signal against ground.',
            'FMI 16, 18 (pressure above or below the limit): check the crankcase mechanically — breather, oil separator, '
            'hoses. If the pressure really is high — look for gas blow-by from the cylinders.',
        ],
        'причины': [
            'Blocked crankcase breather or oil separator.',
            'Hose from the crankcase to the intake that has come off or is pinched.',
            'Worn piston rings: blow-by raises the crankcase pressure.',
            'Connector or the crankcase pressure sensor itself.',
        ],
    },

    106: {
        'узел': 'Absolute pressure sensor in the intake manifold (MAP). The ECU uses it to control boost and engine load. '
                'Usually three-wire: 5 V reference, ground and signal.',
        'нормы': [
            ('Reference voltage at the connector (three-wire sensor), ignition on', '5.0 V ± 0.25'),
            ('Signal with the engine off', 'close to atmospheric pressure — check by diagnostics'),
        ],
        'шаги': [
            'FMI 4 (voltage below the limit): unplug the connector and inspect the contacts. With the ignition on, measure '
            'the 5 V reference between supply and ground. No 5 V — a broken supply or a short to ground in the sensor circuit.',
            'FMI 16 (voltage above the limit): check that the signal wire is not shorted to plus. Measure the signal against '
            'ground: readings above expected point to the sensor or a short to supply.',
            'Inspect the hose from the manifold to the sensor: a leak or a crack gives a false pressure.',
            'Compare the MAP reading with barometric pressure with the engine off: a difference with good wiring means the sensor.',
        ],
        'причины': [
            'MAP sensor connector: corrosion, moisture.',
            'The intake pressure sensor itself.',
            'Air leak or crack in the hose before the sensor.',
            'Open or shorted wires to the ECU.',
        ],
    },

    116: {
        'узел': 'Pressure sensor in the brake actuation circuit. The ECU gets the pressure that the brake system builds in the '
                'circuit from it. Check the pressure with a gauge first to tell a sensor fault from a real pressure problem.',
        'нормы': [
            ('Reference voltage at the connector (three-wire sensor), ignition on', '5.0 V ± 0.25'),
            ('Pressure by gauge and by the ECU reading at the same circuit pressure', 'match, within the manual tolerance'),
        ],
        'шаги': [
            'FMI 0 (reading above normal): fit a mechanical gauge in the circuit through the standard port and compare '
            'with the sensor reading. Match — the ECU or its calibration; mismatch — the sensor.',
            'FMI 1 (reading below normal): check the pressure in the circuit with the gauge with the vehicle parked and '
            'after pumping up. No pressure — a leak in the brake system; the sensor is not the cause.',
            'Check the sensor connector and the wires to the ECU: with the ignition on, measure the reference voltage and the signal.',
            'Inspect the lines and fittings of the circuit for leaks with soapy water.',
        ],
        'причины': [
            'Leak in the brake actuation circuit.',
            'Pressure sensor or its connector.',
            'Wiring from the sensor to the ECU.',
            'Blocked pressure port or line.',
        ],
    },

    122: {
        'узел': 'Engine brake (retarder) torque in percent: the engine ECU gets this value over the CAN bus from the brake '
                'unit and controls the retarder. The code is linked to the small-disconnect solenoid valve and to the bus.',
        'нормы': [
            ('Torque message on the bus', 'arrives regularly — check by diagnostics'),
            ('Small-disconnect solenoid valve on command', 'operates, per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 0 (mechanical fault of the small-disconnect valve): check that the solenoid valve operates on command — '
            'a click is heard. Sticking — repair or replace the valve per the manual.',
            'FMI 9 (no CAN link to the engine ECU): check the CAN wiring between the brake unit and the engine unit, and the '
            'power and ground of both units. Disconnect the units one at a time.',
            'Check the brake torque in diagnostics when the brake pedal is pressed: the value should change.',
        ],
        'причины': [
            'Sticking small-disconnect solenoid valve.',
            'Broken or chafed CAN wire.',
            'Power or ground of the brake unit.',
            'Engine ECU that does not accept the command.',
        ],
    },

    161: {
        'узел': 'Gearbox input shaft speed, which the gearbox sends over the CAN bus. The engine unit and other units use this '
                'value during shifts and in the torque calculation.',
        'нормы': [
            ('Input shaft speed message on the bus', 'arrives regularly — check by diagnostics'),
            ('Input shaft speed with the engine running', 'changes with the engine speed — check by diagnostics'),
        ],
        'шаги': [
            'FMI 9 (message intermittent or not arriving): check the CAN bus at the gearbox and at the unit that needs the '
            'value. Disconnect the units one at a time and see if the message returns.',
            'FMI 19 (invalid data): check the software versions of the gearbox and the receiving unit: a protocol mismatch '
            'gives wrong values.',
            'Check the power and ground of the gearbox unit: without them there is no message.',
        ],
        'причины': [
            'Chafed wire or poor contact on the CAN bus.',
            'Lost power or ground of the gearbox unit.',
            'Faulty gearbox unit.',
            'Mismatched software versions of the units.',
        ],
    },

    173: {
        'узел': 'Exhaust gas temperature sensor in the exhaust system. The ECU uses it to limit the load when the exhaust '
                'overheats. High temperature is most often caused by regeneration, overload or a faulty injector, not by the sensor.',
        'нормы': [
            ('Sensor signal with the engine off', 'close to the outside air temperature — check by diagnostics'),
            ('Exhaust temperature under load', 'rises with engine load — check by diagnostics; limit per the manual'),
        ],
        'шаги': [
            'FMI 0, 15 (temperature above the permitted value): first find out why the exhaust is hot — DPF regeneration, '
            'overload, a faulty injector. Check the sensor only after that.',
            'Compare the reading with another exhaust temperature sensor: a difference points to the sensor.',
            'Inspect the sensor and its connector: melting, cracks, corrosion.',
        ],
        'причины': [
            'Long DPF regeneration or overload.',
            'Faulty exhaust temperature sensor.',
            'Exhaust system leak or air ingress.',
            'Sensor connector and wiring.',
        ],
    },

    247: {
        'узел': 'Total engine running hours. The ECU sends them to the other units and instruments over J1939. The code '
                'means the value is invalid or not arriving.',
        'нормы': [
            ('Running hours on the instrument and in the unit that keeps the counter', 'match — check by diagnostics'),
            ('Running hours message on the bus', 'arrives regularly — check by diagnostics'),
        ],
        'шаги': [
            'FMI 9 (data not arriving): check the CAN bus and the unit that sends the running hours. Disconnect the units one at a time.',
            'FMI 0, 1 (running hours above or below the expected value): compare with the service book and with the unit that '
            'keeps the counter. After a unit replacement the counter may have been reset or copied incorrectly.',
            'FMI 10 (internal clocks of the units do not match): synchronise the unit clocks by diagnostics.',
        ],
        'причины': [
            'Intermittent CAN bus or broken wire.',
            'Faulty unit that sends the running hours.',
            'Unit replaced without transferring the running hours.',
            'Mismatched internal clocks of the units.',
        ],
    },

    251: {
        'узел': 'Internal real-time clock of the ECU. The ECU keeps the time with it and writes it into the event log. If '
                'the clock is invalid, fault records and time-based running data are wrong.',
        'нормы': [
            ('ECU supply voltage at the terminals with the engine off, two 12 V batteries', '25.2…25.6 V'),
            ('Date and time in diagnostics', 'match the actual time — check by diagnostics'),
        ],
        'шаги': [
            'FMI 2, 10 (clock data invalid or jumping): set the time by diagnostics and check whether it holds after the '
            'ignition is switched off.',
            'FMI 3 (ECU supply voltage above normal): measure the voltage at the ECU terminals with the engine running. '
            'Above normal — the alternator regulator or the battery.',
            'If the time resets after every ignition switch-off — check the ECU supply and its ground against the wiring diagram.',
        ],
        'причины': [
            'ECU supply voltage above or below normal.',
            'Poor ECU ground.',
            'Faulty ECU, clock drift.',
        ],
    },

    354: {
        'узел': 'Outside air humidity sensor. The ECU uses the humidity in the climate control and in its calculations. The '
                'sensor is outside, so its connector and wires often suffer from water and dirt.',
        'нормы': [
            ('Sensor reference voltage, ignition on', 'per the manufacturer\'s manual'),
            ('Humidity readings in a dry and in a humid place', 'change — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (voltage above normal, short to plus or open): the signal wire may be shorted to plus. Unplug the sensor: '
            'if the signal at the ECU disappears, the fault is in the wiring; if it stays, it is the sensor.',
            'FMI 4 (voltage below normal, short to ground): check the signal wire to ground from the sensor connector to the ECU.',
            'Unplug the sensor, inspect the contacts for corrosion and water. With the ignition on, measure the supply and the '
            'signal against ground.',
        ],
        'причины': [
            'Corroded sensor connector.',
            'Signal wire shorted to plus or ground.',
            'The humidity sensor itself.',
            'ECU with a faulty input.',
        ],
    },

    515: {
        'узел': 'Target engine speed: the engine ECU compares the speed with the limits at which it cuts fuel or ignition. '
                'The code means the speed has reached the limit.',
        'нормы': [
            ('Engine speed in the working range', 'below the cut-off limits — per the manufacturer\'s manual'),
            ('Speed sensor with the engine running', 'steady, without jumps — check by diagnostics'),
        ],
        'шаги': [
            'FMI 0, 16 (speed has reached the ignition or fuel cut-off limit): check whether the engine runs away with the '
            'pedal released — check the accelerator pedal and fuel delivery by diagnostics.',
            'FMI 15, 31 (speed above the permitted value): check the speed sensor and its connector — false speed jumps give this code.',
            'Compare the speed on the dash with the diagnostic reading: a difference points to the speed sensor.',
        ],
        'причины': [
            'Accelerator pedal or its sensor giving a false signal.',
            'Engine speed sensor or its wiring.',
            'Faulty fuel delivery control.',
            'ECU software.',
        ],
    },

    523: {
        'узел': 'Current gear that the gearbox sends to the engine ECU over the CAN bus. The engine ECU uses it to select the '
                'operating mode and the torque.',
        'нормы': [
            ('Gear message on the bus', 'arrives regularly — check by diagnostics'),
            ('Gear value during a shift', 'changes at each gear change — check by diagnostics'),
        ],
        'шаги': [
            'FMI 9, 13 (message not arriving or intermittent): check the CAN bus and the power of the gearbox unit. Disconnect '
            'the units one at a time and see if the signal returns.',
            'FMI 19 (invalid data on the bus): check the software version of the gearbox and of the receiving unit.',
            'During a shift the value should change: if not — check the gearbox sensors and switch.',
        ],
        'причины': [
            'Intermittent CAN bus or broken wire.',
            'Lost power or ground of the gearbox unit.',
            'Faulty gearbox unit.',
            'Mismatched software versions of the units.',
        ],
    },

    525: {
        'узел': 'Gear requested by the engine ECU from the gearbox. The gear selector reports its state, and the ECU compares '
                'the request with the actual gear.',
        'нормы': [
            ('Requested and actual gear during a shift', 'match after the shift — check by diagnostics'),
            ('ETC1 message on the bus', 'frame length per the specification — per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 7 (the selector reports an internal fault): read the gearbox codes, clear them and check whether the code returns. '
            'If it comes back — the selector or the gearbox unit per the manual.',
            'FMI 19 (ETC1 frame length wrong): check the software versions of the engine and gearbox units. A frame mismatch '
            'is a software issue, not a wire issue.',
            'Check the power and ground of the units and the CAN bus for chafing.',
        ],
        'причины': [
            'Internal fault of the gear selector.',
            'Mismatched software versions of the units.',
            'Intermittent CAN bus.',
            'Faulty gearbox unit.',
        ],
    },

    527: {
        'узел': 'Cruise control status (CCVS message over J1939): the engine ECU gets from the cruise unit and the switches '
                'whether cruise is on and what speed is set. Without the message the ECU does not know whether cruise is working.',
        'нормы': [
            ('CCVS message on the bus', 'arrives regularly — check by diagnostics'),
            ('Cruise state when the buttons are pressed', 'changes — check by diagnostics'),
        ],
        'шаги': [
            'FMI 9, 12 (message not arriving, timeout): check the unit that sends it and the CAN bus. Disconnect the units one '
            'at a time and see if the message returns.',
            'Check the power and ground of the cruise unit and the engine unit.',
            'Check the cruise switches: the state should change when pressed. If not — look at the wiring of the steering-column switch.',
        ],
        'причины': [
            'Broken or kinked CAN wire.',
            'Lost power to the cruise unit or the engine unit.',
            'Faulty steering-column switch.',
            'Faulty unit that sends CCVS.',
        ],
    },

    559: {
        'узел': 'Kickdown switch on the accelerator pedal: the signal for full pedal press, which makes the gearbox shift down. '
                'The gearbox unit gets it over the CAN bus from the pedal unit.',
        'нормы': [
            ('Switch state at full pedal press', 'changes — check by diagnostics'),
            ('Message on the bus', 'arrives regularly — check by diagnostics'),
        ],
        'шаги': [
            'FMI 9 (message intermittent): check the CAN bus and the pedal unit. Disconnect the units one at a time.',
            'FMI 19 (invalid data on CAN): check the software version of the pedal unit and of the gearbox unit.',
            'Check the kickdown switch on the pedal: at full press the state should change. If not — the switch or its wiring.',
        ],
        'причины': [
            'Connector and wiring of the accelerator pedal unit.',
            'Faulty kickdown switch.',
            'Intermittent CAN bus.',
            'Mismatched software versions of the units.',
        ],
    },

    566: {
        'узел': 'State of the rear inter-axle differential lock. The code refers to the relay circuit through which the lock is engaged.',
        'нормы': [
            ('Lock relay current when engaging and disengaging', 'within the working range — per the manufacturer\'s manual'),
            ('Lock state in the cab and in diagnostics', 'match'),
        ],
        'шаги': [
            'FMI 5 (relay current below normal or open): check the relay and its connector. When the lock is engaged the relay '
            'should click; if not — check the relay supply and the wire to the unit.',
            'FMI 6 (relay current too high): check for a short to ground or to plus in the relay circuit. Remove the relay and see if the code clears.',
            'Check the lock mechanism: it must not stick.',
        ],
        'причины': [
            'Broken wire to the lock relay.',
            'Short to ground in the relay circuit.',
            'Sticking lock mechanism.',
            'Faulty relay.',
        ],
    },

    567: {
        'узел': 'State of the front axle 1 differential lock. The unit drives a pneumatic solenoid that engages the lock. The code '
                'refers to the solenoid circuit.',
        'нормы': [
            ('Pneumatic solenoid output current when engaged', 'within the working range — per the manufacturer\'s manual'),
            ('Lock state in the cab and in diagnostics', 'match'),
        ],
        'шаги': [
            'FMI 5 (solenoid current below normal or open circuit): check the solenoid connector and the wire to the unit. When the '
            'lock is engaged a click should be heard.',
            'FMI 6 (current too high): a short to ground or plus in the solenoid circuit. Disconnect the solenoid and see if the code clears.',
            'Check the air supply to the pneumatic solenoid: without pressure the lock will not engage.',
        ],
        'причины': [
            'Broken wire to the solenoid.',
            'Short to ground in the solenoid circuit.',
            'Pneumatic solenoid or its air supply.',
            'Unit output overloaded.',
        ],
    },

    569: {
        'узел': 'State of the rear axle 1 differential lock. The code refers to the lock relay circuit of this axle.',
        'нормы': [
            ('Lock relay current when engaging and disengaging', 'within the working range — per the manufacturer\'s manual'),
            ('Lock state in the cab and in diagnostics', 'match'),
        ],
        'шаги': [
            'FMI 5 (relay current below normal or open circuit): check the relay and its connector. When the lock is engaged the relay '
            'should click; if not — check the relay supply and the wire to the unit.',
            'FMI 6 (relay current too high): check for a short to ground or to plus in the relay circuit.',
            'Check the mechanism of the axle lock.',
        ],
        'причины': [
            'Broken wire to the lock relay.',
            'Short to ground in the relay circuit.',
            'Sticking lock mechanism.',
            'Faulty relay.',
        ],
    },

    570: {
        'узел': 'State of the rear axle 2 differential lock. The code refers to the lock relay circuit of this axle.',
        'нормы': [
            ('Lock relay current when engaging and disengaging', 'within the working range — per the manufacturer\'s manual'),
            ('Lock state in the cab and in diagnostics', 'match'),
        ],
        'шаги': [
            'FMI 5 (relay current below normal or open circuit): check the relay and its connector. When the lock is engaged the relay '
            'should click; if not — check the relay supply and the wire to the unit.',
            'FMI 6 (relay current too high): check for a short to ground or to plus in the relay circuit.',
            'Check the mechanism of the axle lock.',
        ],
        'причины': [
            'Broken wire to the lock relay.',
            'Short to ground in the relay circuit.',
            'Sticking lock mechanism.',
            'Faulty relay.',
        ],
    },

    573: {
        'узел': 'Torque converter lock of the gearbox: the signal that the lock is engaged. The engine ECU gets it over the CAN bus '
                'and takes it into account when calculating the load.',
        'нормы': [
            ('Lock message on the bus', 'arrives regularly — check by diagnostics'),
            ('Lock state during acceleration and shifting', 'changes with the mode — check by diagnostics'),
        ],
        'шаги': [
            'FMI 9 (message intermittent): check the CAN bus and the gearbox unit. Disconnect the units one at a time.',
            'FMI 19 (invalid data): check the software versions of the gearbox and engine units.',
            'Check the power and ground of the gearbox unit.',
        ],
        'причины': [
            'Intermittent CAN bus.',
            'Lost power or ground of the gearbox unit.',
            'Faulty gearbox unit.',
            'Mismatched software versions of the units.',
        ],
    },

    574: {
        'узел': 'Signal that the gearbox is shifting a gear right now. The engine ECU gets it over the CAN bus and changes the '
                'engine operating mode for the time of the shift.',
        'нормы': [
            ('Shift message on the bus', 'arrives regularly — check by diagnostics'),
            ('Signal during a shift', 'appears during the shift and clears after — check by diagnostics'),
        ],
        'шаги': [
            'FMI 9 (message intermittent): check the CAN bus and the gearbox unit. Disconnect the units one at a time.',
            'FMI 19 (invalid data): check the software versions of the gearbox and engine units.',
            'Check the power and ground of the gearbox unit.',
        ],
        'причины': [
            'Intermittent CAN bus.',
            'Lost power or ground of the gearbox unit.',
            'Faulty gearbox unit.',
            'Mismatched software versions of the units.',
        ],
    },

    601: {
        'узел': 'Cruise control resume/set switch on the steering-column switch. The signal goes over wires or over CAN to the engine '
                'ECU. Pressing CC+ and CC− together is an error.',
        'нормы': [
            ('Switch state when pressed and released', 'changes without jumps — check by diagnostics'),
            ('CC+ and CC− pressed together', 'gives no valid signal — an error'),
        ],
        'шаги': [
            'FMI 9, 19 (CAN message intermittent or invalid): check the CAN bus from the steering-column switch to the ECU. '
            'Disconnect the units one at a time.',
            'FMI 12, 14 (both buttons pressed or signal invalid): inspect the steering-column switch and its wiring, and check '
            'whether the button sticks.',
            'FMI 4 (cruise control handle, signals R/+ and S/- at the same time): check the handle and its connections.',
        ],
        'причины': [
            'Sticking or worn switch button.',
            'Chafed wiring in the steering column.',
            'Intermittent CAN bus.',
            'Faulty cruise control unit.',
        ],
    },

    608: {
        'узел': 'J1587 bus (formerly SAE J1708): the older data bus of the truck, on which the units exchange messages, including with the '
                'switches. The code means the bus is lost or shorted.',
        'нормы': [
            ('Link to the units over the bus', 'all units respond — check by diagnostics'),
            ('Resistance between the bus lines with the power off', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 9 (bus lost): check which units are silent. One silent unit — its connector and power. All silent — the bus '
            'itself and its connector.',
            'FMI 8 (bus line shorted to plus): switch the ignition off, disconnect the units one at a time and see if the short clears.',
            'Inspect the bus harness at bends and at the connectors.',
        ],
        'причины': [
            'Broken or shorted bus line.',
            'Corroded connector on the bus.',
            'Faulty unit that shorts the bus.',
            'Extra equipment tapped into the bus.',
        ],
    },

    620: {
        'узел': 'Analogue 5 V supply: the ECU supplies it to the sensors, including the accelerator pedal sensor. If the voltage '
                'goes above or below normal, all sensors on this line give wrong readings.',
        'нормы': [
            ('5 V supply voltage at the connector, ignition on', '5.0 V ± 0.25; above 5.2 V is a fault per the site data'),
            ('Accelerator pedal supply voltage (contact AFP+)', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (voltage above 5.2 V, short to plus): the 5 V line is shorted to plus (+24 V or another circuit). With the ignition '
            'off, check the 5 V wire from the unit to the sensors for continuity to the plus circuits, and inspect the harness for '
            'chafing where it runs alongside the +24 V wires.',
            'FMI 4 (accelerator pedal supply too low, short to ground): check the pedal connector and contact AFP+. Measure the voltage '
            'on the contact with the ignition on. If the voltage is low on the whole 5 V line — disconnect the sensors on the line one '
            'at a time: when the voltage comes back, the disconnected sensor is shorting the line to ground.',
            'If other 5 V sensor codes are active at the same time — the common supply line is the single fault.',
        ],
        'причины': [
            'Shorted sensor on the 5 V line.',
            'Corroded accelerator pedal connector.',
            'Broken supply wire to the sensors.',
            'Faulty ECU.',
        ],
    },

    623: {
        'узел': 'Red emergency stop lamp on the dash. The unit controls it and tells the driver to stop.',
        'нормы': [
            ('Lamp with the ignition on', 'lights and goes out on command from the unit — check by diagnostics'),
            ('Current in the lamp circuit', 'within the working range — per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 4 (voltage below normal or short to ground): check the lamp, its connector and the wire to the unit.',
            'FMI 5 (lamp fault, open circuit): check whether the lamp has burnt out or come loose. Check the wire from the unit to the lamp for continuity.',
            'FMI 6 (lamp circuit current too high): short to ground or to plus. Disconnect the lamp and see if the code clears.',
        ],
        'причины': [
            'Burnt-out lamp.',
            'Corroded lamp connector.',
            'Shorted lamp wiring.',
            'Faulty lamp control in the unit.',
        ],
    },

    631: {
        'узел': 'Calibration module: the EECU stores the production parameters and calibration data in its memory. The code means the '
                'parameters were not applied or the unit memory is faulty.',
        'нормы': [
            ('Unit parameters matched to the vehicle production data', 'applied — check by diagnostics'),
            ('Memory check at power-up', 'passes with no errors — check by diagnostics'),
        ],
        'шаги': [
            'FMI 5 (production parameters not applied): apply the parameters to the unit from the vehicle data. Without the parameters '
            'the unit will not run in normal mode.',
            'FMI 11, 13 (internal fault of the unit): read the codes, clear them and check whether the code returns. If it does — '
            'the unit per the manual.',
            'FMI 14 (EEPROM check failed): the unit must be replaced per the manual; check the power supply before replacing it.',
        ],
        'причины': [
            'Incomplete parameter setup after a unit replacement.',
            'Internal memory fault of the EECU.',
            'Voltage dips while the parameters are written.',
        ],
    },

    647: {
        'узел': 'Fan clutch control output: the unit controls the clutch through the drive circuit. The code refers to the wiring and to '
                'the fan clutch itself, so the connector and the hub are checked first.',
        'нормы': [
            ('Output voltage with the fan on and off', 'from 0 V to the battery voltage — check by diagnostics'),
            ('Clutch coil resistance', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (short to plus or open, with the fan off): check the fan hub and the clutch connector. Disconnect the clutch and measure '
            'the voltage on the wire against ground — there should be no plus.',
            'FMI 4 (short to ground, with the fan on): disconnect the clutch and see if the code clears. If it clears — the wiring to the clutch; if not — the clutch itself.',
            'FMI 5 (open circuit): check the wire from the unit to the clutch for continuity and check the fan electrical components.',
        ],
        'причины': [
            'Corroded clutch or fan hub connector.',
            'Wiring shorted to ground or plus.',
            'Fan clutch coil.',
            'Control output of the ECU.',
        ],
    },

    650: {
        'узел': 'Main power relay of the drive electronic unit. The unit gets its power through it, and it must close when the ignition '
                'is switched on. The code means the relay does not close or closes at the wrong time.',
        'нормы': [
            ('Relay when the ignition is switched on', 'closes — check by diagnostics'),
            ('Output of the relay with the ignition on', 'equal to the battery voltage — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (short to plus): check the insulation of the cable connections against the battery plus. Disconnect the relay and see if the code clears.',
            'FMI 4 (open circuit or short to ground): check the wire to the relay and from the relay to the unit. Check for continuity to ground.',
            'FMI 5 (open circuit): when the ignition is switched on, the relay must close — check its control and coil.',
            'FMI 7 (relay stuck closed or open): check the fuse and the relay operation. A relay stuck in either position is replaced per the manufacturer\'s manual.',
        ],
        'причины': [
            'Burnt relay contacts.',
            'Relay wires shorted to plus or ground.',
            'Broken relay wires.',
            'Faulty power fuse of the unit.',
        ],
    },

    697: {
        'узел': 'Proportional valve of PWM driver group 1: the unit controls it with a PWM signal. The code refers to the valve circuit: '
                'power, ground, open circuit.',
        'нормы': [
            ('Valve coil resistance with the power off', 'per the manufacturer\'s manual'),
            ('PWM signal at the valve on command from the unit', 'appears on command — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (short to plus or open circuit): disconnect the valve connector. With the ignition on, measure the voltage on the '
            'contacts against ground — there should be no plus.',
            'FMI 4 (short to ground): disconnect the valve and see if the code clears. Cleared — the wiring; not cleared — the valve.',
            'FMI 5 (open circuit): check the wire from the unit to the valve and back for continuity.',
            'FMI 6 (valve 1 shorted to ground): inspect the wire for chafing and check the valve itself.',
        ],
        'причины': [
            'Corroded valve connector.',
            'Wiring shorted to ground or plus.',
            'Valve coil.',
            'Output stage of the ECU.',
        ],
    },

    698: {
        'узел': 'Proportional valve of PWM driver group 2: the unit controls it with a PWM signal. The code refers to the valve circuit: '
                'power, ground, open circuit.',
        'нормы': [
            ('Valve coil resistance with the power off', 'per the manufacturer\'s manual'),
            ('PWM signal at the valve on command from the unit', 'appears on command — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (short to battery plus): disconnect the valve connector. With the ignition on, measure the voltage on the contacts '
            'against ground — there should be no plus.',
            'FMI 5 (open circuit of group 2): check the wire from the unit to the valve and back for continuity.',
            'FMI 6 (valve 2 shorted to ground): disconnect the valve and see if the code clears.',
        ],
        'причины': [
            'Corroded valve connector.',
            'Wiring shorted to plus or ground.',
            'Valve coil.',
            'Output stage of the ECU.',
        ],
    },

    699: {
        'узел': 'Proportional valve of PWM driver group 3: the unit controls it with a PWM signal. The code refers to the valve circuit: '
                'power, ground, open circuit.',
        'нормы': [
            ('Valve coil resistance with the power off', 'per the manufacturer\'s manual'),
            ('PWM signal at the valve on command from the unit', 'appears on command — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (short to battery plus): disconnect the valve connector. With the ignition on, measure the voltage on the contacts '
            'against ground — there should be no plus.',
            'FMI 5 (open circuit of valve 3): check the wire from the unit to the valve and back for continuity.',
            'FMI 6 (valve 3 shorted to ground): disconnect the valve and see if the code clears.',
        ],
        'причины': [
            'Corroded valve connector.',
            'Wiring shorted to plus or ground.',
            'Valve coil.',
            'Output stage of the ECU.',
        ],
    },

    700: {
        'узел': 'Proportional valve of PWM driver group 4: the unit controls it with a PWM signal. The code refers to the valve circuit: '
                'power, ground, open circuit.',
        'нормы': [
            ('Valve coil resistance with the power off', 'per the manufacturer\'s manual'),
            ('PWM signal at the valve on command from the unit', 'appears on command — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (short to battery plus): disconnect the valve connector. With the ignition on, measure the voltage on the contacts '
            'against ground — there should be no plus.',
            'FMI 5 (open circuit of valve 4): check the wire from the unit to the valve and back for continuity.',
            'FMI 6 (valve 4 shorted to ground): disconnect the valve and see if the code clears.',
        ],
        'причины': [
            'Corroded valve connector.',
            'Wiring shorted to plus or ground.',
            'Valve coil.',
            'Output stage of the ECU.',
        ],
    },
}

_B = {
    707: {
        'узел': 'Digital output 2/10 of the control unit: it drives the CEL/AWL engine warning lamp. The unit switches the lamp '
                'through this output, so the code points to the lamp wiring or to the output itself.',
        'нормы': [
            ('Output voltage with the lamp on and off', 'from 0 V to the battery voltage — check by diagnostics'),
            ('Lamp at ignition-on', 'lights and goes out on command from the unit — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (short to plus): disconnect the lamp from the output and measure the voltage on the wire against ground — '
            'there should be no plus.',
            'FMI 4 (short to ground): with the lamp disconnected, the wire must not short to ground. Find the short along the harness.',
            'FMI 5 (open circuit, broken wire or disconnected pin): check the continuity of the wire from the unit to the lamp and the lamp connector.',
        ],
        'причины': [
            'Burnt-out or disconnected CEL/AWL lamp.',
            'Lamp wiring shorted to plus or ground.',
            'Broken wire or corroded connector.',
            'Output stage of the control unit.',
        ],
    },

    709: {
        'узел': 'Digital output 3/16 of the control unit: the unit switches a load through it (relay, valve, lamp). The code points to '
                'the wiring of this output and to the load connected to it.',
        'нормы': [
            ('Output voltage with the load on and off', 'from 0 V to the battery voltage — check by diagnostics'),
            ('Load resistance at the output', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (short to plus): disconnect the load from the output and measure the voltage on the wire against ground.',
            'FMI 4 (short to ground): with the load disconnected, the wire must not short to ground. Find the short along the harness.',
            'FMI 5 (open circuit): check the wire from the unit to the load and the load connector for continuity.',
        ],
        'причины': [
            'Load wiring shorted to plus or ground.',
            'Broken wire or corroded connector.',
            'Faulty load (relay, valve, lamp).',
            'Output stage of the control unit.',
        ],
    },

    710: {
        'узел': 'Digital output 4/06 of the control unit: the unit switches a load through it. The code points to the wiring of this '
                'output and to the load connected to it.',
        'нормы': [
            ('Output voltage with the load on and off', 'from 0 V to the battery voltage — check by diagnostics'),
            ('Load resistance at the output', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (short to plus): disconnect the load from the output and measure the voltage on the wire against ground.',
            'FMI 4 (short to ground): with the load disconnected, the wire must not short to ground. Find the short along the harness.',
            'FMI 5 (open circuit): check the wire from the unit to the load and the load connector for continuity.',
        ],
        'причины': [
            'Load wiring shorted to plus or ground.',
            'Broken wire or corroded connector.',
            'Faulty load (relay, valve, lamp).',
            'Output stage of the control unit.',
        ],
    },

    711: {
        'узел': 'Digital output 1/05 of the control unit: the unit switches a load through it. The code points to the wiring of this '
                'output and to the load connected to it.',
        'нормы': [
            ('Output voltage with the load on and off', 'from 0 V to the battery voltage — check by diagnostics'),
            ('Load resistance at the output', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (short to plus): disconnect the load from the output and measure the voltage on the wire against ground.',
            'FMI 4 (short to ground): with the load disconnected, the wire must not short to ground. Find the short along the harness.',
            'FMI 5 (open circuit): check the wire from the unit to the load and the load connector for continuity.',
        ],
        'причины': [
            'Load wiring shorted to plus or ground.',
            'Broken wire or corroded connector.',
            'Faulty load (relay, valve, lamp).',
            'Output stage of the control unit.',
        ],
    },

    712: {
        'узел': 'Digital output 1/04 of the control unit: the unit switches a load through it. The code points to the wiring of this '
                'output and to the load connected to it.',
        'нормы': [
            ('Output voltage with the load on and off', 'from 0 V to the battery voltage — check by diagnostics'),
            ('Load resistance at the output', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (short to plus): disconnect the load from the output and measure the voltage on the wire against ground.',
            'FMI 4 (short to ground): with the load disconnected, the wire must not short to ground. Find the short along the harness.',
            'FMI 5 (open circuit): check the wire from the unit to the load and the load connector for continuity.',
        ],
        'причины': [
            'Load wiring shorted to plus or ground.',
            'Broken wire or corroded connector.',
            'Faulty load (relay, valve, lamp).',
            'Output stage of the control unit.',
        ],
    },

    715: {
        'узел': 'Frequency output 4/12 of the control unit: the unit sends pulses to a load at a frequency it sets itself. The code '
                'points to the wiring of this output and to the pulse receiver.',
        'нормы': [
            ('Pulses at the output in operation', 'present at the set frequency — check by diagnostics'),
            ('Load resistance at the output', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (short to plus): disconnect the pulse receiver and measure the voltage on the wire against ground.',
            'FMI 4 (short to ground): with the receiver disconnected, the wire must not short to ground. Find the short along the harness.',
            'FMI 5 (open circuit): check the wire from the unit to the receiver for continuity.',
        ],
        'причины': [
            'Receiver wiring shorted to plus or ground.',
            'Broken wire or corroded connector.',
            'Faulty pulse receiver.',
            'Output stage of the control unit.',
        ],
    },

    811: {
        'узел': 'ABS warning lamp on the dash. The ABS control unit or the lamp relay switches it on when the brake system has a fault.',
        'нормы': [
            ('ABS lamp at ignition-on', 'lights and goes out after the check — check by diagnostics'),
            ('Lamp circuit with the lamp off', 'no short to ground — check by diagnostics'),
        ],
        'шаги': [
            'FMI 2 (ABS lamp circuit fault on the dash): check the lamp, its connector and the wire to the dash.',
            'FMI 5 (short to ground or burnt-out lamp, per the other brand row): disconnect the lamp and see if the short clears. '
            'A short to ground is the wiring; a burnt lamp is the lamp.',
            'Check the warning lamp relay and its supply against the wiring diagram.',
        ],
        'причины': [
            'Burnt-out lamp on the dash.',
            'Lamp wiring shorted to ground.',
            'Corroded dash connector.',
            'Warning lamp relay.',
        ],
    },

    870: {
        'узел': 'Urea (AdBlue) injector heater in the SCR system. It switches on in the cold so that the urea in the injector does not freeze. '
                'The code refers to the heater circuit.',
        'нормы': [
            ('Injector heater resistance with the power off', 'per the manufacturer\'s manual'),
            ('Heater with the engine cold', 'switches on on command from the unit — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (short to plus or open circuit): check the heater wire; when switched on, measure the voltage on the contacts.',
            'FMI 4 (short to ground): disconnect the heater and see if the code clears. Cleared — the wiring; not cleared — the heater.',
            'FMI 5 (open circuit): check the wire from the unit to the heater and back for continuity.',
        ],
        'причины': [
            'Corroded injector or heater connector.',
            'Wiring shorted to ground or plus.',
            'Broken heater wire.',
            'The injector heater itself.',
        ],
    },

    924: {
        'узел': 'Additional output 1: digital output 4/09 of the control unit. The unit switches a load through it. The code points '
                'to the wiring of this output or to the load on it.',
        'нормы': [
            ('Output voltage with the load on and off', 'from 0 V to the battery voltage — check by diagnostics'),
            ('Load resistance at the output', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (short to plus): disconnect the load from the output and measure the voltage on the wire against ground.',
            'FMI 4 (short to ground): with the load disconnected, the wire must not short to ground.',
            'FMI 5 (open wire or disconnected pin): check the wire from the unit to the load for continuity.',
        ],
        'причины': [
            'Load wiring shorted to plus or ground.',
            'Broken wire or disconnected pin.',
            'Faulty load.',
            'Output stage of the control unit.',
        ],
    },

    925: {
        'узел': 'Additional output 2: digital output 3/17 of the control unit (per the table of one brand), or the proportional '
                'valves of the SCR module (per the table of another brand). The unit switches the load through this output.',
        'нормы': [
            ('Output voltage with the load on and off', 'from 0 V to the battery voltage — check by diagnostics'),
            ('Valve or load resistance at the output', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (short to plus or open circuit): disconnect the load from the output and measure the voltage on the wire against ground.',
            'FMI 4 (short to ground): with the load disconnected, the wire must not short to ground. Find the short along the harness.',
            'FMI 5 (open wire): check the wire from the unit to the load for continuity.',
        ],
        'причины': [
            'Load wiring shorted to plus or ground.',
            'Broken wire or corroded connector.',
            'Faulty load (valve, relay).',
            'Output stage of the control unit.',
        ],
    },

    972: {
        'узел': 'Accelerator pedal lock switch (limit switch). It tells the unit that the pedal is in its rest position and allows or blocks the '
                'fuel supply under certain conditions.',
        'нормы': [
            ('Switch state with the pedal pressed and released', 'changes — check by diagnostics'),
            ('Switch state when stationary and when driving', 'matches the pedal position — check by diagnostics'),
        ],
        'шаги': [
            'FMI 2 (switch fault or speed too high while the lock signal is present): check that the switch operates and its wiring. '
            'The speed must be taken from the unit data.',
            'FMI 6 (current too high in the lock indicator): a short to ground or to plus in the indicator — disconnect the indicator and see if the code clears.',
            'Check the pedal mechanism: the switch must not stick or operate late.',
        ],
        'причины': [
            'Faulty pedal limit switch.',
            'Shorted wiring of the lock indicator.',
            'Accelerator pedal mechanism.',
            'Unit that receives the lock signal.',
        ],
    },

    987: {
        'узел': 'Engine protection lamp (Check Engine). The control unit switches it on for engine and electronics faults, so the lamp '
                'alone does not show the cause.',
        'нормы': [
            ('Lamp at ignition-on', 'lights and goes out after the check — check by diagnostics'),
            ('Lamp circuit', 'no short to ground and no open circuit — check by diagnostics'),
        ],
        'шаги': [
            'FMI 5 (lamp fault, open circuit): check the lamp, its connector and the wire to the dash.',
            'FMI 3 (lamp circuit fault, Check Engine, P0650 per the site data): check that the wire is not shorted to plus; disconnect the '
            'lamp and see if the code clears.',
            'Read all the engine codes first: the lamp also comes on for other faults.',
        ],
        'причины': [
            'Burnt-out lamp on the dash.',
            'Lamp wiring shorted to plus.',
            'Corroded dash connector.',
            'Fault in the engine control unit.',
        ],
    },

    1043: {
        'узел': 'Internal 5 V sensor supply voltage: the ECU supplies it to the sensors, and it must be stable. The code means the voltage '
                'is above or below normal, or the sensor supply line is shorted.',
        'нормы': [
            ('Sensor supply voltage at the connector, ignition on', '5.0 V ± 0.25'),
            ('Supply voltage with one sensor disconnected from the line', 'stays at 5.0 V ± 0.25 — if it drops, a short is in the line'),
        ],
        'шаги': [
            'FMI 0, 1 (internal reference voltage above or below normal): disconnect the sensors from the 5 V line one at a time and watch '
            'the voltage. When it returns to normal, the disconnected sensor is shorting the line.',
            'FMI 2 (5 V supply fault, short to supply on the sensor): measure the voltage between the supply contacts of the unit connector '
            'and the sensor, and check for a short to plus.',
            'If other 5 V sensor codes are active at the same time — the common supply line is the single fault.',
        ],
        'причины': [
            'Shorted sensor on the 5 V line.',
            'Corroded sensor or unit connector.',
            'Short of the supply line to plus.',
            'Faulty control unit.',
        ],
    },

    1044: {
        'узел': 'Hydraulic pump electric motor: the drive of the pump that builds pressure in the hydraulic system of the vehicle. '
                'The control unit switches it on command, and the code refers to the power supply and current of the motor.',
        'нормы': [
            ('Motor voltage with the pump running', 'close to the battery voltage — check by diagnostics'),
            ('Motor current in operation', 'within the working range — per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (voltage above normal or short to the high-voltage circuit): measure the motor terminal voltage with the pump running and on its power wire.',
            'FMI 4 (voltage below normal or short to the low-voltage circuit): check the battery terminals, the power wire and the motor ground.',
            'FMI 5 (current below normal or open circuit): check the motor connector, the contacts and the power wire for an open circuit.',
        ],
        'причины': [
            'Corroded terminals or power wire.',
            'Poor motor ground.',
            'Worn motor brushes or contacts.',
            'Control unit that sends the command.',
        ],
    },

    1047: {
        'узел': 'Electronic pressure control, axle 1: the front EBS module that regulates the pressure in the front-axle pneumatic circuit. '
                'The code refers to the module, its link to the EBS unit and the air circuit.',
        'нормы': [
            ('Link from the front module to the EBS unit over the internal bus', 'without interruptions — check by diagnostics'),
            ('Pressure in the front-axle circuit', 'matches the gauge and the diagnostics'),
        ],
        'шаги': [
            'FMI 2, 7 (pneumatic circuit or module fault): check the front-axle circuit for leaks with soapy water and check the pressure with a gauge.',
            'FMI 9 (no link between the module and the EBS unit): check the 4 wires between the EBS unit and the module for continuity.',
            'FMI 12, 13 (internal module fault or incompatibility): clear the codes; if it returns — replace the module per the manual.',
        ],
        'причины': [
            'Leak in the front-axle pneumatic circuit.',
            'Broken or corroded wires of the internal bus.',
            'Faulty control module.',
            'Wrong module marking after replacement.',
        ],
    },

    1050: {
        'узел': 'Electronic pressure control, axle 2: the rear EBS module that regulates the pressure in the rear-axle pneumatic circuit. '
                'The code refers to the module, its link to the EBS unit and the air circuit.',
        'нормы': [
            ('Link from the rear module to the EBS unit over the internal bus', 'without interruptions — check by diagnostics'),
            ('Pressure in the rear-axle circuit', 'matches the gauge and the diagnostics'),
        ],
        'шаги': [
            'FMI 2, 7 (pneumatic circuit or module fault): check the rear-axle circuit for leaks with soapy water and check the pressure with a gauge.',
            'FMI 9 (no link between the module and the EBS unit): check the 4 wires between the EBS unit and the module for continuity.',
            'FMI 12, 13 (internal module fault or incompatibility): clear the codes; if it returns — replace the module per the manual.',
        ],
        'причины': [
            'Leak in the rear-axle pneumatic circuit.',
            'Broken or corroded wires of the internal bus.',
            'Faulty control module.',
            'Wrong module marking after replacement.',
        ],
    },

    1053: {
        'узел': 'Electronic pressure control, axle 3: the additional-axle EBS module that regulates the pressure in the pneumatic circuit of '
                'this axle. The code refers to the module, its link to the EBS unit and the air circuit.',
        'нормы': [
            ('Link from the additional-axle module to the EBS unit over the internal bus', 'without interruptions — check by diagnostics'),
            ('Pressure in the additional-axle circuit', 'matches the gauge and the diagnostics'),
        ],
        'шаги': [
            'FMI 2, 7 (pneumatic circuit or module fault): check the circuit for leaks with soapy water and check the pressure with a gauge.',
            'FMI 9 (no link between the module and the EBS unit): check the 4 wires between the EBS unit and the module for continuity.',
            'FMI 12, 13 (internal module fault or incompatibility): clear the codes; if it returns — replace the module per the manual.',
        ],
        'причины': [
            'Leak in the additional-axle pneumatic circuit.',
            'Broken or corroded wires of the internal bus.',
            'Faulty control module.',
            'Wrong module marking after replacement.',
        ],
    },

    1086: {
        'узел': 'Air pressure sensor in the third pneumatic circuit (parking brake or trailer). The brake unit uses it to monitor the '
                'pressure in this circuit.',
        'нормы': [
            ('Pressure in the circuit by gauge and by the sensor', 'match, within the manual tolerance'),
            ('Sensor reference voltage, ignition on', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 4 (sensor circuit shorted to ground): disconnect the sensor. If the code clears — the wiring to the sensor; if not — the sensor itself.',
            'FMI 5 (sensor circuit open): check the signal and ground wires from the sensor connector to the unit for continuity.',
            'FMI 7 (mechanical system not holding pressure: leak, valve or circuit): compare with a gauge in the circuit. If the gauge '
            'shows the pressure falling — look for the leak with soapy water on the pipes, fittings and valves. If the gauge holds the '
            'pressure and the sensor reads wrongly — the sensor or its connector.',
        ],
        'причины': [
            'Open circuit or short to ground in the sensor wiring.',
            'Corroded sensor connector.',
            'Leak in the parking brake or trailer circuit.',
            'The air pressure sensor itself.',
        ],
    },

    1184: {
        'узел': 'Turbine outlet temperature sensor. The control unit uses it to monitor turbine heating. High temperature after the turbine is '
                'usually linked to load and operating mode, not to the sensor.',
        'нормы': [
            ('Sensor signal with the engine off', 'close to the outside air temperature — check by diagnostics'),
            ('Temperature after the turbine under load', 'rises with engine load — check by diagnostics'),
        ],
        'шаги': [
            'FMI 0 (temperature too high): first find out why the turbine is hot: load, regeneration, air ingress. The sensor is checked only after that.',
            'FMI 2 (signal invalid): wiggle the harness with the engine running and watch the value. If it jumps — poor contact.',
            'FMI 3, 4 (short to plus or open circuit; short to ground): disconnect the connector, inspect the contacts; with the ignition on, '
            'measure the voltage on the signal wire against ground. Plus or zero — the wiring; a normal value — the sensor.',
        ],
        'причины': [
            'Overload or long filter regeneration.',
            'Air leak or exhaust leak at the turbine.',
            'Corroded sensor connector.',
            'The temperature sensor itself.',
        ],
    },

    1195: {
        'узел': 'Anti-theft password validation indicator: the engine control unit and the anti-theft unit exchange the key confirmation. '
                'The code means the key is not recognised or the link to the anti-theft unit is lost.',
        'нормы': [
            ('Anti-theft indicator at ignition-on', 'lights for 3 seconds and goes out if the key is recognised'),
            ('Link to the anti-theft unit with the ignition on', 'present — check by diagnostics'),
        ],
        'шаги': [
            'FMI 2 (immobiliser not switched off, or engine locked by the anti-theft system): insert the key and switch on again; check '
            'that the indicator goes out after recognition.',
            'FMI 8 (anti-theft unit, no communication): check the wires (SL1/16, SL1/17) and the connectors for continuity and insulation.',
            'FMI 12 (coding or software matching error of the lock): run the full key recognition cycle by diagnostics. If it returns — the unit per the manual.',
        ],
        'причины': [
            'Key not recognised or incorrectly programmed.',
            'Broken or corroded anti-theft unit wires.',
            'Faulty anti-theft unit or lock.',
            'Flat battery in the key.',
        ],
    },

    1243: {
        'узел': 'ABS fully operational signal: the gearbox unit and the engine unit get it from the ABS unit. If ABS works '
                'partially, the unit limits the automatic gear selection.',
        'нормы': [
            ('ABS signal on the bus with the system working', 'present, no interruptions — check by diagnostics'),
            ('ABS lamp at ignition-on', 'lights and goes out after the check — check by diagnostics'),
        ],
        'шаги': [
            'FMI 14 (automatic gear selection limited because of an ABS fault): read and clear the ABS codes first.',
            'FMI 12 (ABS not working fully): check the wheel speed sensors and their connectors; check the ABS codes by diagnostics.',
            'Check the power and ground of the ABS unit and the CAN link between the units.',
        ],
        'причины': [
            'Faulty wheel speed sensor.',
            'Corroded ABS sensor connectors.',
            'Broken or kinked CAN wire.',
            'Faulty ABS unit.',
        ],
    },

    1378: {
        'узел': 'Oil change interval: the control unit counts the running time and warns about an engine oil change. The "change oil" lamp '
                'lights on command from the unit.',
        'нормы': [
            ('Change interval per the service programme', 'per the manufacturer\'s manual'),
            ('Interval reset after an oil change', 'done by diagnostics right after the change'),
        ],
        'шаги': [
            'FMI 31 (engine oil change required): check the service log. If the oil was changed — reset the interval by diagnostics.',
            'FMI 4, 6 ("change oil" lamp): check the lamp, its connector and the wire to the unit. A short to ground or to plus is the wiring.',
            'If the interval resets by itself — check the power supply of the unit.',
        ],
        'причины': [
            'Interval not reset after the oil change.',
            'Burnt-out lamp or its wiring.',
            'Interval entered incorrectly per the service programme.',
        ],
    },

    1387: {
        'узел': 'Urea (AdBlue) pressure sensor in the dosing line of the SCR system. The control unit uses it to check that the urea is '
                'supplied at the right pressure.',
        'нормы': [
            ('Sensor reference voltage, ignition on (three-wire sensor)', '5.0 V ± 0.25'),
            ('Pressure in the line with the system working', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 2 (signal out of range or invalid): check the line pressure by diagnostics and look for leaks at the connections with soapy water.',
            'FMI 3 (short to plus or open circuit): disconnect the connector and the sensor and see whether the signal at the unit disappears.',
            'FMI 4 (short to ground): check the signal wire to the unit for a short to ground; with the sensor disconnected the short clears.',
        ],
        'причины': [
            'Leak or blockage in the urea line.',
            'Corroded sensor connector.',
            'Wiring shorted to plus or ground.',
            'The urea pressure sensor itself.',
        ],
    },

    1390: {
        'узел': 'Absolute fuel pressure sensor at the input of fuel valve 1 (metering valve). The control unit uses it to regulate the fuel '
                'supply. Low pressure at the input is most often caused by the filters and the feed pump.',
        'нормы': [
            ('Sensor reference voltage (three-wire sensor), ignition on', '5.0 V ± 0.25'),
            ('Fuel pressure at the input with the engine running', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 0, 1 (signal above or below the working range): unplug the sensor connector and inspect the contacts. With the ignition on, '
            'measure the reference voltage and the signal against ground.',
            'FMI 17 (fuel pressure at the input too low): check the level, the filters and the feed pump, and air in the line. Check the sensor only after the fuel.',
            'Inspect the pipes and connections for air ingress: bubbles or ingress give a low pressure.',
        ],
        'причины': [
            'Blocked fuel filters.',
            'Air ingress on the suction side.',
            'Corroded sensor connector.',
            'Faulty fuel feed pump.',
        ],
    },

    1548: {
        'узел': 'Air temperature sensor in the heater or air-conditioning duct, at the heater outlet. The control unit uses it to regulate the '
                'cab temperature.',
        'нормы': [
            ('Sensor signal with the engine off', 'close to the duct temperature — check by diagnostics'),
            ('Heater outlet temperature in operation', 'changes with the mode — check by diagnostics'),
        ],
        'шаги': [
            'FMI 0, 1 (sensor reading above or below normal): compare with the cab temperature and the heater outlet; a normal temperature points to the sensor.',
            'FMI 3 (sensor voltage too high): disconnect the sensor and see whether the high voltage at the unit disappears.',
            'FMI 4 (sensor voltage too low): check the signal wire for a short to ground and the sensor connector.',
        ],
        'причины': [
            'Corroded sensor connector.',
            'Signal wire shorted to plus or ground.',
            'The duct temperature sensor itself.',
            'Climate control unit.',
        ],
    },

    1590: {
        'узел': 'Adaptive cruise control mode: the adaptive cruise unit reports its state to the engine unit over the CAN bus. Without the message '
                'the engine unit does not know whether adaptive cruise is working and what gap is set.',
        'нормы': [
            ('Adaptive cruise message on the bus', 'arrives regularly — check by diagnostics'),
            ('System state at switch-on', 'changes on driver command — check by diagnostics'),
        ],
        'шаги': [
            'FMI 9 (message not arriving): check the adaptive cruise unit and the CAN bus. Disconnect the units one at a time.',
            'FMI 0 (state error on the CAN bus): check the bus and the adaptive cruise unit; a loss of link switches off some functions.',
            'FMI 19 (ACC1 frame length wrong on the bus): check the software versions of the units; a protocol mismatch means the software.',
        ],
        'причины': [
            'Intermittent or broken CAN bus.',
            'Lost power to the adaptive cruise unit.',
            'Faulty adaptive cruise unit.',
            'Mismatched software versions of the units.',
        ],
    },

    1633: {
        'узел': 'Cruise control pause switch on the steering-column switch. The signal goes over CAN to the engine unit.',
        'нормы': [
            ('Switch state when pressed and released', 'changes without jumps — check by diagnostics'),
            ('Message from the switch on the bus', 'arrives regularly — check by diagnostics'),
        ],
        'шаги': [
            'FMI 9, 19 (message intermittent or invalid): check the CAN bus from the steering-column switch to the unit. Disconnect the units one at a time.',
            'FMI 14 (signal invalid): check the wiring of the steering-column switch and whether the pause button sticks.',
        ],
        'причины': [
            'Sticking or worn pause button.',
            'Chafed wiring in the steering column.',
            'Intermittent CAN bus.',
            'Faulty cruise control unit.',
        ],
    },

    1810: {
        'узел': 'Longitudinal acceleration sensor, fitted in the stability control unit. The unit uses it to estimate acceleration and '
                'braking of the vehicle. A fault in the sensor affects ESP and ABS.',
        'нормы': [
            ('Sensor signal with the vehicle standing on level ground', 'close to zero after calibration — check by diagnostics'),
            ('Sensor signal under acceleration and braking', 'changes with the acceleration — check by diagnostics'),
        ],
        'шаги': [
            'FMI 0 (zero offset of the sensor): calibrate the sensor by diagnostics on level ground.',
            'FMI 1 (signal does not change under load): check the sensor mounting and its electrical connection.',
            'FMI 7 (sensor installed incorrectly): check the sensor position per the manual; a wrong fitting gives false readings.',
            'FMI 2, 12 (readings invalid or the module reports a sensor fault): check the sensor connector and the unit supply.',
        ],
        'причины': [
            'Zero offset or wrong sensor fitting.',
            'Loose sensor mounting.',
            'Corroded sensor connector.',
            'Faulty stability control unit.',
        ],
    },

    1814: {
        'узел': 'VDC fully operational signal: the stability control system reports the state of its J1939 messages to the engine unit. '
                'Without the message the engine unit limits the torque.',
        'нормы': [
            ('VDC1 message on the bus', 'arrives regularly — check by diagnostics'),
            ('Frame length on the bus', 'matches the specification — per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 9 (VDC1 message not arriving): check the stability control unit, the CAN bus and the unit supply. Disconnect the units one at a time.',
            'FMI 4 (TSC1AE frame length wrong): check the software versions of the ESP unit and the engine unit — the frame depends on the software.',
        ],
        'причины': [
            'Broken or kinked CAN wire.',
            'Lost power to the stability control unit.',
            'Mismatched software versions of the units.',
            'Faulty stability control unit.',
        ],
    },

    1845: {
        'узел': 'Gearbox torque limit: the gearbox unit sends the engine unit its configuration and torque limit over J1939 (TCFG2 message). '
                'Without it the engine unit does not know how much torque the gearbox can transmit.',
        'нормы': [
            ('TCFG2 message on the bus', 'arrives regularly — check by diagnostics'),
            ('Gearbox configuration in diagnostics', 'matches the fitted gearbox — per the manual'),
        ],
        'шаги': [
            'FMI 9, 12 (TCFG2 message not arriving, timeout): check the CAN bus and the gearbox unit. Disconnect the units one at a time '
            'and see if the message returns.',
            'FMI 2 (message failed the SAE J1939 check): check the software versions of the gearbox and engine units.',
            'Check the power and ground of the gearbox unit.',
        ],
        'причины': [
            'Intermittent or broken CAN bus.',
            'Lost power to the gearbox unit.',
            'Mismatched software versions of the units.',
            'Faulty gearbox unit.',
        ],
    },

    1908: {
        'узел': 'SCR air shut-off valve: it cuts off the air supply for urea dosing. The code refers to the valve circuit.',
        'нормы': [
            ('Valve coil resistance with the power off', 'per the manufacturer\'s manual'),
            ('Valve on command from the unit', 'operates — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (short to plus or open circuit): disconnect the valve connector; with the ignition on, measure the voltage on the contacts against ground.',
            'FMI 4 (short to ground): disconnect the valve and see if the code clears. Cleared — the wiring; not cleared — the valve.',
            'FMI 5 (open circuit): check the wire from the unit to the valve and back for continuity.',
        ],
        'причины': [
            'Corroded valve connector.',
            'Wiring shorted to ground or plus.',
            'Valve coil.',
            'Output stage of the control unit.',
        ],
    },

    2011: {
        'узел': 'Network address 11 on the J1939 bus: messages from the unit at this address have stopped arriving. In the table of one brand, '
                'address 11 belongs to the ABS unit. Check the unit that sits on address 11 in your vehicle.',
        'нормы': [
            ('Messages from the address on the bus', 'arrive regularly — check by diagnostics'),
            ('Power and ground of the unit at this address', 'within the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 9 (no messages from the address): read the codes of all units. If one unit is silent — check its power, ground and bus connector.',
            'If several units are silent — the CAN bus: kinks, breaks, corroded connectors.',
            'Disconnect the units one at a time and see whether the message from the address returns.',
        ],
        'причины': [
            'Lost power or ground of the unit at this address.',
            'Broken or kinked CAN wire.',
            'Faulty unit that does not respond on the bus.',
            'Unit addresses mismatched after a replacement.',
        ],
    },

    2581: {
        'узел': 'Electric motor of the hydraulic brake circuit 2 pump. The pump builds the pressure for the brakes. The code refers to the relay '
                'and the power supply of the pump motor, not to the pressure itself.',
        'нормы': [
            ('Voltage at the relay when the pump is switched on', 'present — check by diagnostics'),
            ('Pump motor on command from the unit', 'switches on and off on command — check by diagnostics'),
        ],
        'шаги': [
            'FMI 12 (no voltage at the relay): check the relay fuse, the supply and the control wire of the relay.',
            'FMI 5 (no power to the pump motor): measure the voltage at the motor terminals on the command to switch on.',
            'FMI 3, 4 (pump runs when it should not, or does not start): check the relay and its contacts; a stuck relay is replaced.',
            'FMI 7 (motor does not turn): check the motor and its terminals for corrosion; if it does not turn — the motor.',
        ],
        'причины': [
            'Blown fuse of the pump relay.',
            'Stuck or burnt relay contacts.',
            'Corroded motor terminals.',
            'Faulty pump motor.',
        ],
    },

    2584: {
        'узел': 'Brake hydraulic pressure warning, circuit 1. The sensor or switch of this circuit tells the unit that the pressure is below normal, '
                'and the unit switches on the warning on the dash.',
        'нормы': [
            ('Warning state at ignition-on', 'lights and goes out after the check — check by diagnostics'),
            ('Circuit 1 pressure by gauge', 'within the working range per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (voltage above normal or short to high): disconnect the connector and the sensor and see whether the signal at the unit disappears.',
            'FMI 4 (voltage below normal or short to low): check the signal wire for a short to ground and the connector.',
            'FMI 5 (current below normal or open circuit): check the wire from the unit to the sensor. At the same time check the circuit pressure with a gauge.',
        ],
        'причины': [
            'Leak in the brake hydraulic circuit.',
            'Corroded sensor connector.',
            'Open or shorted wiring.',
            'The circuit pressure sensor itself.',
        ],
    },

    2609: {
        'узел': 'Refrigerant pressure sensor at the cab air-conditioning compressor outlet. The climate control unit uses it to protect the system '
                'from high and low pressure.',
        'нормы': [
            ('Refrigerant pressure at the compressor outlet with the air conditioning on', 'within the working range — per the manufacturer\'s manual'),
            ('Sensor reference voltage, ignition on (three-wire sensor)', '5.0 V ± 0.25'),
        ],
        'шаги': [
            'FMI 0, 1 (sensor reading above or below normal): check the pressure with a gauge at the service ports per the manual; a difference points to the sensor.',
            'FMI 7 (service needed: fan fault or blocked pipe): inspect the condenser fan and the pipe.',
            'FMI 16 (high-pressure protection): check whether the condenser is blocked and whether the fan runs; let the system cool down.',
        ],
        'причины': [
            'Too little or too much refrigerant.',
            'Faulty condenser fan.',
            'Blocked condenser or pipe.',
            'The pressure sensor itself.',
        ],
    },

    2622: {
        'узел': 'Hill start assist system: the assist lamp and the solenoid of the system. The system holds the brake on a start on a slope. '
                'The code refers to the lamp, to the solenoid or to an active system fault.',
        'нормы': [
            ('Hill start assist lamp at ignition-on', 'lights and goes out after the check — check by diagnostics'),
            ('Solenoid on command from the system', 'operates — check by diagnostics'),
        ],
        'шаги': [
            'FMI 2, 5 (short to ground or open circuit of the lamp or solenoid): disconnect the solenoid and the lamp one at a time and see if the short clears.',
            'FMI 3, 13 (short to supply): disconnect the connectors and check the wires for a short to plus against ground.',
            'FMI 2 (active system fault, per the other brand row): read the codes of the system and fix the cause in the brakes.',
        ],
        'причины': [
            'Shorted solenoid wiring to ground or plus.',
            'Burnt-out assist lamp.',
            'Corroded solenoid connector.',
            'Faulty solenoid.',
        ],
    },

    2646: {
        'узел': 'Additional output 4: digital output 4/02 of the control unit. The unit switches a load through it. The code points to the '
                'wiring of this output or to the load on it.',
        'нормы': [
            ('Output voltage with the load on and off', 'from 0 V to the battery voltage — check by diagnostics'),
            ('Load resistance at the output', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (short to plus): disconnect the load from the output and measure the voltage on the wire against ground.',
            'FMI 4 (short to ground): with the load disconnected, the wire must not short to ground.',
            'FMI 5 (open wire or disconnected pin): check the wire from the unit to the load for continuity.',
        ],
        'причины': [
            'Load wiring shorted to plus or ground.',
            'Broken wire or disconnected pin.',
            'Faulty load.',
            'Output stage of the control unit.',
        ],
    },

    2797: {
        'узел': 'Injector group 1: the control unit switches the solenoids of the injectors in this group. The code refers to the power '
                'supply and the circuit of the injectors, and to the cylinder balance.',
        'нормы': [
            ('Injector coil resistance with the power off', 'per the manufacturer\'s manual'),
            ('Control pulse to the injector with the engine running', 'present on each cycle — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (short to plus or open circuit): disconnect the connectors of the group injectors; on command measure the voltage on the contacts.',
            'FMI 4 (short to ground): disconnect the injectors of the group one at a time and see if the code clears.',
            'FMI 5 (open circuit): check the wires from the unit to the injectors and back for continuity.',
            'FMI 9 (cylinder balance, no response in the set time): check the injectors of the group by cylinder balance in diagnostics.',
        ],
        'причины': [
            'Corroded injector connectors.',
            'Wiring shorted to plus or ground.',
            'Worn or stuck injector.',
            'Output of the control unit.',
        ],
    },

    2798: {
        'узел': 'Injector group 2: the control unit switches the solenoids of the injectors in this group. The code refers to the power supply '
                'and the circuit of the injectors.',
        'нормы': [
            ('Injector coil resistance with the power off', 'per the manufacturer\'s manual'),
            ('Control pulse to the injector with the engine running', 'present on each cycle — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (short to plus or open circuit): disconnect the connectors of the group injectors; on command measure the voltage on the contacts.',
            'FMI 4 (short to ground): disconnect the injectors of the group one at a time and see if the code clears.',
            'FMI 5 (open circuit): check the wires from the unit to the injectors and back for continuity.',
        ],
        'причины': [
            'Corroded injector connectors.',
            'Wiring shorted to plus or ground.',
            'Worn or stuck injector.',
            'Output of the control unit.',
        ],
    },

    2884: {
        'узел': 'Auxiliary engine speed governor switch. The signal goes from the switch over CAN to the engine unit; without the auxiliary '
                'messages the unit does not know whether the governor is on.',
        'нормы': [
            ('Auxiliary engine messages on the bus', 'arrive regularly — check by diagnostics'),
            ('Switch state when switched over', 'changes — check by diagnostics'),
        ],
        'шаги': [
            'FMI 9 (message timeout or communication error on the network): check the CAN bus and the switch unit. Disconnect the units one at a time.',
            'Check the power and ground of the unit that sends the messages.',
            'Check the switch itself: its state should change when it is operated.',
        ],
        'причины': [
            'Intermittent or broken CAN bus.',
            'Lost power to the switch unit.',
            'Faulty switch.',
            'Fault in the engine unit.',
        ],
    },

    2900: {
        'узел': 'Engine cranking permission through the gearbox: the gearbox tells the engine unit whether the engine may be cranked by the starter. '
                'Without this permission the engine unit limits the torque and may not allow a start.',
        'нормы': [
            ('ETC7 message on the bus', 'arrives regularly — check by diagnostics'),
            ('Cranking permission in neutral', 'given — check by diagnostics'),
        ],
        'шаги': [
            'FMI 9 (ETC7 message not arriving): check the CAN bus and the gearbox unit. Disconnect the units one at a time.',
            'FMI 2 (cranking permission not given): check the selector position and the start conditions by diagnostics.',
            'Check the power and ground of the gearbox unit.',
        ],
        'причины': [
            'Intermittent CAN bus.',
            'Wrong selector or neutral switch position.',
            'Faulty gearbox unit.',
            'Mismatched software versions of the units.',
        ],
    },

    3217: {
        'узел': 'Oxygen sensor at the catalyst inlet (bank 1). The control unit uses it to monitor the exhaust composition. The code '
                'refers to the sensor, its supply and its signal. According to one brand\'s table, the same row describes a NOx sensor.',
        'нормы': [
            ('NOx sensor supply voltage in operation', 'per the manufacturer\'s manual'),
            ('Oxygen sensor signal with the engine running', 'changes — check by diagnostics'),
        ],
        'шаги': [
            'FMI 0, 1 (signal above or below the working range; sensor supply voltage too high or too low): unplug the connector, inspect the '
            'contacts; with the ignition on, measure the sensor supply and the signal.',
            'FMI 2 (signal invalid): wiggle the harness with the engine running and watch the value. If it jumps — poor contact.',
            'FMI 5 (open circuit of the UEGO sensor): check the sensor wires from the connector to the unit for continuity.',
            'FMI 15–18 (sensor supply voltage above or below normal): check the sensor supply and its ground. Check the sensor after that.',
        ],
        'причины': [
            'Corroded sensor connector.',
            'Broken or shorted sensor wires.',
            'Faulty sensor.',
            'Control unit or its supply.',
        ],
    },

    3221: {
        'узел': 'Wide-range UEGO oxygen sensor at the inlet, whose signal must be stable. The sensor works over CAN and has its own processor. '
                'The code means a problem with the link to the sensor or with its internal state.',
        'нормы': [
            ('Sensor link over CAN', 'present, without loss — check by diagnostics'),
            ('Sensor signal with the engine running', 'stable — check by diagnostics'),
        ],
        'шаги': [
            'FMI 12 (CAN link to the UEGO sensor lost): check the CAN bus to the sensor and the sensor supply; disconnect the units one at a time.',
            'FMI 15, 16 (sensor out of the reasonable range): check the condition of the engine and the exhaust — the sensor shows the real deviations.',
            'FMI 31 (internal processor fault of the sensor): read the codes and replace the sensor per the manual if the code stays.',
        ],
        'причины': [
            'Broken or kinked CAN wire at the sensor.',
            'Faulty UEGO sensor.',
            'Sensor poisoned by oil or fuel.',
            'Sensor supply.',
        ],
    },

    3222: {
        'узел': 'Heater of the oxygen sensor at the catalyst inlet. The heater lets the sensor reach its working temperature quickly. The code '
                'refers to the heater circuit and to the resistance of the sensor heating element.',
        'нормы': [
            ('Heater resistance with a cold sensor', 'per the manufacturer\'s manual'),
            ('Sensor heating after start-up', 'happens within the time set by the unit — check by diagnostics'),
        ],
        'шаги': [
            'FMI 0, 1, 2 (heater signal above or below the working range, or invalid): unplug the heater connector, inspect the contacts, '
            'and with the ignition on measure the voltage on the contacts.',
            'FMI 3 (high armature voltage of the UEGO sensor): check the heater wire for a short to plus.',
            'FMI 10 (slow heating of the heating element): check the heater resistance and the supply; slow heating points to the sensor.',
        ],
        'причины': [
            'Corroded sensor connector.',
            'Broken or shorted heater wires.',
            'Worn sensor or its heater.',
            'Heater supply from the control unit.',
        ],
    },

    3224: {
        'узел': 'NOx sensor at the SCR system inlet, before the catalyst. The control unit uses it to dose urea. An incorrect signal means '
                'inaccurate dosing, and power loss or torque limitation is possible.',
        'нормы': [
            ('NOx sensor signal with the engine running', 'changes with the load — check by diagnostics'),
            ('NOx sensor supply voltage', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (short to plus or open circuit): unplug the sensor, inspect the contacts; with the ignition on, measure the voltage on the contacts.',
            'FMI 4 (short to ground): disconnect the sensor and see if the code clears. Cleared — the wiring; not cleared — the sensor.',
            'FMI 16 (NOx emission above the second threshold): check the urea dosing and the SCR catalyst by diagnostics before replacing the sensor.',
        ],
        'причины': [
            'Corroded sensor connector.',
            'Sensor wires shorted to plus or ground.',
            'Faulty NOx sensor.',
            'Urea dosing or the SCR catalyst.',
        ],
    },

    3232: {
        'узел': 'Heater of the oxygen sensor at the catalyst outlet (HEGO). The sensor after the catalyst checks how it works. The code '
                'refers to the short circuit of the sensor and to the CAN message from this sensor.',
        'нормы': [
            ('Heater resistance with a cold sensor', 'per the manufacturer\'s manual'),
            ('Message from the sensor on the bus', 'arrives regularly — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (HEGO sensor shorted to supply): unplug the sensor connector and see whether the short clears.',
            'FMI 4 (HEGO sensor shorted to ground): disconnect the sensor and see if the code clears. Cleared — the wiring; not cleared — the sensor.',
            'FMI 14, 19 (CAN frame length wrong): check the software versions of the sensor unit and the control unit.',
        ],
        'причины': [
            'Sensor wiring shorted to plus or ground.',
            'Corroded sensor connector.',
            'Faulty HEGO sensor.',
            'Mismatched software versions of the units.',
        ],
    },

    3241: {
        'узел': 'Catalyst temperature sensor (F766) after the exhaust. The control unit uses it to monitor the temperature and the filter '
                'regeneration. The code refers to the sensor reading or to its wiring.',
        'нормы': [
            ('Catalyst temperature with the engine running', 'rises with the load — check by diagnostics'),
            ('Sensor signal with a cold engine', 'close to the outside air temperature — check by diagnostics'),
        ],
        'шаги': [
            'FMI 2, 10 (temperature implausible): compare with the sensor before the catalyst and with the exhaust temperature; a difference points to the sensor.',
            'FMI 3 (short to supply): unplug the sensor, disconnect it and see whether the short clears.',
            'FMI 4 (short to ground): check the signal wire to the unit for a short to ground.',
            'FMI 15 (temperature too high): first find the causes of the exhaust overheating (regeneration, overload), then the sensor.',
            'FMI 31 (sensors F765 and F766 swapped): check the connection of both sensors against the wiring diagram.',
        ],
        'причины': [
            'Corroded sensor connector.',
            'Wiring shorted to plus or ground.',
            'Catalyst overheating during regeneration.',
            'Faulty temperature sensor.',
        ],
    },

    3249: {
        'узел': 'Catalyst temperature sensor (F765) of the second exhaust stage. The control unit uses it to monitor the temperature and the '
                'filter regeneration.',
        'нормы': [
            ('Catalyst temperature with the engine running', 'rises with the load — check by diagnostics'),
            ('Sensor signal with a cold engine', 'close to the outside air temperature — check by diagnostics'),
        ],
        'шаги': [
            'FMI 2, 10 (temperature implausible): compare with another exhaust temperature sensor; a difference points to the sensor.',
            'FMI 3 (short to supply): unplug the sensor, disconnect it and see whether the short clears.',
            'FMI 4 (short to ground): check the signal wire to the unit for a short to ground.',
        ],
        'причины': [
            'Corroded sensor connector.',
            'Wiring shorted to plus or ground.',
            'Catalyst overheating during regeneration.',
            'Faulty temperature sensor.',
        ],
    },

    3413: {
        'узел': 'Door open status sensor (door 1 status). The control unit gets from it whether the door is open. The code means the sensor '
                'is stuck in the open or the closed position, and the unit reduces power.',
        'нормы': [
            ('Sensor state with the door open and closed', 'changes — check by diagnostics'),
            ('Sensor signal with the door closed while parked', 'matches the closed door — check by diagnostics'),
        ],
        'шаги': [
            'FMI 1 (sensor stuck in the open position): inspect the sensor and its mounting and check that the door does not touch it.',
            'FMI 2 (sensor stuck in the closed position): check the sensor mechanism, close and open the door and watch the state.',
            'Check the sensor connection and the connector to the control unit against the wiring diagram.',
        ],
        'причины': [
            'Seized or broken sensor mechanism.',
            'Deformed door or shifted sensor mounting.',
            'Corroded sensor connector.',
            'Faulty sensor.',
        ],
    },

    3414: {
        'узел': 'Door enable sensor (door 1 enable status). The control unit gets from it whether the door may be opened. The code means the door '
                'is stuck in the open position, and the unit reduces power.',
        'нормы': [
            ('Sensor state with the door open and closed', 'changes — check by diagnostics'),
            ('Sensor signal with the door closed while parked', 'matches the closed door — check by diagnostics'),
        ],
        'шаги': [
            'FMI 1, 8 (door stuck in the open position): inspect the door, the hinges and the lock mechanism; check whether anything stops it from closing.',
            'Check the enable sensor and its mounting, then the connector and the wire to the control unit.',
        ],
        'причины': [
            'Seized or broken door mechanism.',
            'Deformed or shifted door.',
            'Corroded sensor connector.',
            'Faulty enable sensor.',
        ],
    },

    3465: {
        'узел': 'Intake throttle actuator command: the engine control unit moves the throttle with an electric actuator. The code '
                'refers to the throttle actuator circuit.',
        'нормы': [
            ('Throttle actuator resistance with the power off', 'per the manufacturer\'s manual'),
            ('Throttle position on command from the unit', 'changes on command — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (open circuit): check the wire from the unit to the throttle actuator and back for continuity.',
            'FMI 4 (short to ground): disconnect the throttle actuator and see if the code clears. Cleared — the wiring; not cleared — the actuator.',
            'FMI 5 (short to plus or open circuit): disconnect the connector; on command measure the voltage on the contacts against ground.',
        ],
        'причины': [
            'Corroded throttle actuator connector.',
            'Open or shorted actuator wiring.',
            'Sticking throttle.',
            'Faulty throttle actuator.',
        ],
    },

    3468: {
        'узел': 'Fuel temperature sensor (second). The control unit uses it to correct the fuel delivery, because fuel density depends on '
                'its temperature. The code means the fuel temperature is outside the limits.',
        'нормы': [
            ('Temperature signal with the cold engine switched off', 'close to the outside air temperature — check by diagnostics'),
            ('Fuel temperature with the engine running', 'rises from the return and the heat — check by diagnostics'),
        ],
        'шаги': [
            'FMI 1 (extremely low temperature): with a cold engine such a reading can be normal. On a warm engine — the sensor or a broken wire.',
            'FMI 3 (high temperature): check whether the fuel is heated by the return line and the tank; compare with the first fuel temperature sensor.',
            'FMI 4 (low temperature): unplug the sensor connector, inspect the contacts; check the signal wire to the unit for continuity.',
        ],
        'причины': [
            'Fuel overheating from the return line or the tank.',
            'Corroded sensor connector.',
            'Broken or shorted signal wire.',
            'The fuel temperature sensor itself.',
        ],
    },

    3485: {
        'узел': 'Atmospheric pressure sensor in the urea (AdBlue) injection system. The control unit corrects the dosing by the air pressure. '
                'A faulty sensor means the wrong dose.',
        'нормы': [
            ('Sensor reference voltage, ignition on (three-wire sensor)', '5.0 V ± 0.25'),
            ('Pressure readings with the system working', 'close to the barometric pressure — check by diagnostics'),
        ],
        'шаги': [
            'FMI 2 (signal out of range or invalid): compare with the barometric pressure by diagnostics; a difference points to the sensor.',
            'FMI 3 (short to plus or open circuit): unplug the sensor, disconnect it and see whether the short clears.',
            'FMI 4 (short to ground): check the signal wire to the unit for a short to ground.',
        ],
        'причины': [
            'Corroded sensor connector.',
            'Short or open circuit in the sensor wiring.',
            'The pressure sensor itself.',
            'Blocked sensor channel.',
        ],
    },

    3489: {
        'узел': 'Air supply valve of the EAS dosing module: the unit controls it to supply air for urea dosing. The code refers to the valve '
                'circuit and to the absence of air supply.',
        'нормы': [
            ('Valve coil resistance with the power off', 'per the manufacturer\'s manual'),
            ('Air supply on command from the unit', 'present during dosing — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (short to supply on the module contact): disconnect the valve and see whether the short clears.',
            'FMI 4 (short to ground or open circuit): check the wire from the module to the valve; a short to ground is the wiring.',
            'FMI 18 (no air supply during dosing): check the air supply hoses and the valve for blockage.',
        ],
        'причины': [
            'Valve wiring shorted to ground or supply.',
            'Blockage or leak in the air line.',
            'Faulty air supply valve.',
            'Dosing module.',
        ],
    },

    3516: {
        'узел': 'Urea (AdBlue) concentration in the SCR system. The unit estimates it from the dosing and a quality sensor. The code means '
                'less urea than needed is being supplied, or its quality is poor.',
        'нормы': [
            ('Urea concentration in the tank', 'per the manufacturer\'s manual'),
            ('Urea dosing with the engine running', 'matches the load — check by diagnostics'),
        ],
        'шаги': [
            'FMI 1 (less urea supplied than needed): check the urea level, the filter and the dosing pump by diagnostics.',
            'FMI 14 (poor urea, low injection or faulty SCR catalyst): check the urea quality by concentration; if needed, drain and refill fresh urea per the manual.',
            'FMI 18 (poor quality or insufficient dosing): check the urea expiry date and how it was stored.',
        ],
        'причины': [
            'Poor or expired urea.',
            'Blocked urea filter or injector.',
            'Faulty dosing pump.',
            'Worn SCR catalyst.',
        ],
    },

    3609: {
        'узел': 'Pressure sensor before the diesel particulate filter (DPF). The control unit uses the pressure drop to estimate how '
                'much soot is in the filter.',
        'нормы': [
            ('Sensor reference voltage (three-wire sensor), ignition on', '5.0 V ± 0.25'),
            ('Pressure before the filter with the engine running', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 2 (signal out of range or invalid): check the pressure port tube, whether it is blocked with soot or frozen.',
            'FMI 3 (short to plus or open circuit): unplug the sensor and see whether the signal at the unit disappears.',
            'FMI 4 (short to ground): check the signal wire to the unit for a short to ground.',
        ],
        'причины': [
            'Blocked pressure port tube.',
            'Corroded sensor connector.',
            'Wiring shorted to plus or ground.',
            'The pressure sensor itself.',
        ],
    },

    3696: {
        'узел': 'Forced DPF regeneration switch (stationary regeneration). The control unit gets from it the command to start the regeneration '
                'while the vehicle is parked.',
        'нормы': [
            ('Switch state when pressed and released', 'changes — check by diagnostics'),
            ('Switch indicator at switch-on', 'lights on command from the unit — check by diagnostics'),
        ],
        'шаги': [
            'FMI 2 (stationary regeneration switch fault): check that the switch operates and its contacts.',
            'FMI 5 (indicator circuit open): check the indicator wire from the switch to the unit for continuity.',
            'FMI 6 (indicator current too high): short to ground or to plus in the indicator — disconnect the indicator and see if the code clears.',
        ],
        'причины': [
            'Stuck or corroded switch.',
            'Broken indicator wire.',
            'Shorted indicator wiring.',
            'Faulty regeneration control unit.',
        ],
    },

    3840: {
        'узел': 'Frequency output 4/15 of the control unit: the unit sends pulses to a load at a frequency it sets itself. The code points '
                'to the wiring of this output and to the pulse receiver.',
        'нормы': [
            ('Pulses at the output in operation', 'present at the set frequency — check by diagnostics'),
            ('Load resistance at the output', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (short to plus): disconnect the pulse receiver and measure the voltage on the wire against ground.',
            'FMI 4 (short to ground): with the receiver disconnected, the wire must not short to ground.',
            'FMI 5 (open wire): check the wire from the unit to the receiver.',
        ],
        'причины': [
            'Receiver wiring shorted to plus or ground.',
            'Broken wire or corroded connector.',
            'Faulty pulse receiver.',
            'Output stage of the control unit.',
        ],
    },

    3841: {
        'узел': 'Frequency output 4/11 of the control unit: the unit sends pulses to a load at a frequency it sets itself. The code points '
                'to the wiring of this output and to the pulse receiver.',
        'нормы': [
            ('Pulses at the output in operation', 'present at the set frequency — check by diagnostics'),
            ('Load resistance at the output', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 3 (short to plus): disconnect the pulse receiver and measure the voltage on the wire against ground.',
            'FMI 4 (short to ground): with the receiver disconnected, the wire must not short to ground.',
            'FMI 5 (open wire): check the wire from the unit to the receiver.',
        ],
        'причины': [
            'Receiver wiring shorted to plus or ground.',
            'Broken wire or corroded connector.',
            'Faulty pulse receiver.',
            'Output stage of the control unit.',
        ],
    },

    3842: {
        'узел': 'Analogue ground 3/02 of the control unit: the common ground to which the sensors are connected. If the ground is poor, all '
                'sensors on it give wrong values, so the code matters even without an obvious sensor fault.',
        'нормы': [
            ('Resistance between the unit analogue ground and the battery ground', 'low — per the manufacturer\'s manual'),
            ('Voltage on the analogue ground against the battery ground', 'close to zero — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (analogue ground shorted to plus): check the ground against the battery plus; find the wire that put plus on the unit ground.',
            'FMI 4 (short to ground): check whether another load or a short through a sensor is connected to the analogue ground.',
            'FMI 5 (open wire): check the unit ground and its connector — broken or corroded.',
        ],
        'причины': [
            'Broken or corroded control unit ground.',
            'Sensor ground connected to plus.',
            'Short to the body through a sensor.',
            'Poor ground bond to the frame.',
        ],
    },

    4335: {
        'узел': 'Absolute pressure of the SCR auxiliary dosing air supply. The sensor measures the atmospheric pressure, and the unit corrects '
                'the air and urea supply by it.',
        'нормы': [
            ('Pressure readings with the system working', 'close to the barometric pressure — check by diagnostics'),
            ('Air supply to the dosing', 'without interruptions — check by diagnostics'),
        ],
        'шаги': [
            'FMI 0, 1 (pressure too high or too low): compare with a barometer by diagnostics; a difference points to the sensor.',
            'FMI 7 (air supply interrupted): check the air line for leaks and blockage with soapy water, and check the hoses.',
            'FMI 14 (the pressure pipe could not be emptied): check the pipe and the air supply valve for blockage.',
        ],
        'причины': [
            'Leak or blockage in the dosing air line.',
            'Faulty air supply valve.',
            'The pressure sensor.',
            'Blocked pressure pipe.',
        ],
    },

    4336: {
        'узел': 'Distribution air valve of the SCR auxiliary dosing supply: it directs air to the urea dosing. The code refers to the valve circuit.',
        'нормы': [
            ('Valve coil resistance with the power off', 'per the manufacturer\'s manual'),
            ('Valve operation on command from the unit', 'present — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (short to ground): disconnect the valve and see if the code clears. Cleared — the wiring; not cleared — the valve.',
            'FMI 4 (short to plus or open circuit): disconnect the valve connector; on command measure the voltage on the contacts against ground.',
            'FMI 5 (open circuit): check the wire from the unit to the valve and back for continuity.',
        ],
        'причины': [
            'Corroded valve connector.',
            'Wiring shorted to ground or plus.',
            'Valve coil.',
            'Blockage in the air line.',
        ],
    },

    4342: {
        'узел': 'AdBlue line heater (second): heats the urea supply line so that the urea does not freeze. The code refers to the heater '
                'circuit and to the feedback signal.',
        'нормы': [
            ('Heater resistance with the power off', 'per the manufacturer\'s manual'),
            ('Heater feedback on switch-on', 'present and matches the command — check by diagnostics'),
        ],
        'шаги': [
            'FMI 2, 3 (heater circuit open, or short to supply): check the heater wire for continuity; when switched on, measure the voltage on the contacts.',
            'FMI 4 (open circuit or short to ground): disconnect the heater and see if the code clears.',
            'FMI 14 (feedback signal invalid): check the heater connector and the feedback wire.',
        ],
        'причины': [
            'Broken heater wire.',
            'Wiring shorted to ground or supply.',
            'Corroded heater connector.',
            'Faulty heater.',
        ],
    },

    4354: {
        'узел': 'AdBlue line heater (first): heats the urea supply pipe so that the urea does not freeze. The code refers to the pipe heater circuit.',
        'нормы': [
            ('Heater resistance with the power off', 'per the manufacturer\'s manual'),
            ('Pipe heating with the engine cold', 'switches on on command from the unit — check by diagnostics'),
        ],
        'шаги': [
            'FMI 3 (short to plus or open circuit): check the heater wire; when switched on, measure the voltage on the contacts.',
            'FMI 4 (short to ground): disconnect the heater and see if the code clears.',
            'FMI 5 (open circuit): check the wire from the unit to the heater and back for continuity.',
            'FMI 7 (circuit fault): check the heater connectors and the wires for corrosion.',
        ],
        'причины': [
            'Broken heater wire.',
            'Wiring shorted to ground or plus.',
            'Corroded heater connector.',
            'Faulty pipe heater.',
        ],
    },

    4375: {
        'узел': 'AdBlue (urea) pump of the SCR system: the unit controls the pump drive level to supply the right amount of urea. The code '
                'refers to the pump flow and to the supply control circuit.',
        'нормы': [
            ('Pump drive level in operation', 'matches the engine load — check by diagnostics'),
            ('Supply control circuit resistance with the power off', 'per the manufacturer\'s manual'),
        ],
        'шаги': [
            'FMI 0 (urea flow too high): check the pump and the dosing line for leaks, and check the pump operation by diagnostics.',
            'FMI 3 (short to plus or open circuit in the supply control): disconnect the pump connector and measure the voltage on the contacts against ground.',
            'FMI 4 (short to ground in the supply control): disconnect the pump and see if the code clears.',
            'FMI 5 (open circuit): check the wire from the unit to the pump and back for continuity.',
        ],
        'причины': [
            'Leak or blockage in the urea line.',
            'Corroded pump connector.',
            'Wiring shorted to ground or plus.',
            'Faulty urea pump.',
        ],
    },
}

for _k, _v in _B.items():
    assert _k not in CHECKS, _k
    CHECKS[_k] = _v
