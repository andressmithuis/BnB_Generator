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

from util import Dice


class LoggerEvent(MDBoxLayout):
    def __init__(self, dice_request, anchor='right', **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (1, None)
        self.adaptive_height = True

        self.dice_request = dice_request

        # (optional) spacer | bubble | (optional) spacer
        if anchor == 'right':
            self.add_widget(Widget())

        self.bubble = EventBubble(
            dice_request = dice_request,
            style='elevated'
        )
        self.add_widget(self.bubble)

        if anchor == 'left':
            self.add_widget(Widget())

        self.bind(size = self.bubble.resize)


class EventBubble(MDCard):
    def __init__(self, dice_request, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.padding = dp(10)
        self.theme_bg_color = 'Custom'
        self.md_bg_color = UITheme.Panel.BG_LIGHT

        self.content = MDBoxLayout(
            orientation = 'horizontal',
            spacing = dp(10)
        )

        # (optional) icon | prompt + buttons
        # - OR -
        # prompt | (optional) icon
        self.leading_img = Image(
            source = 'img/dice_symbol/1d20.png',
            size_hint=(None, None),
            fit_mode = 'contain',
            pos_hint = {'center_y': 0.5}
        )
        self.content.add_widget(self.leading_img)

        self.content.add_widget(
            MDDivider(
                orientation = 'vertical',
                size_hint_y = 1.0,
                pos_hint = {'center_y': 0.5}
            )
        )

        self.body = MDBoxLayout(
            orientation = 'vertical',
            size_hint_y = None,
            spacing = dp(10)
        )

        self.prompt = MDLabel(
            #text = 'Hello World!'
            #text = 'Super duper long text of a lot of letters and characters and spaces and stuff and have we reached a newline yet?',
            text = dice_request.prompt,
            pos_hint = {'top': 1}
        )

        self.user_input = MDBoxLayout(
            size_hint = (None, None),
            pos_hint = {'center_x': 0.5},
            spacing = dp(10)
        )
        self.dice_input = DiceInputField(
            dice=Dice.from_string(dice_request.dice),
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

        # Build Layout
        self.body.add_widget(self.prompt)
        self.body.add_widget(self.user_input)
        self.content.add_widget(self.body)
        self.add_widget(self.content)

        self.submit_button.bind(on_release=self.on_submit)
        self.bind(size=self.resize)

    def resize(self, *args):
        full_w = self.parent.width

        # Resize leading/trailing images based on LoggerEvent.width
        self.leading_img.width = dp(40)
        self.leading_img.height = self.leading_img.width

        # Resize labels based on text width, limit to x% of LoggerEvent.width
        # Include Text wrap

        #  Maximum width = 80% of full width - image_width - (2x) padding - (2x) spacing
        maximum_text_w = full_w * 0.8 - self.leading_img.width - 2 * self.padding[0] - 2 * self.content.spacing

        # Raw text size
        self.prompt.text_size = (None, None)
        self.prompt.texture_update()
        raw_text_width = self.prompt.texture_size[0]

        target_text_width = min(raw_text_width, maximum_text_w)

        # Enable text wrapping
        self.prompt.text_size = (target_text_width+dp(5), None)
        self.prompt.texture_update()

        # Make sure Event Bubble is also resized
        self.width = target_text_width + self.leading_img.width + 2 * self.padding[0] + 2 * self.content.spacing
        self.body.height = self.prompt.texture_size[1] + self.body.spacing + self.user_input.height
        self.height = self.body.height + 2 * self.padding[0]

        # Resize user input field
        self.user_input.width = max(target_text_width * 0.8, dp(100))

        if True:
            print(f"--- Event Resize ---")
            print(f" - Padding top: {self.padding[0]}")
            print(f" - Text texture height: {self.leading_img.texture_size[1]}")
            print(f" - Spacing: {self.body.spacing}")
            print(f" - Input height: {self.user_input.size[1]}")
            print(f" - Padding bottom: {self.padding[0]}")
            print(f" ---- +")
            print(f" - Body height: {self.body.size[1]}")
            print(f" - content height: {self.body.size[1]}")
            print(f" - Bubble height: {self.size[1]}")
            print()
            print(f" - Bubble Width: {self.width} ({self.width / self.parent.width})")

    def on_submit(self, *args):
        if self.dice_input.value is not None:
            print(f"Submitting {self.dice_input.value}")
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

