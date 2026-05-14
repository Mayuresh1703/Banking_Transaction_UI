# Real-Time Banking Transaction Project

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
