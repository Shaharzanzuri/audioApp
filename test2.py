class HoverHeadlineButton(HoverButton):
    """A Button that changes the headline image on hover."""

    def __init__(self, headline_widget, hover_image, default_image, **kwargs):
        super().__init__(**kwargs)
        self.headline_widget = headline_widget
        self.hover_image = hover_image
        self.default_image = default_image

    def on_hover(self):
        """Change the button's appearance and headline image on hover."""
        super().on_hover()
        self.headline_widget.source = self.hover_image

    def on_leave(self):
        """Restore the button's appearance and headline image when not hovered."""
        super().on_leave()
        self.headline_widget.source = self.default_image


class MyApp(MDApp):
    def build(self):
        # Set the application icon
        self.icon = 'WaveMusic.jpg'
        self.title = "Downtube"
        layout = MDRelativeLayout(md_bg_color=red)

        self.headline = Image(
            source="design photos/Untitled design.png",
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            size_hint=(.6, .6),
        )

        self.img = Image(
            source="WaveMusic.jpg",
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            size_hint=(0.3, 0.3),
        )

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

        self.linkbutton = HoverHeadlineButton(
            headline_widget=self.headline,
            hover_image="design photos/hover_headline.png",  # Replace with your hover image path
            default_image="design photos/Untitled design.png",
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

