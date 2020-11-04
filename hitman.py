#!/usr/local/bin/python3.6
import click
import time
from HitmanLibrary import getListHostGroups,getListOfHostGroupsPorts,getLdevFromCU,getCUFromList,getAllAviableLunPerPort,getFirstOfHostGroupsPorts
from HitmanLibrary import getCuFromConfFile,getFirstLdevFromCU,getFirstAviableLunPerPort,getListOfPools
from HitmanLibrary import executeVolumeCreate,executeModifyLdev,executeUnmapResource,executeAddResource,executeMapResource,executeAddLun
 

@click.group()
def cli():
    pass

@click.command()
@click.option('--hostgroups', is_flag=True, help="Print list of HostGroups names.")
@click.option('--pools', is_flag=True, help="Print list of pools id and names.")
@click.option('--porthost', default='', help='Print ports form hostGroup or cluster - required - HostGroup name')
@click.option('--aviable_ldev',default='',help='Print aviables ldevs per hostGroup - required - HostGroup name')
@click.option('--aviable_lun',default='',help='Print aviables luns per hostGroup - required - HostGroup name')
def get(hostgroups,pools,porthost,aviable_ldev,aviable_lun):
    if hostgroups:
        getListHostGroups()
    if pools:
        getListOfPools()
    if porthost:
        count = 1
        for i in getListOfHostGroupsPorts(porthost):
            click.echo("{}.-\t{}".format(count,i))
            count = count+1
    if aviable_ldev:
        count = 1
        for i in getLdevFromCU(getCUFromList(aviable_ldev)):
            click.echo("{}.-\t{}".format(count,i))
            count = count+1
    if aviable_lun:
        count = 1
        for i in getAllAviableLunPerPort(getFirstOfHostGroupsPorts(aviable_lun)):
            click.echo("{}.-\t{}".format(count,i))
            count = count+1

@click.command()
@click.option('--volume_name',default='',required=True,help='set volume name according to standard')
@click.option('--volume_size',default='',required=True,type=int,help='set volume size in GB')
@click.option('--hostgroup_name',default='',required=True,help='set hotgroup name from list')
@click.option('--pool_id',default='',required=True,help='set pool id name from list')
def add(volume_name,volume_size,hostgroup_name,pool_id):
    if volume_name and volume_size and hostgroup_name and pool_id:
        #click.echo("volume name es {}, volume size es {}, hostgroup es {}, pool es {}".format(volume_name,volume_size,hostgroup_name,pool_id))
        if int(pool_id) >= 0 and int(pool_id) <=10:
            cu_from_conf_file = getCuFromConfFile(hostgroup_name)
            first_ldevfromCU = getFirstLdevFromCU(cu_from_conf_file)
            first_hostgroup_port = getFirstOfHostGroupsPorts(hostgroup_name)
            lun_id_aviable = getFirstAviableLunPerPort(first_hostgroup_port)
            all_hostgroup_ports = getListOfHostGroupsPorts(hostgroup_name)
            executeVolumeCreate(cu_from_conf_file,first_ldevfromCU,volume_size,pool_id)
            executeModifyLdev(cu_from_conf_file,first_ldevfromCU,volume_name)
            executeUnmapResource(cu_from_conf_file,first_ldevfromCU)
            executeAddResource(cu_from_conf_file,first_ldevfromCU)
            executeMapResource(cu_from_conf_file,first_ldevfromCU)
            for port_id in all_hostgroup_ports:
                executeAddLun(port_id,cu_from_conf_file,first_ldevfromCU,lun_id_aviable)
                time.sleep(1)
        else:

            click.echo("ERROR\nPool_id are not in a correct format, enter a valid pool_id")
    else:
        click.echo("ERROR\nYou must to enter all options acording to command format\n\nEXAMPLE\nhitman add --volume_name prueba --volume_size 100 --hostgroup_name BDD_ENTERPRICE --pool_id 0")

@click.command()
def about():
    click.echo("ABOUT HITMAN\nhitman is a little CLI program that helps you simplify to create volumes with raidcom\n\nhitman 0.1 was developed by Diego Villegas @ TCS")

cli.add_command(get)       
cli.add_command(add)
cli.add_command(about)

if __name__ == '__main__':
    cli()