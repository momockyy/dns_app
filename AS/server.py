import socket

DNS_DB_FILE = "dns_records.txt"

# Store DNS records
def save_record(name, value):
    with open(DNS_DB_FILE, "a") as file:
        file.write(f"{name} {value}\n")

# Retrieve DNS records
def get_record(name):
    try:
        with open(DNS_DB_FILE, "r") as file:
            for line in file:
                parts = line.strip().split()
                if parts[0] == name:
                    return parts[1]
    except FileNotFoundError:
        return None
    return None

# UDP Server for AS
def start_dns_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 53533))

    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode().split("\n")

        if "VALUE=" in message[2]:  # Registration request
            _, name = message[1].split("=")
            _, value = message[2].split("=")
            save_record(name, value)
        else:  # Query request
            _, name = message[1].split("=")
            value = get_record(name)
            response = f"TYPE=A\nNAME={name}\nVALUE={value if value else 'NOT FOUND'}\nTTL=10\n"
            sock.sendto(response.encode(), addr)

if __name__ == "__main__":
    start_dns_server()
