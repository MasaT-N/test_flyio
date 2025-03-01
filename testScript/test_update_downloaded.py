import requests
import json
import yaml

def load_config(config_file="config.yaml"):
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

def test_update_downloaded(url, secret_key, document_id, downloaded):
    """Tests the /update_downloaded endpoint."""
    headers = {'Content-type': 'application/json'}
    data = {'key': secret_key, 'document_id': document_id, 'downloaded': downloaded}

    try:
        response = requests.post(url, json=data, headers=headers)  # jsonパラメータに変更

        print(f"Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            print(f"Test passed: {document_id}'s downloaded updated successfully to {downloaded}.")
        elif response.status_code == 401:
            print("Test failed: Unauthorized access.")
        elif response.status_code == 404:
            print("Test failed: document_id not found.")
        elif response.status_code == 400:
            print("Test failed: document_id is required or downloaded must be 0 or 1.")
        else:
            print(f"Test failed: downloaded update failed. Status code: {response.status_code}")
    except requests.exceptions.ConnectionError as e:
        print(f"Error: Connection failed to {url}. Is the Flask app running? Error message: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # URL を config.yaml から読み込む
    config = load_config()
    root_url = config.get("root_url", "http://127.0.0.1:5000") # config.yamlからroot_urlを取得(なかった場合はデフォルトを設定)
    update_downloaded_url = f"{root_url}{config.get('update_downloaded_url', '/update_downloaded')}"

    # app.pyのSECRET_KEYと一致させる
    secret_key = config.get("secret_key", "your_secret_key_here")
    # 実際に存在するdocument_idを指定する
    document_id = 41677
    #テストケースの追加
    test_update_downloaded(update_downloaded_url, secret_key, document_id, 0)
    test_update_downloaded(update_downloaded_url, secret_key, document_id, 1)
    #test error case
    # wrong secret key
    test_update_downloaded(update_downloaded_url, "wrong_secret_key", document_id, 0)
    # wrong document_id
    test_update_downloaded(update_downloaded_url, secret_key, 9999, 0)
    # document_id is not exist
    test_update_downloaded(update_downloaded_url, secret_key, "", 0)
    # downloaded is not 0 or 1
    test_update_downloaded(update_downloaded_url, secret_key, document_id, 2)

