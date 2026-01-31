import random
import json

class Account:
    def __init__(self,full_name,email,password,national_id,phone_number,balance=0):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.national_id = national_id
        self.phone_number = phone_number
        self.balance = balance
        self.account_number=random.randint(1000000000,9999999999)

    def return_account_number(self):
        return self.account_number
    
    def to_dict(self):
        return {
            "full_name": self.full_name,
            "email": self.email,
            "password": self.password,
            "national_id": self.national_id,
            "phone_number": self.phone_number,
            "balance": int(self.balance),
            "account_number": self.account_number
        }
    
    def account_info(self):
        return self.full_name,self.phone_number,self.account_number,self.balance

class Bank:
    def __init__(self):
        try:
            with open("db.json", "r") as file:
                self.accounts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.accounts = []
            with open("db.json", "w") as file:
                json.dump(self.accounts, file, indent=4)

    def create_account(self, full_name, email, password, national_id, phone_number, balance=0):
        for acc in self.accounts:
            if acc["email"] == email:
                raise ValueError("An account with this email already exists.")
        account = Account(full_name, email, password, national_id, phone_number, balance)
        self.accounts.append(account.to_dict())
        with open("db.json", "w") as file:
            json.dump(self.accounts, file, indent=4)
        return account


    def withdraw(self, account_number, amount):
        for acc in self.accounts:
            if acc["account_number"] == account_number:
                if acc["balance"] >= amount:
                    acc["balance"] -= amount
                    with open("db.json","w")as file:
                        json.dump(self.accounts,file,indent=4)
                    return True
                else:
                    return False  # Insufficient funds
        return False  # Account not found

    def deposit(self, account_number, amount):
        for acc in self.accounts:
            if acc["account_number"] == account_number:
                acc["balance"] += amount
                with open("db.json","w")as file:
                    json.dump(self.accounts,file,indent=4)
                return True
        return False  # Account not found

    

