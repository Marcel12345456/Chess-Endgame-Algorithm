import requests

def get_tablebase_data(fen):
    return requests.get("https://tablebase.lichess.org/standard", params={"fen": fen})