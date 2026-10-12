# -*- coding: utf-8 -*-
"""English twin of own_checks_motor.py (engine batch). Same fields and keys."""

CHECKS = {
    27: {
        "узел": "The EGR valve position sensor. The valve feeds part of the exhaust back into the intake to cut nitrogen oxides. The sensor tells the ECU how far open the valve really is.",
        "нормы": [
            ("Reference voltage at the connector, ignition on", "5.0 V ± 0.25"),
            ("Signal in the working range", "0.5…4.5 V"),
        ],
        "шаги": [
            "Run the valve test from diagnostics: it should open and close fully.",
            "It does not move or moves in jerks — remove and inspect it: the valve is coked with soot. Clean it if it is not worn.",
            "EGR cooler: a crack lets coolant into the exhaust, which gives white smoke, and steam in the valve.",
            "FMI 3, 4: the connector and the 5 V reference. A connector next to the hot manifold — the plastic crumbles.",
            "After replacement — teach the valve position.",
        ],
        "причины": [
            "Coked valve.",
            "Valve actuator.",
            "Overheated connector.",
            "EGR cooler leak.",
        ],
    },

    29: {
        "узел": "The second channel of the accelerator pedal sensor. The ECU compares it with the first (SPN 91): if they do not agree, the ECU does not trust the pedal and holds idle or limits the revs.",
        "нормы": [
            ("Reference voltage at the connector, ignition on", "5.0 V ± 0.25"),
            ("Second channel", "on many pedals, half the voltage of the first channel"),
        ],
        "шаги": [
            "Watch both channels in diagnostics while pressing the pedal slowly: they should move together, without jumps.",
            "The second channel sometimes has its own 5 V supply — check it separately.",
            "The connector under the pedal, and the wire at floor level.",
            "Wear in one channel still means replacing the whole pedal.",
        ],
        "причины": [
            "Wear of the sensor in the pedal.",
            "Connector under the pedal.",
            "Sensor supply — if codes for other sensors (SPN 3509–3512) appear at the same time.",
        ],
    },

    51: {
        "узел": "The intake throttle position sensor. On a diesel the throttle does not control power: it is closed to push exhaust into recirculation, to heat the particulate filter during regeneration and to shut the engine down more gently.",
        "нормы": [
            ("Reference voltage at the connector, ignition on", "5.0 V ± 0.25"),
            ("Signal in the working range", "0.5…4.5 V"),
        ],
        "шаги": [
            "Remove the intake hose and look at the throttle: oil soot stops it moving and closing fully.",
            "Run the throttle test from diagnostics: it should travel from stop to stop without sticking.",
            "FMI 7 (not responding): soot or a jammed actuator; on a pneumatic actuator — an air leak to it.",
            "FMI 3, 4: the actuator connector and the 5 V reference.",
            "After cleaning or replacement, many makes need the end positions taught.",
        ],
        "причины": [
            "Oil soot on the throttle.",
            "Throttle actuator.",
            "Connector.",
            "End positions not taught.",
        ],
    },

    91: {
        "узел": "The accelerator pedal sensor sits right on the pedal. It has two independent channels inside: the second (SPN 29) lets the ECU catch an error in the first. Many pedals also have an idle switch (SPN 558).",
        "нормы": [
            ("Reference voltage at the connector, ignition on", "5.0 V ± 0.25"),
            ("First channel: pedal released — pressed to the floor", "usually about 0.5…1 V — 3.5…4.5 V"),
            ("Second channel", "on many pedals half of the first — per the factory data"),
        ],
        "шаги": [
            "In diagnostics watch the pedal position in percent: released — 0, floor — 100, and smoothly, without dropouts when pressing slowly.",
            "Dropouts when pressing slowly — the resistive track is worn: the pedal needs replacing.",
            "FMI 3, 4: the connector under the pedal — water from shoes and dirt from the mat get in there. The wire chafes on the floor with every press.",
            "If the code comes together with SPN 29 and 558 — a shared connector or pedal supply.",
            "After replacing the pedal, some makes need the end positions taught.",
        ],
        "причины": [
            "Worn sensor in the pedal.",
            "Water and dirt in the connector under the pedal.",
            "Wire chafed at floor level.",
            "End positions not taught after replacement.",
        ],
    },

    95: {
        "узел": "The differential pressure sensor on the fuel filter compares the pressure before and after the filter. As the difference grows, the filter is clogging.",
        "нормы": [
            ("Reference voltage at the connector, ignition on", "5.0 V ± 0.25"),
        ],
        "шаги": [
            "Replace the fuel filters: this code is almost always genuine.",
            "Filters are new but the code came back soon — dirt in the tank, and in winter wax: a diesel not suited to the season.",
            "In winter: is the filter heater working? Wax clogs a filter in minutes.",
            "FMI 3, 4 (electrical): the connector and the 5 V reference.",
        ],
        "причины": [
            "Clogged fuel filter.",
            "Summer diesel in frost.",
            "Dirty tank.",
            "Connector or sensor.",
        ],
    },

    97: {
        "узел": "The water-in-fuel sensor sits in the sedimenter of the coarse filter (separator). Water is heavier than fuel and collects at the bottom; the sensor detects it by conductivity.",
        "нормы": [
            ("Drain the sediment", "at every service and immediately on the signal"),
        ],
        "шаги": [
            "Drain the sediment from the filter-separator into a clear container. If there is water, the fault is not the sensor: drain until clean fuel comes out.",
            "Water comes back in a day or two — there is a lot of water in the tank: drain the tank sediment and recall where you refuelled.",
            "No water but the signal is there — disconnect the sensor connector, inspect it and wipe the electrodes; check whether the clear bowl has cracked.",
            "In winter the water in the bowl freezes: warm it up, do not replace the sensor.",
        ],
        "причины": [
            "Water in the fuel — a real one.",
            "Dirt on the sensor electrodes.",
            "Corroded connector at the bottom of the filter.",
            "Cracked separator bowl.",
        ],
    },

    98: {
        "узел": "The oil level sensor sits in the sump. Most trucks have a thermal type: the ECU briefly heats a wire in it and tells oil from air by how fast it cools. So the level is measured only with the engine stopped.",
        "нормы": [
            ("When the ECU measures the level", "after the engine is stopped, usually a few minutes later"),
            ("Level by the dipstick", "between the MIN and MAX marks"),
        ],
        "шаги": [
            "Check with the dipstick on level ground, 5–10 minutes after stopping.",
            "Oil above normal is also a code: overfilling, or fuel and coolant in the sump. Smell the oil and look at its colour.",
            "Dipstick level is normal — disconnect the sensor connector under the sump and inspect it: it sits low, where dirt and salt fly.",
            "Parked on a slope, or measured right after stopping — this is not a fault.",
        ],
        "причины": [
            "A real low or high level.",
            "Measurement on a slope.",
            "Connector of the sensor under the sump.",
            "The sensor itself — oil under its seal.",
        ],
    },

    102: {
        "узел": "The boost pressure sensor sits on the intake manifold after the intercooler. Three-wire (5 V, ground, signal), or four-wire together with the intake air temperature sensor (SPN 105). It reads absolute pressure: with the engine off it shows atmospheric, about 1 bar.",
        "нормы": [
            ("Reference voltage at the connector, ignition on", "5.0 V ± 0.25"),
            ("Signal in the working range", "0.5…4.5 V"),
            ("Engine off", "about 1 bar absolute, as for SPN 108"),
            ("Under full load", "usually 2.5…3.5 bar absolute — per the factory data"),
        ],
        "шаги": [
            "With the engine off, compare with atmospheric pressure (SPN 108) in diagnostics. A difference of more than 0.1 bar — the sensor or its supply.",
            "FMI 1, 18 (boost low): hoses and clamps between the turbo and the manifold, cracks in the intercooler. A whistle under load — that is where the hole is.",
            "Turbo actuation: the wastegate (SPN 1192) or variable geometry. A clogged air filter also drops the boost.",
            "FMI 0, 16 (boost high): the turbo wastegate does not open, or the geometry is jammed.",
            "FMI 3, 4: the connector and the 5 V reference. The sensor port clogs with oil soot from the turbo — remove it and look.",
        ],
        "причины": [
            "Boost leak: clamp, hose, intercooler.",
            "Turbo actuation: wastegate or geometry.",
            "Sensor port clogged with oil carbon.",
            "Connector or the sensor.",
            "Worn turbo.",
        ],
    },

    105: {
        "узел": "The intake manifold air temperature sensor, after the turbo and the intercooler. It is often one body with the boost sensor (SPN 102): four wires — 5 V, ground, pressure, temperature. The ECU uses it to protect the engine from hot air and to calculate the fuel quantity.",
        "нормы": [
            ("Resistance of a typical NTC sensor at 20 °C", "about 2…3 kΩ"),
            ("The same at 80 °C", "about 300 Ω — more precisely per the factory table"),
            ("Voltage at the harness connector with the sensor unplugged", "about 5 V"),
            ("Air after the intercooler under load", "usually not above 50…60 °C"),
        ],
        "шаги": [
            "FMI 0, 15, 16 (hot air): the intercooler is clogged with insects and dirt on the outside — wash it. Check the intercooler hoses and clamps: a crack also causes a loss of boost.",
            "FMI 3, 4: unplug the connector and measure the sensor resistance. An open sensor or wire is seen by the ECU as −40 °C frost (voltage high, FMI 3), a short as severe overheating (FMI 4). With the connector unplugged, the harness contacts should show about 5 V.",
            "Compare the diagnostics reading on a cold engine that has stood overnight with other temperatures: air, oil, coolant. All should be close to the outside temperature; one lagging 10 °C or more is suspect.",
            "If the sensor is combined with the boost sensor and SPN 102 is also present — check the connector and the shared 5 V supply, not each sensor separately.",
        ],
        "причины": [
            "Intercooler dirty on the outside.",
            "Corroded connector: the sensor sits low on the manifold, where water gets in.",
            "The sensor itself — an oil film from the turbo on the sensing element.",
            "Chafed wires at the manifold.",
        ],
    },

    108: {
        "узел": "The atmospheric pressure sensor, on most engines, sits inside the engine control unit. The ECU uses it to correct fuel delivery at altitude and checks the boost sensor against it with the engine stopped.",
        "нормы": [
            ("At sea level", "about 1.0 bar (100 kPa)"),
            ("At 1000 m altitude", "about 0.9 bar"),
        ],
        "шаги": [
            "Compare in diagnostics with the boost sensor (SPN 102) with the engine off: they should agree to within 0.1 bar. If they disagree, one of the two is lying.",
            "If the sensor is inside the unit: check for water in the housing, and whether the sensor opening is blocked with dirt or sealant.",
            "On engines with a separate sensor — the connector and the 5 V reference.",
            "Readings correct, supply fine, and the code stays — the control unit: update the software first, and only then decide on replacement.",
        ],
        "причины": [
            "Water or dirt in the unit housing.",
            "The neighbour is lying — the boost sensor, while the unit blames the atmospheric one.",
            "Faulty control unit.",
        ],
    },

    110: {
        "узел": "The coolant temperature sensor sits in the thermostat housing or in the cylinder head. It is a two-wire thermistor (NTC): the hotter it gets, the lower its resistance. The ECU uses it to decide how much fuel to give on start, when to switch on the fan, and when to cut power for overheating.",
        "нормы": [
            ("Resistance of a typical NTC sensor at 20 °C", "about 2…3 kΩ"),
            ("The same at 80 °C", "about 300 Ω — more precisely per the factory table"),
            ("Voltage at the harness connector with the sensor unplugged", "about 5 V"),
            ("Warm engine", "usually 80…95 °C"),
        ],
        "шаги": [
            "FMI 0, 15, 16 (temperature high): check the engine first, not the sensor. Coolant level in the expansion tank, belt and fan clutch, radiator clogged with dirt on the outside, tank cap.",
            "Compare the dash reading with an infrared thermometer on the top radiator hose. If they agree — the overheating is real.",
            "FMI 3, 4: unplug the connector and measure the sensor resistance. An open sensor or wire is seen by the ECU as −40 °C frost (voltage high, FMI 3), a short as severe overheating (FMI 4). With the connector unplugged, the harness contacts should show about 5 V.",
            "Compare the diagnostics reading on a cold engine that has stood overnight with other temperatures: air, oil, coolant. All should be close to the outside temperature; one lagging 10 °C or more is suspect.",
            "FMI 1, 17, 18 (not warming up): a thermostat stuck open — especially in winter at idle.",
        ],
        "причины": [
            "Real overheating: low coolant, dirty radiator, fan clutch, water pump.",
            "Thermostat stuck open or closed.",
            "Corroded sensor connector.",
            "The sensor itself.",
            "Air lock after a coolant change.",
        ],
    },

    111: {
        "узел": "The coolant level sensor sits in the expansion tank. Usually it is a float with a reed switch, or an electrode sensor on two or three wires. It is often wired not to the engine unit but to the dash.",
        "нормы": [
            ("Level in the tank on a cold engine", "between the MIN and MAX marks"),
        ],
        "шаги": [
            "Level in the tank on a cold engine. Low — look for a leak, not a sensor fault: hoses, radiator, water pump, heater, oil cooler.",
            "Coolant disappears with no external trace — it is going into the engine: foam or oil in the tank, white smoke.",
            "Level normal but the code is there — disconnect the connector, inspect it and check the sensor for continuity: the float switches when the tank is tilted.",
            "Float stuck from dirty coolant — flush the tank.",
        ],
        "причины": [
            "A real coolant leak.",
            "Float stuck in a dirty tank.",
            "Connector on the tank — the area is wet.",
            "Head gasket or oil cooler — coolant leaks inside.",
        ],
    },

    131: {
        "узел": "The exhaust back-pressure sensor measures the pressure in the exhaust manifold before the turbo. It is connected to the manifold by a metal pipe so that it does not overheat. It is needed to control gas recirculation and the turbo.",
        "нормы": [
            ("Reference voltage at the connector, ignition on", "5.0 V ± 0.25"),
            ("Signal in the working range", "0.5…4.5 V"),
            ("Engine off", "atmospheric pressure, as for SPN 108"),
        ],
        "шаги": [
            "With the engine off, compare with atmospheric pressure (SPN 108) — they should match.",
            "Take the pipe from the manifold to the sensor off and blow it through: it clogs with soot and condensate, and cracks in it give a low pressure reading.",
            "FMI 0 (pressure high): clogged particulate filter or catalyst, jammed turbo geometry, closed exhaust flap (SPN 1074).",
            "FMI 3, 4: the connector and the 5 V reference.",
        ],
        "причины": [
            "Clogged or cracked pipe to the sensor.",
            "Clogged exhaust aftertreatment system.",
            "Turbo or exhaust flap.",
            "The sensor itself — from overheating.",
        ],
    },

    132: {
        "узел": "The mass air flow sensor sits in the duct after the air filter. Inside is a heated film: the air cools it, and from this the ECU works out how much air goes into the engine. It is needed for exhaust gas recirculation (EGR).",
        "нормы": [
            ("Supply", "per the make's wiring diagram: battery voltage and a separate 5 V"),
            ("Signal with ignition on, engine stopped", "about 1 V"),
        ],
        "шаги": [
            "Remove it and look at the sensing element: oil or dust on it makes the sensor read low. Clean it only with a special cleaner, without touching the film.",
            "The duct from the filter to the sensor, and after it: air leaking past the sensor gives \"too little air\" even though the sensor is good.",
            "Air filter: a torn one lets dust onto the sensor.",
            "Oil on the element comes from the crankcase breather — check the breather.",
            "FMI 3, 4: the connector and the supply per the wiring diagram.",
        ],
        "причины": [
            "Dirty sensing element.",
            "Air leak past the sensor.",
            "Oil from the crankcase breather.",
            "Connector or the sensor itself.",
        ],
    },

    171: {
        "узел": "The outside air temperature sensor sits in the bumper, under the cab or in the mirror. Often it is read by the dash or the climate control, and the engine gets the value over CAN — then FMI 9 and 19 mean the message is lost, not that the sensor is faulty.",
        "нормы": [
            ("Resistance of a typical NTC sensor at 20 °C", "about 2…3 kΩ"),
            ("The same at 80 °C", "about 300 Ω — more precisely per the factory table"),
            ("Voltage at the harness connector with the sensor unplugged", "about 5 V"),
        ],
        "шаги": [
            "FMI 9, 19 (no data on the bus): the code is not about the sensor. Check which unit transmits the temperature (dash or climate control) and its link — SPN 639.",
            "FMI 3, 4: unplug the connector and measure the sensor resistance. An open sensor or wire is seen by the ECU as −40 °C frost (voltage high, FMI 3), a short as severe overheating (FMI 4). With the connector unplugged, the harness contacts should show about 5 V.",
            "Compare with a thermometer in the shade. A sensor at the bumper in the sun, or near a hot engine, reads wrong when parked and evens out on the move — this is not a fault.",
        ],
        "причины": [
            "Sensor broken by a stone or torn off in the bumper.",
            "Corroded connector: the area is wet and salty in winter.",
            "No link to the unit that transmits the value.",
            "The sensor itself.",
        ],
    },

    172: {
        "узел": "The intake air temperature sensor — before the turbo, in the air filter housing or on the duct after it. Often it is combined with the air flow sensor (SPN 132).",
        "нормы": [
            ("Resistance of a typical NTC sensor at 20 °C", "about 2…3 kΩ"),
            ("The same at 80 °C", "about 300 Ω — more precisely per the factory table"),
            ("Voltage at the harness connector with the sensor unplugged", "about 5 V"),
        ],
        "шаги": [
            "FMI 3, 4: unplug the connector and measure the sensor resistance. An open sensor or wire is seen by the ECU as −40 °C frost (voltage high, FMI 3), a short as severe overheating (FMI 4). With the connector unplugged, the harness contacts should show about 5 V.",
            "Compare the diagnostics reading on a cold engine that has stood overnight with other temperatures: air, oil, coolant. All should be close to the outside temperature; one lagging 10 °C or more is suspect.",
            "Reads much warmer than outside while driving — the air is not coming from outside: the intake hose is torn off, and the engine is drawing hot air from under the cab.",
            "If the sensor is shared with the air flow meter and SPN 132 is present — the connector and the supply are shared.",
        ],
        "причины": [
            "Connector or wires.",
            "Torn-off or cracked air intake hose.",
            "The sensor itself.",
        ],
    },

    174: {
        "узел": "The fuel temperature sensor sits on the fuel pump, the filter or the return line. Hot fuel is thinner: the ECU reduces delivery and the engine loses power.",
        "нормы": [
            ("Resistance of a typical NTC sensor at 20 °C", "about 2…3 kΩ"),
            ("The same at 80 °C", "about 300 Ω — more precisely per the factory table"),
            ("Voltage at the harness connector with the sensor unplugged", "about 5 V"),
        ],
        "шаги": [
            "FMI 0, 15, 16 (fuel hot): low fuel in the tank — the return warms a small volume faster. Top up and see whether the code goes away.",
            "Fuel cooler on the return (where fitted) clogged with dirt on the outside.",
            "A large leak-off from the injectors also heats the fuel — check the return.",
            "FMI 3, 4: unplug the connector and measure the sensor resistance. An open sensor or wire is seen by the ECU as −40 °C frost (voltage high, FMI 3), a short as severe overheating (FMI 4). With the connector unplugged, the harness contacts should show about 5 V.",
            "Compare the diagnostics reading on a cold engine that has stood overnight with other temperatures: air, oil, coolant. All should be close to the outside temperature; one lagging 10 °C or more is suspect.",
        ],
        "причины": [
            "Driving on a nearly empty tank.",
            "Dirty fuel cooler.",
            "Worn injectors with high leak-off.",
            "Connector or the sensor itself.",
        ],
    },

    175: {
        "узел": "The oil temperature sensor sits in the block's oil gallery or in the oil module housing. Some are separate, some share a housing with the oil pressure sensor.",
        "нормы": [
            ("Resistance of a typical NTC sensor at 20 °C", "about 2…3 kΩ"),
            ("The same at 80 °C", "about 300 Ω — more precisely per the factory table"),
            ("Voltage at the harness connector with the sensor unplugged", "about 5 V"),
            ("Oil on a warm engine", "usually 90…110 °C"),
        ],
        "шаги": [
            "FMI 0, 15, 16 (oil hot): low oil level; the oil heat exchanger clogged with deposits on the coolant side; the engine ran for a long time at full load at low speed.",
            "Oil hot but the coolant is normal — the heat exchanger or its thermostatic valve.",
            "FMI 3, 4: unplug the connector and measure the sensor resistance. An open sensor or wire is seen by the ECU as −40 °C frost (voltage high, FMI 3), a short as severe overheating (FMI 4). With the connector unplugged, the harness contacts should show about 5 V.",
            "Compare the diagnostics reading on a cold engine that has stood overnight with other temperatures: air, oil, coolant. All should be close to the outside temperature; one lagging 10 °C or more is suspect.",
        ],
        "причины": [
            "Oil heat exchanger clogged.",
            "Low oil level.",
            "Connector of the sensor in the oil or corroded.",
            "The sensor itself.",
        ],
    },

    190: {
        "узел": "The ECU counts engine speed from the sensor on the flywheel (crankshaft). It is an inductive two-wire sensor or a three-wire Hall sensor. Without it the engine will not start or stalls, unless there is a spare sensor on the camshaft (SPN 723).",
        "нормы": [
            ("Resistance of an inductive sensor", "usually about 0.8…1.2 kΩ — per the factory data"),
            ("Air gap to the flywheel teeth", "usually 0.5…1.5 mm"),
            ("Inductive signal on cranking", "from a few tenths of a volt AC"),
        ],
        "шаги": [
            "Remove the sensor and look at the tip: metal swarf on the magnet is the main cause of a weak signal. Wipe it off.",
            "Inductive — measure the resistance and compare with the camshaft sensor if it is the same type.",
            "Is the sensor loose in its bore? Are the flywheel teeth intact?",
            "FMI 2, 8 (signal unreliable): the sensor wire's screen, a wire running alongside the starter or alternator power cables, a crack in the ring gear.",
            "Codes for crankshaft and camshaft at once — check their relative position: after engine repair the timing marks may have shifted by a tooth.",
        ],
        "причины": [
            "Swarf on the sensor.",
            "Connector or wire, especially at the starter.",
            "The sensor itself.",
            "Damaged flywheel teeth.",
        ],
    },

    558: {
        "узел": "The idle switch on the accelerator pedal — a contact that tells the ECU \"pedal released\". The ECU checks it against the pedal sensor (SPN 91).",
        "нормы": [
            ("Pedal released", "contact in one position"),
            ("Pedal slightly pressed", "switches at the very start of travel"),
        ],
        "шаги": [
            "In diagnostics: the switch changes state at the start of pedal travel, earlier than the sensor shows a few percent.",
            "Switches late or not at all — the pedal does not return fully: mat, dirt, spring.",
            "The connector under the pedal.",
            "If that does not help — the switch is inside the pedal; usually the pedal is replaced.",
        ],
        "причины": [
            "Mat or dirt stops the pedal returning.",
            "Switch wear.",
            "Connector under the pedal.",
        ],
    },

    636: {
        "узел": "The crankshaft position sensor sits on the flywheel housing and reads the marks on the flywheel or the rear end of the crankshaft. From it the ECU knows not only the speed but also which cylinder's piston is where — so it knows when to inject.",
        "нормы": [
            ("Resistance of an inductive sensor", "usually about 0.8…1.2 kΩ — per the factory data"),
            ("Air gap to the flywheel", "usually 0.5…1.5 mm"),
        ],
        "шаги": [
            "Remove the sensor: swarf on the tip, a cracked body, marks where it touched the flywheel.",
            "The connector is low on the flywheel housing, where oil from the crankshaft seal gets in. Oil in the connector — look at the seal first.",
            "Inductive sensor — resistance; Hall sensor — supply and ground at the connector.",
            "FMI 7, 11 (position does not match the camshaft): after replacing the timing belt or chain, gears or flywheel — check the marks. A stretched chain over mileage does this too.",
            "The engine is hard to start but does start — the ECU is running on the spare camshaft sensor (SPN 723).",
        ],
        "причины": [
            "Swarf or oil on the sensor.",
            "Connector full of oil from the crankshaft seal.",
            "Timing marks shifted after repair.",
            "The sensor itself.",
        ],
    },

    723: {
        "узел": "The second speed sensor — on the camshaft or on the injection pump drive gear. It tells the ECU which stroke each cylinder is on, and it stands in for the crankshaft sensor if that fails. On its own this code usually does not stop the engine, but starting becomes longer.",
        "нормы": [
            ("Resistance of an inductive sensor", "usually about 0.8…1.2 kΩ — per the factory data"),
        ],
        "шаги": [
            "Remove and inspect the sensor tip: swarf, signs of contact.",
            "Connector and wire: the sensor is on the cylinder head, and the wire runs alongside hot parts — the braid dries out and cracks.",
            "Resistance or supply of the Hall sensor.",
            "FMI 7 (does not match the crankshaft): camshaft marks after repair, a stretched chain.",
        ],
        "причины": [
            "Connector or wire by the hot parts.",
            "Swarf on the sensor.",
            "Shifted marks or a stretched chain.",
            "The sensor itself.",
        ],
    },

    974: {
        "узел": "Remote accelerator or hand throttle — a second control for engine speed: on work equipment, in the body, at the power take-off.",
        "нормы": [
            ("Reference voltage at the connector, ignition on", "5.0 V ± 0.25"),
            ("Signal in the working range", "0.5…4.5 V"),
        ],
        "шаги": [
            "Find out where the remote throttle is on this vehicle: the PTO controller, buttons on the steering wheel, the body builder's remote panel.",
            "Check the connector on the panel — it is often outside the cab, in the dirt.",
            "If there is no remote throttle on the vehicle but the code is present — the parameter has been switched on by mistake: switch it off in the ECU.",
            "Supply and signal at the connector — as for the accelerator pedal.",
        ],
        "причины": [
            "Connector of the remote panel outside the cab.",
            "Parameter enabled, with no panel fitted.",
            "The panel itself.",
        ],
    },

    1071: {
        "узел": "The fan control output: the ECU switches the fan clutch solenoid or the electro-pneumatic valve. The code is about this circuit.",
        "нормы": [
            ("Clutch or valve winding", "per the factory data, usually from a few to tens of ohms"),
        ],
        "шаги": [
            "Fan test from diagnostics: listen whether it switches in.",
            "The connector on the clutch and the wire to it — next to the blades and the belt.",
            "Winding resistance: open — FMI 5, short — FMI 6 or 4.",
            "While the circuit is faulty, many clutches default to running the fan all the time — fuel use and noise.",
        ],
        "причины": [
            "Wire at the clutch.",
            "Winding of the clutch solenoid.",
            "Connector.",
        ],
    },

    1192: {
        "узел": "The control air pressure to the turbo wastegate actuator. Through an electro-pneumatic valve the ECU feeds air to the actuator; the wastegate opens and vents surplus exhaust past the turbo — that is how boost is held.",
        "нормы": [
            ("Reference voltage at the connector, ignition on", "5.0 V ± 0.25"),
            ("Signal in the working range", "0.5…4.5 V"),
            ("Pneumatic system pressure", "working, no leaks"),
        ],
        "шаги": [
            "The tube from the control valve to the turbo actuator: cracked, slipped off, or coked.",
            "Run the valve test: the actuator on the turbo should move the linkage.",
            "The actuator rod on the turbo moves freely by hand; if it is seized, boost rises or falls (SPN 102).",
            "FMI 3, 4: the connector of the electro-pneumatic valve and the sensor.",
        ],
        "причины": [
            "Tube to the actuator.",
            "Seized wastegate rod.",
            "Electro-pneumatic control valve.",
            "Leak in the actuator itself.",
        ],
    },

    1639: {
        "узел": "The cooling fan speed sensor sits on the fan's viscous clutch. The ECU compares how much fan speed it commanded with how fast the fan is actually turning.",
        "нормы": [
            ("Signal", "usually a Hall sensor; supply per the make's diagram"),
        ],
        "шаги": [
            "On a hot engine run the fan test: listen for it picking up.",
            "The fan does not pick up — the clutch: silicone fluid leak, wear.",
            "The connector on the clutch itself: the wire runs to a rotating unit, so it gets chafed and caught by the blades.",
            "If the fan is electronically controlled — the code SPN 1071 for the clutch control circuit.",
        ],
        "причины": [
            "Wire to the clutch chafed or broken by the blades.",
            "Clutch wear.",
            "Sensor on the clutch.",
        ],
    },

    2791: {
        "узел": "EGR valve control: the ECU feeds current or air to the valve actuator. The code is about this control circuit: the actuator itself, its supply, or the valve not moving where it was told.",
        "нормы": [
            ("Electric actuator: winding resistance", "per the factory data, usually from a few to tens of ohms"),
            ("Pneumatic actuator: control pressure", "as in the pneumatic system, without leaks"),
        ],
        "шаги": [
            "Valve test from diagnostics: listen to it moving.",
            "Electric actuator: connector and winding — open, and short to the body.",
            "Pneumatic actuator: the tube to the actuator, the solenoid control valve, leaks.",
            "Valve coked — the actuator cannot move it, and the ECU sees an actuator fault.",
            "If there is also a position code, SPN 27 — check the valve itself first.",
        ],
        "причины": [
            "Coked valve.",
            "Actuator or its connector.",
            "Pneumatic actuator: air leak.",
        ],
    },
}
