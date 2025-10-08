import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# ----------------------------
# Initialize Database
# ----------------------------
def init_db():
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        balance REAL NOT NULL DEFAULT 0.0
    )
    ''')
    conn.commit()
    conn.close()

# ----------------------------
# Main Banking App Class
# ----------------------------
class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏦 Simple Banking System")
        self.root.geometry("440x380")
        self.root.resizable(False, False)

        # Theme state
        self.dark_mode = False
        self.style = ttk.Style()

        # Step 1: Create all widgets first
        self.title_label = tk.Label(
            root,
            text="🏦 Simple Banking System",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=(15, 10))

        btn_width = 30

        self.create_btn = ttk.Button(root, text="🆕 Create Account", command=self.create_account_window, width=btn_width)
        self.deposit_btn = ttk.Button(root, text="📥 Deposit Money", command=self.deposit_window, width=btn_width)
        self.withdraw_btn = ttk.Button(root, text="📤 Withdraw Money", command=self.withdraw_window, width=btn_width)
        self.balance_btn = ttk.Button(root, text="📊 Check Balance", command=self.check_balance_window, width=btn_width)
        self.view_btn = ttk.Button(root, text="📋 View All Accounts", command=self.view_all_accounts, width=btn_width)
        self.theme_btn = ttk.Button(root, text="🌙 Toggle Dark Mode", command=self.toggle_theme, width=btn_width)
        self.exit_btn = ttk.Button(root, text="🚪 Exit", command=root.destroy, width=btn_width)

        for btn in [self.create_btn, self.deposit_btn, self.withdraw_btn,
                    self.balance_btn, self.view_btn, self.theme_btn, self.exit_btn]:
            btn.pack(pady=4)

        # Step 2: Apply theme AFTER all widgets exist
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            bg = "#2b2b2b"
            fg = "white"
            btn_bg = "#3c3f41"
            entry_bg = "#3c3f41"
            tree_bg = "#2b2b2b"
            tree_field_bg = "#3c3f41"
            heading_bg = "#4a4a4a"
            self.root.configure(bg=bg)
            self.title_label.configure(bg=bg, fg=fg)

            self.style.theme_use('clam')
            self.style.configure("TButton", background=btn_bg, foreground="white", borderwidth=1)
            self.style.map("TButton", background=[('active', '#5a5a5a')])
            self.style.configure("TEntry", fieldbackground=entry_bg, foreground="white")
            self.style.configure("Treeview", background=tree_bg, foreground="white", fieldbackground=tree_field_bg)
            self.style.configure("Treeview.Heading", background=heading_bg, foreground="white", font=("Arial", 9, "bold"))
            self.theme_btn.configure(text="☀️ Toggle Light Mode")
        else:
            bg = "white"
            fg = "black"
            self.root.configure(bg=bg)
            self.title_label.configure(bg=bg, fg=fg)

            self.style.theme_use('clam')
            self.style.configure("TButton", background="#e1e1e1", foreground="black", borderwidth=1)
            self.style.map("TButton", background=[('active', '#d0d0d0')])
            self.style.configure("TEntry", fieldbackground="white", foreground="black")
            self.style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
            self.style.configure("Treeview.Heading", background="#f0f0f0", foreground="black", font=("Arial", 9, "bold"))
            self.theme_btn.configure(text="🌙 Toggle Dark Mode")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def get_db_connection(self):
        return sqlite3.connect('banking.db')

    # ------------------ Feature: View All Accounts ------------------
    def view_all_accounts(self):
        win = tk.Toplevel(self.root)
        win.title("📋 All Accounts")
        win.geometry("540x340")
        win.resizable(False, False)
        if self.dark_mode:
            win.configure(bg="#2b2b2b")

        columns = ("ID", "Name", "Balance")
        tree = ttk.Treeview(win, columns=columns, show="headings", height=12)
        tree.heading("ID", text="🆔 Account ID")
        tree.heading("Name", text="👤 Name")
        tree.heading("Balance", text="💰 Balance ($)")

        tree.column("ID", width=100, anchor="center")
        tree.column("Name", width=220)
        tree.column("Balance", width=140, anchor="e")

        v_scroll = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=v_scroll.set)

        conn = self.get_db_connection()
        c = conn.cursor()
        c.execute("SELECT account_id, name, balance FROM accounts")
        for row in c.fetchall():
            tree.insert("", "end", values=(row[0], row[1], f"${row[2]:,.2f}"))
        conn.close()

        tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        v_scroll.pack(side="right", fill="y", pady=10)

        # Apply dark style to Treeview if needed
        if self.dark_mode:
            style = ttk.Style()
            style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#3c3f41")
            style.configure("Treeview.Heading", background="#4a4a4a", foreground="white")

    # ------------------ Feature: Create Account (with ID display) ------------------
    def create_account_window(self):
        win = tk.Toplevel(self.root)
        win.title("🆕 Create Account")
        win.geometry("340x150")
        win.resizable(False, False)
        if self.dark_mode:
            win.configure(bg="#2b2b2b")
            label_bg, label_fg = "#2b2b2b", "white"
        else:
            label_bg, label_fg = "white", "black"

        tk.Label(win, text="Enter your full name:", bg=label_bg, fg=label_fg).pack(pady=(10, 5))
        name_entry = ttk.Entry(win, width=35)
        name_entry.pack(pady=5)

        def submit():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Input Error", "Name cannot be empty!")
                return
            try:
                conn = self.get_db_connection()
                c = conn.cursor()
                c.execute('INSERT INTO accounts (name) VALUES (?)', (name,))
                new_id = c.lastrowid
                conn.commit()
                conn.close()
                messagebox.showinfo(
                    "✅ Success",
                    f"Account created!\n👤 Name: {name}\n🆔 Account ID: {new_id}"
                )
                win.destroy()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
                win.destroy()

        ttk.Button(win, text="🆕 Create Account", command=submit, width=20).pack(pady=10)

    # ------------------ Reusable Transaction Window ------------------
    def _transaction_window(self, title, mode):
        icon = "📥" if mode == "deposit" else "📤"
        win = tk.Toplevel(self.root)
        win.title(f"{icon} {title} Funds")
        win.geometry("340x170")
        win.resizable(False, False)
        if self.dark_mode:
            win.configure(bg="#2b2b2b")
            label_bg, label_fg = "#2b2b2b", "white"
        else:
            label_bg, label_fg = "white", "black"

        tk.Label(win, text="Account ID:", bg=label_bg, fg=label_fg).pack(pady=(10, 3))
        acc_id_entry = ttk.Entry(win, width=25)
        acc_id_entry.pack()

        tk.Label(win, text=f"Amount to {title.lower()} ($):", bg=label_bg, fg=label_fg).pack(pady=(8, 3))
        amount_entry = ttk.Entry(win, width=25)
        amount_entry.pack()

        def process():
            try:
                acc_id = int(acc_id_entry.get())
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive.")

                conn = self.get_db_connection()
                c = conn.cursor()

                if mode == "withdraw":
                    c.execute('SELECT balance FROM accounts WHERE account_id = ?', (acc_id,))
                    result = c.fetchone()
                    if not result:
                        messagebox.showerror("Error", "Account not found!")
                        conn.close()
                        return
                    if result[0] < amount:
                        messagebox.showerror("Error", "Insufficient balance!")
                        conn.close()
                        return
                    c.execute('UPDATE accounts SET balance = balance - ? WHERE account_id = ?', (amount, acc_id))
                else:
                    c.execute('UPDATE accounts SET balance = balance + ? WHERE account_id = ?', (amount, acc_id))

                if c.rowcount == 0:
                    messagebox.showerror("Error", "Account not found!")
                else:
                    conn.commit()
                    messagebox.showinfo("✅ Success", f"${amount:.2f} {title.lower()}ed!")

                conn.close()
                win.destroy()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text=f"{icon} {title}", command=process, width=20).pack(pady=12)

    def deposit_window(self):
        self._transaction_window("Deposit", "deposit")

    def withdraw_window(self):
        self._transaction_window("Withdraw", "withdraw")

    # ------------------ Check Balance ------------------
    def check_balance_window(self):
        win = tk.Toplevel(self.root)
        win.title("📊 Check Balance")
        win.geometry("340x130")
        win.resizable(False, False)
        if self.dark_mode:
            win.configure(bg="#2b2b2b")
            label_bg, label_fg = "#2b2b2b", "white"
        else:
            label_bg, label_fg = "white", "black"

        tk.Label(win, text="Enter Account ID:", bg=label_bg, fg=label_fg).pack(pady=(15, 5))
        acc_id_entry = ttk.Entry(win, width=25)
        acc_id_entry.pack()

        def show_balance():
            try:
                acc_id = int(acc_id_entry.get())
                conn = self.get_db_connection()
                c = conn.cursor()
                c.execute('SELECT name, balance FROM accounts WHERE account_id = ?', (acc_id,))
                result = c.fetchone()
                conn.close()
                if result:
                    name, balance = result
                    messagebox.showinfo(
                        "📊 Balance Info",
                        f"🆔 Account ID: {acc_id}\n👤 Name: {name}\n💰 Balance: ${balance:.2f}"
                    )
                else:
                    messagebox.showerror("Not Found", "Account not found!")
                win.destroy()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid Account ID.")

        ttk.Button(win, text="📊 Check Balance", command=show_balance, width=20).pack(pady=12)

# ----------------------------
# Run Application
# ----------------------------
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop() 