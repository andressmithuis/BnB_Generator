from util import Dice

gun_parts = {
    1: {'gun_damage': 1, 'gun_accuracy': 1, 'swap_checks': 1, 'reload_checks': 1, 'mag_size': 1},
    2: {'gun_damage': 2, 'gun_accuracy': 1, 'swap_checks': 1, 'reload_checks': 1, 'mag_size': 1},
    3: {'gun_damage': 3, 'gun_accuracy': 2, 'swap_checks': 2, 'reload_checks': 2, 'mag_size': 1},
    4: {'gun_damage': 4, 'gun_accuracy': 2, 'swap_checks': 2, 'reload_checks': 2, 'mag_size': 2},
    5: {'gun_damage': 5, 'gun_accuracy': 3, 'swap_checks': 3, 'reload_checks': 3, 'mag_size': 2},
    6: {'gun_damage': 6, 'gun_accuracy': 3, 'swap_checks': 3, 'reload_checks': 3, 'mag_size': 2},
    7: {'gun_damage': 7, 'gun_accuracy': 4, 'swap_checks': 4, 'reload_checks': 4, 'mag_size': 3},
    8: {'gun_damage': 8, 'gun_accuracy': 4, 'swap_checks': 4, 'reload_checks': 4, 'mag_size': 3},
    9: {'gun_damage': 9, 'gun_accuracy': 5, 'swap_checks': 5, 'reload_checks': 5, 'mag_size': 3},
    10: {'gun_damage': 10, 'gun_accuracy': 5, 'swap_checks': 5, 'reload_checks': 5, 'mag_size': 4}
}

element_parts = {
    1: {'elemental_damage': 1, 'effect_chance': 2, 'puddle_chance': 5},
    2: {'elemental_damage': 2, 'effect_chance': 4, 'puddle_chance': 5},
    3: {'elemental_damage': 3, 'effect_chance': 6, 'puddle_chance': 10},
    4: {'elemental_damage': 4, 'effect_chance': 8, 'puddle_chance': 10},
    5: {'elemental_damage': 5, 'effect_chance': 10, 'puddle_chance': 15},
    6: {'elemental_damage': 6, 'effect_chance': 12, 'puddle_chance': 15},
    7: {'elemental_damage': 7, 'effect_chance': 14, 'puddle_chance': 20},
    8: {'elemental_damage': 8, 'effect_chance': 16, 'puddle_chance': 20},
    9: {'elemental_damage': 9, 'effect_chance': 18, 'puddle_chance': 25},
    10: {'elemental_damage': 10, 'effect_chance': 20, 'puddle_chance': 25}
}

action_skill_parts = {
    1: {'action_skill_damage': 1, 'uses_per_day': 1, 'action_skill_duration': 1},
    2: {'action_skill_damage': 2, 'uses_per_day': 1, 'action_skill_duration': 1},
    3: {'action_skill_damage': 3, 'uses_per_day': 2, 'action_skill_duration': 1},
    4: {'action_skill_damage': 4, 'uses_per_day': 2, 'action_skill_duration': 2},
    5: {'action_skill_damage': 5, 'uses_per_day': 3, 'action_skill_duration': 2},
    6: {'action_skill_damage': 6, 'uses_per_day': 3, 'action_skill_duration': 2},
    7: {'action_skill_damage': 7, 'uses_per_day': 4, 'action_skill_duration': 3},
    8: {'action_skill_damage': 8, 'uses_per_day': 4, 'action_skill_duration': 3},
    9: {'action_skill_damage': 9, 'uses_per_day': 5, 'action_skill_duration': 3},
    10: {'action_skill_damage': 10, 'uses_per_day': 5, 'action_skill_duration': 4}
}

health_parts = {
    1: {'max_health': 5, 'health_regen': 1, 'ffyl_duration': 1, 'revive_health': 10}
}

defensive_parts = {
    1: {'shield_capacity': 5, 'shield_recharge': 2, 'elemental_resistance': Dice.from_string('1d4')}
}

melee_parts = {
    1: {'melee_damage': 1, 'melee_attacks': 0, 'move_speed': 1}
}

ammo_parts = {
    1: {'expanded_reserves': 1, 'expanded_grenades': 1}
}