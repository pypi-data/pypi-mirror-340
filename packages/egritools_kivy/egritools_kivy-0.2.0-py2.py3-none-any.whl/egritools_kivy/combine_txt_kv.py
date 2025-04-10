"""
TXT File Combiner - Kivy Edition

Combines all the txt files in a chosen directory into a single txt file.

Created by Christopher (Egrigor86)
"""
__version__ = "0.2.0"


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from plyer import filechooser
import os

class TextCombiner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.folder_path = ""
        self.output_filename = "combined_output.txt"
        self.total_files = 0

        self.folder_label = Label(text="Selected Folder: None", size_hint_y=None, height=30)
        self.add_widget(self.folder_label)

        browse_button = Button(text="Browse Folder", size_hint_y=None, height=40)
        browse_button.bind(on_press=self.browse_folder)
        self.add_widget(browse_button)

        self.output_input = TextInput(text=self.output_filename, hint_text="Output Filename", multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.output_input)

        save_as_button = Button(text="Confirm Output Filename", size_hint_y=None, height=40)
        save_as_button.bind(on_press=self.set_output_name)
        self.add_widget(save_as_button)

        self.combine_button = Button(text="Combine Text Files", size_hint_y=None, height=50)
        self.combine_button.bind(on_press=self.combine_files)
        self.add_widget(self.combine_button)

        self.progress = ProgressBar(max=1, value=0, size_hint_y=None, height=20)
        self.add_widget(self.progress)

        self.status = Label(text="Status: Waiting", size_hint_y=None, height=30)
        self.add_widget(self.status)

        self.log_label = Label(text="", size_hint_y=None, height=300)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.log_label)
        self.add_widget(scroll)

    def browse_folder(self, instance):
        filechooser.choose_dir(on_selection=self.folder_selected)

    def folder_selected(self, selection):
        if selection:
            self.folder_path = selection[0]
            self.folder_label.text = f"Selected Folder: {self.folder_path}"

    def set_output_name(self, instance):
        if self.output_input.text.strip():
            self.output_filename = self.output_input.text.strip()
            self.log(f"[✔] Output filename set to: {self.output_filename}")
        else:
            self.log("[✘] Please enter a valid output filename.")

    def combine_files(self, instance):
        folder = self.folder_path
        filename = self.output_input.text.strip()

        if not folder or not os.path.isdir(folder):
            self.log("[✘] Please select a valid folder.")
            return

        if not filename:
            self.log("[✘] Please provide an output filename.")
            return

        try:
            output_path = os.path.join(os.getcwd(), filename)
            txt_files = [f for f in os.listdir(folder) if f.endswith('.txt')]
            self.total_files = len(txt_files)

            if not self.total_files:
                self.log("[!] No .txt files found.")
                return

            self.progress.max = self.total_files
            self.progress.value = 0
            self.status.text = f"Combining: 0/{self.total_files} files"

            with open(output_path, 'w', encoding='utf-8') as output_file:
                for idx, file in enumerate(txt_files):
                    file_path = os.path.join(folder, file)
                    with open(file_path, 'r', encoding='utf-8') as input_file:
                        content = input_file.read()
                        output_file.write(content + '\n')

                    self.progress.value = idx + 1
                    self.status.text = f"Combining: {idx + 1}/{self.total_files} files"
                    Clock.tick()  # Force UI refresh
                    self.log(f"[+] Added {file}")

            self.log(f"[✔] Files combined into {output_path}")
        except Exception as e:
            self.log(f"[✘] Error: {str(e)}")

    def log(self, message):
        self.log_label.text += message + "\n"

class TextCombinerApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return TextCombiner()

def main():
    TextCombinerApp().run()

if __name__ == "__main__":
    main()
