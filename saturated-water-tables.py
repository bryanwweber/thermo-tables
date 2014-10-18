import requests
import numpy as np
from io import BytesIO
from generate_tex import saturated_temperature_tex
import subprocess

desired_cols = [
    'Temperature_C',
    'Pressure_bar',
    'Volume_l_m3kg',
    'Volume_v_m3kg',
    'Internal_Energy_l_kJkg',
    'Internal_Energy_v_kJkg',
    'Enthalpy_l_kJkg',
    'Enthalpy_v_kJkg',
    'Entropy_l_JgK',
    'Entropy_v_JgK',
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
}

temps = [
        [0.01, 0.02, 1],
        [4, 40, 1],
        [45, 100, 5],
        [100, 370, 10],
        [373.946, 373.946, 1],
        ]

press = [
        [0.04, 0.1, 0.02],
        [0.2, 1, 0.1],
        [1.5, 5, 0.5],
        [6, 10, 1],
        [15, 50, 5],
        [60, 220, 10],
        [220.64, 220.64, 1],
        ]

payload['Type'] = 'SatP'
temp_out = np.zeros((1,len(desired_cols)))
for temp in temps:
    payload['TLow'] = temp[0]
    payload['THigh'] = temp[1]
    payload['TInc'] = temp[2]

    r = requests.get('http://webbook.nist.gov/cgi/fluid.cgi?', params=payload)
    # print(r.url)

    data = np.genfromtxt(BytesIO(r.text.encode()), dtype=float, delimiter='\t', names=True)

    out = []
    for col in desired_cols:
        out.append(data[col])

    temp_out = np.vstack((temp_out, np.array(out).transpose()))

temp_out = np.delete(temp_out, 0, axis=0)
h_fg = temp_out[:,7] - temp_out[:,6]
temp_out = np.insert(temp_out, 7, h_fg, axis=1)

header=('Temperature       Pressure          volume-l          volume-v          '
    'internal-energy-l internal-energy-v enthalpy-l        enthalpy-fg       enthalpy-v        entropy-l         entropy-v')

# print(header+'\n', np.array_str(temp_out, max_line_width=1000).replace('[', '').replace(']', ''))
tex = saturated_temperature_tex(header+'\n'+ np.array_str(temp_out, max_line_width=1000).replace('[', '').replace(']', ''))
# print(tex)
proc = subprocess.Popen('pdflatex -jobname=sat-table', stdin=subprocess.PIPE)
proc.communicate(bytes(tex, 'utf-8'))
proc = subprocess.Popen('pdflatex -jobname=sat-table', stdin=subprocess.PIPE)
proc.communicate(bytes(tex, 'utf-8'))

# np.savetxt('temperature-sat-table.txt', temp_out, fmt='%017.12f', delimiter=' ', newline='\n', header=header, comments='')

# payload['TLow'] = None
# payload['THigh'] = None
# payload['TInc'] = None
# payload['Type'] = 'SatT'
# pres_out = np.zeros((1,len(desired_cols)))
# for pres in press:
#     payload['PLow'] = pres[0]
#     payload['PHigh'] = pres[1]
#     payload['PInc'] = pres[2]

#     r = requests.get('http://webbook.nist.gov/cgi/fluid.cgi?', params=payload)
#     # print(r.url)

#     data = np.genfromtxt(BytesIO(r.text.encode()), dtype=float, delimiter='\t', names=True)

#     out = []
#     for col in desired_cols:
#         out.append(data[col])

#     pres_out = np.vstack((pres_out, np.array(out).transpose()))

# pres_out = np.delete(pres_out, 0, axis=0)
# h_fg = pres_out[:,7] - pres_out[:,6]
# pres_out = np.insert(pres_out, 7, h_fg, axis=1)
# np.savetxt('pressure-sat-table.txt', pres_out, fmt='%017.12f', delimiter=' ', newline='\n', header=header, comments='')
