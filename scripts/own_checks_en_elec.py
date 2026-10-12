# -*- coding: utf-8 -*-
"""English twin of own_checks_elec.py (power, ignition, bus links, relays, lamps). Same fields and keys."""

CHECKS = {
    158: {
        "узел": "The voltage at the ignition lock input (terminal 15) of the ECU. From it the ECU knows the ignition is on. The code means the voltage on this wire is not the same as on the main power supply (SPN 168).",
        "нормы": [
            ("Ignition on, engine off", "as at the battery, about 24…25.5 V"),
            ("Difference from the ECU's main supply", "not more than 0.5 V"),
        ],
        "шаги": [
            "Measure at the ECU's terminal 15 input and at the battery at the same time, under load.",
            "There is a difference — the wire from the lock to the ECU: the lock itself, the terminal 15 relay, the fuse, connectors in the cab.",
            "The contacts of the ignition lock burn over time: when the key is wiggled, the voltage jumps.",
            "The code together with SPN 168 — a common cause: battery, grounds, alternator.",
        ],
        "причины": [
            "Ignition lock contacts.",
            "Terminal 15 relay or fuse.",
            "Connector in the cab.",
            "Common power fault — together with SPN 168.",
        ],
    },

    609: {
        "узел": "Controller No. 2 — an internal fault in the second unit in the system (on different makes this is a different unit: a second processor, a body unit, a gearbox unit). Check it the same way as controller No. 1 (SPN 629).",
        "нормы": [
            ("Supply at the unit connector under load", "as at the battery, sag not more than 0.5 V"),
        ],
        "шаги": [
            "Find out from the factory description which unit is this make's \"controller No. 2\".",
            "Its power, grounds and connectors.",
            "The link between the units — if the code comes with FMI 9 or 19, it is lost messages, not a breakdown.",
            "Update the software, then replace.",
        ],
        "причины": [
            "Power or ground of the unit.",
            "Link between the units.",
            "Faulty unit.",
        ],
    },

    624: {
        "узел": "The yellow warning lamp — the fault warning light. The code is about the lamp's own circuit: the unit cannot switch it on. On new vehicles the lamp is on the dash and the command comes over CAN.",
        "нормы": [],
        "шаги": [
            "When the ignition is switched on, does the lamp light for the check?",
            "Lamp on a wire: the dash connector, the wire, the lamp itself.",
            "Over CAN — the unit's link to the dash (SPN 639).",
            "While the lamp does not work, the driver will not know about other faults — read the codes with diagnostics.",
        ],
        "причины": [
            "Link to the dash.",
            "Lamp wire or connector.",
            "The dash itself.",
        ],
    },

    625: {
        "узел": "A proprietary link — the manufacturer's own bus between the units, besides the standard J1939. It is checked the same way as any CAN bus.",
        "нормы": [
            ("Resistance between CAN-H and CAN-L, power off", "about 60 Ω"),
            ("About 120 Ω", "one resistor or a section of the bus is open"),
            ("About 40 Ω or less", "an extra resistor or a short circuit"),
        ],
        "шаги": [
            "Find from the make's diagram which units are on this link.",
            "Read the codes of all the units: which one is silent.",
            "Resistance between the wires of the link with the power off.",
            "The connectors of the link's units, and taps of added equipment.",
        ],
        "причины": [
            "Connector or water in the connector of one of the units.",
            "Chafed link wire.",
            "Loss of power to one of the units.",
        ],
    },

    627: {
        "узел": "The unit's power supply — a general term for \"something is wrong with the power\": voltage out of range, dropping out, or the unit restarting. Check it the same way as the battery voltage (SPN 168), but on this unit.",
        "нормы": [
            ("Engine off", "25.2…25.6 V on the charged batteries"),
            ("Engine running", "27.5…28.8 V"),
            ("Sag at the unit connector under load", "not more than 0.5 V"),
        ],
        "шаги": [
            "Which unit gave the code — each has its own supply and its own fuse.",
            "Measure the supply and the ground right at the unit's connector, with a load switched on.",
            "Oxidised contacts of the fuse, and of the unit's power relay.",
            "A code on many units at once — battery, alternator, main ground.",
            "FMI 2 (jumps): a contact that is there sometimes and not at others — wiggle the harness and watch the voltage.",
        ],
        "причины": [
            "Unit ground.",
            "Fuse or power relay.",
            "Battery and alternator — if codes are on many units.",
            "Unit connector.",
        ],
    },

    628: {
        "узел": "The unit's program memory. The unit checks the checksum of its program at every switch-on; if it does not match — the code.",
        "нормы": [],
        "шаги": [
            "Disconnect the ground for a minute and reconnect it: the code may clear, if it came from a power failure during a write.",
            "If the unit was recently reprogrammed or \"chipped\" — restore the factory program.",
            "Check the unit's power and grounds: a sag during a write corrupts the memory.",
            "The code stays after reprogramming — the unit needs replacing or repair.",
        ],
        "причины": [
            "Interrupted program write.",
            "Program tampering.",
            "Power sags.",
            "Faulty unit.",
        ],
    },

    629: {
        "узел": "Controller No. 1 — the control unit itself reports its own internal fault. Before blaming the unit, rule out everything that makes it err: power, grounds, water.",
        "нормы": [
            ("Supply at the unit connector under load", "as at the battery, sag not more than 0.5 V"),
            ("Unit ground to the frame", "less than 1 Ω"),
        ],
        "шаги": [
            "Power and grounds at the unit's own connector, under load.",
            "The unit's connectors: water, green on the contacts. A unit on the frame or on the engine — check for moisture inside the housing.",
            "A recent welding job on the vehicle without disconnecting the unit — a frequent cause of internal faults.",
            "Update the unit's software if the manufacturer issued a fix.",
            "Only after everything else — replace the unit and reprogram it for the vehicle.",
        ],
        "причины": [
            "Power or ground of the unit.",
            "Water in the connector or housing.",
            "Welding without disconnecting the unit.",
            "Faulty unit.",
        ],
    },

    630: {
        "узел": "Calibration memory — the area of the unit where the vehicle settings are kept: engine parameters, gear ratios, tyre size, limits. The code means this data is corrupted or does not fit.",
        "нормы": [],
        "шаги": [
            "Was the unit recently replaced, reprogrammed, or had its parameters changed?",
            "Write the parameters again from the factory database by chassis number.",
            "Check the unit's power: a sag during the write corrupts the memory.",
            "The code stays after writing — the unit.",
        ],
        "причины": [
            "Parameters written incompletely or from another vehicle.",
            "Power failure during the write.",
            "Unit memory fault.",
        ],
    },

    645: {
        "узел": "The tachometer signal output: the engine unit sends speed pulses to the tachometer, the tachograph or a body unit. The code is about this circuit.",
        "нормы": [],
        "шаги": [
            "Which consumer on this vehicle takes the signal: the tachometer, the tachograph, or the body unit.",
            "The wire from the unit to the consumer: a short to ground or to plus.",
            "If added equipment is connected to the output (tracker, body speed sensor) — disconnect it and check.",
        ],
        "причины": [
            "Tap of added equipment.",
            "Wire.",
            "Signal consumer.",
        ],
    },

    677: {
        "узел": "The starter relay. The unit permits starting and switches on the relay, and the relay feeds the starter's pull-in solenoid. The code is about this circuit.",
        "нормы": [
            ("Battery voltage during cranking", "not below 18 V"),
            ("At the pull-in solenoid terminal during starting", "almost as at the battery"),
        ],
        "шаги": [
            "Is the relay click audible when the key is turned?",
            "Start-permission conditions: neutral in the gearbox, clutch pressed (SPN 598), parking brake — each make is different. The code may mean a condition is not met.",
            "Swap the relay in the relay block with an identical one.",
            "The wire from the relay to the starter's pull-in solenoid: under the cab and on the engine, in the dirt.",
            "FMI 7 (did not respond): the starter does not crank with the circuit intact — the starter itself, the power wires, the grounds.",
        ],
        "причины": [
            "Start condition not met.",
            "Starter relay.",
            "Wire to the pull-in solenoid.",
            "Starter or its power terminals.",
        ],
    },

    898: {
        "узел": "A request for engine speed or speed limiting over the bus: another unit (gearbox, retarder, body) asks the engine to hold or limit its speed. The code means the request arrived wrong or was lost.",
        "нормы": [],
        "шаги": [
            "FMI 9, 19: the message is lost — the bus link with the unit making the request.",
            "FMI 11, 12: the request is unreliable — read the codes of the unit sending it: the gearbox, the power take-off, the body unit.",
            "A body with speed control (crane, pump) — its parameters and connector.",
        ],
        "причины": [
            "Link with the unit sending the request.",
            "Fault in that unit.",
            "Body unit parameters.",
        ],
    },

    970: {
        "узел": "An additional engine stop switch: the 'stop' button at the engine, on the body, or outside the cab.",
        "нормы": [],
        "шаги": [
            "Find the button: at the engine, on the frame, on the body control panel.",
            "Check that it is not pressed and not stuck.",
            "The connector of the outside button — oxidation gives a false \"pressed\".",
            "On vehicles without such a button — a jumper in the connector in its place: is it in place?",
        ],
        "причины": [
            "Oxidised connector of the outside button.",
            "Stuck button.",
            "No jumper where there is no button.",
        ],
    },

    1108: {
        "узел": "Engine protection override: the driver pressed the button so that the engine does not stop on an alarm signal (overheating, oil pressure). The code is a record that the protection was overridden.",
        "нормы": [],
        "шаги": [
            "Ask the driver why it was pressed. An override is a sign that there was a real fault: check the oil pressure codes (SPN 100) and temperature (SPN 110).",
            "If the button was not pressed — the button is stuck or the wire is shorted.",
        ],
        "причины": [
            "Protection overridden for a real fault.",
            "Stuck button.",
        ],
    },

    1213: {
        "узел": "The malfunction indicator lamp (MIL) — lit for faults that affect emissions. The code is about the lamp's own circuit.",
        "нормы": [],
        "шаги": [
            "Does the lamp light for the check when the ignition is switched on?",
            "The lamp's wire and connector, or the link to the dash over CAN.",
            "A faulty lamp is also a violation: the vehicle will not pass the emissions check.",
        ],
        "причины": [
            "Link to the dash.",
            "Lamp wire.",
            "The dash itself.",
        ],
    },

    1231: {
        "узел": "The second J1939 bus. On many vehicles it carries a separate group of units: body, body unit, cab, trailer. The code means a unit cannot hear its neighbours on it.",
        "нормы": [
            ("Resistance between CAN-H and CAN-L, power off", "about 60 Ω"),
            ("About 120 Ω", "one resistor or a section of the bus is open"),
            ("About 40 Ω or less", "an extra resistor or a short circuit"),
        ],
        "шаги": [
            "Find from the diagram which units are on the second bus on this vehicle.",
            "Resistance between CAN-H and CAN-L of the second bus — separately from the first: each bus has its own two resistors.",
            "Disconnect the units of the second bus one at a time.",
            "Added equipment — body unit, crane, tracker — is often connected precisely to the second bus.",
        ],
        "причины": [
            "Body equipment on the bus.",
            "Connector or wire.",
            "Power to one of the units.",
        ],
    },

    1485: {
        "узел": "The main relay of the engine control unit. The unit switches the relay itself; through it the unit and some actuators are powered, and after the ignition is switched off the unit holds it on for a while to save data.",
        "нормы": [
            ("Relay output voltage, ignition on", "as at the battery"),
        ],
        "шаги": [
            "Find the relay from the diagram; listen for the click when the ignition is switched on.",
            "Swap the relay with an identical neighbouring one.",
            "The relay socket contacts: burnt, oxidised.",
            "The control wire of the relay from the unit.",
            "If the relay drops out straight after the ignition is switched off — the unit has no time to save data, and that is the source of the code.",
        ],
        "причины": [
            "The relay itself.",
            "The relay socket.",
            "Ground switch switched off right after the key.",
            "Control wire.",
        ],
    },
}
