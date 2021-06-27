import ast
import json

import numpy as np
import datetime
import time as t
import random



def findDeadLock(output, covered,  first = None, prev = None):
    #initialization of waiting list
    wait_list = []
    #if previous is not set yet or if previous number was 1
    if(prev == None or prev[2] == 1):
        #if previous is not set, set empty array
        if(prev == None):
            prev = []
        #if first process is not picked yet
        if(first == None):
            #iterate in output directory
            for resource, processes in output.items():
                for process, value in processes.items():
                    #if value of process is 1 and first was not set yet
                    if(value == 1 and first == None):
                        print('first process ', process,' with resourse ', resource , ' locked')
                        print()
                        #set resource and process to first variable, then add process to covered list
                        first = [resource, process]
                        covered.append(process)

        if prev == []:
            #iterate in output directory with resource key
            for key, value in output[first[0]].items():
                #find all -1 in row
                if value == -1:
                    print('found other process ( ' +key+ ' ) who wants resource ', first[0])
                    #add to waitlist
                    wait_list.append([None,key, value])

        # if previous variable was set before
        else:
            #iterate in output directory with resource key from prevouis iteration
            for key, value in output[prev[0]].items():
                #find all -1 in row
                if value == -1:
                    print('found other process ( ' + key + ' ) who wants resource ', prev[0])
                    # add to waitlist
                    wait_list.append([prev[0], key,value])
                    #deadlock detection
                    if(key in covered):
                        print('deadlock found')
                        print('first process ', first[1])
                        print('first resource ', first[0])
                        print('processes causing deadlock: ',  prev[1] , ' and ', key)
                        exit()
        print()
        for i in wait_list:
            #add item from wait list to covered list
            covered.append(i[1])
            print('looking for other resources for process ', i[1])
            print()
            #recursion
            findDeadLock(output, covered, first, i)
    else: #if previous was set or previous process value was not 1
        # iterate in output directory
        for resource, processes in output.items():
            for process, value in processes.items():

                # if process key is same as previous process key
                if(process == prev[1]):
                    # if its value is 1
                    if(value == 1):
                        print('found process ( '+process+' ) with locked resource ' ,resource)
                        print()
                        covered.append(process)
                        #recursion
                        findDeadLock(output,covered,first,[resource, process, value])

class site(object):
    def __init__(self, key):
        self.key = key
        self.loc_processes = [] #local processes
        self.loc_resourcess = [] #local resources

    def printAll(self,sites):
        for key, value in sites.items():
            if(value.loc_resourcess != None):
                print(key, ':',"loc_res: ", value.loc_resourcess)
                print("---- loc_proc: ", value.loc_processes)
            else:
                print(key, ':',"loc_res: ", value.loc_resourcess)
                print("---- loc_proc: ", value.loc_processes)

class process(object):
    def __init__(self, key, resource_key = None, is_blocked = 'no'):
        self.key = key
        self.working_with = resource_key
        self.is_blocked = is_blocked
        self.waitlist = []

    def printAll(self,processes):
        for key, value in processes.items():

            if(value.working_with != None):
                print(key, ':',"working_with: ", value.working_with.key, ' ----- wait list: ', value.waitlist)
            else:
                print(key, ':',"working_with: ", 'none', ' ----- wait list: ', value.waitlist)

class resource(object):
    def __init__(self, key, is_blocked = 'no'):
        self.key = key
        self.is_blocked = 'no'

    def printAll(self,resourcess):
        for key, value in resourcess.items():
            print(key, ':', "is_blocked: ", value.is_blocked)

###################Initialization
sites = {}
sites_names = []

resources = {}
resources_names = []
resources_covered = []

processes = {}
processes_names = []


site_count = 3
data_count = 3 # resources/processes per site

###################

#generate sites
for i in range(site_count):
    key = 's'+str(i)
    sites[key] = site(key) #set site to directory
    sites_names.append(key)

#generate resources
for rs in range(site_count*data_count):
    key = 'r'+str(rs)
    resources[key] = resource(key) #set resource to directory
    resources_names.append(key)

    sites['s'+str(int(rs/3))].loc_resourcess.append(resource(key).key) #set resources to sites

#generate processes
for pro in range(site_count*data_count):
    key = 'p'+str(pro)
    random_resource = resources[random.choice(resources_names)] #random pick from created resources
    if(random_resource.key not in resources_covered and (random.random() > 0.5)): #if not covered already and if random value is greater than 0.5 to cause more unset resources
        random_resource.is_blocked = 'yes'  # set resource status
        processes[key] = process(key, random_resource) # set process with its resource to directory
        processes_names.append(key)
        resources_covered.append(random_resource.key) #set resource as covered
    else:
        processes[key] = process(key) # set process without resource
        processes_names.append(key)

    sites['s'+str(int(pro/3))].loc_processes.append(processes[key].key) #set processes to sites


for key,value in processes.items():
    #how much resources we want to assign to this process
    for x in range(random.randint(0, len(resources))):
        # get random recource key
        wait_resource = resources[random.choice(resources_names)].key
        #if resource is not in waitlist already and process is not working with him already
        if(wait_resource not in processes[key].waitlist and processes[key].working_with != resources[wait_resource].key):
            processes[key].waitlist.append(wait_resource) #add resource to waitlist of process
            if ((processes[key].working_with == None)): #if process dont work with any resource
                if(resources[wait_resource].is_blocked == 'no'): # if resource is not blocked by other processes
                    resources[wait_resource].is_blocked = 'yes' #set resource to blocked
                    processes[key].working_with = resources[wait_resource] # and set this resource to work with process

output = {} #output directory
for key, value in resources.items():
    output[value.key] = {} #create new directory for processes for this resource
    for key2, value2 in processes.items():
        #set 0 as default
        output[value.key][value2.key] = 0
        if(value2.working_with == value): # if process is working with this resource set 1
            output[value.key][value2.key] = 1
        elif(value.key in value2.waitlist): # if process have this resource in waiting list set -1
            output[value.key][value2.key] = -1

#print whole directory
for x in output:
    print (x, output[x])
    print()

#start finding deadlock
findDeadLock(output, covered=[])




