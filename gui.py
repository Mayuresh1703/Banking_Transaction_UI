import tkinter as tk
from tkinter import messagebox, ttk
from decimal import Decimal

from db import get_connection


class BankingUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Banking Transaction UI')
        self.geometry('700x520')
        self.current_user_id = None
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.notebook.add(self.create_login_signup_tab(), text='Login/Signup')
        self.notebook.add(self.create_user_tab(), text='Create User')
        self.notebook.add(self.create_account_tab(), text='Deposit / Withdraw')
        self.notebook.add(self.create_transfer_tab(), text='Transfer')
        self.notebook.add(self.create_balance_tab(), text='Balance & History')

        self.log_text = tk.Text(self, height=8, state='disabled', wrap='word')
        self.log_text.pack(fill='x', padx=10, pady=(0, 10))

        self.update_tab_states()

    def update_tab_states(self):
        # Enable/disable tabs based on login status
        for i in range(1, 5):  # Skip Login/Signup tab
            if self.current_user_id:
                self.notebook.tab(i, state='normal')
            else:
                self.notebook.tab(i, state='disabled')

    def create_login_signup_tab(self):
        frame = ttk.Frame(self)

        ttk.Label(frame, text='Current User:', font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        self.current_user_label = ttk.Label(frame, text='Not logged in', foreground='red')
        self.current_user_label.grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Separator(frame, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)

        ttk.Label(frame, text='Login (Email):').grid(row=3, column=0, sticky='w', pady=4)
        self.login_email = ttk.Entry(frame, width=20)
        self.login_email.grid(row=3, column=1, pady=4, sticky='w')
        ttk.Button(frame, text='Login', command=self.login).grid(row=4, column=1, pady=8, sticky='w')

        ttk.Separator(frame, orient='horizontal').grid(row=5, column=0, columnspan=2, sticky='ew', pady=10)

        ttk.Label(frame, text='Signup (Name):').grid(row=6, column=0, sticky='w', pady=4)
        self.signup_name = ttk.Entry(frame, width=20)
        self.signup_name.grid(row=6, column=1, pady=4, sticky='w')

        ttk.Label(frame, text='Signup (Email):').grid(row=7, column=0, sticky='w', pady=4)
        self.signup_email = ttk.Entry(frame, width=20)
        self.signup_email.grid(row=7, column=1, pady=4, sticky='w')

        ttk.Button(frame, text='Signup', command=self.signup).grid(row=8, column=1, pady=8, sticky='w')

        ttk.Button(frame, text='Logout', command=self.logout).grid(row=9, column=1, pady=12, sticky='w')

        return frame

    def login(self):
        email = self.login_email.get().strip()
        if not email:
            messagebox.showwarning('Validation', 'Email is required for login.')
            return

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM users WHERE email = %s', (email,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror('Error', 'User not found.')
                return
            user_id, name = row
            self.current_user_id = user_id
            self.current_user_label.config(text=f'Logged in as {name} (ID: {user_id})', foreground='green')
            self.update_tab_states()
            messagebox.showinfo('Success', f'Logged in as {name}.')
            self.log(f'Logged in as user_id={user_id} ({email})')
        except Exception as exc:
            messagebox.showerror('Error', str(exc))
            self.log(f'Error during login: {exc}')
        finally:
            cursor.close()
            conn.close()

    def signup(self):
        name = self.signup_name.get().strip()
        email = self.signup_email.get().strip()
        if not name or not email:
            messagebox.showwarning('Validation', 'Name and email are required for signup.')
            return

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
            user_id = cursor.lastrowid
            cursor.execute('INSERT INTO accounts (user_id, balance) VALUES (%s, %s)', (user_id, Decimal('0.00')))
            conn.commit()
            self.current_user_id = user_id
            self.current_user_label.config(text=f'Logged in as {name} (ID: {user_id})', foreground='green')
            self.update_tab_states()
            messagebox.showinfo('Success', f'Account created and logged in as {name} (Email: {email}).')
            self.log(f'Signed up and logged in as user_id={user_id} ({email})')
            # Clear signup fields
            self.signup_name.delete(0, 'end')
            self.signup_email.delete(0, 'end')
        except Exception as exc:
            conn.rollback()
            messagebox.showerror('Error', str(exc))
            self.log(f'Error during signup: {exc}')
        finally:
            cursor.close()
            conn.close()

    def logout(self):
        self.current_user_id = None
        self.current_user_label.config(text='Not logged in', foreground='red')
        self.update_tab_states()
        messagebox.showinfo('Success', 'Logged out.')
        self.log('Logged out')

    def create_user_tab(self):
        frame = ttk.Frame(self)

        ttk.Label(frame, text='Name:').grid(row=0, column=0, sticky='w', pady=4)
        self.name_input = ttk.Entry(frame, width=40)
        self.name_input.grid(row=0, column=1, pady=4, sticky='w')

        ttk.Label(frame, text='Email:').grid(row=1, column=0, sticky='w', pady=4)
        self.email_input = ttk.Entry(frame, width=40)
        self.email_input.grid(row=1, column=1, pady=4, sticky='w')

        ttk.Button(frame, text='Create User', command=self.create_user).grid(row=2, column=1, pady=12, sticky='w')

        return frame

    def create_account_tab(self):
        frame = ttk.Frame(self)

        ttk.Label(frame, text='Amount:').grid(row=0, column=0, sticky='w', pady=4)
        self.account_amount = ttk.Entry(frame, width=20)
        self.account_amount.grid(row=0, column=1, pady=4, sticky='w')

        ttk.Button(frame, text='Deposit', command=self.deposit).grid(row=1, column=0, pady=12, sticky='w')
        ttk.Button(frame, text='Withdraw', command=self.withdraw).grid(row=1, column=1, pady=12, sticky='w')

        return frame

    def create_transfer_tab(self):
        frame = ttk.Frame(self)

        ttk.Label(frame, text='Target User ID:').grid(row=0, column=0, sticky='w', pady=4)
        self.transfer_target_id = ttk.Entry(frame, width=20)
        self.transfer_target_id.grid(row=0, column=1, pady=4, sticky='w')

        ttk.Label(frame, text='Amount:').grid(row=1, column=0, sticky='w', pady=4)
        self.transfer_amount = ttk.Entry(frame, width=20)
        self.transfer_amount.grid(row=1, column=1, pady=4, sticky='w')

        ttk.Button(frame, text='Transfer Funds', command=self.transfer).grid(row=2, column=1, pady=12, sticky='w')

        return frame

    def create_balance_tab(self):
        frame = ttk.Frame(self)

        ttk.Button(frame, text='Get Balance', command=self.get_balance).grid(row=0, column=0, pady=12, sticky='w')
        ttk.Button(frame, text='Show Transactions', command=self.show_transactions).grid(row=0, column=1, pady=12, sticky='w')

        self.transactions_list = tk.Listbox(frame, height=12, width=80)
        self.transactions_list.grid(row=1, column=0, columnspan=2, pady=6, sticky='w')

        return frame

    def log(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert('end', message + '\n')
        self.log_text.configure(state='disabled')
        self.log_text.see('end')

    def create_user(self):
        name = self.name_input.get().strip()
        email = self.email_input.get().strip()
        if not name or not email:
            messagebox.showwarning('Validation', 'Name and email are required.')
            return

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Email already exists. Use a different email or login instead.')
                return

            cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
            user_id = cursor.lastrowid
            cursor.execute('INSERT INTO accounts (user_id, balance) VALUES (%s, %s)', (user_id, Decimal('0.00')))
            conn.commit()
            messagebox.showinfo('Success', f'User created with ID {user_id}.')
            self.log(f'Created user {name} ({email}) with user_id={user_id}')
            self.name_input.delete(0, 'end')
            self.email_input.delete(0, 'end')
        except Exception as exc:
            conn.rollback()
            messagebox.showerror('Error', str(exc))
            self.log(f'Error creating user: {exc}')
        finally:
            cursor.close()
            conn.close()

    def deposit(self):
        self._change_balance('deposit')

    def withdraw(self):
        self._change_balance('withdraw')

    def _change_balance(self, action):
        if not self.current_user_id:
            messagebox.showwarning('Error', 'Please login first.')
            return

        amount_value = self.account_amount.get().strip()
        if not amount_value:
            messagebox.showwarning('Validation', 'Amount is required.')
            return

        try:
            amount = Decimal(amount_value)
        except Exception:
            messagebox.showwarning('Validation', 'Invalid amount format.')
            return

        if amount <= 0:
            messagebox.showwarning('Validation', 'Amount must be positive.')
            return

        conn = get_connection()
        try:
            cursor = conn.cursor()
            row = self._get_account(cursor, self.current_user_id, lock=True)
            if not row:
                messagebox.showerror('Error', 'Account not found.')
                return

            account_id, balance = row
            balance = Decimal(balance)
            if action == 'withdraw' and balance < amount:
                messagebox.showerror('Error', 'Insufficient funds.')
                return

            new_balance = balance + amount if action == 'deposit' else balance - amount
            cursor.execute('UPDATE accounts SET balance = %s WHERE id = %s', (new_balance, account_id))
            cursor.execute(
                'INSERT INTO transactions (account_id, type, amount, description) VALUES (%s, %s, %s, %s)',
                (account_id, action, amount, action.capitalize())
            )
            conn.commit()
            messagebox.showinfo('Success', f'{action.capitalize()} completed. New balance: {new_balance}.')
            self.log(f'{action.capitalize()} {amount} for user_id={self.current_user_id}; new_balance={new_balance}')
        except Exception as exc:
            conn.rollback()
            messagebox.showerror('Error', str(exc))
            self.log(f'Error during {action}: {exc}')
        finally:
            cursor.close()
            conn.close()

    def _get_account(self, cursor, user_id, lock=False):
        sql = 'SELECT id, balance FROM accounts WHERE user_id = %s'
        if lock:
            sql += ' FOR UPDATE'
        cursor.execute(sql, (user_id,))
        return cursor.fetchone()

    def transfer(self):
        if not self.current_user_id:
            messagebox.showwarning('Error', 'Please login first.')
            return

        target_id = self.transfer_target_id.get().strip()
        amount_value = self.transfer_amount.get().strip()
        if not target_id or not amount_value:
            messagebox.showwarning('Validation', 'Target user ID and amount are required.')
            return

        try:
            amount = Decimal(amount_value)
        except Exception:
            messagebox.showwarning('Validation', 'Invalid amount format.')
            return

        source_id = self.current_user_id
        if source_id == target_id:
            messagebox.showwarning('Validation', 'Source and target must differ.')
            return
        if amount <= 0:
            messagebox.showwarning('Validation', 'Amount must be positive.')
            return

        conn = get_connection()
        try:
            cursor = conn.cursor()
            source = self._get_account(cursor, source_id, lock=True)
            target = self._get_account(cursor, target_id, lock=True)
            if not source or not target:
                messagebox.showerror('Error', 'Source or target account not found.')
                return

            source_account_id, source_balance = source
            target_account_id, target_balance = target
            source_balance = Decimal(source_balance)
            target_balance = Decimal(target_balance)

            if source_balance < amount:
                messagebox.showerror('Error', 'Insufficient funds.')
                return

            cursor.execute('UPDATE accounts SET balance = %s WHERE id = %s', (source_balance - amount, source_account_id))
            cursor.execute('UPDATE accounts SET balance = %s WHERE id = %s', (target_balance + amount, target_account_id))
            cursor.execute(
                'INSERT INTO transactions (account_id, type, amount, related_account_id, description) VALUES (%s, %s, %s, %s, %s)',
                (source_account_id, 'transfer_out', amount, target_account_id, f'Transfer to user {target_id}')
            )
            cursor.execute(
                'INSERT INTO transactions (account_id, type, amount, related_account_id, description) VALUES (%s, %s, %s, %s, %s)',
                (target_account_id, 'transfer_in', amount, source_account_id, f'Transfer from user {source_id}')
            )
            conn.commit()
            messagebox.showinfo('Success', f'Transferred {amount} from user {source_id} to user {target_id}.')
            self.log(f'Transfer {amount} from {source_id} to {target_id}')
        except Exception as exc:
            conn.rollback()
            messagebox.showerror('Error', str(exc))
            self.log(f'Error during transfer: {exc}')
        finally:
            cursor.close()
            conn.close()

    def get_balance(self):
        if not self.current_user_id:
            messagebox.showwarning('Error', 'Please login first.')
            return

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT balance FROM accounts WHERE user_id = %s', (self.current_user_id,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror('Error', 'Account not found.')
                return
            balance = Decimal(row[0])
            messagebox.showinfo('Balance', f'Balance for user {self.current_user_id}: {balance}')
            self.log(f'Balance check for user_id={self.current_user_id}: {balance}')
        except Exception as exc:
            messagebox.showerror('Error', str(exc))
            self.log(f'Error checking balance: {exc}')
        finally:
            cursor.close()
            conn.close()

    def show_transactions(self):
        if not self.current_user_id:
            messagebox.showwarning('Error', 'Please login first.')
            return

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM accounts WHERE user_id = %s', (self.current_user_id,))
            account_row = cursor.fetchone()
            if not account_row:
                messagebox.showerror('Error', 'Account not found.')
                return

            account_id = account_row[0]
            cursor.execute(
                'SELECT type, amount, related_account_id, description, created_at FROM transactions WHERE account_id = %s ORDER BY created_at DESC',
                (account_id,)
            )
            rows = cursor.fetchall()
            self.transactions_list.delete(0, 'end')
            for row in rows:
                tx_type, amount, related, desc, created_at = row
                self.transactions_list.insert('end', f'{created_at} - {tx_type} {amount} ({desc}) related={related}')
            self.log(f'Showed {len(rows)} transactions for user_id={self.current_user_id}')
        except Exception as exc:
            messagebox.showerror('Error', str(exc))
            self.log(f'Error fetching transactions: {exc}')
        finally:
            cursor.close()
            conn.close()


if __name__ == '__main__':
    app = BankingUI()
    app.mainloop()
