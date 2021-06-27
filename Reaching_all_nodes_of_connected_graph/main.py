import ast
class Graph(object):

    # Initialize the matrix
    def __init__(self, size, NodeCovered, Verticles):

        self.VisitedNodes = NodeCovered     #   list of Visited Nodes which has been used in recursion already - to prevent infinite recursion
        self.NodeCovered = NodeCovered      #   list of Covered Nodes
        self.Verticles = Verticles

        # Create matrix
        self.adjMatrix = []
        for i in range(size):
            self.adjMatrix.append([0 for i in range(size)]) #initiate matrix
        self.size = size

    def reset(self, starting_node):
        self.VisitedNodes = [starting_node]
        self.NodeCovered = [starting_node]


    # Add edges
    def add_edge(self, v1, v2):
        if v1 == v2:
            print("Same vertex %d and %d" % (v1, v2))
        self.adjMatrix[v1][v2] = 1  #  insert 1 as edge symbol to matrix

    def __len__(self):
        return self.size

    # Print matrix rows
    def print_matrix(self):
        for row in self.adjMatrix:
            print(row)

    # Function to get key name from dictionary based on value
    def getVerticleKey(self,search_val):
        for key, value in self.Verticles.items():

            # if passed value is same as value from dictionary
            if(search_val == value):
                # return key name
                return key

        return 'no key'


    def checkNode(self, v1): # v1 = position of verticle
        # internal counter
        i = 0
        for edge in self.adjMatrix[v1]:
            # if edge symbol is not 0
            if edge != 0:
                # get name of key
                # example:
                # return value from
                #      self.getVerticleKey(0)
                # will be "A"
                verticle_key = self.getVerticleKey(i)

                #if key is not in VisitedNodes already - This if is to prevent recursion
                if verticle_key not in self.VisitedNodes:
                    #add key to Visited Nodes list
                    self.VisitedNodes.insert(len(self.VisitedNodes), verticle_key)
                    # Check child node recursion
                    self.checkNode(i)
            #check if vertical is in CoveredVerticals
                if verticle_key not in self.NodeCovered:
                    # insert key to end of NodeCovered list
                    self.NodeCovered.insert(len(self.NodeCovered),verticle_key)
            i += 1


def main():

    #initiate Nodes as key - value dictionary
    file = open('dictionary.txt','r')
    # opening dictionary from txt with structure like below

    # {"A":["C","D","E"]} is same as
    # {"node_name" : ["node_connected1","node_connected1","node_connected1"]}
    # other example dictionary to file {0:[1],1:[2],2:[0,3,5],3:[6,4],4:[6],5:[7],6:[3],7:[]}
    contents = file.read()
    Nodes_with_connections = ast.literal_eval(contents) # convert string to dictionary
    file.close()

    name_counter = 0 # internal counter
    verticles = {} # initialize verticles dictionary

    for key, value in Nodes_with_connections.items(): # get to name corresponding number from counter
        verticles[key] = name_counter # add key with value to dictionary
        name_counter += 1
        #after this for loop verticles will looks like {"A":0, "B":1} etc.

    graph_size = len(verticles)

    for key in Nodes_with_connections.keys(): # for loop in keys from dictionary
        print("starting node: " + str(key))

        NodeCovered = [key]  # define starting point by typing Verticle name
        checkVerticleNumber = verticles[key]  # define number of starting Verticle

        t1 = Graph(graph_size, NodeCovered, verticles) # create graph

        for key, value in Nodes_with_connections.items(): #for loop in dictionary keys from file
            for val in value: # for loop in values (table as a value in dictionary)
                t1.add_edge(verticles[key], verticles[val]) #here we create all connections



        t1.checkNode(checkVerticleNumber)

        if(len(t1.NodeCovered)==len(verticles)):
            print("From this node u can reach all other nodes")
        else:
            print("u Cant reach all nodes from this one")
        print("covered nodes : " + str(t1.NodeCovered))
        print()
        print()



if __name__ == '__main__':
    main()