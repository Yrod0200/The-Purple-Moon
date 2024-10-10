DEBUG = False # WARNING:
# USE THIS ONLY FOR DEBBUGING, SINCE THE TERMINAL WILL SPAM TEXT


import sys

resp = input("Would you like to start from this file? (Y/n)" )

if not (resp.lower() == "y" or resp == ""):
    sys.exit(1)
else:
    pass

import socket
import threading
import string
import random 
import ast
import traceback

IP =  "0.0.0.0" # Change this only if you know what to do.
PORT = 6100
STRING_HANDLE_PORT = 9857




MAX_CLIENTS = int(input("How many people?"))

srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
str_srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_sock.bind((IP, PORT))
str_srv_sock.bind((IP, STRING_HANDLE_PORT))
if DEBUG:
    print("VERBOSE: Binded port sucessfully")

clients = {}
cli_addrs = {}

def generate_code():
    letters = random.choices(string.ascii_uppercase, k=4)
    numbers = random.choices(string.digits, k=3)

    code = f"{letters[0]}{letters[1]}{numbers[0]}{numbers[1]}{numbers[2]}{letters[2]}{letters[3]}"
    return code

def handle_clients():
    print("Started listening for clients...")

    event_thread = threading.Thread(target=accept_string_port_connections)
    event_thread.start()

    while True:  
        srv_sock.listen(MAX_CLIENTS)

        client_socket, client_addr =  srv_sock.accept()
        if len(clients) >= MAX_CLIENTS:
            print(f"Connection with {client_addr} refused: max client exceeded")
            client_socket.close()


        print(f"Connection accepted from: {client_addr}")

        client_thread = threading.Thread(target=connection_auth, args=(client_socket, client_addr))
        client_thread.start()
        if DEBUG:
            print(f"VERBOSE: Client {client_addr} thread started...")
def connection_auth(csock, caddr):
    try:
        csock.sendall(b"COMMAND: USERNAME_ENTER")
        if DEBUG:
            print(f"VERBOSE: Sent username request for {caddr} ")

        username =  csock.recv(1024).decode('utf-8')
        if not username.strip():
            print(f"USERNAME FOR {caddr} is invalid closing connection!")
            csock.close()
        if DEBUG:
            print(f"VERBOSE: Sucessful accepted username from {caddr}: {username}")

        csock.sendall(b"COMMAND: PASSWORD_ENTER")

        code = generate_code()

        print(f"Code for {username}: {code}")

        if DEBUG:
            print("VERBOSE: Sent password...")

        data = csock.recv(1024).decode('utf-8')

        if DEBUG:
            print(f"VERBOSE: RECIEVED DATA {data}")

        if not data == code:
            csock.sendall(b"AUTH: FAILED: INCORRECT_PASSWORD")
            csock.close()
        else:
            csock.sendall(b"AUTH: SUCESSFULL")
            clients[username] = {"ip":caddr, "username":username, "csock":csock }
            sending_thread = threading.Thread(target=listen_for_client_data, args=(csock, caddr))
            sending_thread.start()
        if DEBUG:
            print("VERBOSE: Sucessfull passed client password phase")
    except Exception as e:
        if DEBUG:
            print(f"ERROR LISTENING FOR DATA: {e}")

def listen_for_client_data(csock, caddr):
    print(f"Listening data from {caddr}")
    while True:
        data = csock.recv(4096)
        if data:
            for cli, cdata in clients.items():
                if cdata["csock"] != csock:
                    try:
                        cdata["csock"].sendall(data)
                    except ConnectionError:
                        if DEBUG:
                            print(f"Client {cli} failed to recieve data. ")


def accept_string_port_connections():
    str_srv_sock.listen(MAX_CLIENTS)
    if DEBUG:
        print("VERBOSE: Started for listening the string port interface...")
    while True:
        try:
            csock, caddr = str_srv_sock.accept()


            csock.sendall("HANDSHAKE: GET: IP_ADDRESS".encode('utf-8'))

            ip_response = csock.recv(1024).decode('utf-8')

            if ip_response.startswith("HANDSHAKE: POST: IP_ADDRESS:"):
                syncd_ip = ip_response.removeprefix("HANDSHAKE: POST: IP_ADDRESS:")
                if DEBUG:
                    print(f"VERBOSE: Sucessfully linked up ip {syncd_ip} with {caddr}")
                if len(syncd_ip) > 25:
                    print("VERBOSE: OVERFLOWED IP! CLOSING CONNECTION! ")
                    csock.close()
                new_ip = ast.literal_eval(syncd_ip)
                if DEBUG:
                    print(f"IP: {syncd_ip}")
                new_ip_dict = {}
                new_ip_dict["ip"] = caddr
                new_ip_dict["mainip"] = syncd_ip
                cli_addrs[syncd_ip[0]] = new_ip_dict
                if DEBUG:
                    print(f"CHANGED: {cli_addrs}")
                csock.sendall(b"HANDSHAKE: IP_ADDRESS: SUCESSFULL")


        except Exception as e:
            if DEBUG:
                print(f"VERBOSE: ERROR WHEN PAIRING STRING PORT: {e}")
                traceback.print_exc()

if __name__ == "__main__":
    if DEBUG:
        print("VERBOSE: Main detected...")
    handle_clients()
