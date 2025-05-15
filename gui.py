import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import threading
import datetime
import os

BG_COLOR = "#f0f4f7"
FG_COLOR = "#212121"
BTN_BG_COLOR = "#007acc"
BTN_FG_COLOR = "#fff"
FONT_HEADER = ("Segoe UI", 22, "bold")
FONT_LABEL = ("Segoe UI", 12)
FONT_ENTRY = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 11, "bold")
FONT_LOG = ("Consolas", 10)
PAD_Y = 12
PAD_X = 20

class BackupAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChronoUser & Backup Automation System")
        self.root.geometry("700x650")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        header = tk.Label(self.root, text="Backup Automation System", font=FONT_HEADER, bg=BG_COLOR, fg=FG_COLOR)
        header.pack(pady=(20, 10))

        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(pady=PAD_Y, padx=PAD_X, fill=tk.X)

        tk.Label(frame, text="Source Folder:", font=FONT_LABEL, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky='w')
        self.source_entry = tk.Entry(frame, font=FONT_ENTRY, width=52)
        self.source_entry.grid(row=1, column=0, padx=(0,10), pady=(0, PAD_Y))
        tk.Button(frame, text="Browse", font=FONT_BTN, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR, command=self.select_source).grid(row=1, column=1, pady=(0, PAD_Y))

        tk.Label(frame, text="Destination Folder:", font=FONT_LABEL, bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky='w')
        self.dest_entry = tk.Entry(frame, font=FONT_ENTRY, width=52)
        self.dest_entry.grid(row=3, column=0, padx=(0,10), pady=(0, PAD_Y))
        tk.Button(frame, text="Browse", font=FONT_BTN, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR, command=self.select_destination).grid(row=3, column=1, pady=(0, PAD_Y))

        tk.Label(frame, text="Backup Frequency:", font=FONT_LABEL, bg=BG_COLOR, fg=FG_COLOR).grid(row=4, column=0, sticky='w')
        self.frequency_var = tk.StringVar(value="daily")
        freq_frame = tk.Frame(frame, bg=BG_COLOR)
        freq_frame.grid(row=5, column=0, sticky='w', pady=(0, PAD_Y))
        tk.Radiobutton(freq_frame, text="Daily", variable=self.frequency_var, value="daily", font=FONT_LABEL, bg=BG_COLOR, fg=FG_COLOR).pack(side='left', padx=10)
        tk.Radiobutton(freq_frame, text="Weekly", variable=self.frequency_var, value="weekly", font=FONT_LABEL, bg=BG_COLOR, fg=FG_COLOR).pack(side='left', padx=10)
        tk.Radiobutton(freq_frame, text="Monthly", variable=self.frequency_var, value="monthly", font=FONT_LABEL, bg=BG_COLOR, fg=FG_COLOR).pack(side='left', padx=10)

        tk.Label(frame, text="Compression:", font=FONT_LABEL, bg=BG_COLOR, fg=FG_COLOR).grid(row=6, column=0, sticky='w')
        self.compression_var = tk.StringVar(value="gzip")
        comp_frame = tk.Frame(frame, bg=BG_COLOR)
        comp_frame.grid(row=7, column=0, sticky='w', pady=(0, PAD_Y))
        tk.Radiobutton(comp_frame, text="None", variable=self.compression_var, value="none", font=FONT_LABEL, bg=BG_COLOR, fg=FG_COLOR).pack(side='left', padx=10)
        tk.Radiobutton(comp_frame, text="gzip", variable=self.compression_var, value="gzip", font=FONT_LABEL, bg=BG_COLOR, fg=FG_COLOR).pack(side='left', padx=10)
        tk.Radiobutton(comp_frame, text="bzip2", variable=self.compression_var, value="bzip2", font=FONT_LABEL, bg=BG_COLOR, fg=FG_COLOR).pack(side='left', padx=10)

        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=(0, PAD_Y))

        self.start_btn = tk.Button(btn_frame, text="Start Backup", font=FONT_BTN, bg="#28a745", fg="white", width=20, command=self.start_backup_thread)
        self.start_btn.pack(side='left', padx=20)

        self.log_btn = tk.Button(btn_frame, text="View Backup Logs", font=FONT_BTN, bg="#17a2b8", fg="white", width=20, command=self.show_logs)
        self.log_btn.pack(side='left', padx=20)

        self.log_frame = tk.Frame(self.root, bg="#222", height=200)
        self.log_text = scrolledtext.ScrolledText(self.log_frame, height=12, bg="#111", fg="#efe", font=FONT_LOG)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def select_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, folder)

    def select_destination(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, folder)

    def start_backup_thread(self):
        t = threading.Thread(target=self.start_backup)
        t.start()

    def start_backup(self):
        source = self.source_entry.get()
        destination = self.dest_entry.get()
        frequency = self.frequency_var.get()
        compression = self.compression_var.get()

        if not source or not destination:
            messagebox.showerror("Input Error", "Please select both source and destination folders.")
            return

        # Ensure log frame is visible before writing log
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=PAD_X, pady=(0, PAD_Y))

        # Disable start button during backup
        self.start_btn.config(state=tk.DISABLED)

        # Clear previous logs
        self.log_text.delete(1.0, tk.END)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] Starting backup...\n")
        self.log_text.see(tk.END)

        try:
            cmd = ["bash", "backup_automation.sh", source, destination, frequency, compression]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            for line in iter(process.stdout.readline, ''):
                if line:
                    # Update log in GUI thread safely
                    self.log_text.after(0, self.log_text.insert, tk.END, line)
                    self.log_text.after(0, self.log_text.see, tk.END)

            process.stdout.close()
            process.wait()

            finish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if process.returncode == 0:
                self.log_text.after(0, self.log_text.insert, tk.END, f"[{finish_time}] Backup finished successfully.\n")
            else:
                self.log_text.after(0, self.log_text.insert, tk.END, f"[{finish_time}] Backup finished with errors.\n")

        except Exception as e:
            messagebox.showerror("Backup Failed", f"An error occurred during backup:\n{e}")

        # Re-enable start button
        self.start_btn.after(0, self.start_btn.config, {'state': tk.NORMAL})

    def show_logs(self):
        log_path = "./logs/backup.log"
        if not os.path.exists(log_path):
            messagebox.showinfo("No Logs", "No backup logs found.")
            return

        with open(log_path, "r") as f:
            content = f.read()

        log_window = tk.Toplevel(self.root)
        log_window.title("Backup Logs")
        log_window.geometry("600x400")
        log_window.configure(bg="#222")

        text_widget = scrolledtext.ScrolledText(log_window, bg="#111", fg="#efe", font=FONT_LOG)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupAutomationApp(root)
    root.mainloop()
