from kivy.clock import Clock
from kivy.tools.pep8checker.pep8 import maximum_line_length
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.divider import MDDivider
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText, MDTextFieldMaxLengthText, MDTextFieldHelperText
from kivy.metrics import dp
from kivy.uix.image import Image

from frontend.ui_components.ui_theme import UITheme
from frontend.ui_components.panels.colored_panel import ColoredPanel

from util import Dice, DiceRequest


class LoggerEventLayout(MDBoxLayout):
    def __init__(self, event, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (1, None)
        self.adaptive_height = True

        # (optional) spacer | bubble | (optional) spacer
        if event.anchor == 'right':
            self.add_widget(Widget())

        self.bubble = EventBubble(
            event = event,
            style='elevated'
        )
        self.add_widget(self.bubble)

        if event.anchor == 'left':
            self.add_widget(Widget())

        self.bind(size = self.bubble.resize)

    def resolve_user_input(self, value):
        self.bubble.md_bg_color = UITheme.Button.PRIMARY
        self.bubble.prompt.text += f"\nRolled:  [b]{value}[/b]"
        self.bubble.body.remove_widget(self.bubble.user_input)


class EventBubble(MDCard):
    def __init__(self, event, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.adaptive_height = True
        self.padding = dp(10)
        self.theme_bg_color = 'Custom'
        self.md_bg_color = UITheme.Button.PRIMARY

        self.leading_img = None
        self.trailing_img = None

        self.content = MDBoxLayout(
            orientation = 'horizontal',
            spacing = dp(10),
            size_hint = (1, None),
            adaptive_height = True
        )

        img_divider = MDDivider(
            orientation = 'vertical',
            size_hint_y = 1.0,
            pos_hint = {'center_y': 0.5}
        )

        # (optional) icon | prompt + buttons
        # - OR -
        # prompt | (optional) icon
        if event.leading_img_src != '':
            self.leading_img = Image(
                source = event.leading_img_src,
                size_hint=(None, None),
                width = dp(40),
                height = dp(40),
                fit_mode = 'contain',
                pos_hint = {'center_y': 0.5}
            )
            self.content.add_widget(self.leading_img)
            self.content.add_widget(img_divider)

        self.body = MDBoxLayout(
            orientation = 'vertical',
            size_hint = (1, None),
            adaptive_height = True,
            pos_hint = {'center_y': 0.5},
            spacing = dp(10)
        )
        self.content.add_widget(self.body)

        if event.trailing_img_src != '':
            self.trailing_img = Image(
                source = event.trailing_img_src,
                size_hint=(None, None),
                width = dp(40),
                height = dp(40),
                fit_mode = 'contain',
                pos_hint = {'center_y': 0.5}
            )
            self.content.add_widget(img_divider)
            self.content.add_widget(self.trailing_img)

        self.prompt = MDLabel(
            text = event.prompt,
            size_hint = (None, None),
            markup = True
        )
        self.body.add_widget(self.prompt)


        # User input
        self.user_input = MDBoxLayout(
            size_hint = (1, None),
            adaptive_height = True,
            pos_hint = {'center_x': 0.5},
            spacing = dp(10),
        )
        if isinstance(event, DiceRequest):
            self.md_bg_color = UITheme.Button.DANGER
            self.dice_input = DiceInputField(
                dice=Dice.from_string(event.dice),
                pos_hint={'center_y': 0.5}
            )
            self.submit_button = MDButton(
                MDButtonText(
                    text = 'Submit'
                ),
                pos_hint = {'center_y': 0.5}
            )
            self.user_input.add_widget(self.dice_input)
            self.user_input.add_widget(self.submit_button)
            self.body.add_widget(self.user_input)

            self.submit_button.bind(on_release=self.on_submit)

        # Build Layout
        self.add_widget(self.content)
        self.bind(size=self.resize)

    def resize(self, *args):
        # LoggerEvent.width
        full_w = self.parent.width
        static_w = 2 * self.padding[0]
        if self.leading_img is not None:
            static_w += self.leading_img.width + 2 * self.content.spacing
        if self.trailing_img is not None:
            static_w += self.trailing_img.width + 2 * self.content.spacing

        # Raw text width (singular line)
        self.prompt.text_size = (None, None)
        self.prompt.texture_update()
        raw_text_width = self.prompt.texture_size[0]

        # Set bubble width based on raw_text_size -OR- 80% of full width
        self.width = min(
            static_w + raw_text_width,
            full_w * 0.8
        )

        # Set maximum text width, enabling text wrapping
        self.prompt.text_size = (
            self.width - static_w,
            None
        )
        self.prompt.texture_update()

        # Resize text space, which resizes bubble as well
        self.prompt.size = self.prompt.texture_size

    def on_submit(self, *args):
        if self.dice_input.value is not None:
            self.md_bg_color = UITheme.Button.PRIMARY
            self.parent.resolve_user_input(self.dice_input.value)
            MDApp.get_running_app().screen.main_section.step_generation(self.dice_input.value)

    def on_enter(self):
        # Disable highlighting effect of MDCard
        pass

    def on_leave(self):
        # Disable highlighting effect of MDCard
        pass


class DiceInputField(MDTextField):
    def __init__(self, dice: Dice, **kwargs):
        super().__init__(**kwargs)
        self.dice = dice

        self.mode = 'filled'
        self.size_hint_x = 1

        self.helper = MDTextFieldHelperText(
            text = 'Help',
            mode = 'on_error'
        )

        self.add_widget(
            MDTextFieldHintText(
                text='Dice'
            )
        )
        self.add_widget(self.helper)
        self.add_widget(
            MDTextFieldMaxLengthText(
                max_text_length=3,
            )
        )

        self.bind(text=self.validate_input)

    def validate_input(self, *args):
        # Check if numeric
        try:
            dice_value = int(self.text)
        except ValueError:
            self.helper.text = 'Please enter a number.'
            self.error = True
            return

        # Check if value is within dice range
        min_value, max_value = self.dice.value_range

        if dice_value < min_value or dice_value > max_value:
            self.helper.text = f"Value '{dice_value}' is not a valid number for '{self.dice}'"
            self.error = True
            return

        self.error = False

    @property
    def value(self):
        self.validate_input()
        if self.error:
            return None

        return int(self.text)

