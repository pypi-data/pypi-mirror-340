import json
import numpy as np
import pandas as pd
import random
import pickle
from sklearn.ensemble import RandomForestClassifier

df = pd.read_pickle("sequence_data/sample_sequences.csv")

# gets list of amino acid letters and creates dictionaries for their one hot encodings
lets = np.unique(list(df.numbered_seq.values[0]+df.numbered_seq.values[1]+df.numbered_seq.values[2]))
lets = [l for l in lets if l != '-']
let_to_hot = {}
hot_to_let = {}
alph_size = len(lets)
for i in range(alph_size):
    coded = np.zeros(alph_size+1)
    coded[i] = 1
    let_to_hot[lets[i]] = coded
    hot_to_let[str(coded)] = lets[i]
coded = np.zeros(alph_size+1)
coded[alph_size] = 1
let_to_hot['-'] = coded
hot_to_let[str(coded)] = '-'


def one_hot(seq):
    """ inputs: seq, string, sequence to be encoded
        outputs: coded, numpy array, encoded sequence
    """
    try:
        coded = let_to_hot[seq[0]]
    except:
        return pd.NA
        
    for l in seq[1:]:
        try:
            coded = np.concatenate((coded,let_to_hot[l]))
        except:
            return pd.NA
    return coded

def decode(one_hot):
    """ inputs: one_hot, numpy array, encoded sequence
        outputs: string, decoded sequence
    """ 
    if len(one_hot) == 21:
        return hot_to_let[str(one_hot)]
    else:
        return hot_to_let[str(one_hot[:21])] + decode(one_hot[21:])

# amino acid alphabet and non cdr region indices
alphabet = pd.DataFrame(np.concatenate((lets,['-']))).apply(lambda x: x[0],axis=1)
non_cdr_reg = list(range(1,27))+list(range(39,56))+list(range(66,105))+list(range(118,129))


def random_proposer(seq, i, num_mutation_per_step):
    """ inputs: seq, string, sequence to change
                i, int, index of where to mutate
                num_mutation_per_step, int, number of amino acids to mutate in a row
        outputs: new_seq, string, randomly mutated sequence
    """
    muts = alphabet.sample(n=num_mutation_per_step).values
    while np.sum([(muts[n] == seq[i+n]) for n in range(num_mutation_per_step)]) != 0 or np.sum([1 for n in range(num_mutation_per_step) if muts[n] == '-']) != 0:
        muts = alphabet.sample().values

    new_seq = [aa for aa in seq]
    for n in range(num_mutation_per_step):
        new_seq[i+n] = muts[n]

    return new_seq

def humanness_score(orig_seq, v_models):
    """ inputs: orig_seq, string, sequence to be scored
                v_models, dictionary of trained sklearn models, trained RF models for each v gene type
        outputs: best_v, int, v gene type that resulted in the highest score
                 best_prob, double, highest humanness score from the models
    """
    enc = one_hot(orig_seq)
    seq = list(orig_seq)
    best_prob = 0
    best_v = None
    for v_type in range(1,8):
        pred = v_models[v_type].predict_proba([enc])[0][1]
        if pred > best_prob:
            best_prob = pred
            best_v = v_type

    return best_v, best_prob

def get_best_mut(orig_seq, seq, start_prob, best_v, v_models, check_all_muts, sequence_proposer, num_mutation_per_step):
    """ inputs: orig_seq, string, fully unmutated sequence
                seq, string, current sequence that is going to be mutated
                start_prob, double, humanness score of the current sequence
                best_v, int, which v gene type to use for the models
                v_models, dictionary of trained sklearn models, trained RF models for each v gene type
                check_all_muts, bool, true if we are checking every possible mutation
                                      false if we are using a particular sequence proposer
                sequence_proposer, function, sequence proposer to use if check_all_muts is false
        outputs: new_seq, string, mutated sequence with highest humanness score
                 best_prob, double, humanness score of new_seq
    """
    best_mut_prob = 0
    best_mut = None
    # only mutates in non cdr regions
    for i in non_cdr_reg:
        # finds right indexing value
        i = i - 1
        if seq[i]=='-':
            continue
        
        # checks all possible mutations
        if check_all_muts:
            for let in lets:
                if let == seq[i]:
                    continue
                new_seq = [aa for aa in seq]
                new_seq[i] = let
                
                mut_enc = one_hot(new_seq)
                mut_score = v_models[best_v].predict_proba([mut_enc])[0][1]
        
                if mut_score > best_mut_prob:
                    best_mut_prob = mut_score
                    best_mut = new_seq

                # monte carlo methods
                elif (np.exp(-(best_mut_prob - mut_score)) > np.random.rand()):
                    best_mut = new_seq
        # checks using a sequence proposed
        else:
            new_seq = sequence_proposer(seq, i, num_mutation_per_step)

            mut_enc = one_hot(new_seq)
            mut_score = v_models[best_v].predict_proba([mut_enc])[0][1]
    
            if (mut_score > best_mut_prob):
                best_mut_prob = mut_score
                best_mut = new_seq

            # monte carlo methods
            elif (np.exp(-(best_mut_prob - mut_score)) > np.random.rand()):
                best_mut = new_seq

    # accepts the best mutation
    if best_mut_prob > start_prob:
        best_prob = best_mut_prob
        new_seq = best_mut
        num_muted = np.sum([l1!=l2 for l1,l2 in zip(list(orig_seq),new_seq)])
        print(str(num_muted) + ': ' + str(best_prob))

    # monte carlo methods
    elif (np.exp(-(start_prob - best_mut_prob)) > np.random.rand()):
        best_prob = start_prob
        new_seq = best_mut
        num_muted = np.sum([l1!=l2 for l1,l2 in zip(list(orig_seq),new_seq)])
        print(str(num_muted) + ': ' + str(best_prob))

    # no improvement possible given mutations check
    else:
        best_prob = start_prob
        new_seq = seq

    return new_seq, best_prob

def load_models(forced):
    """ inputs: forced, bool, true if using the forced distance models
                              false if using the all data models
        outputs: v_models, dictionary of sklearn models
    """
    if forced:
        kw = 'forced'
    else:
        kw = 'all'
    
    v_models = {}
    for i in range(1,8):
        filename = 'saved_models/v' + str(i) + '_model_' + kw + '.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        v_models[i] = loaded_model

    return v_models
    

def humanize_sequence(orig_seq, desired_score, v_models, max_desired_mutations=10, 
                      num_mutation_per_step=1, check_all_muts = True, sequence_proposer=None, 
                      use_known_v_type = False, known_v_type = None):
    """ inputs: orig_seq, string, fully unmutated sequence that is in the universal mapping already
                desired_score, double, desired humanness score threshold to reach
                v_models, dictionary of trained sklearn models, trained RF models for each v gene type
                max_desired_mutations, int, maximum mutations allowed
                num_mutation_per_step, int, number of mutations in each step
                check_all_muts, bool, true if we are checking every possible mutation
                                      false if we are using a particular sequence proposer
                sequence_proposer, function, sequence proposer to use if check_all_muts is false
                use_known_v_type, bool, true if we are give the v gene type to use for a sequence
                known_v_type, int, known v type model to use to humanize the sequence
        outputs: string, humanized sequence
                 best_prob, double, humanness score of humanized sequence
    """
    # encode sequence
    enc = one_hot(orig_seq)
    seq = list(orig_seq)

    if use_known_v_type:
        # using known v gene type model
        best_v = known_v_type
        best_prob = v_models[best_v].predict_proba([enc])[0][1]
    else:
        # check to find the best v type for the sequence
        best_prob = 0
        best_v = None
        for v_type in range(1,8):
            pred = v_models[v_type].predict_proba([enc])[0][1]
            if pred > best_prob:
                best_prob = pred
                best_v = v_type

        # if none of the models score it higher than 0
        # check to find the best score after one mutation for each model
        if best_v == None:
            for v_type in range(1,8):
                v_seq, v_prob = get_best_mut(orig_seq, seq, best_prob, v_type, v_models, check_all_muts,sequence_proposer, num_mutation_per_step)
                if v_prob > best_prob:
                    best_prob = v_prob
                    seq = v_seq
                    best_v = v_type
    print('V'+str(best_v))
    
    print('0: ' + str(best_prob))
    num_muted = 0

    # # uncomment if considering a maximum number of mutations
    # while best_prob < desired_score and num_muted < max_desired_mutations:
    i = 0
    while best_prob < desired_score:
        # mutate until the desired_score threshold is reached
        seq, best_prob = get_best_mut(orig_seq, seq, best_prob, best_v, v_models, check_all_muts, sequence_proposer, num_mutation_per_step)
        i += 1
        if i > max_desired_mutations+10:
            print("could not improve further")
            break

    return ''.join(seq), best_prob