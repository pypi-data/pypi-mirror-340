import subprocess

def main():
    print("""
🧰 EGRIGOR'S Kivy TOOLKIT
=======================
1. Change File Extensions
2. Create Python Venv
3. Upload to HuggingFace
4. Preclean JSON Files
5. Offline Wheel Manager
6. GPT2 Trainer
7. Combine TXT
8. Exit
""")
    choice = input("Pick a tool (1-7): ").strip()

    commands = {
        "1": "change-extension-kv",
        "2": "create-venv-kv",
        "3": "hf-upload-kv",
        "4": "preclean-gui-kv",
        "5": "wheel-manager-kv",
        "6": "gpt2-trainer-kv",
        "7": "combine-txt-kv"
    }

    if choice in commands:
        subprocess.run(commands[choice], shell=True)
    elif choice == "8":
        print("Goodbye.")
    else:
        print("Invalid selection.")
