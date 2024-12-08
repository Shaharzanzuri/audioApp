from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp

import os
import yt_dlp
import webbrowser
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix import widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics.svg import Svg
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp
from kivy.core.window import Window

Window.size = (500, 600)

# colors:
red = [0.905, 0.298, 0.235, 1]
brown = [0.373, 0.325, 0.325, 1]
cream = [0.945, 0.945, 0.925, 1]


# Function to trim the URL before '&list'
def trim_url_before_list(url):
    if '&list' in url:
        return url.split('&list')[0]
    return url  # Return original URL if '&list' is not present


class SvgWidget(Scatter):
    def __init__(self, filename):
        super(SvgWidget, self).__init__()

        self.do_scale = False
        self.do_rotation = False
        self.do_translation = False  # Disable dragging for a static SVG

        # Set position explicitly (top of the screen)
        self.size_hint = (None, None)
        self.pos_hint = {"center_x": 0.5, "top": 1}
        self.size = (400, 300)

        # Load the SVG into the canvas
        with self.canvas:
            Color(0.905, 0.298, 0.235)
            svg = Svg(filename)  # Ensure the SVG file has proper color definitions


class HoverButton(Button):
    """A Button that changes style when hovered."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_color = self.background_color
        self.hover_color = [self.default_color[0] + 0.1, self.default_color[1] + 0.1, self.default_color[2] + 0.1, 1]
        self.border_thickness = 2
        self.thick_border = 4

        # Bind mouse position tracking
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        """Detect mouse position and apply hover effect."""
        pos = args[1]  # Mouse position
        if self.collide_point(*self.to_widget(*pos)):
            self.on_hover()
        else:
            self.on_leave()

    def on_hover(self):
        """Change the button's appearance on hover."""
        self.background_color = self.hover_color
        self.border_width = self.thick_border

    def on_leave(self):
        """Restore the button's original appearance when not hovered."""
        self.background_color = self.default_color
        self.border_width = self.border_thickness


class MyApp(MDApp):

    def show_success_message(self, filepath):
        """Display success message and option to open the file."""
        self.status_label.text = f"Download complete! File saved to:\n{filepath}"

        # Create "Open File" button dynamically
        self.open_button = HoverButton(
            text="Open File",
            size_hint=(.3, .1),
            pos_hint={"center_x": 0.5, "center_y": 0.25},
        )
        self.open_button.bind(on_press=lambda _: webbrowser.open(filepath))
        self.root.add_widget(self.open_button)

    def getLinkInfo(self, instance):
        link = trim_url_before_list(self.linkinput.text)
        download_path = "songs"
        filepath = ""
        try:
            # Ensure the download path exists
            os.makedirs(download_path, exist_ok=True)

            # Configure yt-dlp with the desired download path
            ydl_opts = {
                'format': 'bestaudio/best',  # Best available audio format
                'postprocessors': [],  # No additional processing
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),  # Save with title as filename
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                filepath = os.path.join(download_path, f"{info['title']}.{info['ext']}")
        except Exception as e:
            self.status_label.text = f"An error occurred: {e}"
        finally:
            if filepath:
                self.show_success_message(filepath)

    def build(self):
        # Set the application icon
        self.icon = 'WaveMusic.jpg'
        self.title = "Downtube"
        layout = MDRelativeLayout(md_bg_color=red)

        self.headline = Image(source="design photos/Untitled design.png",
                              pos_hint={'center_x': 0.5, 'center_y': 0.8},
                              size_hint=(.6, .6),
                              )
        self.img = Image(source="WaveMusic.jpg",
                         pos_hint={'center_x': 0.5, 'center_y': 0.2},
                         size_hint=(0.3, 0.3), )

        # Use Scatter to enable rotation for the image
        #    self.img = Image("",
        #                    size_hint=(.5, .5),
        #                   pos_hint={'center_x': 0.5, 'center_y': 0.85})

        self.youtubelink = Label(
            text="Please Enter the YouTube link to Download",
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            font_size=20,
            color=cream,
        )

        self.linkinput = TextInput(
            text="",
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            size_hint=(0.8, None),
            height=48,
            font_size=20,
            multiline=False,
        )

        self.linkbutton = HoverButton(
            text="Click to Download the Song",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(.5, .1),
            color=cream,
            background_color=brown,

        )
        self.linkbutton.bind(on_press=self.getLinkInfo)

        self.status_label = Label(
            text="",
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
            font_size=18,
            color=cream,
        )

        layout.add_widget(self.headline)
        layout.add_widget(self.img)
        layout.add_widget(self.youtubelink)
        layout.add_widget(self.linkinput)
        layout.add_widget(self.linkbutton)
        layout.add_widget(self.status_label)

        return layout


if __name__ == "__main__":
    MyApp().run()
