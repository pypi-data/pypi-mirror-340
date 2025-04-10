"""
Offline Python Wheel Manager - Kivy Edition

This tool allows you to parse pip commands, download and install wheels locally,
generate requirements.txt, and restore environments offline.

Created by Christopher (Egrigor86)
"""
__version__ = "0.2.0"


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserIconView
from kivy.properties import StringProperty
import subprocess
import threading
import json
import os
import re

CONFIG_FILE = "wheeldl_config.json"


class WheelManagerTabs(TabbedPanel):
    packages = StringProperty("")
    index_url = StringProperty("https://download.pytorch.org/whl/cu118")
    save_path = StringProperty("")
    pip_command = StringProperty("")
    local_install = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.load_config()

        self.build_tabs()

    def build_tabs(self):
        self.build_main_tab()
        self.build_advanced_tab()
        self.build_tools_tab()

    def build_main_tab(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll = ScrollView()
        container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        container.bind(minimum_height=container.setter('height'))

        # Pip command
        self.pip_input = self.make_input("Paste pip command (optional)", "pip install numpy -i URL")
        container.add_widget(self.pip_input)
        container.add_widget(self.make_button("Parse pip command", self.parse_pip_command))

        # Package list
        self.package_input = self.make_input("Packages (space-separated)", "numpy pandas torch")
        container.add_widget(self.package_input)
        container.add_widget(self.make_button("Clear Packages", lambda *_: self.set_text(self.package_input, "")))

        # Index URL
        self.index_input = self.make_input("Index URL (optional)", "https://download.pytorch.org/whl/cu118")
        container.add_widget(self.index_input)
        container.add_widget(self.make_button("Clear Index URL", lambda *_: self.set_text(self.index_input, "")))

        # Folder
        self.save_path_input = self.make_input("Save/Load Folder", "/storage/emulated/0/wheels")
        container.add_widget(self.save_path_input)
        container.add_widget(self.make_button("Browse Folder", self.browse_folder))

        # Actions
        container.add_widget(self.make_button("Download Wheels", self.threaded_download))
        container.add_widget(self.make_button("Install from Saved Wheels (above packages)", self.threaded_install))

        scroll.add_widget(container)
        layout.add_widget(scroll)
        self.add_widget(self.make_tab("Main", layout))

    def build_advanced_tab(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll = ScrollView()
        container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        container.bind(minimum_height=container.setter('height'))

        self.local_input = self.make_input("Install (pip-style)", "matplotlib scipy")
        container.add_widget(self.local_input)
        container.add_widget(self.make_button("Install These from Saved Wheels", self.threaded_custom_local_install))
        container.add_widget(self.make_button("Install from requirements.txt", self.threaded_requirements_install))

        scroll.add_widget(container)
        layout.add_widget(scroll)
        self.add_widget(self.make_tab("Advanced", layout))

    def build_tools_tab(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll = ScrollView()
        container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        container.bind(minimum_height=container.setter('height'))

        container.add_widget(self.make_button("View Installed Packages", self.show_installed_packages))
        container.add_widget(self.make_button("View Saved Wheel Packages", self.show_available_wheels))
        container.add_widget(self.make_button("Save Installed Packages as requirements.txt", self.save_installed_packages))
        container.add_widget(self.make_button("Save Config", self.save_config))

        scroll.add_widget(container)
        layout.add_widget(scroll)
        self.add_widget(self.make_tab("Tools", layout))

    def make_input(self, label_text, placeholder):
        box = BoxLayout(orientation='vertical', size_hint_y=None, height=90)
        label = Label(text=label_text, size_hint_y=None, height=20)
        input_field = TextInput(hint_text=placeholder, multiline=False, size_hint_y=None, height=40)
        box.label = label
        box.input = input_field
        box.add_widget(label)
        box.add_widget(input_field)
        return box

    def make_button(self, text, action):
        return Button(text=text, size_hint_y=None, height=45, on_press=action)

    def make_tab(self, title, content):
        from kivy.uix.tabbedpanel import TabbedPanelItem
        tab = TabbedPanelItem(text=title)
        tab.add_widget(content)
        return tab

    def get_text(self, box): return box.input.text.strip()
    def set_text(self, box, val): box.input.text = val

    def save_config(self, *_):
        data = {
            "packages": self.get_text(self.package_input),
            "index_url": self.get_text(self.index_input),
            "save_path": self.get_text(self.save_path_input)
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)
        self.show_popup("Saved", "Configuration saved.")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.packages = data.get("packages", "")
                self.index_url = data.get("index_url", "")
                self.save_path = data.get("save_path", "")

    def parse_pip_command(self, *_):
        cmd = self.get_text(self.pip_input)
        if not cmd.lower().startswith("pip install"):
            self.show_popup("Invalid", "Command must start with 'pip install'")
            return

        parts = cmd.split()
        packages, index_url = [], ""
        skip_next = False
        for i, part in enumerate(parts[2:]):
            if skip_next:
                skip_next = False
                continue
            if part in ("--index-url", "-i") and i + 3 < len(parts):
                index_url = parts[2 + i + 1]
                skip_next = True
            elif part.startswith("--"):
                continue
            else:
                packages.append(part)

        self.set_text(self.package_input, " ".join(packages))
        if index_url:
            self.set_text(self.index_input, index_url)
        self.show_popup("Parsed", "Pip command parsed.")

    def browse_folder(self, *_):
        chooser = FileChooserIconView(path='.', dirselect=True)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(chooser)
        buttons = BoxLayout(size_hint_y=None, height=50)
        ok = Button(text="Select", size_hint_x=0.5)
        cancel = Button(text="Cancel", size_hint_x=0.5)
        popup = Popup(title="Choose Folder", content=layout, size_hint=(0.9, 0.9))
        ok.bind(on_press=lambda *_: self.set_text(self.save_path_input, chooser.path) or popup.dismiss())
        cancel.bind(on_press=popup.dismiss)
        buttons.add_widget(ok)
        buttons.add_widget(cancel)
        layout.add_widget(buttons)
        popup.open()

    def threaded_download(self, *_): threading.Thread(target=self.download_wheels, daemon=True).start()
    def threaded_install(self, *_): threading.Thread(target=self.install_wheels, daemon=True).start()
    def threaded_custom_local_install(self, *_): threading.Thread(target=self.local_install_from_saved, daemon=True).start()
    def threaded_requirements_install(self, *_): threading.Thread(target=self.install_from_requirements_file, daemon=True).start()

    def run_command(self, cmd):
        try:
            subprocess.check_call(cmd, shell=True)
            return True
        except subprocess.CalledProcessError as e:
            self.show_popup("Error", f"Command failed:\n{e}")
            return False

    def download_wheels(self):
        pkgs = self.get_text(self.package_input)
        path = self.get_text(self.save_path_input)
        index = self.get_text(self.index_input)
        if not pkgs or not path:
            self.show_popup("Missing Info", "Please enter packages and select folder.")
            return
        os.makedirs(path, exist_ok=True)
        cmd = f'pip download {pkgs} -d "{path}"'
        if index: cmd += f' --index-url {index}'
        if self.run_command(cmd): self.show_popup("Done", "Download complete.")

    def install_wheels(self):
        pkgs = self.get_text(self.package_input)
        path = self.get_text(self.save_path_input)
        if not pkgs or not path:
            self.show_popup("Missing Info", "Please enter packages and select folder.")
            return
        cmd = f'pip install --no-index --find-links "{path}" {pkgs}'
        if self.run_command(cmd): self.show_popup("Done", "Install complete.")

    def local_install_from_saved(self):
        local = self.get_text(self.local_input)
        path = self.get_text(self.save_path_input)
        if not local or not path:
            self.show_popup("Missing Info", "Please enter pip-style names and select folder.")
            return
        cmd = f'pip install --no-index --find-links "{path}" {local}'
        if self.run_command(cmd): self.show_popup("Done", "Install complete.")

    def install_from_requirements_file(self):
        from tkinter.filedialog import askopenfilename
        req_path = askopenfilename(title="Select requirements.txt", filetypes=[("Text Files", "*.txt")])
        if not req_path: return
        folder = self.get_text(self.save_path_input)
        if not folder or not os.path.isdir(folder):
            self.show_popup("Missing", "Set save folder first.")
            return

        with open(req_path, "r") as f:
            required = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        wheels = [f for f in os.listdir(folder) if f.endswith(".whl")]
        existing = set()
        for w in wheels:
            m = re.match(r"^([A-Za-z0-9_.\-]+)-([0-9][\w\.]*)", w)
            if m:
                existing.add(f"{m.group(1).replace('_','-')}=={m.group(2)}")

        missing = [pkg for pkg in required if pkg not in existing]

        if missing:
            self.show_popup("Missing Packages", f"{len(missing)} missing:\n\n{missing}")
            return

        cmd = f'pip install --no-index --find-links "{folder}" -r "{req_path}"'
        if self.run_command(cmd): self.show_popup("Done", "Installed from requirements.txt")

    def show_installed_packages(self, *_):
        try:
            out = subprocess.check_output("pip list", shell=True, text=True)
            self.show_scroll_popup("Installed Packages", out)
        except Exception as e:
            self.show_popup("Error", str(e))

    def show_available_wheels(self, *_):
        folder = self.get_text(self.save_path_input)
        if not folder or not os.path.isdir(folder):
            self.show_popup("Missing", "Set save folder first.")
            return
        wheels = [f for f in os.listdir(folder) if f.endswith(".whl")]
        if not wheels:
            self.show_popup("Empty", "No wheels found.")
            return
        lines = ["📦 Available Wheels:\n"]
        for w in wheels:
            m = re.match(r"^([A-Za-z0-9_.\-]+)-([0-9][\w\.]*)", w)
            lines.append(f"{m.group(1)}=={m.group(2)}" if m else w)
        self.show_scroll_popup("Saved Wheels", "\n".join(lines))

    def save_installed_packages(self, *_):
        from tkinter.filedialog import asksaveasfilename
        try:
            output = subprocess.check_output("pip freeze", shell=True, text=True)
            path = asksaveasfilename(title="Save requirements.txt", defaultextension=".txt")
            if path:
                with open(path, "w") as f: f.write(output)
                self.show_popup("Saved", f"Saved to {path}")
        except Exception as e:
            self.show_popup("Error", str(e))

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.75, 0.4))
        popup.open()

    def show_scroll_popup(self, title, message):
        scroll = ScrollView()
        label = Label(text=message, size_hint_y=None)
        label.bind(texture_size=lambda i, v: setattr(label, "height", v[1]))
        scroll.add_widget(label)
        popup = Popup(title=title, content=scroll, size_hint=(0.9, 0.9))
        popup.open()


class WheelManagerApp(App):
    def build(self):
        return WheelManagerTabs()


if __name__ == "__main__":
    WheelManagerApp().run()
