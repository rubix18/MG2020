import requests

url = 'http://192.168.1.104:5002/upload'

files = {'file': ('test1.mp4', open('replay.mp4', 'rb'))}

x = requests.post(url, files = files)