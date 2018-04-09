import pandas as pd
import numpy as np
from collections import defaultdict
import re
import math

stats = defaultdict(lambda: np.zeros(6))
stats_by_domain = defaultdict(lambda : defaultdict(lambda: np.zeros(6)))

def parse_answer(answer):
    full_answer = ['I think this phrase would be considered jargon', \
                   'I think this phrase is relevant to the domain', \
                   'This phrase has a definition', \
                   'The definition seems correct (matches and describes phrase)', \
                   'This definition is useful for learning about the domain', \
                   'This was a duplicate of a previous phrase']
    responses = np.zeros(6)
    if type(answer) == type(0.0) and math.isnan(answer):
        #no answers were selected
        return responses
    individual_answers = answer.split(';')
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
