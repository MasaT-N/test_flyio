import requests
import json
import yaml
import os
import dotenv

# .envファイルから環境変数を読み込む
dotenv.load_dotenv()

def load_config(config_file=r"C:\github\test_flyio\testScript\config.yaml"):
    """Loads configuration from a YAML file.

    Args:
        config_file (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration data loaded from the file.
    """
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_file}")
        return {}
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML format in {config_file}: {e}")
        return {}

def test_init_db(url, secret_key):
    """Tests the /init_db endpoint."""
    headers = {'Content-type': 'application/json'}
    data = {'key': secret_key}

    try:
        response = requests.post(url, json=data, headers=headers)  # jsonパラメータに変更

        print(f"Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            print("Test passed: init_db successfully.")

        elif response.status_code == 401:
            print("Test failed: Unauthorized access.")
        else:
            print(f"Test failed: init_db failed. Status code: {response.status_code}")
    except requests.exceptions.ConnectionError as e:
        print(f"Error: Connection failed to {url}. Is the Flask app running? Error message: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # URL を config.yaml から読み込む
    config = load_config()
    root_url = config.get("root_url", "http://127.0.0.1:5000") # config.yamlからroot_urlを取得(なかった場合はデフォルトを設定)
    init_db_url = f"{root_url}{'/init_db'}"

    # SECRET_KEY を書き換える（app.pyのSECRET_KEYと一致させる）
    secret_key = os.environ.get("SECRET_KEY", "your_secret_key_here")
    test_init_db(init_db_url, secret_key)

