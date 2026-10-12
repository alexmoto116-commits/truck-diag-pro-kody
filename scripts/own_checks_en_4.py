# -*- coding: utf-8 -*-
"""English twin of own_checks_4.py: 100 more codes, the same fields and the same keys.
Key = SPN. Numbers, units, FMI values and make names are the same as in the Russian data.
"""

CHECKS = {
    626: {
        "узел": "Engine start enable relay 1. The ECU switches it on before starting. In International data this code is about the fuel heater relay, so we check the current of that relay.",
        "нормы": [
            ("Relay current with the fuel heater on", "per the manufacturer's manual"),
            ("Relay coil resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the fuse and the relay itself in the fuse box. Then check continuity of the wire from the relay to the fuel heater with ignition off.",
            "FMI 6 (current above normal or grounded circuit): disconnect the fuel heater from the relay. Code gone: the heater or its harness is grounded; code still there: the relay circuit is grounded.",
            "Swap the relay with an identical one in the box. If the code moves with the relay, the relay is faulty.",
        ],
        "причины": [
            "Corroded relay or fuse contacts in the box.",
            "Open or grounded wire to the fuel heater.",
            "Fuel heater with a faulty element.",
            "Relay with burnt contacts.",
        ],
    },

    708: {
        "узел": "Additional input/output No. 08. In Mercedes-Benz data this channel works as digital output 3/12: the unit supplies power to it and the load sits on the line. The number in the code is the SPN number, not the connector pin, so check the channel against the make's wiring diagram.",
        "нормы": [
            ("Output voltage with the load switched on", "per the manufacturer's manual"),
            ("Load resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (voltage above normal or shorted high): disconnect the load from the output. Code gone: the wire to the load is shorted to power; code still there: the channel in the unit.",
            "FMI 5 (current below normal or open circuit): with ignition off, check continuity of the wire from the output to the load and check the unit connector for a loose pin.",
            "Find from the make's wiring diagram which load is on output 3/12 and check that load on its own.",
        ],
        "причины": [
            "Chafed wire on the way to the load.",
            "Loose or corroded pin in the unit connector.",
            "Load shorted to power inside.",
            "The output channel of the control unit itself.",
        ],
    },

    714: {
        "узел": "Additional input/output No. 14. In Mercedes-Benz data this channel works as digital output 4/10: the unit connects it to ground through the load. Check the channel against the make's wiring diagram, not by the number in the code.",
        "нормы": [
            ("Output voltage with the load switched on", "per the manufacturer's manual"),
            ("Load resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 4 (voltage below normal or shorted to ground): disconnect the load from the output. Code gone: the wire or the load is shorted to ground; code still there: the channel in the unit.",
            "FMI 5 (current below normal or open circuit): check continuity of the wire from the output to the load with ignition off; check the pin in the unit connector.",
            "Use the make's wiring diagram to find the load on output 4/10 and measure its resistance on its own.",
        ],
        "причины": [
            "Wire shorted to ground on the way to the load.",
            "Open wire or a loose pin in the connector.",
            "Load with a short inside.",
            "The output channel of the control unit itself.",
        ],
    },

    716: {
        "узел": "Additional input/output No. 16. In Mercedes-Benz data this channel works as frequency output 1/09: the unit sends pulses of a set frequency to the load, not a steady voltage.",
        "нормы": [
            ("Pulse frequency at the output with the function running", "per the manufacturer's manual"),
            ("Load resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (voltage above normal or shorted high): disconnect the load. Code gone: the wire to the load is shorted to power; code still there: the channel in the unit.",
            "FMI 4 (voltage below normal or shorted to ground): the same disconnection. Code gone: shorted to ground in the harness or the load; code still there: the channel in the unit.",
            "If a device with a frequency input is on the output, check it separately per the make's wiring diagram.",
        ],
        "причины": [
            "Wire shorted to the body or to power.",
            "Corroded unit connector.",
            "Faulty load with a short inside.",
            "The output channel of the control unit itself.",
        ],
    },

    731: {
        "узел": "Knock sensor: it picks up combustion knock, and the unit uses it to adjust ignition timing. In Sitrak data this code shows an open circuit on the sensor and knock delay up to the limit, so we check both the wiring and the sensor itself.",
        "нормы": [
            ("Sensor resistance and signal voltage at the connector", "per the manufacturer's manual"),
            ("Sensor signal with the engine running and knocking", "rises on knock — from the diagnostic readout"),
        ],
        "шаги": [
            "FMI 4 (voltage below normal or shorted to ground; per Sitrak data — open circuit on knock sensor 1): unplug the sensor connector and inspect the contacts. With ignition off, check continuity of the signal wire from the sensor to the unit: open — the wire or connector; circuit intact — the sensor.",
            "FMI 15 (above normal, low severity; per Sitrak data — knock delay up to the limit): the unit holds back the timing for too long. First check the fuel and the engine condition from the diagnostic readout, then the sensor and its mounting.",
            "Sensor mounting: a loose bolt or a dirty seat distorts the signal. Tightening torque per the manufacturer's manual.",
        ],
        "причины": [
            "Open or chafed signal wire.",
            "Loose sensor mounting on the block.",
            "Low octane fuel.",
            "The knock sensor itself.",
        ],
    },

    829: {
        "узел": "Fuel level sensor in the left tank: it gives the unit the level readings for the dash. In International data this is the sensor of tank 1. Readings above or below normal mean the sensor or its circuit is giving the wrong value.",
        "нормы": [
            ("Level reading with a known fuel volume in the tank", "matches the actual volume — checked by refuelling"),
            ("Sensor resistance or signal with a full and an empty tank", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 0 (data above normal range, most severe level): compare the reading with a refuelling. If the tank holds less than the dash shows, the sensor reads high. If the readings match, check the dash and the unit.",
            "FMI 1 (data below normal range, most severe level): check that the float is not stuck and the sensor is not clogged with deposits. Then the connector and the signal wire from the sensor to the unit.",
            "Compare the left and right tanks: if only the left one is off, the cause is its sensor or its wiring.",
        ],
        "причины": [
            "Float stuck in one position.",
            "Corroded sensor connector.",
            "Open or shorted signal wire.",
            "The level sensor itself.",
        ],
    },

    830: {
        "узел": "Fuel level sensor in the right tank: it gives the unit the level readings for the dash. In International data this is the sensor of tank 2. Readings above or below normal mean the sensor or its circuit is giving the wrong value.",
        "нормы": [
            ("Level reading with a known fuel volume in the tank", "matches the actual volume — checked by refuelling"),
            ("Sensor resistance or signal with a full and an empty tank", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 0 (data above normal range, most severe level): compare the reading with a refuelling. If the tank holds less than the dash shows, the sensor reads high. If the readings match, check the dash and the unit.",
            "FMI 1 (data below normal range, most severe level): check that the float is not stuck and the sensor is not clogged with deposits. Then the connector and the signal wire from the sensor to the unit.",
            "Compare the right and left tanks: if only the right one is off, the cause is its sensor or its wiring.",
        ],
        "причины": [
            "Float stuck in one position.",
            "Corroded sensor connector.",
            "Open or shorted signal wire.",
            "The level sensor itself.",
        ],
    },

    871: {
        "узел": "Air conditioning refrigerant charge: the system tells the unit whether there is enough refrigerant in the circuit. This is a service signal, not a unit failure. In International data the code means refrigerant is low or very low.",
        "нормы": [
            ("Pressure in the air conditioning circuit with the compressor running", "per the manufacturer's manual"),
            ("Charge by volume", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1 (data below normal range, most severe level; per International data — refrigerant very low): do not top up by eye. First find the leak: check the fittings and the radiator under pressure with soapy water or a leak detector.",
            "FMI 18 (below normal, moderate severity; per International data — refrigerant low): check the pressure on the gauges with the compressor running. Top up by volume per the manufacturer's manual only after the leak is fixed.",
            "If the pressure is normal and the code is still there, check the circuit pressure sensor and its connector.",
        ],
        "причины": [
            "Leak in the pipes, fittings or the radiator.",
            "Low charge after repair without vacuum evacuation.",
            "Circuit pressure sensor with wrong readings.",
            "Compressor that does not pump.",
        ],
    },

    876: {
        "узел": "Air conditioning compressor clutch circuit: a relay feeds current to the electromagnetic compressor clutch. The code is about the current in this circuit, so we check the relay, the wire and the clutch itself.",
        "нормы": [
            ("Clutch current with the air conditioning switched on", "per the manufacturer's manual"),
            ("Clutch coil resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — inrush current below normal): check the fuse and the clutch relay. Then check continuity of the wire from the relay to the clutch with ignition off and measure the clutch coil.",
            "FMI 6 (current above normal or grounded circuit): disconnect the clutch from the harness. Code gone: the clutch shorted inside or to ground; code still there: a ground short in the wire.",
            "Swap the clutch relay with an identical one in the box: if the code moves, the relay is faulty.",
        ],
        "причины": [
            "Open wire or corroded clutch connector.",
            "Shorted clutch coil.",
            "Relay with burnt contacts.",
            "Wire shorted to ground near the compressor.",
        ],
    },

    878: {
        "узел": "Circuit for clearance, side and marker lamps. In International data a trailer clearance relay feeds current to the black wire. Check this relay's current: the relay, the fuse and the harness to the trailer.",
        "нормы": [
            ("Clearance relay current with the clearance lights on", "per the manufacturer's manual"),
            ("Load resistance on the line with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the fuse and the clearance relay. Then check continuity of the black wire from the relay to the trailer socket with ignition off.",
            "FMI 6 (current above normal or grounded circuit): disconnect the trailer socket. Code gone: the short is in the trailer or its socket; code still there: the ground short is in the tractor.",
            "Swap the relay with an identical one in the box: if the code moves, the relay is faulty.",
        ],
        "причины": [
            "Chafed black wire near the frame.",
            "Short in the trailer socket or in the trailer lamps.",
            "Corroded socket contacts.",
            "Relay with burnt contacts.",
        ],
    },

    879: {
        "узел": "Left turn signal circuit to the trailer, yellow wire. In International data a trailer turn signal relay feeds current to this circuit. Check the relay's current: the relay, the wire and the trailer socket.",
        "нормы": [
            ("Turn signal relay current with the left turn on", "per the manufacturer's manual"),
            ("Load resistance on the yellow wire with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the fuse and the turn signal relay. Then check continuity of the yellow wire from the relay to the trailer socket with ignition off.",
            "FMI 6 (current above normal or grounded circuit): disconnect the trailer socket. Code gone: the short is in the trailer; code still there: the ground short is in the tractor.",
            "Swap the relay with an identical one in the box: if the code moves, the relay is faulty.",
        ],
        "причины": [
            "Chafed yellow wire near the frame.",
            "Short in the trailer socket or in the trailer lamps.",
            "Corroded socket contacts.",
            "Turn signal relay with burnt contacts.",
        ],
    },

    880: {
        "узел": "Stop lamp circuit on the red wire. The stop lamp relay feeds current to the lamps. The code is about the current in this relay, so we check the relay, the wire and the lamps themselves.",
        "нормы": [
            ("Relay current with the brake pedal pressed", "per the manufacturer's manual"),
            ("Stop lamp resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the stop lamp fuse and the lamps themselves: a burnt-out lamp gives a low current. Then check continuity of the red wire to the trailer socket with ignition off.",
            "FMI 6 (current above normal or grounded circuit): disconnect the lamps or the socket. Code gone: the lamp or the socket; code still there: the ground short in the wire.",
            "Swap the relay with an identical one in the box: if the code moves, the relay is faulty.",
        ],
        "причины": [
            "Burnt-out stop lamp.",
            "Chafed red wire.",
            "Short to ground in the socket or the lamp.",
            "Stop lamp relay with burnt contacts.",
        ],
    },

    881: {
        "узел": "Right turn signal circuit to the trailer, green wire. In International data a trailer turn signal relay feeds current to this circuit. Check the relay's current: the relay, the wire and the trailer socket.",
        "нормы": [
            ("Turn signal relay current with the right turn on", "per the manufacturer's manual"),
            ("Load resistance on the green wire with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the fuse and the turn signal relay. Then check continuity of the green wire from the relay to the trailer socket with ignition off.",
            "FMI 6 (current above normal or grounded circuit): disconnect the trailer socket. Code gone: the short is in the trailer; code still there: the ground short is in the tractor.",
            "Swap the relay with an identical one in the box: if the code moves, the relay is faulty.",
        ],
        "причины": [
            "Chafed green wire near the frame.",
            "Short in the trailer socket or in the trailer lamps.",
            "Corroded socket contacts.",
            "Turn signal relay with burnt contacts.",
        ],
    },

    882: {
        "узел": "Rear clearance and number plate lamp circuit on the brown trailer wire. In International data the number plate lamp relay feeds current to this circuit. Check the relay's current.",
        "нормы": [
            ("Number plate lamp relay current with the clearance lights on", "per the manufacturer's manual"),
            ("Load resistance on the brown wire with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the fuse and the relay. Then check continuity of the brown wire from the relay to the trailer socket with ignition off; check the number plate lamp.",
            "FMI 6 (current above normal or grounded circuit): disconnect the trailer socket. Code gone: the short is in the trailer; code still there: the ground short is in the tractor.",
            "Swap the relay with an identical one in the box: if the code moves, the relay is faulty.",
        ],
        "причины": [
            "Burnt-out number plate lamp.",
            "Chafed brown wire.",
            "Trailer socket shorted to ground.",
            "Number plate lamp relay with burnt contacts.",
        ],
    },

    920: {
        "узел": "Audible alarm (buzzer) in the cab. The unit drives it for warnings. The code is about the buzzer control circuit: a short to power or an open circuit.",
        "нормы": [
            ("Voltage on the buzzer control side when the alarm sounds", "per the manufacturer's manual"),
            ("Buzzer resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (voltage above normal or shorted high; per Sitrak data — control side of the buzzer shorted to the power supply): disconnect the buzzer from the harness. Code gone: the buzzer is shorted to power; code still there: the wire or the unit is shorted.",
            "FMI 5 (current below normal or open circuit; per Sitrak data — open circuit of the buzzer): with ignition off, check continuity of the wire from the unit to the buzzer. An open wire or connector — repair; an open buzzer — replace.",
            "Check whether the buzzer sounds when power is applied directly: if not, the buzzer itself.",
        ],
        "причины": [
            "Open wire or disconnected buzzer connector.",
            "Short to power in the control wire.",
            "Buzzer with an open coil.",
            "Control unit that does not send the signal.",
        ],
    },

    926: {
        "узел": "Additional output No. 3. In Mercedes-Benz data this channel works as digital output 4/01: the unit connects it to ground through the load. Check the channel against the make's wiring diagram, not by the number in the code.",
        "нормы": [
            ("Output voltage with the load switched on", "per the manufacturer's manual"),
            ("Load resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 4 (voltage below normal or shorted to ground): disconnect the load from the output. Code gone: shorted to ground in the harness or the load; code still there: the channel in the unit.",
            "FMI 5 (current below normal or open circuit): check continuity of the wire from the output to the load with ignition off; check the pin in the unit connector.",
            "Use the make's wiring diagram to find the load on output 4/01 and measure its resistance on its own.",
        ],
        "причины": [
            "Wire shorted to ground on the way to the load.",
            "Open wire or a loose pin in the connector.",
            "Load with a short inside.",
            "The output channel of the control unit itself.",
        ],
    },

    928: {
        "узел": "Axle location. The code is about analog input 1, which per International data is used for axle load. The unit uses it to determine which axle is loaded, so the sensor and its circuit are checked first.",
        "нормы": [
            ("Voltage on the analog input with an empty and a full axle", "per the manufacturer's manual"),
            ("Sensor reference voltage with ignition on", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (voltage above normal or shorted high; per International data — input above normal when used for axle load): disconnect the sensor and look at the signal in the unit. Code gone: the sensor or its harness; code still there: the unit input.",
            "FMI 4 (voltage below normal or shorted to ground; per International data — input below normal when used for axle load): the same disconnection. Check the signal wire for a ground short and inspect the sensor connector for corrosion.",
            "Compare the axle load readings with the actual load: weighing, or the air bag pressure on a gauge.",
        ],
        "причины": [
            "Corroded sensor connector.",
            "Signal shorted to ground or to power in the harness.",
            "Sensor with wrong readings.",
            "The control unit that reads the signal.",
        ],
    },

    1075: {
        "узел": "Electric fuel transfer pump of the engine fuel system. The unit switches the transfer pump on when fuel pressure is low. The code is about the output to the pump: an open or a short in its control.",
        "нормы": [
            ("Voltage at the pump output when the transfer pump is switched on", "per the manufacturer's manual"),
            ("Pump winding resistance", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (per the dictionary — voltage above normal or shorted high; per Dongfeng data — open circuit of the pump output at low fuel pressure): with ignition off, check continuity of the wire from the unit to the pump and check the connector. Open — repair the wiring; circuit intact — check the pump by its winding resistance.",
            "FMI 4 (per the dictionary — voltage below normal or shorted to ground; per Dongfeng data — short circuit at the pump output): disconnect the pump from the harness. Code gone: the pump is shorted; code still there: a short in the wire.",
            "Check whether the pump runs when power is applied directly: if not, the pump itself or its relay.",
        ],
        "причины": [
            "Chafed wire on the way to the pump.",
            "Corroded pump connector in the tank.",
            "Shorted pump winding.",
            "Pump relay or the control unit.",
        ],
    },

    1384: {
        "узел": "Engine stopped by a command from the data bus. The engine ECU gets a stop command over CAN from another unit. The code says that bus messages are not acknowledged or that the engine unit does not respond.",
        "нормы": [
            ("Resistance between the CAN wires with ignition off", "60 ohm — per site data (Renault)"),
            ("Communication of all units on the bus with the engine running", "from the diagnostic readout"),
        ],
        "шаги": [
            "FMI 8 (per the dictionary — abnormal frequency or pulse width; per Renault data — bus messages not acknowledged, short between the lines or open circuit): with ignition off, measure the resistance between the CAN lines at the connector. Per site data — 60 ohm. Above that — open; below — short; correct — check the units on the bus.",
            "FMI 9 (per the dictionary — abnormal update rate; per Renault data — engine unit does not respond on CAN): check the engine unit's link to all systems and check the CAN wiring at the connectors per the make's wiring diagram.",
            "Check all the units on the bus: if the code is the same on several units, the cause is the wire, not the unit.",
        ],
        "причины": [
            "Open or shorted CAN wires.",
            "Corroded bus connector contacts.",
            "Engine unit that does not respond on the bus.",
            "Wrong resistance of the bus terminating resistors.",
        ],
    },

    1484: {
        "узел": "Other units on the bus reported faults that affect operation. The code is about a message from another unit, not about its own system: first find which unit sent it.",
        "нормы": [
            ("J1939 messages from the units on the bus without gaps", "from the diagnostic readout"),
            ("Counter and checksum in the messages", "match — from the diagnostic readout"),
        ],
        "шаги": [
            "FMI 9 (per the dictionary — abnormal update rate; per Mercedes-Benz data — J1939 message lost, message counter error): read the codes of all units on the bus and find the unit that does not send messages regularly. Check its power and connector.",
            "FMI 13 (per the dictionary — calibration out of range; per Mercedes-Benz data — J1939 message lost, checksum error): this error is usually caused by noise or a poor contact on the bus. Inspect the bus connectors and wires for chafing; check whether the code comes back after the errors are cleared.",
            "If the code comes with other bus codes, fix the bus first, not the units.",
        ],
        "причины": [
            "Noise on the bus from a poor contact.",
            "Unit that sends faulty messages.",
            "Open or chafed CAN wire.",
            "Corroded connectors.",
        ],
    },

    1547: {
        "узел": "Air conditioning evaporator temperature sensor: the unit uses it to check whether the evaporator is freezing. In International data the code is about the sensor at the heater-air conditioner inlet and the sensor at the air duct inlet.",
        "нормы": [
            ("Temperature at the heater inlet with the air conditioning on", "matches the dash reading — checked with a thermometer"),
            ("Sensor resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 0 (data above normal range, most severe level): compare the reading with a thermometer at the evaporator. If the real temperature is lower and the sensor reads high, check its connector and replace the sensor.",
            "FMI 1 (data below normal range, most severe level): check whether the evaporator is freezing. Compare with the air duct sensor: if they differ, one of them is faulty.",
            "Inspect the sensor connectors for corrosion and moisture.",
        ],
        "причины": [
            "Sensor with wrong readings.",
            "Corroded sensor connector.",
            "Open or shorted signal wire.",
            "Air duct sensor with deposits.",
        ],
    },

    1553: {
        "узел": "Heater and air conditioning blower speed control. The unit gets an analog signal from the panel control and sets the blower speed. The code is based on the readings of the control's analog input.",
        "нормы": [
            ("Blower speed control position on the panel", "readings change smoothly when turned — checked on the panel"),
            ("Voltage on the analog input at the end positions of the control", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 0 (data above normal range, most severe level): turn the control to the stop and read the value in diagnostics. If the value does not match the control position, check the potentiometer and the panel connector.",
            "FMI 1 (data below normal range, most severe level): the same check. If the value does not change, the signal wire is open or the potentiometer is faulty. Check the wire from the panel to the unit.",
            "If the blower runs at one speed only, check the blower motor itself per the manufacturer's manual.",
        ],
        "причины": [
            "Corroded control connector on the panel.",
            "Worn control potentiometer.",
            "Open signal wire.",
            "Blower control unit.",
        ],
    },

    1660: {
        "узел": "Automatic engine start alarm. The buzzer relay gives a signal that the engine may start by itself. The code is based on the current of the buzzer relay.",
        "нормы": [
            ("Buzzer relay current with the signal on", "per the manufacturer's manual"),
            ("Buzzer resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the buzzer relay and its fuse, then check continuity of the wire to the buzzer. A buzzer that does not sound is checked separately.",
            "FMI 6 (current above normal or grounded circuit): disconnect the buzzer. Code gone: the buzzer is shorted; code still there: a ground short in the wire.",
            "Swap the buzzer relay with an identical one in the box: if the code moves, the relay is faulty.",
        ],
        "причины": [
            "Open wire or corroded connector.",
            "Shorted buzzer coil.",
            "Relay with burnt contacts.",
            "Wire shorted to ground.",
        ],
    },

    1695: {
        "узел": "Fuel injection correction from the exhaust oxygen sensor (lambda): the unit checks from the sensor how far the mixture drifts and corrects the injection. The code is about a large correction deviation and an unreliable sensor signal.",
        "нормы": [
            ("Lambda sensor signal with the engine at operating temperature", "per the manufacturer's manual"),
            ("Sensor heating during warm-up", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 0 (data above normal range, most severe level; per KamAZ data — correction deviation too large): check for an air leak at the intake and for exhaust leaks before the sensor, then the sensor itself by its signal in diagnostics.",
            "FMI 2 (data erratic or intermittent; per KamAZ data — signal offset is unreliable): check the sensor: connector, sensor heating, and compare the signal with the reference in the manual. If the signal jumps — the sensor or its harness.",
            "Reset the correction and watch the diagnostics after warm-up: if the code comes back, look for the cause in fuel and air.",
        ],
        "причины": [
            "Air leak at the intake or exhaust leak.",
            "Poisoned or aged lambda sensor.",
            "Faulty sensor heater.",
            "Fuel system with a wrong injection delivery.",
        ],
    },

    1709: {
        "узел": "Gearbox control unit power relay. The PRNDL pseudo-ignition relay driver feeds power to the gearbox unit. The code is based on the currents at the driver output.",
        "нормы": [
            ("Relay driver output current with ignition on", "per the manufacturer's manual"),
            ("Voltage at the gearbox unit with ignition on", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the power fuse of the gearbox unit and the relay. With ignition off, check continuity of the wire from the driver to the relay.",
            "FMI 6 (current above normal or grounded circuit): disconnect the gearbox unit from the harness. Code gone: the unit or its harness; code still there: a ground short in the relay power wire.",
            "Check the ground of the gearbox unit and the voltage at its power input.",
        ],
        "причины": [
            "Burnt fuse or relay with burnt contacts.",
            "Ground short in the wire.",
            "Corroded gearbox unit connector.",
            "The gearbox control unit itself.",
        ],
    },

    1725: {
        "узел": "Air bag pressure, front axle, left. The sensor feeds analog input 2, which per International data is used for axle load. The code is based on this input.",
        "нормы": [
            ("Air bag pressure by gauge and by the sensor", "match — checked with a gauge in the circuit"),
            ("Sensor voltage with ignition on", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (voltage above normal or shorted high; per International data — input 2 above normal): compare the pressure on a gauge with the reading. If the gauge shows normal and the sensor reads wrong, check the sensor and the harness for a short to power.",
            "FMI 4 (voltage below normal or shorted to ground; per International data — input 2 below normal): disconnect the sensor. Code gone: a ground short in the harness or the sensor; code still there: the unit input.",
            "Inspect the air line to the bag: a leak gives a pressure drop, and the unit then sees a real low level.",
        ],
        "причины": [
            "Leak in the air line to the bag.",
            "Corroded sensor connector.",
            "Signal shorted in the harness.",
            "Sensor with wrong readings.",
        ],
    },

    1727: {
        "узел": "Air bag pressure, rear axle, left. The sensor feeds analog input 1, which per International data is used for axle load. The code is based on this input.",
        "нормы": [
            ("Air bag pressure by gauge and by the sensor", "match — checked with a gauge in the circuit"),
            ("Sensor voltage with ignition on", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (voltage above normal or shorted high; per International data — input 1 above normal): compare the pressure on a gauge with the reading. If the gauge shows normal and the sensor reads wrong, check the sensor and the harness for a short to power.",
            "FMI 4 (voltage below normal or shorted to ground; per International data — input 1 below normal): disconnect the sensor. Code gone: a ground short in the harness or the sensor; code still there: the unit input.",
            "Inspect the air line to the bag: a leak gives a pressure drop, and the unit then sees a real low level.",
        ],
        "причины": [
            "Leak in the air line to the bag.",
            "Corroded sensor connector.",
            "Signal shorted in the harness.",
            "Sensor with wrong readings.",
        ],
    },

    1741: {
        "узел": "Suspension level control mode switch. The unit uses it to know in which mode to raise or lower the axle. The code is about the switch itself and the unit.",
        "нормы": [
            ("Mode switch position and the readings in diagnostics", "change when switched — checked on the panel"),
            ("Voltage on the switch with ignition on", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 0 (data above normal range, most severe level; per International data — mode switch damaged or not connected): switch the modes and read the value in diagnostics. If it does not change — the switch or its connector.",
            "FMI 1 (data below normal range, most severe level; per International data — possible fault of the control unit): if the switch works, check the suspension control unit and its power.",
            "Check the switch connector for corrosion and an open wire to the unit.",
        ],
        "причины": [
            "Damaged switch on the panel.",
            "Corroded switch connector.",
            "Open wire to the unit.",
            "Suspension control unit.",
        ],
    },

    1755: {
        "узел": "Rear axle lowering mode. Relay of solenoid B for suspension dump releases the pressure, and the axle lowers. The code is based on the currents of this relay and solenoid.",
        "нормы": [
            ("Solenoid relay current when the axle lowers", "per the manufacturer's manual"),
            ("Solenoid resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the fuse and the relay. Check continuity of the wire to solenoid B. Replace a solenoid with an open coil.",
            "FMI 6 (current above normal or grounded circuit): disconnect the solenoid. Code gone: the solenoid is shorted; code still there: a short in the wire.",
            "Swap the relay with an identical one in the box: if the code moves, the relay is faulty.",
        ],
        "причины": [
            "Open wire or corroded connector.",
            "Shorted solenoid coil.",
            "Relay with burnt contacts.",
            "Wire shorted to ground.",
        ],
    },

    1756: {
        "узел": "Rear axle raising mode. Relay of solenoid A for suspension dump feeds current to the solenoid that raises the axle. The code is based on the currents of this relay and solenoid.",
        "нормы": [
            ("Solenoid relay current when the axle raises", "per the manufacturer's manual"),
            ("Solenoid resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the fuse and the relay. Check continuity of the wire to solenoid A. Replace a solenoid with an open coil.",
            "FMI 6 (current above normal or grounded circuit): disconnect the solenoid. Code gone: the solenoid is shorted; code still there: a short in the wire.",
            "Swap the relay with an identical one in the box: if the code moves, the relay is faulty.",
        ],
        "причины": [
            "Open wire or corroded connector.",
            "Shorted solenoid coil.",
            "Relay with burnt contacts.",
            "Wire shorted to ground.",
        ],
    },

    1820: {
        "узел": "Position of the wheelchair ramp or lift. The unit switches on a solenoid that moves the ramp. The code is based on the current of the solenoid relay.",
        "нормы": [
            ("Solenoid relay current when the ramp moves", "per the manufacturer's manual"),
            ("Solenoid coil resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "Before any check, make sure the ramp is not moving and nobody is in the area.",
            "FMI 5 (current below normal or open circuit): check the fuse and the relay. Check continuity of the wire to the solenoid with ignition off.",
            "FMI 6 (current above normal or grounded circuit): disconnect the solenoid. Code gone: the coil or its connector; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Open wire to the solenoid.",
            "Corroded solenoid connector.",
            "Shorted solenoid coil.",
            "Relay with burnt contacts.",
        ],
    },

    1858: {
        "узел": "Intermittent wiper timing relay. The unit sends a signal to the relay that sets the pauses between sweeps. Per Renault data the code is linked to contact SL2/11 and the wire insulation relative to +24 V and ground.",
        "нормы": [
            ("Relay wire insulation relative to +24 V and ground", "per site data (Renault): check relative to +24 V and to ground"),
            ("Relay coil resistance", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (voltage above normal or shorted high; per Renault data — short to positive): with ignition off, check the insulation of the relay wire relative to +24 V per the wiring diagram, contact SL2/11. A short to +24 V — repair the wiring.",
            "FMI 4 (voltage below normal or shorted to ground; per Renault data — open circuit or short to ground): check the integrity of the wire relative to ground at contact SL2/11 and disconnect the relay. Code gone: the relay or its wire to ground; code still there: the unit.",
        ],
        "причины": [
            "Chafed wire on the way to the relay.",
            "Short to positive or ground in the harness.",
            "Corroded relay connector.",
            "The wiper intermittent timing unit itself.",
        ],
    },

    2000: {
        "узел": "Network address of node 0: the unit with this address on the J1939 bus. Per International data the code is linked to the engine control unit: when the link fails or the address is wrong, the engine unit does not send its messages.",
        "нормы": [
            ("Unit messages on the J1939 bus with the correct address", "arrive regularly — from the diagnostic readout"),
            ("CAN line resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (abnormal update rate; per International data — data bus with the engine control unit lost): check the unit's link to the engine over the bus. Inspect the CAN connectors and wires for kinks and opens.",
            "FMI 19 (error in received network data; per International data — PTC1 message not received from the engine): check the engine unit for its own codes. Then the bus: a missing message is usually caused by noise or an open wire.",
            "If the code appears with bus codes from the engine unit, check the bus first.",
        ],
        "причины": [
            "Open or shorted CAN wires.",
            "Corroded bus connectors.",
            "Engine unit with no bus link.",
            "Wrongly set unit address.",
        ],
    },

    2058: {
        "узел": "Network address of node 58: the unit with this address on the J1939 bus. Per International data this is the rear heater-air conditioner. The code means the link to it has failed or the address conflicts.",
        "нормы": [
            ("Link to the rear heater over the bus", "regular messages without gaps — from the diagnostic readout"),
            ("Supply voltage of the rear heater unit", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (abnormal update rate; per International data — bus link to the rear heater failed): check the power and ground of the rear unit and its bus connector. Inspect the bus wires for disconnection.",
            "FMI 14 (per the dictionary — manufacturer-specific instructions; per International data — bus communication failure with the rear heater data bus): follow the International instructions for this address. Check the unit address against the make's table and check that no other unit has the same address.",
            "If there is no rear heater on the machine, check whether this address is used by another unit on the bus.",
        ],
        "причины": [
            "Rear heater unit without power.",
            "Open or kinked bus wire.",
            "Two units with the same address.",
            "Corroded unit connector.",
        ],
    },

    2132: {
        "узел": "Network address of node 132. Per International data this is the additional switch block No. 3. The unit reports the load connected to its switches and keeps data in memory.",
        "нормы": [
            ("Load in the message and the connected load in AGSP 3", "match — from the diagnostic readout"),
            ("Supply voltage of the switch block", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 11 (per the dictionary — root cause not known; per International data — load in the message does not match the connected load): compare the switched-on loads with the unit's message. Find a load that is on but not listed, and check its switch and harness.",
            "FMI 12 (per the dictionary — faulty device or component; per International data — non-volatile memory failure or checksum error): clear the error from diagnostics. If it comes back, replace the switch block per the manufacturer's instructions.",
            "Check the power and ground of the switch block.",
        ],
        "причины": [
            "Load connected bypassing the unit.",
            "Memory failure of the switch block.",
            "Corroded power connector.",
            "The additional switch block itself.",
        ],
    },

    2167: {
        "узел": "Network address of node 167. Per International data this is the SIC 1 unit. The code is based on the ignition signal in the message and on the unit's memory.",
        "нормы": [
            ("Ignition signal in the message and the actual ignition", "match when switched on — from the diagnostic readout"),
            ("Memory checksum of the unit", "no errors — from the diagnostic readout"),
        ],
        "шаги": [
            "FMI 11 (per the dictionary — root cause not known; per International data — ignition signal in the message does not match the switched ignition): switch the ignition on and off and watch the signal in diagnostics. If it does not match — check the ignition wire at the SIC 1 unit.",
            "FMI 12 (per the dictionary — faulty device or component; per International data — memory or checksum failure in the SIC 1 unit): clear the error and repeat the check. If it comes back — replace the SIC 1 unit per the manufacturer's instructions.",
            "Check the power of the unit and its ground.",
        ],
        "причины": [
            "Burnt or corroded ignition wire.",
            "Memory failure of the SIC 1 unit.",
            "Poor ground of the unit.",
            "The SIC 1 unit itself.",
        ],
    },

    2225: {
        "узел": "Network address of node 225. Per International data this is power module No. 1 (the power module fuse) with the link to RPM module No. 1. The code means a failed link with the module or a wrong module address.",
        "нормы": [
            ("Power module link to the bus and its bus address", "link without gaps, address matches the make's table — from the diagnostic readout"),
            ("Module supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (abnormal update rate; per International data — link with RPM module No. 1 failed): check the module's power and bus connector. A module without power does not answer on the bus.",
            "FMI 14 (per the dictionary — manufacturer-specific instructions; per International data — address problem of power module No. 1): check the module address against the make's table and check that no other module has the same address. Change the address only per the manufacturer's instructions.",
            "If several power modules have the code, look for a common cause: power or the bus, not the module.",
        ],
        "причины": [
            "Power module without voltage.",
            "Open or kinked bus wire.",
            "Address conflict between modules.",
            "The RPM module itself.",
        ],
    },

    2226: {
        "узел": "Network address of node 226. Per International data this is power module No. 2 with the link to RPM module No. 2. The code means a failed link with the module or a wrong module address.",
        "нормы": [
            ("Power module link to the bus and its bus address", "link without gaps, address matches the make's table — from the diagnostic readout"),
            ("Module supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (abnormal update rate; per International data — link with RPM module No. 2 failed): check the module's power and bus connector. A module without power does not answer on the bus.",
            "FMI 14 (per the dictionary — manufacturer-specific instructions; per International data — address problem of power module No. 2): check the module address against the make's table and check that no other module has the same address. Change the address only per the manufacturer's instructions.",
            "If several power modules have the code, look for a common cause: power or the bus, not the module.",
        ],
        "причины": [
            "Power module without voltage.",
            "Open or kinked bus wire.",
            "Address conflict between modules.",
            "The RPM module itself.",
        ],
    },

    2227: {
        "узел": "Network address of node 227. Per International data this is power module No. 3 with the link to RPM module No. 3. The code means a failed link with the module or a wrong module address.",
        "нормы": [
            ("Power module link to the bus and its bus address", "link without gaps, address matches the make's table — from the diagnostic readout"),
            ("Module supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (abnormal update rate; per International data — link with RPM module No. 3 failed): check the module's power and bus connector. A module without power does not answer on the bus.",
            "FMI 14 (per the dictionary — manufacturer-specific instructions; per International data — address problem of power module No. 3): check the module address against the make's table and check that no other module has the same address. Change the address only per the manufacturer's instructions.",
            "If several power modules have the code, look for a common cause: power or the bus, not the module.",
        ],
        "причины": [
            "Power module without voltage.",
            "Open or kinked bus wire.",
            "Address conflict between modules.",
            "The RPM module itself.",
        ],
    },

    2228: {
        "узел": "Network address of node 228. Per International data this is power module No. 4 with the link to RPM module No. 4. The code means a failed link with the module or a wrong module address.",
        "нормы": [
            ("Power module link to the bus and its bus address", "link without gaps, address matches the make's table — from the diagnostic readout"),
            ("Module supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (abnormal update rate; per International data — link with RPM module No. 4 failed): check the module's power and bus connector. A module without power does not answer on the bus.",
            "FMI 14 (per the dictionary — manufacturer-specific instructions; per International data — address problem of power module No. 4): check the module address against the make's table and check that no other module has the same address. Change the address only per the manufacturer's instructions.",
            "If several power modules have the code, look for a common cause: power or the bus, not the module.",
        ],
        "причины": [
            "Power module without voltage.",
            "Open or kinked bus wire.",
            "Address conflict between modules.",
            "The RPM module itself.",
        ],
    },

    2229: {
        "узел": "Network address of node 229. Per International data this is power module No. 5 with the link to RPM module No. 5. The code means a failed link with the module or a wrong module address.",
        "нормы": [
            ("Power module link to the bus and its bus address", "link without gaps, address matches the make's table — from the diagnostic readout"),
            ("Module supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (abnormal update rate; per International data — link with RPM module No. 5 failed): check the module's power and bus connector. A module without power does not answer on the bus.",
            "FMI 14 (per the dictionary — manufacturer-specific instructions; per International data — address problem of power module No. 5): check the module address against the make's table and check that no other module has the same address. Change the address only per the manufacturer's instructions.",
            "If several power modules have the code, look for a common cause: power or the bus, not the module.",
        ],
        "причины": [
            "Power module without voltage.",
            "Open or kinked bus wire.",
            "Address conflict between modules.",
            "The RPM module itself.",
        ],
    },

    2230: {
        "узел": "Network address of node 230. Per International data this is power module No. 6 with the link to RPM module No. 6. The code means a failed link with the module or a wrong module address.",
        "нормы": [
            ("Power module link to the bus and its bus address", "link without gaps, address matches the make's table — from the diagnostic readout"),
            ("Module supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (abnormal update rate; per International data — link with RPM module No. 6 failed): check the module's power and bus connector. A module without power does not answer on the bus.",
            "FMI 14 (per the dictionary — manufacturer-specific instructions; per International data — address problem of power module No. 6): check the module address against the make's table and check that no other module has the same address. Change the address only per the manufacturer's instructions.",
            "If several power modules have the code, look for a common cause: power or the bus, not the module.",
        ],
        "причины": [
            "Power module without voltage.",
            "Open or kinked bus wire.",
            "Address conflict between modules.",
            "The RPM module itself.",
        ],
    },

    2231: {
        "узел": "Network address of node 231. Per International data this is power module No. 7 with the link to RPM module No. 7. The code means a failed link with the module or a wrong module address.",
        "нормы": [
            ("Power module link to the bus and its bus address", "link without gaps, address matches the make's table — from the diagnostic readout"),
            ("Module supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (abnormal update rate; per International data — link with RPM module No. 7 failed): check the module's power and bus connector. A module without power does not answer on the bus.",
            "FMI 14 (per the dictionary — manufacturer-specific instructions; per International data — address problem of power module No. 7): check the module address against the make's table and check that no other module has the same address. Change the address only per the manufacturer's instructions.",
            "If several power modules have the code, look for a common cause: power or the bus, not the module.",
        ],
        "причины": [
            "Power module without voltage.",
            "Open or kinked bus wire.",
            "Address conflict between modules.",
            "The RPM module itself.",
        ],
    },

    2239: {
        "узел": "Network address of node 239. Per International data this is the HCM unit. The code is about the link to it over the bus or about an address conflict.",
        "нормы": [
            ("Link to the HCM unit over the bus", "without gaps — from the diagnostic readout"),
            ("Unit address on the bus", "unique, per the make's table"),
        ],
        "шаги": [
            "FMI 9 (abnormal update rate; per International data — bus link with the HCM unit failed): check the power of the HCM unit, its bus connector and the wires for kinks.",
            "FMI 14 (per the dictionary — manufacturer-specific instructions; per International data — address conflict of the HCM unit): check the unit address against the make's table and find another unit with the same address. Set a unique address per the manufacturer's instructions.",
        ],
        "причины": [
            "HCM unit without power.",
            "Open or kinked bus wire.",
            "Two units with the same address.",
            "Corroded unit connector.",
        ],
    },

    2362: {
        "узел": "Rear work lamps on the tractor. The unit feeds current to them through a relay. The code is based on the current in this circuit.",
        "нормы": [
            ("Lamp current when switched on", "per the manufacturer's manual"),
            ("Lamp resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the fuse and the lamp relay. Check whether at least one lamp lights; if none do — check continuity of the wire to the lamps.",
            "FMI 6 (current above normal or grounded circuit): disconnect the lamps from the harness. Code gone: a lamp or its wire is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Burnt-out lamp.",
            "Corroded lamp connector.",
            "Wire shorted to ground.",
            "Lamp relay with burnt contacts.",
        ],
    },

    2368: {
        "узел": "Left turn signals. The code is about the circuit of the front left turn signal: the unit feeds current to it through a relay.",
        "нормы": [
            ("Front left turn signal current with the turn on", "per the manufacturer's manual"),
            ("Turn signal resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — current of the front left turn signal below normal): check the fuse and the relay. Check whether the turn signal itself works; if not — check continuity of the wire.",
            "FMI 6 (current above normal or grounded circuit): disconnect the turn signal. Code gone: the turn signal is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Burnt-out turn signal lamp.",
            "Corroded turn signal connector.",
            "Open or shorted wire.",
            "Turn signal relay with burnt contacts.",
        ],
    },

    2370: {
        "узел": "Right turn signals. The code is about the circuit of the front right turn signal: the unit feeds current to it through a relay.",
        "нормы": [
            ("Front right turn signal current with the turn on", "per the manufacturer's manual"),
            ("Turn signal resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — current of the front right turn signal below normal): check the fuse and the relay. Check whether the turn signal itself works; if not — check continuity of the wire.",
            "FMI 6 (current above normal or grounded circuit): disconnect the turn signal. Code gone: the turn signal is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Burnt-out turn signal lamp.",
            "Corroded turn signal connector.",
            "Open or shorted wire.",
            "Turn signal relay with burnt contacts.",
        ],
    },

    2372: {
        "узел": "Left stop lamp. Per International data the code runs on the current of the left rear turn signal, so the same circuit and relay are checked.",
        "нормы": [
            ("Left rear turn signal current with the turn on", "per the manufacturer's manual"),
            ("Lamp resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — current of the left rear turn signal below normal): check the fuse and the relay, then the lamps. Check continuity of the wire to the rear of the tractor.",
            "FMI 6 (current above normal or grounded circuit; per International data — current of the left rear turn signal above normal): disconnect the lamps. Code gone: a lamp is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Burnt-out lamp.",
            "Corroded lamp connector.",
            "Open or shorted wire.",
            "Relay with burnt contacts.",
        ],
    },

    2374: {
        "узел": "Right stop lamp. Per International data the code runs on the current of the right rear turn signal, so the same circuit and relay are checked.",
        "нормы": [
            ("Right rear turn signal current with the turn on", "per the manufacturer's manual"),
            ("Lamp resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — current of the right rear turn signal below normal): check the fuse and the relay, then the lamps. Check continuity of the wire to the rear of the tractor.",
            "FMI 6 (current above normal or grounded circuit; per International data — current of the right rear turn signal above normal): disconnect the lamps. Code gone: a lamp is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Burnt-out lamp.",
            "Corroded lamp connector.",
            "Open or shorted wire.",
            "Relay with burnt contacts.",
        ],
    },

    2378: {
        "узел": "Tractor clearance lamps, parking lights. The unit feeds current to them through a relay. The code is based on the current in this circuit.",
        "нормы": [
            ("Parking light current when switched on", "per the manufacturer's manual"),
            ("Lamp resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — parking light current below normal): check the fuse and the relay. Check whether all the lamps light; if not — check continuity of the wire to the lights.",
            "FMI 6 (current above normal or grounded circuit; per International data — parking light current above normal): disconnect the lights from the harness. Code gone: a light is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Burnt-out lamp.",
            "Corroded light connector.",
            "Wire shorted to ground.",
            "Clearance relay with burnt contacts.",
        ],
    },

    2388: {
        "узел": "Front fog lamps on the tractor. The unit sends the command through the fog lamp relay. The code is based on the current of this relay.",
        "нормы": [
            ("Fog lamp relay current when switched on", "per the manufacturer's manual"),
            ("Lamp resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — fog lamp relay current below normal): check the fuse and the relay, then check continuity of the wire to the lamps with ignition off.",
            "FMI 6 (current above normal or grounded circuit): disconnect the lamps from the harness. Code gone: a lamp is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Burnt-out fog lamp.",
            "Corroded lamp connector.",
            "Wire shorted to ground.",
            "Fog lamp relay with burnt contacts.",
        ],
    },

    2390: {
        "узел": "Rear fog lamps. The unit feeds current through a relay to the rear lamps. The code is based on the current of this relay.",
        "нормы": [
            ("Rear fog lamp relay current when switched on", "per the manufacturer's manual"),
            ("Lamp resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the fuse and the relay, then check continuity of the wire to the lamps with ignition off.",
            "FMI 6 (current above normal or grounded circuit): disconnect the lamps from the harness. Code gone: a lamp is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Burnt-out lamp.",
            "Corroded lamp connector.",
            "Wire shorted to ground.",
            "Relay with burnt contacts.",
        ],
    },

    2392: {
        "узел": "Reverse lamp and reverse warning signal. The relay feeds current to the reverse lamps. The code is based on the current of this relay.",
        "нормы": [
            ("Reverse lamp relay current with reverse gear engaged", "per the manufacturer's manual"),
            ("Lamp resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the fuse and the relay, then check continuity of the wire to the lamps with ignition off. Check the reverse warning signal separately.",
            "FMI 6 (current above normal or grounded circuit): disconnect the lamps from the harness. Code gone: a lamp is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Burnt-out reverse lamp.",
            "Corroded lamp connector.",
            "Wire shorted to ground.",
            "Lamp relay with burnt contacts.",
        ],
    },

    2404: {
        "узел": "Daytime running lights. Per International data the code is about the control relay of the clearance light, which switches the light on when driving.",
        "нормы": [
            ("Control relay current with the clearance light on", "per the manufacturer's manual"),
            ("Lamp resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the fuse and the control relay, then check continuity of the wire to the lights with ignition off.",
            "FMI 6 (current above normal or grounded circuit): disconnect the lights from the harness. Code gone: a light is shorted; code still there: a ground short in the wire or the relay.",
        ],
        "причины": [
            "Burnt-out running light.",
            "Corroded light connector.",
            "Wire shorted to ground.",
            "Control relay with burnt contacts.",
        ],
    },

    2636: {
        "узел": "Wiper motor on and off. The relay feeds power to the wiper motor. The code is based on the current of this relay.",
        "нормы": [
            ("Relay current with the wiper on", "per the manufacturer's manual"),
            ("Wiper motor resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the fuse and the motor relay, then check continuity of the wire to the motor with ignition off.",
            "FMI 6 (current above normal or grounded circuit): disconnect the wiper motor from the harness. Code gone: the motor is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Open wire or corroded motor connector.",
            "Shorted motor winding.",
            "Relay with burnt contacts.",
            "Wire shorted to ground.",
        ],
    },

    2637: {
        "узел": "Wiper motor speed. The speed switching relay selects the motor winding. The code is based on the current of this relay.",
        "нормы": [
            ("Speed switching relay current at the selected speed", "per the manufacturer's manual"),
            ("Motor winding resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): check the fuse and the speed relay, then check continuity of the wire from the relay to the motor with ignition off.",
            "FMI 6 (current above normal or grounded circuit): disconnect the motor from the harness. Code gone: the motor is shorted; code still there: a ground short in the relay wire.",
        ],
        "причины": [
            "Open wire to the speed winding.",
            "Corroded contacts of the speed relay.",
            "Shorted motor winding.",
            "Relay with burnt contacts.",
        ],
    },

    2641: {
        "узел": "Audible horn. The unit or the switch feeds current to the electric horn. The code is based on the current of this circuit.",
        "нормы": [
            ("Horn current with the button pressed", "per the manufacturer's manual"),
            ("Horn resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal; per International data — horn current below normal): check the fuse, the button and the connector. Feed power to the horn directly: if it sounds, the fault is in the control circuit.",
            "FMI 6 (current above normal; per International data — horn current above normal): disconnect the horn from the harness. Code gone: the horn itself is shorted; code still there: a short in the wire.",
        ],
        "причины": [
            "Corroded horn connector.",
            "Shorted horn coil.",
            "Button stuck.",
            "Wire shorted to ground.",
        ],
    },

    2642: {
        "узел": "Mirror heater. The code is about mirror heater 1 (left) per International data: the heating element and its circuit.",
        "нормы": [
            ("Mirror heater current when switched on", "per the manufacturer's manual"),
            ("Heating element resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal; per International data — left mirror current below normal): check the fuse and the heater switch, then measure the resistance of the mirror element.",
            "FMI 6 (current above normal; per International data — left mirror current above normal): disconnect the element from the harness. Code gone: the element is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Open heating element.",
            "Corroded mirror connector.",
            "Element shorted to ground.",
            "Heater switch with burnt contacts.",
        ],
    },

    2653: {
        "узел": "Left headlamp low beam No. 1. The unit feeds current to the left headlamp bulb. The code is based on the current of this circuit.",
        "нормы": [
            ("Low beam bulb current when switched on", "per the manufacturer's manual"),
            ("Bulb resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal; per International data — current below normal): check the bulb and the fuse. If the bulb is out — replace it per the manual, then check continuity of the wire to the headlamp.",
            "FMI 6 (current above normal or grounded circuit): disconnect the headlamp from the harness. Code gone: the headlamp is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Burnt-out low beam bulb.",
            "Corroded headlamp connector.",
            "Wire shorted to ground.",
            "Light control unit.",
        ],
    },

    2655: {
        "узел": "Right headlamp low beam No. 1. The unit feeds current to the right headlamp bulb. The code is based on this circuit.",
        "нормы": [
            ("Low beam bulb current when switched on", "per the manufacturer's manual"),
            ("Bulb resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (open circuit; per International data — open circuit): check the bulb and the fuse. With ignition off, check continuity of the wire from the unit to the headlamp; an open wire — repair the wiring.",
            "FMI 6 (current above normal or grounded circuit; per International data — ground short): disconnect the headlamp from the harness. Code gone: the headlamp shorted to ground; code still there: a short in the wire.",
        ],
        "причины": [
            "Open wire to the headlamp.",
            "Corroded headlamp connector.",
            "Wire shorted to ground.",
            "Burnt-out bulb.",
        ],
    },

    2819: {
        "узел": "Parking lock: the lock solenoid on the gearbox holds the parking position. The code is based on the current at the solenoid output. Before any check the machine must stand on level ground with wheel chocks.",
        "нормы": [
            ("Lock solenoid current when the parking is engaged", "per the manufacturer's manual"),
            ("Solenoid winding resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — current at the lock solenoid output below normal): check the fuse and the unit output. With ignition off, check continuity of the wire to the solenoid and measure the winding.",
            "FMI 6 (current above normal or grounded circuit): disconnect the solenoid. Code gone: the solenoid is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Open wire to the solenoid.",
            "Shorted solenoid winding.",
            "Corroded solenoid connector.",
            "Control unit with a faulty output.",
        ],
    },

    3227: {
        "узел": "HEGO oxygen sensor after the catalyst of the aftertreatment system 1. The unit uses it to monitor the catalyst.",
        "нормы": [
            ("HEGO sensor signal at the operating temperature", "swings between lean and rich mixture — from the diagnostic readout"),
            ("Sensor heating during warm-up", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per Sitrak data — open circuit of the HEGO sensor): check the sensor connector and the signal wire; with ignition off, check continuity of the wire from the sensor to the unit. An open wire — repair the wiring; an open heater in the sensor — replace the sensor.",
            "FMI 11 (per the dictionary — root cause not known; per Sitrak data — slow response of the HEGO sensor): check whether the sensor is clogged with soot and whether it is worn out. If the response is slow at operating temperature — replace the sensor per the manufacturer's manual.",
        ],
        "причины": [
            "Open wire or corroded sensor connector.",
            "Old sensor with a slow response.",
            "Dirty sensor.",
            "Air leak before the sensor.",
        ],
    },

    3242: {
        "узел": "Temperature sensor before the oxidation catalyst of the aftertreatment system 1. The unit uses it to know the gas temperature at the inlet of the soot filter (DPF). The code is based on the sensor signal.",
        "нормы": [
            ("Sensor resistance", "per the manufacturer's manual"),
            ("Sensor voltage with ignition on", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (per the dictionary — voltage above normal or shorted high; per KamAZ data — also open circuit of the sensor): with ignition off, disconnect the sensor and check continuity of the signal wire to the unit. A short to power or an open — repair the wiring.",
            "FMI 4 (voltage below normal or shorted to ground): disconnect the sensor. Code gone: a short in the wire or the sensor; code still there: the control unit.",
        ],
        "причины": [
            "Open or shorted sensor wire.",
            "Corroded sensor connector.",
            "Sensor with wrong readings.",
            "Control unit.",
        ],
    },

    3250: {
        "узел": "Temperature sensor after the oxidation catalyst of the aftertreatment system 1. The unit uses it to monitor the gas temperature in the soot filter (DPF) after the catalyst. The code is based on the sensor signal.",
        "нормы": [
            ("Sensor resistance", "per the manufacturer's manual"),
            ("Sensor voltage with ignition on", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (per the dictionary — voltage above normal or shorted high; per KamAZ data — also open circuit of the sensor): with ignition off, disconnect the sensor and check continuity of the signal wire to the unit. A short to power or an open — repair the wiring.",
            "FMI 4 (voltage below normal or shorted to ground): disconnect the sensor. Code gone: a short in the wire or the sensor; code still there: the control unit.",
        ],
        "причины": [
            "Open or shorted sensor wire.",
            "Corroded sensor connector.",
            "Sensor with wrong readings.",
            "Control unit.",
        ],
    },

    3313: {
        "узел": "Fifth wheel coupling status indicator. The solenoid releases the jaws on the fifth wheel, and the indicator shows the status. The code is based on the current at the output of solenoid 1.",
        "нормы": [
            ("Release solenoid current in operation", "per the manufacturer's manual"),
            ("Solenoid winding resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — current at solenoid 1 output below normal): check the fuse and the unit output. With ignition off, check continuity of the wire to the solenoid.",
            "FMI 6 (current above normal or grounded circuit): disconnect the solenoid. Code gone: the solenoid is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Open wire to the solenoid.",
            "Corroded connector on the fifth wheel.",
            "Shorted solenoid coil.",
            "Control unit with a faulty output.",
        ],
    },

    3316: {
        "узел": "Fifth wheel slide lock indicator. The lock of the sliding fifth wheel and its indicator. The code is based on the current at the lock.",
        "нормы": [
            ("Sliding fifth wheel lock current in operation", "per the manufacturer's manual"),
            ("Lock winding resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — current below normal or open circuit): check the fuse and the unit output. With ignition off, check continuity of the wire to the lock.",
            "FMI 6 (current above normal or grounded circuit; per International data — current above normal): disconnect the lock from the harness. Code gone: the lock is shorted; code still there: a short in the wire.",
        ],
        "причины": [
            "Open wire to the lock.",
            "Corroded connector on the sliding fifth wheel.",
            "Shorted lock winding.",
            "Control unit with a faulty output.",
        ],
    },

    3456: {
        "узел": "Permission to engage the power take-off (PTO) from the gearbox input shaft No. 1. The solenoid relay A allows the PTO to engage. The code is based on the current of this relay.",
        "нормы": [
            ("Solenoid relay A current when the PTO is engaged", "per the manufacturer's manual"),
            ("Solenoid resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — current of the PTO A solenoid relay below normal): check the fuse and the relay, then check continuity of the wire to the solenoid with ignition off.",
            "FMI 6 (current above normal or grounded circuit; per International data — current of the PTO A solenoid relay above normal): disconnect the solenoid. Code gone: the solenoid is shorted; code still there: a ground short in the wire.",
            "When checking the PTO, do not leave it engaged unattended and do not work on it without the machine stood on wheel chocks.",
        ],
        "причины": [
            "Open wire to the PTO A solenoid.",
            "Corroded connector.",
            "Shorted solenoid winding.",
            "Relay with burnt contacts.",
        ],
    },

    3457: {
        "узел": "Permission to engage the power take-off (PTO) from the gearbox input shaft No. 2. The solenoid relay B allows the PTO to engage. The code is based on the current of this relay.",
        "нормы": [
            ("Solenoid relay B current when the PTO is engaged", "per the manufacturer's manual"),
            ("Solenoid resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — current of the PTO B solenoid relay below normal): check the fuse and the relay, then check continuity of the wire to the solenoid with ignition off.",
            "FMI 6 (current above normal or grounded circuit; per International data — current of the PTO B solenoid relay above normal): disconnect the solenoid. Code gone: the solenoid is shorted; code still there: a ground short in the wire.",
            "When checking the PTO, do not leave it engaged unattended and do not work on it without the machine stood on wheel chocks.",
        ],
        "причины": [
            "Open wire to the PTO B solenoid.",
            "Corroded connector.",
            "Shorted solenoid winding.",
            "Relay with burnt contacts.",
        ],
    },

    3461: {
        "узел": "PTO engagement status from the gearbox input shaft No. 2. The pneumatic solenoid of the PTO shows whether the PTO is engaged. The code is based on the current of this solenoid.",
        "нормы": [
            ("Pneumatic PTO solenoid current when engaged and disengaged", "per the manufacturer's manual"),
            ("Solenoid resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — current of the PTO pneumatic solenoid below normal): check the fuse and the unit output, then check continuity of the wire to the solenoid with ignition off.",
            "FMI 6 (current above normal or grounded circuit; per International data — current of the PTO pneumatic solenoid above normal): disconnect the solenoid. Code gone: the solenoid is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Open wire to the solenoid.",
            "Corroded connector.",
            "Shorted solenoid winding.",
            "PTO pneumatics with the piston in the wrong position.",
        ],
    },

    3515: {
        "узел": "Urea (AdBlue) temperature sensor in the tank or the supply line. The unit uses it to keep the urea from freezing or overheating. The code is based on the sensor input.",
        "нормы": [
            ("Urea temperature by the sensor and by a thermometer", "match — from the diagnostic readout"),
            ("Sensor resistance", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (per the dictionary — voltage above normal or shorted high; per KamAZ data — input shorted to power): with ignition off, disconnect the sensor and check continuity of the wire to the unit. A short to power — repair the wiring.",
            "FMI 4 (voltage below normal or shorted to ground; per KamAZ data — input shorted to ground): disconnect the sensor. Code gone: a short in the harness or the sensor; code still there: the urea supply control unit.",
        ],
        "причины": [
            "Wire shorted to power or ground.",
            "Corroded sensor connector in the tank.",
            "Sensor with wrong readings.",
            "AdBlue supply control unit.",
        ],
    },

    3697: {
        "узел": "Diesel particulate filter (DPF) lamp on the dash. The lamp relay feeds current to it when the soot filter needs attention. The code is based on the current of the relay.",
        "нормы": [
            ("Lamp relay current with the lamp on", "per the manufacturer's manual"),
            ("Lamp resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — lamp relay current below normal): check the lamp on the dash and the fuse. Then check continuity of the wire from the relay to the dash with ignition off.",
            "FMI 6 (current above normal or grounded circuit; per International data — lamp relay current above normal): disconnect the lamp from the harness. Code gone: the lamp or the dash; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Burnt-out lamp on the dash.",
            "Open wire to the lamp relay.",
            "Wire shorted to ground.",
            "Lamp relay with burnt contacts.",
        ],
    },

    3698: {
        "узел": "High exhaust temperature lamp on the dash. The unit switches it on when the exhaust is hot. The code is based on the current of this circuit: the lamp, its relay and the wire. The lamp itself does not show overheating.",
        "нормы": [
            ("Lamp current with ignition on", "per the manufacturer's manual"),
            ("Lamp resistance with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit; per International data — current below normal or open circuit): check the lamp on the dash and the fuse. With ignition off, check continuity of the wire to the lamp.",
            "FMI 6 (current above normal or grounded circuit; per International data — current above normal): disconnect the lamp from the harness. Code gone: the lamp is shorted; code still there: a ground short in the wire.",
        ],
        "причины": [
            "Burnt-out lamp on the dash.",
            "Open wire.",
            "Wire shorted to ground.",
            "Control unit with a faulty output.",
        ],
    },

    3826: {
        "узел": "Average urea (AdBlue) consumption of the aftertreatment system 1. The unit counts how much urea goes into the system during operation. The code is about a consumption above or below normal.",
        "нормы": [
            ("Urea consumption in normal operation of the system", "per the manufacturer's manual"),
            ("Dosing valve and supply pump", "checked from the diagnostic readout"),
        ],
        "шаги": [
            "FMI 0 (data above normal range, most severe level; per KamAZ data — consumption too high): check the dosing valve for leaks and for sticking in the open position. Then the supply pump and the line pressure per the manual.",
            "FMI 1 (data below normal range, most severe level; per KamAZ data — consumption too low): check the line and the filter for clogging, the supply pressure, and whether the doser is blocked by crystals. Then the level and the quality of the urea.",
        ],
        "причины": [
            "Clogged doser or line.",
            "Dosing valve stuck.",
            "Poor AdBlue quality or low level.",
            "Supply pump with a pressure drop.",
        ],
    },

    3828: {
        "узел": "Set urea (AdBlue) consumption of the aftertreatment system 1. The unit compares the set consumption, which it has calculated, with what is actually supplied. The code is about the comparison of these values.",
        "нормы": [
            ("Set and actual urea consumption", "match within tolerance — from the diagnostic readout"),
            ("Dosing valve and supply pump", "checked from the diagnostic readout"),
        ],
        "шаги": [
            "FMI 0 (data above normal range, most severe level; per KamAZ data — consumption too high): check the dosing valve for leaks and sticking. Then the supply pump and the line pressure per the manual.",
            "FMI 1 (data below normal range, most severe level; per KamAZ data — consumption too low): check the line and the filter for clogging, the supply pressure and the doser. Then the level and the quality of the urea.",
        ],
        "причины": [
            "Clogged doser or line.",
            "Dosing valve stuck.",
            "Poor AdBlue quality or low level.",
            "Supply pump with a pressure drop.",
        ],
    },

    3843: {
        "узел": "Additional input/output No. 20. In Mercedes-Benz data this channel works as digital input 1/01: the unit reads whether a switch or sensor is shorted to it.",
        "нормы": [
            ("Input voltage with the switch open", "per the manufacturer's manual"),
            ("Input voltage with the switch closed", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (voltage above normal or shorted high): disconnect the switch or sensor from the input. Code gone: a short to power in the harness or the switch; code still there: the input of the unit.",
            "FMI 4 (voltage below normal or shorted to ground): disconnect the switches and sensors connected to this line one by one. Code gone: the one that shorted to ground; if all are disconnected and the code is still there, the harness to the unit.",
        ],
        "причины": [
            "Chafed wire on the body.",
            "Switch or sensor with a short.",
            "Corroded unit connector.",
            "The input of the control unit itself.",
        ],
    },

    3844: {
        "узел": "Additional input/output No. 21. In Mercedes-Benz data this channel works as digital input 1/02: the unit reads whether a switch or sensor is shorted to it.",
        "нормы": [
            ("Input voltage with the switch open", "per the manufacturer's manual"),
            ("Input voltage with the switch closed", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (voltage above normal or shorted high): disconnect the switch or sensor from the input. Code gone: a short to power in the harness or the switch; code still there: the input of the unit.",
            "FMI 4 (voltage below normal or shorted to ground): disconnect the switches and sensors connected to this line one by one. Code gone: the one that shorted to ground; if all are disconnected and the code is still there, the harness to the unit.",
        ],
        "причины": [
            "Chafed wire on the body.",
            "Switch or sensor with a short.",
            "Corroded unit connector.",
            "The input of the control unit itself.",
        ],
    },

    3845: {
        "узел": "Additional input/output No. 22. In Mercedes-Benz data this channel works as digital input 1/12: the unit reads whether a switch or sensor is shorted to it.",
        "нормы": [
            ("Input voltage with the switch open", "per the manufacturer's manual"),
            ("Input voltage with the switch closed", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (voltage above normal or shorted high): disconnect the switch or sensor from the input. Code gone: a short to power in the harness or the switch; code still there: the input of the unit.",
            "FMI 4 (voltage below normal or shorted to ground): disconnect the switches and sensors connected to this line one by one. Code gone: the one that shorted to ground; if all are disconnected and the code is still there, the harness to the unit.",
        ],
        "причины": [
            "Chafed wire on the body.",
            "Switch or sensor with a short.",
            "Corroded unit connector.",
            "The input of the control unit itself.",
        ],
    },

}
