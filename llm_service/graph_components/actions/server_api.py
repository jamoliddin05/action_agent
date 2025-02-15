import requests

MOCK_SERVER_URL = "http://mock_server:5000"

def execute_command(command: str) -> dict:
    """
    Sends a Linux command to the mock server for execution.

    Args:
        command (str): The Linux command to be executed.

    Returns:
        dict: The response JSON if successful, or an error message.
    """
    payload = {"command": command}  # Wrap command in a JSON object

    try:
        response = requests.post(f"{MOCK_SERVER_URL}/execute", json=payload)
        response.raise_for_status()  # Raise an error for 4xx and 5xx responses
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}