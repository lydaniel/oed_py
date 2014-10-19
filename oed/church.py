# Library for executing and parsing church programs

import subprocess
import os

import pmf

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

# To a church list
def to_church_list(lst, ld='(', rd=')'):
    string = ld
    for (i, lst_el) in enumerate(lst) :
        if (isinstance(lst_el, list)) :
            string += to_church_list(lst_el, ld, rd) + ' '
        else :
            string += lst_el + ' '

    return string[:-1] + rd

# Executes a church program and overwrites output with the church-produced PMF
def exec_model(filename, inputs, output, query=None, church_exec="church") :
    if (query == None) :
        return None
    else :
        command = church_exec + " -a \"" + inputs + "\" " + filename 
        model_process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        model_output_raw = model_process.stdout.read()

        output.clear()

        if ((query == "mh-query") or (query == "rejection-query")):
            model_output_list = parse_church_list(model_output_raw)

            #if (isinstance(model_output_list[0], list)) :
            #    for (i, ml) in enumerate(model_output_list) :
            #       model_output_list[i] = " ".join(ml)

            for ml in model_output_list :
                found = False
                for mo in output :
                    if (ml == mo.x) :
                        mo.p += 1
                        found = True
                        break
                            
                if (found == False) :
                    output.append(pmf.P(ml, 1))

            output.normalize()
            output.pmf.sort(key=lambda p: p.x)

        elif (query == "enumeration-query") :
            model_output_list_base  = parse_church_list(model_output_raw)
            model_output_list_x_raw = model_output_list_base[0]
            model_output_list_pmf   = model_output_list_base[1]

            model_output_list_x = model_output_list_x_raw
            for (i, mlx) in enumerate(model_output_list_x_raw) :
                if (isinstance(mlx, list)) :
                    model_output_list_x[i] = to_church_string(mlx)

            for (i, ml) in enumerate(model_output_list_x) :
                output.append(pmf.P(model_output_list_x[i], model_output_list_pmf[i]))

            output.normalize()
            output.pmf.sort(key=lambda p: p.x)

        elif (query == "raw") :
            model_output_list = parse_church_list(model_output_raw)
            for (i, ml) in enumerate(model_output_list) :
                output.append(pmf.P(i, ml))


def homogenize_outputs(outputs) :
    all_output_x = []
    for op in outputs :
        for opp in op.pmf :
            if opp.x not in all_output_x :
                all_output_x.append(opp.x)

    for op in outputs :
        op_dirty = False
        for aox in all_output_x :
            no_aox = True
            for opp in op.pmf :
                if (opp.x == aox) :
                    no_aox = False
                    break

            if (no_aox) :
                op.append(pmf.P(aox, 0))
                op_dirty = True

        if (op_dirty) :
            op.pmf.sort(key=lambda p: p.x)


