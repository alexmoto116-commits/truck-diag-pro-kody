# -*- coding: utf-8 -*-
"""English twin of own_checks_fuel.py (fuel, injectors, glow and intake heaters,
sensor supply lines). Same fields and keys.

The per-cylinder and per-line records share one wording, so they are built from
a template with the cylinder/line numbers filled in; the wording is the same as
in the Russian file.
"""

# цилиндр: (положение от вентилятора, порядок зажигания, «после и перед», соседний цилиндр, группа проводов)
_INJ = {
    1: ("the first from the fan, at the front of the head", "1st", "after 4 and before 5", 2, "1–3", 1323),
    2: ("the second from the fan", "5th", "after 6 and before 4", 3, "1–3", 1324),
    3: ("the third from the fan, nearer the middle of the head", "3rd", "after 5 and before 6", 2, "1–3", 1325),
    4: ("the fourth from the fan, in the middle of the head nearer the cab", "6th", "after 2 and before 1", 5, "4–6", 1326),
    5: ("the fifth, nearer the flywheel", "2nd", "after 1 and before 3", 4, "4–6", 1327),
    6: ("the last, at the flywheel and the rear of the head", "4th", "after 3 and before 2", 5, "4–6", 1328),
}

# цилиндр в записи SPN 1323–1328 (то же положение, что у форсунки)
_CYL = {
    1: "cylinder 1 (the first from the fan, at the front of the head)",
    2: "cylinder 2 (the second from the fan)",
    3: "cylinder 3 (the third from the fan, nearer the middle of the head)",
    4: "cylinder 4 (the fourth from the fan, in the middle of the head nearer the cab)",
    5: "cylinder 5 (the fifth, nearer the flywheel)",
    6: "cylinder 6 (the last, at the flywheel and the rear of the head)",
}

_SOLENOID = ("Solenoid injector: winding resistance",
             "usually a fraction of an ohm, about 0.2…0.6 Ω — per the factory data")
_PIEZO = ("Piezo injector", "hundreds of kΩ — do not compare with a solenoid one")
_WIRE = ("Wire resistance to the body", "infinity")


def _injector(n):
    pos, ordn, ba, swap, grp, _spn = _INJ[n]
    return {
        "узел": ("The electrical circuit of injector %d — %s. On an in-line six it fires %s in the "
                 "1-5-3-6-2-4 order: %s. The injector wires run under the valve cover." % (n, pos, ordn, ba)),
        "нормы": [_SOLENOID, _PIEZO, _WIRE],
        "шаги": [
            "Check whether there are codes for other injectors. If several cylinders of the %s group "
            "show at once — on many ECUs they share a supply wire: look there and at the connector on "
            "the head, not in the injector." % grp,
            "FMI 3, 4, 5, 6 (open or short): unplug the harness connector on the head, measure the "
            "winding of injector %d and compare it with the neighbouring injector %d. Measure twice — "
            "at the head connector and directly at the injector: the difference is the wire under the cover." % (n, swap),
            "The wire under the valve cover: oil and heat make the insulation brittle, and it chafes "
            "against the rocker. The nuts on the injector terminals — tighten by hand; over-tightened "
            "ones snap the stud.",
            "FMI 7, 11, 12, 14 (injector not responding): swap injector %d into cylinder %d. If the code "
            "moves with the injector — the injector; if it stays — the wire or the ECU." % (n, swap),
            "Also check the misfires in this cylinder — SPN %d." % _INJ[n][5],
        ],
        "причины": [
            "Wire under the valve cover: chafed, dried out, burnt terminal.",
            "Harness connector on the head — oil inside the connector.",
            "Injector winding.",
            "Shared supply wire of the %s group — if the code is not the only one." % grp,
            "ECU output — only after everything else has been checked.",
        ],
    }


def _misfire(n):
    pos, _ordn, _ba, swap, grp, _spn = _INJ[n]
    return {
        "узел": ("The ECU sees from the uneven rotation of the crankshaft that %s is not doing its "
                 "share. The code is not about the wire but about combustion: fuel, compression, air." % _CYL[n]),
        "нормы": [
            ("Diesel compression in a healthy cylinder", "usually 25…35 bar — per the factory data"),
            ("Compression difference between cylinders", "usually not more than 10%"),
        ],
        "шаги": [
            "Check the codes of this cylinder's injector — SPN %d. If present — start with the injector's "
            "electrical circuit." % (650 + n),
            "Cylinder balance test or injector balance in diagnostics: cylinder %d adds less than the others." % n,
            "Compare the leak-off from injector %d on the return with its neighbours: a large leak-off "
            "means the injector is worn." % n,
            "Swap injector %d into cylinder %d: if the misfire moves with it — the injector." % (n, swap),
            "Not the injector — measure the compression in cylinder %d and the valve clearances of that "
            "cylinder. A burnt valve or piston gives misfire and smoke." % n,
        ],
        "причины": [
            "Injector of cylinder %d: wear, coked nozzle." % n,
            "Electrical circuit of the injector.",
            "Valve clearance, burnt valve.",
            "Low compression: rings, piston.",
            "Sealing washer under the injector passes gas.",
        ],
    }


def _line(n):
    return {
        "узел": ("Sensor supply line No. %d — stabilised 5 V that the ECU supplies to a group of sensors. "
                 "If the line sags, all sensors on it drop at once, and there are often many codes." % n),
        "нормы": [
            ("Line voltage at the connector of any sensor on it", "5.0 V ± 0.25"),
            ("Line resistance to ground with ignition off", "not zero — units of kΩ or more"),
        ],
        "шаги": [
            "Write down all the codes: which sensors dropped together with line No. %d. They are its group — "
            "exactly which depends on the make and the engine." % n,
            "FMI 4, 6 (short, voltage low): unplug the sensors of the group one at a time with the ignition "
            "on. When the voltage returns to 5 V after a sensor — that sensor or its wire is shorting the line.",
            "FMI 3 (voltage high): the 5 V wire touches the vehicle's battery plus — look for a chafed "
            "harness where the sensor wires run alongside the power cables.",
            "All sensors unplugged and the line still faulty — the wire from the ECU to the first junction, "
            "or the ECU itself.",
        ],
        "причины": [
            "Shorted sensor on the line — most often the one in water or oil.",
            "Chafed harness.",
            "Water in the connector.",
            "The ECU — rarely.",
        ],
    }


CHECKS = {}
for _n in range(1, 7):
    CHECKS[650 + _n] = _injector(_n)
CHECKS.update({
    676: {
        "узел": "The glow plug relay switches on the glow plugs in the cylinders before starting. On trucks it is less common than the intake air heater — more often on light and medium engines.",
        "нормы": [
            ("Working glow plug resistance", "a fraction of an ohm — about 0.5…1.5 Ω"),
        ],
        "шаги": [
            "Does the relay click when the ignition is switched on with a cold engine?",
            "Disconnect the wires from the glow plugs and check each one for continuity: an open circuit means the plug has burnt out.",
            "The relay's power contacts and the common glow plug busbar.",
            "If the relay has a control unit — it has its own diagnostics: read its codes.",
        ],
        "причины": [
            "Burnt-out glow plug.",
            "Burnt relay contacts.",
            "Oxidised glow plug busbar.",
        ],
    },

    729: {
        "узел": "The output to the intake air heater — a powerful heating element in the manifold, switched on through a relay before starting in frost. This code is about the relay control circuit or the heater itself.",
        "нормы": [
            ("Heater current", "hundreds of amps — hence the relay"),
            ("Heater resistance", "a fraction of an ohm — measure with it disconnected"),
        ],
        "шаги": [
            "Switch the ignition on with a cold engine: the heater relay clicks, and the 'wait to start' lamp on the dash lights (SPN 1081).",
            "The relay does not click — the control wire from the ECU, the relay winding.",
            "The relay clicks but the heater stays cold — the relay's power contacts, the thick wire to the heater, the heater itself (broken element).",
            "Power terminals on the heater: oxidation heats the terminal and melts the insulation.",
        ],
        "причины": [
            "Burnt contacts of the heater relay.",
            "Oxidised power terminals.",
            "Burnt-out heater.",
            "Relay winding or control wire.",
        ],
    },

    730: {
        "узел": "The second output to the air heater. On engines with two heaters or two heating stages, each is switched by its own relay: the first — SPN 729, the second — this one. The second stage often switches on later, or only in hard frost, so its fault is not noticed straight away.",
        "нормы": [
            ("Heater current", "hundreds of amps — hence the relay"),
            ("Heater resistance", "a fraction of an ohm — measure with it disconnected"),
        ],
        "шаги": [
            "Swap the relays of the first and second stages. If the code moves to SPN 729 — the relay is at fault; if it stays — the wire or the second-stage heater.",
            "The second heater is cold after preheating while the first is warm — the power wire or the coil of the second.",
            "Check the relay winding and the control wire from the ECU separately from the first stage: they have different contacts on the ECU connector.",
            "Power terminals on the heater — oxidation heats the terminal and melts the insulation.",
        ],
        "причины": [
            "Second-stage relay.",
            "Power wire or terminal of the second heater.",
            "Burnt-out coil.",
        ],
    },

    1079: {
        "узел": "The sensor supply voltage — 5 V that the ECU supplies to the pressure and position sensors. SPN 1079 is the old designation of the first line; on newer units the same thing is written as SPN 3509. If the line sags, all its sensors drop at once.",
        "нормы": [
            ("Line voltage at the connector of any sensor on it", "5.0 V ± 0.25"),
            ("Line resistance to ground with ignition off", "not zero — units of kΩ or more"),
        ],
        "шаги": [
            "Check whether SPN 3509 is also in memory: on some units both numbers are written for one line — that is one fault, not two.",
            "Write down which sensors dropped together with the supply: usually the pressure sensors (boost, rail, oil) and the position sensors (pedal, valves).",
            "FMI 4 (voltage low): with the ignition on, unplug these sensors one at a time, starting with those low on the engine and in the oil. When 5 V comes back — found it.",
            "FMI 3 (high): the 5 V wire touches plus — look for a chafed harness at the power cables.",
        ],
        "причины": [
            "A shorted sensor on the line — most often the one in water or oil.",
            "Chafed harness.",
            "Water in the connector.",
            "The ECU — rarely.",
        ],
    },

    1081: {
        "узел": "The 'wait to start' lamp on the dash — lit while the heating runs. This code is about the lamp circuit, not the heating. On new vehicles the lamp is on the dash and the command comes over CAN.",
        "нормы": [],
        "шаги": [
            "Switch the ignition on: does the symbol light on the dash during the lamp check?",
            "If the lamp is on a wire — the dash connector and the lamp itself; if it is over CAN — the link to the dash (SPN 639).",
            "While the lamp is not working, wait before starting in frost for a set time: a few seconds after the relay clicks.",
        ],
        "причины": [
            "No link to the dash.",
            "The lamp or its wire.",
        ],
    },

    1322: {
        "узел": "Misfire in several cylinders at once. When not one cylinder but many run poorly, the cause is usually common to all of them: fuel, air, or the shared injector wiring.",
        "нормы": [
            ("Rail pressure at idle", "per the factory data; see SPN 157"),
        ],
        "шаги": [
            "Check which cylinders: if all are from one group (1–3 or 4–6) — the shared injector supply wire of that group.",
            "Fuel: filters, air leak, water in the fuel (SPN 97), rail pressure.",
            "Air: clogged air filter, boost leak (SPN 102).",
            "In winter with a cold engine — the intake air heater (SPN 729, 730) and fuel quality.",
            "If nothing is common — go through the cylinders one at a time.",
        ],
        "причины": [
            "Fuel: filters, air, water, wax.",
            "Shared injector group wire.",
            "Cold start without heating.",
            "Air path.",
        ],
    },

    1347: {
        "узел": "The pump unit — the fuel metering valve on the Common Rail high-pressure pump. The ECU uses it to decide how much fuel the pump delivers to the rail. This code is about this valve's circuit, or about pressure it cannot hold.",
        "нормы": [
            ("Metering valve winding resistance", "usually a few ohms — per the factory data"),
            ("Rail pressure", "see SPN 157"),
        ],
        "шаги": [
            "FMI 3, 4: unplug the connector on the pump, inspect it, and measure the valve winding.",
            "FMI 0, 7 (pressure will not hold): fuel first — filters, transfer pump, air. The metering valve sticks from dirt and water in the fuel.",
            "Check the leak-off from the injectors and the rail's relief valve — they draw the pressure down, and the ECU blames the pump.",
            "On many systems the valve is replaced separately from the pump — do not rush to replace the pump.",
        ],
        "причины": [
            "Dirt or water in the fuel — the metering valve sticks.",
            "Connector on the pump.",
            "Pressure leak through the injectors or the relief valve.",
            "Worn high-pressure pump.",
        ],
    },

    3050: {
        "узел": "Catalyst self-check: the ECU compares the sensors before and after the catalyst (temperatures, NOx) and decides whether it is working. The code means the exhaust cleaning is below the threshold.",
        "нормы": [],
        "шаги": [
            "Check the related codes: NOx sensors, exhaust temperature, AdBlue. The catalyst code is often the consequence of a faulty sensor.",
            "AdBlue quality: diluted or old solution gives the same code.",
            "Look at the catalyst: dents, signs of overheating, exhaust leaks before the sensors — a leak spoils the readings.",
            "Oil and coolant in the exhaust (turbo, EGR cooler) poison the catalyst.",
        ],
        "причины": [
            "NOx or exhaust temperature sensor.",
            "Poor AdBlue.",
            "Exhaust leak before the sensors.",
            "Oil-poisoned or worn catalyst.",
        ],
    },
})
for _n in range(1, 7):
    CHECKS[1322 + _n] = _misfire(_n)
for _n in range(1, 5):
    CHECKS[3508 + _n] = _line(_n)
