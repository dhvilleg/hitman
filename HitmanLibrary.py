import re
import pandas as pd
import os

GLOBAL_RESOURSE = "445759"
HORCM_INSTANCE = "I910"
VIRTUAL_VSP = ""

def getListHostGroups():
    tableParser = pd.read_csv("hostGroupList.conf")
    tableParser.head()
    print(tableParser)

def getAviableLunPerPort(portId):
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
    ldev_inicio = cu_number+"00"
    ldev_fin = cu_number+"FF"
    ldev_inicio = int(ldev_inicio,16)
    ldev_fin = int (ldev_fin,16)
    print("raidcom get ldev -ldev_id {}-{} -s {} -{} -fx  | grep ""LDEV : "" | grep -v VIR_LDEV".format(ldev_inicio,ldev_fin,GLOBAL_RESOURSE,HORCM_INSTANCE))
    
    
    

def getListOfHostGroupsPorts(hostGroupVar):
    my_list_of_hostsGroups = []
    tableParser = pd.read_csv("hostGroupsPorts.conf")
    tableParser.head()
    tableParser_filter = tableParser[(tableParser.hostgroup == hostGroupVar)]
    tableParser_filter.shape
    my_list_of_hostsGroups = tableParser_filter['port'].values.tolist()
    return my_list_of_hostsGroups
    

if __name__ == '__main__':
    #print(getListOfHostGroupsPorts("BDD_ENTERPRICE"))
    #getListHostGroups()
    #getAviableLunPerPort("prueba.csv")
    getLdevFromCU(getCUFromList("BDD_ENTERPRICE"))