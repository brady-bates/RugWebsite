from flask import Flask

# Start
print("hello world")

app = Flask(__name__)

@app.route('/')

def index(): 
    return 'Web App with Python Flask!'

app.run(host='0.0.0.0', port=81)
