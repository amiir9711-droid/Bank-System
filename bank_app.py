from bank_system import Bank
import tkinter as tk
from tkinter import messagebox
import json,os,bcrypt,re
bank = Bank()
def show_password():
    if show_pass_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="•")
def login():
    def hash_password(password: str) -> str:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed.decode()
    def settings():
        root5 = tk.Toplevel(root1)
        root5.title("Settings")
        root5.geometry("200x100+900+400")
        root5.configure(bg="#1e1e2f")
        def password_change_choice():
            pw_window = tk.Toplevel(root5)
            pw_window.title("Change Password")
            pw_window.geometry("300x110+850+400")
            pw_window.configure(bg="#1e1e2f")
            tk.Label(pw_window, text="New Password:", bg="#1e1e2f", fg="white").grid(row=0, column=0, padx=10, pady=5)
            tk.Label(pw_window, text="Confirm Password:", bg="#1e1e2f", fg="white").grid(row=1, column=0, padx=10, pady=5)
            password_entry = tk.Entry(pw_window, show="•")
            password_entry.grid(row=0, column=1, padx=10, pady=5)
            conferm_password_entry = tk.Entry(pw_window, show="•")
            conferm_password_entry.grid(row=1, column=1, padx=10, pady=5)
            def change_password():
                if password_entry.get() == conferm_password_entry.get():
                    new_password = password_entry.get()
                    hashed_new_password = hash_password(new_password)
                    with open("db.json", "r") as file:
                        data = json.load(file)
                    for acc in data:
                        if acc["email"] == user_name:  
                            acc["password"] = hashed_new_password
                            break
                    with open("db.json", "w") as file:
                        json.dump(data, file, indent=4)
                    messagebox.showinfo("Success", "Password changed successfully!")
                    pw_window.destroy()
                else:
                    messagebox.showerror("Error", "Passwords do not match")
            tk.Button(pw_window, text="Change Password", command=change_password, bg="#4CAF50", fg="white").grid(row=3, column=0, columnspan=2, pady=10)
        def phone_number_change_choice():
            phone_window = tk.Toplevel(root5)
            phone_window.title("Change Phone Number")
            phone_window.geometry("300x100+850+350")
            phone_window.configure(bg="#1e1e2f")
            tk.Label(phone_window, text="New Phone Number:", bg="#1e1e2f", fg="white").grid(row=0, column=0, padx=10, pady=10)
            phone_entry = tk.Entry(phone_window)
            phone_entry.grid(row=0, column=1, padx=10, pady=10)
            def change_phone():
                new_phone = phone_entry.get().strip()
                if not new_phone.isdigit():
                    messagebox.showerror("Error", "Phone number must be numeric!")
                    return
                with open("db.json", "r") as file:
                    data = json.load(file)
                for acc in data:
                    if acc["email"] == user_name:  
                        acc["phone_number"] = new_phone
                        break
                with open("db.json", "w") as file:
                    json.dump(data, file, indent=4)
                messagebox.showinfo("Success", "Phone number changed successfully!")
                phone_window.destroy()
            tk.Button(phone_window, text="Change Phone Number", command=change_phone, bg="#4CAF50", fg="white").grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(root5, text="Change Password", command=password_change_choice, bg="#2196F3", fg="white").grid(row=0, column=0, padx=20, pady=10,sticky="w")
        tk.Button(root5, text="Change Phone Number", command=phone_number_change_choice, bg="#2196F3", fg="white").grid(row=1, column=0, padx=20, pady=10,sticky="w")
    def logout():
        root2.destroy()
        root1.deiconify()
    def check_password(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    def transfer():
        def deposite_btn():
            nonlocal balance
            amount = int(deposite_entry.get())
            bank.deposit(account_number, amount)
            balance += amount
            label_balance.config(text=f"{balance}")
        def withdraw_btn():
            nonlocal balance
            amount = int(withdraw_entry.get())
            bank.withdraw(account_number,amount)
            if bank.withdraw(account_number,amount) or balance == amount:
                balance -= amount
                label_balance.config(text=f"{balance}")
            else:
                messagebox.showerror("Error", " Insufficient funds")
        root2.geometry("400x200")
        tk.Button(root2,text="deposite",padx=12,bg="#176BAF",command=deposite_btn).grid(row=5,column=0)
        tk.Button(root2,text="withdraw",padx=10,bg="#176BAF",command=withdraw_btn).grid(row=6,column=0)
        deposite_entry=tk.Entry(root2)
        deposite_entry.grid(row=5,column=1)
        withdraw_entry=tk.Entry(root2)
        withdraw_entry.grid(row=6,column=1)
    user_name=user_entry.get()
    password=password_entry.get()
    with open("db.json","r") as file:
        data=json.load(file)
    for acc in data:
        if acc["email"] == user_name and check_password(password, acc["password"]):
            root1.withdraw()
            root2 = tk.Toplevel(root1)
            root2.configure(bg="#1e1e2f")
            root2.title("Account")
            root2.geometry("400x150+800+400")
            full_name = acc["full_name"]
            balance = acc["balance"]
            phone_number=acc["phone_number"]
            account_number=acc["account_number"]
            tk.Label(root2, text=f"Welcome {full_name}",padx=10,bg="#1e1e2f",anchor="center",foreground="#ffffff",font=("Arial",12,"bold")).grid(row=0, column=0,sticky="e")
            tk.Button(root2,text="⚙️settings",bg="#535353",command=settings).grid(row=0,column=1,sticky="e")
            tk.Label(root2, text=f"Balance:",padx=10,bg="#1e1e2f",foreground="white",font=("Arial",10,"bold")).grid(row=1, column=0,sticky="e")
            label_balance=tk.Label(root2, text=f"{balance}",padx=10,bg="#1e1e2f",foreground="#a09978",font=("Arial",10,"bold"))
            label_balance.grid(row=1, column=1,sticky="w")
            tk.Label(root2, text=f"Phone Number:",padx=10,bg="#1e1e2f",foreground="#ffffff",font=("Arial",10,"bold")).grid(row=2, column=0,sticky="e")
            tk.Label(root2, text=f" {phone_number}",padx=10,bg="#1e1e2f",foreground="#a09978",font=("Arial",10,"bold")).grid(row=2, column=1,sticky="w")
            tk.Label(root2, text=f"Account Number:",padx=10,bg="#1e1e2f",foreground="#ffffff",font=("Arial",10,"bold")).grid(row=3, column=0,sticky="e")
            tk.Label(root2, text=f"{account_number}",padx=10,bg="#1e1e2f",foreground="#a09978",font=("Arial",10,"bold")).grid(row=3, column=1,sticky="w")
            Transfers_btn=tk.Button(root2,text=f"Transfers",padx=40,pady=5,bg="#4CAF50",font=("Arial",10,"bold"),command=transfer)
            Transfers_btn.grid(row=4,column=0,padx=30)
            tk.Button(root2,text="Logout",padx=40,pady=5,bg="#4CAF50",font=("Arial",10,"bold"),command=logout).grid(row=4,column=1)
            return
    messagebox.showerror("Error", "Invalid email or password")
def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.com$"
    return re.match(pattern, email) is not None
def create_account():
    def back_main_page():
        root3.destroy()
        root1.deiconify()
    def show_password():
        if show_pass_var.get():
            password_entry.config(show="")
        else:
            password_entry.config(show="•")
    def show_confirm_password():
        if show_confirm_var.get():
            conferm_password_entry.config(show="")
        else:
            conferm_password_entry.config(show="•")
    def hash_password(password: str) -> str:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed.decode()
    root1.withdraw()
    root3=tk.Toplevel(root1)
    root3.configure(bg="#1e1e2f")
    root3.title("Create Account")
    root3.geometry("500x400+800+300")
    tk.Label(root3, text="Create New Account",padx=40,pady=10,bg="#1e1e2f",foreground="white",font=("Arial",12,"bold")).grid(row=0, column=1,sticky="w")
    tk.Label(root3, text="Full Name:",padx=10,pady=10, bg="#1e1e2f",foreground="white",anchor="w",font=("Arial",10,"bold")).grid(row=1, column=0,sticky="w")
    tk.Label(root3, text="Email:",padx=10,pady=10, bg="#1e1e2f",foreground="white",anchor="w",font=("Arial",10,"bold")).grid(row=2, column=0,sticky="w")
    tk.Label(root3, text="Password:",padx=10,pady=10, bg="#1e1e2f",foreground="white",anchor="w",font=("Arial",10,"bold")).grid(row=3, column=0,sticky="w")
    tk.Label(root3, text="Conferm Password:",padx=10,pady=10, bg="#1e1e2f",foreground="white",anchor="w",font=("Arial",10,"bold")).grid(row=4, column=0,sticky="w")
    tk.Label(root3, text="national_id:",padx=10,pady=10, bg="#1e1e2f",foreground="white",anchor="w",font=("Arial",10,"bold")).grid(row=5, column=0,sticky="w")
    tk.Label(root3, text="phone_number:",padx=10,pady=10, bg="#1e1e2f",foreground="white",anchor="w",font=("Arial",10,"bold")).grid(row=6, column=0,sticky="w")
    tk.Label(root3, text="balance",padx=10,pady=10, bg="#1e1e2f",foreground="white",anchor="w",font=("Arial",10,"bold")).grid(row=7, column=0,sticky="w")
    full_name_entry=tk.Entry(root3)
    full_name_entry.grid(row=1, column=1)
    email_entry=tk.Entry(root3)
    email_entry.grid(row=2, column=1)
    password_entry=tk.Entry(root3,show="•")
    password_entry.grid(row=3, column=1)
    show_password_btn = tk.Checkbutton(root3,variable=show_pass_var,command=show_password,bg="#1e1e2f",activebackground="#1e1e2f")
    show_password_btn.grid(row=3,column=2)
    show_conferm_password_btn = tk.Checkbutton(root3,variable=show_confirm_var,command=show_confirm_password,bg="#1e1e2f",activebackground="#1e1e2f")
    show_conferm_password_btn.grid(row=4,column=2)
    conferm_password_entry=tk.Entry(root3,show="•")
    conferm_password_entry.grid(row=4, column=1)
    national_id_entry=tk.Entry(root3)
    national_id_entry.grid(row=5, column=1)
    phone_number_entry=tk.Entry(root3)
    phone_number_entry.grid(row=6, column=1)
    balance_entry=tk.Entry(root3)
    balance_entry.grid(row=7, column=1)
    def submit_account():
        email = email_entry.get().strip().lower()
        if not is_valid_email(email):
            messagebox.showerror("Error", "Email must be like example@domain.com")
            return
        for acc in bank.accounts:
            if acc["email"] == email:
                messagebox.showerror("Error", "Email is already exists")
                return
        if password_entry.get() == conferm_password_entry.get():
            hashed_password = hash_password(password_entry.get())
            account=bank.create_account(full_name_entry.get(),
                                        email_entry.get(),
                                        hashed_password,
                                        national_id_entry.get(),
                                        phone_number_entry.get(),
                                        balance_entry.get())
            messagebox.showinfo("Account Created",f"Account created successfully!")
            root3.destroy()
            root1.deiconify()
        else:
            messagebox.showerror("Error", "password doesnot match")
    tk.Button(root3, text="Submit",padx=40,bg="#4CAF50",pady=5,foreground="white",font=("Arial",10,"bold"),command=submit_account).grid(row=8, column=1)
    back_main_page_btn=tk.Button(root3,text="Back",command=back_main_page)
    back_main_page_btn.grid(row=8,column=2)
    root3.mainloop()
# Main Window
root1=tk.Tk()
root1.configure(bg="#1e1e2f")
root1.title("KB Bank")
root1.geometry("400x240+800+400") 
tk.Label(root1, text="Welcome to KB Bank",padx=40,pady=10, bg="#1e1e2f",foreground="white",font=("Arial",12,"bold")).grid(row=0, column=1)
tk.Label(root1, text="User name:",padx=10,pady=10,bg="#1e1e2f",foreground="white",font=("Arial",10,"bold")).grid(row=1, column=0)
tk.Label(root1, text="Password:",padx=10,pady=10,bg="#1e1e2f",foreground="white",font=("Arial",10,"bold")).grid(row=2, column=0)
user_entry=tk.Entry(root1)
user_entry.grid(row=1, column=1)
password_entry=tk.Entry(root1,show="•")
password_entry.grid(row=2, column=1)
tk.Label(root1, text="Show password:",bg="#1e1e2f",foreground="white",font=("Arial",9,"bold")).grid(row=3, column=1)
show_pass_var = tk.BooleanVar()
show_confirm_var = tk.BooleanVar()
show_password_btn = tk.Checkbutton(
    root1,
    variable=show_pass_var,
    command=show_password,
    bg="#1e1e2f",
    activebackground="#1e1e2f"
)
show_password_btn.grid(row=2, column=3)
login_button=tk.Button(root1, text="Login",padx=39,pady=5,bg="#4CAF50",foreground="white",font=("Arial",10,"bold"),command=login).grid(row=4, column=1)
create_account_button=tk.Button(root1, text="create account",padx=10,pady=5,bg="#2196F3",foreground="white",font=("Arial",10,"bold"),command=create_account).grid(row=5, column=1)
root1.mainloop()
print("DB PATH:", os.path.abspath("db.json"))
# change password
# change phone number
