# -*- coding: utf-8 -*-
"""English twin of own_checks_brake.py (ABS wheel sensors and modulator valves,
EBS, pedal switches, retarder, engine brake, speed signals, PTO). Same fields and keys.

Wheel sensors (789–794) and modulator valves (795–800) share one wording and differ
only by axle and side, so they are built from templates; the wording is the same
as in the Russian file.
"""

_SENSOR_NORMS = [
    ("Sensor resistance, WABCO", "0.9…1.3 kΩ"),
    ("Sensor resistance, Knorr-Bremse", "about 1.7 kΩ"),
    ("Sensor-to-ring gap", "not more than 0.7 mm"),
    ("Voltage with the wheel turning at 3 km/h", "not less than 100 mV AC"),
]

_SENSOR_TAIL = [
    "FMI 1, 2, 7, 8, 10 (weak or erratic signal): push the sensor home against the ring — it will "
    "settle at the right gap on the first turn of the wheel. Check the hub play.",
    "Turn the wheel and look at the ring: broken teeth, dirt, rust, run-out. Replace the sensor "
    "together with its clamping bush and grease.",
]

_SENSOR_CAUSES_TAIL = [
    "The sensor itself.",
    "A sensor of another make: WABCO and Knorr-Bremse have different resistance.",
]


def _wheel_front(side, other):
    return {
        "узел": ("The ABS wheel speed sensor on the %s wheel of the front axle. Inductive, two-wire: it "
                 "sits in the steering knuckle, and the cable runs to the frame in a loop that flexes at "
                 "every steering turn. It has no supply — it generates an AC voltage itself when the wheel "
                 "turns." % side),
        "нормы": list(_SENSOR_NORMS),
        "шаги": [
            "Disconnect the sensor's connector at the ABS unit and measure the resistance together with the "
            "extension cable. Compare with the sensor on the %s of the same axle — the best reference." % other,
            "FMI 3, 4, 5, 6 (open or short): if out of spec, remove the extension and measure directly at the "
            "sensor. If the sensor is in spec — the cable, most often at the bend by the steering knuckle: the "
            "cable breaks from the steering turns.",
            "Turn the steering to the stop both ways and check whether the cable pulls tight or rubs against "
            "the knuckle or the track rod.",
        ] + _SENSOR_TAIL,
        "причины": [
            "The sensor has moved away from the ring: old bush, hub play, repair without pushing it home.",
            "The cable at the bend by the steering knuckle: it breaks from steering turns.",
            "Dirty or damaged toothed ring.",
        ] + _SENSOR_CAUSES_TAIL,
    }


def _wheel_second(side, other):
    return {
        "узел": ("The ABS wheel speed sensor on the %s wheel of the second (usually driven) axle. Inductive, "
                 "two-wire: it sits in a holder on the axle beam behind the brake mechanism, and the cable runs "
                 "along the beam to the frame. It has no supply — it generates an AC voltage itself when the "
                 "wheel turns." % side),
        "нормы": list(_SENSOR_NORMS),
        "шаги": [
            "Disconnect the sensor's connector at the ABS unit and measure the resistance together with the "
            "extension cable. Compare with the sensor on the %s of the same axle — the best reference." % other,
            "FMI 3, 4, 5, 6 (open or short): if out of spec, remove the extension and measure directly at the "
            "sensor. If the sensor is in spec — the cable, most often on the axle beam and by the spring, where "
            "it is clamped by the straps.",
            "Inspect the hub seal: oil from the hub settles on the sensor and the ring, dirt sticks — the signal weakens.",
        ] + _SENSOR_TAIL,
        "причины": [
            "The sensor has moved away from the ring: old bush, hub play, repair without pushing it home.",
            "The cable on the axle beam and by the spring, where it is clamped by the straps.",
            "Dirty or damaged toothed ring.",
        ] + _SENSOR_CAUSES_TAIL,
    }


def _wheel_third(side, other):
    return {
        "узел": ("The ABS wheel speed sensor on the %s wheel of the third axle. Inductive, two-wire: it sits at "
                 "the hub of the third axle; on many vehicles this axle is a lift or tag axle. It has no supply — "
                 "it generates an AC voltage itself when the wheel turns." % side),
        "нормы": list(_SENSOR_NORMS),
        "шаги": [
            "Disconnect the sensor's connector at the ABS unit and measure the resistance together with the "
            "extension cable. Compare with the sensor on the %s of the same axle — the best reference." % other,
            "FMI 3, 4, 5, 6 (open or short): if out of spec, remove the extension and measure directly at the "
            "sensor. If the sensor is in spec — the cable, most often between the beam and the frame: on a lift "
            "axle the cable tightens at every lift.",
            "If the axle is a lift axle — raise it and lower it, watching the cable: does it go taut in the raised position?",
        ] + _SENSOR_TAIL,
        "причины": [
            "The sensor has moved away from the ring: old bush, hub play, repair without pushing it home.",
            "The cable between the beam and the frame: on a lift axle it tightens at every lift.",
            "Dirty or damaged toothed ring.",
        ] + _SENSOR_CAUSES_TAIL,
    }


_VALVE_NORMS = [
    ("One coil, valve at 24 V", "10.7…25 Ω, usually about 15"),
    ("Both coils in series (between the two coil terminals)", "21.4…50 Ω"),
    ("Same for a 12 V valve", "4.0…9.2 and 8.0…18.4 Ω"),
    ("Coil to body", "infinity"),
]


def _valve(where):
    return {
        "узел": ("The ABS pressure modulator valve for the %s — it sits on the frame near the wheel, between the "
                 "brake valve and the brake chamber. Inside are two solenoids: the inlet one holds the pressure, "
                 "the outlet one releases it. The ABS unit clicks them when the wheel starts to lock." % where),
        "нормы": list(_VALVE_NORMS),
        "шаги": [
            "Switch the ignition on: during the check the ABS unit clicks the valves one after another — audible "
            "at each wheel. This valve is silent — the circuit.",
            "FMI 3, 4, 5, 6: unplug the valve connector and measure each coil against the common terminal. Zero — "
            "a short; megohms — an open circuit.",
            "Coils within spec — check the wire from the valve to the ABS unit for continuity: the valve connector "
            "on the frame is in dirt and salt.",
            "The valve bleeds air constantly — dirt or water under the diaphragm: check the air dryer.",
            "Check with the test in diagnostics: the chamber pressure falls and rises on command.",
        ],
        "причины": [
            "Valve connector on the frame: oxidation, water.",
            "Wire to the valve.",
            "Valve coil.",
            "Dirt and water in the valve — from a failed air dryer.",
        ],
    }


CHECKS = {
    84: {
        "узел": "Vehicle speed from the wheel sensors: the ABS or EBS unit calculates it from the wheel sensors and sends it over the bus. The engine, the gearbox, the cruise control and the dash take it from there.",
        "нормы": [
            ("Difference from the tachograph speed (SPN 1624)", "within a few per cent"),
        ],
        "шаги": [
            "Read the codes of the ABS unit: a faulty wheel sensor (SPN 789–794) immediately spoils the speed too.",
            "FMI 9, 19: the message is lost — the bus link with the ABS unit (SPN 639).",
            "FMI 2 (unreliable): compare with the tachograph. If it differs by a constant percentage — the ABS unit has the wrong tyre size or ring tooth count, or the tyres fitted are of a different size.",
            "Different tyres on the axles also give a difference in wheel speeds.",
        ],
        "причины": [
            "ABS wheel sensor.",
            "Wrong tyre size in the parameters.",
            "Link with the ABS unit.",
        ],
    },

    520: {
        "узел": "The actual retarder braking torque in per cent — the retarder reports it over the bus. FMI 9, 11, 12 mean the message is lost or unreliable.",
        "нормы": [],
        "шаги": [
            "Read the codes of the retarder unit itself — the cause is there.",
            "The retarder unit's link over the bus.",
            "Retarder oil: level and temperature — when overheated, the retarder reduces its torque.",
        ],
        "причины": [
            "Link with the retarder unit.",
            "Retarder fault.",
            "Overheated retarder oil.",
        ],
    },

    596: {
        "узел": "The cruise control enable switch — the main button, or the position of the stalk switch that switches the cruise on.",
        "нормы": [],
        "шаги": [
            "Check the switching in diagnostics.",
            "The stalk switch: the connector under the steering column cover, and the spiral cable that turns with the wheel.",
            "The cruise does not switch on even without a code — conditions: the brake switch (SPN 597) and the clutch switch (SPN 598), speed (SPN 84).",
        ],
        "причины": [
            "Stalk switch.",
            "Connector under the column cover.",
            "Switch-on conditions not met.",
        ],
    },

    597: {
        "узел": "The brake pedal switch. The engine uses it to cancel the cruise control, the gearbox uses it to allow manoeuvres, and the brake lights come on from it. The unit checks it against other signs of braking — pressure or the pedal sensor.",
        "нормы": [
            ("Pedal released — pressed", "the contact switches at the start of pedal travel"),
        ],
        "шаги": [
            "Watch the switch state in diagnostics while pressing the pedal slowly: does it switch, and at what point?",
            "The switch may be a dual one — two contacts, normally open and normally closed. The unit catches it if they do not match.",
            "Adjustment of the switch relative to the pedal.",
            "The connector under the pedal.",
            "On vehicles with EBS the pedal signal comes from the brake module over the bus — check its codes (SPN 1066, 1067).",
        ],
        "причины": [
            "Misadjusted switch.",
            "Switch wear.",
            "Connector.",
            "Pedal does not return fully.",
        ],
    },

    598: {
        "узел": "The clutch pedal switch: for the cruise control, start permission and gear changes.",
        "нормы": [
            ("Pedal released — pressed", "the contact switches"),
        ],
        "шаги": [
            "Watch the switch state in diagnostics when the pedal is pressed.",
            "Adjustment and mounting of the switch on the pedal.",
            "The connector under the pedal.",
            "On vehicles with an automated gearbox there is no clutch pedal — the code means the switch is enabled in the parameters by mistake.",
        ],
        "причины": [
            "Adjustment or mounting of the switch.",
            "Switch wear.",
            "Connector.",
            "Parameter set with no pedal fitted.",
        ],
    },

    801: {
        "узел": "The retarder control relay: the ABS or EBS unit switches the retarder off when the wheels start to lock. The code is about this circuit.",
        "нормы": [],
        "шаги": [
            "Find the relay from the diagram; check its click with the test in diagnostics.",
            "Swap in an identical relay.",
            "The wire from the unit to the relay, and from the relay to the retarder.",
            "If the vehicle has no retarder — the output is enabled in the parameters by mistake.",
        ],
        "причины": [
            "Relay.",
            "Wire.",
            "Parameter with no retarder fitted.",
        ],
    },

    810: {
        "узел": "A speed signal input: the unit receives speed from an external source over a wire, not over the bus. The code means the signal is unreliable or lost.",
        "нормы": [],
        "шаги": [
            "Find from the diagram where the unit takes the signal from: the tachograph, the gearbox sensor.",
            "The signal wire: short, open circuit, interference from neighbouring power cables.",
            "Compare with other speeds (SPN 84, 1624).",
        ],
        "причины": [
            "Signal wire.",
            "Signal source.",
            "Different speed parameters in the units.",
        ],
    },

    985: {
        "узел": "The air-conditioning condenser fan relay, on high pressure: when the refrigerant pressure is high, the fan switches on to cool the condenser.",
        "нормы": [],
        "шаги": [
            "The relay per the diagram — check its click with the test, and swap it.",
            "The pressure sensor in the air-conditioning circuit and its connector.",
            "The condenser clogged with dirt on the outside — the pressure rises.",
        ],
        "причины": [
            "Relay.",
            "Air-conditioning pressure sensor.",
            "Dirty condenser.",
        ],
    },

    1056: {
        "узел": "Trailer control in the tractor's electronic brake system (EBS): a proportional valve in the trailer control valve. The EBS unit sets the pressure in the trailer's yellow (control) line through it.",
        "нормы": [
            ("Pressure in the red (supply) head", "usually 7.0…8.1 bar"),
            ("Pressure to the trailer", "not more than 8.5 bar"),
        ],
        "шаги": [
            "FMI 3, 4, 5, 6: the connector on the trailer control valve — it is on the frame at the back of the cab, in dirt. Check the coil and the wires to the EBS unit for continuity.",
            "FMI 7, 13: the pressure is not what was commanded. Connect a gauge to the yellow head, press the brake, and compare with what the diagnostics shows.",
            "Trailer control valve: dirt and water inside — from a failed air dryer.",
            "A leak in the yellow line up to the head, or in the head — the valve cannot hold the pressure.",
        ],
        "причины": [
            "Connector on the trailer control valve.",
            "Dirt and water in the valve.",
            "Leak in the line to the trailer.",
            "The valve itself.",
        ],
    },

    1066: {
        "узел": "The brake signal sensor-transmitter — the electrical part of the brake module under the pedal in the EBS system. It has two channels that tell the unit how far the pedal is pressed.",
        "нормы": [],
        "шаги": [
            "Watch both pedal channels in diagnostics while pressing slowly: they should move together, without jumps.",
            "The connector of the brake module: it is under the cab, in water and dirt.",
            "The pedal travels to the stop freely — the mat and dirt do not get in the way.",
            "Codes persist with a clean connector — the electrical part of the module; usually the whole module is replaced.",
        ],
        "причины": [
            "Connector of the brake module under the cab.",
            "Wear of the sensors in the module.",
            "Pedal does not return.",
        ],
    },

    1067: {
        "узел": "The first brake signal channel in the EBS brake module. The unit compares it with the second channel and with the pressure in the circuits.",
        "нормы": [],
        "шаги": [
            "Compare the channels in diagnostics when the pedal is pressed slowly.",
            "The connector of the brake module under the cab.",
            "FMI 7 (does not match the pressure): a leak in the module's pneumatic circuit — then the signal is there but the pressure is not.",
            "Replacing the module — with the pedal zero position taught by the programme.",
        ],
        "причины": [
            "Module connector.",
            "Sensor wear.",
            "Leak in the pneumatic part of the module.",
        ],
    },

    1072: {
        "узел": "Output to the compression engine brake: the unit switches on a solenoid valve, which changes how the exhaust valves work through oil or air.",
        "нормы": [
            ("Engine brake valve winding", "per the factory data, usually from a few to tens of ohms"),
        ],
        "шаги": [
            "Switch the engine brake on with the test on site: is the change in the engine's sound audible?",
            "FMI 3, 4, 5, 6: the valve connector — on many engines it is under the valve cover.",
            "FMI 7: the circuit is intact but there is no braking — oil pressure at the valve, adjustment of the engine brake mechanism's clearance.",
            "The engine brake should not work below the threshold speed or without the right revs — that is not a fault.",
        ],
        "причины": [
            "Wire or connector under the valve cover.",
            "Valve winding.",
            "Adjustment of the engine brake mechanism.",
        ],
    },

    1074: {
        "узел": "Output to the engine brake with an exhaust-pipe flap: the unit feeds air through an electro-pneumatic valve into the flap's cylinder, and the flap closes.",
        "нормы": [
            ("Pneumatic system pressure", "working"),
        ],
        "шаги": [
            "Switch the brake on with the test: the flap in the exhaust pipe moves.",
            "The rod of the pneumatic cylinder — seized from soot and salt, the flap does not move.",
            "The tube to the cylinder and the electro-pneumatic valve itself.",
            "FMI 3, 4, 5, 6: the valve connector.",
        ],
        "причины": [
            "Seized flap.",
            "Actuator tube or cylinder.",
            "Electro-pneumatic valve.",
        ],
    },

    1351: {
        "узел": "Compressor status: the unit controls the switching off of the compressor (clutch or idle valve) and monitors the build-up of pressure.",
        "нормы": [
            ("Regulator cut-out pressure", "usually about 8…12.5 bar — per the factory data"),
            ("Build-up from zero to working pressure", "usually a few minutes at idle — per the factory standards"),
        ],
        "шаги": [
            "Build-up time and cut-out pressure from the gauge on the dash.",
            "Slow build-up — leaks in the pneumatic system, compressor wear, a delivery pipe clogged with carbon.",
            "FMI 3, 4, 5, 6: the solenoid valve controlling the compressor or its clutch, and its connector.",
            "Air dryer: if it does not purge, the compressor works against the pressure.",
        ],
        "причины": [
            "Air leaks.",
            "Clogged delivery pipe.",
            "Compressor control valve.",
            "Compressor wear.",
        ],
    },

    1624: {
        "узел": "Tachograph speed: the tachograph calculates it from the sensor at the gearbox output and sends it over the bus. Wheel speed (SPN 84) is checked against it.",
        "нормы": [
            ("Sensor on the gearbox", "pulse type, supplied by the tachograph"),
        ],
        "шаги": [
            "Read the codes of the tachograph itself: the speed sensor on the gearbox and its cable.",
            "The connector of the gearbox sensor — low down, in dirt. The armoured cable to it breaks at the bends.",
            "FMI 2: the tachograph speed does not match the wheel speed — tachograph calibration (coefficient) or tyre size.",
            "FMI 9, 19: the link with the tachograph over the bus.",
            "Tampering with the tachograph sensor ('magnet', 'dummy') — this code is what gets recorded.",
        ],
        "причины": [
            "Speed sensor on the gearbox or its cable.",
            "Tachograph calibration.",
            "Link with the tachograph.",
            "Tampering with the sensor.",
        ],
    },

    1653: {
        "узел": "The speed limiter enable switch — the button with which the driver switches on a limiter that they set themselves, below the legal limit.",
        "нормы": [],
        "шаги": [
            "Check the switching in diagnostics.",
            "The switch connector.",
            "If there is no such button on the vehicle — the parameter is enabled by mistake.",
        ],
        "причины": [
            "Switch or connector.",
            "Parameter without a button.",
        ],
    },

    4047: {
        "узел": "The power take-off drive on the output shaft of the transfer case: the unit engages it with a valve and checks with a switch that it has engaged.",
        "нормы": [],
        "шаги": [
            "Engagement conditions: stationary, neutral, revs — each make is different.",
            "The position switch on the PTO box: the connector low down, in dirt.",
            "The electro-pneumatic engagement valve and the air to it.",
            "FMI 10 (did not engage in time): the engagement mechanism — teeth, fork.",
        ],
        "причины": [
            "Position switch.",
            "Engagement valve or air.",
            "Engagement mechanism.",
        ],
    },
}

CHECKS[789] = _wheel_front("left", "right")
CHECKS[790] = _wheel_front("right", "left")
CHECKS[791] = _wheel_second("left", "right")
CHECKS[792] = _wheel_second("right", "left")
CHECKS[793] = _wheel_third("left", "right")
CHECKS[794] = _wheel_third("right", "left")

CHECKS[795] = _valve("left wheel of the front axle")
CHECKS[796] = _valve("right wheel of the front axle")
CHECKS[797] = _valve("left wheel of the second (usually driven) axle")
CHECKS[798] = _valve("right wheel of the second (usually driven) axle")
CHECKS[799] = _valve("left wheel of the third axle")
CHECKS[800] = _valve("right wheel of the third axle")
