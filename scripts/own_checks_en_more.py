# -*- coding: utf-8 -*-
"""English twin of own_checks_more.py (second hundred: codes with 2–3 makes and a standard name).

Same kind of records as own_checks_en.py: узел, нормы, шаги, причины.
Figures are the same as in the Russian data; where the Russian says "по руководству
производителя", the English says "per the manufacturer's manual". Make names and
FMI values are kept as they are in the Russian file.
"""

CHECKS = {
    18: {
        "узел": "The low-pressure fuel sensor (extended range): it measures the pressure in the line before the high-pressure pump.",
        "нормы": [
            ("Signal with the engine off", "per the manufacturer's manual"),
            ("Line pressure by gauge", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (Renault: short to 0 V): check the connector and the wire from the sensor to the unit.",
            "FMI 16 (Sitrak: sensor zero offset above tolerance): check the connector; if it is clean — the sensor.",
            "Compare with a gauge on the line, if there is one.",
        ],
        "причины": [
            "Coarse fuel filter.",
            "The low-pressure sensor itself.",
            "Sensor connector or wire.",
        ],
    },

    69: {
        "узел": "The two-speed (range) axle switch: it tells the unit which range the axle is in. The unit takes it into account when choosing gears and speed.",
        "нормы": [
            ("Switch state when the axle range is changed", "changes on switching — per diagnostics"),
            ("Switch connector", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Switch the axle and watch the switch state in diagnostics.",
            "FMI 2 (International: switch fault): check the switch on the axle and its adjustment.",
            "FMI 9, 19 (KamAZ, Sitrak: the CCVS message over the bus arrives with gaps or the wrong length): see the general methods for the J1939 bus.",
        ],
        "причины": [
            "Axle range switch.",
            "Oxidised connector.",
            "Gaps on the CAN bus.",
        ],
    },

    70: {
        "узел": "The parking brake switch: it tells the unit whether the pneumatic parking brake is applied. Automatic application and protection against moving with the brake on depend on it.",
        "нормы": [
            ("Switch state with the brake applied and released", "changes with the brake — checked per diagnostics"),
            ("Parking brake circuit pressure", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Apply and release the parking brake on a stationary vehicle and watch the switch state in diagnostics.",
            "FMI 2, 13, 19 (unreliable signal, vehicle moving): if in doubt, stop at once; check the switch connector and the adjustment of the parking brake mechanism.",
            "FMI 9, 19 (over CAN, arriving with gaps): see the J1939 bus sections higher up the list — the general methods are the same.",
            "FMI 7 (circuit fault): check the parking brake air system for leaks with soapy water.",
        ],
        "причины": [
            "Stuck switch or its oxidised connector.",
            "Leak in the parking brake air system.",
            "Adjustment of the parking brake mechanism.",
            "CAN bus gaps from the brake unit.",
        ],
    },

    81: {
        "узел": "The inlet pressure sensor of the diesel particulate filter (DPF). From it the unit sees how clogged the filter is, and starts regeneration.",
        "нормы": [
            ("DPF inlet pressure in operation", "per diagnostics; rises as the filter clogs"),
            ("Sensor tube resistance", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Check the sensor tubes: whether they are clogged with soot or water.",
            "FMI 0, 1, 2, 3 (Sitrak: soot neutraliser clogged): check the filter for soot and the regeneration per the manual.",
            "The Renault line in the factory table is about battery voltage, not pressure. We do not use it here.",
        ],
        "причины": [
            "Clogged DPF.",
            "Clogged sensor tubes.",
            "Regeneration not carried out.",
            "The sensor itself.",
        ],
    },

    94: {
        "узел": "Fuel pressure in the supply system: a sensor on the line before the high-pressure pump. The unit uses it to see whether there is enough pressure for injection. Low pressure causes loss of power and stalling.",
        "нормы": [
            ("Fuel pressure at idle and under load", "per the manufacturer's manual"),
            ("Sensor signal with the engine off", "neither zero nor at plus — per diagnostics"),
        ],
        "шаги": [
            "FMI 1, 17 (low pressure, Foton): check the filters, the transfer pump and the air on the suction side (clear tube, bubbles).",
            "FMI 0, 1, 2, 3 (KamAZ: input shorted to plus or ground): unplug the sensor connector and measure to plus and to ground with the ignition on.",
            "FMI 0, 3, 4, 8 (Renault: injection pressure above normal): check the sensor and the pressure regulator; if it repeats — per the injection system troubleshooting guide.",
            "FMI 4, 6 (International: fuel supply limitation lamp): check the lamp and the fuel supply per the manual.",
        ],
        "причины": [
            "Clogged fuel filters.",
            "Air leak on the suction side.",
            "Transfer pump or pressure regulator.",
            "Pressure sensor or its connector.",
        ],
    },

    96: {
        "узел": "The fuel level sensor in the tank. It gives the level to the unit and to the dash. The dash readings and the low-level warning depend on it.",
        "нормы": [
            ("Dash reading with a full and an empty tank", "smooth from full to empty, without jumps"),
            ("Sensor resistance and connector", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Compare the dash reading with how much fuel was put in at refuelling. Jumps while driving — the float or the sensor contact.",
            "FMI 4, 5, 7, 9 (short to ground, open circuit, signal lost): unplug the sensor connector and check the ground and the wire.",
            "FMI 13, 19 (no signal from the sensor, Mercedes): check the connector at the tank and the wire to the unit.",
            "FMI 1, 12, 19 (Sitrak: level too low): if there is enough fuel — the sensor and the float; if little — refuel.",
        ],
        "причины": [
            "Float stuck.",
            "Oxidised sensor connector at the tank.",
            "Sensor ground or broken wire.",
            "Fuel sloshing in the tank gives jumping readings.",
        ],
    },

    103: {
        "узел": "The turbocharger speed sensor: it measures how fast the turbine turns. The unit uses it to monitor boost and to protect the turbine from overspeed.",
        "нормы": [
            ("Turbine speed under engine load", "rises with load — per diagnostics"),
            ("Turbine speed limit", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (KamAZ: short to ground): unplug the sensor connector and check the wire to ground.",
            "FMI 0 (Sitrak: overspeed): check the bypass valve and the boost — if the turbine has overspun, the cause is in the boost.",
            "Inspect the sensor for clearance to the teeth and for contamination.",
        ],
        "причины": [
            "Short in the sensor wiring.",
            "Turbo overspeed from the bypass.",
            "Clearance and dirt at the sensor.",
        ],
    },

    107: {
        "узел": "The air filter clogging sensor: it measures the pressure drop across the filter. The more the filter is clogged, the greater the drop, and the more the unit restricts the air supply.",
        "нормы": [
            ("Pressure drop across a clean filter", "minimal — per the manufacturer's manual"),
            ("Drop limit at which the filter is changed", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Inspect the filter: is it clogged, and when was it last changed? Clogged — change it.",
            "Blow through or check the sensor tubes: if they are clogged with dust or water, the drop reading will be false.",
            "FMI 0, 3, 4 (KamAZ, Mercedes: sensor or drop out of spec): unplug the sensor connector and check the wire.",
            "The Renault line in the factory table refers to the clutch sensor, not to the filter. We do not use it here.",
        ],
        "причины": [
            "Clogged air filter.",
            "Clogged sensor tube or water in it.",
            "Oxidised sensor connector.",
            "The sensor itself.",
        ],
    },

    135: {
        "узел": "The fuel supply pressure sensor: it measures the pressure in the line from the pump to the rail or the injection pump. Low pressure causes loss of power and hard starting.",
        "нормы": [
            ("Supply pressure with the engine running", "per the manufacturer's manual"),
            ("Sensor signal with the engine off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Compare the reading with a gauge at the test point on the line, if there is one.",
            "FMI 10 (Renault: open circuit): check the sensor connector and wire.",
            "FMI 11 (Sitrak: rail pressure below minimum): check the filters, the transfer pump and air leaks on the suction side.",
        ],
        "причины": [
            "Clogged fuel filters.",
            "Transfer pump.",
            "Air leak on the suction side.",
            "The pressure sensor itself.",
        ],
    },

    164: {
        "узел": "The injection control pressure sensor: it measures the pressure that controls the injectors. The unit adjusts it to the load; if it deviates, the engine runs rough or loses power.",
        "нормы": [
            ("Injection control pressure", "per the manufacturer's manual"),
            ("Reference voltage at the sensor connector", "5.0 V ± 0.25"),
        ],
        "шаги": [
            "Look at the pressure in diagnostics at idle and under load. Deviation from the set value — check the regulator and the pump.",
            "FMI 0, 7, 8, 12 (Renault: pressure above normal, regulation): check the pressure regulator and its connector; if it repeats — per the injection system troubleshooting guide.",
            "FMI 12 (Sitrak: regulator does not go to closed loop): check the regulator, the connector and the supply.",
            "The Foton line in the factory table refers to coolant temperature, not to pressure. We do not use it.",
        ],
        "причины": [
            "Pressure regulator or pump.",
            "Leak in the control line.",
            "Oxidised sensor connector.",
            "The pressure sensor itself.",
        ],
    },

    167: {
        "узел": "The alternator voltage (charging system) that the control unit sees. From it the unit knows whether the batteries are charging and whether there is enough supply for the actuators.",
        "нормы": [
            ("Two charged 12 V batteries, engine off", "25.2…25.6 V"),
            ("Engine running, alternator charging", "27.5…28.8 V"),
        ],
        "шаги": [
            "Measure the battery terminal voltage with the engine off and with it running; compare with the norms above.",
            "FMI 1, 16, 18 (critically low alternator voltage): check the belt, the wire from the alternator and the regulator.",
            "FMI 3, 4 (Sitrak: vehicle system voltage above the limit): the alternator regulator. Above 29.5 V — the regulator.",
            "FMI 1, 16, 18 (DAF: low ECU supply voltage): the unit's terminals and grounds.",
        ],
        "причины": [
            "Alternator regulator.",
            "Belt or the wire from the alternator.",
            "Worn or discharged batteries.",
            "Oxidised terminals and grounds.",
        ],
    },

    177: {
        "узел": "The gearbox oil temperature sensor: the gearbox unit and the dash get the oil temperature. The unit flags gearbox overheating in advance.",
        "нормы": [
            ("Gearbox oil temperature", "per the manufacturer's manual"),
            ("Oil level on the dipstick", "within the marks per the manual"),
        ],
        "шаги": [
            "Check the gearbox oil level and condition with the dipstick, or per the manual.",
            "FMI 0 (International: readings above normal): check whether the gearbox is actually overheated, and the sensor itself.",
            "FMI 12 (Sitrak: no TRF1 frame on the bus): see the general J1939 bus methods higher up the list.",
        ],
        "причины": [
            "Low level or contaminated oil.",
            "Gearbox overheating.",
            "The sensor itself.",
            "CAN bus gaps.",
        ],
    },

    191: {
        "узел": "A J1939 message: the gearbox output shaft speed (ETC1 message from the gearbox unit). The gearbox unit must send it. Units that need it do not see this signal when the message drops out.",
        "нормы": [
            ("Message arrives regularly, without gaps", "checked per diagnostics; gaps are a fault"),
            ("CAN-H and CAN-L resistance, power off", "about 60 Ω"),
        ],
        "шаги": [
            "Read the codes of all units. If many have them — look at the bus; if one unit is silent — look at that unit.",
            "Measure the supply and the ground of the unit that should send the message. Without power the unit is silent.",
            "FMI 9, 13 (message missing): inspect this unit's connector on the CAN bus for oxidation and a chafed wire. Disconnect the units one at a time and see whether the message returns.",
            "FMI 12 (no frame, timeout expired) and FMI 19 (frame of wrong length): check the software version of the sending unit and its parameter settings; for units of different makes these are different actions.",
        ],
        "причины": [
            "Sending unit without power or with faulty software.",
            "Oxidation or a broken wire in the CAN connector.",
            "Added equipment interfering with the bus.",
            "Wrong parameter setting of the unit.",
        ],
    },

    524: {
        "узел": "A J1939 message: the selected gear of the gearbox (ETC2 message from the gearbox unit). The gearbox unit must send it. Units that need it do not see this signal when the message drops out.",
        "нормы": [
            ("Message arrives regularly, without gaps", "checked per diagnostics; gaps are a fault"),
            ("CAN-H and CAN-L resistance, power off", "about 60 Ω"),
        ],
        "шаги": [
            "Read the codes of all units. If many have them — look at the bus; if one unit is silent — look at that unit.",
            "Measure the supply and the ground of the unit that should send the message. Without power the unit is silent.",
            "FMI 9, 13 (message missing): inspect this unit's connector on the CAN bus for oxidation and a chafed wire. Disconnect the units one at a time and see whether the message returns.",
            "FMI 12 (no frame, timeout expired) and FMI 19 (frame of wrong length): check the software version of the sending unit and its parameter settings; for units of different makes these are different actions.",
        ],
        "причины": [
            "Sending unit without power or with faulty software.",
            "Oxidation or a broken wire in the CAN connector.",
            "Added equipment interfering with the bus.",
            "Wrong parameter setting of the unit.",
        ],
    },

    533: {
        "узел": "Exceeding the maximum crankshaft speed: the unit records engine overspeed and may cut the fuel. The code means the speed was exceeded, or the speed sensor is giving a false signal.",
        "нормы": [
            ("Crankshaft speed limit", "per the manufacturer's manual"),
            ("Speed sensor signal with the engine running", "smooth, without jumps — per diagnostics"),
        ],
        "шаги": [
            "Think back: was there an overspeed — driving in a low gear downhill, a late change up?",
            "Check the crankshaft speed sensor: signal jumps at idle mean the sensor or the clearance at the ring gear.",
            "Inspect the sensor connector and the wire: a chafed wire gives false speed.",
        ],
        "причины": [
            "A real engine overspeed.",
            "Crankshaft speed sensor.",
            "Chafed sensor wire.",
        ],
    },

    599: {
        "узел": "The cruise control set button (SET/RESUME, 'CC−' per the factory table). The unit gets its state from the control panel or the steering wheel.",
        "нормы": [
            ("Button state when pressed and released", "changes without jumps — checked per diagnostics"),
            ("Button at rest", "no signal until the button is pressed"),
        ],
        "шаги": [
            "FMI 2 (switch fault): with the ignition on, press each button in turn and watch the state in diagnostics. A button that sticks — replace the switch.",
            "FMI 9, 19 (signal arrives with gaps): turn the steering wheel by hand and watch whether the signal drops out. If it drops out on turning — the steering wheel spiral cable.",
            "Inspect the connector under the steering wheel: oxidation and water. The switch itself — if the connector is in order.",
        ],
        "причины": [
            "Stuck or dirty button.",
            "Steering wheel spiral cable.",
            "Oxidised connector under the steering wheel.",
            "Poor supply to the control panel.",
        ],
    },

    600: {
        "узел": "The cruise control deceleration button ('reduce' per the factory table). The unit gets its state from the control panel or the steering wheel.",
        "нормы": [
            ("Button state when pressed and released", "changes without jumps — checked per diagnostics"),
            ("Button at rest", "no signal until the button is pressed"),
        ],
        "шаги": [
            "FMI 2 (switch fault): with the ignition on, press each button in turn and watch the state in diagnostics. A button that sticks — replace the switch.",
            "FMI 9, 19 (signal arrives with gaps): turn the steering wheel by hand and watch whether the signal drops out. If it drops out on turning — the steering wheel spiral cable.",
            "Inspect the connector under the steering wheel: oxidation and water. The switch itself — if the connector is in order.",
        ],
        "причины": [
            "Stuck or dirty button.",
            "Steering wheel spiral cable.",
            "Oxidised connector under the steering wheel.",
            "Poor supply to the control panel.",
        ],
    },

    602: {
        "узел": "The cruise control acceleration button ('increase' per the factory table). The unit gets its state from the control panel or the steering wheel.",
        "нормы": [
            ("Button state when pressed and released", "changes without jumps — checked per diagnostics"),
            ("Button at rest", "no signal until the button is pressed"),
        ],
        "шаги": [
            "FMI 2 (switch fault): with the ignition on, press each button in turn and watch the state in diagnostics. A button that sticks — replace the switch.",
            "FMI 9, 19 (signal arrives with gaps): turn the steering wheel by hand and watch whether the signal drops out. If it drops out on turning — the steering wheel spiral cable.",
            "Inspect the connector under the steering wheel: oxidation and water. The switch itself — if the connector is in order.",
        ],
        "причины": [
            "Stuck or dirty button.",
            "Steering wheel spiral cable.",
            "Oxidised connector under the steering wheel.",
            "Poor supply to the control panel.",
        ],
    },

    603: {
        "узел": "The second brake pedal switch (the pedal press contact). From it the units learn that the pedal is pressed. It works separately from the first switch.",
        "нормы": [
            ("Signal 'pressed' and 'not pressed'", "changes when the pedal is pressed"),
            ("Brake pedal adjustment", "per the manufacturer's manual"),
        ],
        "шаги": [
            "With the ignition off, unplug the switch connector and see whether the code goes away: a ground on the signal means the switch or the wiring.",
            "Press the pedal and watch the switch state in diagnostics: it should change.",
            "Pedal adjustment — check the pedal travel per the manual.",
        ],
        "причины": [
            "Brake pedal switch.",
            "Short to ground in the wiring.",
            "Pedal adjustment.",
        ],
    },

    604: {
        "узел": "The gearbox neutral switch: it tells the unit whether the gearbox is in neutral. Starting and some automatic gearbox functions depend on it.",
        "нормы": [
            ("Switch state in neutral and in any gear", "in neutral — 'neutral', in gear — 'not neutral', without delays"),
            ("Selector lever or rod adjustment", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Put the gearbox in neutral with the ignition on and watch the state in diagnostics. If it does not change, the switch or its contact is jammed (per the factory line, the contact is in the open or closed position).",
            "FMI 2 (switch fault): check the switch connector on the gearbox — oxidation and water.",
            "Check the adjustment of the selector lever and rods: the switch operates from the rod position.",
        ],
        "причины": [
            "Jammed neutral switch contact.",
            "Oxidised connector on the gearbox.",
            "Wrong adjustment of the lever or rods.",
            "Sticking switch rod on the gearbox.",
        ],
    },

    632: {
        "узел": "Fuel cut-off valve No. 1: a solenoid valve on the low-pressure line. The unit closes it when the fuel supply has to be shut off.",
        "нормы": [
            ("Valve winding resistance", "per the manufacturer's manual"),
            ("Valve state when running and when stopped", "open when the engine runs — per diagnostics"),
        ],
        "шаги": [
            "FMI 5 (KamAZ: cut-off valve circuit open): check the valve connector and the winding resistance per the manual.",
            "FMI 3 (Sitrak: low-pressure solenoid valve shorted to supply): unplug the valve connector with the ignition off, then switch it on. If the code goes — the valve; if it stays — the wiring.",
        ],
        "причины": [
            "Solenoid cut-off valve.",
            "Short to supply or open circuit in the wiring.",
            "Oxidised valve connector.",
        ],
    },

    633: {
        "узел": "The injection pump valve (solenoid valve) controlling fuel delivery: the unit uses it to regulate the fuel supplied to the high-pressure pump.",
        "нормы": [
            ("Solenoid valve resistance", "per the manufacturer's manual"),
            ("Internal ECU faults", "absent when the valve is in good order"),
        ],
        "шаги": [
            "Measure the resistance of the injection pump valve with the ignition off and compare with the manual.",
            "FMI 31 (internal ECU fault, DAF, or unreliable valve resistance, Dongfeng): check the valve and its connector.",
            "FMI 7 (Isuzu: rail pressure limiting valve opened): check the rail pressure limiting valve and the rail.",
        ],
        "причины": [
            "Solenoid valve of the injection pump.",
            "Oxidised valve connector.",
            "Rail pressure limiting valve.",
            "Control unit.",
        ],
    },

    657: {
        "узел": "Cylinder No. 7 injector: it injects fuel into this cylinder. The unit controls it electrically through the power stage. The code refers to this cylinder.",
        "нормы": [
            ("Injector winding resistance and connector", "per the manufacturer's manual"),
            ("Cylinder No. 7 at idle", "smooth, per diagnostics, without misfires"),
        ],
        "шаги": [
            "FMI 3, 5, 6, 7 (KamAZ: injector fault or warning): unplug the injector connector, inspect the contacts and check the wire to the unit for continuity.",
            "FMI 3, 8, 11, 12 (MAZ and YaMZ: negative wire shorted to the battery in the injector circuit): unplug the injector connector and watch the code. If the code goes — the wiring to the unit; if it stays — the injector or the unit.",
            "Swap the injector connector with the neighbouring cylinder's: if the code moves — the injector; if it stays — the wiring.",
        ],
        "причины": [
            "Cylinder No. 7 injector.",
            "Negative wire shorted to the battery in the injector wiring.",
            "Oxidised injector connector.",
            "Injector control unit.",
        ],
    },

    658: {
        "узел": "Cylinder No. 8 injector: it injects fuel into this cylinder. The unit controls it electrically through the power stage. The code refers to this cylinder.",
        "нормы": [
            ("Injector winding resistance and connector", "per the manufacturer's manual"),
            ("Cylinder No. 8 at idle", "smooth, per diagnostics, without misfires"),
        ],
        "шаги": [
            "FMI 3, 5, 6, 7 (KamAZ: injector fault or warning): unplug the injector connector, inspect the contacts and check the wire to the unit for continuity.",
            "FMI 3, 8, 11, 12 (MAZ and YaMZ: negative wire shorted to the battery in the injector circuit): unplug the injector connector and watch the code. If the code goes — the wiring to the unit; if it stays — the injector or the unit.",
            "Swap the injector connector with the neighbouring cylinder's: if the code moves — the injector; if it stays — the wiring.",
        ],
        "причины": [
            "Cylinder No. 8 injector.",
            "Negative wire shorted to the battery in the injector wiring.",
            "Oxidised injector connector.",
            "Injector control unit.",
        ],
    },

    701: {
        "узел": "Additional control unit output No. 1: it switches the differential lock. The number in the factory table is the unit's internal number, which does not match across makes. So the search is by the circuit, not by the number: what is connected to this output — check against the manual.",
        "нормы": [
            ("Output voltage with the load off", "about zero"),
            ("Load resistance (valve or relay)", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3, 4 (3 — short to plus, 4 — to ground): with the ignition off, unplug the load connector and switch the ignition on. If the code stays — a short in the wiring to the load. If the code goes — the load is faulty.",
            "FMI 5 (open circuit): check the wire from the output to the load, and measure the load resistance; compare with the manual.",
            "Factory table entries: Meritor — differential lock; Mercedes — digital output 3/07. Before replacing anything, check which load is actually fitted to this output.",
        ],
        "причины": [
            "Breakdown or overheating of the valve or load relay.",
            "Wire in the harness chafed at the bends.",
            "Oxidised load connector.",
            "Short to plus in the trailer harness or in the cab wiring.",
        ],
    },

    702: {
        "узел": "Additional control unit output No. 2: it switches the transfer case lock. The number in the factory table is the unit's internal number, which does not match across makes. So the search is by the circuit, not by the number: what is connected to this output — check against the manual.",
        "нормы": [
            ("Output voltage with the load off", "about zero"),
            ("Load resistance (valve or relay)", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3, 4 (3 — short to plus, 4 — to ground): with the ignition off, unplug the load connector and switch the ignition on. If the code stays — a short in the wiring to the load. If the code goes — the load is faulty.",
            "FMI 5 (open circuit): check the wire from the output to the load and measure the load resistance; compare with the manual.",
            "Factory table entries: Meritor — transfer case lock; Mercedes — digital output 3/08. Before replacing anything, check which load is actually fitted to this output.",
        ],
        "причины": [
            "Breakdown or overheating of the valve or load relay.",
            "Wire in the harness chafed at the bends.",
            "Oxidised load connector.",
            "Short to plus in the trailer harness or in the cab wiring.",
        ],
    },

    703: {
        "узел": "Additional control unit output No. 3: it switches the trailer modulator (IV). The number in the factory table is the unit's internal number, which does not match across makes. So the search is by the circuit, not by the number: what is connected to this output — check against the manual.",
        "нормы": [
            ("Output voltage with the load off", "about zero"),
            ("Load resistance (valve or relay)", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3, 4 (3 — short to plus, 4 — to ground): with the ignition off, unplug the load connector and switch the ignition on. If the code stays — a short in the wiring to the load. If the code goes — the load is faulty.",
            "FMI 5 (open circuit): check the wire from the output to the load and measure the load resistance; compare with the manual.",
            "Factory table entries: Meritor — trailer modulator IV; Mercedes — digital output 3/09. Before replacing anything, check which load is actually fitted to this output.",
        ],
        "причины": [
            "Breakdown or overheating of the valve or load relay.",
            "Wire in the harness chafed at the bends.",
            "Oxidised load connector.",
            "Short to plus in the trailer harness or in the cab wiring.",
        ],
    },

    704: {
        "узел": "Additional control unit output No. 4: it switches the trailer modulator (OV). The number in the factory table is the unit's internal number, which does not match across makes. So the search is by the circuit, not by the number: what is connected to this output — check against the manual.",
        "нормы": [
            ("Output voltage with the load off", "about zero"),
            ("Load resistance (valve or relay)", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3, 4 (3 — short to plus, 4 — to ground): with the ignition off, unplug the load connector and switch the ignition on. If the code stays — a short in the wiring to the load. If the code goes — the load is faulty.",
            "FMI 5 (open circuit): check the wire from the output to the load and measure the load resistance; compare with the manual.",
            "Factory table entries: Meritor — trailer modulator OV; Mercedes — digital output 4/07. Before replacing anything, check which load is actually fitted to this output.",
        ],
        "причины": [
            "Breakdown or overheating of the valve or load relay.",
            "Wire in the harness chafed at the bends.",
            "Oxidised load connector.",
            "Short to plus in the trailer harness or in the cab wiring.",
        ],
    },

    705: {
        "узел": "Additional control unit output No. 5: it switches the 3/2 pressure regulator valve. The number in the factory table is the unit's internal number, which does not match across makes. So the search is by the circuit, not by the number: what is connected to this output — check against the manual.",
        "нормы": [
            ("Output voltage with the load off", "about zero"),
            ("Load resistance (valve or relay)", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3, 4 (3 — short to plus, 4 — to ground): with the ignition off, unplug the load connector and switch the ignition on. If the code stays — a short in the wiring to the load. If the code goes — the load is faulty.",
            "FMI 5 (open circuit): check the wire from the output to the load and measure the load resistance; compare with the manual.",
            "Factory table entries: Meritor — 3/2 pressure regulator valve; on KamAZ this number is a different valve — a gas lock, check. Before replacing anything, check which load is actually fitted to this output.",
        ],
        "причины": [
            "Breakdown or overheating of the valve or load relay.",
            "Wire in the harness chafed at the bends.",
            "Oxidised load connector.",
            "Short to plus in the trailer harness or in the cab wiring.",
        ],
    },

    706: {
        "узел": "Additional control unit output No. 6: it switches the 3/2 air dryer regeneration valve. The number in the factory table is the unit's internal number, which does not match across makes. So the search is by the circuit, not by the number: what is connected to this output — check against the manual.",
        "нормы": [
            ("Output voltage with the load off", "about zero"),
            ("Load resistance (valve or relay)", "per the manufacturer's manual"),
        ],
        "шаги": [
            "KamAZ entry: proportional valve 6 — open circuit; check the valve and the wire.",
            "FMI 3, 4 (3 — short to plus, 4 — to ground): with the ignition off, unplug the load connector and switch the ignition on. If the code stays — a short in the wiring to the load. If the code goes — the load is faulty.",
            "FMI 5 (open circuit): check the wire from the output to the load and measure the load resistance; compare with the manual.",
            "Factory table entries: Meritor — 3/2 air dryer regeneration valve; on KamAZ this number is a proportional valve, check. Before replacing anything, check which load is actually fitted to this output.",
        ],
        "причины": [
            "Breakdown or overheating of the valve or load relay.",
            "Wire in the harness chafed at the bends.",
            "Oxidised load connector.",
            "Short to plus in the trailer harness or in the cab wiring.",
        ],
    },

    746: {
        "узел": "Solenoid differential lock valve No. 1: on an electrical command it feeds air to the differential lock.",
        "нормы": [
            ("Lock engages on command", "yes — per diagnostics"),
            ("Valve winding resistance", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (short to ground, Knorr-Bremse and MAN): disconnect the valve with the ignition off and watch the code. If the code goes — the valve; if it stays — the wiring.",
            "Check the air supply to the valve, and look for leaks at the joints with soapy water.",
        ],
        "причины": [
            "Solenoid lock valve.",
            "Short to ground in the wiring.",
            "Air leak in the lock air system.",
        ],
    },

    776: {
        "узел": "Speed sensor of the torque converter turbine wheel. From it the unit sees how the turbine turns, and engages or disengages the torque converter lock-up. The code name refers to the lock-up drive, but the factory lines are about turbine speed, so we go by those.",
        "нормы": [
            ("Turbine wheel speed on pull-away", "rises with vehicle speed — per diagnostics"),
            ("Sensor clearance to the teeth", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Compare the turbine speed with the vehicle's movement when pulling away. Zero or jumping — the sensor.",
            "FMI 2, 255 (unreliable speed): check the sensor connector and the clearance to the teeth; a dirty magnet gives faults.",
            "Inspect the sensor for swarf and metal dust: they disturb the signal.",
        ],
        "причины": [
            "Turbine speed sensor.",
            "Clearance of the sensor to the teeth.",
            "Swarf and dirt on the sensor.",
            "Chafed wire.",
        ],
    },

    802: {
        "узел": "Relay of diagonal 1: it supplies the power circuit of the valves and ABS modulators of the first brake diagonal.",
        "нормы": [
            ("Voltage at the power terminals of the ABS unit, ignition on", "as at the battery, without sags"),
            ("Voltage at the modulator output with the ignition off", "none"),
        ],
        "шаги": [
            "FMI 3, 4 (Bendix: the common modulator wire shorted to supply): disconnect the modulators of this diagonal one at a time and watch the code.",
            "FMI 2, 3, 4, 12 (Renault: short at the power terminals of the EBS unit, or loss of ground for part of the ABS functions): check the unit's ground and the power terminals.",
            "FMI 4, 5, 7 (Wabco: supply voltage too low): check the terminals and the power wires of the unit.",
        ],
        "причины": [
            "Burnt diagonal relay.",
            "Loss of ground at the ABS or EBS unit.",
            "Short to supply in the modulator.",
            "Oxidised power terminals.",
        ],
    },

    803: {
        "узел": "Relay of diagonal 2: it supplies the power circuit of the ABS valves and modulators of one brake diagonal.",
        "нормы": [
            ("Voltage at the power terminals of the ABS unit, ignition on", "as at the battery, without sags"),
            ("Voltage at the modulator output with the ignition off", "none"),
        ],
        "шаги": [
            "FMI 3, 4, 5, 6 (Wabco: modulator output shorted to supply): disconnect the modulators of this diagonal one at a time and watch the code.",
            "FMI 2, 3, 4 (Renault: fault in some functions due to ground): check the ABS unit's ground and power terminals.",
            "Relay — if the contacts are burnt, replace the relay; if not — the wiring.",
        ],
        "причины": [
            "Burnt diagonal relay.",
            "ABS unit ground.",
            "Short to supply in the modulator.",
            "Chafed wire.",
        ],
    },

    806: {
        "узел": "The ASR (anti-slip regulation) valve of the driven axle: on command from the unit it engages the differential lock of the driven axle, so that one wheel does not spin.",
        "нормы": [
            ("ASR valve operation on command", "yes, on switching — checked per diagnostics and on the bench"),
            ("Valve inlet pressure", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3, 4, 5, 13 (short to supply or open circuit): unplug the valve with the ignition off and switch it on. If the code goes — the valve; if it stays — the wiring.",
            "Check the ASR valve pneumatically: supply present, but no pressure after the valve on command — the valve is not opening.",
            "Check the valve's joints for leaks with soapy water.",
        ],
        "причины": [
            "ASR valve with a sticking spool.",
            "Short to supply in the harness to the valve.",
            "Air leak at the valve joints.",
            "ABS modulator of the driven axle (per the Wabco factory line).",
        ],
    },

    807: {
        "узел": "The ASR (anti-slip regulation) valve of the front axle (differential 2 per the factory table). It works on the same principle as the driven-axle valve and is controlled by the same ABS/EBS unit.",
        "нормы": [
            ("ASR valve operation on command", "yes — checked per diagnostics"),
            ("Valve inlet pressure", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3, 4, 5, 13 (short to supply or open circuit): disconnect the valve and watch the code, as for the driven-axle valve (code 806).",
            "FMI 1, 2, 3, 4 (Wabco: front-axle ABS modulator, short to supply): check the modulator of this axle.",
            "Check the valve's joints for leaks with soapy water.",
        ],
        "причины": [
            "ASR valve of the front axle.",
            "Short to supply in the harness.",
            "Air leak at the joints.",
            "ABS modulator of the front axle.",
        ],
    },

    904: {
        "узел": "A J1939 message: front axle speed (EBC2 message from the brake unit). The brake unit (EBS/ABS) must send it. Units that need it do not see this signal when the message drops out.",
        "нормы": [
            ("Message arrives regularly, without gaps", "checked per diagnostics; gaps are a fault"),
            ("CAN-H and CAN-L resistance, power off", "about 60 Ω"),
        ],
        "шаги": [
            "Read the codes of all units. If many have them — look at the bus; if one unit is silent — look at that unit.",
            "Measure the supply and the ground of the unit that should send the message. Without power the unit is silent.",
            "FMI 9, 13 (message missing): inspect this unit's connector on the CAN bus for oxidation and a chafed wire. Disconnect the units one at a time and see whether the message returns.",
            "FMI 12 (no frame, timeout expired) and FMI 19 (frame of wrong length): check the software version of the sending unit and its parameter settings; for units of different makes these are different actions.",
        ],
        "причины": [
            "Sending unit without power or with faulty software.",
            "Oxidation or a broken wire in the CAN connector.",
            "Added equipment interfering with the bus.",
            "Wrong parameter setting of the unit.",
        ],
    },

    932: {
        "узел": "The solenoid valve of the ABS modulator, inlet valve (axle 1, left wheel). The inlet valve stops pressure from reaching the brake chamber when the ABS is holding the wheel. It sits in the modulator at the wheel of this axle.",
        "нормы": [
            ("Valve winding resistance", "per the manufacturer's manual"),
            ("Unit output voltage with the valve off", "no voltage; a voltage at plus means a short"),
        ],
        "шаги": [
            "FMI 5, 6, 7, 10 (per the factory table — short to ground): unplug the modulator connector, inspect the contacts, and measure the winding resistance of this valve and of the valve of the other wheel on the same axle. The difference is a reason to replace the valve.",
            "Disconnect the valve connector with the ignition off, then switch the ignition on. If the code goes — the problem is in the wiring to the valve. If it stays — the valve or the modulator.",
            "Check the modulator for leaks with soapy water at the valve outlet while holding pressure.",
            "If the wheel has the same codes on both valves — the cause is common: the unit's ground or the modulator's power.",
        ],
        "причины": [
            "Oxidised or water-filled modulator connector.",
            "Short to ground in the harness along the frame.",
            "Valve with a contaminated seat.",
            "ABS unit sending a wrong signal to the valve.",
        ],
    },

    933: {
        "узел": "The solenoid valve of the ABS modulator, inlet valve (axle 1, right wheel). The inlet valve stops pressure from reaching the brake chamber when the ABS is holding the wheel. It sits in the modulator at the wheel of this axle.",
        "нормы": [
            ("Valve winding resistance", "per the manufacturer's manual"),
            ("Unit output voltage with the valve off", "no voltage; a voltage at plus means a short"),
        ],
        "шаги": [
            "FMI 5, 6, 7, 10 (per the factory table — short to ground): unplug the modulator connector, inspect the contacts, and measure the winding resistance of this valve and of the valve of the other wheel on the same axle. The difference is a reason to replace the valve.",
            "Disconnect the valve connector with the ignition off, then switch the ignition on. If the code goes — the problem is in the wiring to the valve. If it stays — the valve or the modulator.",
            "Check the modulator for leaks with soapy water at the valve outlet while holding pressure.",
            "If the wheel has the same codes on both valves — the cause is common: the unit's ground or the modulator's power.",
        ],
        "причины": [
            "Oxidised or water-filled modulator connector.",
            "Short to ground in the harness along the frame.",
            "Valve with a contaminated seat.",
            "ABS unit sending a wrong signal to the valve.",
        ],
    },

    938: {
        "узел": "The solenoid valve of the ABS modulator, release valve (axle 1, left wheel). The release valve lets pressure out of the chamber when the ABS releases the wheel. It sits in the modulator at the wheel of this axle.",
        "нормы": [
            ("Valve winding resistance", "per the manufacturer's manual"),
            ("Unit output voltage with the valve off", "no voltage; a voltage at plus means a short"),
        ],
        "шаги": [
            "FMI 5, 6, 7, 10 (per the factory table — short to ground): unplug the modulator connector, inspect the contacts, and measure the winding resistance of this valve and of the valve of the other wheel on the same axle. The difference is a reason to replace the valve.",
            "Disconnect the valve connector with the ignition off, then switch the ignition on. If the code goes — the problem is in the wiring to the valve. If it stays — the valve or the modulator.",
            "Check the modulator for leaks with soapy water at the valve outlet while holding pressure.",
            "If the wheel has the same codes on both valves — the cause is common: the unit's ground or the modulator's power.",
        ],
        "причины": [
            "Oxidised or water-filled modulator connector.",
            "Short to ground in the harness along the frame.",
            "Valve with a contaminated seat.",
            "ABS unit sending a wrong signal to the valve.",
        ],
    },

    939: {
        "узел": "The solenoid valve of the ABS modulator, release valve (axle 1, right wheel). The release valve lets pressure out of the chamber when the ABS releases the wheel. It sits in the modulator at the wheel of this axle.",
        "нормы": [
            ("Valve winding resistance", "per the manufacturer's manual"),
            ("Unit output voltage with the valve off", "no voltage; a voltage at plus means a short"),
        ],
        "шаги": [
            "FMI 5, 6, 7, 10 (per the factory table — short to ground): unplug the modulator connector, inspect the contacts, and measure the winding resistance of this valve and of the valve of the other wheel on the same axle. The difference is a reason to replace the valve.",
            "Disconnect the valve connector with the ignition off, then switch the ignition on. If the code goes — the problem is in the wiring to the valve. If it stays — the valve or the modulator.",
            "Check the modulator for leaks with soapy water at the valve outlet while holding pressure.",
            "If the wheel has the same codes on both valves — the cause is common: the unit's ground or the modulator's power.",
        ],
        "причины": [
            "Oxidised or water-filled modulator connector.",
            "Short to ground in the harness along the frame.",
            "Valve with a contaminated seat.",
            "ABS unit sending a wrong signal to the valve.",
        ],
    },

    973: {
        "узел": "The engine brake stage selector switch: the engine unit uses it to know which engine brake stage the driver has selected on the panel or the lever.",
        "нормы": [
            ("Switch state when changing stages", "each stage gives its own state, without jumps"),
            ("Switch connector", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Switch the stages in turn and watch the state in diagnostics — one stage should change at a time.",
            "FMI 2 (switch fault, International): check the switch on the panel, the button sticking and the connector.",
            "FMI 2, 9 (Mercedes: retarder lever position unreliable): check the lever and its connector.",
            "FMI 9, 19 (KamAZ: message over the bus arrives with gaps): see the general methods for the J1939 bus.",
        ],
        "причины": [
            "Stuck or dirty stage switch.",
            "Oxidised panel connector.",
            "Gaps on the CAN bus.",
        ],
    },

    986: {
        "узел": "A J1939 message: the required fan speed in per cent (it reports the speed the fan should run at). The engine unit or the fan control unit must send it. Units that need it do not see this signal when the message drops out.",
        "нормы": [
            ("Message arrives regularly, without gaps", "checked per diagnostics; gaps are a fault"),
            ("CAN-H and CAN-L resistance, power off", "about 60 Ω"),
        ],
        "шаги": [
            "FMI 2 (fan switch fault on the panel, International): check the switch and its connector.",
            "Read the codes of all units. If many have them — look at the bus; if one unit is silent — look at that unit.",
            "Measure the supply and the ground of the unit that should send the message. Without power the unit is silent.",
            "FMI 9, 13 (message missing): inspect this unit's connector on the CAN bus for oxidation and a chafed wire. Disconnect the units one at a time and see whether the message returns.",
        ],
        "причины": [
            "Sending unit without power or with faulty software.",
            "Oxidation or a broken wire in the CAN connector.",
            "Added equipment interfering with the bus.",
            "Wrong parameter setting of the unit.",
        ],
    },

    1041: {
        "узел": "The terminal 50 circuit — the 'start' signal from the ignition lock to the unit and the starter. From it the unit sees that the key is turned to start.",
        "нормы": [
            ("Voltage on the terminal 50 wire with the ignition off", "absent — plus here means a short"),
            ("Terminal 50 signal with the key turned to start", "appears only on starting"),
        ],
        "шаги": [
            "With the ignition off, measure the voltage on the terminal 50 wire at the unit. Plus present — the circuit is shorted.",
            "Disconnect the terminal 50 wire at the lock or the starter relay and watch whether the voltage disappears. If it does — a short in the wiring to the unit.",
            "Check the ignition lock and the starter relay: stuck contacts give a permanent plus.",
            "MAZ and YaMZ: a flashing code 1-2-2 (terminal T50 permanently on battery '+') — look for the same circuit.",
        ],
        "причины": [
            "Stuck starter relay.",
            "Terminal 50 wiring shorted to plus.",
            "Ignition lock with burnt contacts.",
        ],
    },

    1042: {
        "узел": "The electronic interface between tractor and trailer: the ISO 11992 bus (trailer CAN) through the 7-pin socket. Over it the tractor communicates with the trailer electronics.",
        "нормы": [
            ("Communication with the trailer with the socket connected", "present — checked per diagnostics"),
            ("Trailer CAN line resistance", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 10 (bus open circuit, Knorr-Bremse and MAN): check the trailer CAN line at the socket and in the trailer cable.",
            "FMI 7 (Renault: fault on the 7-pin socket): inspect the socket, the data contacts and the oxidation.",
            "If communication is lost only with a particular trailer — check its cable and module.",
        ],
        "причины": [
            "Oxidised contacts of the 7-pin socket.",
            "Chafed trailer cable.",
            "Faulty trailer module.",
            "Open circuit of the trailer CAN line at the socket.",
        ],
    },

    1045: {
        "узел": "The brake pedal switch (stop signal No. 1). It switches on the stop lights and sends the units the 'brake pressed' signal.",
        "нормы": [
            ("Signal 'pressed' and 'not pressed'", "changes when the pedal is pressed and released"),
            ("Brake pedal adjustment", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Press and release the pedal with the ignition on and watch the switch state in diagnostics. If it does not change — the switch or the pedal adjustment.",
            "FMI 2, 4, 7 (switch faulty or no communication channel): measure the switch with a multimeter in both positions.",
            "If the stop lights do not come on — check the fuse and the common stop light line.",
        ],
        "причины": [
            "Stop light switch.",
            "Pedal adjustment.",
            "Burnt stop light or fuse.",
            "Open communication channel to the unit.",
        ],
    },

    1057: {
        "узел": "The central trailer control unit and its air pressure sensor in the backup line. If the main trailer air channel does not work, the unit holds backup control and monitors the pressure.",
        "нормы": [
            ("Response of the backup line pressure sensor", "present — checked per diagnostics"),
            ("Backup line pressure by gauge", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (no response from the air pressure sensor): check the sensor connector and the wire to the unit.",
            "FMI 7 (Renault: fault in the pneumatic supply): check the trailer pneumatic supply circuit with soapy water.",
            "If there is no pressure in the backup line — check the backup channel valve per the manual.",
        ],
        "причины": [
            "Backup line pressure sensor.",
            "Air leak in the trailer pneumatics.",
            "Central unit connector.",
        ],
    },

    1058: {
        "узел": "The trailer control module, pressure sensor: it measures the pressure in the trailer brake line and passes it to the tractor unit.",
        "нормы": [
            ("Trailer line pressure by gauge", "per the manufacturer's manual"),
            ("Difference between the module sensor and the gauge", "within tolerance per the manufacturer's manual"),
        ],
        "шаги": [
            "Screw a gauge into the test point of the trailer line and compare it with the reading in diagnostics.",
            "FMI 1, 2, 8 (pressure above normal by the sensor): if the gauge shows normal — the module's sensor.",
            "FMI 7 (Renault: fault in the module's pneumatic system): check the pneumatics and the leaks with soapy water.",
        ],
        "причины": [
            "Module pressure sensor.",
            "Leak in the trailer line.",
            "Trailer control module connector.",
        ],
    },

    1060: {
        "узел": "The lining wear sensor, axle 1, left (wheel No. 1). It is built into the pad lining of this wheel's brake pad and gives a signal when the lining has worn to the limit. The signal goes to the ABS/EBS unit and to the dash.",
        "нормы": [
            ("Pad lining thickness", "not less than the minimum per the manufacturer's manual"),
            ("Difference in pad wear between the two wheels of one axle", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1, 2 (wear above normal): remove the wheel and inspect this wheel's lining. Worn to the limit — replace the pads on this wheel and look at the paired wheel of the same axle.",
            "Compare the pads of the two wheels on one axle: if one is noticeably more worn, check the caliper on that side — the piston and the guide pins.",
            "FMI 2, 12 (sensor signal fault): inspect the sensor connector at the wheel and the cable to the unit. Check the cable from the pad to the connector for open circuit.",
            "If the lining is new and the code does not go — the sensor or the cable. Replace the sensor only after the cable has been checked.",
        ],
        "причины": [
            "Linings worn to the limit.",
            "Seized caliper or piston: one side wears faster.",
            "Sensor connector or cable at the wheel: chafed, pinched or oxidised.",
            "Water and dirt in the sensor connector.",
        ],
    },

    1061: {
        "узел": "The lining wear sensor, axle 1, right (wheel No. 2). It is built into the pad lining of this wheel's brake pad and gives a signal when the lining has worn to the limit. The signal goes to the ABS/EBS unit and to the dash.",
        "нормы": [
            ("Pad lining thickness", "not less than the minimum per the manufacturer's manual"),
            ("Difference in pad wear between the two wheels of one axle", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1, 2 (wear above normal): remove the wheel and inspect this wheel's lining. Worn to the limit — replace the pads on this wheel and look at the paired wheel of the same axle.",
            "Compare the pads of the two wheels on one axle: if one is noticeably more worn, check the caliper on that side — the piston and the guide pins.",
            "FMI 2, 12 (sensor signal fault): inspect the sensor connector at the wheel and the cable to the unit. Check the cable from the pad to the connector for open circuit.",
            "If the lining is new and the code does not go — the sensor or the cable. Replace the sensor only after the cable has been checked.",
        ],
        "причины": [
            "Linings worn to the limit.",
            "Seized caliper or piston: one side wears faster.",
            "Sensor connector or cable at the wheel: chafed, pinched or oxidised.",
            "Water and dirt in the sensor connector.",
        ],
    },

    1062: {
        "узел": "The lining wear sensor, axle 2, left (wheel No. 3). It is built into the pad lining of this wheel's brake pad and gives a signal when the lining has worn to the limit. The signal goes to the ABS/EBS unit and to the dash.",
        "нормы": [
            ("Pad lining thickness", "not less than the minimum per the manufacturer's manual"),
            ("Difference in pad wear between the two wheels of one axle", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1, 2 (wear above normal): remove the wheel and inspect this wheel's lining. Worn to the limit — replace the pads on this wheel and look at the paired wheel of the same axle.",
            "Compare the pads of the two wheels on one axle: if one is noticeably more worn, check the caliper on that side — the piston and the guide pins.",
            "FMI 2, 12 (sensor signal fault): inspect the sensor connector at the wheel and the cable to the unit. Check the cable from the pad to the connector for open circuit.",
            "If the lining is new and the code does not go — the sensor or the cable. Replace the sensor only after the cable has been checked.",
        ],
        "причины": [
            "Linings worn to the limit.",
            "Seized caliper or piston: one side wears faster.",
            "Sensor connector or cable at the wheel: chafed, pinched or oxidised.",
            "Water and dirt in the sensor connector.",
        ],
    },

    1063: {
        "узел": "The lining wear sensor, axle 2, right (wheel No. 4). It is built into the pad lining of this wheel's brake pad and gives a signal when the lining has worn to the limit. The signal goes to the ABS/EBS unit and to the dash.",
        "нормы": [
            ("Pad lining thickness", "not less than the minimum per the manufacturer's manual"),
            ("Difference in pad wear between the two wheels of one axle", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1, 2 (wear above normal): remove the wheel and inspect this wheel's lining. Worn to the limit — replace the pads on this wheel and look at the paired wheel of the same axle.",
            "Compare the pads of the two wheels on one axle: if one is noticeably more worn, check the caliper on that side — the piston and the guide pins.",
            "FMI 2, 12 (sensor signal fault): inspect the sensor connector at the wheel and the cable to the unit. Check the cable from the pad to the connector for open circuit.",
            "If the lining is new and the code does not go — the sensor or the cable. Replace the sensor only after the cable has been checked.",
        ],
        "причины": [
            "Linings worn to the limit.",
            "Seized caliper or piston: one side wears faster.",
            "Sensor connector or cable at the wheel: chafed, pinched or oxidised.",
            "Water and dirt in the sensor connector.",
        ],
    },

    1064: {
        "узел": "The lining wear sensor, axle 3, left (wheel No. 5). It is built into the pad lining of this wheel's brake pad and gives a signal when the lining has worn to the limit. The signal goes to the ABS/EBS unit and to the dash.",
        "нормы": [
            ("Pad lining thickness", "not less than the minimum per the manufacturer's manual"),
            ("Difference in pad wear between the two wheels of one axle", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1, 2 (wear above normal): remove the wheel and inspect this wheel's lining. Worn to the limit — replace the pads on this wheel and look at the paired wheel of the same axle.",
            "Compare the pads of the two wheels on one axle: if one is noticeably more worn, check the caliper on that side — the piston and the guide pins.",
            "FMI 2, 12 (sensor signal fault): inspect the sensor connector at the wheel and the cable to the unit. Check the cable from the pad to the connector for open circuit.",
            "If the lining is new and the code does not go — the sensor or the cable. Replace the sensor only after the cable has been checked.",
        ],
        "причины": [
            "Linings worn to the limit.",
            "Seized caliper or piston: one side wears faster.",
            "Sensor connector or cable at the wheel: chafed, pinched or oxidised.",
            "Water and dirt in the sensor connector.",
        ],
    },

    1065: {
        "узел": "The lining wear sensor, axle 3, right (wheel No. 6). It is built into the pad lining of this wheel's brake pad and gives a signal when the lining has worn to the limit. The signal goes to the ABS/EBS unit and to the dash.",
        "нормы": [
            ("Pad lining thickness", "not less than the minimum per the manufacturer's manual"),
            ("Difference in pad wear between the two wheels of one axle", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1, 2 (wear above normal): remove the wheel and inspect this wheel's lining. Worn to the limit — replace the pads on this wheel and look at the paired wheel of the same axle.",
            "Compare the pads of the two wheels on one axle: if one is noticeably more worn, check the caliper on that side — the piston and the guide pins.",
            "FMI 2, 12 (sensor signal fault): inspect the sensor connector at the wheel and the cable to the unit. Check the cable from the pad to the connector for open circuit.",
            "If the lining is new and the code does not go — the sensor or the cable. Replace the sensor only after the cable has been checked.",
        ],
        "причины": [
            "Linings worn to the limit.",
            "Seized caliper or piston: one side wears faster.",
            "Sensor connector or cable at the wheel: chafed, pinched or oxidised.",
            "Water and dirt in the sensor connector.",
        ],
    },

    1068: {
        "узел": "The secondary (duplicate) brake demand signal from the brake pedal. The units compare it with the first signal. If the signals disagree or the second one is lost, the unit limits the braking functions.",
        "нормы": [
            ("First and second signals when the pedal is pressed", "rise together, without divergence"),
            ("Signal on the CAN bus when pressed", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Press the pedal with the ignition on and watch both signals in diagnostics. If they disagree — the pedal or its connector.",
            "FMI 2 (open or short of the secondary circuit, Bendix): check the pedal sensor connector and the wiring to the unit.",
            "FMI 2, 4, 5, 13 (Meritor: PWM signal out of range): check the pedal sensor and its supply; if it repeats — the unit, per the manual.",
            "FMI 12 (Sitrak: duplicate signal lost on the bus): see the general methods for the J1939 bus higher up the list.",
        ],
        "причины": [
            "Brake pedal sensor.",
            "Oxidised pedal connector.",
            "Chafed wire on the way to the unit.",
            "Pedal adjustment.",
        ],
    },

    1069: {
        "узел": "Tyre size check: the unit compares the tyre sizes of the front and rear axles. A difference in radii distorts the speed readings and the ABS/EBS operation.",
        "нормы": [
            ("Difference in tyre radii between the front and rear axles", "within tolerance per the manufacturer's manual"),
            ("Tyre size parameters in the unit", "match the actual tyres"),
        ],
        "шаги": [
            "Check whether the tyres are the same size across the axles, including the spare wheel if it is in use.",
            "Compare the tyre size parameters in the unit with the actual tyres. If they do not match — enter them per the manual.",
            "FMI 1 (Wabco: TPM tyre pressure check): check the tyre pressure sensors separately.",
        ],
        "причины": [
            "Different tyres on the axles, or wear that changes the radius.",
            "Wrong tyre size parameters in the unit.",
            "Faulty tyre pressure sensor.",
        ],
    },

    1073: {
        "узел": "Output to the solenoid valve of the compression engine brake, stage 2. The unit switches the valve on the driver's command, and the brake works on the required stage.",
        "нормы": [
            ("Output state when the brake is switched on and off", "changes on command — per diagnostics"),
            ("Solenoid valve resistance", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3, 4 (3 — short to supply; 4 — open circuit or ground): unplug the valve connector with the ignition off and switch it on. If the code stays — the wiring to the valve. If the code goes — the valve.",
            "FMI 4, 5 (Renault: short to ground, JACOB 2 solenoid valve): check the JACOB 2 solenoid valve and the cable connections.",
            "Check which stage is engaged by the button on the panel — link with the stage selection code (973).",
        ],
        "причины": [
            "Engine brake solenoid valve.",
            "Short to ground in the harness near the engine.",
            "Oxidised valve connector.",
            "Control unit that keeps the output on.",
        ],
    },

    1080: {
        "узел": "Sensor supply branch No. 2 (reference 5 V). The unit supplies the reference voltage to a group of sensors on this branch. If the branch is shorted, all sensors on it lose their signal.",
        "нормы": [
            ("Reference voltage at the sensor connector, ignition on", "5.0 V ± 0.25"),
            ("Branch voltage with the sensors unplugged", "the same reference, without a drop"),
        ],
        "шаги": [
            "Measure the branch's reference voltage at the connector with the ignition on.",
            "FMI 2 (Isuzu: wrong 5 V voltage, circuit 2): unplug the branch's sensors one at a time and see whether the fault goes.",
            "FMI 3, 4 (3 — Sitrak: high voltage; 4 — KamAZ: sensor voltage, branch 2): the same — find the sensor that shorts the branch.",
            "If with all sensors unplugged the voltage is not normal — the control unit.",
        ],
        "причины": [
            "The sensor that shorted the supply branch.",
            "Chafed wire or oxidised connector.",
            "Control unit.",
        ],
    },

    1087: {
        "узел": "Air pressure sensor in the first service brake circuit. It shows the pressure in this circuit's reservoir, and the unit uses it to decide whether there is enough air for braking.",
        "нормы": [
            ("Reservoir pressure per the dash and the gauge", "per the manufacturer's manual"),
            ("Difference between the sensor and the gauge", "not more than the tolerance per the manufacturer's manual"),
        ],
        "шаги": [
            "Compare the dash reading with a mechanical gauge screwed into the test point of the reservoir of circuit 1 (if there is one).",
            "FMI 7 (insufficient pressure): find the leak with soapy water at the circuit's joints, on the reservoir assembly and at the condensate drain. If the pressure falls overnight — a leak.",
            "FMI 0, 1 (sensor reads above normal): unplug the sensor and, with the gauge screwed in, compare the readings. If the sensor lies — replace the sensor.",
            "FMI 4, 5 (short to ground or open circuit of the sensor circuit): check the wire from the sensor to the unit for continuity.",
            "If the pressure is normal and the code is there — the cable from the sensor to the unit: open or ground.",
        ],
        "причины": [
            "Leak in the circuit: joints, hoses, reservoir.",
            "Moisture and condensate in the reservoir.",
            "The pressure sensor itself.",
            "Open or short in the cable to the unit.",
        ],
    },

    1088: {
        "узел": "Air pressure sensor in the second service brake circuit. It shows the pressure in this circuit's reservoir, and the unit uses it to decide whether there is enough air for braking.",
        "нормы": [
            ("Reservoir pressure per the dash and the gauge", "per the manufacturer's manual"),
            ("Difference between the sensor and the gauge", "not more than the tolerance per the manufacturer's manual"),
        ],
        "шаги": [
            "Compare the dash reading with a mechanical gauge screwed into the test point of the reservoir of circuit 2 (if there is one).",
            "FMI 7 (insufficient pressure): find the leak with soapy water at the circuit's joints, on the reservoir assembly and at the condensate drain. If the pressure falls overnight — a leak.",
            "FMI 0, 1 (sensor reads above normal): unplug the sensor and, with the gauge screwed in, compare the readings. If the sensor lies — replace the sensor.",
            "FMI 4, 5 (short to ground or open circuit of the sensor circuit): check the wire from the sensor to the unit for continuity.",
            "If the pressure is normal and the code is there — the cable from the sensor to the unit: open or ground.",
        ],
        "причины": [
            "Leak in the circuit: joints, hoses, reservoir.",
            "Moisture and condensate in the reservoir.",
            "The pressure sensor itself.",
            "Open or short in the cable to the unit.",
        ],
    },

    1089: {
        "узел": "Pressure sensor in the additional reservoir — the supply for the add-on equipment (4th circuit). The unit sees the supply pressure and warns if it is not normal.",
        "нормы": [
            ("Reservoir pressure per the dash and the gauge", "per the manufacturer's manual"),
            ("Difference between the sensor and the gauge", "not more than the tolerance per the manufacturer's manual"),
        ],
        "шаги": [
            "Compare the dash reading with a mechanical gauge at the test point of the additional reservoir.",
            "FMI 4, 5, 7 (short to ground of the sensor circuit, KamAZ): unplug the sensor and check the wire to ground.",
            "FMI 0, 1 (pressure above normal, International): check the sensor with the gauge screwed in.",
            "FMI 9, 13 (Mercedes: AIR1 message over J1939 does not arrive): see the general methods for the bus higher up the list.",
        ],
        "причины": [
            "Leak in the circuit: joints, hoses, reservoir.",
            "Moisture and condensate in the reservoir.",
            "The pressure sensor itself.",
            "Open or short in the cable to the unit.",
        ],
    },

    1136: {
        "узел": "The internal temperature sensor of the engine control unit. The unit watches its own overheating and limits power at high temperature.",
        "нормы": [
            ("Control unit temperature per diagnostics", "within the working range per the manufacturer's manual"),
            ("Voltage of the built-in temperature sensor", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Check the cooling and ventilation of the control unit compartment: are the vents blocked, is there dirt on the housing?",
            "FMI 0, 1 (unit temperature high, KamAZ): check whether the harness and the unit's connectors near the engine are heating up.",
            "FMI 2, 3, 4 (unreliable signal or voltage above the limit): clear the codes; if it repeats — the control unit, per the manual.",
        ],
        "причины": [
            "Overheating of the control unit compartment.",
            "Dirt and blocked ventilation of the unit.",
            "Faulty internal sensor of the unit.",
        ],
    },

    1188: {
        "узел": "The turbo wastegate actuator: on command from the unit it opens the valve that lets part of the exhaust bypass the turbine, and regulates the boost.",
        "нормы": [
            ("Actuator rod travel", "per the manufacturer's manual"),
            ("Actuator position feedback sensor signal", "changes with the actuator position — per diagnostics"),
        ],
        "шаги": [
            "FMI 7 (mechanical fault of the wastegate): with the engine off, turn the actuator rod by hand. If it sticks or has play — the valve or the joints.",
            "Inspect the rod and the joints: carbon and soot get in the way of movement.",
            "FMI 0, 1, 2, 3 (Sitrak: feedback sensor voltage above the limit): check the position sensor, the connector and the supply.",
        ],
        "причины": [
            "Carbon and soot on the wastegate.",
            "Seized rod or joints.",
            "Actuator feedback sensor.",
            "Oxidised actuator connector.",
        ],
    },

    1235: {
        "узел": "The third CAN network (line C): units that are not on the main bus are connected over it. The Busoff code means a unit has disconnected itself from the line because of many transmission errors.",
        "нормы": [
            ("CAN-H and CAN-L resistance of line C, power off", "check against the line diagram; on the main bus about 60 Ω"),
            ("Voltage on line C in operation", "per the manufacturer's manual"),
        ],
        "шаги": [
            "From the diagram find the units on line C, and check their power and ground.",
            "Measure the resistance between CAN-H and CAN-L of line C with the power off: compare it with the diagram.",
            "Busoff: the unit has disconnected itself from the line. Reset the unit's power per the manual and see whether the link holds.",
            "Check the connectors of line C for oxidation and a chafed wire.",
        ],
        "причины": [
            "Unit on line C that shorts the bus.",
            "Open circuit or oxidation at the line C connector.",
            "Wrong resistor, or no resistor at the end of the line.",
            "Unit with faulty power.",
        ],
    },

    1268: {
        "узел": "The ignition coil of cylinder No. 1: it gives the spark to this cylinder's plug. The control unit switches it on with a control pulse. The code refers only to this coil; the neighbouring cylinders are not to blame in this code.",
        "нормы": [
            ("Resistance of the coil's primary and secondary windings", "per the manufacturer's manual"),
            ("Coil of the neighbouring cylinder of the same series", "compare: identical coils read the same"),
        ],
        "шаги": [
            "Swap the coil with the neighbouring cylinder's and start the engine at idle. If the code moves with the coil — the coil is faulty. If the code stays with this cylinder — the problem is in the connector, the wiring or the control unit.",
            "FMI 3, 4, 5 (3 — short to plus, 4 — to ground, 5 — open circuit): with the ignition off, unplug the coil connector, inspect the contacts and measure the winding resistance. Compare the value with the manual.",
            "The plug of this same cylinder: gap and condition of the electrode. A flooded or worn plug gives misfires that look like a coil failure.",
        ],
        "причины": [
            "Breakdown or crack in the coil insulator.",
            "Oxidised connector or water in the coil connector.",
            "Chafed coil control wire.",
            "Flooded or worn plug of the same cylinder.",
        ],
    },

    1269: {
        "узел": "The ignition coil of cylinder No. 2: it gives the spark to this cylinder's plug. The control unit switches it on with a control pulse. The code refers only to this coil; the neighbouring cylinders are not to blame in this code.",
        "нормы": [
            ("Resistance of the coil's primary and secondary windings", "per the manufacturer's manual"),
            ("Coil of the neighbouring cylinder of the same series", "compare: identical coils read the same"),
        ],
        "шаги": [
            "Swap the coil with the neighbouring cylinder's and start the engine at idle. If the code moves with the coil — the coil is faulty. If the code stays with this cylinder — the problem is in the connector, the wiring or the control unit.",
            "FMI 3, 4, 5 (3 — short to plus, 4 — to ground, 5 — open circuit): with the ignition off, unplug the coil connector, inspect the contacts and measure the winding resistance. Compare the value with the manual.",
            "The plug of this same cylinder: gap and condition of the electrode. A flooded or worn plug gives misfires that look like a coil failure.",
        ],
        "причины": [
            "Breakdown or crack in the coil insulator.",
            "Oxidised connector or water in the coil connector.",
            "Chafed coil control wire.",
            "Flooded or worn plug of the same cylinder.",
        ],
    },

    1270: {
        "узел": "The ignition coil of cylinder No. 3: it gives the spark to this cylinder's plug. The control unit switches it on with a control pulse. The code refers only to this coil; the neighbouring cylinders are not to blame in this code.",
        "нормы": [
            ("Resistance of the coil's primary and secondary windings", "per the manufacturer's manual"),
            ("Coil of the neighbouring cylinder of the same series", "compare: identical coils read the same"),
        ],
        "шаги": [
            "Swap the coil with the neighbouring cylinder's and start the engine at idle. If the code moves with the coil — the coil is faulty. If the code stays with this cylinder — the problem is in the connector, the wiring or the control unit.",
            "FMI 3, 4, 5 (3 — short to plus, 4 — to ground, 5 — open circuit): with the ignition off, unplug the coil connector, inspect the contacts and measure the winding resistance. Compare the value with the manual.",
            "The plug of this same cylinder: gap and condition of the electrode. A flooded or worn plug gives misfires that look like a coil failure.",
        ],
        "причины": [
            "Breakdown or crack in the coil insulator.",
            "Oxidised connector or water in the coil connector.",
            "Chafed coil control wire.",
            "Flooded or worn plug of the same cylinder.",
        ],
    },

    1271: {
        "узел": "The ignition coil of cylinder No. 4: it gives the spark to this cylinder's plug. The control unit switches it on with a control pulse. The code refers only to this coil; the neighbouring cylinders are not to blame in this code.",
        "нормы": [
            ("Resistance of the coil's primary and secondary windings", "per the manufacturer's manual"),
            ("Coil of the neighbouring cylinder of the same series", "compare: identical coils read the same"),
        ],
        "шаги": [
            "Swap the coil with the neighbouring cylinder's and start the engine at idle. If the code moves with the coil — the coil is faulty. If the code stays with this cylinder — the problem is in the connector, the wiring or the control unit.",
            "FMI 3, 4, 5 (3 — short to plus, 4 — to ground, 5 — open circuit): with the ignition off, unplug the coil connector, inspect the contacts and measure the winding resistance. Compare the value with the manual.",
            "The plug of this same cylinder: gap and condition of the electrode. A flooded or worn plug gives misfires that look like a coil failure.",
        ],
        "причины": [
            "Breakdown or crack in the coil insulator.",
            "Oxidised connector or water in the coil connector.",
            "Chafed coil control wire.",
            "Flooded or worn plug of the same cylinder.",
        ],
    },

    1272: {
        "узел": "The ignition coil of cylinder No. 5: it gives the spark to this cylinder's plug. The control unit switches it on with a control pulse. The code refers only to this coil; the neighbouring cylinders are not to blame in this code.",
        "нормы": [
            ("Resistance of the coil's primary and secondary windings", "per the manufacturer's manual"),
            ("Coil of the neighbouring cylinder of the same series", "compare: identical coils read the same"),
        ],
        "шаги": [
            "Swap the coil with the neighbouring cylinder's and start the engine at idle. If the code moves with the coil — the coil is faulty. If the code stays with this cylinder — the problem is in the connector, the wiring or the control unit.",
            "FMI 3, 4, 5 (3 — short to plus, 4 — to ground, 5 — open circuit): with the ignition off, unplug the coil connector, inspect the contacts and measure the winding resistance. Compare the value with the manual.",
            "The plug of this same cylinder: gap and condition of the electrode. A flooded or worn plug gives misfires that look like a coil failure.",
        ],
        "причины": [
            "Breakdown or crack in the coil insulator.",
            "Oxidised connector or water in the coil connector.",
            "Chafed coil control wire.",
            "Flooded or worn plug of the same cylinder.",
        ],
    },

    1273: {
        "узел": "The ignition coil of cylinder No. 6: it gives the spark to this cylinder's plug. The control unit switches it on with a control pulse. The code refers only to this coil; the neighbouring cylinders are not to blame in this code.",
        "нормы": [
            ("Resistance of the coil's primary and secondary windings", "per the manufacturer's manual"),
            ("Coil of the neighbouring cylinder of the same series", "compare: identical coils read the same"),
        ],
        "шаги": [
            "Swap the coil with the neighbouring cylinder's and start the engine at idle. If the code moves with the coil — the coil is faulty. If the code stays with this cylinder — the problem is in the connector, the wiring or the control unit.",
            "FMI 3, 4, 5 (3 — short to plus, 4 — to ground, 5 — open circuit): with the ignition off, unplug the coil connector, inspect the contacts and measure the winding resistance. Compare the value with the manual.",
            "The plug of this same cylinder: gap and condition of the electrode. A flooded or worn plug gives misfires that look like a coil failure.",
        ],
        "причины": [
            "Breakdown or crack in the coil insulator.",
            "Oxidised connector or water in the coil connector.",
            "Chafed coil control wire.",
            "Flooded or worn plug of the same cylinder.",
        ],
    },

    1329: {
        "узел": "Misfire in cylinder No. 7: the unit sees that the mixture did not ignite in this cylinder. The code refers to this cylinder; the neighbours are not to blame in it.",
        "нормы": [
            ("Cylinder No. 7 at idle", "smooth, without misfires — per diagnostics"),
            ("Comparison with the neighbouring cylinder", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Swap the plug or the coil of cylinder No. 7 with the neighbour's (as for the coil, see codes 1268–1273) and watch whether the code moves.",
            "Check the injector of cylinder No. 7 (code 657): sticking or leaking gives misfires.",
            "MAZ and YaMZ: a flashing code 5-1-4 (misfire in the 7th cylinder) — check the same ignition circuit.",
        ],
        "причины": [
            "Plug or ignition coil of cylinder No. 7.",
            "Injector of cylinder No. 7.",
            "Low compression in the cylinder.",
        ],
    },

    1330: {
        "узел": "Misfire in cylinder No. 8: the unit sees that the mixture did not ignite in this cylinder. The code refers to this cylinder.",
        "нормы": [
            ("Cylinder No. 8 at idle", "smooth, without misfires — per diagnostics"),
            ("Comparison with the neighbouring cylinder", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Swap the plug or the coil of cylinder No. 8 with the neighbour's and watch whether the code moves.",
            "Check the injector of cylinder No. 8 (code 658): sticking or leaking gives misfires.",
            "MAZ and YaMZ: a flashing code 5-3-4 (misfire in the 8th cylinder) — the same circuit.",
        ],
        "причины": [
            "Plug or ignition coil of cylinder No. 8.",
            "Injector of cylinder No. 8.",
            "Low compression in the cylinder.",
        ],
    },

    1382: {
        "узел": "Differential pressure sensor on the fuel filter, suction side (between the pump and the tank). When the filter is clogged the pump pulls harder, and the sensor sees this.",
        "нормы": [
            ("Drop across a new filter", "minimal, per the manufacturer's manual"),
            ("Drop limit at which the filter is changed", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Inspect the filter: replace it if it is clogged. Check for water in the sedimenter.",
            "Check for air leaks on the suction side with soapy water at the line's joints.",
            "FMI 1 (MAZ and YaMZ: pre-filter clogged, flashing code 2-1-7): replace the filter and check the sensor tubes.",
            "FMI 14 (International: filter between the pump and the tank): check that the filter is in its place, and the sensor tubes.",
        ],
        "причины": [
            "Clogged fuel filter.",
            "Water or wax in the fuel.",
            "Air leak on the suction side.",
            "Clogged sensor tubes.",
        ],
    },

    1438: {
        "узел": "The yellow ABS/EBS warning signal on the dash: it lights when the ABS or EBS is not working fully. The lamp circuit runs from the ABS unit to the dash through the warning lamp relay.",
        "нормы": [
            ("Lamp at ignition on", "flashes on and off — if it stays lit permanently, it is a fault"),
            ("Warning lamp relay", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Check the lamp on the dash: at ignition on it should flash and go out.",
            "FMI 5 (International: ABS lamp fault; Meritor: warning lamp relay — open circuit or ground): check the relay and the circuit to the dash for a short to ground.",
            "If the lamp is working and the code is there — the ABS or EBS unit, per the manual.",
        ],
        "причины": [
            "Burnt-out lamp on the dash.",
            "Warning lamp relay.",
            "Open circuit or ground in the wiring to the dash.",
            "ABS or EBS unit.",
        ],
    },

    1592: {
        "узел": "The speed of the front axle left wheel: the ABS sends it over the J1939 bus (HRW message). The unit uses it for speed and stability.",
        "нормы": [
            ("HRW message on the bus", "arrives regularly — per diagnostics"),
            ("Signal of the front axle left wheel sensor", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (Mercedes: HRW message from the ABS does not arrive): see the general methods for the J1939 bus higher up the list.",
            "FMI 12 (Sitrak: no HRWS frame): check the ABS unit, its supply and the bus.",
            "If the message is there but the speed is wrong — the speed sensor of the front axle left wheel (see the ABS sensor pages).",
        ],
        "причины": [
            "ABS unit without power or with faulty software.",
            "Left wheel speed sensor.",
            "Break or oxidation in the CAN connector.",
        ],
    },

    1623: {
        "узел": "A J1939 message: the tachograph output shaft speed (the units calculate speed and mileage from it). The tachograph, or the unit that passes on its signal, must send it. Units that need it do not see this signal when the message drops out.",
        "нормы": [
            ("Message arrives regularly, without gaps", "checked per diagnostics; gaps are a fault"),
            ("CAN-H and CAN-L resistance, power off", "about 60 Ω"),
        ],
        "шаги": [
            "Read the codes of all units. If many have them — look at the bus; if one unit is silent — look at that unit.",
            "Measure the supply and the ground of the unit that should send the message. Without power the unit is silent.",
            "FMI 9, 13 (message missing): inspect this unit's connector on the CAN bus for oxidation and a chafed wire. Disconnect the units one at a time and see whether the message returns.",
            "FMI 12 (no frame, timeout expired) and FMI 19 (frame of wrong length): check the software version of the sending unit and its parameter settings; for units of different makes these are different actions.",
        ],
        "причины": [
            "Sending unit without power or with faulty software.",
            "Oxidation or a broken wire in the CAN connector.",
            "Added equipment interfering with the bus.",
            "Wrong parameter setting of the unit.",
        ],
    },

    1716: {
        "узел": "A J1939 message: the state of the retarder (not the engine brake) and the torque it has requested. The retarder, or the unit that drives it, must send it. Units that need it do not see this signal when the message drops out.",
        "нормы": [
            ("Message arrives regularly, without gaps", "checked per diagnostics; gaps are a fault"),
            ("CAN-H and CAN-L resistance, power off", "about 60 Ω"),
        ],
        "шаги": [
            "Read the codes of all units. If many have them — look at the bus; if one unit is silent — look at that unit.",
            "Measure the supply and the ground of the unit that should send the message. Without power the unit is silent.",
            "FMI 9, 13 (message missing): inspect this unit's connector on the CAN bus for oxidation and a chafed wire. Disconnect the units one at a time and see whether the message returns.",
            "FMI 12 (no frame, timeout expired) and FMI 19 (frame of wrong length): check the software version of the sending unit and its parameter settings; for units of different makes these are different actions.",
        ],
        "причины": [
            "Sending unit without power or with faulty software.",
            "Oxidation or a broken wire in the CAN connector.",
            "Added equipment interfering with the bus.",
            "Wrong parameter setting of the unit.",
        ],
    },

    1761: {
        "узел": "The urea (AdBlue) level sensor in the tank. The unit uses it to see how much fluid is left, and warns the driver in advance.",
        "нормы": [
            ("Level on the dash and the actual volume", "match — checked by refilling a known volume"),
            ("Level sensor resistance and connector", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Compare the dash reading with how much urea has been added and how much is left: when refilling with a known volume, the level should rise accordingly.",
            "FMI 1 (critically low level): check whether the float is stuck or the filter on the intake is clogged.",
            "FMI 3, 4, 18 (electrics or signal out of range): unplug the sensor connector, inspect it for oxidation and urea crystals; check the wire for continuity.",
            "FMI 0 (Sitrak: readings too high): the sensor — after checking the connector.",
        ],
        "причины": [
            "Float or level sensor stuck.",
            "Urea crystals on the connector and the sensor.",
            "Open circuit or short of the sensor wire.",
            "A real under-fill — the code is honest.",
        ],
    },

    1807: {
        "узел": "The steering wheel angle sensor. It tells the stability and brake units how the steering wheel is turned. Without a zero position the unit does not know where the wheels are pointing.",
        "нормы": [
            ("Steering wheel position with the wheels straight", "zero value, as recorded in the calibration per the manual"),
            ("Signal with the wheel turned to the stop both ways", "changes smoothly, without dips — per diagnostics"),
        ],
        "шаги": [
            "Set the steering wheel straight and look at the value in diagnostics. Compare with zero per the manual.",
            "Turn the wheel to the stop both ways and watch whether the signal changes smoothly. Jumps — the sensor or the connector.",
            "FMI 2, 9, 12, 13 (signal does not change or is out of range): check the sensor connector under the steering column and the cable, which can chafe when the wheel is turned.",
            "FMI 0, 1, 7, 8 (zero offset): calibrate the zero position per the manufacturer's manual after steering repair.",
        ],
        "причины": [
            "Zero offset after steering repair or column replacement.",
            "Chafed sensor cable under the steering wheel.",
            "Oxidised connector.",
            "The sensor itself.",
        ],
    },

    1808: {
        "узел": "The yaw rate sensor in the stability control unit. It shows how fast the vehicle rotates about its vertical axis. From it the unit decides whether it is time to intervene in a turn.",
        "нормы": [
            ("Signal on a stationary vehicle", "per the manufacturer's manual"),
            ("Signal in a turn", "changes — per diagnostics"),
        ],
        "шаги": [
            "Check the stability control unit's connector, its mounting and the supply of the sensor bus.",
            "FMI 2, 9, 13, 14 (Bendix: sensor CAN bus supply, voltage out of range): check the unit's power and the bus.",
            "FMI 1, 2, 3, 5 (Meritor: signal does not change under load): sensor — calibration per the manual after frame repair or replacing the unit.",
        ],
        "причины": [
            "Stability control sensor or unit.",
            "Supply of the sensor bus.",
            "Calibration after repair.",
        ],
    },

    1809: {
        "узел": "The lateral acceleration sensor in the stability control unit. It shows how hard the vehicle is being pushed sideways in a turn. From it the unit decides whether stability assistance is needed.",
        "нормы": [
            ("Signal on a stationary vehicle", "per the manufacturer's manual"),
            ("Signal in a turn", "changes — per diagnostics"),
        ],
        "шаги": [
            "Check the stability control unit's connector and mounting.",
            "FMI 2, 13 (Bendix: signal out of range, static calibration error): calibration per the manual.",
            "FMI 1, 7, 12, 14 (Meritor: signal does not change under load): sensor or unit per the manual.",
        ],
        "причины": [
            "Stability control sensor or unit.",
            "Calibration after repair or replacement.",
            "Unit connector.",
        ],
    },

    2023: {
        "узел": "The unit with address 23 on the J1939 network. Per the factory table this is the dash unit. The code means that messages do not come from this address, or there is a fault in its analogue input.",
        "нормы": [
            ("Messages from address 23 over J1939", "arrive regularly"),
            ("Power and ground of the dash unit", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Check whether the dash works: do the lamps light at ignition on, does the supply not drop out?",
            "FMI 9 (Mercedes: no messages from address 23): see the general methods for the J1939 bus higher up the list.",
            "FMI 3, 4, 6, 9 (International: dash analogue input, light sensor): inspect the light sensor and the dash connector.",
        ],
        "причины": [
            "Dash without power or with faulty software.",
            "Break in the CAN bus wire.",
            "Light sensor or its connector.",
        ],
    },

    2623: {
        "узел": "The secondary accelerator pedal channel (position sensor 2). A two-channel pedal: the unit checks both channels, and if they disagree, it cuts the fuel supply.",
        "нормы": [
            ("Two pedal channels when pressed", "rise together, without divergence — per diagnostics"),
            ("Pedal reference voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Press the pedal with the ignition on and watch both channels in diagnostics. If they disagree — the pedal or its connector.",
            "FMI 3, 4 (3 — short to supply, 4 — short to ground; DAF and Dongfeng): unplug the pedal connector and inspect the contacts.",
            "FMI 2, 8 (Mercedes: channel readings disagree): check the linkage and the pedal adjustment, and the wear of the tracks.",
        ],
        "причины": [
            "Oxidised pedal connector.",
            "Wear of the pedal sensor tracks.",
            "Water or dust got into the pedal housing.",
            "Pedal linkage adjustment.",
        ],
    },

    2630: {
        "узел": "The air temperature sensor after the charge air cooler (intercooler). The unit uses it to monitor air cooling and the boost supply.",
        "нормы": [
            ("Temperature after the intercooler", "noticeably lower than before it when the engine works under load"),
            ("Sensor voltage and connector", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Inspect the intercooler and the hoses: cracks and leaks. If the air is not being cooled, the sensor will show a high temperature.",
            "FMI 0 (credibility fault, MAZ and YaMZ, flashing code 6-1-3): check the intercooler, the hoses and the sensor itself.",
            "FMI 3, 4, 12, 15 (sensor voltage above the limit, Sitrak): check the sensor connector and wiring.",
        ],
        "причины": [
            "Dirty or cracked intercooler.",
            "Air leak in the hoses after the intercooler.",
            "The temperature sensor itself.",
            "Oxidised connector.",
        ],
    },

    2634: {
        "узел": "The main power relay of the control unit. It supplies power to the unit after the ignition is switched on. The code of a short to battery or to ground is about the relay circuit and its contacts.",
        "нормы": [
            ("Voltage at the relay contacts, ignition on", "as at the battery"),
            ("Voltage at the contacts with the ignition off", "none"),
        ],
        "шаги": [
            "FMI 3, 4 (3 — short to battery, 4 — short to ground): unplug the relay, inspect the contacts and the sockets under it for burning.",
            "Check whether there is power at the relay coil with the ignition on, and whether it has a ground.",
            "If the relay hums or clicks but the code stays — replace the relay. If it does not click — the supply circuit of the coil.",
        ],
        "причины": [
            "Burnt relay contacts.",
            "Oxidised relay sockets.",
            "Short in the unit's power wiring.",
            "Unit power fuse.",
        ],
    },

    3031: {
        "узел": "The AdBlue (urea) tank temperature sensor. The unit measures whether the urea has frozen and whether its temperature is too high; this decides whether it can dose and whether the tank can be heated.",
        "нормы": [
            ("Urea temperature in the tank", "within the ambient temperature per diagnostics; readings too high or zero — a fault"),
            ("Sensor resistance and connector", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Compare the reading with the cab temperature and by touch: in frost the tank cannot read warm; in a warm garage — frost.",
            "FMI 2 (unreliable temperature signal): unplug the sensor connector in the tank and inspect it for oxidation and leaks. White crystals on the connector are a sign of urea leakage.",
            "FMI 3 (short to supply): with the ignition off, unplug the connector and check the wire to the unit for a short to plus.",
            "FMI 4 (short to ground): with the ignition off, unplug the connector and check the wire to the unit for a short to ground; check the sensor's resistance against the manual.",
            "FMI 0 (Sitrak: readings too high): the sensor — if the wiring is in order; after replacement, clear the code and check at idle in diagnostics.",
        ],
        "причины": [
            "Oxidised sensor connector or urea crystals on it.",
            "Open circuit or short of the temperature sensor wire.",
            "The sensor itself.",
            "SCR control unit, if several tank sensors show a fault at once.",
        ],
    },

    3216: {
        "узел": "The NOx sensor before the catalyst: it shows how much nitrogen oxide comes out of the engine before cleaning. From it the unit calculates the urea dose.",
        "нормы": [
            ("NOx reading with the engine running", "per diagnostics; no zero or jumping values"),
            ("High NOx before SCR", "a sign that the engine or the EGR is not working right, not only the sensor"),
        ],
        "шаги": [
            "First check whether the NOx is actually high: engine mode, EGR and injection — per the manual — and only then the sensor.",
            "FMI 0, 1, 2, 3 (Sitrak: reading too high): NOx sensor connector, supply and the wiring shield.",
            "FMI 18 (DAF: NOx before the catalyst too high for a long period): check the sensor and the engine per the manual.",
        ],
        "причины": [
            "Faulty NOx sensor.",
            "Injection or EGR operating out of mode.",
            "Oxidised sensor connector.",
        ],
    },

    3226: {
        "узел": "The NOx reading at the SCR system outlet. From it the unit judges how well the catalyst cleans the exhaust (catalyst efficiency).",
        "нормы": [
            ("Outlet NOx reading with clean cleaning", "low; per diagnostics and the manual"),
            ("NOx sensor and connector", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 0, 2, 4, 9 (DAF and Dongfeng: very high NOx, emission above the limit): check the urea supply, the catalyst and the inlet sensor.",
            "FMI 15 (KamAZ: raised emission before cleaning): this is about the engine, not the catalyst — check the engine's mode per the manual.",
            "FMI 15, 17, 19 (Sitrak: NOx sensor reading too high): sensor connector, supply and wire.",
        ],
        "причины": [
            "Catalyst that has lost efficiency.",
            "Insufficient or incorrect urea dosing.",
            "Faulty NOx sensor.",
            "Engine mode with high emission.",
        ],
    },

    3234: {
        "узел": "The NOx sensor after the catalyst (at the SCR outlet). It shows how much nitrogen oxide goes into the atmosphere. The unit uses it to check the catalyst's efficiency.",
        "нормы": [
            ("Sensor signal with the engine running", "present, without zero or jumping values"),
            ("Sensor resistance and supply", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (DAF: signal absent or unlikely): check the connector, the supply and the sensor's link to the unit.",
            "FMI 2 (KamAZ: signal out of range or unreliable): check the connector and the wire.",
            "Compare with the NOx sensor before the catalyst (code 3216): if the input is high and the output zero — the outlet sensor.",
        ],
        "причины": [
            "The outlet NOx sensor itself.",
            "Oxidised connector.",
            "Chafed wire.",
        ],
    },

    3251: {
        "узел": "The differential pressure sensor on the diesel particulate filter (DPF). It shows how clogged the filter is with soot; the unit uses it to decide whether a regeneration is needed.",
        "нормы": [
            ("Pressure drop across the particulate filter", "rises as it clogs — per diagnostics; the limit per the manual"),
            ("Sensor tube resistance", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Check the sensor tubes: whether they are clogged with soot or water. Blow through per the manual.",
            "FMI 0, 1, 7, 15 (KamAZ: drop too high): check the filter for soot, and whether there has been a regeneration recently.",
            "FMI 3, 4, 20 (Sitrak: sensor voltage above the limit): the sensor's connector and supply.",
        ],
        "причины": [
            "Clogged particulate filter.",
            "Clogged sensor tubes.",
            "No regeneration carried out — short trips.",
            "The sensor itself.",
        ],
    },

    3361: {
        "узел": "The AdBlue dosing unit (SCR 1): the urea pump and injector. It feeds the required amount of urea into the exhaust before the catalyst.",
        "нормы": [
            ("Urea pump temperature", "within the working range per diagnostics"),
            ("Urea injector resistance and connector", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Check whether the urea nozzle is clogged with crystals: remove the injector and inspect the opening.",
            "FMI 3, 4, 5 (KamAZ: injector short to plus or open circuit): unplug the injector connector, inspect it and check the wire.",
            "FMI 2, 9, 12 (unreliable internal pump temperature): check the pump connector and cooling; if it repeats — the pump per the manual.",
            "FMI 2, 3, 4, 5 (Sitrak: metering spray valve jammed): after checking the connector, replace the unit.",
        ],
        "причины": [
            "Urea crystallisation in the injector.",
            "Oxidised connector or chafed wire.",
            "Pump or metering unit with a faulty valve.",
            "Poor-quality urea (see code 3364).",
        ],
    },

    3363: {
        "узел": "The AdBlue tank heater (the tank heating valve). In winter it stops the urea freezing in the tank; without it the system does not work in frost.",
        "нормы": [
            ("Heater and valve circuit resistance", "per the manufacturer's manual"),
            ("Valve voltage with the heating on", "present and holding, without dips"),
        ],
        "шаги": [
            "Check whether the heating switches on on command: per diagnostics the valve state should change.",
            "FMI 3, 4, 5, 7 (short to plus or open circuit): unplug the valve connector, check the wire and the valve itself.",
            "FMI 0, 2, 3, 4 (overheating of the circuit, Sitrak): inspect the connector — is it getting hot? Overheating of the circuit is a sign of a short.",
            "If the code is present in frost and the valve is fine — check the heating relay and the fuse.",
        ],
        "причины": [
            "Open circuit of the heater or its connector.",
            "Short to plus in the heating wiring.",
            "Heating relay or fuse.",
            "Overheated connector with burnt contacts.",
        ],
    },

    3364: {
        "узел": "The AdBlue quality sensor in the tank: it measures whether the urea is diluted. From it the unit decides whether it can dose, and by how much.",
        "нормы": [
            ("Urea quality", "per the manufacturer's manual"),
            ("Dose correction after a top-up", "happens without a permanent code — per diagnostics"),
        ],
        "шаги": [
            "Check what has been added: AdBlue to the standard, not water and not diesel. If in doubt — drain and refill with good-quality urea.",
            "FMI 2, 3, 4, 5 (Sitrak: after a top-up the dose cannot be corrected): flush the system per the manual and check the quality sensor.",
            "FMI 9 (Foton: SCR system fault): check the tank sensors and the system per the manual.",
        ],
        "причины": [
            "Poor-quality or diluted urea.",
            "Urea quality sensor.",
            "Dirty tank.",
        ],
    },

    3464: {
        "узел": "The throttle actuator command (intake or exhaust, per the factory table). The unit sets the throttle position, the actuator moves it, and gives feedback.",
        "нормы": [
            ("Throttle position on command", "matches the set value — checked per diagnostics"),
            ("Throttle and actuator travel without sticking", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Check whether the throttle sticks: with the engine off turn it by hand (where access allows); the movement should be even, without sticking.",
            "FMI 0, 1, 2, 3 (regulation error, deviation): check the throttle actuator, the connector and the throttle for carbon.",
            "FMI 2, 3, 4, 6 (KamAZ: internal fault of the control unit): first check the actuator's connector and supply; if it repeats after a reset — the control unit per the manual.",
        ],
        "причины": [
            "Carbon and dirt on the throttle.",
            "Throttle actuator or its connector.",
            "Internal fault of the control unit.",
        ],
    },

    3513: {
        "узел": "The 5 V reference that the unit supplies to the sensors: one sensor supply branch. If the voltage is high or drops out, the sensors on this branch give wrong readings or go silent.",
        "нормы": [
            ("Reference voltage at the sensor connector, ignition on", "5.0 V ± 0.25"),
            ("Voltage at the unit pin with the sensor unplugged", "the same reference, without a drop"),
        ],
        "шаги": [
            "Measure the reference voltage at the connector with the ignition on.",
            "FMI 4 (voltage below normal, a drop): unplug the sensors of this branch one at a time. When the voltage returns to 5 V — this sensor or its wire is shorting the branch to ground.",
            "FMI 3 (voltage above normal): look for a short of the branch wire to plus. With the ignition off, check the sensor supply wire for a short to plus (+24 V or another circuit) and inspect the harness for chafing.",
            "FMI 5 (open circuit of the reference line, KamAZ): check the wire from the unit to the sensor connectors for continuity.",
            "If the voltage is still not normal with all sensors unplugged — the control unit.",
        ],
        "причины": [
            "Sensor that shorted the supply branch.",
            "Chafed wire or oxidised sensor supply connector.",
            "Control unit that does not hold the voltage.",
        ],
    },

    3673: {
        "узел": "The throttle position sensor, channel 2. The unit checks it against channel 1; if they disagree, it limits the fuel supply.",
        "нормы": [
            ("Two channels as the throttle moves", "rise together — per diagnostics"),
            ("Channel 2 signal in the working range", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Open the throttle (where accessible per the manual) and watch both channels in diagnostics.",
            "FMI 0, 1, 2 (KamAZ: signal above or below the working range): the sensor's connector and supply.",
            "FMI 1, 2, 3, 4 (Sitrak: open H-bridge of the throttle actuator): check the throttle actuator, its connector and the throttle sticking.",
        ],
        "причины": [
            "Carbon and dirt on the throttle.",
            "Oxidised sensor connector.",
            "Faulty throttle actuator.",
        ],
    },

    4334: {
        "узел": "The AdBlue (urea) pressure sensor in the dosing module. The unit uses it to check that the urea is being supplied at the right pressure.",
        "нормы": [
            ("Urea pressure when the system is running", "per the manufacturer's manual"),
            ("Pressure at system start", "within the limits the unit allows per diagnostics"),
        ],
        "шаги": [
            "Inspect the urea line and filter: crystals, leaks, blockage.",
            "FMI 1, 7, 12, 18 (pressure dropped, system shut down, KamAZ): check the urea pump, the leak in the line, the filter and the line heating in frost.",
            "FMI 18 (unlikely pressure at start, DAF): check the sensor and the connector; crystallisation in the module — clean it per the manual.",
        ],
        "причины": [
            "Urea crystallisation.",
            "Clogged urea filter.",
            "Urea pump.",
            "Leak in the line.",
        ],
    },

    4340: {
        "узел": "AdBlue line heater No. 1 (the urea supply line). In winter it stops the urea freezing in the pipe; without it the system does not supply urea in frost.",
        "нормы": [
            ("Heater resistance", "per the manufacturer's manual"),
            ("Heating switches on on command", "present — per diagnostics"),
        ],
        "шаги": [
            "FMI 3, 4 (3 — short to supply, 4 — open circuit; Dongfeng): unplug the heater connector and check the heater and the wire for continuity.",
            "FMI 2, 3, 4, 5 (Sitrak: output stage overheating): check the connector and the heater unit — is the connector itself getting hot?",
            "If the code is present in frost and the heater is fine — check the heating relay and the fuse.",
        ],
        "причины": [
            "Open circuit of the urea line heater.",
            "Oxidised heater connector.",
            "Heating relay or fuse.",
            "Overheating of the output stage.",
        ],
    },

    4360: {
        "узел": "The gas temperature sensor at the SCR catalyst inlet (SCR 1). The unit checks what temperature the exhaust arrives at the catalyst with: low temperature hinders SCR, high temperature is a risk of overheating; the limits are per the manual.",
        "нормы": [
            ("Temperature at the SCR inlet", "rises with engine load — per diagnostics; working range per the manual"),
            ("Temperature difference between SCR inlet and outlet", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Compare the reading with the exhaust temperature on other sensors (for example, at the SCR outlet, see code 4363) under the same load. If they differ a lot — the sensor.",
            "FMI 0, 15, 16 (temperature above normal): check whether the DPF is clogged with soot and whether the regeneration is working.",
            "FMI 2, 3, 4 (unreliable signal, electrics): the sensor connector and the wire for open circuit and short.",
        ],
        "причины": [
            "Clogged particulate filter or failed regeneration.",
            "The temperature sensor itself.",
            "Oxidised connector or chafed wire.",
            "Exhaust leak before the sensor, giving false readings.",
        ],
    },

    4363: {
        "узел": "The gas temperature sensor at the SCR catalyst outlet (SCR 1). It shows how hot the exhaust leaving the catalyst is. The unit uses it to monitor the SCR operation.",
        "нормы": [
            ("Temperature after the catalyst", "per diagnostics, within the working range per the manual"),
            ("Difference from the SCR inlet sensor (code 4360)", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Compare with the inlet sensor (code 4360) at the same load. A large gap with no reason — the sensor.",
            "FMI 0 (temperature after SCR too high): check whether the catalyst is not working and whether the DPF is clogged.",
            "FMI 3, 4, 15 (short circuit or open circuit): the sensor connector and the wire for open circuit and short.",
        ],
        "причины": [
            "Catalyst or DPF malfunction.",
            "The temperature sensor itself.",
            "Oxidised connector or chafed wire.",
        ],
    },
}
