import re
import pandas as pd
import os

GLOBAL_RESOURSE = "445759"
HORCM_INSTANCE = "I910"
VIRTUAL_VSP = "vdkc_445023"

def getListHostGroups():
    tableParser = pd.read_csv("hostGroupList.conf")
    tableParser.head()
    print(tableParser)

def getListOfPools():
    pool_file = open("pools.conf")
    for i in pool_file:
        print(i,end='')
    

def getFirstAviableLunPerPort(portId):
    my_list_of_luns = []
    aviable_list_of_luns = []
    for i in range(255):
        aviable_list_of_luns.append(i)
    cmd = "cat {} | sed 's/O_B/O B/g'> luns.csv".format(portId)
    os.system(cmd)
    tableParser = pd.read_csv("luns.csv",delimiter='\s+')
    tableParser.head()
    tableParser.shape
    tableParser
    my_list_of_luns = tableParser['LUN'].values.tolist()
    for e in range(len(my_list_of_luns)):
        aviable_list_of_luns.remove(my_list_of_luns[e])                
    return aviable_list_of_luns[0]

def getAllAviableLunPerPort(portId):
    my_list_of_luns = []
    aviable_list_of_luns = []
    for i in range(255):
        aviable_list_of_luns.append(i)
    cmd = "cat {} | sed 's/O_B/O B/g'> luns.csv".format(portId)
    os.system(cmd)
    tableParser = pd.read_csv("luns.csv",delimiter='\s+')
    tableParser.head()
    tableParser.shape
    tableParser
    my_list_of_luns = tableParser['LUN'].values.tolist()
    for e in range(len(my_list_of_luns)):
        aviable_list_of_luns.remove(my_list_of_luns[e])                
    return aviable_list_of_luns

def getCUFromList(hostGroupVar):
    my_list_of_hostsGroups = []
    tableParser = pd.read_csv("hostGroupsPorts.conf")
    tableParser.head()
    tableParser_filter = tableParser[(tableParser.hostgroup == hostGroupVar)]
    tableParser_filter.shape
    my_list_of_hostsGroups = tableParser_filter['CU'].values.tolist()
    return my_list_of_hostsGroups[0]

def getLdevFromCU(cu_number):
    my_list_of_ldev = []
    ldev_inicio = cu_number+"00"
    ldev_fin = cu_number+"FF"
    ldev_inicio = int(ldev_inicio,16)
    ldev_fin = int (ldev_fin,16)
    print("raidcom get ldev -ldev_id {}-{} -s {} -{} -fx  | grep ""LDEV : "" | grep -v VIR_LDEV".format(ldev_inicio,ldev_fin,GLOBAL_RESOURSE,HORCM_INSTANCE))
    ldev_file = open("ldevList.tmp")
    for i in ldev_file:
        my_list_of_ldev.append(i.split(" ")[-1].replace("\n","")[-2:])
    return my_list_of_ldev

def getFirstLdevFromCU(cu_number):
    my_list_of_ldev = []
    ldev_inicio = cu_number+"00"
    ldev_fin = cu_number+"FF"
    ldev_inicio = int(ldev_inicio,16)
    ldev_fin = int (ldev_fin,16)
    print("raidcom get ldev -ldev_id {}-{} -s {} -{} -fx  | grep ""LDEV : "" | grep -v VIR_LDEV".format(ldev_inicio,ldev_fin,GLOBAL_RESOURSE,HORCM_INSTANCE))
    ldev_file = open("ldevList.tmp")
    for i in ldev_file:
        my_list_of_ldev.append(i.split(" ")[-1].replace("\n","")[-2:])
    return my_list_of_ldev[0]

def getListOfHostGroupsPorts(hostGroupVar):
    my_list_of_hostsGroups = []
    tableParser = pd.read_csv("hostGroupsPorts.conf")
    tableParser.head()
    tableParser_filter = tableParser[(tableParser.hostgroup == hostGroupVar)]
    tableParser_filter.shape
    my_list_of_hostsGroups = tableParser_filter['port'].values.tolist()
    return my_list_of_hostsGroups

def getFirstOfHostGroupsPorts(hostGroupVar):
    my_list_of_hostsGroups = []
    tableParser = pd.read_csv("hostGroupsPorts.conf")
    tableParser.head()
    tableParser_filter = tableParser[(tableParser.hostgroup == hostGroupVar)]
    tableParser_filter.shape
    my_list_of_hostsGroups = tableParser_filter['port'].values.tolist()
    return my_list_of_hostsGroups[0]

def getCuFromConfFile(hostGroupVar):
    my_list_of_hostsGroups = []
    tableParser = pd.read_csv("hostGroupsPorts.conf")
    tableParser.head()
    tableParser_filter = tableParser[(tableParser.hostgroup == hostGroupVar)]
    tableParser_filter.shape
    my_list_of_hostsGroups = tableParser_filter['CU'].values.tolist()
    return my_list_of_hostsGroups[0]

def executeVolumeCreate(ldevId,ldevNumber,capacity,pool):
    print("raidcom add ldev -ldev_id {}:{} -capacity {}g -pool {} -s {} -{}".format(ldevId,ldevNumber,capacity,pool,GLOBAL_RESOURSE,HORCM_INSTANCE))

def executeModifyLdev(ldevId,ldevNumber,ldevName):
    print("raidcom modify ldev -ldev_id {}:{} -ldev_name {} -s {} -{}".format(ldevId,ldevNumber,ldevName,GLOBAL_RESOURSE,HORCM_INSTANCE))

def executeUnmapResource(ldevId,ldevNumber):
    print("raidcom unmap resource -ldev_id {}:{} -virtual_ldev_id {}:{} -s {} -{}".format(ldevId,ldevNumber,ldevId,ldevNumber,GLOBAL_RESOURSE,HORCM_INSTANCE))

def executeAddResource(ldevId,ldevNumber):
    print("raidcom add resource -resource_name {} -ldev_id {}:{} -s {} -{}".format(VIRTUAL_VSP,ldevId,ldevNumber,GLOBAL_RESOURSE,HORCM_INSTANCE))

def executeMapResource(ldevId,ldevNumber):
    print("raidcom map resource -ldev_id {}:{} -virtual_ldev_id {}:{} -s {} -{}".format(ldevId,ldevNumber,ldevId,ldevNumber,GLOBAL_RESOURSE,HORCM_INSTANCE))

def executeAddLun(portId,ldevId,ldevNumber,lun_id):
    print("raidcom add lun -port {} -ldev_id {}:{} -lun_id {} -s {} -{}".format(portId,ldevId,ldevNumber,lun_id,GLOBAL_RESOURSE,HORCM_INSTANCE))
    

#if __name__ == '__main__':
    #print(getListOfHostGroupsPorts("BDD_ENTERPRICE"))
    #getListHostGroups()
    #print(getAviableLunPerPort("prueba.csv"))
    #print(getLdevFromCU(getCUFromList("BDD_ENTERPRICE")))
    #executeVolumeCreate("04","f9",1024,0)
    #executeModifyLdev("04","f9","prueba")
    #executeUnmapResource("04","f9")
    #executeAddResource("04","f9")
    #executeMapResource("04","f9")
    #executeAddLun("CL1-B-5","04","f9",100)
    #getListOfPools()