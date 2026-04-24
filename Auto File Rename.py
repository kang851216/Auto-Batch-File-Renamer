import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def browse_folder():
    selected = filedialog.askdirectory(title="Select folder containing target files")
    if selected:
        folder_var.set(selected)


def apply_rename():
    folder_path = folder_var.get().strip()
    rule = rule_var.get().strip()
    option = option_var.get()
    status_var.set("Validating inputs...")

    if not folder_path:
        messagebox.showerror("Missing Folder", "Please select a target folder.")
        status_var.set("Missing folder path.")
        return
    if not os.path.isdir(folder_path):
        messagebox.showerror("Invalid Folder", "The selected folder does not exist.")
        status_var.set("Invalid folder path.")
        return
    if not rule:
        messagebox.showerror("Missing Rule", "Please enter a file name rule.")
        status_var.set("Missing rename rule.")
        return

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not files:
        messagebox.showinfo("No Files", "No files found in the selected folder.")
        status_var.set("No files found in selected folder.")
        return

    status_var.set(f"Processing {len(files)} file(s)...")

    renamed = 0
    skipped = 0
    failed = []
    for file_name in files:
        name, ext = os.path.splitext(file_name)

        if option == 1:
            new_name = rule + name + ext
        elif option == 2:
            new_name = name + rule + ext
        elif option == 3:
            if name.startswith(rule):
                new_name = name[len(rule):] + ext
            else:
                append_log(f"Skipped (prefix not found): {file_name}")
                skipped += 1
                continue
        elif option == 4:
            if name.endswith(rule):
                new_name = name[: -len(rule)] + ext
            else:
                append_log(f"Skipped (suffix not found): {file_name}")
                skipped += 1
                continue

        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(folder_path, new_name)

        try:
            os.rename(old_path, new_path)
            renamed += 1
            append_log(f"Renamed: {file_name}  →  {new_name}")
        except Exception as e:
            failed.append(f"{file_name}: {e}")
            append_log(f"Failed:  {file_name}: {e}")

    summary = f"Renamed: {renamed}  |  Skipped: {skipped}  |  Failed: {len(failed)}  (of {len(files)} total)"
    append_log(summary)
    status_var.set(summary)
    if failed:
        messagebox.showwarning(
            "Completed with Errors",
            f"Renamed {renamed}, skipped {skipped} of {len(files)} files.\n\nFailed:\n" + "\n".join(failed),
        )
    else:
        messagebox.showinfo("Done", f"Renamed {renamed}, skipped {skipped} of {len(files)} file(s).")


def append_log(message):
    log_box.config(state="normal")
    log_box.insert("end", f"{message}\n")
    log_box.see("end")
    log_box.config(state="disabled")


def clear_log():
    log_box.config(state="normal")
    log_box.delete("1.0", "end")
    log_box.config(state="disabled")
    status_var.set("Log cleared.")


# ── Root window ──────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Auto File Renamer")
root.geometry("900x640")
root.minsize(840, 580)

style = ttk.Style(root)
style.theme_use("clam")
style.configure("App.TFrame", background="#f3f6fb")
style.configure("Card.TLabelframe", background="#ffffff", padding=12)
style.configure("Card.TLabelframe.Label", font=("Segoe UI", 10, "bold"), foreground="#1f2937")
style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), background="#f3f6fb", foreground="#111827")
style.configure("SubHeader.TLabel", font=("Segoe UI", 10), background="#f3f6fb", foreground="#4b5563")
style.configure("Status.TLabel", font=("Segoe UI", 9), background="#eaf1fb", foreground="#1d4ed8", padding=8)
style.configure("Accent.TButton", font=("Segoe UI", 9, "bold"))

folder_var = tk.StringVar()
option_var = tk.IntVar(value=1)
rule_var = tk.StringVar()
status_var = tk.StringVar(value="Ready")

main_frame = ttk.Frame(root, style="App.TFrame", padding=16)
main_frame.pack(fill="both", expand=True)

header_frame = ttk.Frame(main_frame, style="App.TFrame")
header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 12))
ttk.Label(header_frame, text="Auto File Renamer", style="Header.TLabel").grid(row=0, column=0, sticky="w")
ttk.Label(
    header_frame,
    text="Batch rename files with prefix/suffix add/remove rules.",
    style="SubHeader.TLabel",
).grid(row=1, column=0, sticky="w", pady=(2, 0))

inputs_frame = ttk.LabelFrame(main_frame, text="Inputs", style="Card.TLabelframe")
inputs_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))
inputs_frame.columnconfigure(1, weight=1)

# ── Folder path row ───────────────────────────────────────────────────────────
ttk.Label(inputs_frame, text="Folder Path:").grid(
    row=0, column=0, sticky="w", pady=(0, 8)
)
folder_entry = ttk.Entry(inputs_frame, textvariable=folder_var)
folder_entry.grid(row=0, column=1, sticky="we", padx=(8, 6), pady=(0, 8))
ttk.Button(inputs_frame, text="Browse…", command=browse_folder).grid(
    row=0, column=2, sticky="w", pady=(0, 8)
)

# ── File name rule row ────────────────────────────────────────────────────────
ttk.Label(inputs_frame, text="File Name Rule:").grid(
    row=1, column=0, sticky="w"
)
rule_entry = ttk.Entry(inputs_frame, textvariable=rule_var)
rule_entry.grid(row=1, column=1, sticky="we", padx=(8, 6))

# ── Option selector ───────────────────────────────────────────────────────────
option_frame = ttk.LabelFrame(main_frame, text="Rename Options", style="Card.TLabelframe")
option_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 10))

ttk.Radiobutton(
    option_frame,
    text="Option 1 — Add rule text in FRONT of the existing file name",
    variable=option_var,
    value=1,
).pack(fill="x")
ttk.Radiobutton(
    option_frame,
    text="Option 2 — Add rule text AFTER the existing file name (before extension)",
    variable=option_var,
    value=2,
).pack(fill="x")
ttk.Radiobutton(
    option_frame,
    text="Option 3 — Remove rule text from the FRONT of the file name (if present)",
    variable=option_var,
    value=3,
).pack(fill="x")
ttk.Radiobutton(
    option_frame,
    text="Option 4 — Remove rule text from the BACK of the file name (before extension, if present)",
    variable=option_var,
    value=4,
).pack(fill="x")

# ── Action buttons ────────────────────────────────────────────────────────────
action_frame = ttk.Frame(main_frame, style="App.TFrame")
action_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 10))
action_frame.columnconfigure(0, weight=1)

ttk.Button(action_frame, text="Clear Log", command=clear_log).grid(row=0, column=1, padx=(0, 8))
ttk.Button(action_frame, text="Apply Rename", style="Accent.TButton", command=apply_rename).grid(row=0, column=2)

# ── Log box ───────────────────────────────────────────────────────────────────
log_frame = ttk.LabelFrame(main_frame, text="Activity Log", style="Card.TLabelframe")
log_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
log_frame.rowconfigure(0, weight=1)
log_frame.columnconfigure(0, weight=1)

log_box = tk.Text(
    log_frame,
    height=14,
    state="disabled",
    bg="#f9fafb",
    fg="#111827",
    relief="flat",
    borderwidth=0,
    padx=8,
    pady=8,
    font=("Consolas", 10),
)
log_box.grid(row=0, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(log_frame, command=log_box.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
log_box.config(yscrollcommand=scrollbar.set)

status_label = ttk.Label(main_frame, textvariable=status_var, style="Status.TLabel", anchor="w")
status_label.grid(row=5, column=0, columnspan=3, sticky="ew")

main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(4, weight=1)

folder_entry.focus_set()

root.mainloop()
