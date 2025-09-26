lang python
start python app.py

file app.py:
  from flask import Flask
  app = Flask(__name__)

dep python requirements flask==2.3.3

tool rest.get as fetch
tool notifier as notify

call fetch as resp url="https://api.example.com" expect.status=200
if ${resp.data.count} > 10:
  call notify message="High volume"
else:
  call notify message="Low volume"
