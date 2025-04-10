"""
Preclean Json Arrays - Kivy Edition

Cleans the data from before the first { and last } in a json file.

Created by Christopher (Egrigor86)
"""
__version__ = "0.2.0"

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from plyer import filechooser
import os

class JSONPrecleaner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)

        self.folder_path = ""
        self.folder_input = TextInput(hint_text="Select folder to clean", multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.folder_input)

        browse_button = Button(text="Browse Folder", size_hint_y=None, height=40)
        browse_button.bind(on_press=self.browse_folder)
        self.add_widget(browse_button)

        clean_button = Button(text="Start Cleaning", size_hint_y=None, height=50)
        clean_button.bind(on_press=self.start_cleaning)
        self.add_widget(clean_button)

        self.log_output = Label(text="", size_hint_y=None, height=300)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.log_output)
        self.add_widget(scroll)

    def browse_folder(self, instance):
        filechooser.choose_dir(on_selection=self.set_folder_path)

    def set_folder_path(self, selection):
        if selection:
            self.folder_path = selection[0]
            self.folder_input.text = self.folder_path

    def show_popup(self, title, message):
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=message))
        close_btn = Button(text="Close", size_hint_y=None, height=40)
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()

    def log(self, message):
        self.log_output.text += message + "\n"

    def clean_json_files(self, folder_path):
        cleaned_count = 0
        skipped_files = []

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()

                    start_index = content.find("{")
                    end_index = content.rfind("}") + 1

                    if start_index == -1 or end_index == 0:
                        skipped_files.append(filename)
                        continue

                    cleaned_content = content[start_index:end_index]

                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(cleaned_content)

                    cleaned_count += 1
                except Exception as e:
                    self.log(f"❌ Error processing {filename}: {e}")

        self.log(f"\n✔ Cleaned {cleaned_count} file(s).")
        if skipped_files:
            self.log(f"⚠ Skipped (not valid JSON): {', '.join(skipped_files)}")

    def start_cleaning(self, instance):
        folder = self.folder_input.text.strip()
        if not os.path.isdir(folder):
            self.show_popup("Invalid Folder", "Please select a valid folder.")
            return
        self.log_output.text = ""  # Clear previous log
        self.clean_json_files(folder)

class JSONPrecleanerApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return JSONPrecleaner()

def main():
    JSONPrecleanerApp().run()

if __name__ == "__main__":
    main()
