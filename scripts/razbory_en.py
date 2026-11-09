# -*- coding: utf-8 -*-
"""
Раздел «Разборы», английские тексты (09.11.2026). Формат - как в razbory_ru.py.
Это пересказ по смыслу, а не дословный перевод; ссылки ведут на en-страницы.
"""

A = {}

A['eberspacher-011'] = dict(
    title=u'Eberspächer 011: low voltage shutdown - what to check',
    h1=u'Eberspächer shows 011: the heater is not getting enough voltage',
    desc=u'Eberspächer code 011 means undervoltage for more than 20 seconds. Thresholds by model, how the '
         u'code looks on different controllers, what to check yourself and when to see a workshop.',
    short=u'Code 011 is not about the burner or the fuel: the control unit received too little voltage '
          u'and shut the heater down. Start with the fuses, the power wires, the ground and the positive '
          u'battery terminal.',
    body=[
        (u'What the unit actually records', [
            u'In the Eberspächer factory table, 011 is undervoltage with shutdown. The condition is simple: '
            u'the voltage at the control unit stayed low for at least 20 seconds in a row. A brief dip does '
            u'not set the code.',
            u'The thresholds differ slightly between manuals:',
            ('tbl', [u'Heater', u'System', u'Code is set if voltage is'],
             [[u'Hydronic', u'24 V', u'below 19 V'],
              [u'Airtronic 2 and 4 (Espar manual)', u'12 V', u'below 10.2 V'],
              [u'Airtronic 2 and 4 (Espar manual)', u'24 V', u'below 20.4 V']]),
        ]),
        (u'How the code looks on different controllers', [
            u'The same fault is shown differently, so you will not see "011" everywhere:',
            ('tbl', [u'Controller', u'What the driver sees'],
             [[u'Old modular timer 1531', u'A three-digit number 011 marked AF (active fault) or F1-F5 (from memory)'],
              [u'EasyStart Pro', u'No number: a red flashing ring on the button and the text "Undervoltage"'],
              [u'EasyStart Select', u'No number: an icon meaning "heater off, undervoltage"']]),
        ]),
        (u'Neighbouring codes people mix up with 011', [
            ('tbl', [u'Code', u'Meaning', u'Condition'],
             [[u'011', u'Undervoltage, shutdown', u'low for at least 20 s in a row'],
              [u'010', u'Overvoltage', u'above 16 V (12 V system) or above 32 V (24 V system), at least 20 s'],
              [u'012', u'Overheat at the overheat sensor', u'a different cause, not related to power'],
              [u'091', u'External interference voltage', u'noise in the supply, not a sag']]),
            u'Details for each: [[/en/otopiteli/eberspacher-011.html|011]], '
            u'[[/en/otopiteli/eberspacher-010.html|010]], [[/en/otopiteli/eberspacher-012.html|012]], '
            u'[[/en/otopiteli/eberspacher-091.html|091]].',
        ]),
        (u'What to check without instruments', [
            u'For code 011 the factory names four checks; do them in this order:',
            ('ol', [u'The fuses in the heater circuit.',
                    u'The power wires to the heater: breaks, corrosion, damaged insulation.',
                    u'The negative connections (ground): tight and clean.',
                    u'The positive battery terminal: corrosion and a firm contact.']),
            u'Everything else is measuring and replacing parts.',
        ]),
        (u'When to go to a workshop', [
            [u'the code returns after the fuses, wires, ground and terminal have been checked;',
             u'the voltage at the heater connector has to be measured: per the manual it should equal the '
             u'battery voltage, and that measurement is a workshop job.'],
        ]),
    ],
    faq=[
        (u'How is 011 different from 010?',
         u'011 means there is too little voltage, 010 too much (above 16 V on a 12 V system and above 32 V on '
         u'a 24 V system). Both are set if the condition lasts at least 20 seconds.'),
        (u'Why does my controller not show 011?',
         u'EasyStart Pro shows a red flashing ring and the word Undervoltage instead of a number, EasyStart '
         u'Select shows an icon. The old modular timer 1531 shows the three-digit number.'),
        (u'Does it mean the heater is broken?',
         u'Not necessarily. The code is about the supply, not the burner or the fuel: the cause is usually '
         u'a fuse, wiring, ground or the battery terminal.'),
        (u'What voltage should be at the heater connector?',
         u'According to the factory manual, the same as at the battery. Measuring it is a workshop task.'),
    ],
    more=[(u'/en/otopiteli/eberspacher-011.html', u'Code 011 Eberspächer - code page'),
          (u'/en/marki/eberspacher.html', u'All Eberspächer codes'),
          (u'/en/otopiteli/', u'Index of heater codes')],
)

A['planar-kod-13-i-miganiya-pu5'] = dict(
    title=u'Planar code 13 and PU-5 blinks - correspondence table',
    h1=u'Planar: why code 13 and 13 blinks are different faults',
    desc=u'Planar has two code systems: the number on the controller display and the PU-5 blinks. A '
         u'correspondence table, a look at 13, 29, 78, 04 and 06, and what to check yourself.',
    short=u'Code 13 on a display controller matches two blinks of the PU-5, while 13 blinks is code 35, '
          u'found only on the Planar 8DM. The numbers in the two systems do not match, so first find out '
          u'exactly what you are looking at.',
    body=[
        (u'Two systems, one heater', [
            u'**Repair code**: a number from the repair manual table, shown on a display controller such as '
            u'the PU-22: 01, 02, 13, 29, 78 and so on.',
            u'**PU-5 blinks**: this controller has no display; a red LED blinks the needed number of times '
            u'and pauses. Any button resets the signal.',
            u'The same failure carries different numbers in the two systems. The correspondence is given in '
            u'the Autoterm user manual.',
        ]),
        (u'Table: repair code and PU-5 blinks', [
            ('tbl', [u'Repair code', u'PU-5 blinks', u'What happened'],
             [[u'01', u'1', u'Heat exchanger overheated'],
              [u'02', u'12', u'Possible overheating near the control unit'],
              [u'13', u'2', u'Failed to start after two attempts'],
              [u'29 (and 08)', u'3', u'Flame-out during operation'],
              [u'78', u'3', u'Flame-out (air bubble, pump, flame indicator)'],
              [u'09', u'4', u'Glow plug'],
              [u'05', u'5', u'Flame indicator'],
              [u'04 / 06', u'6', u'Temperature sensor in the control unit'],
              [u'17', u'7', u'Fuel pump'],
              [u'20', u'8', u'No link between the controller and the unit'],
              [u'12 and 15', u'9', u'Voltage: high and low share one number'],
              [u'16', u'10', u'Ventilation time exceeded'],
              [u'10, 27, 28', u'11', u'Air blower']]),
            u'Three traps follow from the table. Two blinks on the PU-5 are not code 02 but code 13. Four '
            u'blinks are not 04 but the glow plug (09). And 13 blinks are not code 13 but code 35: flame-out '
            u'caused by a voltage dip, present only on the Planar 8DM.',
        ]),
        (u'The most common codes', [
            u'**13: the heater did not start.** Two automatic start attempts failed. The manual says to check '
            u'the fuel (is there any, and is it suitable for the temperature), the fuel line for leaks and '
            u'blockage, the air intake and exhaust, the blower and whether the glow plug heats. Checking the '
            u'plug and the voltage at the unit counts as repair work.',
            u'**29 and 78: flame-out.** The flame went out during operation. Causes: too little fuel, a '
            u'faulty pump or flame indicator; for 78 an air bubble in the fuel system is added. On the PU-5 '
            u'both codes give three blinks.',
            u'**04 and 06: temperature sensor in the unit.** It is built into the control unit and is not '
            u'replaced separately; it has no wiring. The only cure is replacing the unit, which is service work.',
        ]),
        (u'What to check yourself', [
            [u'fuel in the tank and whether it suits the season;',
             u'exhaust and air intake: the passage must be clear;',
             u'fuel line: leaks and tight clamps;',
             u'blower: no sticking and no foreign objects.'],
        ]),
        (u'When to see a workshop', [
            [u'code 04 or 06: the control unit must be replaced;',
             u'13 or 29 repeat after the fuel, exhaust and fuel line were checked;',
             u'the plug, fuel pump or flame indicator needs testing;',
             u'you could not find the cause from the list above.'],
        ]),
    ],
    faq=[
        (u'Are two blinks on the PU-5 code 02?',
         u'No. Two blinks correspond to repair code 13 (failed to start after two attempts). Code 02 on the '
         u'PU-5 is twelve blinks.'),
        (u'What do three blinks on the PU-5 mean?',
         u'Flame-out during operation: in the repair table that is codes 29 and 08 (and 78 with air in the '
         u'fuel system). There is no code 03 in the repair table.'),
        (u'Can the temperature sensor be replaced separately for code 04 or 06?',
         u'No, it is built into the control unit. The whole unit is replaced, and that is service work.'),
        (u'Where do 13 blinks come from?',
         u'That is code 35, flame-out due to a voltage dip, and only on the Planar 8DM. It has nothing to do '
         u'with code 13.'),
    ],
    more=[(u'/en/otopiteli/planar-13.html', u'Code 13 - failed to start'),
          (u'/en/otopiteli/planar-29.html', u'Code 29 - flame-out'),
          (u'/en/otopiteli/planar-78.html', u'Code 78 - flame-out, air in the fuel'),
          (u'/en/otopiteli/planar-4.html', u'Code 4 - temperature sensor in the unit'),
          (u'/en/otopiteli/planar-6.html', u'Code 6 - temperature sensor in the unit'),
          (u'/en/otopiteli/planar-2.html', u'Code 2 - possible overheating'),
          (u'/en/marki/planar.html', u'All Planar codes')],
)

A['webasto-f-kody-i-sluzhebnye-kody'] = dict(
    title=u'Webasto F-codes and service codes - what differs',
    h1=u'Webasto: why service code 03 and F03 are different things',
    desc=u'Table of Air Top 2000 ST F-codes, how Thermo Top Evo differs, how the code appears on the '
         u'timer and how F-codes differ from the service codes of the diagnostic software.',
    short=u'Webasto has two code systems: F00-F15 on the timer and hexadecimal service codes in the '
          u'workshop software. The digits coincide, the meaning does not: service 03 is flame-out, F03 is '
          u'voltage. A driver needs the F-code and the model of the heater.',
    body=[
        (u'Where the confusion comes from', [
            u'One F-code on the timer groups several service codes. On the Air Top 2000 ST service code 03 is '
            u'flame-out, which the timer shows as F02. F03 is a voltage problem, with service codes 84 and 04. '
            u'The Thermo Top Evo table has no service code 03 at all.',
        ]),
        (u'Air Top 2000 ST F-codes', [
            ('tbl', [u'On the timer', u'What happened'],
             [[u'F00', u'Control unit fault'],
              [u'F01', u'No start'],
              [u'F02', u'Flame-out'],
              [u'F03', u'Voltage: below 10.5 V (21 V on a 24 V system) for more than 20 s or above 16 V (32 V) for more than 6 s'],
              [u'F04', u'Flame before combustion starts'],
              [u'F05', u'Flame sensor (petrol only)'],
              [u'F06', u'External temperature sensor'],
              [u'F07', u'Metering pump'],
              [u'F08', u'Drive: combustion and heating air fan'],
              [u'F09', u'Glow plug'],
              [u'F10', u'Overheating'],
              [u'F11', u'Overheat sensor'],
              [u'F12', u'Heater lock-out'],
              [u'F14', u'Overheat sensor installed incorrectly'],
              [u'F15', u'Setpoint potentiometer']]),
            u'This model has no F13.',
        ]),
        (u'What changes on the Thermo Top Evo', [
            u'The numbers are the same, but some meanings differ:',
            ('tbl', [u'Code', u'Air Top 2000 ST', u'Thermo Top Evo'],
             [[u'F11', u'overheat sensor', u'coolant pump'],
              [u'F14', u'overheat sensor installed incorrectly', u'overheat sensor'],
              [u'F15', u'setpoint potentiometer', u'glow plug circuit'],
              [u'F13', u'none', u'vehicle fan'],
              [u'F16', u'none', u'high exhaust temperature'],
              [u'F17', u'none', u'exhaust sensor'],
              [u'F05, F12', u'present', u'absent']]),
            u'F03 on the Thermo Top Evo is also about the on-board voltage. The repair table labels it "too '
            u'high", the user manual "too low or raised"; for the driver it is one thing: check the supply '
            u'voltage. The conclusion: read an F-code only together with the heater model.',
        ]),
        (u'How the driver sees the code', [
            [u'**Combined timer on the Air Top 2000 ST:** a code number on the screen until the fault is '
             u'cleared; the manual advises contacting a Webasto service.',
             u'**ON indicator without a display:** 5 seconds of rapid flashing, then the number of long '
             u'flashes equals the F-code number (F04 is four long flashes). Plain rapid flashing is F00.',
             u'**MultiControl and SmartControl on the Thermo Top Evo:** F01-F15 on the display, while '
             u'F16-F19 show as "- -". Codes of the form TXX belong to the controller itself.',
             u'**W-bus and analog connection on the Thermo Top Evo:** hexadecimal Hxx numbers over W-bus, '
             u'Fxx over analog.'],
            u'Telestart and ThermoCall controllers show neither the F-code number nor the fact of a heater '
            u'fault, only the state of the link, battery and module. ThermoCall has a general warning (the '
            u'heater does not execute the command, service needed). The F-code comes from the heater itself '
            u'or the indicator in the cab.',
        ]),
        (u'What you can do and when to see a workshop', [
            [u'identify the heater model and the type of controller;',
             u'for F03, inspect the terminals and charge the battery;',
             u'do not compare the number with the service-code table: use the table for your model.'],
            u'Factory manuals leave the driver little to do. The Webasto instruction directly advises '
            u'contacting a service for any number code on the timer. Diagnostics are needed for F00, F07, F08, '
            u'F09, F10 and F11: the control unit, pump, drive, glow plug and overheating.',
        ]),
    ],
    faq=[
        (u'Are service code 03 and F03 the same?',
         u'No. On the Air Top 2000 ST service 03 is flame-out, which the timer shows as F02. F03 is the '
         u'on-board voltage.'),
        (u'Why does the same F-code mean something else on the Thermo Top Evo?',
         u'The code tables differ between models. For example F11 is the overheat sensor on the Air Top '
         u'2000 ST and the coolant pump on the Thermo Top Evo.'),
        (u'Will a Telestart or ThermoCall controller show an F-code?',
         u'No, they show the link, battery charge and module state. The F-code comes from the heater or its '
         u'indicator.'),
        (u'What does the number of long flashes on the ON indicator equal?',
         u'The F-code number: after 5 seconds of rapid flashing, four long flashes are F04. Plain rapid '
         u'flashing means F00.'),
    ],
    more=[(u'/en/otopiteli/webasto-f03.html', u'F03 - on-board voltage'),
          (u'/en/otopiteli/webasto-f02.html', u'F02 - flame-out'),
          (u'/en/otopiteli/webasto-f07.html', u'F07 - metering pump'),
          (u'/en/otopiteli/webasto-f08.html', u'F08 - fan drive'),
          (u'/en/otopiteli/webasto-f09.html', u'F09 - glow plug'),
          (u'/en/otopiteli/webasto-f10.html', u'F10 - overheating'),
          (u'/en/marki/webasto.html', u'All Webasto codes')],
)

A['kamaz-spn-97-voda-v-toplive'] = dict(
    title=u'KAMAZ SPN 97: water in fuel - can you keep driving',
    h1=u'KAMAZ, SPN 97: water in the filter - when to drive, what to drain',
    desc=u'SPN 97 is the water-in-fuel sensor signal. What FMI 15, 16, 3 and 4 mean, whether you can '
         u'drive, how to drain the sump and what to do if there is no water but the code stays.',
    short=u'SPN 97 comes from the water sensor in the sump of the primary fuel filter. While the engine '
          u'pulls evenly and no red lamp is on, you can reach a stop and drain the water there, but do not '
          u'wait for scheduled service: water damages injectors and the high-pressure pump.',
    body=[
        (u'What the code says', [
            u'In the SAE J1939 list SPN 97 is Water In Fuel Indicator. Water is heavier than diesel and '
            u'collects at the bottom of the sump, where the sensor sits. The second part (FMI) says what '
            u'happened. By the Cummins table, whose engines are fitted to some KAMAZ models:',
            ('tbl', [u'FMI', u'Meaning', u'Cummins code'],
             [[u'15', u'Water above normal, least severe level', u'418'],
              [u'16', u'Water above normal, moderately severe level', u'1852'],
              [u'3', u'Sensor circuit: voltage above normal or short to positive', u'428'],
              [u'4', u'Sensor circuit: voltage below normal or short to ground', u'429']]),
            u'FMI 15 and 16 are about water, FMI 3 and 4 about the sensor electrics. On KAMAZ, YaMZ and MAZ '
            u'FMI 11 also occurs: the standard calls it "cause unknown", and its meaning comes from the '
            u'vehicle table.',
        ]),
        (u'Can you keep driving', [
            u'Cummins puts FMI 15 at the lightest level and FMI 16 at the middle: a warning, not an order to '
            u'stop. A rule of thumb:',
            [u'even pull and no red lamp: reach the nearest stop and drain the water;',
             u'power lost or a red STOP lamp: stop; per the Cummins card you must not drive with the red lamp on;',
             u'do not wait for scheduled service: drain at the first opportunity.'],
            u'How exactly a KAMAZ behaves (lamp, power reduction) is in the manual for your model.',
        ]),
        (u'How to drain the sump', [
            ('ol', [u'Shut off the engine and set the parking brake.',
                    u'Place a clear container under the drain tap of the primary fuel filter (separator).',
                    u'Open the tap and drain the sediment; the clear jar is there so you can see the water.',
                    u'Look at what came out: besides water, the Detroit Diesel instruction says to look for '
                    u'AdBlue, petrol, kerosene and coolant in the fuel.',
                    u'Drain until clean fuel comes out, close the tap but do not overtighten it.',
                    u'Prime the system with the hand pump per the manual, start the engine and see whether '
                    u'the signal returns.']),
            u'If the water comes back in a day or two, there is a lot in the tank: drain the tank sump and '
            u'think about where you refuelled.',
        ]),
        (u'No water but the code is there', [
            u'Detroit Diesel describes a case where coolant got into the harness connectors, the contacts '
            u'oxidised and the unit "saw" water. The principle is general: inspect the sensor connector for '
            u'moisture and green deposits. FMI 3 and 4 mean a sensor circuit fault: break, short, poor contact. '
            u'Replace the sensor only after draining the water and inspecting the connector.',
        ]),
        (u'What not to do and when to see a workshop', [
            [u'do not clear the code and drive on without draining the sump;',
             u'do not overtighten the drain tap: per Detroit Diesel it can damage the tap and the housing;',
             u'do not buy a sensor until the water is drained and the connector checked.'],
            u'See a workshop if water returns after draining and cleaning the tank, a red STOP lamp is on or '
            u'power is lost, something besides water and diesel is in the drain (AdBlue, petrol, coolant), or '
            u'the code stays after draining and connector inspection.',
        ]),
    ],
    faq=[
        (u'What does SPN 97 mean on a KAMAZ?',
         u'The water-in-fuel sensor signals that water has collected in the sump of the primary fuel '
         u'filter. Sometimes the sensor or its connector is the cause.'),
        (u'Can I drive with SPN 97?',
         u'With an even pull and no red lamp you can reach a stop and drain the water. If power is lost or a '
         u'red STOP lamp is on, stop.'),
        (u'How is FMI 15 different from FMI 3?',
         u'FMI 15 is water above normal (the lightest level), FMI 3 is sensor electrics: voltage above '
         u'normal or a short to positive. Replacing the sensor for FMI 15 is premature.'),
        (u'There is no water in the sump but the code is set. Why?',
         u'Moisture and oxidation in the sensor connector or a circuit fault (FMI 3 and 4) are possible. '
         u'Inspect the connector first and only then replace the sensor.'),
    ],
    more=[(u'/en/kody/spn-97.html', u'SPN 97 - water in fuel, all makes'),
          (u'/en/kody/spn-95.html', u'SPN 95 - fuel filter differential pressure'),
          (u'/en/kody/spn-94.html', u'SPN 94 - fuel pressure'),
          (u'/en/marki/kamaz.html', u'All KAMAZ codes')],
)

A['mercedes-actros-spn-107'] = dict(
    title=u'Mercedes Actros SPN 107: air filter or sensor fault',
    h1=u'Actros, SPN 107: clogged filter or a lying sensor',
    desc=u'SPN 107 is the differential pressure across the engine air filter. What FMI 0, 2, 3 and 4 '
         u'mean, what to check yourself on a Mercedes-Benz Actros and when to see a workshop.',
    short=u'The control unit sees too large a pressure difference across the air filter. Most often the '
          u'filter really is clogged, but sometimes the tube, connector or the sensor is to blame, so '
          u'inspect the filter and tubes first and buy a sensor only afterwards.',
    body=[
        (u'What the sensor measures', [
            u'In the SAE J1939 list SPN 107 is Engine Air Filter 1 Differential Pressure; Daimler and Deutz '
            u'list it the same way. The sensor does not measure air pressure in general but the difference '
            u'before and after the filter: the dirtier the filter, the larger it is.',
            ('tbl', [u'FMI', u'Meaning'],
             [[u'0', u'Differential above normal: filter clogged'],
              [u'2', u'Signal unstable or erratic'],
              [u'4', u'Sensor circuit: voltage below normal or short to ground'],
              [u'3', u'Sensor circuit: by the standard voltage above normal or short to positive; Mercedes '
                     u'tables say "open circuit" - verify on the vehicle']]),
            u'On machines with Cummins engines FMI 15 and 16 also occur ("above normal", different urgency). '
            u'Open sources have no such data for the Actros.',
        ]),
        (u'What the driver sees, and can you drive', [
            u'Open sources do not say which lamp and message the Actros shows for SPN 107, so do not look for '
            u'a photo of someone else\'s icon: check your own vehicle. A scanner, however, shows SPN 107 and '
            u'FMI. On Multiquip machines with a Hatz engine the same code lit a red lamp and put the engine '
            u'into reduced-power limp mode; how the Actros behaves, check the manual or a workshop.',
            u'Sources give no trigger threshold or permission to drive for the Actros, so the decision stays '
            u'with the driver. In doubt, stop and check the filter. Power gone or a red lamp on: stay put.',
        ]),
        (u'Order of checks', [
            ('ol', [u'Recall when the air filter was last changed. If long ago, start there: manufacturer '
                     u'tables advise cleaning or replacing the filter for FMI 0.',
                    u'Check for an extra insert filter inside the housing: on Multiquip machines exactly this '
                    u'gave an inflated differential.',
                    u'Clamps and pipes between the air filter, turbo and intercooler: any loose ones.',
                    u'Connector and harness of the differential sensor: corrosion, moisture, breaks.',
                    u'Pressure sampling tubes at the sensor: dry and unblocked.']),
            u'Measuring the sensor signal and reading the unit are workshop jobs.',
        ]),
        (u'What not to do and when to see a workshop', [
            [u'do not clear the code and drive on without looking at the filter;',
             u'do not replace the sensor until the filter, tubes and connector are checked.'],
            u'See a workshop if the filter is new and the code returns; if you need the exact meaning of '
            u'FMI 3 and the trigger threshold for your engine (for example OM 471 or OM 501), which are in '
            u'Mercedes-Benz diagnostics; or if a red lamp is on or power is lost.',
        ]),
    ],
    faq=[
        (u'What does SPN 107 mean on a Mercedes Actros?',
         u'Too large a pressure difference across the engine air filter. Most often the filter is clogged, '
         u'but faulty tubes, a connector or the sensor are possible.'),
        (u'How is FMI 0 different from FMI 3 and 4?',
         u'FMI 0 is a differential above normal, i.e. a clogged filter. FMI 3 and 4 are faults in the '
         u'sensor\'s electrical circuit; the filter has nothing to do with it.'),
        (u'Can I drive with SPN 107?',
         u'Sources name neither a threshold nor permission for the Actros. If power is lost or a red lamp is '
         u'on, stop. If unsure, check the filter first.'),
        (u'Should I replace the sensor for SPN 107?',
         u'Only after checking the filter, the pressure tubes and the connector. The sensor often turns out '
         u'to be fine.'),
    ],
    more=[(u'/en/kody/spn-107.html', u'SPN 107 - air filter differential pressure'),
          (u'/en/kody/spn-102.html', u'SPN 102 - boost pressure'),
          (u'/en/kody/spn-105.html', u'SPN 105 - intake air temperature'),
          (u'/en/marki/mercedes.html', u'All Mercedes-Benz codes')],
)

A['sazhevyy-filtr-dpf'] = dict(
    title=u'Truck DPF: codes, lamps and regeneration explained',
    h1=u'Diesel particulate filter (DPF): what the lamps and codes mean, when you can drive',
    desc=u'How a DPF cleans itself, which SPNs the unit reports, what a steady and a flashing lamp mean, '
         u'how to run a parked regeneration and when the filter needs a workshop.',
    short=u'On a steady amber DPF lamp you can drive, but regeneration has to be arranged straight away. A '
          u'flashing lamp together with check engine cannot wait: a parked regeneration is needed. A red '
          u'STOP lamp with DPF means the vehicle must not be operated.',
    body=[
        (u'How the filter cleans itself', [
            u'The Cummins manual describes three ways:',
            [u'**passive regeneration**: while driving, when the exhaust is hot enough on its own and the '
             u'unit does nothing;',
             u'**active**: the unit lacks heat, injects a little unburnt fuel into the stream and ignites the soot;',
             u'**forced (parked)**: the vehicle stands, revs are raised, the filter cleans for up to an hour; '
             u'started with a button or from a menu if a highway run did not help or the lamp flashes.'],
            u'Short trips and cold exhaust get in the way, which is why the lamp comes on more often in city '
            u'driving.',
        ]),
        (u'Main SPN codes', [
            ('tbl', [u'SPN', u'Meaning'],
             [[u'3719', u'DPF soot load, in percent. FMI 15, 16, 0 are three levels, from low to most severe'],
              [u'3251', u'DPF differential pressure - how clogged the filter is. FMI 15, 16, 0: above normal; FMI 3 and 4: sensor circuit; FMI 2: unstable signal'],
              [u'3697', u'DPF lamp command on the dashboard'],
              [u'3698', u'High exhaust temperature lamp command (HEST)'],
              [u'3703', u'Active regeneration inhibited by the inhibit switch (FMI 31: condition exists)'],
              [u'3695 and 3696', u'Switches: regeneration inhibit and forced regeneration']]),
            u'SPN 3719 and 3251 are linked: the unit judges clogging by the differential pressure and then '
            u'computes the soot load. Numbers 3700-3702 (regeneration status) differ between sources, so '
            u'they are left out of the table. Code page for the differential pressure: [[/en/kody/spn-3251.html|SPN 3251]].',
        ]),
        (u'Which lamp demands what', [
            ('tbl', [u'On the dashboard', u'What to do'],
             [[u'DPF steady', u'The filter needs regeneration. Make sure the inhibit switch is off. At the first '
                              u'chance get onto a highway and keep going for 20-30 minutes. The Actros gives a window '
                              u'on a steady amber lamp: first four hours, then 30 minutes'],
              [u'DPF flashing', u'Regeneration is urgent, power may drop automatically. On the Actros a flashing '
                                u'amber lamp means start regeneration manually at once'],
              [u'DPF flashing and check engine on', u'Immediate parked regeneration is needed, power is cut harder; '
                                                    u'"I will make it home" is no longer an option'],
              [u'Red STOP lamp together with DPF', u'The vehicle must not be operated: stop and call a workshop'],
              [u'HEST (high exhaust temperature)', u'Regeneration is under way and the exhaust is hot. Not a '
                                                   u'fault; do not point the pipe at flammable objects']]),
        ]),
        (u'Parked regeneration, step by step', [
            u'Per the Cummins driver card (on an Actros the start procedure is in the on-board manual):',
            ('ol', [u'Park on level ground with nothing near the exhaust.',
                    u'Parking brake on, gearbox in neutral or Park.',
                    u'Fast idle and power take-off (PTO) off.',
                    u'Press the manual regeneration switch.',
                    u'Revs will rise and the turbo sound will change; this is normal. Regeneration takes up to an hour.',
                    u'Stay by the vehicle and watch the exhaust. If it becomes unsafe, shut off the engine or '
                    u'press the brake or accelerator pedal: that interrupts regeneration.',
                    u'After it ends the exhaust and surfaces stay hot for another 3-5 minutes.']),
        ]),
        (u'What not to do', [
            [u'interrupt an active regeneration without need;',
             u'start a forced regeneration without finding the cause: otherwise the vehicle will be back with '
             u'the same problem in a week;',
             u'keep the inhibit switch on without reason: per Cummins this leads to frequent parked '
             u'regenerations and a clogged filter;',
             u'expect regeneration to clear ash: ash does not burn, it is removed by cleaning or replacing the filter;',
             u'replace the filter for SPN 3251 without checking the sensor tubes, connector and the sensor itself.'],
            u'See a workshop if regeneration does not run and the lamp stays on, a red STOP lamp is on with '
            u'DPF, SPN 3251 with FMI 0 and 16 remains after regeneration, or regenerations are needed more '
            u'and more often. Related pages: [[/en/problemy/zabit-sazhevyy-filtr.html|clogged particulate filter]] '
            u'and [[/en/problemy/ne-idet-regeneratsiya.html|regeneration will not run]].',
        ]),
    ],
    faq=[
        (u'Can I drive with the amber DPF lamp on?',
         u'Yes, if it is steady, but regeneration must be done at once: get onto a highway and keep going '
         u'for at least 20-30 minutes. A flashing lamp with check engine cannot wait.'),
        (u'How long does a parked regeneration take?',
         u'Up to an hour. Stay by the vehicle and watch the exhaust the whole time; afterwards it stays hot '
         u'for 3-5 minutes.'),
        (u'Why does regeneration not remove everything from the filter?',
         u'Soot burns off, ash does not. Ash is removed by cleaning or replacing the filter.'),
        (u'How is SPN 3719 different from SPN 3251?',
         u'SPN 3251 is the differential pressure across the filter, from which the unit judges clogging. '
         u'SPN 3719 is the computed soot load in percent.'),
    ],
    more=[(u'/en/kody/spn-3251.html', u'SPN 3251 - DPF differential pressure'),
          (u'/en/problemy/zabit-sazhevyy-filtr.html', u'Clogged particulate filter - signs and codes'),
          (u'/en/problemy/ne-idet-regeneratsiya.html', u'Regeneration will not run')],
)

A['webasto-f03'] = dict(
    title=u'Webasto F03 on the timer: on-board voltage',
    h1=u'Webasto F03: supply voltage too low or too high',
    desc=u'F03 on a Webasto is an on-board voltage problem, not a flame-out. Thresholds for the Air Top '
         u'2000 ST, the advice for the Thermo Top Evo and the driver\'s order of actions.',
    short=u'F03 speaks only of the on-board voltage: low or high, the timer does not say which. Flame-out '
          u'on the timer is F02. Start with the battery, the terminals and the fuse.',
    body=[
        (u'What F03 means', [
            u'The code does not distinguish "too little" from "too much": both are in one entry, and the '
            u'difference can be found by workshop diagnostics. For the Air Top 2000 ST the factory thresholds are:',
            ('tbl', [u'What', u'12 V system', u'24 V system', u'For how long'],
             [[u'Low voltage', u'below 10.5 V', u'below 21 V', u'more than 20 s'],
              [u'High voltage', u'above 16 V', u'above 32 V', u'more than 6 s']]),
            u'For other models look in the manual for your model. The factory advice in both cases is the '
            u'same: charge the battery.',
        ]),
        (u'Thermo Top Evo', [
            u'On the Thermo Top Evo F03 is also about the on-board voltage, too low or raised. The manual '
            u'advises charging the vehicle battery and then switching the heater off and on again.',
        ]),
        (u'Can you drive', [
            u'A heater is not an engine, and F03 by itself does not forbid driving. But the code points to '
            u'a power problem, and a discharged battery may fail to start the vehicle in the morning. Charge '
            u'or check it before the next overnight stop.',
        ]),
        (u'Order of actions', [
            ('ol', [u'Inspect the heater fuses and connectors, where the factory instruction starts. Look for '
                     u'corrosion, loose contacts, poor crimps, corroded wires and fuses.',
                    u'Inspect the battery terminals: corrosion, loose nuts.',
                    u'Charge the battery.',
                    u'Switch the heater off for at least 2 seconds and on again.']),
        ]),
        (u'When to see a workshop', [
            [u'F03 did not go away after charging the battery and checking contacts: the instruction advises '
             u'a check at a Webasto-trained service;',
             u'F03 keeps coming back with a charged battery.'],
        ]),
    ],
    faq=[
        (u'Is F03 on a Webasto a flame-out?',
         u'No. Flame-out on the timer shows as F02, while F03 is the on-board voltage.'),
        (u'At what voltage is F03 set on the Air Top 2000 ST?',
         u'Below 10.5 V (21 V on a 24 V system) for more than 20 seconds or above 16 V (32 V) for more than 6 seconds.'),
        (u'What should I do first?',
         u'Inspect the fuses and connectors, then the battery terminals, charge the battery and switch the '
         u'heater off and on with a pause of at least 2 seconds.'),
        (u'Why does the code stay with a charged battery?',
         u'Then workshop diagnostics are needed: the cause may be the wiring or the power connectors rather '
         u'than the battery itself.'),
    ],
    more=[(u'/en/otopiteli/webasto-f03.html', u'Webasto F03 - code page'),
          (u'/en/otopiteli/webasto-f02.html', u'F02 - flame-out'),
          (u'/en/otopiteli/webasto-f01.html', u'F01 - no start'),
          (u'/en/marki/webasto.html', u'All Webasto codes')],
)

A['webasto-f10'] = dict(
    title=u'Webasto F10 on the timer: heater overheating',
    h1=u'Webasto F10: the heater overheated - where to start',
    desc=u'F10 on the Air Top 2000 ST is an overheat lock-out. The factory checks: air intake, exhaust, '
         u'warm-air outlet, fuel system, and when a workshop is needed.',
    short=u'F10 is the heater\'s overheat lock-out, not an engine fault. The factory requires finding and '
          u'removing the cause of the overheating: first check the air intake, the exhaust and the warm-air outlet.',
    body=[
        (u'Which model this is about', [
            u'F10 in this sense applies to the Webasto Air Top 2000 ST and matches service codes 06 and 17. '
            u'On other models F10 may mean something else, so first find out the model.',
        ]),
        (u'What to inspect', [
            ('tbl', [u'What to check', u'What to look for'],
             [[u'Air intake and exhaust', u'Snow, ice, dirt, a crushed pipe'],
              [u'Warm-air outlet into the cab', u'Whether it is blocked'],
              [u'Fuel system', u'Leaks']]),
        ]),
        (u'Order of actions', [
            ('ol', [u'Inspect the air intake and the exhaust.',
                    u'Make sure the warm-air outlet into the cab is not blocked.',
                    u'Inspect the fuel system for leaks.',
                    u'Remove what you found and switch the heater on again.']),
            u'This is not an engine fault, but the factory wants the cause of the overheating found and '
            u'removed, not just the heater restarted.',
        ]),
        (u'When to see a workshop', [
            u'If air and exhaust are clear and the overheating repeats, the heat exchanger needs cleaning and '
            u'the overheat sensor checking.',
        ]),
    ],
    faq=[
        (u'What does F10 mean on a Webasto timer?',
         u'On the Air Top 2000 ST the overheat lock-out has triggered: the heater overheated and stopped.'),
        (u'Is it an engine fault?',
         u'No, it is the heater\'s overheat lock-out.'),
        (u'What should I check first?',
         u'The air intake and the exhaust (snow, ice, dirt, a crushed pipe), then the warm-air outlet into '
         u'the cab and the fuel system for leaks.'),
        (u'When is a workshop needed for F10?',
         u'If air and exhaust are clear and the overheating repeats: heat exchanger cleaning and an '
         u'overheat sensor check.'),
    ],
    more=[(u'/en/otopiteli/webasto-f10.html', u'Webasto F10 - code page'),
          (u'/en/otopiteli/webasto-f03.html', u'F03 - on-board voltage'),
          (u'/en/otopiteli/webasto-f02.html', u'F02 - flame-out'),
          (u'/en/marki/webasto.html', u'All Webasto codes')],
)

A['spn-100-davlenie-masla'] = dict(
    title=u'SPN 100: low oil pressure - do not drive',
    h1=u'SPN 100: oil pressure has dropped - shut the engine off',
    desc=u'SPN 100 is engine oil pressure in J1939. What FMI 1, 18, 3 and 4 mean, how to check the level '
         u'and the pressure with a gauge and when a workshop is needed.',
    short=u'With FMI 1 and 18 the oil pressure really is below normal and the engine must be shut off at '
          u'once: without oil the crankshaft and bearings wear out within minutes. FMI 3 and 4 concern the '
          u'sensor, but until the pressure is checked with a mechanical gauge, treat it as real.',
    body=[
        (u'FMI breakdown', [
            u'SPN 100 in the J1939 standard is Engine oil pressure.',
            ('tbl', [u'FMI', u'Meaning', u'What to do'],
             [[u'1', u'Pressure below normal, most severe level (Cummins ISB 6.7: FC 415)', u'Shut off the engine'],
              [u'18', u'Pressure below normal, medium urgency (Cummins ISB 6.7: FC 143)', u'Do not drive, find the cause'],
              [u'3', u'Sensor circuit voltage above normal or short to positive (Cummins FC 135)', u'Check connector and wiring'],
              [u'4', u'Sensor circuit voltage below normal or short to ground (Cummins FC 141)', u'Check connector and wiring']]),
            u'FMI 1 and 18 speak of the pressure itself, FMI 3 and 4 of the sensor\'s electrical circuit.',
        ]),
        (u'Can you drive', [
            u'No. With FMI 1 and 18 shut the engine off at once and do not push on "to the nearest place": '
            u'oil starvation destroys the crankshaft and bearings within minutes. With FMI 3 and 4 first '
            u'check whether the sensor is lying by fitting a mechanical gauge.',
        ]),
        (u'What the driver does', [
            ('ol', [u'Stop and shut off the engine.',
                    u'Wait a few minutes and check the oil level on the dipstick on level ground.',
                    u'Inspect the engine for oil leaks.',
                    u'Level is fine: screw a mechanical gauge in place of the sensor and compare with the dashboard.',
                    u'Gauge shows normal: the sensor or wiring is at fault, so inspect the connector and wires. '
                    u'No pressure: do not start the engine, call a tow truck.']),
        ]),
        (u'When to see a workshop', [
            [u'pressure is really low with a normal oil level: a clogged pickup screen, a worn oil pump or '
             u'bearings, fuel or coolant in the oil are possible;',
             u'FMI 3 or 4 repeats after the connector and wiring were checked: sensor and sensor supply line diagnostics are needed.'],
        ]),
    ],
    faq=[
        (u'Can I drive with SPN 100 FMI 1?',
         u'No. Shut the engine off at once: without oil pressure the crankshaft and bearings wear out within minutes.'),
        (u'How is FMI 18 different from FMI 1?',
         u'Both mean pressure below normal. FMI 1 is the most severe level, FMI 18 medium urgency; in both '
         u'cases you must not drive and must find the cause.'),
        (u'What do FMI 3 and 4 mean for SPN 100?',
         u'A fault in the sensor circuit (voltage above normal or short to positive, below normal or short '
         u'to ground), not proof that the oil is low.'),
        (u'How do I confirm the pressure is really low?',
         u'Screw a mechanical gauge in place of the sensor and compare the reading with the dashboard.'),
    ],
    more=[(u'/en/kody/spn-100.html', u'SPN 100 - oil pressure, all makes'),
          (u'/en/kody/spn-110.html', u'SPN 110 - coolant temperature'),
          (u'/en/kody/spn-97.html', u'SPN 97 - water in fuel')],
)

A['spn-110-peregrev'] = dict(
    title=u'SPN 110: engine overheating - what to do',
    h1=u'SPN 110: coolant temperature - when to stop',
    desc=u'SPN 110 is engine coolant temperature. A table of FMI 0, 15, 16, 3 and 4, how to check overheating '
         u'safely and when a workshop is needed.',
    short=u'With FMI 0, 15 and 16 treat the overheating as real: stop at the first safe opportunity and let '
          u'the engine cool. FMI 3 and 4 point to the sensor circuit, but until the temperature is checked '
          u'with a second thermometer, assume the overheating is real.',
    body=[
        (u'FMI breakdown', [
            u'SPN 110 in J1939 is Engine coolant temperature.',
            ('tbl', [u'FMI', u'Meaning', u'What to do'],
             [[u'0', u'Above normal, most severe level (Cummins ISB 6.7: FC 151)', u'Stop, let it cool'],
              [u'16', u'Above normal, medium urgency (Cummins FC 146)', u'Do not drive, find the cause'],
              [u'15', u'Above normal, low urgency (Cummins FC 2963)', u'Do not drive, find the cause'],
              [u'3', u'Sensor circuit voltage above normal or short to positive (Cummins FC 144)', u'Check connector and wiring'],
              [u'4', u'Sensor circuit voltage below normal or short to ground (Cummins FC 145)', u'Check connector and wiring']]),
            u'Temperature thresholds and the unit\'s reaction (warning, derate, shutdown) differ between '
            u'manufacturers: check the manual for your engine.',
        ]),
        (u'Can you drive', [
            u'No. The time reserve in overheating is measured in minutes, and pushing on "to the nearest '
            u'place" quickly destroys the cylinder head and gasket. With FMI 3 and 4 first check whether the '
            u'sensor is lying.',
        ]),
        (u'Order of actions', [
            ('ol', [u'Stop and let the engine cool.',
                    u'Do not open the expansion tank cap on a hot engine: the liquid under pressure is thrown out as steam.',
                    u'When cooled, check the coolant level, the fan belt and clutch, and radiator dirt.',
                    u'Compare the dashboard with an infrared thermometer on the upper radiator hose: a match means the overheating is real.',
                    u'No match: inspect the sensor connector and wiring; a break gives a falsely high '
                    u'voltage, a short gives a false overheat.']),
        ]),
        (u'When to see a workshop', [
            [u'temperature really is high with a normal coolant level: a faulty thermostat, pump, fan clutch '
             u'or an air lock after a coolant change are possible;',
             u'FMI 3 or 4 repeats after the connector and wiring were checked: diagnostics of the sensor and its circuit.'],
        ]),
    ],
    faq=[
        (u'Can I drive with SPN 110 FMI 0?',
         u'No. Stop at the first safe opportunity and let the engine cool.'),
        (u'Can I open the expansion tank cap?',
         u'Not on a hot engine: the liquid under pressure is thrown out as steam.'),
        (u'How do I tell real overheating from a sensor fault?',
         u'Compare the dashboard with an infrared thermometer on the upper radiator hose. If they match, '
         u'the overheating is real.'),
        (u'What do FMI 3 and 4 mean?',
         u'The sensor circuit: voltage above normal or short to positive (3), below normal or to ground (4). '
         u'It is not proof that the engine is overheated.'),
    ],
    more=[(u'/en/kody/spn-110.html', u'SPN 110 - coolant temperature'),
          (u'/en/kody/spn-111.html', u'SPN 111 - coolant level'),
          (u'/en/problemy/greetsya-v-goru.html', u'Overheating uphill'),
          (u'/en/kody/spn-100.html', u'SPN 100 - oil pressure')],
)

A['spn-1761-mochevina-adblue'] = dict(
    title=u'SPN 1761: low AdBlue level - you can drive, but not far',
    h1=u'SPN 1761: urea tank level - how far can you go',
    desc=u'SPN 1761 is the urea (AdBlue, DEF) tank level. A table of FMI 1, 17, 18, 3 and 4, how the '
         u'engine limits power and what the driver should do.',
    short=u'The engine will not stall in the middle of the road, but the unit applies protection in steps: '
          u'a lamp, then a power drop, then a speed limit. Top up the urea at the first opportunity.',
    body=[
        (u'What the code shows', [
            u'SPN 1761 in J1939 is Aftertreatment 1 Diesel Exhaust Fluid Tank Level: the level of the '
            u'exhaust treatment fluid in the tank.',
            ('tbl', [u'FMI', u'Meaning', u'What to do'],
             [[u'1', u'Level below normal, most severe', u'Top up urea'],
              [u'17', u'Below normal, low urgency (Cummins: FC 3497)', u'Top up urea'],
              [u'18', u'Below normal, medium urgency (Cummins: FC 3498)', u'Top up urgently'],
              [u'3', u'Sensor circuit voltage above normal or short to positive', u'Check connector and wiring'],
              [u'4', u'Sensor circuit voltage below normal or short to ground', u'Check connector and wiring']]),
            u'FMI 10, 11 and 13 are rarer: level changing too fast, cause not determined, sensor out of '
            u'calibration. FMI 1, 17 and 18 are about the level itself, FMI 3 and 4 about the sensor electrics.',
        ]),
        (u'How far can you go', [
            u'There is no universal "kilometres to the limit": the number of steps and when they engage '
            u'depend on the manufacturer, model year and the code itself. Usually a lamp comes on first, '
            u'then power drops, then speed may be limited. Exact thresholds are in your vehicle manual. So top '
            u'up the urea at the first opportunity and do not wait for the limits.',
        ]),
        (u'What the driver does', [
            ('ol', [u'Top up urea of the proper quality (not water) in the tank with the blue cap.',
                    u'Check whether the level on the dashboard rose and the code cleared. Sometimes the unit '
                    u'needs time or an ignition restart, and sometimes a workshop clears it with a scanner.',
                    u'For FMI 3 or 4, unplug the level sensor connector and inspect it: oxidation and urea '
                    u'crystals occur. Check the wires.',
                    u'Tank full but the code remains: the sensor or circuit is at fault, see a workshop.']),
        ]),
        (u'When to see a workshop', [
            [u'urea topped up but the dashboard level does not change or the code returns: level sensor and circuit diagnostics;',
             u'FMI 3 or 4 repeats after cleaning the connector: check the wiring and the unit;',
             u'do not disable the system or fit emulators: that does not remove the problem and codes keep piling up.'],
        ]),
    ],
    faq=[
        (u'Can I drive with SPN 1761?',
         u'Yes, but not far: the unit applies protection in steps - a lamp, then a power drop, then a speed '
         u'limit. Top up the urea at the first opportunity.'),
        (u'How many kilometres until the limit?',
         u'There is no single number; it depends on the manufacturer, model year and code. See your '
         u'vehicle manual.'),
        (u'What do FMI 3 and 4 mean for SPN 1761?',
         u'The level sensor\'s electrical circuit: voltage above normal or short to positive (3), below '
         u'normal or to ground (4). There may be enough urea.'),
        (u'The code stayed after topping up. What now?',
         u'Wait or restart the ignition; sometimes a workshop clears it with a scanner. If it returns, the '
         u'level sensor and its circuit need diagnostics.'),
    ],
    more=[(u'/en/kody/spn-1761.html', u'SPN 1761 - urea level'),
          (u'/en/kody/spn-100.html', u'SPN 100 - oil pressure'),
          (u'/en/kody/spn-110.html', u'SPN 110 - coolant temperature')],
)

A['planar-kod-29-sryv-plameni'] = dict(
    title=u'Planar code 29: flame-out during operation - what to check',
    h1=u'Planar went out while running: code 29 or three blinks',
    desc=u'Planar code 29 is flame-out during operation. How it looks on the PU-5 and PU-22, how it '
         u'differs from 78 and 13, what to check yourself and when a workshop is needed.',
    short=u'Code 29 (three blinks on the PU-5) means the flame went out during operation, not at start-up. '
          u'Causes per the manual: too little fuel, a faulty pump or a faulty flame indicator.',
    body=[
        (u'Which heaters and controllers it applies to', [
            u'Code 29 comes from Advers (Autoterm brand) factory documents for the Planar 2D, 4D, 8D and 9D '
            u'air heaters. Codes differ by model and controller, so what you see matters:',
            ('tbl', [u'What you look at', u'What is shown', u'Meaning'],
             [[u'Repair code table', u'Code 29; code 08 refers to 29', u'Flame-out during operation'],
              [u'PU-5, controller without a display', u'3 flashes of the red LED', u'Too many flame-outs during operation'],
              [u'PU-22, controller with a display', u'The number 29', u'Permitted number of flame-outs exceeded'],
              [u'Code 78 (also 3 blinks on the PU-5)', u'The number 78', u'Flame-out, air in the fuel system']]),
            u'Three blinks is not code 03: the repair table has no such code; three blinks match codes 29, '
            u'08 and 78. Two blinks on the PU-5 are already code 13 (did not start), and 13 blinks are code '
            u'35, flame-out on a voltage dip, only on the Planar 8DM.',
        ]),
        (u'What code 29 means', [
            u'The flame was interrupted while the heater was running. Per the factory manual the causes are: '
            u'insufficient fuel supply, a faulty fuel pump, a faulty flame indicator.',
        ]),
        (u'What to check yourself', [
            ('ol', [u'Fuel line: leaks, blockage, tight clamps.',
                    u'Air intake and exhaust pipe: the passage for combustion air and exhaust must be clear.',
                    u'The amount of fuel in the tank and the fuel supply to the heater.']),
            u'For code 78 the manual specifically names air in the fuel system; the checks are the same.',
        ]),
        (u'When a workshop is needed', [
            [u'the flame-out repeats after the fuel line, air intake and exhaust were checked;',
             u'the amount of fuel the pump delivers has to be checked and the pump replaced if necessary - per '
             u'the manual a separate repair operation;',
             u'if the heater then starts, the manual requires checking the flame indicator and replacing it if faulty.'],
        ]),
    ],
    faq=[
        (u'What does code 29 mean on a Planar?',
         u'Flame-out during operation: the flame in the combustion chamber went out while the heater was running.'),
        (u'Are three blinks on the PU-5 code 03?',
         u'No, the repair table has no such code. Three blinks match codes 29, 08 and 78.'),
        (u'How is code 78 different from 29?',
         u'The same flame-out, but for 78 the manual specifically names air in the fuel system.'),
        (u'What if the flame-out repeats?',
         u'After checking the fuel line, air intake and exhaust a workshop is needed: a check of pump '
         u'delivery and of the flame indicator.'),
    ],
    more=[(u'/en/otopiteli/planar-29.html', u'Code 29 - code page'),
          (u'/en/otopiteli/planar-78.html', u'Code 78 - flame-out, air in the fuel'),
          (u'/en/otopiteli/planar-13.html', u'Code 13 - failed to start'),
          (u'/en/marki/planar.html', u'All Planar codes')],
)

A['spn-102-davlenie-nadduva'] = dict(
    title=u'SPN 102: boost pressure - can you keep driving',
    h1=u'SPN 102: boost out of range - whistling, smoke, oil on the pipes',
    desc=u'SPN 102 is intake manifold pressure. A table of FMI 16, 18, 2, 3 and 4, how the engine '
         u'reacts, what to inspect and when a workshop is needed.',
    short=u'If power has dropped but there is no whistle, smoke or oil on the pipes, you can usually get to '
          u'base without load. Whistling, smoke or oil on the pipes: stop, a boost leak or a faulty turbo '
          u'will not clear by itself.',
    body=[
        (u'What the code means', [
            u'SPN 102 in J1939 is Engine intake manifold 1 pressure, i.e. the boost from the turbocharger.',
            ('tbl', [u'FMI', u'Meaning', u'What to do'],
             [[u'16', u'Boost above normal, medium urgency (Detroit DD13/DD15: "over-boost detected"; Cummins L9: FC 124)', u'Check the turbo wastegate and the sensor'],
              [u'18', u'Boost below normal, medium urgency (Detroit: "lower than expected under load"; Cummins L9: FC 125)', u'Look for an air leak and a blocked path'],
              [u'2', u'Data erratic or incorrect (Cummins ISB 6.7: FC 2973)', u'Check the sensor and connector'],
              [u'3', u'Sensor circuit voltage above normal or short to positive (Cummins ISB 6.7: FC 122)', u'Check connector and wiring'],
              [u'4', u'Sensor circuit voltage below normal or short to ground (Cummins ISB 6.7: FC 123)', u'Check connector and wiring']]),
            u'FMI 16 and 18 speak of the pressure itself, FMI 2, 3 and 4 of the sensor and its circuit. Until '
            u'the reading is verified, treat the boost as real. Thresholds differ between engines.',
        ]),
        (u'Can you drive', [
            u'The engine\'s reaction depends on the manufacturer. Per Foton and SITRAK factory tables, torque '
            u'is limited and black smoke appears with FMI 16 and 18. On the Detroit DD13 and DD15 the same '
            u'codes only light the lamps and the engine does not react.',
            [u'power dropped but there is no whistle, smoke or oil on the pipes: get to base without extra load and look for the cause at once;',
             u'you hear a whistle, see smoke or oil on the pipes: stop.'],
        ]),
        (u'What to inspect', [
            ('ol', [u'In a safe place inspect the pipes and clamps between the turbo, intercooler and intake '
                    u'manifold. Under load a leak is heard as a whistle.',
                    u'Check the intercooler for cracks and oil, the air filter for clogging.',
                    u'Look at the turbo actuator: the wastegate and its tubes. FMI 16 occurs when the valve '
                    u'does not open or the variable geometry is stuck.',
                    u'With the engine off and ignition on, compare the sensor reading with atmospheric '
                    u'pressure. On a Detroit the allowed difference is up to 10.3 kPa (1.5 psi); more, and '
                    u'you inspect the connector and replace the sensor.',
                    u'If there is oil on the pipes or the sensor port is clogged with carbon, remove and '
                    u'clean it, and look for the cause in the turbo.']),
        ]),
        (u'When to see a workshop', [
            [u'whistle, smoke or oil on the pipes: repair of the air path or the turbo;',
             u'the code repeats after inspecting the pipes, intercooler and turbo actuator: turbo and valve diagnostics;',
             u'FMI 2, 3 or 4 repeats after the connector and wiring were checked: diagnostics of the sensor and its 5 V supply line.'],
        ]),
    ],
    faq=[
        (u'Can I drive with SPN 102?',
         u'If power has dropped but there is no whistle, smoke or oil on the pipes, you can get to base '
         u'without extra load. With a whistle, smoke or oil, stop.'),
        (u'How is FMI 16 different from FMI 18?',
         u'FMI 16 is boost above normal (over-boost), FMI 18 below normal. Both are medium urgency.'),
        (u'What do FMI 2, 3 and 4 mean for SPN 102?',
         u'A fault of the sensor or its circuit, not necessarily of the turbo: check the connector and wiring first.'),
        (u'How do I check the pressure sensor?',
         u'With the engine off and ignition on, compare its reading with atmospheric pressure; on a Detroit '
         u'the allowed difference is up to 10.3 kPa (1.5 psi).'),
    ],
    more=[(u'/en/kody/spn-102.html', u'SPN 102 - intake manifold pressure'),
          (u'/en/kody/spn-105.html', u'SPN 105 - intake air temperature'),
          (u'/en/kody/spn-108.html', u'SPN 108 - barometric pressure'),
          (u'/en/kody/spn-107.html', u'SPN 107 - air filter differential pressure')],
)
