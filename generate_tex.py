from collections import OrderedDict, namedtuple
from math import log10, floor

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x)))))

Columns = namedtuple('Columns', ['col_name', 'unit', 'num_of_cols'])

sat_cols = [
    Columns('Specific Volume', '\\meter\\cubed\\per\\kilogram', 2),
    Columns('Internal Energy', '\\kilo\\joule\\per\\kilogram', 2),
    Columns('Enthalpy', '\\kilo\\joule\\per\\kilogram', 3),
    Columns('Entropy', '\\kilo\\joule\\per\\kilogram\\per\\kelvin', 2),
]

sat_col_list = OrderedDict()
sat_col_list['volume-l'] = "column type={S[table-omit-exponent, fixed-exponent=-3, table-format=1.4, round-mode=places, round-precision=4,]},\n"
sat_col_list['volume-v'] = "column type={S[table-format=3.6, round-mode=places, round-precision=3,]},\n"
sat_col_list['internal-energy-l'] = "column type={S[table-format=4.2, round-mode=places, round-precision=2,]},\n"
sat_col_list['internal-energy-v'] = "column type={S[table-format=4.1, round-mode=places, round-precision=1,]},\n"
sat_col_list['enthalpy-l'] = "column type={S[table-format=4.2, round-mode=places, round-precision=2,]},\n"
sat_col_list['enthalpy-fg'] = "column type={S[table-format=4.1, round-mode=places, round-precision=1,]},\n"
sat_col_list['enthalpy-v'] = "column type={S[table-format=4.1, round-mode=places, round-precision=1,]},\n"
sat_col_list['entropy-l'] = "column type={S[table-format=1.4, round-mode=places, round-precision=4,]},\n"
sat_col_list['entropy-v'] = "column type={S[table-format=1.4, round-mode=places, round-precision=4,]},\ncolumn type/.add={}{|},\n"

def tex_begin():
    return ("\\documentclass{article}\n\\usepackage[margin=0.5in]{geometry}\n"
            "\\usepackage{pgfplotstable}\n\\pgfplotsset{compat=1.11}\n"
            "\\usepackage{booktabs}\n\\usepackage{siunitx}\n\\sisetup{\n"
            "per-mode=symbol,\ntable-omit-exponent,\n}\n\\pagestyle{empty}\n"
            "\\usepackage{longtable}\n\\begin{document}\n\\begin{center}\n"
           )

def tex_end():
    return "\\end{center}\n\\end{document}\n"

def saturated_temperature_tex(input_table):
    sat_col_list['Temperature'] = "column type={S[table-format=3.2, round-mode=places, round-precision=2, zero-decimal-to-integer,]},\n"
    sat_col_list['Pressure'] = "column type={S[table-format=3.4, round-mode=places, round-precision=4,]},\n"
    sat_col_list.move_to_end('Pressure', last=False)
    sat_col_list.move_to_end('Temperature', last=False)
    tex_string = ("\\pgfplotstabletypeset[\nevery head row/.style={\nbefore row={"
                   "\\multicolumn{12}{c}{\\Large Properties of Saturated Water "
                   "(Liquid-Vapor): Temperature Table} \\\\[5pt] \\toprule\n&& ")

    for col in sat_cols:
        name = col.col_name
        ncols = col.num_of_cols
        tex_string += "\\multicolumn{{{ncols}}}{{c|}}{{{name}}} & ".format(ncols=ncols, name=name)

    tex_string += "\\\\\n&& "

    for col in sat_cols:
        unit = col.unit
        ncols = col.num_of_cols
        tex_string += "\\multicolumn{{{ncols}}}{{c|}}{{\\si{{{unit}}}}} & ".format(ncols=ncols, unit=unit)

    tex_string += ("\\\\\n\cmidrule{3-11}%\n&& {Sat.} & {Sat.} & {Sat.} & {Sat.} "
                   "& {Sat.} & & {Sat.} & {Sat.} & {Sat.} & \\\\%\n{Temp.} & {Pres.} "
                   "& {Liquid} & {Vapor} & {Liquid} & {Vapor} & {Liquid} & {Evap.} & "
                   "{Vapor} & {Liquid} & {Vapor} & {Temp.} \\\\%\n},\nafter row={%\n"
                   "\\si{\\degreeCelsius} & \\si{\\bar} & {$v_f \\times 10^3$} & "
                   "$v_g$ & $u_f$ & $u_g$ & $h_f$ & $h_{fg}$ & $h_g$ & $s_f$ "
                   "& $s_g$ & \\si{\\degreeCelsius} \\\\%\n\\midrule\\endhead%\n},\noutput empty row,\n},\n"
                   "begin table=\\begin{longtable},\nend table=\\end{longtable},\n"
                   "every nth row={4}{before row={\\midrule}},\ncolumns={"
                  )

    format_chunk = ""
    for col, fmt in sat_col_list.items():
        tex_string += "{col}, ".format(col=col)
        format_chunk += "columns/{col}/.style={{\nstring type,\n".format(col=col)
        format_chunk += fmt
        if '-l' in col:
            format_chunk += "column type/.add={|}{},\n"

        format_chunk += "},\n"
    else:
        tex_string += "Temperature},\n"

    tex_string += format_chunk
    tex_string += "]\n{\n"
    tex_string += input_table
    tex_string += "\n}\n"
    return tex_string

def saturated_pressure_tex(input_table):
    sat_col_list['Temperature'] = "column type={S[table-format=3.2, round-mode=places, round-precision=2,]},\n"
    sat_col_list['Pressure'] = "column type={S[table-format=3.2, round-mode=places, round-precision=2,]},\n"
    sat_col_list.move_to_end('Temperature', last=False)
    sat_col_list.move_to_end('Pressure', last=False)
    tex_string = ("\\pgfplotstabletypeset[\nevery head row/.style={\nbefore row={"
                   "\\multicolumn{12}{c}{\\Large Properties of Saturated Water "
                   "(Liquid-Vapor): Pressure Table} \\\\[5pt] \\toprule\n&& ")

    for col in sat_cols:
        name = col.col_name
        ncols = col.num_of_cols
        tex_string += "\\multicolumn{{{ncols}}}{{c|}}{{{name}}} & ".format(ncols=ncols, name=name)

    tex_string += "\\\\\n&& "

    for col in sat_cols:
        unit = col.unit
        ncols = col.num_of_cols
        tex_string += "\\multicolumn{{{ncols}}}{{c|}}{{\\si{{{unit}}}}} & ".format(ncols=ncols, unit=unit)

    tex_string += ("\\\\\n\cmidrule{3-11}%\n&& {Sat.} & {Sat.} & {Sat.} & {Sat.} "
                   "& {Sat.} & & {Sat.} & {Sat.} & {Sat.} & \\\\%\n{Pres.} & {Temp.} "
                   "& {Liquid} & {Vapor} & {Liquid} & {Vapor} & {Liquid} & {Evap.} & "
                   "{Vapor} & {Liquid} & {Vapor} & {Pres.} \\\\%\n},\nafter row={%\n"
                   "\\si{\\bar} & \\si{\\degreeCelsius} & {$v_f \\times 10^3$} & "
                   "$v_g$ & $u_f$ & $u_g$ & $h_f$ & $h_{fg}$ & $h_g$ & $s_f$ "
                   "& $s_g$ & \\si{\\bar} \\\\%\n\\midrule\\endhead%\n},\noutput empty row,\n},\n"
                   "begin table=\\begin{longtable},\nend table=\\end{longtable},\n"
                   "every nth row={4}{before row={\\midrule}},\ncolumns={"
                  )

    format_chunk = ""
    for col, fmt in sat_col_list.items():
        tex_string += "{col}, ".format(col=col)
        format_chunk += "columns/{col}/.style={{\nstring type,\n".format(col=col)
        format_chunk += fmt
        if '-l' in col:
            format_chunk += "column type/.add={|}{},\n"

        format_chunk += "},\n"
    else:
        tex_string += "Pressure},\n"

    tex_string += format_chunk
    tex_string += "]\n{\n"
    tex_string += input_table
    tex_string += "\n}\n"
    return tex_string

def superheated_begin_tex(low_pres, high_pres):
    tex_string = ("\\pgfplotstabletypeset[\nevery head row/.style={\nbefore row={"
                  "\\multicolumn{11}{c}{\\Large Properties of Superheated Water "
                  "Vapor} \\\\[5pt] \\toprule%\n$T$ & $v$ & $u$ & $h$ & $s$ &&& $v$ & "
                  "$u$ & $h$ & $s$ \\\\%\n\\si{\\degreeCelsius} & "
                  "\\si{\\meter\\cubed\\per\\kilogram} & \\si{\\kilo\\joule\\per\\kilogram} & "
                  "\\si{\\kilo\\joule\\per\\kilogram} & \\si{\\kilo\\joule\\per\\kilogram\\per\\kelvin} &"
                  "&& \\si{\\meter\\cubed\\per\\kilogram} & \\si{\\kilo\\joule\\per\\kilogram} & "
                  "\\si{\\kilo\\joule\\per\\kilogram} & \\si{\\kilo\\joule\\per\\kilogram\\per\\kelvin} "
                  "\\\\%\n\\midrule%\n},\noutput empty row,\n},\n"
                  "every first row/.style={%\nbefore row/.add={%\n& "
                 )
    tex_string += ("\\multicolumn{{4}}{{c}}{{$p = {low_pres} \\si{{\\bar}} = "
                   "{low_mpa} \\si{{\\MPa}}$}} &&& \\multicolumn{{4}}{{c}}{{$p "
                   "= {high_pres} \\si{{\\bar}} = {high_mpa} \\si{{\\MPa}}$}} "
                   "\\\\\n".format(low_pres=round_sig(low_pres, 3), low_mpa=round_sig(low_pres/10, 3),
                   high_pres=round_sig(high_pres, 3), high_mpa=round_sig(high_pres/10, 3))
                  )
    print(tex_string)

def superheated_new_pressure_tex():
    tex_string = ("\\pgfplotstabletypeset[\nevery head row/.style={\noutput empty row\n},\n")

if __name__ == '__main__':
    superheated_begin_tex(1.000, 100.0)