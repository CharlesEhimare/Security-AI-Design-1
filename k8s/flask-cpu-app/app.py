from flask import Flask
import time
app = Flask(__name__)

def cpu_work(iterations=200000):
    s = 0
    for i in range(iterations):
        s += i*i
    return s

@app.route('/')
def index():
    start = time.time()
    result = cpu_work()
    elapsed = time.time() - start
    return f"done work elapsed={elapsed:.4f}\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
