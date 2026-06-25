from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

from frontend.ui_components.panels.colored_panel import ColoredPanel


class Banner(ColoredPanel):

    def __init__(self, title_text, **kwargs):
        super().__init__(**kwargs)

        orientation = 'horizontal'

        # Banner Text
        self.label = MDLabel(
            text=f"{title_text}",
            halign='center'
        )
        self.add_widget(self.label)

        # (Centered) Roll Button
        roll_button = MDRaisedButton(
            text='Roll',
            size_hint=(1, None),
            height=40
        )
        roll_button.bind(
            on_release=lambda x: print(f"WIP: Ask for rolls to generate Card...")
        )

        roll_button_widget = ColoredPanel(
            orientation = 'vertical',
            size_hint_x = None,
            width = 200,
            padding = 10
        )
        roll_button_widget.add_widget(Widget())
        roll_button_widget.add_widget(roll_button)
        roll_button_widget.add_widget(Widget())
        self.add_widget(roll_button_widget)

        # (Centered) Generate Button
        generate_button = MDRaisedButton(
            text = 'Generate',
            size_hint = (1, None),
            height = 40
        )
        generate_button.bind(
            on_release=lambda x: print(f"Poof! A new Card has appeared!")
        )

        generate_button_widget = ColoredPanel(
            orientation='vertical',
            size_hint_x=None,
            width=200,
            padding=10
        )
        generate_button_widget.add_widget(Widget())
        generate_button_widget.add_widget(generate_button)
        generate_button_widget.add_widget(Widget())
        self.add_widget(generate_button_widget)

