#!/usr/bin/python
# import libraries
import sys
sys.path.append('../oed')

import oed
import pmf
import church

import copy

# define church programs
# -- models is a PMF of the belief distribution for all the mdoels
# -- the first arguments are the filename of each church program
# -- the second arguments are the prior belief distribution of each church program (which is uniform in this example)
models = pmf.PMF(3)
models[0] = pmf.P("model_0.church", 1.0)
models[1] = pmf.P("model_1.church", 1.0)
models[2] = pmf.P("model_2.church", 1.0)
models.normalize()

# define space of possible outputs
# -- output_pmf is a PMF to store the resulting distributions from the church programs
# -- the first arguments are the possible output values
# -- the second arguments will be overwritten and do not matter
output_pmf = pmf.PMF(5)
output_pmf[ 0] = pmf.P(0.100, 1.0)
output_pmf[ 1] = pmf.P(0.300, 1.0)
output_pmf[ 2] = pmf.P(0.500, 1.0)
output_pmf[ 3] = pmf.P(0.700, 1.0)
output_pmf[ 4] = pmf.P(0.900, 1.0)
output_pmf.normalize() 

# generate an array of output_pmfs for each church program
outputs = [0]*len(models)
for m in range(len(models)) :
    outputs[m] = copy.deepcopy(output_pmf)

# define the query time for each church program
query = [0]*len(models)
query[0] = "mh-query"
query[1] = "enumeration-query"
query[2] = "rejection-query"

# define the exeuction path of church
church_exec_path = "/opt/webchurch/church"

# define input space
# -- the first input is a symbolic list of four values
# -- the second input is a boolean value
i_syms = ['alpha', 'beta', 'gamma', 'delta']
i_bools = ['0', '1']

# iterate over all possible inputs
for i_sym in i_syms :
    for i_bool in i_bools :
        # generate the inputs as a comma-separated list
        inputs = i_sym + ',' + i_bool

        # for each model, execute the church program
        for m in range(len(models)) :
            church.exec_model(models[m].x, inputs, outputs[m], query[m], \
                              church_exec_path, church.Type._float)

        # using the computed output distribution, compute and print the expected KL-divergence for each input
        expected_kl = oed.get_expected_kl(models, outputs)
        print inputs, " = ", expected_kl

