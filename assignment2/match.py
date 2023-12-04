import numpy as np
from typing import List, Tuple
from collections import deque

def adjust_scores_for_preferences(scores: np.ndarray, genders: List[str], preferences: List[str]) -> np.ndarray:
    """
    Adjust scores based on gender identities and preferences.
    Sets the score to 0 for incompatible gender-preference combinations.
    """
    gender_map = {"Male": "Men", "Female": "Women", "Nonbinary": "Bisexual"}
    for i in range(len(scores)):
        for j in range(len(scores[i])):
            # Set score to 0 if preferences don't match
            if preferences[i] != "Bisexual" and (gender_map[genders[j]] != preferences[i]):
                scores[i][j] = 0
    return scores

def create_preference_lists(scores: np.ndarray) -> List[List[int]]:
    """
    Create preference lists for each user based on scores.
    Higher scores imply higher preference.
    """
    return [list(np.argsort(-scores[i])) for i in range(len(scores))]

def gale_shapley_algorithm(scores: np.ndarray, genders: List[str], preferences: List[str]) -> Tuple[List[Tuple], List[List[int]]]:
    """
    Implement the Gale-Shapley algorithm to find stable matches.
    """
    adjusted_scores = adjust_scores_for_preferences(scores, genders, preferences)
    preference_lists = create_preference_lists(adjusted_scores)

    n = len(scores)
    proposers = deque(range(n // 2))  # First half as proposers
    receivers = set(range(n // 2, n))  # Second half as receivers

    proposals_made = [set() for _ in range(n)]
    matches = [None] * n

    while proposers:
        proposer = proposers.popleft()
        for receiver in preference_lists[proposer]:
            if receiver not in proposals_made[proposer] and receiver in receivers:
                proposals_made[proposer].add(receiver)
                if matches[receiver] is None:
                    matches[proposer] = receiver
                    matches[receiver] = proposer
                    break
                else:
                    current_match = matches[receiver]
                    if preference_lists[receiver].index(proposer) < preference_lists[receiver].index(current_match):
                        matches[proposer] = receiver
                        matches[receiver] = proposer
                        proposers.append(current_match)
                        break

    # Ensure each participant is included in the matches list
    for receiver in receivers:
        if matches[receiver] is None:
            proposer = next(p for p in proposers if receiver in preference_lists[p])
            matches[proposer] = receiver
            matches[receiver] = proposer

    return [(i, matches[i]) for i in range(n // 2)], preference_lists

def is_stable_match(matches, preference_lists):
    for a, b in matches:
        index_b_in_a = preference_lists[a].index(b)
        for preferred in preference_lists[a][:index_b_in_a]:
            current_partner_of_preferred = next((x for x, y in matches if y == preferred), None)
            if current_partner_of_preferred is not None:
                if preference_lists[preferred].index(a) < preference_lists[preferred].index(current_partner_of_preferred):
                    return False

        index_a_in_b = preference_lists[b].index(a)
        for preferred in preference_lists[b][:index_a_in_b]:
            current_partner_of_preferred = next((x for x, y in matches if y == preferred), None)
            if current_partner_of_preferred is not None:
                if preference_lists[preferred].index(b) < preference_lists[preferred].index(current_partner_of_preferred):
                    return False

    return True

def run_matching(scores: List[List[float]], gender_id: List[str], gender_pref: List[str]) -> Tuple[List[Tuple], List[List[int]]]:
    scores_array = np.array(scores)
    return gale_shapley_algorithm(scores_array, gender_id, gender_pref)

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            genders.append(line.strip())

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            gender_preferences.append(line.strip())

    gs_matches, preference_lists = run_matching(raw_scores, genders, gender_preferences)
    print("Matches:", gs_matches)
    print("Stable Match:", is_stable_match(gs_matches, preference_lists))
