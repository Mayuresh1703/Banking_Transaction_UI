# Real-Time Banking Transaction Project

<img width="896" height="736" alt="Screenshot 2026-05-14 155106" src="https://github.com/user-attachments/assets/e5f2e3d3-3ee1-4b28-a996-2e9bf5ea1ea9" />
<img width="971" height="836" alt="Screenshot 2026-05-14 160004" src="https://github.com/user-attachments/assets/c8062f25-6fad-4ab8-b5ac-1b2652908684" />
<img width="981" height="731" alt="Screenshot 2026-05-14 160032" src="https://github.com/user-attachments/assets/41179b2f-30b9-45a6-a7d1-d1a3e46f8df3" />
<img width="1030" height="896" alt="Screenshot 2026-05-14 160126" src="https://github.com/user-attachments/assets/1193dcb7-ae80-46ab-ada5-1808f98b2298" />
<img width="1081" height="743" alt="Screenshot 2026-05-14 160157" src="https://github.com/user-attachments/assets/57a52eb7-12d0-4ae0-a24e-e86777063807" />
<img width="1090" height="775" alt="Screenshot 2026-05-14 160220" src="https://github.com/user-attachments/assets/e23d5e8d-3b07-4c19-9637-317709a2e54f" />
<img width="1077" height="767" alt="Screenshot 2026-05-14 160309" src="https://github.com/user-attachments/assets/07538d16-3e4a-4086-bbf0-66e5239375fe" />
<img width="1002" height="722" alt="Screenshot 2026-05-14 160334" src="https://github.com/user-attachments/assets/e3459391-55e7-4022-a8f1-6f8d074f976d" />
<img width="885" height="707" alt="Screenshot 2026-05-14 160348" src="https://github.com/user-attachments/assets/3bc95277-6d26-4848-8609-76fa0ae5e5d4" />




This project demonstrates a simple banking system with user accounts, credit/debit operations, transaction history, and balance tracking using MySQL.

## Features

- Create bank users and accounts
- Deposit and withdraw money
- Transfer funds between users
- Track transaction history
- Query current account balance

## Requirements

- Python 3.10+
- MySQL server
- `mysql-connector-python`
- `Flask`

## Setup

1. Create a MySQL database user and start MySQL.
2. Copy `.env.example` to `.env` and update `DB_HOST`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`.
   - If your MySQL user has no password, set `DB_PASSWORD=` with no value.
   - If you prefer, run `python configure_db.py` to generate `.env` interactively.
3. Verify MySQL connectivity before creating the schema:

```bash
python db_test_connection.py
```

4. Use MySQL Workbench or the provided scripts to verify the connection.
5. Run the schema initializer to create the database and tables:

```bash
python db_setup.py
```

5. Start the API server:

```bash
python app.py
```
5. Start the Tkinter UI:

```bash
python gui.py
```
6. Use the CLI client to perform operations against the database:

```bash
python client/cli.py create-user --name "Alice" --email "alice@example.com"
```

### Using MySQL Workbench

- Open MySQL Workbench and connect to your server.
- Verify that the `bank` database exists after running `db_setup.py`.
- Browse the `users`, `accounts`, and `transactions` tables to confirm data.

5. Use the sample client script in `client/cli.py` to test transactions locally:

```bash
python client/cli.py create-user --name "Alice" --email "alice@example.com"
```
## API Endpoints

- `POST /user` - create user and account
- `POST /deposit` - add money to a user account
- `POST /withdraw` - remove money from a user account
- `POST /transfer` - transfer money between accounts
- `GET /balance/<user_id>` - get current balance
- `GET /transactions/<user_id>` - get transaction history

## Notes

- This is a demo project. In production, add authentication, validation, concurrency safeguards, and transaction isolation.
