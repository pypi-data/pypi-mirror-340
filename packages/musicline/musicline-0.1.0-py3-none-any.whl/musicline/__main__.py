from textual.app import App, ComposeResult, Screen
from textual.widgets import Footer, Header, OptionList, Markdown, Static, MarkdownViewer
from textual.message import Message
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import pygame
import tomlkit
import os

pygame.mixer.init()

def get_files(path: str) -> list[str]:
    files = os.listdir(path)
    files = [f for f in files if f.endswith('.mp3')]
    return files


class CustomMessage(Message):
    def __init__(self, sender, content: str):
        super().__init__()
        self.sender = sender
        self.content = content

class HelpScreen(Screen):
    """Help screen of the app."""
    HELP_MARKDOWN = """
# Musicline Help

This is a help for Musicline.

## Commands

- **d**: Toggle dark mode
- **p**: Play music
- **a**: Pause music
- **s**: Stop music
- **q**: Quit

## Config file

Config file are in TOML format. The config file must be in ~/.config/musicline/musicline.conf.

- **music_path**: Path to the music folder

## Themes

MusicLine has many themes. Thanks to [Textual](https://textual.textualize.io/) for the themes.

Press Ctrl+P, then type `theme` in the search bar.

Then select "Change theme"
"""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield MarkdownViewer(self.HELP_MARKDOWN, show_table_of_contents=True)
        yield Footer()
        
    def action_pop_screen(self) -> None:
        self.app.pop_screen()

    def action_toggle_dark(self) -> None:
        self.app.theme = (
            "textual-dark" if self.app.theme == "textual-light" else "textual-light"
        )

class AboutScreen(Screen):
    """About screen of the app."""
    ABOUT_MARKDOWN = """
# MusicLine

Music in the terminal.

# About MusicLine
MusicLine is a music player in the terminal. It is written in Python and uses [pygame](https://www.pygame.org/news) for playing music.
It is a simple and lightweight music player that can play music in the terminal. TUI uses Textual.
It is designed for command-line lovers who want to listen to music while working in the terminal.
It mix music with terminal vibes.

#### Author
Mani Arasteh and contributors

#### License
The license of MusicLine is MIT license, which means you must obey the license of the project.

#### Dependencies
Without these modules, this project wouldn't be a thing. Thanks to all of them (and their authors).

- [pygame](https://www.pygame.org/news): pygame is a set of Python modules designed for writing video games. It provides functionalities like sound, music, and graphics.
- [textual](https://textual.textualize.io/): Textual is a TUI (Text User Interface) framework for Python, allowing developers to create interactive terminal applications with rich user interfaces.
- [mutagen](https://mutagen.readthedocs.io/en/latest/): Mutagen is a Python module to handle audio metadata. It supports various formats, including MP3, FLAC, and Ogg Vorbis.
- [tomlkit](https://tomlkit.readthedocs.io/en/latest/): A Python library for parsing and creating TOML files, which are used for configuration.

### Contributing
If you want to contribute to this project, please fork the repository and create a pull request. All contributions are welcome.

Remember! You must act politely and respectfully. If you don't, you will be banned from the project.

If you're already banned and want to be unbanned, please contact the author of the project with email. Email: mani.arasteh92@gmail.com

"""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield MarkdownViewer(self.ABOUT_MARKDOWN, show_table_of_contents=True)
        yield Footer()

    def action_pop_screen(self) -> None:
        self.app.pop_screen()

    def action_toggle_dark(self) -> None:
        self.app.theme = (
            "textual-dark" if self.app.theme == "textual-light" else "textual-light"
        )

class Musicline(App):
    """Music in a terminal"""

    MUSIC_LIST_CSS_PATH = "music_list.tcss"

    MUSIC_INFO_MARKDOWN = "# No music is currently playing"

    CONFIG_FILE = "musicline.conf"

    def __init__(self):
        super().__init__()
        if not os.path.exists(os.getcwd() + "/" + self.CONFIG_FILE):
            print("Config file not found")
            exit(1)

        with open(self.CONFIG_FILE, "r") as f:
            self.config = tomlkit.load(f)
            self.music_path = self.config["music_path"]
            self.music_list = get_files(self.music_path)
            self.music_name = ""
            self.artist = ""
            self.album = ""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("p", "select", "Play music"),
        ("a", "pause", "[Un]Pause music"),
        ("s", "stop", "Stop the music"),
        ("?", "help", "Help"),
        ("*", "show_about", "About this app"),
        ("q", "quit", "Quit"),
        ("t", "change_theme", "Change theme"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static()
        yield Markdown(self.MUSIC_INFO_MARKDOWN)
        yield OptionList(*self.music_list)
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_select(self) -> None:
        option_list = self.query_one(OptionList)
        highlighted_index = option_list.highlighted
        if highlighted_index is None:
            self.notify("No item selected")
        selected_option = option_list.get_option_at_index(highlighted_index)
        selected_option_str = selected_option.prompt
        if self.music_path.endswith("/"):
            self.selected_option = self.music_path + selected_option_str
        else:
            self.selected_option = self.music_path + "/" + selected_option_str
        self.filename = self.selected_option
        try:
            self.song_name = MP3(self.filename, ID3=EasyID3)
            self.artist = self.song_name["artist"][0]
            self.album = self.song_name["album"][0]
            self.music_name = self.song_name["title"][0]
        except Exception:
            pass
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play()
        if not self.music_name:
            self.notify("Playing: {}".format(self.filename))
        else:
            self.notify("Playing: {} • {} • {}".format(self.music_name, self.artist, self.album))

        if self.music_name == "":
            self.MUSIC_INFO_MARKDOWN = "# {}".format(selected_option_str)
        else:
            self.MUSIC_INFO_MARKDOWN = f"""
# {self.music_name} • {self.artist} • {self.album}
"""
        self.query_one(Markdown).update(self.MUSIC_INFO_MARKDOWN)

    def action_pause(self) -> None:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.notify("Music paused")
        else:
            pygame.mixer.music.unpause()
            self.notify("Music unpaused")
    
    def action_stop(self) -> None:
        pygame.mixer.music.stop()
        self.notify("Music stopped")
        self.query_one(Markdown).update("# No music is currently playing")

    def action_help(self) -> None:
        self.push_screen(HelpScreen())
        
    def action_show_about(self) -> None:
        self.push_screen(AboutScreen())

if __name__ == "__main__":
    app = Musicline()
    app.run()
