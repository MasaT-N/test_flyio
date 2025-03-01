import requests
import json
import yaml

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

def test_get_document_list(url, secret_key):
    """Tests the /get_document_list endpoint."""
    headers = {'Content-type': 'application/json'}
    data = {'key': secret_key}

    try:
        response = requests.post(url, json=data, headers=headers)  # jsonパラメータに変更

        print(f"Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            print("Test passed: Data retrieved successfully.")
            
            try:
                json_data = response.json()
                print("Returned JSON Data:")
                print(json.dumps(json_data, ensure_ascii=False, indent=4))
            except json.JSONDecodeError as e:
                print(f"Error: Could not decode JSON response: {e}")

        elif response.status_code == 401:
            print("Test failed: Unauthorized access.")
        else:
            print(f"Test failed: Data retrieval failed. Status code: {response.status_code}")
    except requests.exceptions.ConnectionError as e:
        print(f"Error: Connection failed to {url}. Is the Flask app running? Error message: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # URL を config.yaml から読み込む
    config = load_config()
    root_url = config.get("root_url", "http://127.0.0.1:5000") # config.yamlからroot_urlを取得(なかった場合はデフォルトを設定)
    get_document_list_url = f"{root_url}{config.get('get_document_list_url', '/get_document_list')}"

    # SECRET_KEY を書き換える（app.pyのSECRET_KEYと一致させる）
    secret_key = config.get("secret_key", "your_secret_key_here")
    test_get_document_list(get_document_list_url, secret_key)
