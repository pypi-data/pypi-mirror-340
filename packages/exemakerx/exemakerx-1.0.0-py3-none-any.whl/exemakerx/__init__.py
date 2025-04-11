import argparse
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

class ExeMakerX:
    def __init__(self):
        pass

    def convert(self, filepath, onefile=True, noconsole=False, icon=None):
        if not os.path.isfile(filepath) or not filepath.endswith(".py"):
            raise ValueError("Invalid .py file path.")

        command = [sys.executable.replace('pythonw.exe', 'python.exe'), '-m', 'PyInstaller', filepath]

        if onefile:
            command.append("--onefile")
        if noconsole:
            command.append("--noconsole")
        if icon:
            command.extend(["--icon", icon])

        subprocess.run(command)

    def launch_gui(self):
        def select_file():
            path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
            if path:
                entry_file.delete(0, tk.END)
                entry_file.insert(0, path)

        def build():
            path = entry_file.get()
            if not path:
                messagebox.showerror("Error", "Please select a .py file.")
                return

            try:
                self.convert(
                    filepath=path,
                    onefile=var_onefile.get(),
                    noconsole=not var_console.get(),
                    icon=entry_icon.get() or None
                )
                messagebox.showinfo("Success", "✔ .exe created successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        root = tk.Tk()
        root.title("ExeMakerX")
        root.geometry("450x280")
        root.resizable(False, False)

        tk.Label(root, text="📝 Python File:", anchor='w').pack(fill='x', padx=10, pady=(10, 0))
        entry_file = tk.Entry(root, width=60)
        entry_file.pack(padx=10, pady=2)
        tk.Button(root, text="Browse", command=select_file).pack(pady=3)

        tk.Label(root, text="🎨 Icon File (.ico):", anchor='w').pack(fill='x', padx=10, pady=(10, 0))
        entry_icon = tk.Entry(root, width=60)
        entry_icon.pack(padx=10, pady=2)

        var_onefile = tk.BooleanVar(value=True)
        var_console = tk.BooleanVar(value=True)

        tk.Checkbutton(root, text="Bundle into one .exe", variable=var_onefile).pack(pady=5)
        tk.Checkbutton(root, text="Show Console Window", variable=var_console).pack(pady=5)

        tk.Button(root, text="🚀 Convert to .exe", command=build, bg='#3cba54', fg='white').pack(pady=10)

        root.mainloop()

def main():
    parser = argparse.ArgumentParser(description="ExeMakerX - .py to .exe converter with GUI/CLI")
    parser.add_argument("command", help="Command to run: convert or gui")
    parser.add_argument("filepath", nargs="?", help="Python file path")
    parser.add_argument("--noconsole", action="store_true", help="Hide terminal window")
    parser.add_argument("--no-onefile", action="store_true", help="Don't bundle into one file")
    parser.add_argument("--icon", help="Path to .ico file")
    args = parser.parse_args()

    tool = ExeMakerX()

    if args.command == "convert":
        if not args.filepath:
            print("Please provide a Python file path.")
            return
        tool.convert(
            filepath=args.filepath,
            onefile=not args.no_onefile,
            noconsole=args.noconsole,
            icon=args.icon
        )
    elif args.command == "gui":
        tool.launch_gui()
    else:
        print("Unknown command. Use 'convert' or 'gui'.")

if __name__ == "__main__":
    main()