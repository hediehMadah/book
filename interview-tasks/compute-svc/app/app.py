from flask import Flask, request, jsonify
import os
import time

app = Flask(__name__)

@app.route('/healthz', methods=['GET'])
def health_check():
    return '', 200

@app.route('/readyz', methods=['GET'])
def readiness_check():
    return '', 200

@app.route('/version', methods=['GET'])
def version():
    return jsonify(version=os.environ.get('APP_VERSION', 'unknown')), 200

@app.route('/compute', methods=['POST'])
def compute():
    data = request.json
    n = data.get('n', 0)
    
    def fibonacci(n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)

    start_time = time.time()
    result = fibonacci(n)
    latency = time.time() - start_time

    return jsonify(result=result, latency=latency), 200

@app.route('/metrics', methods=['GET'])
def metrics():
    return 'metrics', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
