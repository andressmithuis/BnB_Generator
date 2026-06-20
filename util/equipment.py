from .rarity import Rarity
from .modifier import mod_template

class Equipment:
    def __init__(self):
        self._rarity = Rarity.COMMON

        self.equipment_properties = []
        self.equipment_modifiers = []

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
                self.active_mods.remove(modifier)

    def add_modifiers(self, modifiers):
        # Load in new properties
        for modifier in modifiers:
            print(f"Adding {modifier.name} - {modifier.effect}({modifier.situational})")
            self.linked_equipment.equipment_modifiers.append(modifier)
            self.active_mods.append(modifier)

    def replace_modifiers(self, new_modifiers):
        self.clear_modifiers()
        self.add_modifiers(new_modifiers)

    def reload_modifiers(self):
        self.replace_modifiers([mod_template(self.name, self.effect)])
