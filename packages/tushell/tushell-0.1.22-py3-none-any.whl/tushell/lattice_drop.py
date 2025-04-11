import requests
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file in current directory or from HOME/.env
load_dotenv()
dotenv_path = os.path.join(os.path.expanduser("~"), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

#Add path to current file
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def fetch_echonode_data():
    url = f"{os.getenv('EH_API_URL')}/api/echonode"
    headers = {
        "Authorization": "Bearer ITERAX_TOKEN"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def process_echonode_data(data):
    # Process the data as needed
    return data

def render_echonode_data(data):
    # Render the data as part of the memory key graph
    for key, value in data.items():
        print(f"{key}: {value}")

def emit_live_reports():
    echonode_data = fetch_echonode_data()
    if echonode_data:
        processed_data = process_echonode_data(echonode_data)
        render_echonode_data(processed_data)
        # Additional logic for live reporting
        print("Live report emitted from EchoNode tied to active narrative arcs.")

def fetch_echonode_data_optimized():
    url = f"{os.getenv('EH_API_URL')}/api/echonode"
    headers = {
        "Authorization": "Bearer ITERAX_TOKEN"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def process_echonode_data_optimized(data):
    # Process the data as needed
    return data

def render_echonode_data_optimized(data):
    # Render the data as part of the memory key graph
    for key, value in data.items():
        print(f"{key}: {value}")

def emit_live_reports_optimized():
    echonode_data = fetch_echonode_data_optimized()
    if echonode_data:
        processed_data = process_echonode_data_optimized(echonode_data)
        render_echonode_data_optimized(processed_data)
        # Additional logic for live reporting
        print("Live report emitted from EchoNode tied to active narrative arcs.")
