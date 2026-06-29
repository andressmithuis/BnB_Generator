from copy import deepcopy

from .common_modifiers import *
from .rarity import Rarity
from .modifier import AdditiveModifier
from .elements import Element

class Equipment:
    def __init__(self):
        self.name_prefix = ''
        self.name_raw = ''
        self.level = 1
        self.tier = 1
        self._rarity = Rarity.COMMON

        self.manufacturer = None
        self.eridian = False

        self.n_parts = 0

        self.equipment_properties = []

    def has_property(self, property_type):
        for property in self.equipment_properties:
            if isinstance(property, property_type):
                return True

        return False

    def update_modifiers(self):
        for property in self.equipment_properties:
            property.reload_modifiers()

    def has_modifier(self, modifier_type):
        for modifier in self.equipment_modifiers:
            if isinstance(modifier, modifier_type):
                return True

        return False

    def get_modifier_value(self, modifier_type):
        mod_value = 0
        for modifier in self.equipment_modifiers:
            if isinstance(modifier, modifier_type):
                mod_value += modifier.value

        return mod_value

    @property
    def name(self):
        return f"{self.name_prefix}{' ' if len(self.name_prefix) != 0 else ''}{self.name_raw}"

    @property
    def rarity(self):
        return self._rarity

    @rarity.setter
    def rarity(self, new_rarity):
        # Automatically triggers a reload of weapon properties when the gun rarity changes
        self._rarity = new_rarity
        self.update_modifiers()

    @property
    def forced_elemental(self):
        return self.has_modifier(mod_is_elemental)

    @property
    def forced_non_elemental(self):
        return self.has_modifier(mod_non_elemental)

    @property
    def elemental_roll_bonus(self):
        return self.get_modifier_value(mod_elemental_roll_bonus)

    @property
    def elements(self):
        element_list = []
        for mod in self.equipment_modifiers:
            if isinstance(mod, Element):
                element_list.append(mod)

        return element_list

    @property
    def forced_element(self):
        forced_element = None
        for modifier in self.equipment_modifiers:
            if isinstance(modifier, mod_forced_element):
                forced_element = modifier.type
                break

        return forced_element

    @property
    def blacklisted_elements(self):
        blacklist = []
        for modifier in self.equipment_modifiers:
            if isinstance(modifier, mod_blacklisted_element):
                blacklist.append(modifier.type)

        return blacklist


    @property
    def equipment_modifiers(self):
        linked_mods = []
        for property in self.equipment_properties:
            for mod in property.active_mods:
                added_to_list = False
                if isinstance(mod, AdditiveModifier):
                    # Check if mod is already present in the list. Add values together if it is, add it new if it isn't
                    for existing_mod in linked_mods:
                        if isinstance(existing_mod, type(mod)):
                            existing_mod += mod
                            added_to_list = True
                            break

                if added_to_list is False:
                    linked_mods.append(deepcopy(mod))

        return linked_mods


class EquipmentProperty:
    name = '<Property Name>'
    effect = '<Property Effect>'
    enable_modifier_reload = True

    def __init__(self):
        self.linked_equipment = None
        self.active_mods = []

    def attach(self, equipment):
        #print(f"Attaching <{self.name}> --> ({id(equipment)})")
        # Link to equipment
        self.linked_equipment = equipment
        self.linked_equipment.equipment_properties.append(self)

        # Load/Attach modifiers
        self.load_modifiers()

    def detach(self):
        if self.linked_equipment is not None:
            #print(f"Detaching <{self.name}> --> ({id(self.linked_equipment)})")
            # Remove modifiers
            self.remove_modifiers()

            # Break link to equipment
            self.linked_equipment.equipment_properties.remove(self)
            self.linked_equipment = None

    def load_modifiers(self):
        # Should be overridden by subclass
        pass

    def remove_modifiers(self):
        if len(self.active_mods) > 0:
            linked_mods = self.active_mods.copy()
            self.detach_modifiers(linked_mods)

    def reload_modifiers(self):
        if self.enable_modifier_reload is True:
            self.remove_modifiers()
            self.load_modifiers()

    def attach_modifiers(self, modifier_list):
        # Attach and add to active_mods
        for modifier in modifier_list:
            mod_copy = deepcopy(modifier)
            mod_copy.attach(self)
            print(f"Attaching <{mod_copy.effect}>")

    def detach_modifiers(self, modifier_list):
        # Detach and remove from active_mods
        for modifier in modifier_list:
            if modifier.linked_property is not None:
                print(f"Detaching <{modifier.effect}>")
            modifier.detach()

    def link_to_equipment(self, equipment):
        self.linked_equipment = equipment

    def unlink_from_equipment(self):
        self.linked_equipment = None
