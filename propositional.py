import re

def negation(term):
    return f'~{term}' if term[0] != '~' else term[1]

def revv(clause):
    if len(clause) > 2:
        t = split_exp(clause)
        return f'{t[1]}v{t[0]}'
    return 

def split_exp(rule):
    exp = '(~*[PQRS])'
    terms = re.findall(exp, rule)
    return terms

split_exp('~PvR')

def con(goal, clause):
    cons = [ f'{goal}v{negation(goal)}', f'{negation(goal)}v{goal}']
    return clause in cons or revv(clause) in cons
    
def solve(rules, goal):
    temp = rules.copy()
    temp += [negation(goal)]
    steps = dict()
    for rule in temp:
        steps[rule] = 'Given.'
    steps[negation(goal)] = 'negationd conclusion.'
    i = 0
    while i < len(temp):
        n = len(temp)
        j = (i + 1) % n
        clauses = []
        while j != i:   
            terms1 = split_exp(temp[i])
            terms2 = split_exp(temp[j])
            for c in terms1:
                if negation(c) in terms2:
                    t1 = [t for t in terms1 if t != c]
                    t2 = [t for t in terms2 if t != negation(c)]
                    gen = t1 + t2
                    if len(gen) == 2:
                        if gen[0] != negation(gen[1]):
                            clauses += [f'{gen[0]}v{gen[1]}']
                        else:
                            if con(goal,f'{gen[0]}v{gen[1]}'):
                                temp.append(f'{gen[0]}v{gen[1]}')
                                steps[''] = f"Solved {temp[i]} and {temp[j]} to {temp[-1]}, hence is null. \
                                \ncon when {negation(goal)} is true. So {goal} is true."
                                return steps
                    elif len(gen) == 1:
                        clauses += [f'{gen[0]}']
                    else:
                        if con(goal,f'{terms1[0]}v{terms2[0]}'):
                            temp.append(f'{terms1[0]}v{terms2[0]}')
                            steps[''] = f"Solved {temp[i]} and {temp[j]} to {temp[-1]}, hence is null. \
                            \ncon when {negation(goal)} is true. So {goal} is true."
                            return steps
            for clause in clauses:
                if clause not in temp and clause != revv(clause) and revv(clause) not in temp:
                    temp.append(clause)
                    steps[clause] = f'Solved from {temp[i]} and {temp[j]}.'
            j = (j + 1) % n
        i += 1
    return steps

def main(rules, goal):
    rules = rules.split(' ')
    steps = solve(rules, goal)
    print('\nStep\t|Clause\t|Derivation\t')
    print('~' * 30)
    i = 1
    for step in steps:
        print(f' {i}.\t| {step}\t| {steps[step]}\t')
        i += 1
        

rules = input("Enter the knowledge base 'use whitespace' :")
query=input("query: ")
main(rules, query)
    
    
