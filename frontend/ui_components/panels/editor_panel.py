from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.divider import MDDivider

from frontend.ui_components.widgets.placeholder_bubble import PlaceholderPopup
from frontend.ui_components.panels.card_inspector_panel.card_inspector_panel import CardInspectorPanel
from frontend.ui_components.panels.colored_panel import ColoredPanel
from frontend.ui_components.panels.common_settings import CommonSettingsPanel

from frontend.ui_components.ui_theme import UITheme


class EditorPanel(ColoredPanel):
    def __init__(self, parent_section, **kwargs):
        super().__init__(**kwargs)

        # --- Card Inspector Panel ---
        self.card_inspection_panel = CardInspectorPanel()

        # --- Editor Menu ---
        editor_menu = ColoredPanel(
            orientation = 'vertical',
            size_hint_x = 0.3,
            bg_color = UITheme.Panel.BG_BORDER,
            padding = 40,
            spacing = 10
        )

        btn_generate = MDButton(
            MDButtonText(text='Generate Card'),
            MDButtonIcon(icon='reload'),
            theme_bg_color='Custom',
            md_bg_color = UITheme.Button.PRIMARY,
            on_release = lambda x: parent_section.generate_new_card(),
            pos_hint = {'center_x': 0.5}
        )

        btn_generate_roll = MDButton(
            MDButtonText(text='Roll for Card'),
            MDButtonIcon(icon='dice-6'),
            theme_bg_color='Custom',
            md_bg_color=UITheme.Button.PRIMARY,
            #text_color = UITheme.Button.DISABLED_TEXT,
            on_release=lambda x: (
                parent_section.generate_new_card(manual_input=True),
                parent_section.dicerequest_panel.open_panel(),
            ),
            pos_hint = {'center_x': 0.5}
        )

        btn_load_card = MDButton(
            MDButtonText(text='Load Card'),
            MDButtonIcon(icon='folder'),
            md_bg_color=UITheme.Button.DISABLED,
            #text_color=UITheme.Button.DISABLED_TEXT,
            on_release=lambda x: PlaceholderPopup().open(),
            pos_hint = {'center_x': 0.5}
        )

        btn_save_card = MDButton(
            MDButtonText(text='Save Card'),
            MDButtonIcon(icon='content-save'),
            theme_bg_color='Custom',
            md_bg_color=UITheme.Button.DISABLED,
            #text_color=UITheme.Button.DISABLED_TEXT,
            on_release=lambda x: PlaceholderPopup().open(),
            pos_hint = {'center_x': 0.5}
        )

        btn_gen_log = MDButton(
            MDButtonText(text='Generation Log'),
            MDButtonIcon(icon='view-list'),
            theme_bg_color='Custom',
            md_bg_color=UITheme.Button.PRIMARY,
            on_release=lambda x: parent_section.dicerequest_panel.open_panel(),
            pos_hint={'center_x': 0.5}
        )

        btn_export_card = MDButton(
            MDButtonText(text='Export Card'),
            MDButtonIcon(icon='download'),
            theme_bg_color = 'Custom',
            md_bg_color=UITheme.Button.PRIMARY,
            on_release=lambda x: parent_section.export_card(),
            pos_hint={'center_x': 0.5}
        )

        # Add Buttons
        editor_menu.add_widget(btn_generate)
        editor_menu.add_widget(btn_generate_roll)
        editor_menu.add_widget(MDDivider(size_hint_x=1))
        editor_menu.add_widget(btn_save_card)
        editor_menu.add_widget(btn_load_card)
        editor_menu.add_widget(MDDivider(size_hint_x = 1))
        editor_menu.add_widget(btn_gen_log)
        editor_menu.add_widget(btn_export_card)
        editor_menu.add_widget(Widget())


        # --- Card Settings ---
        settings_panel = BoxLayout(
            orientation = 'vertical',
            size_hint_x = 0.5
        )

        settings_panel.add_widget(
            CommonSettingsPanel(
                size_hint_y = 0.5
            )
        )
        settings_panel.add_widget(
            CommonSettingsPanel(
                size_hint_y=0.5
            )
        )

        # --- Build Panel Widgets ---
        self.add_widget(self.card_inspection_panel)
        self.add_widget(editor_menu)
        self.add_widget(settings_panel)

    def find_parent_widget(self, parent_type):
        parent = self.parent
        while parent:
            if isinstance(parent, parent_type):
                return parent
            parent = parent.parent

        return parent