DEBUG = True # WARNING:
# USE THIS ONLY FOR DEBBUGING, SINCE THE TERMINAL WILL SPAM TEXT


#test

import socket
import threading
import string
import random 
IP =  "localhost"
PORT = 6100
STRING_HANDLE_PORT = 9857

MAX_CLIENTS = int(input("How many people?"))

srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
str_srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_sock.bind((IP, PORT))
str_srv_sock.bind((IP, STRING_HANDLE_PORT))
if DEBUG:
    print("VERBOSE: Binded port sucessfully")

clients = []
cli_addrs = []

def generate_code():
    letters = random.choices(string.ascii_uppercase, k=4)
    numbers = random.choices(string.digits, k=3)

    code = f"{letters[0]}{letters[1]}{numbers[0]}{numbers[1]}{numbers[2]}{letters[2]}{letters[3]}"
    return code

def handle_clients():
    print("Started listening for clients...")
    while True:  
        srv_sock.listen(MAX_CLIENTS)
        client_socket, client_addr =  srv_sock.accept()
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
        if DEBUG:
            print(f"VERBOSE: Sucessful accepted username from {caddr}: {username}")
        print(f"Going back to password connection...")

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
        else:
            csock.sendall(b"AUTH: SUCESSFULL")
            clients.append(csock)
            cli_addrs.append(caddr)
            sending_thread = threading.Thread(target=listen_for_client_data, args=(csock, caddr, username))
            sending_thread.start()
        if DEBUG:
            print("VERBOSE: Sucessfull passed client password phase")
    except:
        csock.close()
    finally:
        pass

def listen_for_client_data(csock, caddr, username):
    print(f"Listening data from {caddr}")
    while True:
        data = csock.recv(4096)
        if data:
            for cli in clients:
                if cli != csock:
                    cli.sendall(data)


def accept_string_port_connections():
    str_srv_sock.listen(MAX_CLIENTS)
    if DEBUG:
        print("VERBOSE: Started for listening the string port interface...")
    while True:
        try:
            csock, caddr = str_srv_sock.accept()
            if DEBUG:
                print(f"VERBOSE: String Port Accepted from {caddr}")
            if not caddr in cli_addrs:
                if DEBUG:
                    print("VERBOSE: ", cli_addrs, "and", caddr)

                csock.sendall(b"FATAL_ERROR: NOT_AUTHED_IN")
                if DEBUG:
                    print("VERBOSE: CLIENT NOT LOGGED IN.")
                csock.close()
            else:
                if DEBUG:
                    print("VERBOSE: Stabilished Connection in Port STRING")
                csock.sendall(b"HANDSHAKE: ACCEPT")

                if DEBUG:
                    print("VERBOSE: Sucessfully sent handshake to accept.")
                response = csock.recv(1024).decode('utf-8')
                if response.startswith("HANDSHAKE: OK"):
                    print("Sucessfully stabilhised handshake connecton.")
                    while True:
                        pass
                else:
                    if DEBUG:
                        print(f"VERBOSE: Invalid handshake: {response}. Expected: HANDSHAKE: OK")

        except Exception as e:
            if DEBUG:
                print(f"VERBOSE: ERROR WHEN PAIRING STRING PORT: {e}")


if __name__ == "__main__":
    handle_clients()