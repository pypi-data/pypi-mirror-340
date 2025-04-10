"""
Python Virual Environment Creator - Kivy Edition

Checks for eg c:/python310 installations and lets the user create a custom python venv with a start.bat for easy use.

Created by Christopher (Egrigor86)
"""
__version__ = "0.2.0"

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.clock import Clock
from plyer import filechooser
import os
import sys
import subprocess

class VenvCreator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.available_paths = self.find_python_versions()
        self.selected_path = self.available_paths[0] if self.available_paths else ''
        self.target_folder = ""
        self.extra_packages = ""

        self.spinner = Spinner(text=self.selected_path, values=self.available_paths, size_hint_y=None, height=40)
        self.spinner.bind(text=self.set_selected_path)
        self.add_widget(Label(text="Select Python Interpreter", size_hint_y=None, height=30))
        self.add_widget(self.spinner)

        self.folder_label = Label(text="Target Folder: None", size_hint_y=None, height=30)
        self.add_widget(self.folder_label)

        browse_button = Button(text="Browse Folder", size_hint_y=None, height=40)
        browse_button.bind(on_press=self.browse_folder)
        self.add_widget(browse_button)

        self.pkg_input = TextInput(hint_text="Extra Packages (e.g. numpy pandas)", multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.pkg_input)

        create_button = Button(text="Create Virtual Environment", size_hint_y=None, height=50)
        create_button.bind(on_press=self.create_venv)
        self.add_widget(create_button)

        self.progress = ProgressBar(max=100, value=0, size_hint_y=None, height=20)
        self.add_widget(self.progress)

        self.status = Label(text="Status: Waiting", size_hint_y=None, height=30)
        self.add_widget(self.status)

        self.log_label = Label(text="", size_hint_y=None, height=300)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.log_label)
        self.add_widget(scroll)

    def set_selected_path(self, spinner, text):
        self.selected_path = text

    def browse_folder(self, instance):
        filechooser.choose_dir(on_selection=self.folder_selected)

    def folder_selected(self, selection):
        if selection:
            self.target_folder = selection[0]
            self.folder_label.text = f"Target Folder: {self.target_folder}"

    def find_python_versions(self):
        if sys.platform.startswith('win'):
            possible_paths = []
            drives = ['C:/']
            for d in drives:
                for entry in os.listdir(d):
                    path = os.path.join(d, entry, "python.exe")
                    if os.path.isfile(path):
                        possible_paths.append(path)
            return possible_paths or ["No Python versions found."]
        else:
            return [sys.executable]  # Android/Pyroid fallback

    def create_venv(self, instance):
        path = self.selected_path
        folder = self.target_folder
        extras = self.pkg_input.text.strip().split()

        if not path or not folder:
            self.log("❌ Please select both Python path and target folder.")
            return

        self.progress.value = 0
        self.status.text = "Creating environment..."

        try:
            # Step 1: venv
            self.log(f"🔧 Running: {path} -m venv {folder}")
            subprocess.run([path, "-m", "venv", folder], check=True)
            self.progress.value = 40
            Clock.tick()

            # Step 2: Create start.bat for Windows
            if sys.platform.startswith("win"):
                bat_path = os.path.join(folder, "start.bat")
                activate_path = os.path.join(folder, "Scripts", "activate")
                with open(bat_path, "w") as f:
                    f.write(f'start cmd /k "{activate_path}"')
                self.log(f"[✔] Created: {bat_path}")

            # Step 3: Install packages
            pip_path = os.path.join(folder, "Scripts" if sys.platform.startswith("win") else "bin", "pip")
            for pkg in extras:
                self.log(f"⏳ Installing {pkg}...")
                result = subprocess.run([pip_path, "install", pkg], capture_output=True, text=True)
                if result.returncode == 0:
                    self.log(f"[✔] Installed {pkg}")
                else:
                    self.log(f"[!] Failed {pkg}: {result.stderr}")
                Clock.tick()

            self.progress.value = 100
            self.status.text = "✅ Environment Ready"
            self.log("✅ Virtual environment created successfully.")

        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            self.status.text = "Error"

    def log(self, message):
        self.log_label.text += message + "\n"

class VenvCreatorApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return VenvCreator()

def main():
    VenvCreatorApp().run()

if __name__ == "__main__":
    main()
