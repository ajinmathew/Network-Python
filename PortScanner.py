import socket
import threading
import pyfiglet
import time
from queue import Queue

class PortScanner:
    def __init__(self,target):
        self.target=target
        self.queue=Queue()
        self.open_ports = []
    #Function to check connection is successful or not...
    def portscanner(self,port):
        try:
            #defining IPv4 and TCP...
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((self.target,port))
            return True
        except:
            return False
    #accepting port number from Queue and send to scanning...
    def worker(self):
        while not self.queue.empty():
            port=self.queue.get()
            if self.portscanner(port):
                print("[->] Port {} is open".format(port))
                self.open_ports.append(port)

def main():
    
    banner=pyfiglet.figlet_format("Port Scanner")
    print(banner)
    target = str(input("Enter the Host to Scan : "))
    portScanner=PortScanner(target)
    print("Select the mode of scanning..")
    print("1. 1-500 Ports\n2. 1-1000 Ports\n3. All Ports\n4. User Specified Ports")
    choice=input("Enter your choice : ")
    if choice=="1":
        for i in range(1,500):
            portScanner.queue.put(i) 
    elif choice=="2":
        for i in range(1,1000):
            portScanner.queue.put(i)   
    elif choice=="3":
        for i in range(1,65535):
            portScanner.queue.put(i)  
    elif choice=="4":
        inp_port_list = input("Enter ports separated by comma : ")
        port_list=inp_port_list.split(",")
        for i in port_list:
            portScanner.queue.put(int(i))
    else:
        print("Invalid Input...")
    #calculating time...
    startTime=time.time()        
    #creating threads...
    portScanner.thread_list=[]
    for t in range(100):
        thread=threading.Thread(target=portScanner.worker)
        portScanner.thread_list.append(thread)
    for thread in portScanner.thread_list:
        thread.start()
    for thread in portScanner.thread_list:
        thread.join()    
    print("Open ports are,",portScanner.open_ports) 
    endTime=time.time()
    print(f"Scanned in {endTime - startTime}s")


if __name__ == '__main__':
	main()    



