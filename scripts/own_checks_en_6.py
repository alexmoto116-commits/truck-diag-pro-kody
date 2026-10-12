# -*- coding: utf-8 -*-
"""English twin of own_checks_6.py: the same codes, the same fields and the same keys.
Key = SPN. Numbers, units, FMI values and make names are the same as in the Russian data.
Where one number means different things to different makes, the record carries the
field 'по_маркам' (the same key as in the Russian file): a list of (make, node, steps).
"""

CHECKS = {
    523350: {
        "узел": "Power stage of the first injector group. It sits in the injector driver module and, on the ECU's command, feeds current to the group. The code points first at the circuit between the module and the first group, not at a single injector: one short on the group line stops the whole group.",
        "нормы": [
            ("Winding resistance of each injector in the group, connector unplugged", "per the manufacturer's manual"),
            ("Resistance of the harness from the module to the group connector, no load", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3, 4 (short to power or to ground): unplug the module connector and the first-group connector, inspect the harness for chafing at the ECU and in the engine bay.",
            "FMI 4 (minus wire shorted to ground): unplug the injectors of the group one at a time and watch whether the code clears. It clears with one unplugged: the short is in that injector or its harness.",
            "FMI 3 (short to power): with the ignition off, measure the resistance of each injector and compare with the factory value. If all are the same, look for insulation damage on the common line.",
            "FMI 11 (failure mode not determined): read the code with the module, clear it and check whether it comes back on a warm engine. YaMZ's factory table lists a short circuit of the first group as code 151.",
        ],
        "причины": [
            "Chafed harness between the module and the first-group injectors.",
            "Corroded contacts in the module or injector connector.",
            "Injector with a shorted winding.",
            "Faulty injector driver module.",
        ],
    },

    523351: {
        "узел": "The same first injector group, but this code reports an open circuit (FMI 12) and an undetermined fault (FMI 11). The makes agree on the component and differ on the consequence: at FMI 12 YaMZ and MAZ show the engine will not start, while KAMAZ shows only a warning. Check against the factory data.",
        "нормы": [
            ("Winding resistance of the first-group injector, connector unplugged", "per the manufacturer's manual"),
            ("Resistance of the circuit from the module to the group connector", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 12 (open circuit, faulty device): check the harness from the module to the first-group connector and each injector of the group by resistance. An open on the common line switches off every injector of the group at once.",
            "FMI 11 (failure mode not determined): see which code appears at cranking on a cold engine and on a warm one. If only cold, check the connector contacts and the ground.",
            "After repair, clear the code and start the engine. If it comes back at once, the circuit is not fixed; keep tracing the harness.",
        ],
        "причины": [
            "Open harness at the injector or on the route through the engine bay.",
            "Corroded or oil-filled injector connector.",
            "Injector with an open winding.",
        ],
    },

    523352: {
        "узел": "Second injector group: the same scheme as the first group, but on its own power channel in the module. The code means a short to power or to ground in the second group's circuit; a single injector does not produce it.",
        "нормы": [
            ("Winding resistance of the second-group injector, connector unplugged", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (short to power): check whether the group wire is tied to supply. Unplug the connector and see whether the code clears without the module connector.",
            "FMI 4 (to ground): measure resistance from the group wire to ground. A low reading means a short; trace the harness section by section.",
            "FMI 11: check whether the module calibration was disturbed after an injector was replaced. YaMZ's factory table lists this case as code 152, the second group.",
        ],
        "причины": [
            "Second-group wire shorted to ground or to supply.",
            "Punctured harness insulation in the engine bay.",
            "Injector replaced without calibration.",
            "Injector driver module with a faulty second-group channel.",
        ],
    },

    523218: {
        "узел": "A message with vehicle speed and cruise-control status. The engine ECU receives it over the CAN bus from another unit (usually the brake or instrument unit). The code means the message has stopped and the ECU does not see it when it should.",
        "нормы": [
            ("RxCCVS message on the bus with the engine running", "arrives without gaps; check with a bus monitor"),
            ("Resistance between CAN-H and CAN-L with power off", "about 60 ohms: two terminating resistors of 120 ohms each"),
        ],
        "шаги": [
            "FMI 12 (faulty device; per KAMAZ, YaMZ and MAZ — message timeout): first check that the sending unit is switched on and has power and ground at its connector.",
            "Check with a bus monitor whether RxCCVS arrives. If it does not at all, find the source. If it arrives with gaps, check the connectors and the harness shield along the route.",
            "Measure the resistance between CAN-H and CAN-L with the ignition off. About 120 ohms means one resistor is missing; about 60 ohms is normal; infinity means an open line.",
            "YaMZ's flash code for this fault is 4-4-5. If the code appears only on the move, check vibration and the cab connectors.",
        ],
        "причины": [
            "Sending unit switched off or without power.",
            "Open or corroded CAN line.",
            "Missing 120-ohm terminating resistor.",
            "Faulty sending unit.",
        ],
    },

    523222: {
        "узел": "A message from the tachograph with speed and operating mode, which the engine ECU receives over CAN. A timeout means the tachograph does not answer on the bus, or its message does not get through.",
        "нормы": [
            ("TCO1 message on the bus when driving", "arrives without gaps"),
            ("Tachograph power at the connector with the ignition on", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 12 (timeout per KAMAZ, YaMZ and MAZ): check whether the tachograph is fitted and switched on. A removed or unplugged tachograph gives the same code.",
            "Check power and ground at the tachograph connector, then the CAN line from the tachograph to the engine ECU.",
            "Watch TCO1 with a bus monitor while driving. No message means the tachograph or its wire; a message present means the engine ECU side.",
            "YaMZ's flash code is 4-4-6. If the tachograph itself is fine, check the connector at the ECU.",
        ],
        "причины": [
            "Tachograph without power or removed.",
            "Open or corroded CAN line to the tachograph.",
            "Faulty tachograph.",
        ],
    },

    523420: {
        "узел": "The ECU watchdog: a separate circuit that checks the processor is running and keeping time. If its count diverges, the ECU treats itself as unreliable. This code comes from supply dips more often than from a faulty watchdog.",
        "нормы": [
            ("ECU supply voltage at the connector during cranking", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): clear the code, start the engine and let it run 10–15 minutes. If the code does not come back, the fault was one-off, and you should look at the supply at that moment.",
            "Check the ECU power and ground at the connector: voltage dips during cranking upset the timer first.",
            "If the code returns, replace the ECU after diagnosis. Per YaMZ, with this code the ECU must shut down and the engine will not start (flash code 2-6-4).",
        ],
        "причины": [
            "Dips or interference on the ECU supply.",
            "Poor ECU ground.",
            "Internal ECU failure.",
        ],
    },

    523500: {
        "узел": "Messages that the engine ECU itself sends on the CAN bus. The code means the other units on the bus do not confirm receipt of its messages: the bus is overloaded, broken, or has no other units on it.",
        "нормы": [
            ("Resistance between CAN-H and CAN-L with power off", "about 60 ohms: two terminating resistors of 120 ohms each"),
            ("Number of units on the bus when running", "at least two, per the vehicle wiring diagram"),
        ],
        "шаги": [
            "FMI 12 (faulty device; per KAMAZ, YaMZ and MAZ — outgoing message timeout): check that there are other units on the bus and that they are switched on. A single unit on the bus almost always gives this code.",
            "Measure the bus resistance with the power off and compare with the norm. A missing 120-ohm resistor shows at once.",
            "Check the CAN contacts at the ECU connector. Corrosion causes a failure only on the move, so watch the code under vibration.",
            "YaMZ's flash code is 4-3-1. Do not replace the ECU until the bus and the resistors are checked.",
        ],
        "причины": [
            "Terminating resistor missing from the bus.",
            "Open or shorted CAN line.",
            "Another unit disconnected from the bus.",
            "Faulty CAN transceiver in the ECU itself.",
        ],
    },

    523550: {
        "узел": "The time processor: part of the ECU microcontroller that counts the timing for injection and ignition. The code means its count has diverged from the main processor timer. It most often follows supply dips rather than wear.",
        "нормы": [
            ("ECU supply voltage during cranking", "per the manufacturer's manual"),
            ("ECU supply with the engine running", "steady, with no dips on the scope"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): clear the code and do a start. If the fault came during a supply dip, find the dip at the terminals, grounds and relays.",
            "Check the ECU ground and the supply at the connector: unstable supply upsets the microcontroller timers first.",
            "If the code returns on a steady supply, replace the ECU. YaMZ's factory table lists this as code 115: time processor fault, replace the ECU.",
        ],
        "причины": [
            "Supply dips during cranking.",
            "Poor ECU grounds.",
            "Internal failure of the ECU microcontroller.",
        ],
    },

    523600: {
        "узел": "Internal link between the ECU's main processor and its watchdog block over an SPI bus. This is not a vehicle wire; it is the connection inside the control unit itself.",
        "нормы": [
            ("ECU supply voltage at the connector", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 12 (faulty device): check the ECU supply and grounds at the connector. The internal link suffers first from supply dips.",
            "Clear the code and do a test start. If it comes back, replace the ECU per the factory recommendation; YaMZ's flash code is 4-1-4.",
            "Before replacing, check whether other ECU codes appeared at the same moment. If they did, the cause is the supply, not the unit.",
        ],
        "причины": [
            "Internal ECU failure.",
            "Dips in the ECU supply.",
            "Poor ground of the control unit.",
        ],
    },

    523604: {
        "узел": "A message with exhaust gas temperature that the engine ECU receives over CAN from the aftertreatment unit or another module. The code is a timeout of this message on the bus.",
        "нормы": [
            ("RxEngTemp2 message on the bus with the engine running", "arrives without gaps"),
        ],
        "шаги": [
            "FMI 12 (faulty device; per KAMAZ, YaMZ and MAZ — timeout): check which unit sends RxEngTemp2 and whether it is switched on.",
            "Check the message with a bus monitor. If it is missing, check the CAN connectors on the route from the sending unit to the engine.",
            "YaMZ's flash code is 4-5-1, and its factory table lists this as code 451. Same case: the message does not arrive; it is not a temperature out of range.",
        ],
        "причины": [
            "Sending unit switched off or without power.",
            "Open CAN line.",
            "Faulty sending unit.",
        ],
    },

    523605: {
        "узел": "TSC1-AE message: a torque and speed control request that one unit sends to the engine over CAN. The code is a timeout of that request. Per YaMZ and MAZ, FMI 11 refers to the active message and FMI 12 to the inactive one.",
        "нормы": [
            ("TSC1-AE message on the bus while the sending unit works", "arrives at the required rate"),
            ("Resistance of the CAN line between units with power off", "about 60 ohms"),
        ],
        "шаги": [
            "FMI 11 (per the FMI table: failure mode not determined; per YaMZ and MAZ: active message timeout): check whether the sending unit transmits TSC1-AE when its function is on. If the function is off, the code may be false.",
            "FMI 12 (per the FMI table: faulty device; per the makes: inactive message timeout): the sending unit is switched off or not on the network. Check its power and connector.",
            "Check the CAN line by resistance and with a bus monitor. YaMZ's factory table lists TSC1-AE and TSC1-AR as one code, 421, flash code 4-2-1.",
        ],
        "причины": [
            "Sending unit does not transmit the message.",
            "Open or overloaded CAN line.",
            "Faulty sending unit.",
        ],
    },

    523607: {
        "узел": "TSC1-DE message on the CAN bus: the same class of engine control requests as TSC1-AE, but from a different source. The code is a timeout of this message, per KAMAZ, YaMZ and MAZ, with the active and inactive states treated separately.",
        "нормы": [
            ("TSC1-DE on the bus when the function is on", "per the vehicle diagram; the message does not drop out"),
        ],
        "шаги": [
            "FMI 11 (active message timeout): check whether the sending unit's function is on. Without it there is no message, and the code is false.",
            "FMI 12 (inactive message timeout): with a bus monitor, check whether TSC1-DE arrives even in standby. If not, check the source or its connector.",
            "YaMZ's factory table lists TSC1-DE and TSC1-DR as code 422, flash code 4-2-2.",
        ],
        "причины": [
            "Message source not switched on in the wiring.",
            "Open line on the way to the sending unit.",
            "Faulty sending unit.",
        ],
    },

    523612: {
        "узел": "Internal ECU supply that feeds the CJ940 module (injector power stages). The code is a voltage inside the unit above or below the norm. The vehicle supply may be fine, so check it first.",
        "нормы": [
            ("ECU supply voltage at the connector with the ignition on", "per the manufacturer's manual"),
            ("ECU supply voltage with the alternator running", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (voltage above the norm): check whether the vehicle voltage from the alternator or regulator is too high. If it is normal, the ECU is at fault.",
            "FMI 4 (voltage below the norm): check the battery terminals, grounds and the starter cable; look for a dip at cranking.",
            "YaMZ's flash code is 2-6-3, with the recommendation to replace the ECU. Replace only after the supply is checked; in the factory table this is code 263, the same CJ940 module.",
        ],
        "причины": [
            "Excess voltage from the alternator or regulator.",
            "Dips or corrosion at the battery and ground terminals.",
            "Faulty internal supply of the ECU.",
        ],
    },

    523617: {
        "узел": "Link between the ECU and the CJ940 module (injector power stages) over an internal SPI bus. The code is a link fault, not an injector supply fault: the module may be fine while the channel between it and the ECU is not.",
        "нормы": [
            ("ECU link with the CJ940 module at cranking", "no link errors in diagnostics"),
        ],
        "шаги": [
            "FMI 11 (failure mode not determined; per all three makes — link fault with the CJ940 module): check the module supply and grounds, then clear the code and see whether it returns.",
            "Look at the neighbouring CJ940 codes: voltage and power stages. If they are present too, the fault is in the module or the supply. If this is the only one, the link is on the ECU board.",
            "YaMZ's flash code is 2-6-3. Repair means replacing the ECU per the factory recommendation, but only after the module supply is checked.",
        ],
        "причины": [
            "Dip in the CJ940 module supply.",
            "Faulty CJ940 module.",
            "Internal ECU fault.",
        ],
    },

    523623: {
        "узел": "A DM1 message from the instrument unit (DCU): the fault list that the engine ECU receives over CAN. A timeout means the instrument unit does not answer on the bus.",
        "нормы": [
            ("DM1DCU message on the bus with the instrument unit working", "arrives regularly"),
        ],
        "шаги": [
            "FMI 3 (per the FMI table: voltage above the norm or short to power; per KAMAZ, YaMZ and MAZ: CAN message timeout): check the instrument unit first — supply, connector, bus operation.",
            "Check the CAN line on the way to the instrument unit, especially where it passes through the cab bulkhead.",
            "YaMZ's flash code is 4-6-6. The factory recommendation is to go to a service centre if the instrument unit is fine.",
        ],
        "причины": [
            "Instrument unit switched off or without power.",
            "Open CAN line in the cab.",
            "Faulty instrument unit.",
        ],
    },

    4034: {
        "узел": "The central brake unit (EBS) keeps its settings and program in EEPROM memory. The code says the write checksum does not match. The sensors and valves usually keep working.",
        "нормы": [
            ("EEPROM checksum after writing", "matches the reference from the manufacturer's program"),
            ("Unit supply voltage while settings are written", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 8 (per the FMI table: abnormal frequency or pulse duty; per MAN and Knorr-Bremse: wrong checksum signal): clear the code and switch the ignition off for half a minute. If it does not return, the fault came during writing.",
            "If the code returns, check whether the vehicle current dropped while the settings were written. Do not write settings on a weak battery.",
            "Write the configuration again with the diagnostic tool, then compare the checksum with the reference.",
            "If the checksum still does not match, replace the unit per the MAN or Knorr-Bremse recommendation.",
        ],
        "причины": [
            "Settings written on a weak supply.",
            "Incomplete write after replacing the unit.",
            "Wear of a memory cell in the unit.",
        ],
    },

    4035: {
        "узел": "The central EBS unit stores the ABS configuration: which axles and which sensors are fitted. The code means the unit does not recognise the stored configuration or check it against the equipment.",
        "нормы": [
            ("ABS configuration in the unit after writing", "matches the axle equipment"),
            ("Number of speed sensors in the configuration", "equal to the number of fitted wheels"),
        ],
        "шаги": [
            "FMI 3 (per the FMI table: voltage above the norm or short to power; per MAN and Knorr-Bremse: configuration not recognised): compare the configuration in the unit with the axle and sensor equipment.",
            "If there is a difference, write the configuration again with the diagnostic tool to match the equipment. If it matches, check the unit supply.",
            "Clear the code and check on the road. If it repeats, replace or reprogram the unit per the manufacturer's instructions.",
        ],
        "причины": [
            "Configuration not written after replacing the unit.",
            "Wrong sensor equipment on an axle.",
            "Faulty unit memory.",
        ],
    },

    4050: {
        "узел": "The brake system CAN: the line over which the EBS exchanges messages with the engine, instruments and trailer. The code applies to the whole bus, not to one sensor: if many units disappear at once, look for the line.",
        "нормы": [
            ("Resistance between the CAN lines with the ignition off", "about 60 ohms"),
            ("Units visible on the brake-system bus", "all those listed in the wiring diagram"),
        ],
        "шаги": [
            "FMI 4 (per the FMI table: low voltage or short to ground; per MAN and Knorr-Bremse: no signal): see which units have dropped off the bus. If all of them, it is the line; if one, its connector and wire.",
            "FMI 0 (per the FMI table: value above the norm; per MAN and Knorr-Bremse: undetermined fault): check the terminating resistors and the harness shield near the unit.",
            "Measure the resistance between the CAN lines and compare with the norm. A missing or extra resistor shows at once.",
        ],
        "причины": [
            "Open or chafed CAN line.",
            "Missing terminating resistor.",
            "Faulty CAN transmitter in one of the units on the bus.",
        ],
    },

    4052: {
        "узел": "The EBS unit compares the voltage on terminals 30 (permanent positive) and 15 (ignition switched). A difference between them is a sign of poor supply or ground at the unit, not of a sensor fault.",
        "нормы": [
            ("Voltage difference between terminals 30 and 15 with the engine running", "per the manufacturer's manual"),
            ("Voltage at terminal 30 with the engine off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (per the FMI table: voltage above the norm; per MAN: difference not recognised): measure the voltage at terminals 30 and 15 on the unit with the ignition on. A large difference means a drop in the wire or a poor contact.",
            "FMI 8 (per the FMI table: abnormal signal frequency; per MAN and Knorr-Bremse: wrong difference signal): check the unit ground and the supply fuses.",
            "Check whether the supply connector of the unit gets warm with the engine running. A warm connector means resistance in the contact.",
        ],
        "причины": [
            "Poor contact at terminal 30 or 15.",
            "Damaged unit ground.",
            "Burnt supply fuses.",
        ],
    },

    4054: {
        "узел": "After the ignition is switched off, the EBS unit keeps running for a while to save data and close the valves. The delayed switch-off circuit controls this mode. The code means the circuit is not working to its program.",
        "нормы": [
            ("Unit run time after the ignition is switched off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (per the FMI table: abnormal data update rate; per MAN and Knorr-Bremse: fault in the delay circuit): switch the ignition off, wait out the full delay, switch on and check the code.",
            "If the code repeats, check the relay that keeps the unit running after switch-off, and the unit supply.",
            "If the delay circuit does not work, replace the unit per the factory recommendation.",
        ],
        "причины": [
            "Stuck relay supplying the unit.",
            "Fault in the delay circuit of the unit.",
            "Broken unit ground.",
        ],
    },

    4059: {
        "узел": "Steering wheel angle sensor: it passes the steering angle to the EBS and ESP units. The code means a signal above the norm or an unreliable signal. MAN writes FMI 1 as \"too high a value\"; the FMI table gives FMI 1 as below the norm. The meanings differ, so read the value in diagnostics.",
        "нормы": [
            ("Signal of the steering angle in the straight-ahead position", "close to zero, per the manufacturer's manual"),
            ("Sensor supply at the connector", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1 (per the FMI table: data below the norm; per MAN: value too high; per Knorr-Bremse: above the norm): the meanings conflict. Read the angle value in diagnostics: with the wheel straight, a drift beyond the limit points to the sensor or its mount.",
            "FMI 3 (per the FMI table: voltage above the norm or short to power; per MAN: not recognised): unplug the sensor, inspect the contacts, measure the supply at the connector.",
            "If the signal jitters under vibration, move the harness with the engine running and watch the angle value.",
        ],
        "причины": [
            "Sensor connector: corrosion or loose contact.",
            "The steering angle sensor itself.",
            "Harness chafed at the steering column pivot.",
            "Sensor installed wrongly after column repair.",
        ],
    },

    4060: {
        "узел": "The steering angle sensor has not been configured in the unit. The unit does not know that such a sensor is fitted or where, and stability control relies on its signal.",
        "нормы": [
            ("Sensor configuration in the unit after writing", "matches the vehicle equipment"),
        ],
        "шаги": [
            "FMI 9 (per the FMI table: abnormal data update rate; per MAN and Knorr-Bremse: not configured or faulty device): check whether the sensor is fitted according to the vehicle equipment.",
            "Write the sensor configuration with the diagnostic tool and run the calibration per the manufacturer's instructions.",
            "If the code comes back after writing, check the sensor connector and the sensor itself.",
        ],
        "причины": [
            "Sensor replaced but not configured.",
            "Unit replaced without transferring the configuration.",
            "Faulty sensor.",
        ],
    },

    4061: {
        "узел": "ESP yaw-rate sensor: it gives the unit the rate of body rotation about the vertical axis. The code means the sensor is out of range or faulty; per the FMI table, FMI 0 is a value above the norm.",
        "нормы": [
            ("Sensor signal with the vehicle stationary", "close to zero, per the manufacturer's manual"),
            ("Sensor supply at the connector", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 0 (per the FMI table: value above the norm; per MAN and Knorr-Bremse: sensor faulty): check the value in diagnostics with the vehicle stationary. The signal should be close to zero.",
            "If the signal has drifted from zero, remove the sensor and check its mounting. A loose sensor gives a constant offset.",
            "Replace the sensor only after the supply and the connector are checked.",
        ],
        "причины": [
            "Loose sensor mounting.",
            "Faulty sensor.",
            "Dirty connector.",
        ],
    },

    4062: {
        "узел": "Speed sensor that gives the ESP and EBS units the vehicle speed. Its signal must match the other wheels and the instruments.",
        "нормы": [
            ("Speed signal on the road", "matches the speedometer in diagnostics"),
            ("Signal when stationary", "zero"),
        ],
        "шаги": [
            "FMI 0 (per the FMI table: above the norm; per MAN and Knorr-Bremse: undetermined fault): read the speed on the road in diagnostics and compare with the speedometer.",
            "FMI 1 (per the FMI table: below the norm; per MAN and Knorr-Bremse: above the norm): check which way the signal drifts. If it differs from the instruments, look at the sensor and its gap.",
            "Check the sensor gap and the condition of the trigger ring, then the connector.",
        ],
        "причины": [
            "Dirty sensor or trigger ring.",
            "Changed gap after hub repair.",
            "Faulty sensor.",
        ],
    },

    4063: {
        "узел": "Speed and yaw sensors connected to the ESP unit over CAN. The code applies to the CAN link with the sensor, not to the sensor itself.",
        "нормы": [
            ("Sensor message on the bus when driving", "arrives without gaps"),
        ],
        "шаги": [
            "FMI 4 (per the FMI table: low voltage or short to ground; per MAN and Knorr-Bremse: no signal over CAN): check whether the unit sees the sensor on the bus. If not, check the connector and the line from the sensor.",
            "FMI 10 (per the FMI table: abnormal rate of change; per MAN: open circuit of the yaw sensor over CAN): check the line to the yaw sensor separately from the speed sensor.",
            "Measure the CAN line resistance and check the terminating resistors on the bus.",
        ],
        "причины": [
            "Open CAN line to the sensor.",
            "Faulty sensor.",
            "Terminating resistor missing from the bus.",
        ],
    },

    4064: {
        "узел": "Yaw sensor: it measures the rotation of the body. The code means the sensor is installed wrongly: its axis, direction or mounting does not match what is written in the unit.",
        "нормы": [
            ("Sensor position in the configuration", "matches the installation per the manufacturer's instructions"),
        ],
        "шаги": [
            "FMI 0 (per the FMI table: above the norm; per MAN and Knorr-Bremse: installed wrongly): check the sensor orientation against the mark on the bracket and the instructions.",
            "If the sensor was moved, run the orientation calibration with the diagnostic tool.",
            "If the code repeats after calibration, the sensor is faulty.",
        ],
        "причины": [
            "Sensor moved wrongly after repair.",
            "Orientation knocked out on the bracket.",
            "Faulty sensor.",
        ],
    },

    4065: {
        "узел": "The speed sensor for ESP has not been configured in the unit. The unit does not know which sensor is fitted and at which wheel.",
        "нормы": [
            ("Number of speed sensors in the configuration", "equal to the number of fitted wheels"),
        ],
        "шаги": [
            "FMI 9 (per the FMI table: abnormal update rate; per MAN and Knorr-Bremse: not configured or faulty device): see which sensors are written in the unit and compare them with the equipment.",
            "Write the configuration per the manufacturer's instructions and check the sensor on the road.",
            "If the sensor does not match the catalogue, fit a suitable one.",
        ],
        "причины": [
            "Sensor replaced without writing the configuration.",
            "Unit replaced without transferring the configuration.",
            "Faulty sensor.",
        ],
    },

    4066: {
        "узел": "Speed sensor that the ESP unit calibrates on the road from long-term statistics: the difference between wheels and the tyre circumference. The code means the calibration has drifted out of range.",
        "нормы": [
            ("Speed difference between wheels on a straight road", "within the tolerance per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 0 (per the FMI table: above the norm; per MAN and Knorr-Bremse: long-term calibration error): check the tyre size and pressure. Tyres of different diameter pull the calibration off.",
            "Reset the calibration per the instructions and drive a straight, flat road until it finishes.",
            "If the drift repeats, check the sensor and the trigger ring.",
        ],
        "причины": [
            "Tyres of different size or wear.",
            "Wrong tyre pressure.",
            "Dirty sensor.",
        ],
    },

    4068: {
        "узел": "Steering angle sensor that the ESP unit calibrates from steering statistics. The code means the calibration has moved away from the real steering position.",
        "нормы": [
            ("Signal when driving straight on a flat road", "near the centre, per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 0 (per the FMI table: above the norm; per MAN and Knorr-Bremse: long-term calibration error): check whether the wheel sits at centre when driving straight. If not, the centre is out.",
            "Write the centre per the instructions and calibrate on a flat road.",
            "If the code returns, check the steering column play and the sensor connector.",
        ],
        "причины": [
            "Steering centre knocked out after repair.",
            "Play in the steering column.",
            "Faulty sensor.",
        ],
    },

    4069: {
        "узел": "The ESP unit compares the steering angle with the speed and yaw that should result from that turn. The code means the steering signal does not agree with the speed.",
        "нормы": [
            ("Steering angle and speed on a turn", "agree in diagnostics per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (per the FMI table: voltage above the norm or short to power; per MAN: signal does not match the base speed; per Knorr-Bremse: unreliable signal): first check the speed sensor that gives the base speed.",
            "If the speed is correct, check the steering sensor: unplug it, look at the contacts, measure the supply.",
            "Drive a turn on a flat area and watch the steering and speed signals together.",
        ],
        "причины": [
            "Fault in the speed sensor.",
            "Steering sensor with a poor contact.",
            "Knocked-out steering calibration.",
        ],
    },

    4070: {
        "узел": "Characteristic of the steering angle sensor: the link between angle and output voltage. The code means the characteristic is out of range. MAN writes FMI 1 as \"too high a value\", Knorr-Bremse as \"above the norm\"; the FMI table gives FMI 1 as below the norm.",
        "нормы": [
            ("Signal at the extreme steering positions", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1 (per the FMI table: data below the norm; per MAN and Knorr-Bremse: above the norm): the makes agree on one thing, a signal out of range. Check the signal at the extreme steering positions in diagnostics.",
            "If the signal does not reach the extremes or drifts, check the sensor and its mechanical fit on the column.",
            "Check the sensor supply and connector. If in doubt, replace the sensor.",
        ],
        "причины": [
            "Sensor shifted on the column.",
            "Corroded connector.",
            "Faulty sensor.",
        ],
    },

    4071: {
        "узел": "Steering angle sensor on the column. The code means the sensor is installed wrongly: the signal does not match the real steering position.",
        "нормы": [
            ("Sensor position in the configuration", "matches the manufacturer's instructions"),
        ],
        "шаги": [
            "FMI 0 (per the FMI table: above the norm; per MAN and Knorr-Bremse: installed wrongly): check the sensor position against the mark and the instructions. Moving it after column repair is a common cause.",
            "Register the neutral steering position with the diagnostic tool.",
            "If the code repeats, check the sensor or its cable.",
        ],
        "причины": [
            "Sensor moved when the column was repaired.",
            "Mount shifted.",
            "Faulty sensor.",
        ],
    },

    4072: {
        "узел": "Supply that the unit gives the ESP sensors: steering, speed and yaw. The code means the supply voltage is out of range. One sensor may be at fault, or the supply may be poor for all of them at once.",
        "нормы": [
            ("ESP sensor supply voltage at the connector", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1 (per the FMI table: below the norm; per MAN: too high a value; per Knorr-Bremse: above the norm): the meanings conflict. Measure the sensor supply at the unit connector with the ignition on and compare with the factory norm.",
            "FMI 2 (per the FMI table: data unreliable; per MAN and Knorr-Bremse: below the norm): check the ground and dips in the supply at cranking.",
            "FMI 3 (per the FMI table: voltage above the norm or short to power; per MAN: not recognised): check the sensor supply lines against the wiring diagram for a short to power.",
        ],
        "причины": [
            "Sensor supply line shorted to power.",
            "Poor ESP unit ground.",
            "Faulty unit that supplies the sensors.",
        ],
    },

    4073: {
        "узел": "Supply for the brake pedal module that the EBS unit gives the module. The code means the supply voltage is above or below the norm. Per the FMI table, FMI 1 is below the norm; MAN and Knorr-Bremse write it as above the norm.",
        "нормы": [
            ("Pedal module supply voltage at the connector", "per the manufacturer's manual"),
            ("Pedal signal when pressed", "changes smoothly from zero to full travel"),
        ],
        "шаги": [
            "FMI 1 (per the FMI table: below the norm; per MAN and Knorr-Bremse: above the norm): the meanings conflict. Measure the pedal module supply at the connector with the ignition on and compare with the norm.",
            "FMI 2 (per the FMI table: data unreliable; per MAN and Knorr-Bremse: below the norm): check the battery terminals and the unit ground.",
            "Check the pedal module with a normal supply: the signal should change smoothly as the pedal is pressed.",
        ],
        "причины": [
            "Sagging supply or poor contact.",
            "Faulty pedal module.",
            "Excess voltage from the alternator.",
        ],
    },

    4074: {
        "узел": "Pressure regulating module: the valves that build pressure in the brake chambers on the EBS command. The code means the module program is outdated or does not match the unit program.",
        "нормы": [
            ("Program version of the module and the EBS unit", "matches the manufacturer's version table"),
        ],
        "шаги": [
            "FMI 0 (per the FMI table: above the norm; per MAN and Knorr-Bremse: undetermined fault, outdated software): check the program version of the module and the EBS unit.",
            "Update the program as the manufacturer directs. The unit and the module versions must match.",
            "If the code returns after the update, replace the module or the unit.",
        ],
        "причины": [
            "Program not updated after repair.",
            "Module and unit with different versions.",
            "Faulty module memory.",
        ],
    },

    4075: {
        "узел": "Pressure regulating module working with the EBS unit. The code means the program is unstable: the module and the unit carry out different commands.",
        "нормы": [
            ("Operation of the module and the unit at start-up", "no link errors in diagnostics"),
        ],
        "шаги": [
            "FMI 0 (per the FMI table: above the norm; per MAN: unstable EBS program; per Knorr-Bremse: unstable software): clear the code, switch the ignition off and on.",
            "If the code returns, check the supply of the unit and the module at start-up. Dips upset the program.",
            "Do the program update only after the supply has been checked.",
        ],
        "причины": [
            "Supply dips.",
            "Program fault after reflashing.",
            "Faulty unit memory.",
        ],
    },

    4078: {
        "узел": "Trailer inlet valve, controlled by the trailer module. The code applies to the valve itself or its circuit.",
        "нормы": [
            ("Valve winding resistance, connector unplugged", "per the manufacturer's manual"),
            ("Voltage at the valve connector when energised", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 6 (per the FMI table: current above the norm or short to ground; per MAN: short to power; per Knorr-Bremse: short to supply): the meanings differ. Check the valve for a short to power and to ground separately.",
            "FMI 7 (per the FMI table: mechanical system not responding; per the makes: short circuit): check whether the valve responds to the command.",
            "FMI 9 (per the FMI table: abnormal update rate; per the makes: fault): replace the valve if its resistance is out of norm.",
            "FMI 10 (per the FMI table: abnormal rate of change; per the makes: open circuit): check the line from the module to the valve for continuity.",
        ],
        "причины": [
            "Open or chafed wire.",
            "Short to power or to ground.",
            "Valve stuck by contamination.",
            "Faulty valve.",
        ],
    },

    4080: {
        "узел": "Reserve trailer brake valve in the trailer module: if the main valve fails, it takes over control. The code applies to the valve or its circuit.",
        "нормы": [
            ("Winding resistance of the reserve valve", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 6 (per the FMI table: current above the norm; per MAN: short to power; per Knorr-Bremse: short to supply): the meanings differ. Check what the valve wire is shorted to.",
            "FMI 7 (per the FMI table: not responding; per the makes: short circuit): check the reserve valve's response to the module command.",
            "FMI 9 (per the FMI table: abnormal update rate; per the makes: valve fault): replace the valve if its resistance is out of norm.",
            "FMI 10 (per the FMI table: abnormal rate of change; per the makes: open circuit): check the wire to the valve for continuity first, then the valve itself.",
        ],
        "причины": [
            "Open wire to the valve.",
            "Valve shorted to power or to ground.",
            "Faulty reserve valve.",
        ],
    },
    4081: {
        "узел": "Pressure sensor that the trailer module supplies: the module gives it voltage and takes its signal. The code means the sensor supply is out of range. Per the FMI table FMI 1 is below the norm; MAN and Knorr-Bremse write it as above the norm.",
        "нормы": [
            ("Trailer pressure sensor supply at the connector", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1 (per the FMI table: below the norm; per MAN and Knorr-Bremse: above the norm): the meanings conflict. Measure the voltage at the sensor connector with the ignition on and compare with the norm.",
            "FMI 2 (per the FMI table: data unreliable; per MAN and Knorr-Bremse: below the norm): check the supply wire from the module to the sensor and its ground.",
        ],
        "причины": [
            "Open or chafed sensor supply wire.",
            "Supply line shorted to ground.",
            "Faulty pressure sensor.",
        ],
    },

    4084: {
        "узел": "Inlet and reserve valves of the trailer: the trailer module holds them in the required position. The code means the valves are stuck, so the trailer brake does not release or does not apply.",
        "нормы": [
            ("Valve operation on the module command", "audible and visible in diagnostics"),
        ],
        "шаги": [
            "FMI 7 (mechanical system not responding; per MAN: inlet and reserve valves shorted; per Knorr-Bremse: stuck, short circuit): check the valves for travel and for response to the command.",
            "If a valve does not move mechanically, it is contaminated or seized: remove it and clean it per the instructions.",
            "If it moves but the code stays, there is a short in the wire: trace it back to the module.",
        ],
        "причины": [
            "Contamination and seizing of the valve.",
            "Short in the valve wire.",
            "Faulty trailer module.",
        ],
    },

    4085: {
        "узел": "Dosing and reserve valves of the trailer. The trailer module drives them to meter the pressure in the trailer circuit. The code means the valves are stuck in the dosing mode.",
        "нормы": [
            ("Dosing valve operation on the module command", "pressure rises and falls smoothly"),
        ],
        "шаги": [
            "FMI 7 (mechanical system not responding; per MAN: outlet and reserve valves shorted; per Knorr-Bremse: dosing and reserve valves stuck): check the valve response to the dosing commands in diagnostics.",
            "If a valve is stuck mechanically, remove and clean it per the instructions. If it responds but the code stays, look for a short in the wire.",
        ],
        "причины": [
            "Dosing valve stuck.",
            "Short circuit in the valve wire.",
            "Faulty trailer module.",
        ],
    },

    4086: {
        "узел": "Speed sensor of wheel No. 7 by the unit's numbering. The unit takes the wheel speed from it for ABS and ESP. The code means there is no signal from the sensor or a short in its circuit.",
        "нормы": [
            ("Sensor signal on the road", "changes as the wheel speed rises"),
            ("Sensor gap to the trigger ring", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 4 (per the FMI table: low voltage or short to ground; per MAN and Knorr-Bremse: no signal): check the sensor connector and the wire to the unit.",
            "FMI 7 (per the FMI table: mechanical system not responding; per MAN and Knorr-Bremse: short circuit): measure the resistance of the sensor and the wire to ground.",
            "Check the gap and the trigger ring, then the sensor itself.",
        ],
        "причины": [
            "Broken sensor wire.",
            "Short to ground in the harness.",
            "Dirty sensor or ring.",
            "Faulty sensor.",
        ],
    },

    4087: {
        "узел": "Speed sensor of wheel No. 7 in the unit's configuration. The code means the sensor device is faulty: the sensor is fitted, but the unit does not accept it as working.",
        "нормы": [
            ("Sensor in the unit configuration", "fitted at wheel No. 7 per the diagram"),
        ],
        "шаги": [
            "FMI 9 (per the FMI table: abnormal data update rate; per MAN and Knorr-Bremse: device fault): check whether the sensor was replaced without writing the settings.",
            "Write the configuration as instructed and check the sensor on the road. If the code repeats, check the sensor or its connector.",
        ],
        "причины": [
            "Sensor replaced without writing settings.",
            "Faulty sensor.",
        ],
    },

    4088: {
        "узел": "Speed sensor of wheel No. 8 by the unit's numbering: the speed signal for ABS and ESP at that wheel. The code means no signal or a short in the circuit.",
        "нормы": [
            ("Sensor signal with the wheel turning", "present and rising with speed"),
        ],
        "шаги": [
            "FMI 4 (per the FMI table: low voltage; per MAN and Knorr-Bremse: no signal): check the sensor wire from the connector to the unit for an open.",
            "FMI 7 (per the FMI table: mechanical system not responding; per the makes: short circuit): measure the resistance of the sensor and the wire to ground.",
        ],
        "причины": [
            "Broken sensor wire.",
            "Wire shorted to ground.",
            "Faulty sensor.",
        ],
    },

    4089: {
        "узел": "Speed sensor of wheel No. 8 in the unit configuration. The code means the sensor device is faulty or not accepted by the unit as working.",
        "нормы": [
            ("Sensor in the unit configuration", "fitted at wheel No. 8 per the diagram"),
        ],
        "шаги": [
            "FMI 9 (per the FMI table: abnormal update rate; per MAN and Knorr-Bremse: device fault): see whether the sensor is written in the unit and compare with the equipment.",
            "Write the configuration and check the sensor on the road.",
        ],
        "причины": [
            "Sensor replaced without writing the configuration.",
            "Faulty sensor.",
        ],
    },

    4091: {
        "узел": "Brake pad wear sensor on wheel No. 7. It shows how much friction material is left. The code means the readings are above or below the norm.",
        "нормы": [
            ("Wear sensor reading with new pads", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1 (per the FMI table: below the norm; per MAN and Knorr-Bremse: above the norm): the meanings differ. Compare the reading with the actual pad wear on that wheel.",
            "FMI 2 (unstable data; per both makes: below the norm): check the sensor connector and the wire.",
            "If the pads are in norm, replace the sensor. If the pads are worn, replace the pads and the sensor separately.",
        ],
        "причины": [
            "Worn pads.",
            "Sensor with an open or poor contact.",
            "Faulty sensor.",
        ],
    },

    4092: {
        "узел": "Pad wear sensor on wheel No. 7 and its signal. The code is a large discrepancy: the unit gets data from the sensor that does not match the expected wear.",
        "нормы": [
            ("Discrepancy of the wear sensor signal", "small, within the manufacturer's tolerance"),
        ],
        "шаги": [
            "FMI 0 (per the FMI table: above the norm; per MAN and Knorr-Bremse: undetermined fault): compare the sensor signal with the pad wear on both wheels of the axle.",
            "A discrepancy only at wheel No. 7 means the sensor or its wire. A discrepancy across the whole axle means the unit that calculates the wear.",
        ],
        "причины": [
            "Wear sensor contaminated or open.",
            "Sensor configuration written wrongly.",
            "Fault in the signal-processing unit.",
        ],
    },

    4093: {
        "узел": "Pad wear sensor on wheel No. 8. The code means the sensor reading is above or below the norm: the unit records wear that does not match the expected value.",
        "нормы": [
            ("Wear sensor reading", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1 (per the FMI table: below the norm; per MAN and Knorr-Bremse: above the norm): the meanings differ. Compare the reading with the real pad wear at wheel No. 8.",
            "FMI 2 (per the FMI table: data unreliable; per the makes: below the norm): check the sensor connector and wire for an open and for ground.",
        ],
        "причины": [
            "Worn pads at wheel No. 8.",
            "Open sensor wire.",
            "Faulty sensor.",
        ],
    },

    4057: {
        "узел": "This number means different things to different makes: MAN and Knorr-Bremse describe the pressure regulating valve in the brake module, International describes the windscreen wiper motor. Each make is covered separately below.",
        "по_маркам": [
            ("MAN and Knorr-Bremse", "Pressure regulating valve in the brake module: on the unit's command it holds the pressure in the circuit. The code means the valve is shorted to ground or to power.", [
                "FMI 5 (current below the norm or open circuit): valve connector, winding resistance, and the wire for an open.",
                "FMI 6 (per the FMI table: current above the norm or short to ground; per MAN: short to power; per Knorr-Bremse: short to supply): check what the wire is shorted to.",
            ]),
            ("International", "Windscreen wiper motor. The code concerns the motor current, not the pressure valve.", [
                "FMI 5 (current below the norm): check the fuse and the wiper motor connector.",
                "FMI 6 (current above the norm): the mechanism is jammed. Remove the blades and check the arm movement.",
            ]),
        ],
    },

    4038: {
        "узел": "This number means different things to different makes: MAN and Knorr-Bremse describe the ASR configuration in the unit memory, International describes the snowplough front lighting relay. Each make is covered below.",
        "по_маркам": [
            ("MAN and Knorr-Bremse", "Central unit: ASR configuration in EEPROM. The code means an incorrect signal of the written settings.", [
                "FMI 8: write the ASR configuration again with the diagnostic tool and compare it with the axle equipment.",
            ]),
            ("International", "Snowplough front lighting relay 2, right headlamp circuit.", [
                "FMI 5 (current below the norm or open): check the fuse and the right headlamp bulb.",
                "FMI 6 (short to ground): check the wire to ground for continuity.",
            ]),
        ],
    },

    4039: {
        "узел": "This number means different things to different makes: MAN and Knorr-Bremse describe the ESP configuration in the unit memory, International describes the snowplough lighting relay, left headlamp circuit. Each make is covered below.",
        "по_маркам": [
            ("MAN and Knorr-Bremse", "Central unit: ESP configuration in EEPROM. The code means the value is not recognised.", [
                "FMI 3: check the ESP configuration against the equipment and write it again. If it is still not recognised after writing, the unit is at fault.",
            ]),
            ("International", "Snowplough front lighting relay 1, left headlamp circuit.", [
                "FMI 5: the circuit current is below the norm: check the bulb and the connector.",
                "FMI 6: short to ground: check the wire for continuity.",
            ]),
        ],
    },

    4055: {
        "узел": "This number means different things to different makes: MAN and Knorr-Bremse describe an incorrect ASR configuration, International describes the gearbox retarder switch. Each make is covered below.",
        "по_маркам": [
            ("MAN and Knorr-Bremse", "Anti-slip system ASR: the stored configuration does not match the fitted equipment.", [
                "FMI 8: check the ASR configuration against the fitted sensors and write it again.",
            ]),
            ("International", "Retarder switch on the gearbox lever.", [
                "FMI 2 (switch fault): check the switch and its connector. Do not confuse it with a brake sensor.",
            ]),
        ],
    },

    4058: {
        "узел": "This number means different things to different makes: MAN and Knorr-Bremse describe the steering angle sensor on the CAN bus, International describes the cab lamp switch. Each make is covered below.",
        "по_маркам": [
            ("MAN and Knorr-Bremse", "Steering angle sensor, CAN link. The code means no signal or an incorrect signal.", [
                "FMI 4 (no signal): check the sensor connector and the CAN line to the unit.",
                "FMI 8 (incorrect signal): the sensor or the bus; compare with the other messages on the bus.",
            ]),
            ("International", "Cab lamp switch 1.", [
                "FMI 2: check the cab lamp switch and its connector. It has nothing to do with the steering.",
            ]),
        ],
    },

    4023: {
        "узел": "This number means different things to different makes: Renault describes missing messages from the ABS/EBS unit, International describes the tail-lift power switch. Each make is covered below.",
        "по_маркам": [
            ("Renault", "No messages from the ABS/EBS unit. The code means the unit does not answer on the bus.", [
                "FMI 4: check the supply and ground of the ABS/EBS unit, then the CAN line between it and the instruments.",
            ]),
            ("International", "Tail-lift power switch.", [
                "FMI 2 (switch fault): check the switch and its contacts.",
            ]),
        ],
    },

    4024: {
        "узел": "This number means different things to different makes: Renault describes buffer memory overflow, International describes the clearance light cut-off switch. Each make is covered below.",
        "по_маркам": [
            ("Renault", "The unit's buffer memory is full.", [
                "FMI 0: switch the ignition off, switch it on again and repeat the test. If the overflow comes back, the unit is at fault.",
            ]),
            ("International", "Clearance light cut-off switch.", [
                "FMI 2 (switch fault): check the switch and its connector; replace the switch if it has failed.",
            ]),
        ],
    },

    4026: {
        "узел": "This number means different things to different makes: Renault describes missing messages from the ABS/EBS unit, International describes the right mirror heater. Each make is covered below.",
        "по_маркам": [
            ("Renault", "No messages from the ABS/EBS unit.", [
                "FMI 4: the same CAN line from the ABS/EBS unit. Check the unit and the line.",
            ]),
            ("International", "Mirror heater 2, right mirror circuit.", [
                "FMI 5 (current below the norm): an open heater element or connector.",
                "FMI 6 (current above the norm): short to ground; check the wire for continuity.",
            ]),
        ],
    },

    4028: {
        "узел": "This number means different things to different makes: Renault describes missing messages from the EECU, International describes the first-circuit air tank drain valve. Each make is covered below.",
        "по_маркам": [
            ("Renault", "No messages from the EECU (engine unit).", [
                "FMI 4: check the EECU supply and ground, and the engine CAN line.",
            ]),
            ("International", "Air tank drain valve, circuit 1, solenoid.", [
                "FMI 5 (current below the norm or open): check the coil and its connector.",
                "FMI 6 (short to ground): check the solenoid wire for continuity.",
            ]),
        ],
    },

    4029: {
        "узел": "This number means different things to different makes: Renault describes missing messages from the tachograph, International describes the air tank drain valve switch. Each make is covered below.",
        "по_маркам": [
            ("Renault", "No messages from the tachograph unit.", [
                "FMI 4: check the tachograph supply and its connector, then the CAN line to the unit.",
            ]),
            ("International", "Air tank drain valve switch, circuit 1.", [
                "FMI 2 (switch fault): check the switch and its contacts.",
            ]),
        ],
    },

    4008: {
        "узел": "This number means different things to different makes: Renault describes the handle supply, International describes a fog lamp. Each make is covered below.",
        "по_маркам": [
            ("Renault", "Handle supply: short to ground or to power.", [
                "FMI 5 (short to ground): check the handle connector and the wires to ground.",
                "FMI 6 (short): check the handle supply and the cable connections.",
            ]),
            ("International", "Fog lamp 2, right lamp circuit.", [
                "FMI 5 (current below the norm): bulb or open circuit.",
                "FMI 6 (current above the norm): short to ground.",
            ]),
        ],
    },

    4010: {
        "узел": "This number means different things to different makes: Renault describes a proportional solenoid valve, International describes the relay of the fuel tank transfer pump. Each make is covered below.",
        "по_маркам": [
            ("Renault", "Proportional solenoid valve.", [
                "FMI 5 (short to ground): check the valve and the wire for continuity.",
                "FMI 6 (short): check the valve and the harness.",
            ]),
            ("International", "Fuel tank transfer pump relay.", [
                "FMI 5 (relay current below the norm): check the relay and the fuse.",
                "FMI 6 (relay shorted to ground): check the relay wire for continuity.",
            ]),
        ],
    },

    4014: {
        "узел": "This number means different things to different makes: Renault describes a proportional solenoid valve, International describes a heavy-current load switch. Each make is covered below.",
        "по_маркам": [
            ("Renault", "Proportional solenoid valve: current too high or too low.", [
                "FMI 1 (current too high): check the valve and its resistance.",
                "FMI 2 (current too low): check the valve contact and its supply.",
            ]),
            ("International", "Heavy-current load switch 1.", [
                "FMI 2 (switch fault): check the switch.",
            ]),
        ],
    },

    4016: {
        "узел": "This number means different things to different makes: Renault describes the handle position, International describes a heavy-current supply relay. Each make is covered below.",
        "по_маркам": [
            ("Renault", "Handle position mismatch.", [
                "FMI 3: run the handle test in diagnostics. If the mismatch repeats, replace the handle.",
            ]),
            ("International", "Heavy-current supply relay 1, load current.", [
                "FMI 5 (load current below the norm or open): an open relay or its circuit.",
                "FMI 6 (load current above the norm): short to ground; check for continuity.",
            ]),
        ],
    },

    4022: {
        "узел": "This number means different things to different makes: Renault describes an internal unit fault, International describes the lift-board supply enable. Each make is covered below.",
        "по_маркам": [
            ("Renault", "Internal unit fault.", [
                "FMI 0: switch the ignition off, switch it on again and repeat the test. If it repeats, replace the unit.",
            ]),
            ("International", "Lift-board supply enable, circuit current.", [
                "FMI 5 (current below the norm): check the circuit and its fuse.",
                "FMI 6 (current above the norm): short; check for continuity.",
            ]),
        ],
    },

    4076: {
        "узел": "This number means different things to different makes: MAN and Knorr-Bremse describe the checksum of the external memory of the pressure regulating module, Sitrak describes the coolant temperature at the outlet. Each make is covered below.",
        "по_маркам": [
            ("MAN and Knorr-Bremse", "Pressure regulating module: external memory checksum error.", [
                "FMI 0: rewrite the module program. If the error repeats, replace the module.",
            ]),
            ("Sitrak", "Coolant temperature at the outlet above the thresholds. Scanner code P0115.", [
                "FMI 22, 23, 24 (above thresholds 1–3): compare the temperature with the instruments. If the engine overheats, look for the cause in the cooling system.",
            ]),
        ],
    },

    4032: {
        "узел": "This number means different things to different makes: MAN and Knorr-Bremse describe the central unit memory checksum, International describes the supply reservoir drain valve switch. Each make is covered below.",
        "по_маркам": [
            ("MAN and Knorr-Bremse", "Central unit: EEPROM memory checksum.", [
                "FMI 8: switch the ignition off and on. If it repeats, rewrite the unit memory or replace the unit.",
            ]),
            ("International", "Supply reservoir drain valve switch.", [
                "FMI 2 (switch fault): check the drain valve switch and its connector.",
            ]),
        ],
    },

    4036: {
        "узел": "This number means different things to different makes: MAN and Knorr-Bremse describe the ABS configuration in the unit memory, Renault describes missing messages from the VECU. Each make is covered below.",
        "по_маркам": [
            ("MAN and Knorr-Bremse", "Central unit: ABS configuration in EEPROM.", [
                "FMI 8: write the ABS configuration again and compare it with the axle equipment.",
            ]),
            ("Renault", "No messages from the VECU.", [
                "FMI 4: check the VECU, its supply and the CAN line. Messages are missing, so this is not ABS memory.",
            ]),
        ],
    },

    4037: {
        "узел": "This number means different things to different makes: MAN and Knorr-Bremse describe the ASR configuration in the unit memory, Renault describes missing messages from the VECU. Each make is covered below.",
        "по_маркам": [
            ("MAN and Knorr-Bremse", "Central unit: ASR configuration in EEPROM.", [
                "FMI 3: check the ASR configuration against the equipment and write it again.",
            ]),
            ("Renault", "No messages from the VECU.", [
                "FMI 4: check the VECU and its CAN line.",
            ]),
        ],
    },

    4040: {
        "узел": "This number means different things to different makes: MAN and Knorr-Bremse describe the ESP configuration in the unit memory, International describes the snowplough lighting mode switch. Each make is covered below.",
        "по_маркам": [
            ("MAN and Knorr-Bremse", "Central unit: ESP configuration in EEPROM, incorrect signal.", [
                "FMI 8: write the ESP configuration again and check it against the equipment.",
            ]),
            ("International", "Snowplough lighting mode switch.", [
                "FMI 2 (switch fault): check the lighting mode switch and its connector.",
            ]),
        ],
    },

    4042: {
        "узел": "This number means different things to different makes: MAN and Knorr-Bremse describe the unit's own ESP configuration, International describes the trailer auxiliary power switch. Each make is covered below.",
        "по_маркам": [
            ("MAN and Knorr-Bremse", "Central unit: own ESP configuration in EEPROM.", [
                "FMI 8: check the unit's own ESP configuration and write it if it does not match the equipment.",
            ]),
            ("International", "Trailer auxiliary power switch.", [
                "FMI 2 (switch fault): check the switch and its connector.",
            ]),
        ],
    },

    4048: {
        "узел": "This number means different things to different makes: MAN and Knorr-Bremse describe the EBS data in the central unit memory, International describes the transfer case range switch. Each make is covered below.",
        "по_маркам": [
            ("MAN and Knorr-Bremse", "Central unit: EBS data in EEPROM. The code means the stored data signal is incorrect.", [
                "FMI 8: write the EBS data again with the diagnostic tool, then check the code on the road.",
            ]),
            ("International", "Transfer case range switch.", [
                "FMI 2 (switch fault): check the range switch and its connector.",
            ]),
        ],
    },
}
