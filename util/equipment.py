from copy import deepcopy

from .rarity import Rarity
from .modifier import AdditiveModifier
from .common_modifiers import mod_template

class Equipment:
    def __init__(self):
        self.name = ''
        self.name_prefix = ''
        self.level = 1
        self.tier = 1
        self._rarity = Rarity.COMMON

        self.manufacturer = None
        self.eridian = False

        self.n_parts = 0
        self.max_parts = 0

        self.equipment_properties = []
        self.equipment_modifiers = []

        self.elements = []

        self.forced_elemental = False
        self.forced_non_elemental = False
        self.elemental_roll_bonus = 0
        self.min_elements = 0
        self.disabled_elements = []

    def add_property(self, property):
        # Link property and add modifiers
        self.equipment_properties.append(property)
        property.link_to_equipment(self)
        property.reload_modifiers()

    def remove_property(self, property):
        property.clear_modifiers()
        property.unlink_from_equipment()
        if property in self.equipment_properties:
            self.equipment_properties.remove(property)

    def update_modifiers(self):
        for property in self.equipment_properties:
            property.reload_modifiers()

    @property
    def rarity(self):
        return self._rarity

    @rarity.setter
    def rarity(self, new_rarity):
        # Automatically triggers a reload of weapon properties when the gun rarity changes
        self._rarity = new_rarity
        self.update_modifiers()


class EquipmentProperty:
    name = '<Property Name>'
    effect = '<Property Effect>'

    def __init__(self):
        self.linked_equipment = None
        self.active_mods = []

    def link_to_equipment(self, equipment):
        self.linked_equipment = equipment

    def unlink_from_equipment(self):
        self.linked_equipment = None

    def clear_modifiers(self):
        # Delete previous properties
        if len(self.active_mods) > 0:
            to_delete = self.active_mods.copy()

            for modifier in to_delete:
                print(f"Removing {modifier.name} - {modifier.effect}({modifier.situational})")
                self.linked_equipment.equipment_modifiers.remove(modifier)
                modifier.revert_from_equipment(self.linked_equipment)
                modifier.linked_properties.remove(self)
                self.active_mods.remove(modifier)

    def add_modifiers(self, modifiers):
        # Load in new properties
        for modifier in modifiers:
            new_modifier = deepcopy(modifier)
            modifier_applied = False
            new_modifier.linked_properties.append(self)

            #print(f"Adding {new_modifier.name} - {new_modifier.effect}({new_modifier.situational})")
            equipment = self.linked_equipment

            if isinstance(new_modifier, AdditiveModifier):
                for existing_mod in equipment.equipment_modifiers:
                    if isinstance(new_modifier, type(existing_mod)):
                        existing_mod += new_modifier
                        existing_mod.linked_properties.append(self)
                        self.active_mods.append(existing_mod)
                        modifier_applied = True
                        break

            if modifier_applied is False:
                equipment.equipment_modifiers.append(new_modifier)
                new_modifier.apply_to_equipment(equipment)

                self.active_mods.append(new_modifier)

    def remove_modifiers(self):
        if len(self.active_mods) > 0:
            to_delete = self.active_mods.copy()

            equipment = self.linked_equipment

            for modifier in to_delete:
                #print(f"Removing {modifier.name} - {modifier.effect}")
                if isinstance(modifier, AdditiveModifier):
                    for existing_mod in equipment.equipment_modifiers:
                        if isinstance(modifier, type(existing_mod)):
                            existing_mod -= modifier
                            existing_mod.linked_properties.remove(self)

                else:
                    modifier.revert_from_equipment(self.linked_equipment)
                    equipment.equipment_modifiers.remove(modifier)
                    modifier.linked_properties.remove(self)
                    self.active_mods.remove(modifier)



    def replace_modifiers(self, new_modifiers):
        self.remove_modifiers()
        self.add_modifiers(new_modifiers)

    def reload_modifiers(self):
        self.replace_modifiers([mod_template(self.name, self.effect)])
