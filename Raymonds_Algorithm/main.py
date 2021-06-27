import ast
import numpy as np
import datetime
import time as t

class Node(object):
    def __init__(self, key, counter, parent, wantCS, token=False, localque = []):
        self.key = key # namme in  dictionary
        self.counter = counter #
        self.parent = parent #parent name
        self.wantCS = wantCS # if want to reach CS
        self.localque = localque # local wait list
        self.token = token

    def sendRequest(self,nodes, CS_TIME, CS_FLAG): #sending to get in waitlist of parents
        if(self.parent != 'none'): #if not root
            if(self.key not in nodes[self.parent].localque): #if not already in wait list of parent
                nodes[self.parent].localque.append(self.key) # add this node name in parent local wait list
            print()
            print('node ', self.key, ' send token to his parent ', self.parent)
            self.printnodes(nodes,CS_TIME, CS_FLAG) #printing structure
            nodes[self.parent].sendRequest(nodes,CS_TIME,CS_FLAG) #recursion with parent node



    def printnodes(self, nodes, CS_TIME, CS_FLAG):
        for key, value in nodes.items(): # loop in all nodes to print all their info
            print()
            print("Node: ", key)
            print("-- waiting list: ", nodes[key].localque)
            print("-- parent: ", nodes[key].parent)
            print("-- token: ", nodes[key].token)
            print("-- want CS: ", nodes[key].wantCS)
            print("-- CS Time: ", CS_TIME)
            print("-- CS Flag: ", CS_FLAG)
            print()

    def sendBack(self,nodes, CS_TIME, CS_FLAG):
        self.printnodes(nodes,CS_TIME, CS_FLAG) #printing structure
        print()

        if(self.parent == 'none' and len(self.localque) ==0 and self.token == True): #if root, if no wait list and if token is set as True
            exit(0) # program is done, exit to prevent infinite loop
        if (CS_TIME != None and CS_FLAG != None):  # if node is in CS
            if (datetime.datetime.now() > CS_TIME):  # check if node reach the end of his time
                print('node ' + str(CS_FLAG) + ' went out from CS')

                tmp = CS_FLAG # save flag to temporary variable
                CS_TIME = None  # reset CS variable
                CS_FLAG = None  # reset CS variable
                self.printnodes(nodes, CS_TIME, CS_FLAG) #print all nodes
                if (len(nodes[tmp].localque) != 0): #if wait list is not empty
                    for i in nodes[tmp].localque: # loop on wait list
                        if (i not in covered_list): # if node from wait list were not already in CS
                            print('node ', tmp, ' sending token to ', i)
                            self.token = False #set token of this node
                            nodes[i].token = True #set token of node which we send request
                            nodes[i].sendBack(nodes, CS_TIME, CS_FLAG) #send request
                else: # if wait list is empty
                    if (nodes[tmp].parent != 'none'): # if node who went out from CS is not root
                        print('node ', tmp, ' sending token to ', nodes[tmp].parent)
                        self.token = False # set this node token as false
                        nodes[nodes[tmp].parent].token = True # and give token to his parent
                        nodes[nodes[tmp].parent].sendBack(nodes, CS_TIME, CS_FLAG) # send request to parent

        if(CS_FLAG == self.key): # if flag is this key (for looping)
            print('node ', self.key, ' is still in CS. Looping')
            self.printnodes(nodes)
            self.sendBack(nodes,CS_TIME,CS_FLAG) # send request to himself

        if(self.parent != 'none'): # if not root
            if(self.key in  nodes[self.parent].localque): # if node name is in local wait list of parent
                nodes[self.parent].localque.remove(self.key) # delete node name from parent wait list

        if(self.key not in covered_list): # if not covered already
            if(self.wantCS == 'yes' and CS_FLAG == None): # if want to reach CS and CS is not filled already
                    print('node ', self.key, ' want to take CS')
                    print('node ', self.key, ' is in cs')
                    CS_TIME = datetime.datetime.now() + datetime.timedelta(seconds=1)  # set CS LOCK TIME TO 4 second from now
                    CS_FLAG = self.key  # set node key as CS_Flag
                    covered_list.append(self.key) # add node name to covered list
                    t.sleep(1)
                    self.sendBack(nodes,CS_TIME,CS_FLAG) # send request

            elif(self.wantCS == 'no' and CS_FLAG == None): #if dont want to reach CS and CS is free
                print('node ',self.key, ' dont want to be in CS')
                pass

            elif(CS_FLAG != None): # if CS is taken
                print('node ', self.key , ' is still in CS. Looping')
                nodes[self.key].sendBack(nodes, CS_TIME,CS_FLAG) # loop request to himself

        if(len(self.localque) != 0): # if wait list is not empty
            print('node ', self.key, ' have waiting list:  ', self.localque)
            for i in self.localque: # loop on wait list
                if(i not in covered_list): # if not covered already
                    print('node ', self.key, ' sending token to ', i)
                    self.token = False # set this node token as false
                    nodes[i].token = True # and give token to first node from wait list
                    nodes[i].sendBack(nodes,CS_TIME,CS_FLAG) # send request to first node from wait list

        else: # if wait list is empty
            if(self.parent != 'none'): # if not root node
                print('node ', self.key, ' sending token to ', self.parent)
                self.Token = False # set token to this node as False
                nodes[self.parent].token = True # set token of parent as True
                nodes[self.parent].sendBack(nodes,CS_TIME,CS_FLAG)  # and send request to parent

#initialization
covered_list = []
CS_TIME = None
CS_FLAG = None

#initiate Nodes as key - value dictionary
# opening dictionary from txt with structure like below

# {"7":{"parent","6", "wantCS":"no"}} is same as
# {"child_node" : {"parent_node_key_name","value","child_node_key_name","value"}}

file = open('dictionary.txt','r')
contents = file.read()
Nodes_with_connections = ast.literal_eval(contents) # convert string to dictionary
file.close()

name_counter = 0 # internal counter
nodes = {} # initialize nodes dictionary
nodes_wantCS = [] #array for names of nodes who want to reach CS
root_node = None


for key, value in Nodes_with_connections.items(): # get to name corresponding number from counter
    nodes[key] = Node(key=key, counter=name_counter, parent=value['parent'], wantCS=value['wantCS'], token=False, localque=[]) #initialize nodes dictionary
    if(value['parent'] == 'none'):
        root_node = key
    if(value['wantCS'] == 'yes'):
        nodes_wantCS.append(key)
    name_counter += 1 # increment internal counter

#starting with root in CS
print('root node ', root_node ,' is in cs')
CS_TIME = datetime.datetime.now() + datetime.timedelta(seconds=1) # set CS LOCK TIME TO 4 second from now
CS_FLAG = root_node # set root as CS_Flag
nodes[root_node].token = True # set root token as true
nodes[root_node].printnodes(nodes, CS_TIME,CS_FLAG) #print structure


covered_list = [root_node] # we started with covered root

for i in nodes_wantCS:
    nodes[i].sendRequest(nodes, CS_TIME, CS_FLAG) #start sending requests from nodes willing to take CS

while(True):
    if (CS_TIME != None and CS_FLAG != None): # if node is in CS
        if (datetime.datetime.now() > CS_TIME): # check if node reach the end of his time
            print('node '+str(CS_FLAG)+' went out from CS')
            tmp = CS_FLAG # temporary set node name here
            CS_TIME = None  # reset CS variable
            CS_FLAG = None #reset CS variable
            nodes[tmp].token = True #set token of node as True (here will be root)
            nodes[tmp].sendBack(nodes,CS_TIME,CS_FLAG) # start requesting back from wait list






