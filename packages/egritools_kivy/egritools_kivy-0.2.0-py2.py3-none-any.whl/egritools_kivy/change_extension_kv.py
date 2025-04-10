"""
Extension Changer Tool - Kivy Edition

Batch-renames files from one extension to another in a selected folder.

Created by Christopher (Egrigor86)
"""
__version__ = "0.2.0"

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from plyer import filechooser
import os

class ExtensionChanger(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.folder_path = ''
        
        self.folder_label = Label(text="Selected Folder: None", size_hint_y=None, height=30)
        self.add_widget(self.folder_label)

        self.browse_button = Button(text="Browse Folder", size_hint_y=None, height=40)
        self.browse_button.bind(on_press=self.browse_folder)
        self.add_widget(self.browse_button)

        self.old_ext_input = TextInput(hint_text="Old Extension (e.g. .txt)", multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.old_ext_input)

        self.new_ext_input = TextInput(hint_text="New Extension (e.g. .md)", multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.new_ext_input)

        self.rename_button = Button(text="Rename Files", size_hint_y=None, height=50)
        self.rename_button.bind(on_press=self.rename_files)
        self.add_widget(self.rename_button)

        self.log_label = Label(text="", size_hint_y=None, height=300, markup=True)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.log_label)
        self.add_widget(scroll)

    def browse_folder(self, instance):
        filechooser.choose_dir(on_selection=self.folder_selected)

    def folder_selected(self, selection):
        if selection:
            self.folder_path = selection[0]
            self.folder_label.text = f"Selected Folder: {self.folder_path}"

    def rename_files(self, instance):
        old_ext = self.old_ext_input.text.strip()
        new_ext = self.new_ext_input.text.strip()
        folder = self.folder_path

        if not folder or not os.path.isdir(folder):
            self.log("❌ Please select a valid folder.")
            return
        if not old_ext or not new_ext:
            self.log("❌ Please provide both extensions.")
            return
        if not old_ext.startswith("."):
            old_ext = "." + old_ext
        if not new_ext.startswith("."):
            new_ext = "." + new_ext

        count = 0
        for filename in os.listdir(folder):
            if filename.endswith(old_ext):
                new_filename = filename[:-len(old_ext)] + new_ext
                os.rename(os.path.join(folder, filename), os.path.join(folder, new_filename))
                self.log(f"[color=00ff00]Renamed:[/color] {filename} ➜ {new_filename}")
                count += 1

        self.log(f"\n✔ Renamed {count} file(s) in '{folder}'.")

    def log(self, message):
        self.log_label.text += message + "\n"

class ExtensionChangerApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return ExtensionChanger()

def main():
    ExtensionChangerApp().run()

if __name__ == "__main__":
    main()
