from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from AdvancedBnB import Manufacturers

from frontend.ui_components.panels.colored_panel import ColoredPanel
from frontend import UITheme

from .dropdown_grid import DropdownGrid, DropdownGridItem, DropdownGridItemData


class EquipmentSettingsPanel(ColoredPanel):
    def __init__(self, parent_section, **kwargs):
        super().__init__(**kwargs)

        self.equipment_obj = parent_section.equipment_obj

        self.orientation = 'vertical'

        self.add_widget(
            MDLabel(
                text='[u]Equipment Properties[/u]',
                markup=True,
                font_style='Headline',
                role='small',
                halign='left',
                valign='center',
                adaptive_height = True
            )
        )

        # Level / Tier
        self.add_widget(LevelTierRow())

        # Name
        self.add_widget(NameRow())

        # Rarity Dropdown
        self.add_widget(RarityRow())

        # Manufacturer Dropdown
        self.add_widget(ManufacturerRow())

        # Type Dropdown

        self.add_widget(Widget())

    def on_card_generated(self):
        for row in self.children:
            if isinstance(row, Row):
                row.update_values(self.equipment_obj)



class Row(ColoredPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (1, None)
        self.spacing = dp(10)

        self.bind(size=self.update_height)
        Clock.schedule_once(self.delayed_init)

    def delayed_init(self, *args):
        self.update_height()
        equipment_obj = self.parent.equipment_obj
        self.update_values(equipment_obj)

    def update_height(self, *args):
        row_height = self.minimum_height
        self.height = row_height

    def update_values(self, equipment_obj):
        pass



class LevelTierRow(Row):
    tier_value = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 50% width Level + Input | 50% Tier
        level_column = ColoredPanel(
            size_hint_x = 0.5,
            spacing = dp(5)
        )

        level_column.add_widget(
            MDLabel(
                text='Level:',
                halign='left',
                valign='center',
                size_hint_x = None
            )
        )

        self.level_input_field = TextInput(
            text='Y',
            multiline=False,
            size_hint = (1, None)
        )
        self.level_input_field.bind(on_text_validate=self.on_level_input)

        level_column.add_widget(self.level_input_field)

        self.add_widget(level_column)

        self.tier_label = MDLabel(
            text='',
            valign='center',
            size_hint_x = 0.5
        )
        self.add_widget(self.tier_label)

    def update_height(self, *args):
        row_height = self.level_input_field.minimum_height
        self.level_input_field.height = row_height
        self.height = row_height

    def update_values(self, equipment_obj):
        if equipment_obj is not None:
            self.level_input_field.text = f"{equipment_obj.level}"
            self.tier_label.text = f"Tier: {equipment_obj.tier}"

    def update_tier_label(self, *args):
        self.tier_label.text = f"Tier: {self.tier_value}"

    def on_level_input(self, widget):
        try:
            lvl_value = int(widget.text)
        except ValueError:
            lvl_value = -1

        if lvl_value < 1:
            widget.text = '1'
            lvl_value = 1

        equipment_obj = self.parent.equipment_obj

        equipment_obj.level = lvl_value
        self.update_values(equipment_obj)

        print(f"Level: {equipment_obj.level}, Tier: {equipment_obj.tier}!")


class NameRow(Row):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(
            MDLabel(
                text='Name: ',
                halign='left',
                valign='center',
                size_hint_x = None
            )
        )

        self.input_field = TextInput(
            text='Y',
            multiline=False,
            size_hint= (1, None)
        )

        self.add_widget(self.input_field)

    def update_height(self, *args):
        row_height = self.input_field.minimum_height
        self.input_field.height = row_height
        self.height = row_height

    def update_values(self, equipment_obj):
        if equipment_obj is not None:
            self.input_field.text = f"{equipment_obj.name}"


class RarityRow(Row):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(
            MDLabel(
                text='Rarity: ',
                halign='left',
                valign='center',
                size_hint_x=None
            )
        )

        # TODO: Add Dropdown menu

    def update_height(self, *args):
        row_height = self.children[0].texture_size[1]
        self.height = row_height


class ManufacturerRow(Row):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.add_widget(
            MDLabel(
                text='Manufacturer: ',
                halign='left',
                valign='center',
                size_hint_x=None
            )
        )

        # Dropdown menu
        self.menu = DropdownGrid()

        for manufacturer in Manufacturers.all():
            item_data = DropdownGridItemData(manufacturer.name, f"img/guild_logo/AdvancedBnB/{manufacturer.logo_file}")
            self.menu.add_item(DropdownGridItem(item_data))

        self.add_widget(self.menu)

    def update_height(self, *args) -> None:
        row_height = self.children[1].texture_size[1]
        self.height = row_height
