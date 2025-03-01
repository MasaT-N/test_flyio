import requests
import json
import os
import time
import yaml
from typing import Dict

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


def main():
    # URL of the /submit endpoint (adjust if your app runs on a different port)
    config = load_config()
    root_url = config.get("root_url", "http://127.0.0.1:5000")  # デフォルトはhttp://127.0.0.1:5000
    submit_url = f"{root_url}{config.get('submit_url', '/submit')}"  # デフォルトは/submit

    for i in range(1, 6):
        print(f"Test {i}:")
        # Path to the test JSON file (create a test.json file with sample data)
        json_file_path = os.path.join(os.getcwd(), f'C:/github/test_flyio/testData/test{i}.json')

        # Run the test
        test_submit_endpoint(submit_url, json_file_path)
        # time.sleep(1)


def test_submit_endpoint(url, json_file):
    """
    Tests the /submit endpoint of a FastAPI application by sending a POST request
    with data from a JSON file.

    Args:
        url (str): The URL of the /submit endpoint.
        json_file (str): The path to the JSON file containing the data to be posted.
    """
    try:
        # Load JSON data from the file
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        #Pydanticモデルでjsonをチェックしたいときは、以下の行を追加(必要に応じて)
        # from pydantic import ValidationError
        # from app import Document
        # try:
        #    Document(**data)
        # except ValidationError as e:
        #    print(f"Error: Invalid JSON format according to Pydantic Model:{e}")
        #    return


    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {json_file}: {e}")
        return

    try:
        # Send POST request to the /submit endpoint
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)  # json パラメータを使用

        # Check the response status code and content
        print(f"Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            print("Test passed: Data submitted successfully.")
        else:
            print(f"Test failed: Data submission failed. Status code: {response.status_code}")
    except requests.exceptions.ConnectionError as e:
        print(f"Error: Connection failed to {url}. Is the FastAPI app running? Error message: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
