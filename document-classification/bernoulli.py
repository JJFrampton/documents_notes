#!/bin/python3

import copy

vocabulary = ['hired', 'fired', 'lazy', 'slow', 'happy', 'sad', 'strong', 'quick']
feature_vectors = [0,0,0,0,0,0,0,0]

r1 = {
    'doc': 'hello the i would like to get hired im happy and strong but sometimes sad',
    'class': 'h'
}
r2 = {
    'doc': 'hello the i would like to get hired or fired im lazy and slow but sometimes quick',
    'class': 'h'
}
r3 = {
    'doc': 'hello the i would like to get hired im strong and quick',
    'class': 'h'
}
r4 = {
    'doc': 'hello the i would like to get hired very quick happy',
    'class': 'h'
}
r5 = {
    'doc': 'I was fired from my last job because i was really lazy',
    'class': 'r'
}
r6 = {
    'doc': 'I was fired from my last job because i was slow and sad',
    'class': 'r'
}
r7 = {
    'doc': 'I was fired or hired from my last job because i was really sad',
    'class': 'r'
}

docs = [r1,r2,r3,r4,r5,r6,r7]

for index, item in enumerate(docs, start=1):
    # print(item['class'])
    item['features'] = item['doc'].split()
    item['feature_vectors'] = copy.copy(feature_vectors)
    for feature in item['features']:
        try:
            result = vocabulary.index(feature)
            item['feature_vectors'][result] = item['feature_vectors'][result] + 1
        except ValueError:
            no=[]
        else:
            no=[]
            # print(feature)
            # print(result)
            # print(item['feature_vectors'])
            # print('ok')


# need to check if any of the totals are 0
# if so then add 1 or less than 1

# print("calculating totals")
totals = {
    'h' : [0,0,0,0,0,0,0,0],
    'r' : [0,0,0,0,0,0,0,0]
}
hn = 0
rn = 0
for doc in docs:
    if doc['class'] == 'h':
        # for vector in doc['feature_vectors']:
        totals['h'] = [x + y for x, y in zip(doc['feature_vectors'], totals['h'])]
        hn = hn + 1
        # print(totals['h'])
    elif doc['class'] == 'r':
        totals['r'] = [x + y for x, y in zip(doc['feature_vectors'], totals['r'])]
        rn = rn + 1
        # print(totals['r'])

n = hn + rn

ph = hn / n
pr = rn / n
# remove 0s and calculate probabilities:

for i, vector in enumerate(totals['h']):
    if vector == 0:
        totals['h'][i] = 1
    totals['h'][i] = totals['h'][i] / hn
for i, vector in enumerate(totals['r']):
    if vector == 0:
        totals['r'][i] = 1
    totals['r'][i] = totals['r'][i] / rn

# print(totals['h'])
# print(totals['r'])

# need to build the function to predict class

new_result = [0,0,0,0,0,0,0,0]

test_data = input('type out a resume : ')
test_data = test_data.split()
for word in test_data:
    try:
        result = vocabulary.index(word)
        new_result[result] = new_result[result] + 1
    except ValueError:
        no=[]
    else:
        no=[]

class_hired = copy.copy(new_result)
class_rejected = copy.copy(new_result)

for i, vector in enumerate(class_hired):
    if vector == 1:
        class_hired[i] = totals['h'][i]
    elif vector == 0:
        class_hired[i] = 1 - totals['h'][i]
    if class_hired[i] == 0:
        class_hired[i] = 0.01

for i, vector in enumerate(class_rejected):
    if vector == 1:
        class_rejected[i] = totals['r'][i]
    elif vector == 0:
        class_rejected[i] = 1 - totals['r'][i]
    if class_rejected[i] == 0:
        class_rejected[i] = 0.01

prob_of_hired = 1.0
prob_of_rejected = 1.0

for vector in class_hired:
    # print(vector)
    prob_of_hired *= vector

for vector in class_rejected:
    # print(vector)
    prob_of_rejected *= vector

prob_of_hired = prob_of_hired * ph
prob_of_rejected = prob_of_rejected * pr

# print(class_hired)
# print(class_rejected)

# print(new_result)
print("probability of class_hired: " + str(prob_of_hired))
print("probability of class_rejected: " + str(prob_of_rejected))
