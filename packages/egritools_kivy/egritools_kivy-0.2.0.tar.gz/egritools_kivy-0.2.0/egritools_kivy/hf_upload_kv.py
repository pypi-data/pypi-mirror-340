
"""
Huggingface Dataset Uploader GUI - Kivy Edition

Created by Christopher (Egrigor86)
"""

__version__ = "0.3.0"


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from plyer import filechooser
from datasets import Dataset
from huggingface_hub import HfApi
import os
import json

class HFUploader(BoxLayout):
    selected_mode = StringProperty("1")
    use_system_prompt = BooleanProperty(False)
    token_override = None

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)

        self.dataset_name = TextInput(hint_text="Dataset Name", multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.dataset_name)

        self.add_widget(Label(text="Upload Type:", size_hint_y=None, height=30))
        self.mode_buttons = []
        mode_labels = [
            ("All JSON fields (structured)", "1"),
            ("Only 'fact' or 'answer' (text-based)", "2"),
            ("Q&A only", "3"),
            ("Q&A with tags + optional system prompt", "4"),
            ("Text files as dataset", "5")
        ]
        for label, val in mode_labels:
            btn = ToggleButton(text=label, group="mode", size_hint_y=None, height=40, allow_no_selection=False)
            btn.bind(on_press=self.set_mode)
            if val == "1":
                btn.state = "down"
            btn.mode_value = val
            self.mode_buttons.append(btn)
            self.add_widget(btn)

        self.checkbox_layout = BoxLayout(size_hint_y=None, height=40)
        self.system_prompt_checkbox = CheckBox()
        self.system_prompt_checkbox.bind(active=self.toggle_system_prompt)
        self.checkbox_layout.add_widget(self.system_prompt_checkbox)
        self.checkbox_layout.add_widget(Label(text="Include System Prompt"))
        self.add_widget(self.checkbox_layout)

        self.system_prompt_input = TextInput(hint_text="System Prompt (optional)", multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.system_prompt_input)
        self.system_prompt_input.disabled = True
        self.checkbox_layout.disabled = True

        token_btn = Button(text="Browse for Token File", size_hint_y=None, height=40)
        token_btn.bind(on_press=self.browse_token_file)
        self.add_widget(token_btn)

        self.upload_btn = Button(text="Upload Dataset", size_hint_y=None, height=50)
        self.upload_btn.bind(on_press=self.upload_dataset)
        self.add_widget(self.upload_btn)

        self.log_output = Label(text="", size_hint_y=None, height=300)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.log_output)
        self.add_widget(scroll)

    def browse_token_file(self, instance):
        filechooser.open_file(on_selection=self.set_token_file)

    def set_token_file(self, selection):
        if selection:
            try:
                with open(selection[0], "r", encoding="utf-8") as f:
                    self.token_override = f.read().strip()
                    self.log("✅ Token loaded from file.")
            except Exception as e:
                self.log(f"❌ Failed to read token file: {str(e)}")

    def show_token_help_popup(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(
            text="No HuggingFace token found.\n\nPlease create a file named 'hf.token' in this folder.\n\nIt should contain your HuggingFace access token as a single line."
        ))
        close_btn = Button(text="OK", size_hint_y=None, height=40)
        popup = Popup(title="Missing HuggingFace Token", content=content, size_hint=(0.9, 0.6))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()

    def get_hf_token(self):
        if self.token_override:
            return self.token_override

        token = os.getenv("HF_TOKEN")
        if token:
            return token

        token_path = os.path.join(os.getcwd(), "hf.token")
        if os.path.exists(token_path):
            with open(token_path, "r", encoding="utf-8") as f:
                return f.read().strip()

        return None

    def set_mode(self, instance):
        self.selected_mode = instance.mode_value
        if self.selected_mode == "4":
            self.checkbox_layout.disabled = False
            self.system_prompt_input.disabled = not self.system_prompt_checkbox.active
        else:
            self.checkbox_layout.disabled = True
            self.system_prompt_input.disabled = True
            self.system_prompt_checkbox.active = False

    def toggle_system_prompt(self, instance, value):
        self.system_prompt_input.disabled = not value

    def log(self, message):
        self.log_output.text += message + "\n"

    def sanitize_entry(self, entry):
        required_fields = {"id": None, "question": "", "answer": "", "tags": [], "system": None}
        clean = {}

        for key in required_fields:
            value = entry.get(key, required_fields[key])
            if key == "id":
                try: clean[key] = int(value) if value is not None else None
                except: clean[key] = None
            elif key in ("question", "answer"):
                clean[key] = str(value) if value is not None else ""
            elif key == "tags":
                clean[key] = [str(tag) for tag in value] if isinstance(value, list) else [str(value)] if value else []
            elif key == "system":
                clean[key] = str(value) if value else None

        for key, value in entry.items():
            if key not in clean:
                try:
                    if isinstance(value, (str, int, float, bool)) or value is None:
                        clean[key] = value
                    elif isinstance(value, list):
                        clean[key] = [str(v) for v in value if isinstance(v, (str, int, float, bool))]
                    elif isinstance(value, dict):
                        clean[key] = self.sanitize_entry(value)
                    else:
                        clean[key] = str(value)
                except:
                    continue
        return clean

    def process_files(self):
        full, fact, qa, ans, tagged, text_data = [], [], [], [], [], []
        for fname in os.listdir():
            if fname.endswith('.txt'):
                try:
                    with open(fname, encoding='utf-8') as f:
                        text_data.append({"content": f.read()})
                except:
                    continue
            elif fname.endswith('.json'):
                try:
                    with open(fname, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                            if not isinstance(data, list):
                                raise ValueError()
                        except:
                            f.seek(0)
                            raw = f.read().strip()
                            data = json.loads(f"[{raw.replace('}\n{', '}, {')}]")
                    for entry in data:
                        if not isinstance(entry, dict):
                            continue
                        clean = self.sanitize_entry(entry)
                        if "fact" in clean:
                            full.append(clean)
                            fact.append({"content": clean["fact"]})
                        elif "question" in clean and "answer" in clean:
                            qa.append(clean)
                            ans.append({"content": clean["answer"]})
                            t = {
                                "prompt": clean["question"],
                                "response": clean["answer"],
                                "tags": clean.get("tags", [])
                            }
                            if "system" in clean:
                                t["system"] = clean["system"]
                            tagged.append(self.sanitize_entry(t))
                except Exception as e:
                    self.log(f"⚠️ Skipped file {fname}: {str(e)}")
        return full, fact, qa, ans, tagged, text_data

    def upload_dataset(self, instance):
        try:
            token = self.get_hf_token()
            if not token:
                self.log("❌ No HuggingFace token found.")
                self.show_token_help_popup()
                return

            name = self.dataset_name.text.strip()
            if not name:
                self.log("❌ Dataset name required.")
                return

            full, fact, qa, ans, tagged, text_data = self.process_files()

            if self.selected_mode == "1":
                dataset = Dataset.from_list([self.sanitize_entry(e) for e in full + qa])
            elif self.selected_mode == "2":
                dataset = Dataset.from_list([self.sanitize_entry(e) for e in fact + ans])
            elif self.selected_mode == "3":
                dataset = Dataset.from_list([self.sanitize_entry(e) for e in qa])
            elif self.selected_mode == "4":
                if self.system_prompt_checkbox.active and self.system_prompt_input.text.strip():
                    for e in tagged:
                        if "system" not in e:
                            e["system"] = self.system_prompt_input.text.strip()
                dataset = Dataset.from_list([self.sanitize_entry(e) for e in tagged])
            elif self.selected_mode == "5":
                dataset = Dataset.from_list([self.sanitize_entry(e) for e in text_data])
            else:
                self.log("❌ Invalid mode selected.")
                return

            dataset.save_to_disk(f"./{name}")
            HfApi().create_repo(repo_id=name, token=token, repo_type="dataset", exist_ok=True)
            dataset.push_to_hub(name, token=token)

            self.log(f"✅ Uploaded '{name}' successfully.")
        except Exception as e:
            self.log(f"❌ Upload failed: {str(e)}")

class HFUploaderApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return HFUploader()

def main():
    HFUploaderApp().run()

if __name__ == "__main__":
    main()
