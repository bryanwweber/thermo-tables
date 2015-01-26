import requests
import numpy as np
from io import BytesIO

desired_cols = [
    'Temperature_C',
    'Pressure_bar',
    'Volume_m3kg',
    'Internal_Energy_kJkg',
    'Enthalpy_kJkg',
    'Entropy_JgK',
]

payload = {
    'Action' : 'Data',
    'Wide' : 'on',
    'ID' : 'C7732185',
    'Digits' : '12',
    'RefState' : 'DEF',
    'TUnit' : 'C',
    'PUnit' : 'bar',
    'DUnit' : 'kg/m3',
    'HUnit' : 'kJ/kg',
    'WUnit' : 'm/s',
    'VisUnit' : 'uPa*s',
    'STUnit' : 'N/m',
    'Type' : 'IsoBar',
}

conditions = {
             0.060: [36.16, 80, 500, 40],
             0.350: [72.69, 80, 500, 40],
             0.700: [89.95, 100, 500, 40],
             1.000: [99.63, 100, 500, 40],
             1.500: [111.37, 120, 600, 40],
             3.000: [133.55, 160, 600, 40],
             # 5.000: [151.86, 180, 700, 40],
             # 7.000: [164.97, 180, 700, 40],
             # 10.00: [179.91, 200, 640, 40],
             # 15.00: [198.32, 200, 640, 40],
             # 20.00: [212.42, 240, 700, 40],
             # 30.00: [233.90, 240, 700, 40],
             # 40.00: [250.40, 280, 740, 40],
             # 60.00: [275.64, 280, 740, 40],
             # 80.00: [295.06, 320, 740, 40],
             # 100.0: [311.06, 320, 740, 40],
             # 120.0: [324.75, 360, 740, 40],
             # 140.0: [336.75, 360, 740, 40],
             # 160.0: [347.44, 360, 740, 40],
             # 180.0: [357.06, 360, 740, 40],
             # 200.0: [365.81, 400, 800, 40],
             # 240.0: [000.00, 400, 800, 40],
             # 280.0: [000.00, 400, 900, 40],
             # 320.0: [000.00, 400, 900, 40],
             }
tex = ""
col_number = 0

for pressure, temp_conds in sorted(conditions.items()):

    payload['P'] = pressure
    payload['TLow'] = temp_conds[1]
    payload['THigh'] = temp_conds[2]
    payload['TInc'] = temp_conds[3]

    r = requests.get('http://webbook.nist.gov/cgi/fluid.cgi?', params=payload)
    # print(r.url)

    data = np.genfromtxt(BytesIO(r.text.encode()), dtype=float, delimiter='\t', names=True)

    out = []
    for col in desired_cols:
        out.append(data[col].tolist())
    # print(out)

    # header=('Temperature Pressure volume internal-energy enthalpy entropy '
            # 'Pressure volume internal-energy enthalpy entropy')

    if col_number == 0:
        # First pressure
        temp_out = out
        col_number = 1
    elif col_number == 1:
        # Second pressure
        if len(out[0]) != len(temp_out[0]):
            for lst in out:
                lst.insert(0,'{\\textemdash}')

        temp_out.extend(out[1:])
        print(list(map(list, zip(*temp_out))))
        # print(temp_out)
        col_number = 0

    # np.savetxt('{}-bar-table.txt'.format(pressure), temp_out, fmt='%017.12f', delimiter=' ', newline='\n', header=header, comments='')
