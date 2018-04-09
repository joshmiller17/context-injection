#
# This file parses the survey results CSV and generates the following
# evaluation statistics:
#
# in all results, an array of 6 elements corresponds to the questions in the
# following order:
#
# I think this phrase would be considered jargon
# I think this phrase is relevant to the domain
# This phrase has a definition
# This definition seems correct (matches and describes phrase)
# This definition is useful for learning about the domain
# This was a duplicate of a previous phrase
#
# avg_agreement_by_q: this is the average agreement over all pairs
#   of participants for each question
# avg_agreement_overall: this is the average agreement over all participants
#   for all questions
# avg_results_by_domain: this is the average positive response rate for each
#   question divided by domain. The results are provided in a dictionary with
#   the key corresponding to the domain
# avg_results_overall: this is the average positive response rate for each
#   question for all domains combined
#

import pandas as pd
import numpy as np
from collections import defaultdict
import re
import math
from itertools import combinations

stats = defaultdict(lambda: np.zeros(6))
stats_by_domain = defaultdict(lambda : defaultdict(lambda: np.zeros(6)))

def parse_answer(answer):
    full_answer = ['Ithinkthisphrasewouldbeconsideredjargon', \
                   'Ithinkthisphraseisrelevanttothedomain', \
                   'Thisphrasehasadefinition', \
                   'Thisdefinitionseemscorrect(matchesanddescribesphrase)', \
                   'Thisdefinitionisusefulforlearningaboutthedomain', \
                   'Thiswasaduplicateofapreviousphrase']
    responses = np.zeros(6)
    if type(answer) == type(0.0) and math.isnan(answer):
        #no answers were selected
        return responses
    #correct for variation in question phrasing
    individual_answers = re.sub("\s*", "", answer)
    individual_answers = re.sub("Thedefinition", "Thisdefinition", individual_answers)
    individual_answers = individual_answers.split(';')
    for i, a in enumerate(full_answer):
        if a in individual_answers:
            responses[i] = 1
    return responses

df = pd.read_csv('NLP Participant Survey.csv')

questions = df.axes[1][1:]
for question in questions:
    match = re.match(r"The domain is: (.*) \[(.*)\]", question)
    domain = match.group(1)
    phrase = match.group(2)
    for i, participant in df.iterrows():
        answer = participant[question]
        response = parse_answer(answer)
        stats[phrase] += response
        stats_by_domain[domain][phrase] += response

avg_agreement_by_q = np.zeros(6)
avg_agreement_overall = 0
for p1, p2 in combinations(df.iterrows(), 2):
    p1 = p1[1]
    p2 = p2[1]
    agreement = np.zeros(6)
    for question in questions:
        match = re.match(r"The domain is: (.*) \[(.*)\]", question)
        domain = match.group(1)
        phrase = match.group(2)
        answer1 = p1[question]
        answer2 = p2[question]
        response1 = parse_answer(answer1)
        response2 = parse_answer(answer2)
        agreement += np.ones(6) - np.abs(response1-response2)
    agreement_by_q = agreement/len(questions)
    agreement_overall = sum(agreement)/(len(questions)*6)
    avg_agreement_by_q += agreement_by_q
    avg_agreement_overall += agreement_overall
num_combos = math.factorial(len(df.axes[0])) / math.factorial(2) / math.factorial(len(df.axes[0])-2)
avg_agreement_by_q = avg_agreement_by_q/num_combos
avg_agreement_overall = avg_agreement_overall/num_combos

avg_results_by_domain = defaultdict(lambda: np.zeros(6))
for domain in stats_by_domain.keys():
    for response in stats_by_domain[domain].values():
        avg_results_by_domain[domain] += response
    avg_results_by_domain[domain] = avg_results_by_domain[domain]/ \
                                    (len(stats_by_domain[domain])*len(df.axes[0]))

avg_results_overall = np.zeros(6)
for response in stats.values():
    avg_results_overall += response
avg_results_overall = avg_results_overall/ \
                      (len(stats)*len(df.axes[0]))

print('Average positive response rate by domain:')
for domain, results in avg_results_by_domain.items():
    print(domain)
    print(results)
print('Average positive response rate over all domains:')
print(avg_results_overall)
print('Average agreement for each question')
print(avg_agreement_by_q)
print('Average agreement over all questions')
print(avg_agreement_overall)
