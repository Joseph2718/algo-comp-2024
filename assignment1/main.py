#!usr/bin/env python3
import json
import sys
import os
from math import sqrt

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

users_data_json = '''
{
  "users": [
    {
      "name": "Alex",
      "gradYear": 2024,
      "gender": "M",
      "preferences": ["F"],
      "responses": [1, 1, 2, 0, 3, 2, 1, 4, 2, 4, 1, 1, 0, 3, 4, 1, 2, 1, 4, 4]
    },
    {
      "name": "Anurag",
      "gradYear": 2023,
      "gender": "M",
      "preferences": ["F"],
      "responses": [1, 3, 2, 0, 3, 3, 2, 2, 2, 4, 0, 3, 1, 1, 0, 0, 1, 4, 4, 3]
    },
    {
      "name": "Ashley",
      "gradYear": 2023,
      "gender": "F",
      "preferences": ["M"],
      "responses": [0, 0, 3, 0, 0, 3, 4, 0, 0, 4, 3, 4, 2, 1, 0, 0, 0, 2, 2, 0]
    },
    {
      "name": "Chelsea",
      "gradYear": 2024,
      "gender": "F",
      "preferences": ["M"],
      "responses": [3, 3, 3, 2, 1, 2, 1, 3, 1, 3, 3, 4, 4, 3, 1, 2, 2, 0, 2, 2]
    },
    {
      "name": "Chiara",
      "gradYear": 2022,
      "gender": "F",
      "preferences": ["M"],
      "responses": [3, 2, 1, 2, 3, 1, 4, 3, 2, 1, 2, 0, 0, 2, 3, 4, 1, 4, 1, 1]
    },
    {
      "name": "Jeremy",
      "gradYear": 2024,
      "gender": "M",
      "preferences": ["F"],
      "responses": [4, 4, 3, 0, 4, 5, 1, 5, 0, 3, 3, 1, 4, 2, 5, 4, 1, 2, 4, 4]
    },
    {
      "name": "Kat",
      "gradYear": 2023,
      "gender": "F",
      "preferences": ["M"],
      "responses": [2, 4, 3, 4, 3, 3, 2, 4, 4, 0, 3, 1, 0, 3, 0, 4, 4, 1, 4, 2]
    },
    {
      "name": "Katherine",
      "gradYear": 2023,
      "gender": "F",
      "preferences": ["M"],
      "responses": [3, 4, 4, 2, 0, 1, 0, 1, 1, 1, 3, 2, 1, 4, 0, 1, 1, 1, 2, 3]
    },
    {
      "name": "Leonard",
      "gradYear": 2024,
      "gender": "M",
      "preferences": ["F"],
      "responses": [0, 3, 0, 1, 5, 0, 3, 1, 1, 2, 0, 1, 0, 1, 3, 4, 2, 2, 4, 0]
    },
    {
      "name": "Melissa",
      "gradYear": 2022,
      "gender": "F",
      "preferences": ["M"],
      "responses": [0, 3, 3, 3, 0, 3, 4, 4, 2, 2, 3, 4, 2, 2, 0, 2, 0, 5, 0, 0]
    },
    {
      "name": "Quan",
      "gradYear": 2023,
      "gender": "M",
      "preferences": ["F"],
      "responses": [0, 2, 2, 0, 2, 4, 4, 4, 1, 0, 3, 1, 1, 1, 1, 1, 0, 1, 3, 2]
    },
    {
      "name": "Tarun",
      "gradYear": 2023,
      "gender": "M",
      "preferences": ["F"],
      "responses": [1, 1, 4, 2, 4, 2, 3, 2, 3, 2, 4, 1, 1, 2, 2, 4, 3, 2, 1, 1]
    }
  ]
}
'''

users_data = json.loads(users_data_json)
question_distribution = [{'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0} for _ in range(20)]

for user in users_data['users']:
    responses = user['responses']
    for question_index, response in enumerate(responses):

        response_key = str(response)
        if response_key in question_distribution[question_index]:
            question_distribution[question_index][response_key] += 1

formatted_distribution = []
for question_index, counts in enumerate(question_distribution):
    formatted_distribution.append({
        'question': question_index + 1, 
        'counts': counts
    })

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses

def cosine_similarity(v1, v2):
    sum_xx, sum_xy, sum_yy = 0, 0, 0
    for i in range(len(v1)):
        x, y = v1[i], v2[i]
        sum_xx += x * x
        sum_yy += y * y
        sum_xy += x * y
    denominator = sqrt(sum_xx * sum_yy)
    if not denominator:
        return 0.0
    else:
        return sum_xy / denominator

def compare_responses(response1, response2, question_distribution):
    total_same = 0
    weighted_score = 0.0
    for i in range(len(response1)):
        if response1[i] == response2[i]:
            total_same += 1
            weighted_score += 1.0 / (1.0 + question_distribution[i][response1[i]])
    if total_same == 0:
        return 0.0 
    else:
        return weighted_score / total_same


def grad_year_comparison(year1, year2, gender1, gender2):
    # pretty basic, lowkey unsure of how to take gender into account rn
    year_difference = abs(year1 - year2)
    year_constant = 0.1
    score = 1.0 / (1.0 + year_constant * year_difference)
    return score


# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2, question_distribution):
    score = 0.0
    if user1.gender in user2.preferences and user2.gender in user1.preferences:
        score += 0.1
    answer_similarity = cosine_similarity(user1.responses, user2.responses)
    answer_similarity_weighted = compare_responses(user1.responses, user2.responses, question_distribution)

    grad_year_score = grad_year_comparison(user1.grad_year, user2.grad_year, user1.gender, user2.gender)

    score += answer_similarity * 0.6  # 60% weight
    score += answer_similarity_weighted * 0.2  # 20% weight
    score += grad_year_score * 0.1  # 10% weight

    score = max(0.0, min(score, 1.0)) 

    return score


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    question_distribution = []  # Placeholder for the question distribution data

    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

        if 'question_distribution' in data:
            question_distribution = data['question_distribution']
        else:
            print("No question distribution data found in the input file.")
            sys.exit(1)  # Exit with an error code

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2, question_distribution)  # Now passing question_distribution
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))

