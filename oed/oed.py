# Library for computing OED measures

import math

import church

# Computes an array of KL-divergences that corresponds to each output
def get_output_kl(models, outputs) :
    p_model_g_input_output_summand = [0]*len(models)
    for m in range(len(models)) :
        p_model_g_input_output_summand[m] = [0]*len(outputs[m])
        for i in range(len(p_model_g_input_output_summand[m])) :
            p_model_g_input_output_summand[m][i] += outputs[m][i].p*models[m].p

    p_model_g_input_output_sum = [0]*len(outputs[0])
    for i in range(len(p_model_g_input_output_sum)) :
        for m in range(len(models)) :
            p_model_g_input_output_sum[i] += p_model_g_input_output_summand[m][i]

    p_model_g_input_output = [0]*len(models) 
    for m in range(len(models)) :
        p_model_g_input_output[m] = [0]*len(outputs[m])
        for i in range(len(p_model_g_input_output[m])) :
            if (p_model_g_input_output_sum[i] == 0) :
                p_model_g_input_output[m][i] = 0
            else :
                p_model_g_input_output[m][i] = p_model_g_input_output_summand[m][i]/p_model_g_input_output_sum[i]

    output_kl = [0]*len(outputs[0])
    for i in range(len(output_kl)) :
        for m in range(len(models)) :
            if (p_model_g_input_output[m][i] == 0) :
                output_kl[i] += 0
            else :
                output_kl[i] += p_model_g_input_output[m][i]*math.log(p_model_g_input_output[m][i]/models[m].p)
    return output_kl

# Computes an array of the PDF of each output
def get_output_pmf(models, outputs) :
    p_model_g_input_output_summand = [0]*len(models)
    for m in range(len(models)) :
        p_model_g_input_output_summand[m] = [0]*len(outputs[m])
        for i in range(len(p_model_g_input_output_summand[m])) :
            p_model_g_input_output_summand[m][i] += outputs[m][i].p*models[m].p

    p_model_g_input_output_sum = [0]*len(outputs[0])
    for i in range(len(p_model_g_input_output_sum)) :
        for m in range(len(models)) :
            p_model_g_input_output_sum[i] += p_model_g_input_output_summand[m][i]

    return p_model_g_input_output_sum

# Computes the expected KL-divergence over all the outputs
def get_expected_kl(models, outputs, output_kl=None, output_pmf=None) :
    expected_kl = 0

    if (output_kl or output_pmf) :
        if not output_kl :
            output_kl = get_output_kl(models, outputs)

        if not output_pmf :
            output_pmf = get_output_pmf(models, outputs)

        for i in range(len(output_kl)) :
            expected_kl += output_kl[i]*output_pmf[i]
    else :
        for i in range(len(outputs[0])) :
            p_output = 0
            for m in range(len(models)) :
                p_output += outputs[m][i].p*models[m].p
            for m in range(len(models)) :
                expected_kl += outputs[m][i].p*models[m].p*math.log(outputs[m][i].p/p_output)

    return expected_kl
        
