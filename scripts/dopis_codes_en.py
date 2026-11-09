# -*- coding: utf-8 -*-
# Dopisyvanie 09.11.2026: English texts for code pages. Key 'code-en:<SPN>'
# ('code-en:97+' is added after the existing 'code-en:97' blocks).
# Read by build_en_pages.py (bp.extra_html / bp.extra_faq).

BLOCKS = {

'code-en:97+': {'tail': [
    (u'Reading SPN 97 by FMI', [
        u'The FMI is the half of the code that says how the water sensor is failing. These are the values people search for most, based on SAE J1939-73 and the usual Cummins listings.',
        [u'**SPN 97 FMI 15** - water detected, data valid but above normal (some engines add FMI 16 as a second, higher stage). On Cummins this is fault code 418. It lights the warning but does not by itself cut power.',
         u'**SPN 97 FMI 3** - circuit voltage above normal, or shorted high. In practice this often means an open circuit: an unplugged connector, a broken wire, or a sensor left disconnected after a filter change (Cummins code 428).',
         u'**SPN 97 FMI 4** - circuit voltage below normal, or shorted low: a wet connector, a chafed wire, a failed sensor (Cummins code 429).',
         u'**SPN 97 FMI 2** - erratic or intermittent signal: a corroded pin or a harness that moves with vibration.'],
    ]),
    (u'Step-by-step check', [
        u'1. Drain the separator into a container until clean fuel with no cloudy layer comes out. Water is heavier than diesel and sits at the bottom.',
        u'2. Clear the code and run the engine. If FMI 15 returns within a day or two, take a sample from the tank bottom into a clear jar and let it settle: a separate water layer means the tank or the supplier is the problem.',
        u'3. For FMI 3, 4 or 2, look at the sensor connector first. Green corrosion, a loose latch or a wire rubbing on the bracket are the usual findings.',
        u'4. Only then test or replace the sensor.',
        u'Water matters beyond the warning: modern high-pressure common-rail pumps rely on diesel for lubrication and water shortens their life quickly, so a repeat code is worth chasing.',
    ]),
    (u'More questions', [
        (u'What is the difference between SPN 97 FMI 3 and FMI 15?',
         u'FMI 15 means the engine computer thinks there is water. FMI 3 means the electrical circuit is open or shorted high, and there may be no water at all.'),
        (u'Will the engine derate with SPN 97 FMI 15?',
         u'Usually not on its own; it is a warning. But if water reaches the injection pump the engine can lose power, so drain it promptly.'),
    ]),
]},

'code-en:110': {'tail': [
    (u'What SPN 110 and its FMI tell you', [
        u'SPN 110 is engine coolant temperature in SAE J1939. The sensor is a thermistor in the cylinder head or the coolant outlet: its resistance falls as it gets hotter. '
        u'The engine computer uses it to switch the fan on, to derate power and, in the worst case, to shut the engine down.',
        [u'**FMI 0** - temperature above normal, most severe (Cummins SID 151). The engine is overheating: stop.',
         u'**FMI 15 and 16** - above normal, least and moderately severe. A warning first, then a power reduction.',
         u'**FMI 3** - circuit voltage high, i.e. an open circuit (Cummins 144). The computer thinks the engine is cold, so protection and fan control may be wrong.',
         u'**FMI 4** - circuit voltage low or shorted to ground (Cummins 145). The computer thinks the engine is overheating.',
         u'**FMI 2** - the reading jumps or disagrees with other data.'],
    ]),
    (u'Causes of a real overheat, most common first', [
        [u'Low coolant from a leak at the radiator, hoses, water pump or heater circuit.',
         u'The fan not engaging: a failed clutch, a drive fault or a relay.',
         u'A blocked radiator, dirty outside (insects, chaff) or scaled inside.',
         u'A thermostat stuck closed: the upper radiator hose is hot while the lower one stays cool.',
         u'A weak radiator cap, or a pump with a worn impeller.',
         u'A leaking head gasket: bubbles in the expansion tank, oil in the coolant, white smoke. This is the worst case.'],
    ]),
    (u'How to check', [
        u'1. Stop and let the engine cool before opening the cap. Check the level in the expansion tank and look for drips.',
        u'2. Compare the scan-tool temperature with reality. After a cold night it should equal the ambient temperature. If it does not, the sensor or its circuit is at fault.',
        u'3. With the engine warm, listen for the fan engaging and feel the hoses (carefully): hot upper and cold lower hose points to a closed thermostat.',
        u'4. For FMI 3 and 4, inspect the sensor connector for corrosion and test the sensor against the manual\'s resistance table.',
        u'Normal operating temperature on most diesels is roughly 80-95 C; check your engine manual for exact limits.',
    ]),
    (u'Can you keep driving?', [
        u'Not with FMI 0 or a red coolant lamp: a few minutes of overheating can warp the head. Pull over and let the engine cool. With FMI 15 or 16, find a safe place and diagnose; '
        u'driving on with a climbing gauge is how head gaskets fail. With FMI 3 or 4 the engine may be fine, but the over-temperature protection is blind, so watch the dash gauge closely.',
    ]),
    (u'Questions and answers', [
        (u'It only overheats on hills. Is that SPN 110?',
         u'The code is only the reporter. The cause is usually a radiator or fan that cannot keep up under load: check the fins, the fan clutch and the thermostat.'),
        (u'The gauge reads far too cold or too hot right after starting. Why?',
         u'That points to an open or shorted sensor circuit (FMI 3 or 4). Check the connector and wiring, then the sensor.'),
        (u'Can I top up with plain water to get home?',
         u'Only as an emergency measure to reach the nearest safe stop, and only after the engine has cooled. Plain water lowers corrosion protection and the boiling point margin.'),
    ]),
]},

'code-en:107': {'tail': [
    (u'What SPN 107 is measuring', [
        u'SPN 107 reports the pressure difference across the engine air filter. A sensor compares the pressure before and after the filter element; as dust loads the filter, the difference rises. '
        u'The engine computer uses it to warn the driver that the filter needs service.',
        [u'**FMI 15** (and 0 or 16 on some engines) - restriction above normal. The filter is blocked or the sensor reads high.',
         u'**SPN 107 FMI 15** is by far the most searched value and in most cases means exactly what it says: the element is loaded.',
         u'**FMI 3 and 4** - the sensor circuit is open or shorted high or low.',
         u'**FMI 2** - an implausible reading, for example the difference stays at zero while the engine is under load.'],
    ]),
    (u'Why it matters and how to check', [
        u'A restricted air filter starves the engine of air: black smoke, lost power, higher fuel use and, on engines with EGR or a particulate filter, more soot and more regeneration. '
        u'A commonly quoted service limit for heavy-duty diesels is about 6 kPa (25 inches of water), but engines differ, so use your manual.',
        u'1. Look at the element. Tap it gently; heavy dust, oil or a wet filter confirms the code. Check the housing seals and the intake hose for leaks and cracks: unfiltered air is worse than a clogged filter.',
        u'2. If the filter is new or clean and the code stays, check the sensor hose or port. A cracked or blocked sensing tube gives a false reading.',
        u'3. For FMI 3 and 4, inspect the sensor connector and the wiring.',
        u'4. Replace the sensor only when the filter, housing and hoses are good.',
    ]),
    (u'Can you keep driving?', [
        u'A warning at FMI 15 is not an emergency: you can reach a service point, ideally with the filter changed soon. If power is falling or the exhaust is black, do not drive hard. '
        u'The risk is dust entering the engine if the housing is damaged, not the code itself.',
    ]),
    (u'Questions and answers', [
        (u'Can I clean the filter with compressed air?',
         u'Some manufacturers allow it for dry dust with low pressure from the inside out, but paper filters are best replaced. Follow the manufacturer\'s procedure.'),
        (u'The filter is new but SPN 107 FMI 15 remains. Why?',
         u'The sensor port or hose may be blocked, the housing may not seal, or the code was stored earlier and not cleared.'),
    ]),
]},

'code-en:806': {'tail': [
    (u'What SPN 806 is', [
        u'SPN 806 is the ASR valve, differential 1. ASR is the traction-control function of the brake electronics, and this is one of the solenoid valves it drives. '
        u'In this database the number appears for Renault Trucks. The exact role of the valve depends on the brake system fitted, so use the make table above for its precise wording. The electronics check the valve coil and its wiring.',
        [u'**SPN 806 FMI 5** - current below normal or open circuit: a broken wire, a corroded pin or a failed coil. This is the most common entry.',
         u'**FMI 6** - current above normal or shorted to ground: chafed wire or wet connector.',
         u'**FMI 3 and 4** - circuit voltage high or low.',
         u'**FMI 7** - the valve is not responding mechanically.'],
    ]),
    (u'Checks', [
        u'1. Read all brake codes. If supply or ground codes appear with it, fix those first.',
        u'2. Find the valve (the make manual shows where) and look at the connector for water and corrosion.',
        u'3. Measure the coil resistance (values are in the workshop manual; a few ohms to a few tens of ohms is typical for such solenoids). Infinite means open, near zero means shorted.',
        u'4. Wiggle the harness while watching the reading to find an intermittent break.',
        u'5. Replace the valve only when the coil and wiring are proven bad.',
    ]),
    (u'Can you keep driving?', [
        u'Normal braking is not affected by this code alone. Traction control may be switched off, so starting on ice or wet ground is harder. Drive carefully and repair soon; the ABS function may also be limited on some systems.',
    ]),
    (u'Questions and answers', [
        (u'Why does a traction-control valve code turn on the ABS lamp?',
         u'On many systems ASR and ABS share the same electronic unit and valve block, so a fault in one lights the common lamp.'),
        (u'Is SPN 806 an engine fault?',
         u'No. It is a brake and traction system fault, although ASR does exchange torque requests with the engine.'),
    ]),
]},

'code-en:799': {'tail': [
    (u'What SPN 799 refers to', [
        u'SPN 799 is the ABS pressure modulator valve of axle 3, left side. The modulator is a solenoid valve in the air line of the brake chamber: on command from the ABS unit it holds, '
        u'releases or builds up pressure so the wheel does not lock. Axle 3 is the third axle of a multi-axle tractor or trailer, often a lift or steering axle.',
        u'The ABS unit energises the coil and checks the circuit, so nearly all SPN 799 codes are electrical, not pneumatic.',
        [u'**SPN 799 FMI 5** - current below normal or open circuit. The commonest entry: a broken wire to the modulator, corroded connector pins or an open coil.',
         u'**FMI 6** - current above normal or shorted to ground: chafed wire, water in the connector, shorted turns.',
         u'**FMI 3 and 4** - voltage high or low in the circuit.',
         u'**FMI 7** - mechanical fault: the valve sticks although the circuit is healthy.'],
    ]),
    (u'Step-by-step check', [
        u'1. Read all ABS codes. If several axles are listed at once, test supply voltage and ground of the ABS unit before the valves.',
        u'2. Find the axle 3 left modulator, inspect its connector and wire, clean and dry the contacts.',
        u'3. Measure the coil resistance against the manual. Open means a broken coil or wire, near zero means a short.',
        u'4. Test each wire for continuity back to the ABS unit while flexing the harness.',
        u'5. Check the air supply to the valve. Replace the modulator last.',
    ]),
    (u'Can you keep driving?', [
        u'The service brakes still work, but ABS on that wheel is disabled and it may lock on a slippery road. Drive with extra distance and gentle braking, and repair the fault soon. A faulty ABS can fail a roadworthiness test.',
    ]),
    (u'Questions and answers', [
        (u'Does SPN 799 FMI 5 mean the modulator is dead?',
         u'Not necessarily. An open wire or connector is far more common than a failed coil. Test the resistance first.'),
        (u'What is the difference between SPN 799 and SPN 800?',
         u'The same modulator on the other side of axle 3: 799 is left, 800 is right.'),
    ]),
]},

'code-en:800': {'tail': [
    (u'SPN 800: axle 3, right side', [
        u'SPN 800 is the ABS modulator of axle 3 on the right-hand side. Axle 3 is typically the rear or additional axle of a three-axle tractor or a trailer, where the connector hangs low and collects spray and road salt. '
        u'That is why a code on the right side often comes from the kerb-side harness, which is exposed to dirt and potholes.',
        [u'**FMI 5** - open circuit or low current: the usual finding is a broken wire near the axle or a corroded plug.',
         u'**FMI 6** - high current or short to ground: a wire rubbed through against the chassis.',
         u'**FMI 3 and 4** - voltage high or low in the circuit.',
         u'**FMI 7** - the valve is mechanically stuck.'],
    ]),
    (u'How to check', [
        u'1. Compare with SPN 799 on the other side. If both axle 3 valves are logged, look for a shared harness section or a shared connector between them.',
        u'2. Disconnect the plug, check for water and green deposits, dry and treat the contacts.',
        u'3. Measure the coil: it should be a few ohms to a few tens of ohms depending on the valve (use the manual). Open or shorted values condemn the coil.',
        u'4. Check wires for chafing at the spring brackets and the suspension.',
        u'5. Replace the modulator only if the coil is bad.',
    ]),
    (u'Can you keep driving?', [
        u'Braking continues, ABS on that wheel is off. Brake early and gently, keep a larger gap, and get the plug and wiring fixed; it is rarely an expensive repair.',
    ]),
    (u'Questions and answers', [
        (u'Could the other side of axle 3 fail as well?',
         u'Yes, because the cause is often shared: the same harness, ground or supply. Read both codes before you replace anything.'),
        (u'Is the pressure in the brake chamber affected?',
         u'The modulator can no longer release or hold pressure during an ABS event, but normal braking pressure still reaches the chamber.'),
    ]),
]},

'code-en:796': {'tail': [
    (u'SPN 796: axle 1, right side', [
        u'SPN 796 is the ABS pressure modulator of axle 1 on the right. Axle 1 is the front axle, which steers. That makes this valve more important than the one on the rear axle: '
        u'when ABS works on the front it lets you keep steering while braking hard. If the valve is disabled, a locked front wheel gives understeer and no steering response.',
        [u'**SPN 796 FMI 5** - open circuit or current below normal (the usual query is "spn 796 fmi 5"): a broken wire, a worn connector, or a coil with an open winding.',
         u'**FMI 6** - current above normal or short to ground.',
         u'**FMI 3 and 4** - circuit voltage high or low.',
         u'**FMI 7** - the valve does not respond.'],
    ]),
    (u'Where to look first', [
        [u'The harness at the front axle flexes with every steering movement and every suspension stroke. Look for wire breaks near the clamps and bends.',
         u'The connector on the kerb side of the front axle takes spray from the tyre. Corrosion and loose pins are common.',
         u'After tyre or brake work: a connector that was not refitted, or a wire trapped under a bracket.'],
        u'Then test the coil resistance against the manual, and test continuity of each wire back to the ABS unit while moving the harness. Replace the valve last.',
    ]),
    (u'Can you keep driving?', [
        u'Normal braking works, but a front wheel can lock on a wet or icy road and you can no longer steer around an obstacle. On this axle, avoid motorway speeds and long trips until it is repaired.',
    ]),
    (u'Questions and answers', [
        (u'Is a front axle ABS code more serious than a rear axle code?',
         u'Yes, in terms of handling: front lock-up means loss of steering. Repair it sooner.'),
        (u'Does SPN 796 have anything to do with SPN 795?',
         u'They are the two sides of the same axle: 795 is left, 796 is right.'),
    ]),
]},

'code-en:798': {'tail': [
    (u'SPN 798: axle 2, right side', [
        u'SPN 798 is the ABS pressure modulator of axle 2, right. Axle 2 is normally the first rear or drive axle on a three-axle truck or a tractor. '
        u'It carries most of the load and the drive torque, so the same valve also works with traction control (ASR) on many trucks.',
        [u'**FMI 5** - open circuit: broken wire at the axle or a corroded connector (the most frequent search is "spn 798 fmi 5").',
         u'**FMI 6** - short to ground, often a chafed wire against the chassis or suspension.',
         u'**FMI 3 and 4** - voltage out of range in the circuit.',
         u'**FMI 7** - valve not moving.'],
    ]),
    (u'Checks and typical causes', [
        [u'Connectors at the drive axle: dirt, oil and heat. Check pins for corrosion.',
         u'Harness along the axle and the air springs: rubbing and heat damage.',
         u'Supply and ground of the ABS unit, if codes from several valves are present.',
         u'The coil itself, after resistance has been measured and compared with the manual.'],
        u'Disconnect the plug, check the pins and wires, measure the coil, and only then replace the valve. Always clear the code and test-drive to see whether it returns.',
    ]),
    (u'Can you keep driving?', [
        u'The truck brakes normally but without ABS on that wheel. A locked drive wheel on a loaded truck can cause the rear to swing out. Keep speed down, drive smoothly and repair soon.',
    ]),
    (u'Questions and answers', [
        (u'Is SPN 798 the same as SPN 797?',
         u'No, 798 is the right side and 797 the left side of the same axle. Check both if both codes appear.'),
        (u'Can a trailer cause this code?',
         u'No. SPN 798 belongs to the tractor\'s own axle. Trailer faults are reported through the trailer ABS unit.'),
    ]),
]},

'code-en:629': {'tail': [
    (u'What SPN 629 means', [
        u'SPN 629 is "Controller #1": it reports a problem inside the engine control unit itself (or one of its internal channels), not in a sensor. That makes it a code that should be treated carefully: '
        u'a large share of SPN 629 entries are caused by power and ground problems that disturb the controller rather than by a failed unit.',
        [u'**FMI 12** - bad intelligent device: the controller reports an internal failure.',
         u'**FMI 14** - special instructions; follow the make-specific text.',
         u'**FMI 8 and 2** - abnormal signal or erratic data.',
         u'**FMI 13** - out of calibration: wrong or damaged software.'],
    ]),
    (u'Before you condemn the controller', [
        [u'Battery voltage and terminals: low or unstable supply causes internal resets that are logged as a controller fault.',
         u'Ground straps from the engine to the frame, and the controller\'s own ground pins.',
         u'Connector pins: bent, pushed back or corroded.',
         u'Software: an outdated calibration, an interrupted update or a wrong parameter file.',
         u'Water in the controller connector or a damaged seal.'],
        u'Test supply and ground under load, inspect the connector, check whether a calibration update exists, clear the code and see whether it returns. If SPN 629 returns with healthy power, replace or reflash the controller as the manufacturer prescribes.',
    ]),
    (u'Can you keep driving?', [
        u'If the engine runs normally and the lamp is amber, you can reach a service point but expect random resets. If the engine stalls, derates or refuses to start, stop and call for help.',
    ]),
    (u'Questions and answers', [
        (u'Does SPN 629 always mean a new ECU?',
         u'No. Voltage problems, grounds and software often cause it. Replace the controller only after those checks.'),
        (u'Will a reflash fix it?',
         u'If the cause is a corrupted or old calibration, yes. If it is hardware or power, no.'),
    ]),
]},

'code-en:558': {'tail': [
    (u'What SPN 558 is for', [
        u'SPN 558 is the accelerator pedal idle validation (limit) switch. Electronic pedals have two ways to prove the driver has lifted the foot: the position sensor reads a low value, and a switch '
        u'closes at idle. The computer compares them. If they disagree, it records SPN 558 or SPN 91 and may limit power.',
        [u'**SPN 558 FMI 2** - the switch and the sensor disagree. This is the most-searched entry.',
         u'**FMI 13** - out of calibration.',
         u'**FMI 3 and 4** - the switch circuit is open or shorted.',
         u'**FMI 14** - special instructions, make-specific.'],
    ]),
    (u'Checks', [
        u'1. In the scan tool watch pedal position and the idle switch status while you press and release slowly. The switch should change state right at the start of travel.',
        u'2. If the switch stays set, or the sensor shows a value with the foot off, the pedal is out of adjustment, worn or dirty.',
        u'3. Check the pedal connector for corrosion and for a loose latch.',
        u'4. Look for an obstruction under the pedal, such as a floor mat, and the pedal stop.',
        u'5. If the pedal was replaced recently, check whether it needs a learning or calibration procedure.',
        u'Replace the pedal assembly if the sensor and switch cannot be brought to agree, since they are normally one part.',
    ]),
    (u'Can you keep driving?', [
        u'The engine usually goes to idle or to limited throttle. That is not safe in traffic. Drive slowly to the nearest stop and call for service.',
    ]),
    (u'Questions and answers', [
        (u'How does SPN 558 differ from SPN 91?',
         u'SPN 91 is the pedal position sensor. SPN 558 is the idle switch that confirms that sensor. Both are often logged together.'),
        (u'Why does a floor mat matter?',
         u'A mat can stop the pedal from returning fully, so the idle switch never closes.'),
    ]),
]},

'code-en:790': {'tail': [
    (u'SPN 790: front axle, right wheel sensor', [
        u'SPN 790 is the ABS wheel speed sensor at the right wheel of axle 1, the front axle. Most truck sensors are inductive: a two-wire coil that produces an AC voltage as the toothed ring '
        u'passes. There is no supply voltage; the signal grows with speed. On the steering axle the cable also flexes with every turn of the wheel, which is why it fails more often than rear sensors.',
        [u'**SPN 790 FMI 1** - data below normal, most severe: no signal or a very weak one (the second most-searched entry).',
         u'**FMI 2** - erratic signal: air gap too large, a dirty or damaged tone ring, wheel bearing play.',
         u'**FMI 3, 4, 5, 6** - open circuit, shorts to ground or supply: usually a broken cable or connector.',
         u'**FMI 7, 8, 10** - mechanical or frequency faults, usually from the ring or the gap.'],
    ]),
    (u'Check in this order', [
        u'1. Measure the sensor resistance with the connector disconnected. WABCO sensors are typically around 0.9-1.3 kOhm, Knorr-Bremse ones around 1.7 kOhm; compare with the other front sensor.',
        u'2. Turn the steering lock to lock while watching the resistance. A jump or an open reading shows a broken cable at the knuckle.',
        u'3. Inspect the toothed ring for damaged, rusty or dirty teeth, and check wheel bearing play.',
        u'4. Push the sensor fully into its clamp so the gap is set automatically, and use new grease or a new clamp sleeve.',
        u'5. Measure the AC output while spinning the wheel: it should be steady and rise with speed.',
    ]),
    (u'Can you keep driving?', [
        u'Normal braking works, but ABS on the front axle is off. A locked front wheel means no steering on a slippery surface. Drive slowly and repair soon.',
    ]),
    (u'Questions and answers', [
        (u'Why does the code come back after cleaning the sensor?',
         u'The cable may be broken inside the insulation at the knuckle, or the gap may be wrong. Test while turning the wheel.'),
        (u'Is SPN 790 the left or the right wheel?',
         u'Right. The left front wheel of the same axle is SPN 789.'),
    ]),
]},

'code-en:1056': {'tail': [
    (u'What SPN 1056 refers to', [
        u'SPN 1056 is the electronic pressure control for the trailer control valve in an electronic braking system. The valve sets the brake pressure sent to the trailer line, '
        u'and the electronics check its circuit and, on many systems, compare commanded and measured pressure.',
        [u'**FMI 2** - erratic signal or the pressure does not match the command (a frequent search).',
         u'**FMI 5** - open circuit: the wire, the plug or the coil.',
         u'**FMI 6 and 4** - short to ground or low voltage.',
         u'**FMI 3** - voltage high or shorted to supply.',
         u'**FMI 7** - the valve is mechanically stuck.'],
    ]),
    (u'Checks', [
        [u'The 7-pin and 15-pin connectors between tractor and trailer, and the coiled air hoses: leakage or a loose connection.',
         u'The trailer control valve connector: corrosion and water.',
         u'Air pressure in the supply line, with the gauge, to rule out a leak that looks like a valve fault.',
         u'Brake-pressure sensor in the trailer line, where fitted.'],
        u'Compare the commanded and measured pressure in the scan tool while applying the brake. A good valve follows the command within a small margin. Only if wiring and plugs are clean should the valve be replaced.',
    ]),
    (u'Can you keep driving?', [
        u'Brake performance of the combination may be reduced, because the trailer brake pressure is not controlled correctly. Drive carefully with a lighter load and shorter speeds until you have it checked.',
    ]),
    (u'Questions and answers', [
        (u'Does SPN 1056 appear without a trailer?',
         u'It can, if the system tests the valve circuit regardless. A code with no trailer points to the tractor-side valve or harness.'),
        (u'Could it be only a connector problem?',
         u'Yes, quite often. Check connectors and hoses first.'),
    ]),
]},

}
