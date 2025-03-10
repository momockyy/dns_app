from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

# Compute Fibonacci sequence
def fibonacci(n):
    if n < 0:
        return None
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n+1):
            a, b = b, a + b
        return b

# Register FS with AS
@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    if not data or 'hostname' not in data or 'ip' not in data or 'as_ip' not in data or 'as_port' not in data:
        return "Bad Request", 400

    hostname = data['hostname']
    ip_address = data['ip']
    as_ip = data['as_ip']
    as_port = int(data['as_port'])

    # Register hostname with AS using UDP
    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip_address}\nTTL=10\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (as_ip, as_port))
    sock.close()

    return "Registered", 201

# Serve Fibonacci requests
@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')
    if not number or not number.isdigit():
        return "Bad Request", 400

    fib_value = fibonacci(int(number))
    return jsonify({"fibonacci": fib_value}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
