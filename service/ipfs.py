import requests
import pandas as pd
import json


# Replace <IPFS_GATEWAY_URL> with the URL of your IPFS gateway
ipfs_gateway_url = 'http://127.0.0.1:5001'

# Set up the API endpoint URL
api_endpoint = ipfs_gateway_url + '/api/v0/add'


def add_files(files):
    response = requests.post(api_endpoint, files=files, params={'wrap-with-directory': True})
    lines = response.text.strip().split('\n')
    json_data = f'[{",".join(lines)}]'
    data = json.loads(json_data)
    df = pd.json_normalize(data)
    return df 



