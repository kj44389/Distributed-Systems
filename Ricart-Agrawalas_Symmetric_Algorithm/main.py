import ast
import numpy as np
import datetime
import time as t







class Node(object):
    def __init__(self, key,  counter, time_stamp, nodes, wantCS , requesting_nodes = {}):

        self.key = key # namme in  dictionary
        self.counter = counter #
        self.time_stamp = time_stamp
        self.wantCS = wantCS # if node want to reach CS
        self.nodes_status = np.zeros(shape= len(nodes)) # array with [0,1] status for each node (based on nodes dictionary below)
        self.nodes = nodes # array with all nodes keys
        self.requesting_nodes = requesting_nodes # dictionary with requesting nodes

    def sendRequest(self,nodes,covered_list, CS_TIME, CS_FLAG):
        i = 0 # internal counter

        ####################### Loop in other nodes ( sending requests )
        if(self.key not in covered_list): # if key of launching sendRequest object were not in CS already
            print('Launching requests from node ', self.key)

        for node in self.nodes:
            if (self.key not in covered_list): # if key of launching sendRequest object were not in CS already

                if (nodes[node].wantCS == 'no'): # if object dont want to reach CS just set its status as 1
                    self.nodes_status[i] = 1
                    print("node " + self.key + " get response from: ", nodes[node].key, ' with status ', self.nodes_status[i])

                else: # if object (node) want to reach CS
                    if(nodes[node].key not in covered_list): # if was not already in CS
                        if (self.time_stamp < nodes[node].time_stamp): # if node timestamp is lower than requesting ones
                            self.nodes_status[i] = 1 # just set 1 to its status
                            print("node " + self.key + " get response from: ", nodes[node].key , ' with status ',
                                    self.nodes_status[i])
                            if(nodes[node].key not in self.requesting_nodes): # this if is to add node to requesting nodes dictionary if was not here. (its used when some node is in CS already)
                                self.requesting_nodes[nodes[node].key] = nodes[node].time_stamp # adding as this ["node_key":time stamp value] to dictionary | nodes[node].time_stamp is to get timestamp value of node
                        else: # if this node value is greater than requesting ones
                            if (self.key not in nodes[node].requesting_nodes): # if node timestamp is lower than requesting ones
                                nodes[node].requesting_nodes[nodes[node].key] = nodes[node].time_stamp # add this node to requesting list of different node
                            print("node ", self.key, ' with timestamp: ', self.time_stamp, 'lost vs node ',
                                      nodes[node].key, ' with timestamp ', nodes[node].time_stamp)
                            print('swaping nodes')
                            print()

                            CS_TIME, CS_FLAG = nodes[node].sendRequest(nodes,covered_list, CS_TIME, CS_FLAG) # recursion, sending node with lower timestamp
                    else:
                        self.nodes_status[i] = 1 # if node is covered set 1
                    print("node " + self.key + " get response from: ", nodes[node].key, ' with status ', self.nodes_status[i])
                i += 1 # increment internal counter

                if(np.sum(self.nodes_status) == 4): # if status of all nodes are 1 (in this example we have 5 nodes. 4 when excluded this node.
                    if(CS_FLAG == None and CS_TIME == None): # if CS_FLAG and CS_TIME is not set
                        print()
                        print("node " + self.key + " is in CS")
                        print("node " + self.key + " get response from: ", self.nodes , ' with status ', self.nodes_status)
                        CS_TIME = datetime.datetime.now() + datetime.timedelta(seconds=1) # set CS LOCK TIME TO 1 second from now
                        CS_FLAG = self.key # set key as CS_Flag
                        covered_list.append(CS_FLAG) # add key name to covered list array
                        print()

        return CS_TIME, CS_FLAG # return were needed to work on Global variables - CS_TIME and CS_FLAG

#initialization

covered_list = []
CS_TIME = None
CS_FLAG = None

#initiate Nodes as key - value dictionary
# opening dictionary from txt with structure like below

# {"A":{"wantCS","yes", "timestamp":1}} is same as
# {"node_name" : {"child_node_key_name","value","child_node_key_name","value"}}

file = open('dictionary.txt','r')
contents = file.read()
Nodes_with_connections = ast.literal_eval(contents) # convert string to dictionary
file.close()

name_counter = 0 # internal counter
nodes = {} # initialize nodes dictionary
nodes_with_cs_requests = [] # initialize list of nodes who are willing to reach CS
generic = 0 # if we want to random timestamp values (0 - no and we need to give timestamp values in txt files) (1 - yes its will be random)

for key, value in Nodes_with_connections.items(): # get to name corresponding number from counter

    if(generic == 1):
        random_value = np.random.rand()
        nodes[key] = Node(key=key, counter=name_counter, time_stamp=random_value, wantCS=value['wantCS'], nodes=Nodes_with_connections.keys() - key)
    else:
        nodes[key] = Node(key = key, counter=name_counter, time_stamp= value['value'], wantCS=value['wantCS'], nodes=Nodes_with_connections.keys()-key)


    if(nodes[key].wantCS == "yes"): # if node is willing to reach CS
        nodes_with_cs_requests.append(key) # add its name to array
    name_counter += 1 # increment internal counter


while(len(covered_list) != len(nodes_with_cs_requests)): # finite loop (will end if all nodes will reach CS)
    t.sleep(1) # to prevent to many request while in CS
    if (CS_TIME != None and CS_FLAG != None): # if node is in CS
        if (datetime.datetime.now() > CS_TIME): # check if node reach the end of his time
            print('node '+CS_FLAG+' went out from CS')
            print('covered nodes list ', covered_list)
            lowest_timestamp = ['key', 0] # init array

            if(len(nodes[CS_FLAG].requesting_nodes.keys()) != 0): #if node who were in CS have requesting nodes
                print("nodes who are on request list", list(nodes[CS_FLAG].requesting_nodes.keys()))
                for key, value in nodes[CS_FLAG].requesting_nodes.items(): # loop for requesting nodes of this node.
                    if(key not in covered_list): #if requesting node were in CS already (in covered list)

                        if(lowest_timestamp[0] == 'key' and lowest_timestamp[1]==0): # if lowest_timestamp array is empty
                            lowest_timestamp[0] = key
                            lowest_timestamp[1] = value
                        else: # if its been already changed
                            if(value < lowest_timestamp[1]): # check if current timestamp value is lower than timestamp from array
                                print('node ', key ,' have lower timestamp (',value,') than node ',lowest_timestamp[0],' with timestamp (',lowest_timestamp[1],')')
                                print('swaping nodes')
                                lowest_timestamp[0] = key # change key
                                lowest_timestamp[1] = value # change value
            CS_TIME = None #reset CS variable
            CS_FLAG = None #reset CS variable
            if(lowest_timestamp[0] != 'key' and lowest_timestamp[1] != 0): # if there is any requesting node ( with lowest timestamp - because its changed above to pick the lowest)
                CS_TIME , CS_FLAG = nodes[lowest_timestamp[0]].sendRequest(nodes, covered_list, CS_TIME, CS_FLAG) # launch requesting node with lowest timestamp


    for key in nodes: # we just get keys of all nodes here in loop
        if(nodes[key].wantCS == 'yes'): # if this node is willing to reach CS
            if(key not in covered_list): # if its were not in CS already
                # print('Launching requests from node ', key)
                CS_TIME, CS_FLAG = nodes[key].sendRequest(nodes, covered_list=covered_list, CS_TIME = CS_TIME, CS_FLAG= CS_FLAG) #launch sending requests from this node


print('covered nodes list ' ,covered_list, ' , nodes who wanted to go to CS ' ,nodes_with_cs_requests)