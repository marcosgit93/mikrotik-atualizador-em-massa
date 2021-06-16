# -*- coding: utf-8 -*-
import routeros_api
import paramiko
from paramiko import SSHClient
from scp import SCPClient
############################################################################
################ DESENVOLVIDO POR VINICIUS #################################
############################################################################
contador=0
contador_Arm=0
contador_Title=0
contador_Mipsbe=0
contador_x86=0
mk_username = 'usuario'
mk_password = 'senha'
mk_version='6.48.2'
ssh_port = '9996'
destination_volume = '\\'
def ssh_scp_files(ssh_host, mk_username, mk_password, ssh_port, source_volume, destination_volume):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_host, username=mk_username, password=mk_password,port=ssh_port, look_for_keys=False)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(source_volume, recursive=True, remote_path=destination_volume)
file = open("lojas.txt", "r")
for x in file:
    try:
            ssh_host = str(x.replace('\n',''))
            connection = routeros_api.RouterOsApiPool(ssh_host, username=mk_username, password=mk_password,port=9995,plaintext_login=True)
            api = connection.get_api()
            checksun = api.get_resource('/').call('system/resource/print')
            print("**********************************************")
            print(x)
            versao=(checksun[0]['version'])
            arquitetura=("Arquitetura: "+checksun[0]['architecture-name'])
            print("**********************************************")
            if "arm" in str(arquitetura):
                contador_Arm += 1
                if str(mk_version) not in str(versao):
                    checkfile = api.get_resource('/').call('file/print')
                    if "routeros-arm-"+str(mk_version)+'.npk' not in str(checkfile):
                        source_volume = r'E:\mikrotik\routeros-arm-'+str(mk_version)+'.npk'
                        ssh_scp_files(ssh_host, mk_username, mk_password, ssh_port, source_volume, destination_volume)
            if "tile" in str(arquitetura):
                contador_Title += 1
                if str(mk_version) not in str(versao):
                    pass
            if "mipsbe" in str(arquitetura):
                contador_Mipsbe += 1
                if str(mk_version) not in str(versao):
                    checkfile = api.get_resource('/').call('file/print')
                    if "routeros-mipsbe-"+str(mk_version)+'.npk' not in str(checkfile):
                        source_volume = r'E:\mikrotik\routeros-mipsbe-'+str(mk_version)+'.npk'
                        ssh_scp_files(ssh_host, mk_username, mk_password, ssh_port, source_volume, destination_volume)
            if "x86" in str(arquitetura):
                contador_x86 += 1
                if str(mk_version) not in str(versao):
                    checkfile = api.get_resource('/').call('file/print')
                    if "routeros-x86-"+str(mk_version)+'.npk' not in str(checkfile):
                        source_volume = r'E:\mikrotik\routeros-x86-'+mk_version+'.npk'
                        ssh_scp_files(ssh_host, mk_username, mk_password, ssh_port, source_volume, destination_volume)
    except Exception as e:
        print(e)
        print("ERROR NO IP: "+x)
print("Quantidade Arm:    " + str(contador_Arm))
print("Quantidade Title:  " + str(contador_Title))
print("Quantidade Mipsbe: " + str(contador_Mipsbe))
print("Quantidade X86: " + str(contador_x86))
