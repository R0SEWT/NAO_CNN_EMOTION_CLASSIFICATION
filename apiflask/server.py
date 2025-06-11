from flask import Flask

app = Flask(__name__)

@app.route("/emocion")
def emocion():
    return "happy"  # o "confused" según modelo

app.run(host="0.0.0.0", port=5001)


