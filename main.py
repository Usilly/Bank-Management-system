import customtkinter as ctk
from tkinter import messagebox
import string
import json
import random
from pathlib import Path


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Bank:

    database = 'data.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fr:
                data = json.loads(fr.read())

    except Exception as err:
        print(f"Some exception occurred: {err}")

    @staticmethod
    def update():
        with open(Bank.database, 'w') as fs:
            fs.write(json.dumps(Bank.data, indent=4))

    @classmethod
    def account_generate(cls):
        alpha = random.choices(string.ascii_uppercase, k=3)
        digi = random.choices(string.digits, k=3)
        ids = alpha + digi
        random.shuffle(ids)
        return "".join(ids)

    @staticmethod
    def find_user(accountno, pin):

        userdata = [
            i for i in Bank.data
            if i['accountNo'] == accountno and i['pin'] == pin
        ]

        if userdata:
            return userdata[0]

        return None


class BankGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("700x650")

        title = ctk.CTkLabel(
            root,
            text="BANK MANAGEMENT SYSTEM",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=20)

        self.frame = ctk.CTkFrame(root)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.create_widgets()

    def clear_frame(self):

        for widget in self.frame.winfo_children():
            widget.destroy()

    def create_widgets(self):

        self.clear_frame()

        buttons = [
            ("Create Account", self.create_account_ui),
            ("Deposit Money", self.deposit_ui),
            ("Withdraw Money", self.withdraw_ui),
            ("Show Details", self.show_details_ui),
            ("Update Details", self.update_details_ui),
            ("Delete Account", self.delete_account_ui),
            ("Exit", self.root.destroy)
        ]

        for text, command in buttons:

            btn = ctk.CTkButton(
                self.frame,
                text=text,
                command=command,
                height=45,
                font=("Arial", 16)
            )

            btn.pack(pady=12, padx=30, fill="x")

    def create_account_ui(self):

        self.clear_frame()

        labels = ["Name", "Age", "PIN", "Email"]
        entries = {}

        for label in labels:

            ctk.CTkLabel(self.frame, text=label).pack(pady=5)

            entry = ctk.CTkEntry(self.frame, width=300)
            entry.pack(pady=5)

            entries[label.lower()] = entry

        def create_account():

            info = {
                'name': entries['name'].get(),
                'age': entries['age'].get(),
                'pin': entries['pin'].get(),
                'email': entries['email'].get(),
                'accountNo': Bank.account_generate(),
                'balance': 0
            }

            if int(info['age']) < 18 or len(info['pin']) != 4:

                messagebox.showerror(
                    "Error",
                    "Age must be 18+ and PIN must be 4 digits"
                )

                return

            Bank.data.append(info)
            Bank.update()

            messagebox.showinfo(
                "Success",
                f"Account Created Successfully\n\nAccount No: {info['accountNo']}"
            )

            self.create_widgets()

        ctk.CTkButton(
            self.frame,
            text="Create Account",
            command=create_account
        ).pack(pady=20)

        ctk.CTkButton(
            self.frame,
            text="Back",
            command=self.create_widgets
        ).pack(pady=10)

    def deposit_ui(self):

        self.transaction_ui("deposit")

    def withdraw_ui(self):

        self.transaction_ui("withdraw")

    def transaction_ui(self, action):

        self.clear_frame()

        ctk.CTkLabel(self.frame, text="Account Number").pack(pady=5)
        account_entry = ctk.CTkEntry(self.frame, width=300)
        account_entry.pack(pady=5)

        ctk.CTkLabel(self.frame, text="PIN").pack(pady=5)
        pin_entry = ctk.CTkEntry(self.frame, width=300, show="*")
        pin_entry.pack(pady=5)

        ctk.CTkLabel(self.frame, text="Amount").pack(pady=5)
        amount_entry = ctk.CTkEntry(self.frame, width=300)
        amount_entry.pack(pady=5)

        def perform_action():

            user = Bank.find_user(
                account_entry.get(),
                pin_entry.get()
            )

            if not user:
                messagebox.showerror("Error", "Account not found")
                return

            amount = int(amount_entry.get())

            if amount < 1:
                messagebox.showerror("Error", "Invalid amount")
                return

            if action == "deposit":

                if amount > 10000:
                    messagebox.showerror(
                        "Error",
                        "Cannot deposit more than 10K"
                    )
                    return

                user['balance'] += amount

                messagebox.showinfo(
                    "Success",
                    f"Amount Deposited\n\nBalance: {user['balance']}"
                )

            else:

                if amount > user['balance']:
                    messagebox.showerror(
                        "Error",
                        "Insufficient balance"
                    )
                    return

                user['balance'] -= amount

                messagebox.showinfo(
                    "Success",
                    f"Amount Withdrawn\n\nBalance: {user['balance']}"
                )

            Bank.update()

        ctk.CTkButton(
            self.frame,
            text=action.capitalize(),
            command=perform_action
        ).pack(pady=20)

        ctk.CTkButton(
            self.frame,
            text="Back",
            command=self.create_widgets
        ).pack(pady=10)

    def show_details_ui(self):

        self.clear_frame()

        ctk.CTkLabel(self.frame, text="Account Number").pack(pady=5)
        account_entry = ctk.CTkEntry(self.frame, width=300)
        account_entry.pack(pady=5)

        ctk.CTkLabel(self.frame, text="PIN").pack(pady=5)
        pin_entry = ctk.CTkEntry(self.frame, width=300, show="*")
        pin_entry.pack(pady=5)

        result = ctk.CTkTextbox(self.frame, width=500, height=250)
        result.pack(pady=20)

        def show_details():

            user = Bank.find_user(
                account_entry.get(),
                pin_entry.get()
            )

            if not user:
                messagebox.showerror("Error", "Account not found")
                return

            result.delete("1.0", "end")

            for i in user:

                value = user[i]

                if i == 'pin':
                    value = "****"

                result.insert("end", f"{i} : {value}\n")

        ctk.CTkButton(
            self.frame,
            text="Show Details",
            command=show_details
        ).pack(pady=10)

        ctk.CTkButton(
            self.frame,
            text="Back",
            command=self.create_widgets
        ).pack(pady=10)

    def update_details_ui(self):

        self.clear_frame()

        labels = [
            "Account Number",
            "PIN",
            "New Name",
            "New Email",
            "New PIN"
        ]

        entries = {}

        for label in labels:

            ctk.CTkLabel(self.frame, text=label).pack(pady=5)

            entry = ctk.CTkEntry(self.frame, width=300)
            entry.pack(pady=5)

            entries[label] = entry

        def update_details():

            user = Bank.find_user(
                entries['Account Number'].get(),
                entries['PIN'].get()
            )

            if not user:
                messagebox.showerror("Error", "Account not found")
                return

            if entries['New Name'].get():
                user['name'] = entries['New Name'].get()

            if entries['New Email'].get():
                user['email'] = entries['New Email'].get()

            if entries['New PIN'].get():

                if len(entries['New PIN'].get()) != 4:
                    messagebox.showerror(
                        "Error",
                        "PIN must be 4 digits"
                    )
                    return

                user['pin'] = entries['New PIN'].get()

            Bank.update()

            messagebox.showinfo(
                "Success",
                "Details updated successfully"
            )

        ctk.CTkButton(
            self.frame,
            text="Update Details",
            command=update_details
        ).pack(pady=20)

        ctk.CTkButton(
            self.frame,
            text="Back",
            command=self.create_widgets
        ).pack(pady=10)

    def delete_account_ui(self):

        self.clear_frame()

        ctk.CTkLabel(self.frame, text="Account Number").pack(pady=5)
        account_entry = ctk.CTkEntry(self.frame, width=300)
        account_entry.pack(pady=5)

        ctk.CTkLabel(self.frame, text="PIN").pack(pady=5)
        pin_entry = ctk.CTkEntry(self.frame, width=300, show="*")
        pin_entry.pack(pady=5)

        def delete_account():

            user = Bank.find_user(
                account_entry.get(),
                pin_entry.get()
            )

            if not user:
                messagebox.showerror("Error", "Account not found")
                return

            Bank.data.remove(user)
            Bank.update()

            messagebox.showinfo(
                "Success",
                "Account deleted successfully"
            )

            self.create_widgets()

        ctk.CTkButton(
            self.frame,
            text="Delete Account",
            fg_color="red",
            hover_color="darkred",
            command=delete_account
        ).pack(pady=20)

        ctk.CTkButton(
            self.frame,
            text="Back",
            command=self.create_widgets
        ).pack(pady=10)


root = ctk.CTk()
app = BankGUI(root)
root.mainloop()
