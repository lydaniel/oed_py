# Library for executing and parsing church programs

import subprocess
import os

# Enumerated types for string parsing
class Type:
    _string = 0
    _float = 1

# Splits nested, delimited strings into tokenized lists
def tokenize(string, ld='(', rd=')'):
    return string.replace(ld,' ' + ld + ' ').replace(rd,' ' + rd + ' ').split()

# Parses tokenized lists into hierarchical lists
def parse(tokens, ld='(', rd=')'):
    token = tokens.pop(0)
    if (token == ld) :
        lst = []
        while (tokens[0] != rd) :
            lst.append(parse(tokens, ld, rd))
        tokens.pop(0) 
        return lst
    else:
        return token

# Parses a church list
def parse_church_list(string, ld='(', rd=')') :
    return parse(tokenize(string, ld, rd), ld, rd)

# Executes a church program and overwrites output with the church-produced PMF
def exec_model(filename, inputs, output, query=None, church_exec="church", var_type=Type._string) :
    if (query == None) :
        return None
    else :
        command = church_exec + " -a \"" + inputs + "\" " + filename 
        model_process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        model_output_raw = model_process.stdout.read()

        output.clear()

        if ((query == "mh-query") or (query == "rejection-query")):
            model_output_list = parse_church_list(model_output_raw)
            for ml in model_output_list :
                for mo in output :
                    if (var_type == Type._string) :
                        if (ml == mo.x) :
                            mo.p += 1
                            break
                    elif (var_type == Type._float) :
                        if (float(ml) == float(mo.x)) :
                            mo.p += 1
                            break

        elif (query == "enumeration-query") :
            model_output_list_base  = parse_church_list(model_output_raw)
            model_output_list_x_raw = model_output_list_base[0]
            model_output_list_pmf   = model_output_list_base[1]

            model_output_list_x = model_output_list_x_raw
            for (i, mlx) in enumerate(model_output_list_x_raw) :
                if (isinstance(mlx, list)) :
                    model_output_list_x[i] = ''
                    for mli in mlx :
                        model_output_list_x[i] += mli + ' '
                    model_output_list_x[i] = model_output_list_x[i][:-1]

            for (i, ml) in enumerate(model_output_list_x) :
                for mo in output :
                    if (var_type == Type._string) :
                        if (ml == mo.x) :
                            mo.p = float(model_output_list_pmf[i])
                            break
                    elif (var_type == Type._float) :
                        if (float(ml) == float(mo.x)) :
                            mo.p = float(model_output_list_pmf[i])
                            break

        output.normalize()

