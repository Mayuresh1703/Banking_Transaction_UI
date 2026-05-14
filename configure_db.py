import os
from pathlib import Path

from dotenv import load_dotenv


def prompt_value(prompt, default=''):
    value = input(f'{prompt} [{default}]: ').strip()
    return value if value else default


def main():
    env_path = Path(__file__).with_name('.env')
    if env_path.exists():
        print(f'Found existing .env at {env_path}.')
        overwrite = input('Overwrite existing .env? (y/N): ').strip().lower()
        if overwrite != 'y':
            print('Keeping existing .env. No changes made.')
            return

    host = prompt_value('DB_HOST', '127.0.0.1')
    port = prompt_value('DB_PORT', '3306')
    user = prompt_value('DB_USER', 'root')
    password = input('DB_PASSWORD (leave empty for no password): ').strip()
    auth_plugin = prompt_value('DB_AUTH_PLUGIN', '')
    db_name = prompt_value('DB_NAME', 'bank')
    api_url = prompt_value('BANKING_API_URL', 'http://127.0.0.1:5000')

    env_contents = (
        f'DB_HOST={host}\n'
        f'DB_PORT={port}\n'
        f'DB_USER={user}\n'
        f'DB_PASSWORD={password}\n'
        f'DB_AUTH_PLUGIN={auth_plugin}\n'
        f'DB_NAME={db_name}\n'
        f'BANKING_API_URL={api_url}\n'
    )

    env_path.write_text(env_contents, encoding='utf-8')
    print(f'Created .env at {env_path}.')
    print('Run python db_test_connection.py to verify credentials.')


if __name__ == '__main__':
    load_dotenv()
    main()
