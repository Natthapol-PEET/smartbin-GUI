import requests

def check_internet():
    url = "https://kusechatbot.csc.ku.ac.th/_smartbin/v1/bin/secret/types"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to the Internet")
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")