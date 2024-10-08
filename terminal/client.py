import socket
import pyaudio
import threading

IP = input("Enter the IP you want to connect: ")
PORT = 6100
STRING_HANDLE_PORT = 9857

#VOICE CHAT OPTIONS:
# (ONLY CONFIG IF YOU KNOW WHAT'S YOU DOOIM)
RATE = 44100
TYPE = pyaudio.paInt16
CHANNELS = 2
BUFFER = 4096 # IF YOU CHANGE THIS TO A SMALLER OR BIGGER NUMBER IT CAN STOP WORKING 
# UNTIL THE SERVER AND OTHER CLIENTS IS CONFIGURIRED.

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.connect((IP, PORT))
event_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def is_utf_8(data):
    try:
        data.decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False


def start_connection():
    try:
        uname_input = main_socket.recv(1024).decode('utf-8')

        if uname_input.startswith("COMMAND: USERNAME"):
            username = input("Insert Username: ")
            main_socket.sendall(username.encode('utf-8'))

        data =  main_socket.recv(1024).decode('utf-8')

        if data.startswith("COMMAND: PASSWORD_ENTER"):

            password = input("Insert the password shown on the server... ")
            main_socket.sendall(password.encode('utf-8'))

            response = main_socket.recv(1024).decode('utf-8')
            if response.startswith("AUTH: FAILED: INCORRECT_PASSWORD"):
                print("Incorrect password. Aborting for stopping brute force attacks...")
            elif response.startswith("AUTH: SUCESSFULL"):
                print("Password is correct! Starting Session...")
                snd_trd = threading.Thread(target=send_data)
                wrt_trd = threading.Thread(target=write_data)
                snd_trd.start()
                wrt_trd.start()
                snd_trd.join()
                wrt_trd.join()

    finally:
        main_socket.close()

pyaud = pyaudio.PyAudio()

inp_stream = pyaud.open(
    rate=RATE,
    channels=CHANNELS,
    format=TYPE,
    input=True,
    frames_per_buffer=BUFFER
)
out_stream = pyaud.open(
    rate=RATE,
    channels=CHANNELS,
    format=TYPE,
    output=True,
    frames_per_buffer=BUFFER
)



def send_data():
    try:
        while True:
            data = inp_stream.read(BUFFER)
            if data:
                main_socket.send(data)
    except Exception as e:
        print(f"ERROR: {e}")

def write_data():
    while True:
        try:
            data = main_socket.recv(4096)
            if data:
                out_stream.write(data)
        except Exception as e:
            print(f"ERROR: {e}")

        

if __name__ == "__main__":
    start_connection()
