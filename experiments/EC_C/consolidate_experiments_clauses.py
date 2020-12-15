import os
import math
import re

# set these variables according to your experiments #
dirpath = 'data/'
experiments_type = [
#  'flat_big',
#'tilted_big',
 'plastic_big'
#,'baseline_big'
]
environments = {
#  'flat_big': ['plane'],
#'tilted_big': ['tilted5'],
  'plastic_big': ['plane','tilted5']
# ,'baseline_big': ['plane','tilted5']
                 }
runs = range(1,21)
#Set hardcoded to True or False, whether the regulation of the clauses was harcoded
hardcoded = False


# set these variables according to your experiments #

def get_clauses(path3):
    # function to get the clauses from the genotype txt file to use as input for the true_clauses() function
    file = open(path3, 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        #change ]] into a letter that does not occur in the genotype to be able to extract the clause
        pre_clauses = re.sub("]]", "q", line)
        # select clauses
        clauses = re.findall("'hill', '==',.{4,36}eq", pre_clauses)

    return clauses

def true_clauses(clauses, env, hardcoded):
    #function to calculate the number of true clauses
    n_clauses = 0
    for i in range(0, len(clauses)):
        if not hardcoded:
            if env == 'tilted5':
                if 'and' in clauses[i] and 'True' in clauses[i] and 'False' not in clauses[i]:
                    n_clauses += 1
                elif 'or' in clauses[i] and 'True' in clauses[i]:
                    n_clauses += 1
                elif 'True' in clauses[i] and 'and' not in clauses[i] and 'or' not in clauses[i]:
                    n_clauses += 1
            elif env == 'plane':
                if 'and' in clauses[i] and 'False' in clauses[i] and 'True' not in clauses[i]:
                    n_clauses += 1
                elif 'or' in clauses[i] and 'False' in clauses[i]:
                    n_clauses += 1
                elif 'Flase' in clauses[i] and 'and' not in clauses[i] and 'or' not in clauses[i]:
                    n_clauses += 1
        elif hardcoded:
            if env == 'tilted5':
                if i % 2:
                    n_clauses += 1
            elif env == 'plane':
                if not i % 2:
                    n_clauses += 1

    return n_clauses

def build_headers(path1a, path1b, path2a, path2b):
    file_summary = open(path1a + "/all_measures.tsv", "w+")
    file_summary.write('robot_id\t')

    behavior_headers = []
    behavior_headers.append('velocity')
    file_summary.write(behavior_headers[-1]+'\t')
    behavior_headers.append('displacement_velocity')
    file_summary.write(behavior_headers[-1]+'\t')
    behavior_headers.append('displacement_velocity_hill')
    file_summary.write(behavior_headers[-1]+'\t')
    behavior_headers.append('head_balance')
    file_summary.write(behavior_headers[-1]+'\t')
    behavior_headers.append('contacts')
    file_summary.write(behavior_headers[-1]+'\t')
    # use this instead? but what if the guy is none?
    # with open(path + '/data_fullevolution/descriptors/behavior_desc_robot_1.txt') as file:
    #     for line in file:
    #         measure, value = line.strip().split(' ')
    #         behavior_headers.append(measure)
    #         file_summary.write(measure+'\t')

    phenotype_headers = []
    with open(path1b + '/descriptors/phenotype_desc_robot_1.txt') as file:
        for line in file:
            measure, value = line.strip().split(' ')
            phenotype_headers.append(measure)
            file_summary.write(measure+'\t')
    file_summary.write('n_true_clauses\t')
    file_summary.write('fitness\t cons_fitness\n')
    file_summary.close()

    file_summary = open(path2a + "/snapshots_ids.tsv", "w+")
    file_summary.write('generation\trobot_id\n')
    file_summary.close()

    return behavior_headers, phenotype_headers

for exp in experiments_type:

    for env in environments[exp]:

        for run in runs:

            path0 = '/storage/karine/journal2/' + exp + "_" + str(run) + '/data_fullevolution'
            path1a = dirpath + exp + "_" + str(run) + '/data_fullevolution/' + env
            path1b = '/storage/karine/journal2/' + exp + "_" + str(run) + '/data_fullevolution/' + env
            path2a = dirpath + exp + "_" + str(run) + '/selectedpop_' + env
            path2b = '/storage/karine/journal2/' + exp + "_" + str(run) + '/selectedpop_' + env
            path3 = '/storage/karine/journal2/' + exp + "_" + str(run) + '/data_fullevolution/genotypes/genotype_robot_'

            behavior_headers, phenotype_headers = build_headers(path1a, path1b, path2a, path2b)

            file_summary = open(path1a + "/all_measures.tsv", "a")
            for r, d, f in os.walk(path0+'/consolidated_fitness'):
                for file in f:

                    robot_id = file.split('.')[0].split('_')[-1]
                    file_summary.write(robot_id+'\t')

                    bh_file = path1b+'/descriptors/behavior_desc_robot_'+robot_id+'.txt'
                    if os.path.isfile(bh_file):
                        with open(bh_file) as file:
                            for line in file:
                                if line != 'None':
                                    measure, value = line.strip().split(' ')
                                    file_summary.write(value+'\t')
                                else:
                                    for h in behavior_headers:
                                        file_summary.write('None'+'\t')
                    else:
                        for h in behavior_headers:
                            file_summary.write('None'+'\t')

                    pt_file = path1b+'/descriptors/phenotype_desc_robot_'+robot_id+'.txt'
                    if os.path.isfile(pt_file):
                        with open(pt_file) as file:
                            for line in file:
                                measure, value = line.strip().split(' ')
                                file_summary.write(value+'\t')
                    else:
                        for h in phenotype_headers:
                            file_summary.write('None'+'\t')

                    clauses = get_clauses(path3 + robot_id + '.txt')
                    n_true_clauses = str(true_clauses(clauses, env, hardcoded))
                    file_summary.write(n_true_clauses + '\t')

                    f_file = open(path1b+'/fitness/fitness_robot_'+robot_id+'.txt', 'r')
                    fitness = f_file.read()
                    file_summary.write(fitness + '\t')

                    cf_file = open(path0+'/consolidated_fitness/consolidated_fitness_robot_'+robot_id+'.txt', 'r')
                    cons_fitness = cf_file.read()
                    file_summary.write(cons_fitness + '\n')

            num_files = len(f)
            list_gens = []
            for r, d, f in os.walk(path2b):
                for dir in d:
                    if 'selectedpop' in dir:
                        gen = dir.split('_')[1]
                        list_gens.append(int(gen))
            list_gens.sort()
            if len(list_gens)>0:
                gen = list_gens[-1]
            else:
                gen = -1
            print(exp, run, num_files, gen, num_files-(gen*100+100))

            file_summary.close()

            file_summary = open(path2a + "/snapshots_ids.tsv", "a")
            for r, d, f in os.walk(path2b):
                for dir in d:
                    if 'selectedpop' in dir:
                        gen = dir.split('_')[1]
                        for r2, d2, f2 in os.walk(path2b + '/selectedpop_' + str(gen)):
                            for file in f2:
                                if 'body' in file:
                                    id = file.split('.')[0].split('_')[-1]
                                    file_summary.write(gen+'\t'+id+'\n')

            file_summary.close()
