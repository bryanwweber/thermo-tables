from collections import OrderedDict, namedtuple

Columns = namedtuple('Columns', ['col_name', 'unit', 'num_of_cols'])

sat_cols = [
    Columns('Specific Volume', '\\meter\\cubed\\per\\kilogram', 2),
    Columns('Internal Energy', '\\kilo\\joule\\per\\kilogram', 2),
    Columns('Enthalpy', '\\kilo\\joule\\per\\kilogram', 3),
    Columns('Entropy', '\\kilo\\joule\\per\\kilogram\\per\\kelvin', 2),
]

def saturated_temperature_tex(input_table):
    tex_string = "\\input{preamble.tex}\n\\begin{document}\n\\begin{center}\n"
    tex_string += ("\\pgfplotstabletypeset[\nevery head row/.style={\nbefore row={"
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

    tex_string += ("\\\\\n\cmidrule{3-11}%\n&& Sat. & Sat. & Sat. & Sat. & Sat."
                   " & & Sat. & Sat. & Sat. & \\\\%\n},\nafter row={%\n"
                   "\\si{\\degreeCelsius} & \\si{\\bar} & $v_f \\times 10^3$ & "
                   "$v_g$ & $u_f$ & $u_g$ & $h_f$ & $h_{fg}$ & $h_g$ & $s_f$ "
                   "& $s_g$ & \\si{\\degreeCelsius} \\\\%\n\\midrule\\endhead%\n},\n},\n"
                   "begin table=\\begin{longtable},\nend table=\\end{longtable},\n"
                   "every nth row={4}{before row={\\midrule}},\ncolumns={"
                  )
    col_list = OrderedDict()
    col_list['Temperature'] = "column name={Temp.},\nprecision=2,\n"
    col_list['Pressure'] = "column name={Pres.},\nfixed zerofill,\nprecision=5,\n"
    col_list['volume-l'] = "multiply by={1000},\nprecision=4,\n"
    col_list['volume-v'] = "precision=3,\n"
    col_list['internal-energy-l'] = "precision=2,\n"
    col_list['internal-energy-v'] = "precision=1,\n"
    col_list['enthalpy-l'] = "precision=2,\n"
    col_list['enthalpy-fg'] = "precision=1,\n,fixed zerofill,\ncolumn name={Evap.},\n"
    col_list['enthalpy-v'] = "precision=1,\n"
    col_list['entropy-l'] = "precision=4,\n"
    col_list['entropy-v'] = "precision=4,\ncolumn type/.add={}{|},\n"

    format_chunk = ""
    for col, fmt in col_list.items():
        tex_string += "{col}, ".format(col=col)
        format_chunk += "columns/{col}/.style={{\nfixed,\n".format(col=col)
        format_chunk += fmt
        if '-l' in col:
            format_chunk += "column name={Liquid},\nfixed zerofill,\ncolumn type/.add={|}{},\n"
        elif '-v' in col:
            format_chunk += "column name={Vapor},\nfixed zerofill,\n"
        format_chunk += "},\n"
    else:
        tex_string += "Temperature},\n"

    tex_string += format_chunk
    tex_string += "]\n{\n"
    tex_string += input_table
    tex_string += "\n}\n\\end{center}\n\\end{document}\n"
    return tex_string
    # print(tex_string)

if __name__ == '__main__':
    saturated_temperature_tex('1')