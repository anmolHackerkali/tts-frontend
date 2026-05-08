from flask import Flask, render_template
import threading
from bot import start_bot

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# Bot ko alag thread me run karo
threading.Thread(target=start_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)