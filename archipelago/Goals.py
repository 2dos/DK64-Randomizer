"""Script for determining win conditions."""

from random import Random
import typing

from archipelago.Options import Goal, GoalQuantity, GoalTasks
from randomizer.Enums.Settings import WinConditionComplex

# Goal mapping for wincon determination
GOAL_MAPPING = {
    Goal.option_acquire_keys_3_and_8: WinConditionComplex.get_keys_3_and_8,
    Goal.option_acquire_key_8: WinConditionComplex.get_key8,
    Goal.option_kremling_kapture: WinConditionComplex.krem_kapture,
    Goal.option_dk_rap: WinConditionComplex.dk_rap_items,
    Goal.option_golden_bananas: WinConditionComplex.req_gb,
    Goal.option_blueprints: WinConditionComplex.req_bp,
    Goal.option_company_coins: WinConditionComplex.req_companycoins,
    Goal.option_keys: WinConditionComplex.req_key,
    Goal.option_medals: WinConditionComplex.req_medal,
    Goal.option_crowns: WinConditionComplex.req_crown,
    Goal.option_fairies: WinConditionComplex.req_fairy,
    Goal.option_rainbow_coins: WinConditionComplex.req_rainbowcoin,
    Goal.option_bean: WinConditionComplex.req_bean,
    Goal.option_pearls: WinConditionComplex.req_pearl,
    Goal.option_bosses: WinConditionComplex.req_bosses,
    Goal.option_bonuses: WinConditionComplex.req_bonuses,
    Goal.option_treasure_hurry: WinConditionComplex.req_key,
    Goal.option_krools_challenge: WinConditionComplex.krools_challenge,
    Goal.option_kill_the_rabbit: WinConditionComplex.kill_the_rabbit,
    Goal.option_mechanical_fish: WinConditionComplex.mech_fish,
    Goal.option_dk_arcade: WinConditionComplex.arcade,
    Goal.option_jetpac: WinConditionComplex.jetpac,
    Goal.option_toy_monster: WinConditionComplex.bad_hit_detection_man,
    Goal.option_rareware_gb: WinConditionComplex.rareware_gb_check,
    Goal.option_blast_courses: WinConditionComplex.blast_courses,
    Goal.option_tasks: WinConditionComplex.tasks,
}
# List of goals that care about the quantity field
QUANTITY_GOALS = {
    Goal.option_golden_bananas: "golden_bananas",
    Goal.option_blueprints: "blueprints",
    Goal.option_company_coins: "company_coins",
    Goal.option_keys: "keys",
    Goal.option_medals: "medals",
    Goal.option_crowns: "crowns",
    Goal.option_fairies: "fairies",
    Goal.option_rainbow_coins: "rainbow_coins",
    Goal.option_pearls: "pearls",
    Goal.option_bosses: "bosses",
    Goal.option_bonuses: "bonuses",
    Goal.option_kremling_kapture: "kremling_kapture",
    Goal.option_blast_courses: "blast_courses",
}
# Maximum possible goals for each wincon
QUANTITY_MAX = {
    "golden_bananas": 201,
    "blueprints": 40,
    "company_coins": 2,
    "keys": 8,
    "medals": 40,
    "crowns": 10,
    "fairies": 20,
    "rainbow_coins": 16,
    "pearls": 5,
    "bosses": 7,
    "bonuses": 53,
    "kremling_kapture": 44,
    "blast_courses": 7,
}
TASK_GOALS = {task_name: GOAL_MAPPING[Goal.options[task_name]] for task_name in GoalTasks.max_values_dict}


def calculate_quantity(wincon_name: str, option_value: typing.Any, random: Random):
    """Calculate bounds of wincon value."""
    assert wincon_name in QUANTITY_MAX.keys()
    requested_quantity = option_value.get(wincon_name, GoalQuantity.default[wincon_name])

    try:
        # Try the easy case where this is just a number first
        quantity = int(requested_quantity)
        assert quantity <= QUANTITY_MAX[wincon_name]
        return quantity
    except (TypeError, ValueError):
        # User requested a range, so give them a random option
        assert requested_quantity == "random" or len(requested_quantity.split("-")) == 2
        upper_bound = (QUANTITY_MAX[wincon_name] if requested_quantity == "random" else int(requested_quantity.split("-")[1])) + 1
        lower_bound = 1 if requested_quantity == "random" else int(requested_quantity.split("-")[0])
        return random.randrange(lower_bound, upper_bound)


def build_goal_tasks(goal_tasks: typing.Dict[str, typing.Any], random: Random) -> typing.List[typing.Tuple[WinConditionComplex, int]]:
    """Turn the goal_tasks option into (win condition, amount) pairs, in the order they were listed."""
    tasks = []
    for task_name in list(goal_tasks.keys())[: GoalTasks.max_tasks]:
        # Tasks without an amount, like jetpac, only need doing once
        count = calculate_quantity(task_name, goal_tasks, random) if task_name in QUANTITY_MAX else 1
        tasks.append((TASK_GOALS[task_name], count))
    return tasks


def pp_wincon(win_condition_item, wc_count=0):
    """Pretty print win condition name with count."""
    win_con_name_table = {
        WinConditionComplex.beat_krool: "Beat K. Rool",
        WinConditionComplex.get_key8: "Acquire Key 8",
        WinConditionComplex.get_keys_3_and_8: "Acquire Keys 3 and 8",
        WinConditionComplex.krem_kapture: f"Kremling Kapture ({wc_count} Photo{'s' if wc_count != 1 else ''})",
        WinConditionComplex.dk_rap_items: "Complete the Rap",
        WinConditionComplex.req_bean: "Acquire the Bean",
        WinConditionComplex.req_bp: f"{wc_count} Blueprint{'s' if wc_count != 1 else ''}",
        WinConditionComplex.req_companycoins: f"{wc_count} Company Coin{'s' if wc_count != 1 else ''}",
        WinConditionComplex.req_crown: f"{wc_count} Crown{'s' if wc_count != 1 else ''}",
        WinConditionComplex.req_fairy: f"{wc_count} Fair{'ies' if wc_count != 1 else 'y'}",
        WinConditionComplex.req_gb: f"{wc_count} Golden Banana{'s' if wc_count != 1 else ''}",
        WinConditionComplex.req_key: f"{wc_count} Key{'s' if wc_count != 1 else ''}",
        WinConditionComplex.req_medal: f"{wc_count} Medal{'s' if wc_count != 1 else ''}",
        WinConditionComplex.req_pearl: f"{wc_count} Pearl{'s' if wc_count != 1 else ''}",
        WinConditionComplex.req_rainbowcoin: f"{wc_count} Rainbow Coin{'s' if wc_count != 1 else ''}",
        WinConditionComplex.req_bonuses: f"{wc_count} Bonus Barrel{'s' if wc_count != 1 else ''}",
        WinConditionComplex.req_bosses: f"{wc_count} Boss{'es' if wc_count != 1 else ''}",
        WinConditionComplex.krools_challenge: "Krool's Challenge",
        WinConditionComplex.kill_the_rabbit: "Kill the Rabbit",
        WinConditionComplex.mech_fish: "Shoot the Mechanical Fish",
        WinConditionComplex.arcade: "Beat DK Arcade Round 2",
        WinConditionComplex.jetpac: "Beat Jetpac",
        WinConditionComplex.bad_hit_detection_man: "Defeat the Toy Monster",
        WinConditionComplex.rareware_gb_check: "Collect the Rareware GB",
        WinConditionComplex.blast_courses: f"{wc_count} Blast Course{'s' if wc_count != 1 else ''}",
        WinConditionComplex.tasks: "Tasks",
    }
    if win_condition_item in win_con_name_table:
        return win_con_name_table[win_condition_item]
    else:
        return win_condition_item.name


def pp_tasks(settings) -> typing.List[str]:
    """Pretty print each active task of the tasks win condition."""
    tasks = []
    for task_index in range(1, 9):
        condition = getattr(settings, f"task_{task_index}_condition")
        if condition != WinConditionComplex.inactive:
            tasks.append(pp_wincon(condition, getattr(settings, f"task_{task_index}_count")))
    return tasks
