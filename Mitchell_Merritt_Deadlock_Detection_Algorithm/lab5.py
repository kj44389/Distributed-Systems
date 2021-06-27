import datetime
import threading
import time
import numpy as np
import random

deadlock = 'false' # global deadlock variable


class MyThread(threading.Thread):
    def __init__(self, threadID, name, counter, publickey, privatekey,  flag = 'transmit'):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threads = {}
        self.name = name
        self.counter = counter
        self.next = []
        self.nextPointer = [] # pointer to thread objects
        self.initNodesCounter = 0 # how much next nodes assigned to this node before any operations
        self.publickey = publickey
        self.privatekey = privatekey
        self.flag = flag

    def startprint(self):
        print("Node " + self.name)
        print("next " + str(self.next))
        print("public key " + str(self.publickey))
        print("private key " + str(self.privatekey))
        print()

    def printState(self):
        print("Node " + self.name)
        print("next " + str(self.next))
        print("public key " + str(self.publickey))
        print("private key " + str(self.privatekey))
        print()

    def run(self):
        while((datetime.datetime.now() < (datetime.datetime.now() + datetime.timedelta(seconds=1)))): # run thread for 1 second

            if(globals()['deadlock'] == 'true'): #if deadlock is detected
                print('closing node ', self.name)
                print()
                break #go out from while => end thread

            if (self.initNodesCounter < len(self.next) and self.flag != 'block'): # if number of next nodes rised ( this happens when edge is added)
                print('changing flag for node ', self.name, " to block")
                self.flag = 'block'

            for key, value in self.threads.items(): # for in all threads
                for n in self.next: # for in all next nodes
                    if(value.name == n): # if thread name is same as name in next array

                        if(self.privatekey == value.publickey): #deadlock detection
                            print('deadlock detected between nodes: ', self.name , ' and ', value.name)
                            globals()['deadlock'] = 'true'

                        else: # if deadlock not detected

                            if(self.publickey <= value.publickey and self.flag == 'transmit'): # if public key is lower than next node public key and if this node is not blocked
                                self.publickey = value.publickey # set this node public key as next node publickey

                            elif(self.publickey <= value.publickey and self.flag == 'block'): # if public key is lower than next node public key and if node is blocked
                                self.publickey = value.publickey+1 # set public key and private key as publickey from next node
                                self.privatekey = value.publickey+1
                                self.flag = 'transmit'
                                print('changing flag for node ', self.name, " to transmit")
                                self.initNodesCounter = len(self.next) # set new number of next nodes (update number of edges)


if __name__ == '__main__':

    #INITIALIZATION
    # Nodes = {'node_key' : {'edges':['node_key'], 'public_key': number, 'private_key': number}}
    Nodes = {
                "a":{'next':["b"], 'public':13, 'private':11},
                "b":{'next':["c"], 'public':7, 'private':4},
                'c':{'next':['d'], 'public':6, 'private':5 },
                'd':{'next':[], 'public':3, 'private':6}
             }
    # Add_node = {'new_node_key' : {'edges':['node_key'], 'public_key': number, 'private_key': number}}
    Add_node = {
                'e':{'next':[], 'public':19, 'private':6}
    }
    # Add_edge = {'first_node_key' : 'next_node_key_to_create_edge}
    Add_edge = {
                'c':'e',
                'e':'a'
    }
    threads = {}

    for key, value in Nodes.items(): #creating threads


        threads[key]= MyThread(len(threads), name=key, counter=len(threads), publickey= value['public'], privatekey=value['private']) #set thread to dictionary

        threads_counter = len(threads)-1 #get number of threads
        for i in value['next']: #for in all edges
            if(len(threads)>0): # if no threads
                threads[key].next.append(i) #add edge node name to object variable
        threads[key].initNodesCounter = len(threads[key].next) #update number of assigned edges

    for key, value in Add_node.items(): #adding nodes from Add_node directory
        threads[key] = MyThread(len(threads), name=key, counter=len(threads), publickey=value['public'], privatekey=value['private'])  #set thread to dictionary

    for key,value in Add_edge.items(): #adding edges from add_edge directory
        threads[key].next.append(threads[value].name)  #add edge to node object

    # Start new Threads
    for key in threads.keys():
        threads[key].threads = threads # assign all threads to object
        threads[key].start()

    while True:
        if(globals()['deadlock'] == 'true'): #if deadlock is detected
            time.sleep(2)
            for key in threads.keys(): #print all threads info
                threads[key].printState()
            exit()


