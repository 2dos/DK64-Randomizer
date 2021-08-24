"""Randomize your seed via your settings."""
import random

def randomize(banana_groups: list, bananasPerKong: int = 100):
    #For each kong, select random group out of all available groups (vanilla + new)
    #If selected group size is more than remaining bananas for the kong, try next group
    #subtract selected group size from 100 for the kong
    #mark selected group as used so it can't be selected again
    #when all 100 bananas are assigned, move to next kong
    
    groups_remaining = banana_groups.copy()

    kongs = ['dk','diddy','lanky','tiny','chunky']
    kongs_groups = {}

    for kong in kongs:
        print("Begin assigning bananas for " + kong)
        bananas_remaining = bananasPerKong
        kong_groups = []
        iterations = 0
        
        while bananas_remaining > 0 and iterations < 1000:
            iterations += 1
            if len(groups_remaining) == 0:
                print("Ran out of banana groups to choose from!")
                return
            selected_group = random.choice(groups_remaining)
            group_size = selected_group["size"]
            if group_size % 5 != 0:
                groups_remaining.remove(selected_group)
                print("Removing group " + str(selected_group['group']) + " with uneven size of: " + str(group_size))
            else: 
                if group_size <= bananas_remaining and selected_group['kongs'][kong] == True :
                    groups_remaining.remove(selected_group)
                    print(str(len(groups_remaining)) + " groups remaining.")
                    print("Bananas remaining: " + str(bananas_remaining))
                    bananas_remaining -= group_size
                    kong_groups.append(selected_group)
        print("Number of Iterations for " + kong + ": " + str(iterations))
        kongs_groups[kong] = kong_groups
    print("Color Banana Randomization done")
    return kongs_groups
