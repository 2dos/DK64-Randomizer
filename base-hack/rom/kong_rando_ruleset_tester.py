"""Generate list of all permutations for Kong Rando with a given ruleset."""

import math

traps = ["japes", "llama", "icetemple", "factory"]
trap_names = ["Jungle Japes", "Llama Temple", "Tiny Temple", "Frantic Factory"]
roles = ["lock", "puzz"]
role_names = ["Locked", "Puzzle"]


def numToBase(n, b, d):
    """Convert number n to base b with number of digits d."""
    if n == 0:
        digits = [0]
    else:
        digits = []
        while n:
            digits.append(int(n % b))
            n //= b
    if len(digits) < d:
        diff = d - len(digits)
        for x in range(diff):
            digits.append(0)
    return digits[::-1]


random_ruleset = {
    "starting": [0, 1, 2, 3, 4],
    "japes": {
        "lock": [0, 1, 2, 3, 4],
        "puzz": [0, 1, 2, 3, 4],
    },
    "llama": {
        "lock": [0, 1, 2, 3, 4],
        "puzz": [0, 2, 3],
    },
    "icetemple": {
        "lock": [0, 2, 3, 4],
        "puzz": [1],
    },
    "factory": {
        "lock": [0, 1, 2, 3, 4],
        "puzz": [2, 3],
    },
}

random_ruleset_free_llama_temple = {
    "starting": [0, 1, 2, 3, 4],
    "japes": {
        "lock": [0, 1, 2, 3, 4],
        "puzz": [0, 1, 2, 3, 4],
    },
    "llama": {
        "lock": [0, 1, 2, 3, 4],
        "puzz": [0, 1, 2, 3, 4],
    },
    "icetemple": {
        "lock": [0, 2, 3, 4],
        "puzz": [1],
    },
    "factory": {
        "lock": [0, 1, 2, 3, 4],
        "puzz": [2, 3],
    },
}

vanilla_ruleset = {
    "starting": [0, 1, 2, 3, 4],
    "japes": {
        "lock": [0, 1, 2, 3, 4],
        "puzz": [0, 1, 2, 3, 4],
    },
    "llama": {
        "lock": [1, 2, 3, 4],
        "puzz": [0],
    },
    "icetemple": {
        "lock": [0, 2, 3, 4],
        "puzz": [1],
    },
    "factory": {
        "lock": [0, 1, 3, 4],
        "puzz": [2],
    },
}

expanded_random = {
    "starting": [0, 1, 2, 3, 4],
    "japes": {
        "lock": [0, 1, 2, 3, 4],
        "puzz": [0, 1, 2, 3, 4],
    },
    "llama": {
        "lock": [0, 1, 2, 3, 4],
        "puzz": [0, 1, 2, 3, 4],
    },
    "icetemple": {
        "lock": [0, 1, 2, 3, 4],
        "puzz": [1, 4],
    },
    "factory": {
        "lock": [0, 1, 2, 3, 4],
        "puzz": [0, 1, 2, 3, 4],
    },
}

ruleset = expanded_random

total_perm = 0
checks = 0
fail_by_invalid_lock = 0
fail_by_unreachable_kongs = 0
fail_by_nonmatching_ruleset = 0
total_verif = 0
unreach_kongs_total = [0, 0, 0, 0, 0, 0]
balance = {
    "starting": [0, 0, 0, 0, 0],
    "japes": {
        "lock": [0, 0, 0, 0, 0],
        "puzz": [0, 0, 0, 0, 0],
    },
    "llama": {
        "lock": [0, 0, 0, 0, 0],
        "puzz": [0, 0, 0, 0, 0],
    },
    "icetemple": {
        "lock": [0, 0, 0, 0, 0],
        "puzz": [0, 0, 0, 0, 0],
    },
    "factory": {
        "lock": [0, 0, 0, 0, 0],
        "puzz": [0, 0, 0, 0, 0],
    },
}


def verifyBeatable(info):
    """Verify assortment is beatable, and filter non-beatable seeds."""
    global fail_by_unreachable_kongs
    global fail_by_invalid_lock
    global fail_by_nonmatching_ruleset
    locked = []
    locked.append(info["starting"])
    locked.append(info["japes"]["lock"])
    locked.append(info["llama"]["lock"])
    locked.append(info["icetemple"]["lock"])
    locked.append(info["factory"]["lock"])
    # All Kongs locked up
    for x in range(5):
        if x not in locked:
            fail_by_invalid_lock += 1
            return False
    # Verify assortment matches ruleset
    if info["starting"] not in ruleset["starting"]:
        return False
    for trap in traps:
        for role in roles:
            if info[trap][role] not in ruleset[trap][role]:
                fail_by_nonmatching_ruleset += 1
                return False
    # Can get all kongs without KKO
    used_up = []
    kongs_access = [info["starting"]]
    for kong in range(5):
        for trap in traps:
            if info[trap]["puzz"] in kongs_access and trap not in used_up:
                used_up.append(trap)
                kongs_access.append(info[trap]["lock"])
    for kong in range(5):
        if kong not in kongs_access:
            fail_by_unreachable_kongs += 1
            unreach_kongs_total[len(kongs_access)] += 1
            return False
    return True


def printPerm(lst, name):
    """Print permutations."""
    temp = [0, 0, 0, 0, 0]
    for x in range(5):
        if total_perm == 0:
            perc = 0
        else:
            perc = (lst[x] * 100) / total_perm
        perc = math.floor(perc * 100)
        perc /= 100
        temp[x] = str(perc) + "%"
    print(f"{name}: {str(temp)}")


for permutation in range(int(math.pow(5, 5))):
    kong_unlocks = numToBase(permutation, 5, 5)
    cont = True
    for x in range(5):
        if x not in kong_unlocks:
            cont = False
    if cont:
        checks += 1
        for sub_perm in range(int(math.pow(5, 4))):
            kong_puzzle = numToBase(sub_perm, 5, 4)
            base5 = []
            for x in range(9):
                base5.append(0)
            base5[0] = kong_unlocks[0]
            for x in range(4):
                base5[1 + (2 * x)] = kong_unlocks[x + 1]
                base5[2 + (2 * x)] = kong_puzzle[x]
            info = {
                "starting": base5[0],
            }
            index = 1
            for trap in traps:
                info[trap] = {"lock": base5[index], "puzz": base5[index + 1]}
                index += 2
            total_verif += 1
            passes = verifyBeatable(info)
            if passes:
                balance["starting"][info["starting"]] += 1
                for trap in traps:
                    for role in roles:
                        balance[trap][role][info[trap][role]] += 1
                total_perm += 1

print(f"Total Verifications: {total_verif}")
print(f"Fail (Invalid Lock): {fail_by_invalid_lock}")
print(f"Fail (Unreachable Kongs): {fail_by_unreachable_kongs}")
print(f"Fail (Ruleset): {fail_by_nonmatching_ruleset}")
print("Unreachable Kongs Count:")
for x in range(6):
    print(f"\t{5 - x} Kongs: {unreach_kongs_total[x]}")
print(f"Total Permutations: {total_perm}")
printPerm(balance["starting"], "Starting Kong")
for x in range(4):
    trap = traps[x]
    trap_name = trap_names[x]
    for y in range(2):
        role = roles[y]
        role_name = role_names[y]
        printPerm(balance[trap][role], f"{trap_name} - {role_name}")
