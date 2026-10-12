# -*- coding: utf-8 -*-
"""English twin of own_checks_5.py: the same codes, the same fields and the same keys.
Key = SPN. Numbers, units, FMI values and make names are the same as in the Russian data.
"""

CHECKS = {
    4364: {
        "узел": "SCR catalyst (SCR 1) in the exhaust: urea from the doser turns NOx into nitrogen and water. The ECU compares NOx before and after the catalyst. The code is about exceeded emissions, not necessarily a broken catalyst.",
        "нормы": [
            ("NOx after the catalyst, first threshold", "per the manufacturer's manual"),
            ("NOx after the catalyst, second threshold", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 15 (above normal, low urgency) and FMI 16 (above normal, medium urgency). On KAMAZ-5490 these are MR2 12971 and MR2 12972. First read the NOx values before and after the catalyst with the engine warm.",
            "Check the AdBlue: quality, shelf life, level in the tank. Poor-quality urea lowers NOx conversion, and emissions go above the threshold.",
            "Check the AdBlue doser and injector: no dose means NOx rises, and the code appears at the catalyst.",
            "Inspect the exhaust before the catalyst and the sensor: air leaks give a low NOx reading or, the other way round, a false value.",
            "After repair, clear the code and do a test drive. If the code comes back after warm-up, keep looking instead of replacing the sensor.",
        ],
        "причины": [
            "AdBlue of poor quality or out of date.",
            "Clogged or faulty AdBlue doser module.",
            "Catalyst wear or blockage.",
            "Faulty NOx sensor after the catalyst.",
            "Exhaust leak before the sensor.",
        ],
    },

    4809: {
        "узел": "Temperature sensor at the inlet of the SCR warm-up catalyst. The ECU uses it to decide when to turn on heating and dosing. On KAMAZ-5490 this is the temperature sensor of catalyst 1.",
        "нормы": [
            ("Sensor on the connector with ignition off", "per the manufacturer's manual"),
            ("Sensor resistance at room temperature", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (input shorted to positive): unplug the sensor connector and check for voltage on the signal pin with ignition off. Voltage present means a short to positive in the harness; no voltage means the sensor.",
            "FMI 4 (input shorted to ground): unplug the connector and check the signal wire for continuity to ground. Code gone means a short in the harness; code still there means the sensor.",
            "Check the connector for corrosion and urea leaks: urea gets into the contacts and makes a false circuit.",
            "Compare the reading with the exhaust temperature sensor next to it: a gap larger than the engine temperature gap points to the sensor.",
        ],
        "причины": [
            "Short to positive or ground in the harness near the catalyst.",
            "Temperature sensor open or shorted inside.",
            "Corroded connector at the hot exhaust.",
            "Damaged wire insulation from heat.",
        ],
    },

    5430: {
        "узел": "Absolute pressure sensor of the EGR system (exhaust gas recirculation). The ECU uses it to know how much exhaust goes back into the engine. On Sitrak data this is the EGR pressure sensor.",
        "нормы": [
            ("Reference voltage at the sensor connector", "5.0 V ± 0.25"),
            ("Pressure with the engine off, against the barometer", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (voltage above normal): with ignition on, measure the reference voltage at the sensor connector against ground. Above the table value — check the ECU and the supply wire.",
            "FMI 4 (voltage below normal): unplug the sensor and inspect the contacts. If there is no reference voltage, check continuity from the ECU to the sensor.",
            "Compare the reading with the barometer with the engine off. The values should match atmospheric pressure.",
            "Inspect the EGR sensor hose and fittings: a blocked or pinched hose gives a wrong pressure under load.",
        ],
        "причины": [
            "Corroded or oil-soaked sensor connector.",
            "EGR pressure sensor with drift or a short.",
            "Open or shorted signal wire.",
            "Blocked or pinched sensor hose.",
        ],
    },

    5543: {
        "узел": "Engine brake command switch (exhaust flap) on the steering column or the panel. Pressing it tells the ECU to engage the flap. On Sitrak data the code is about the switch being shorted to supply or to ground.",
        "нормы": [
            ("Switch on the connector, pressed and released", "the contact closes and opens without bounce"),
            ("Signal voltage with the switch released", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 3 (short to supply): with the switch unplugged, check for voltage on its signal contact with ignition on. Voltage present means the wire is shorted to positive.",
            "FMI 4 (short to ground): unplug the switch connector and check the signal wire for continuity to ground. Code gone means a short in the harness; code still there means the switch.",
            "With the engine running, press the switch a few times and watch the state in diagnostics. No change means the switch or its contact.",
            "Check the fuse of the switch circuit and the connector under the steering column for corrosion.",
        ],
        "причины": [
            "Stuck or broken engine brake switch.",
            "Wire shorted to ground or positive in the column.",
            "Corroded connector under the steering column.",
            "Pinched or worn insulation in the spiral cable.",
        ],
    },

    109: {
        "узел": "Coolant pressure sensor. On International data this SPN gives high refrigerant pressure (a manufacturer-specific code). In J1939 it is FMI 14, a special case the manufacturer describes separately.",
        "нормы": [
            ("Coolant circuit pressure with the engine hot", "per the manufacturer's manual"),
            ("Pressure with the expansion tank cap open", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 14 (special instruction from the manufacturer): by the standard a special case, by International data high refrigerant pressure. First check the coolant level and the leaks: overheating and coolant pressure go together.",
            "Check the pressure relief valve in the expansion tank cap: a stuck valve holds the pressure above normal.",
            "Measure the pressure on the circuit with a mechanical gauge with the engine hot and compare with the sensor.",
            "Check the thermostat: if it does not open, the pressure rises during warm-up.",
        ],
        "причины": [
            "Stuck valve in the tank cap.",
            "Blocked radiator or a thermostat that does not open.",
            "Faulty coolant pressure sensor.",
            "Gas leak into the cooling circuit from the cylinder head.",
        ],
    },

    115: {
        "узел": "Alternator current: the ECU monitors the current the alternator delivers. On International data this code is about phase loss or an alternator fault. There is no separate current sensor here; the deviation shows up in how the alternator behaves.",
        "нормы": [
            ("Alternator current at mid speed, engine running", "per the manufacturer's manual"),
            ("On-board voltage with the engine running", "27.5…28.8 V"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): check the alternator terminals and the engine ground, then the drive belt. A loose belt or slip gives an unstable current.",
            "Measure the battery voltage with the engine running, with and without load: above 28.8 V — the regulator; below 27.5 V — the alternator or the wire.",
            "Check each output wire of the alternator for an open circuit: a phase loss in the rectifier gives current ripple.",
            "Turn on the load (headlights, heater fan) and check the alternator: the current should rise. If not, the alternator.",
        ],
        "причины": [
            "Worn belt or tensioner.",
            "Corroded alternator terminals or ground.",
            "Faulty rectifier or alternator winding.",
            "Voltage regulator.",
        ],
    },

    412: {
        "узел": "EGR temperature sensor (recirculated exhaust gas). It shows how hot the exhaust going back into the engine is. On Sitrak data the code is about too high EGR temperature.",
        "нормы": [
            ("EGR temperature with the engine warm, under load", "per the manufacturer's manual"),
            ("Temperature at cold start, engine cold", "close to the outside air temperature"),
        ],
        "шаги": [
            "FMI 0 (data above normal): check the EGR cooler coolant flow and whether the cooler is blocked. Without cooling the temperature rises.",
            "Check the EGR valve: if it stays open under load, hot exhaust goes into the engine without the proper cooling.",
            "Compare the sensor reading with the exhaust temperature before the catalyst. A difference points to the sensor.",
            "Check the sensor connector and the wire for an open circuit, and the harness for heat damage.",
        ],
        "причины": [
            "Blocked or leaking EGR cooler.",
            "EGR valve stuck open.",
            "Faulty EGR temperature sensor.",
            "Low coolant in the EGR circuit.",
        ],
    },

    556: {
        "узел": "Retarder reference torque of the gearbox retarder: the value the ECU uses to calculate braking. The retarder sends it over J1939 in the RC message. On Mercedes-Benz data the code is about the RC message from the retarder not arriving.",
        "нормы": [
            ("RC message on the bus with the engine running", "arrives regularly, without gaps"),
            ("Retarder supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (no J1939 message): check in diagnostics which units have dropped off the bus. If only the retarder is missing, look at the retarder unit or its supply.",
            "Check the power and ground of the retarder unit, then the CAN connector on it.",
            "Check the CAN bus resistance with power off: about 60 ohm.",
            "If the message arrives but the value is zero, check the retarder parameters in diagnostics.",
        ],
        "причины": [
            "Open or corroded CAN connector at the retarder.",
            "Loss of power to the retarder unit.",
            "Faulty retarder unit.",
            "Wrong communication parameters.",
        ],
    },

    571: {
        "узел": "Retarder enable switch (auxiliary braking) on the panel or the lever. The driver uses it to enable the retarder and the auxiliary brake. On International data the code is about a switch fault.",
        "нормы": [
            ("Switch on the connector, on and off", "the contact closes and opens without bounce"),
            ("Signal voltage with the switch off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): toggle the switch several times and watch the state in diagnostics. If it changes erratically, it is the switch.",
            "Check the switch connector and the signal wire for corrosion and an open circuit with ignition off.",
            "Check the fuse of the switch circuit.",
            "Compare with the engine brake switch: if that one also shows a fault, the common supply of the panel is the problem.",
        ],
        "причины": [
            "Wear or sticking of the switch itself.",
            "Corroded connector on the panel.",
            "Open signal wire.",
            "Faulty circuit fuse.",
        ],
    },

    577: {
        "узел": "Hill holder switch for ASR. The driver turns it on so the truck does not roll back when starting on a slope. On International data the code is about a fault in the HSA disable switch.",
        "нормы": [
            ("Switch state in both positions", "the contact changes cleanly, without bounce"),
            ("Signal contact voltage with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): toggle the switch with the engine running and watch its state in diagnostics. No change or an unstable change — the switch.",
            "Check the switch connector for corrosion and an open signal wire with ignition off.",
            "Check the ASR unit: if it reads the switch differently from what the switch shows, check the unit parameters.",
            "Clear the code and test the function on level ground, then on a slight slope.",
        ],
        "причины": [
            "Worn switch contacts.",
            "Corroded connector on the panel.",
            "Open signal wire.",
            "Wrong ASR unit parameters.",
        ],
    },

    685: {
        "узел": "Switch for the front axle 1 differential lock release request. The driver releases the lock, and the ECU sends the request to the actuator. On International data the code is about a fault in the lock switch.",
        "нормы": [
            ("Switch state in both positions", "the contact changes cleanly"),
            ("Signal voltage with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): toggle the switch and watch the request state in diagnostics. No change — the switch or its connector.",
            "Check the switch connector and the signal wire for corrosion, an open circuit and a short to ground.",
            "Check whether the front axle lock actuator follows the request. If the actuator stays in one position while the switch shows the other, the two are out of step.",
            "Clear the code and test the release at standstill, then on the road.",
        ],
        "причины": [
            "Wear or sticking of the switch button.",
            "Corroded connector in the cab.",
            "Open signal wire.",
            "Mismatch with the axle lock actuator.",
        ],
    },

    691: {
        "узел": "Switch for the release request of the rear axle inter-axle differential (central rear). The ECU sends the request to the inter-axle lock actuator. On International data the code is about a fault in the inter-axle lock switch.",
        "нормы": [
            ("Switch state in both positions", "the contact changes cleanly"),
            ("Signal voltage with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): toggle the switch with the truck standing still and watch the request state. No change — the switch.",
            "Check the switch connector and the signal wire for an open circuit and a short to ground with ignition off.",
            "Check the inter-axle lock actuator: when switched on, there should be a click and a change of the actuator position.",
            "Clear the code and test the lock at standstill.",
        ],
        "причины": [
            "Wear or sticking of the switch.",
            "Corrosion at the connector.",
            "Open signal wire.",
            "Faulty inter-axle lock actuator.",
        ],
    },

    979: {
        "узел": "Remote control switch for the preset PTO speed. The driver sets the PTO speed with a button. On Mercedes-Benz data the code is about no PTO message on J1939 since ignition was switched on.",
        "нормы": [
            ("PTO message on the bus since ignition on", "arrives right away and regularly"),
            ("PTO unit supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (no J1939 message): check whether the PTO unit sends messages on the bus. If there are none from the first second after ignition on, look at the PTO unit supply and its connector.",
            "Check the power and ground of the PTO unit and the CAN connector on it.",
            "Check the remote control switch: if it works and there is still no message, the problem is in the PTO unit itself.",
            "Clear the code and switch the PTO on at standstill to see if the message appears.",
        ],
        "причины": [
            "Loss of power to the PTO unit.",
            "Open or corroded CAN connector at the PTO unit.",
            "Faulty PTO unit.",
            "Wrong unit address on the bus.",
        ],
    },

    980: {
        "узел": "PTO enable switch (KOM) in the cab. The driver uses it to enable the power take-off from the engine. On International data the code is about a fault in the engine KOM switch.",
        "нормы": [
            ("Switch state in both positions", "the contact changes cleanly"),
            ("Signal voltage with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): toggle the switch with the truck standing still and watch the KOM state in diagnostics. No change — the switch.",
            "Check the switch connector for corrosion and an open signal wire with ignition off.",
            "Check whether the KOM unit gives the enable signal: compare it with the state of the panel switch.",
            "Clear the code and test the enable at standstill.",
        ],
        "причины": [
            "Wear of the switch contacts.",
            "Corrosion at the panel connector.",
            "Open signal wire.",
            "Faulty KOM unit.",
        ],
    },

    1048: {
        "узел": "Pneumatic pressure regulation on the first axle (front circuit). The module measures the circuit pressure and controls the valves. On Renault data the code is about a fault in the pneumatic system of the front circuit or an internal module fault.",
        "нормы": [
            ("Front circuit pressure with the compressor running", "per the manufacturer's manual"),
            ("Pressure drop with the compressor off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 7 (mechanical system not responding): by the standard, the valve or mechanism does not respond to the command; by Renault data, a fault in the pneumatic circuit of the front axle. First check for leaks at the module inlet and outlet with soapy water.",
            "Check the air lines for kinks and contamination, then the exhaust at the valve and at the module.",
            "Check the minimum pressure gauges in the front axle circuit.",
            "Clear the code and check the circuit pressure with the compressor running.",
        ],
        "причины": [
            "Air leak at the fittings or in the front circuit line.",
            "Contaminated or stuck module valve.",
            "Faulty pressure regulation module.",
            "Kinked or contaminated air line.",
        ],
    },

    1051: {
        "узел": "Pneumatic pressure regulation on the second axle (rear circuit). The module measures the circuit pressure and controls the valves. On Renault data the code is about a fault in the pneumatic system of the rear circuit or an internal module fault.",
        "нормы": [
            ("Rear circuit pressure with the compressor running", "per the manufacturer's manual"),
            ("Pressure drop with the compressor off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 7 (mechanical system not responding): by the standard, the mechanism does not respond to the command; by Renault data, a fault in the pneumatic circuit of the rear axle. Check the leaks at the module inlet and outlet with soapy water.",
            "Check the rear circuit lines for kinks and contamination, then the exhaust at the valve and the module.",
            "Compare the rear circuit pressure with the front one: a large gap points to a leak in one of the circuits.",
            "Clear the code and check the circuit pressure under load.",
        ],
        "причины": [
            "Air leak in the rear circuit or at the fittings.",
            "Contaminated rear circuit module valve.",
            "Faulty pressure regulation module.",
            "Kinked rear circuit line.",
        ],
    },

    1127: {
        "узел": "Boost pressure of turbocharger 1, after the turbocharger. The ECU compares it with the target set by the pedal position and the engine speed. On KAMAZ-5490 data the code is about a boost pressure error on acceleration, MR2 14259.",
        "нормы": [
            ("Boost pressure on acceleration under load", "per the manufacturer's manual"),
            ("Boost pressure at idle", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1 (below normal, most serious): by the standard, the pressure is below normal; by KAMAZ data, a boost pressure error on acceleration. Check the air filter and the air lines from the turbocharger to the throttle.",
            "Check the turbocharger wastegate valve and its actuator: a stuck valve stops the boost from rising.",
            "Measure the boost pressure with a mechanical gauge on acceleration and compare with the sensor.",
            "Check the charge air hoses after the turbocharger for leaks: an air leak causes a pressure drop.",
        ],
        "причины": [
            "Leak in the hoses after the turbocharger.",
            "Stuck wastegate valve or its actuator.",
            "Blocked air filter.",
            "Turbocharger wear.",
        ],
    },

    1194: {
        "узел": "Anti-theft key indicator: the presence of the encryption key of the anti-theft system. The VECU checks whether the anti-theft function is fitted and validated. On Renault data the code is about wrong parameterization: the function is present but not validated.",
        "нормы": [
            ("Anti-theft parameter in the unit", "matches the fitted equipment"),
            ("Voltage at the unit in operation", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 13 (calibration altered): by the standard, calibration or setup is disturbed; by Renault data, wrong parameterization. Check whether the anti-theft equipment is fitted on the truck and whether that matches the unit parameters.",
            "Restore the anti-theft function with the diagnostic PC, or remove the transmit block if no equipment is fitted.",
            "Check the key connector and the wire to the unit for an open circuit and corrosion.",
            "Clear the code and check the engine start with the normal key.",
        ],
        "причины": [
            "Anti-theft function enabled in the parameters, but no equipment fitted.",
            "Equipment fitted, but the parameter is off.",
            "Corroded transmit block connector.",
            "Faulty VECU unit.",
        ],
    },

    1237: {
        "узел": "Engine stop cancel switch. The driver holds it to cancel the automatic engine stop. On Mercedes-Benz data the code is written when the switch is held for more than 5 seconds, and the switch is shorted to ground.",
        "нормы": [
            ("Holding the switch", "the code is written only when held for more than 5 seconds"),
            ("Switch resistance with the button released", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 4 (below normal or short to ground): unplug the switch connector and check the signal wire for a short to ground with ignition off. A short to ground is the wire or the switch.",
            "If the code clears after unplugging, look for a short in the harness on the way to the switch.",
            "If the code stays, replace the switch and check its operation without long holding.",
            "Clear the code and test the stop cancel on the road without holding the button for long.",
        ],
        "причины": [
            "Stuck or broken switch.",
            "Wire shorted to ground in the harness.",
            "Corroded connector on the panel.",
            "Driver holding the button for a long time.",
        ],
    },

    1238: {
        "узел": "ASR disable switch. The driver uses it to turn off ASR, for example for off-road driving. On International data the code is about a fault in the off-road mode switch.",
        "нормы": [
            ("Switch state in both positions", "the contact changes cleanly"),
            ("Signal voltage with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): toggle the switch with the truck standing still and watch the ASR state in diagnostics. No change or an unstable change — the switch.",
            "Check the switch connector for corrosion and an open signal wire.",
            "Check which mode the panel shows: if the indicator and the unit disagree, look for a fault in the wiring.",
            "Clear the code and test the mode change on the road.",
        ],
        "причины": [
            "Worn switch contacts.",
            "Corroded connector on the panel.",
            "Open signal wire.",
            "Wrong ASR unit parameters.",
        ],
    },

    1239: {
        "узел": "Fuel leak on the low-pressure circuit: fuel leaks away, and the pump cannot build the required pressure. On Isuzu data this is code P0087, the pump does not build pressure because of a leak.",
        "нормы": [
            ("Fuel supply pressure during cranking", "per the manufacturer's manual"),
            ("Fuel leak in the return line", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1 (below normal, most serious): by the standard, the pressure is below normal; by Isuzu data, the pump does not build pressure because of a leak. Check all low-pressure connections and the filter for seepage.",
            "Measure the supply pressure with a gauge at the filter fitting. Low pressure with a good pump means a leak.",
            "Check the return line: if more fuel returns than normal, look for a leak at the injectors or the pipes.",
            "Check the priming pump and its seals.",
        ],
        "причины": [
            "Seepage at the low-pressure connections.",
            "Cracked or loosely tightened fitting.",
            "Leak in the injector return line.",
            "Worn priming pump.",
        ],
    },

    1240: {
        "узел": "Second fuel leak point: the low-pressure circuit after the priming pump. On Isuzu data this is code P1093, the pump does not build pressure because of a leak at another point of the circuit.",
        "нормы": [
            ("Fuel supply pressure after the priming pump", "per the manufacturer's manual"),
            ("Fuel leak in the circuit at standstill", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1 (below normal, most serious): by the standard, the pressure is below normal; by Isuzu data, a leak on the pump path. Check the connections after the priming pump and the high-pressure pipe for seepage.",
            "Measure the pressure after the priming pump. A low value with a good pump means a leak between the pump and the rail.",
            "Check the relief valve and its seals: leaking at the valve causes a pressure loss.",
            "Clear the code and check the pressure with the engine warm.",
        ],
        "причины": [
            "Seepage at the fittings after the priming pump.",
            "Faulty relief valve.",
            "Crack in the fuel pipe.",
            "Worn pump seals.",
        ],
    },

    1348: {
        "узел": "Electrovalve of fuel pump 2 in the fuel system: it controls the fuel supply to the pump. On Renault data the code is about an open circuit or a short on the electrovalve.",
        "нормы": [
            ("Electrovalve coil resistance", "per the manufacturer's manual"),
            ("Electrovalve voltage with ignition on", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 4 (below normal or short to ground): by the standard, the voltage is below normal or shorted to ground; by Renault data, an open circuit or a short of the electrovalve circuit. Unplug the valve connector and check the coil for continuity.",
            "Check the wires from the ECU to the valve with ignition off for an open circuit or a short to ground in the harness.",
            "If the code clears after unplugging the valve, look for a short in the valve; if it stays, in the harness.",
            "Check the electrovalve itself: the coil must have the resistance from the manual, and the valve should click when power is applied.",
        ],
        "причины": [
            "Open or shorted wire to the valve.",
            "Corroded valve connector.",
            "Shorted electrovalve coil.",
            "Valve stuck from fuel contamination.",
        ],
    },

    1439: {
        "узел": "Red EBS warning lamp on the panel: it shows a fault in the brake pressure system. On International data the code is about a fault in the brake pressure lamp.",
        "нормы": [
            ("Lamp with ignition on before starting", "lit, goes out after the start"),
            ("Lamp voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): by the standard, an open circuit or low current; by International data, a fault in the brake pressure lamp. Check the lamp on the panel: it should light up when ignition is switched on.",
            "If the lamp does not light, check the fuse and the lamp wire with ignition off.",
            "Check the brake circuit pressure with a gauge: the lamp should reflect the real pressure.",
            "Clear the code and check the lamp after switching the ignition on again.",
        ],
        "причины": [
            "Burnt-out lamp on the panel.",
            "Open wire to the lamp.",
            "Faulty indicator circuit fuse.",
            "Low pressure in the brake circuit.",
        ],
    },

    1482: {
        "узел": "Address of the gearbox control unit on the J1939 bus. This unit sends the gearbox mode in the TC1 message. On Mercedes-Benz data the code is about the TC1 message not arriving on J1939.",
        "нормы": [
            ("TC1 message on the bus with the engine running", "arrives regularly"),
            ("Gearbox unit supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (no J1939 message): check in diagnostics whether the gearbox unit sends messages on the bus. If not, look at the supply and the CAN connector on the unit.",
            "Check the power and ground of the gearbox unit with ignition off and on.",
            "Check the CAN bus resistance: about 60 ohm with power off.",
            "Clear the code and check whether the TC1 message appears at start.",
        ],
        "причины": [
            "Loss of power to the gearbox unit.",
            "Open or corroded CAN connector.",
            "Faulty gearbox unit.",
            "Wrong unit address on the bus.",
        ],
    },

    1552: {
        "узел": "Cab climate control input on the panel: the buttons and knobs the driver uses to set the temperature and the airflow. On International data the code is about a fault in the temperature blend on the control panel.",
        "нормы": [
            ("Blend flap position at the end position of the knob", "per the manufacturer's manual"),
            ("Panel signal voltage with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): turn the temperature knob and watch in diagnostics whether the blend position changes. No change or jumps — the panel or the actuator.",
            "Check the panel connector for corrosion and an open signal wire with ignition off.",
            "Check the blend flap actuator: when the knob turns, it should move without sticking.",
            "Clear the code and check the climate control at all knob positions.",
        ],
        "причины": [
            "Worn potentiometer on the panel.",
            "Corroded panel connector.",
            "Sticking blend flap actuator.",
            "Open signal wire.",
        ],
    },

    1681: {
        "узел": "Hold state of the main battery switch: with the key off, the unit checks that the battery master switch holds the circuit. On Mercedes-Benz data the code is about no BM message (battery master switch) on J1939.",
        "нормы": [
            ("BM message on the bus with the switch on", "arrives regularly"),
            ("Voltage at the unit with the battery master switch on", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (no J1939 message): check whether the master switch unit sends messages on the bus. If not, look at its supply and connector.",
            "Check the master switch itself: when switched on, there should be a click and a change of state in diagnostics.",
            "Check the switch unit connector and its ground for corrosion.",
            "Clear the code and check the message with the switch on and off.",
        ],
        "причины": [
            "Loss of power to the master switch unit.",
            "Corroded unit connector.",
            "Faulty main battery switch.",
            "Open CAN bus wire.",
        ],
    },

    1747: {
        "узел": "Request for the lowering mode of the air suspension (kneeling) from the cab. The driver lowers the suspension for loading. On International data the code is about a fault in the air suspension reset switch, that is the mode request switch.",
        "нормы": [
            ("Switch state in both positions", "the contact changes cleanly"),
            ("Signal voltage with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): press the switch several times and watch the request state. No change — the switch.",
            "Check the switch connector for corrosion and an open signal wire.",
            "Check the suspension valves: on request the suspension should lower, otherwise look for a faulty valve.",
            "Clear the code and test the lowering mode at standstill.",
        ],
        "причины": [
            "Worn switch contacts.",
            "Corrosion at the connector in the cab.",
            "Open signal wire.",
            "Faulty air suspension valve.",
        ],
    },

    1792: {
        "узел": "Trailer ABS signal on the tractor: the tractor shows the driver that the trailer ABS is faulty. On International data the code is about a fault in the trailer ABS lamp.",
        "нормы": [
            ("Trailer ABS lamp with ignition on", "lit, goes out after the check"),
            ("Lamp voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): by the standard, an open circuit or low current; by International data, a fault in the trailer ABS lamp. Check the lamp on the tractor panel.",
            "Check the trailer plug connector and the trailer ABS contact with ignition off.",
            "Check the signal from the trailer ABS unit: if the signal is there but the lamp stays off, look at the lamp wiring.",
            "Clear the code and check the lamp at start.",
        ],
        "причины": [
            "Burnt-out lamp on the panel.",
            "Corroded trailer plug contacts.",
            "Open trailer ABS signal wire.",
            "Faulty trailer ABS unit.",
        ],
    },

    1793: {
        "узел": "ATC/ASR information signal: a lamp on the panel shows whether the traction control is working or faulty. On International data the code is about a fault in the traction control lamp.",
        "нормы": [
            ("ASR lamp with ignition on", "lit, goes out after the check"),
            ("Lamp voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 5 (current below normal or open circuit): by the standard, an open circuit or low current; by International data, a fault in the ASR lamp. Check the lamp on the panel when the ignition is switched on.",
            "If the lamp does not light up at switch-on, check the fuse and the lamp wire.",
            "Check the ASR unit in diagnostics: if the unit shows an error, the lamp only reflects it.",
            "Clear the code and check the lamp after start.",
        ],
        "причины": [
            "Burnt-out lamp on the panel.",
            "Open wire to the lamp.",
            "Faulty circuit fuse.",
            "Fault in the ASR unit.",
        ],
    },

    1837: {
        "узел": "Convoy headlight selection: in blackout mode the ECU turns on the headlights at reduced power. On International data the code is about excess headlight current in the blackout mode.",
        "нормы": [
            ("Headlight current with the convoy mode on", "per the manufacturer's manual"),
            ("Headlight current with the mode off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 6 (current above normal or short to ground): by the standard, current above normal or a short to ground; by International data, excess current of the headlights in the blackout mode. Check the headlight fuse and relay.",
            "Turn the convoy mode off and see if the code clears: if it does, look for a short in the mode circuit.",
            "Check the headlight harness and connectors for a short to ground with ignition off.",
            "Check the headlights themselves: an overheated or stuck element draws current above normal.",
        ],
        "причины": [
            "Short to ground in the headlight harness.",
            "Faulty headlight element.",
            "Overloaded fuse or relay.",
            "Corroded headlight connector.",
        ],
    },

    1841: {
        "узел": "Stop lamp selection in blackout mode: in this mode the stop lamp lights at reduced brightness. On International data the code is about excess stop lamp current.",
        "нормы": [
            ("Stop lamp current with the brake pressed", "per the manufacturer's manual"),
            ("Stop lamp current with the brake released", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 6 (current above normal or short to ground): by the standard, current above normal or a short to ground; by International data, excess stop lamp current. Check the stop lamp fuse.",
            "Turn the blackout mode off and see if the code clears.",
            "Check the stop lamp harness and the trailer plug for a short to ground.",
            "Check the stop lamps themselves: a burnt or shorted lamp draws too much current.",
        ],
        "причины": [
            "Short to ground in the stop lamp harness.",
            "Faulty stop lamp.",
            "Overloaded stop lamp fuse.",
            "Corroded trailer connector.",
        ],
    },

    2017: {
        "узел": "Address 17 on the J1939 bus: messages from the cruise control unit arrive from it. On Mercedes-Benz data the code is about no messages from address 17, so the cruise control unit does not respond.",
        "нормы": [
            ("Messages from address 17 on the bus in operation", "arrive regularly"),
            ("Cruise control unit supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (no J1939 message): check in diagnostics which addresses are silent. If only address 17 is silent, look at the cruise control unit or its connector.",
            "Check the power and ground of the cruise control unit with ignition off and on.",
            "Check the CAN connector on the unit and the bus resistance: about 60 ohm.",
            "Clear the code and check whether the messages appear at start.",
        ],
        "причины": [
            "Loss of power to the cruise control unit.",
            "Open or corroded CAN connector.",
            "Faulty cruise control unit.",
            "Address conflict on the bus.",
        ],
    },

    2033: {
        "узел": "Address 33 on the bus: the data of the ESC (electronic stability control) unit comes from it. On International data the code is about losing the data bus to the ESC unit, so the link to the unit has dropped.",
        "нормы": [
            ("ESC unit messages on the bus in operation", "arrive regularly"),
            ("CAN bus resistance with power off", "about 60 ohm"),
        ],
        "шаги": [
            "FMI 9 (no J1939 message): check whether the ESC unit sends messages on the bus. If not, look at its supply and connector.",
            "Check the CAN bus resistance between CAN-H and CAN-L: about 60 ohm with power off.",
            "Check the ESC unit connector for corrosion and an open circuit.",
            "Clear the code and check the link to the unit with the engine running.",
        ],
        "причины": [
            "Open or corroded ESC unit connector.",
            "Loss of power to the ESC unit.",
            "Chafed CAN bus wire.",
            "Faulty ESC unit.",
        ],
    },

    2236: {
        "узел": "Address 236 on the bus: the driver door module. It sends the state of the door and the lock to the bus. On International data the code is about a communication fault of the driver door module on the data bus.",
        "нормы": [
            ("Door module messages on the bus", "arrive regularly"),
            ("Door module supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (no J1939 message): check whether messages stop only from address 236. If so, look at the driver door module.",
            "Check the door module connector for corrosion and water in the connector: the door harness often gets wet.",
            "Check the power and ground of the door module with ignition off.",
            "Check the CAN bus on the way to the door: rubber seals and kinks at the hinges.",
        ],
        "причины": [
            "Water or corrosion in the door connector.",
            "Chafed wire in the door harness.",
            "Faulty driver door module.",
            "Loss of power to the module.",
        ],
    },

    2361: {
        "узел": "Rear work lights command of the tractor: the panel switch turns on the rear work lights. On International data the code is about a fault in the work light switch.",
        "нормы": [
            ("Switch state in both positions", "the contact changes cleanly"),
            ("Current of the rear work lights when on", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): turn the switch on and off and watch the command state in diagnostics. No change — the switch.",
            "Check the switch connector for corrosion and an open signal wire.",
            "Check whether the rear work lights come on when the command is given. If not, look at the relay and the fuse.",
            "Clear the code and check the command at standstill.",
        ],
        "причины": [
            "Worn switch contacts.",
            "Corrosion at the panel connector.",
            "Open signal wire.",
            "Faulty work light relay.",
        ],
    },

    2387: {
        "узел": "Front fog light command of the tractor: the panel switch turns on the front fog lights. On International data the code is about a switch fault.",
        "нормы": [
            ("Switch state in both positions", "the contact changes cleanly"),
            ("Fog light current when on", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): turn the switch on several times and watch the command state. Unstable — the switch.",
            "Check the switch connector and the signal wire for corrosion and an open circuit.",
            "Check the fog light relay and the fuse if the lights do not come on with the command.",
            "Clear the code and check the lights at standstill.",
        ],
        "причины": [
            "Worn switch contacts.",
            "Corrosion at the panel connector.",
            "Open signal wire.",
            "Faulty light relay.",
        ],
    },

    2436: {
        "узел": "Average AC frequency of the alternator: the ECU calculates the alternator speed from its AC output. On KAMAZ-5490 data the code is about the alternator speed signal dropping out, MR2 12712.",
        "нормы": [
            ("AC frequency at mid speed", "per the manufacturer's manual"),
            ("Speed signal with the engine running", "steady, with no drop-outs"),
        ],
        "шаги": [
            "FMI 9 (abnormal update rate): by the standard, the data arrives at an irregular rate; by KAMAZ data, the alternator speed signal drops out. Check the alternator connector and the speed signal wire.",
            "Check the alternator drive belt: slipping gives an unstable frequency.",
            "Measure the voltage at the alternator terminals with the engine running: if the voltage drops together with the signal, look for a common open circuit.",
            "Clear the code and check the signal at mid and high speed.",
        ],
        "причины": [
            "Corroded alternator connector.",
            "Open speed signal wire.",
            "Faulty alternator.",
            "Slipping drive belt.",
        ],
    },

    2796: {
        "узел": "Transfer case switch on the panel: the driver selects whether the front axle works and shifts the transfer case. On International data the code is about a fault in the front axle switch.",
        "нормы": [
            ("Switch state in both positions", "the contact changes cleanly"),
            ("Signal voltage with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): shift the switch with the truck standing still and watch the front axle state in diagnostics. No change — the switch.",
            "Check the switch connector for corrosion and an open wire.",
            "Check the position of the front axle actuator: when switched on there should be a click or a change of position.",
            "Clear the code and check the shifting at standstill.",
        ],
        "причины": [
            "Worn switch contacts.",
            "Corrosion at the panel connector.",
            "Open signal wire.",
            "Faulty front axle actuator.",
        ],
    },

    3187: {
        "узел": "LIN line to the gear selector console: along it the console sends the gear selection commands to the gearbox unit. On Mercedes-Benz data the code is about a fault in the LIN line to the console.",
        "нормы": [
            ("LIN signal at the console with ignition on", "steady, with no drop-outs"),
            ("Console supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (abnormal update rate): by the standard, the data arrives at an irregular rate; by Mercedes-Benz data, a fault in the LIN line. Check the connector of the gear selector console for corrosion and water.",
            "Check the power and ground of the console with ignition off and on.",
            "Check the LIN wire for an open circuit and a short to ground or positive with ignition off.",
            "Clear the code and check the transmission from the console at standstill.",
        ],
        "причины": [
            "Corroded or flooded console connector.",
            "Open or shorted LIN wire.",
            "Faulty gear selector console.",
            "Loss of power to the console.",
        ],
    },

    3219: {
        "узел": "NOx sensor at the inlet of the SCR catalyst (SCR 1). It works only at operating temperature, and the ECU waits for it before dosing. On KAMAZ-5490 data the code is about the NOx sensor not reaching operating temperature, MR2 12823.",
        "нормы": [
            ("NOx sensor temperature during warm-up", "per the manufacturer's manual"),
            ("Sensor warm-up time from a cold start", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1 (below normal, most serious): by the standard, the value is below normal; by KAMAZ data, the NOx sensor has not reached operating temperature. Check the sensor heater and its supply with ignition off.",
            "Check the NOx sensor connector for corrosion and water: moisture at a hot sensor often gives a poor warm-up.",
            "Check the exhaust temperature: if the exhaust does not warm up, look for the problem in the engine, not the sensor.",
            "Clear the code and check the sensor warm-up after a cold start.",
        ],
        "причины": [
            "Faulty NOx sensor heater.",
            "Corrosion or moisture in the sensor connector.",
            "Open wire to the heater supply.",
            "Cold exhaust because of an engine fault.",
        ],
    },

    3220: {
        "узел": "NOx reading at the SCR inlet (SCR 1): the ECU gets the NOx concentration from the sensor over the CAN bus. On KAMAZ-5490 data the code is about the NOx concentration message disappearing, MR2 12804.",
        "нормы": [
            ("NOx message on the bus with the engine running", "arrives regularly"),
            ("NOx sensor supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (abnormal update rate): by the standard, the data arrives at an irregular rate; by KAMAZ data, the NOx message on CAN has disappeared. Check whether other messages from the same unit are on the bus.",
            "Check the power and ground of the NOx sensor unit with ignition off and on.",
            "Check the CAN connector on the NOx unit and the bus resistance with power off.",
            "Clear the code and check the message after the engine starts.",
        ],
        "причины": [
            "Loss of power to the NOx sensor unit.",
            "Open or corroded CAN connector.",
            "Faulty NOx sensor unit.",
            "Interference on the bus from a high-power consumer.",
        ],
    },

    3228: {
        "узел": "Power supply of the NOx sensor at the outlet of the SCR catalyst (SCR 1). The sensor gets its power from the ECU, and without it the readings do not come. On Dongfeng data the code is about a fault in the NOx sensor power supply.",
        "нормы": [
            ("NOx sensor supply voltage with ignition on", "per the manufacturer's manual"),
            ("Sensor supply current in operation", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): by the standard, the data is unreliable; by Dongfeng data, a fault in the NOx sensor power supply. Measure the supply voltage at the sensor connector with ignition on.",
            "Check the fuse and the relay of the NOx sensor supply.",
            "Check the supply and ground wires of the sensor for an open circuit and a short.",
            "Clear the code and check the supply after the engine starts.",
        ],
        "причины": [
            "Burnt-out sensor supply fuse.",
            "Open or corroded supply wires.",
            "Faulty supply relay.",
            "Faulty NOx sensor.",
        ],
    },

    3246: {
        "узел": "Gas temperature at the outlet of the diesel particulate filter (DPF, SCR 1): the ECU uses it to tell whether the filter regeneration is running. On KAMAZ-5490 data the code is about the filter not reaching the required temperature, MR2 14238.",
        "нормы": [
            ("DPF outlet temperature during regeneration", "per the manufacturer's manual"),
            ("DPF outlet temperature in normal operation", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 1 (below normal, most serious): by the standard, the value is below normal; by KAMAZ data, the required filter temperature has not been reached. Check whether the regeneration starts and how long it runs.",
            "Check the DPF outlet temperature sensor: if it is open, the ECU sees a cold filter.",
            "Check the fuel supply for regeneration and the operation of the injector or the doser.",
            "Check the filter itself for blockage: a clogged filter does not heat up properly.",
        ],
        "причины": [
            "Faulty DPF temperature sensor.",
            "Faulty fuel supply for regeneration.",
            "Blocked particulate filter.",
            "Engine running short trips and never reaching operating mode.",
        ],
    },

    3314: {
        "узел": "Fifth wheel coupling control: the driver uncouples the semi-trailer with a button or a lever. The ECU checks that the jaws are in the required state. On International data the code is about an invalid state of the jaw release switch.",
        "нормы": [
            ("Jaw switch state in both positions", "the contact changes cleanly"),
            ("Signal voltage with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): check the state of the jaw switch with the semi-trailer removed and fitted. If the state does not match the jaw position, it is the switch or its adjustment.",
            "Inspect the fifth wheel jaws: with ignition off, check that they sit fully and without gaps.",
            "Check the jaw switch connector and the signal wire for an open circuit.",
            "Clear the code and check the uncoupling at standstill without the semi-trailer.",
        ],
        "причины": [
            "Jaw switch not adjusted or worn.",
            "Dirt on the fifth wheel stopping the jaws from closing fully.",
            "Corroded switch connector.",
            "Open signal wire.",
        ],
    },

    3353: {
        "узел": "D+ terminal of the alternator: the alternator tells the ECU through it that the batteries are charging. On Mercedes-Benz data the code is about a fault on the D+ terminal and no charge signal.",
        "нормы": [
            ("D+ voltage with the engine running", "close to the on-board voltage"),
            ("D+ voltage with the engine off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): measure the voltage at the D+ terminal with the engine running. No signal or a jumping signal — the wire or the terminal.",
            "Check the D+ terminal on the alternator and the regulator connector for corrosion.",
            "Check the D+ wire for an open circuit with ignition off.",
            "Check the voltage regulator: if the on-board voltage is normal but D+ drops out, look for an open circuit in the wire.",
        ],
        "причины": [
            "Corroded or loose D+ terminal.",
            "Open D+ wire.",
            "Faulty voltage regulator.",
            "Worn alternator brushes.",
        ],
    },

    3362: {
        "узел": "Inlet lines of the AdBlue dosing unit (SCR 1): along them the urea goes from the tank to the doser. On Dongfeng data the code is about an external fault of the SCR dosing module.",
        "нормы": [
            ("AdBlue pressure in the line with the doser running", "per the manufacturer's manual"),
            ("Line temperature in operation", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 31 (condition exists): by the standard, the condition is present, see the manufacturer's description; by Dongfeng data, an external fault of the SCR dosing module. Check the lines for kinks, leaks and urea crystallisation.",
            "Check the urea line heating at a cold start: frozen urea gives a dosing error.",
            "Check the urea filter and the pump for blockage.",
            "Clear the code and check the urea supply with the engine warm.",
        ],
        "причины": [
            "Urea crystallisation in the line.",
            "Kinked or chafed AdBlue line.",
            "Blocked urea filter.",
            "Faulty line heating.",
        ],
    },

    3412: {
        "узел": "Door lock status 1 (driver's door): the lock motor reports the lock position. On International data the code is about a failure of the driver's door lock motor.",
        "нормы": [
            ("Lock motor on the open and close command", "responds without delay, with a click"),
            ("Motor voltage on the command", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 7 (mechanical system not responding): by the standard, the mechanism does not respond to the command; by International data, a failure of the driver's door lock motor. Open and close the door with the button a few times and listen to the motor.",
            "Check the lock motor connector for corrosion and water: water in the door often kills the motor.",
            "Check the lock mechanism: if the rod sticks, the motor cannot cope.",
            "Clear the code and check the lock after repair.",
        ],
        "причины": [
            "Water in the door and corrosion in the connector.",
            "Sticking rod or lock mechanism.",
            "Worn or failed lock motor.",
            "Open motor wire.",
        ],
    },

    3418: {
        "узел": "Door lock status 3 (rear door on the driver's side): the lock motor reports the lock position. On International data the code is about a failure of the rear driver-side door lock motor.",
        "нормы": [
            ("Lock motor on the open and close command", "responds without delay, with a click"),
            ("Motor voltage on the command", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 7 (mechanical system not responding): by the standard, the mechanism does not respond to the command; by International data, a failure of the rear driver-side door lock motor. Check the motor with the command from the button.",
            "Check the flexible harness of the rear door: it chafes at every opening.",
            "Check the motor connector for corrosion and water.",
            "Clear the code and check the locks on all doors after repair.",
        ],
        "причины": [
            "Chafed flexible harness of the rear door.",
            "Water and corrosion in the connector.",
            "Failed lock motor.",
            "Sticking lock mechanism on the rear door.",
        ],
    },

    3452: {
        "узел": "PTO enable switch from input shaft 1 of the gearbox. The driver enables power take-off from this shaft. On International data the code is about a fault in the KOM A switch and the KOM engage switch.",
        "нормы": [
            ("Switch state in both positions", "the contact changes cleanly"),
            ("Signal voltage with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): by International data there are two lines here, the KOM A switch and the KOM engage switch. Toggle the switch and see which of the two changes.",
            "Check the switch connector and the signal wire for corrosion and an open circuit with ignition off.",
            "Check whether the power take-off itself works: if the drive does not respond, the problem is in the drive.",
            "Clear the code and check the enable at standstill.",
        ],
        "причины": [
            "Worn KOM A switch contacts.",
            "Corrosion at the panel connector.",
            "Open signal wire.",
            "Faulty power take-off drive.",
        ],
    },

    3453: {
        "узел": "PTO enable switch from input shaft 2 of the gearbox. The driver enables power take-off from another input shaft. On International data the code is about a fault in the KOM B switch.",
        "нормы": [
            ("Switch state in both positions", "the contact changes cleanly"),
            ("Signal voltage with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): toggle the KOM B switch with the truck standing still and watch the state in diagnostics. No change — the switch.",
            "Check the switch connector and the signal wire for an open circuit and a short to ground.",
            "Compare with the KOM A switch: if that one works, the problem is in this specific switch, not in the common supply.",
            "Clear the code and check the enable at standstill.",
        ],
        "причины": [
            "Worn KOM B switch.",
            "Corrosion at the connector.",
            "Open signal wire.",
            "Faulty KOM unit.",
        ],
    },

    3455: {
        "узел": "PTO enable switch from the transfer case output shaft. The driver enables power take-off from the transfer case. On International data the codes are about a fault in the transfer case switch and the KOM switch.",
        "нормы": [
            ("Switch state in both positions", "the contact changes cleanly"),
            ("Signal voltage with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): by International data there are two lines here, the transfer case switch and the KOM switch. Toggle the switch with the truck standing still and see which line changes.",
            "Check the switch connector and the signal wire for corrosion and an open circuit.",
            "Check the transfer case position: if the case is in the right position but the signal is missing, look at the switch.",
            "Clear the code and check the enable at standstill.",
        ],
        "причины": [
            "Worn transfer case switch.",
            "Corrosion at the connector.",
            "Open signal wire.",
            "Wrong transfer case position.",
        ],
    },

    3520: {
        "узел": "Preliminary FMI of AdBlue properties (SCR 1): the ECU assesses the urea quality from the tank sensor signal. On KAMAZ-5490 data the code is about poor urea quality, MR2 14235.",
        "нормы": [
            ("Urea concentration from the tank sensor", "per the manufacturer's manual"),
            ("Urea shelf life", "per the label on the container"),
        ],
        "шаги": [
            "FMI 18 (below normal, medium urgency): by the standard, the value is below normal; by KAMAZ data, poor urea quality. Take a urea sample and measure its concentration.",
            "Check the shelf life and the storage conditions: urea loses quality in frost or in heat.",
            "Check the tank and the filler neck for contamination: another liquid gives the same code.",
            "Clear the code and check the quality after refilling with proper urea.",
        ],
        "причины": [
            "Poor-quality or expired urea.",
            "Contaminated AdBlue tank.",
            "Faulty quality sensor in the tank.",
            "Filled with the wrong fluid.",
        ],
    },

    3645: {
        "узел": "Transfer case (TCI): the unit on the J1939 bus sends the state of the transfer case and the all-wheel drive mode. On Mercedes-Benz data the code is about no message from the transfer case.",
        "нормы": [
            ("TCI message on the bus in operation", "arrives regularly"),
            ("Transfer case unit supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 9 (no J1939 message): check whether the transfer case unit sends messages on the bus. If not, look at its supply and connector.",
            "Check the power and ground of the transfer case unit with ignition off and on.",
            "Check the CAN connector on the unit and the bus resistance: about 60 ohm.",
            "Clear the code and check the message at engine start.",
        ],
        "причины": [
            "Loss of power to the transfer case unit.",
            "Open or corroded CAN connector.",
            "Faulty transfer case unit.",
            "Wrong unit address on the bus.",
        ],
    },

    3695: {
        "узел": "DPF regeneration block switch: the driver blocks regeneration, for example in a garage or near people. On International data the code is about a switch fault.",
        "нормы": [
            ("Switch state in both positions", "the contact changes cleanly"),
            ("Signal voltage with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): toggle the switch and watch the regeneration block state. No change — the switch.",
            "Check the switch connector for corrosion and an open signal wire.",
            "Check whether regeneration starts after the block is removed: if not, look at the regeneration control unit.",
            "Clear the code and check regeneration at standstill with the engine warm.",
        ],
        "причины": [
            "Worn switch contacts.",
            "Corrosion at the panel connector.",
            "Open signal wire.",
            "Switch stuck in the block position.",
        ],
    },

    4000: {
        "узел": "Engine brake enable switch on the panel: the driver enables the engine brake and the retarder. On International data the code is about a fault in the switch that engages the retarder and the auxiliary braking.",
        "нормы": [
            ("Switch state in both positions", "the contact changes cleanly"),
            ("Signal voltage with ignition off", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): toggle the switch several times and watch the state in diagnostics. Unstable — the switch.",
            "Check the switch connector and the signal wire for an open circuit with ignition off.",
            "Check the engine brake operation with the enable on: if it does not engage, look at the unit.",
            "Clear the code and check the operation at standstill.",
        ],
        "причины": [
            "Worn switch.",
            "Corrosion at the connector.",
            "Open signal wire.",
            "Faulty engine brake unit.",
        ],
    },

    4213: {
        "узел": "Crankshaft rotation check: diagnostics turns the engine with the starter without fuel injection to check the mechanics. On KAMAZ-5490 data the code is about engine cranking without fuel injection, MR2 14275.",
        "нормы": [
            ("Speed during starter cranking", "per the manufacturer's manual"),
            ("Oil pressure during cranking", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 7 (mechanical system not responding): by the standard, the mechanism does not respond; by KAMAZ data, the cranking check without injection did not pass. Check that the engine cranks evenly with the starter, without jerks.",
            "Check the oil level and pressure: without pressure the engine does not turn over properly.",
            "Check the starter and the batteries: a weak starter cranks unevenly.",
            "Clear the code and repeat the check with the engine warm.",
        ],
        "причины": [
            "Mechanical seizure in the engine.",
            "Weak starter or batteries.",
            "Low oil pressure.",
            "Fault in the diagnostic check itself.",
        ],
    },

    4332: {
        "узел": "SCR system state (SCR 1): the general self-diagnosis of the dosing control unit. On KAMAZ-5490 data the code is about an internal fault of the SCR control unit, MR2 16293.",
        "нормы": [
            ("SCR unit with ignition on", "passes the self-test without errors"),
            ("SCR unit supply voltage", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 12 (faulty device): by the standard, a fault in the device or component; by KAMAZ data, an internal error of the SCR control unit. Check the power supply of the unit and its ground.",
            "Check the SCR unit connectors for corrosion and water.",
            "Clear the code and check the unit self-test with ignition on.",
            "If the code stays, replace the SCR control unit after checking all wires.",
        ],
        "причины": [
            "Loss of power or ground to the SCR unit.",
            "Corrosion or water in the unit connectors.",
            "Faulty SCR control unit.",
            "Interference from neighbouring units.",
        ],
    },

    5285: {
        "узел": "Charge air cooler (intercooler) efficiency. On Sitrak data the code is about insufficient cooler efficiency, scanner code P026A. Torque limitation is possible.",
        "нормы": [
            ("Air temperature before and after the cooler under load", "per the manufacturer's manual"),
            ("Temperature difference across the cooler", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 2 (data unreliable): by Sitrak data, insufficient cooler efficiency. Inspect the cooler for dirt, leaves and damage to the fins.",
            "Measure the air temperature before and after the cooler under load. A weak difference points to a blockage or a leak.",
            "Check the boost hoses for leaks: a leak after the cooler reduces efficiency.",
            "Clear the code and check the operation under load.",
        ],
        "причины": [
            "Dirty charge air cooler.",
            "Leak in the hoses after the cooler.",
            "Damaged cooler fins.",
            "Faulty boost temperature sensor.",
        ],
    },

    5392: {
        "узел": "Loss of prime of the AdBlue dosing unit (SCR 1): the dosing module does not build the required urea pressure at start. On DAF data the code is about module B494 and low AdBlue pressure at start over a long period.",
        "нормы": [
            ("AdBlue pressure at engine start", "per the manufacturer's manual"),
            ("Time to build pressure at a cold start", "per the manufacturer's manual"),
        ],
        "шаги": [
            "FMI 31 (condition exists): by the standard, the condition is present, see the manufacturer's description; by DAF data, module B494 gives low AdBlue pressure at start. Check the lines and the urea filter for blockage and air.",
            "Check the urea level in the tank and the absence of air in the line: an air lock stops the pressure from building.",
            "Check the line heating and the tank at a cold start: frozen urea does not flow.",
            "Clear the code and repeat the engine start.",
        ],
        "причины": [
            "Air in the AdBlue line.",
            "Blocked urea filter.",
            "Frozen or crystallised urea.",
            "Faulty dosing module B494.",
        ],
    },
}
