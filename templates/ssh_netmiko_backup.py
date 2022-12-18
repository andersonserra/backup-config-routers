#!/usr/bin/python3

from netmiko import ConnectHandler
import time
import datetime
import logging

usuario = 'admin'
senha = 'password'


timestamp =  datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#Diretorio de Backup
BackupDir='/root/scripts/backup_ativos/dados'
#Data que sera concatenada no nome do arquivo log: backup.YYYYMMDD.log , um arquivo log por dia
LogData=datetime.datetime.now().strftime("%Y%m%d")
Log = BackupDir + "/logs/backup." + LogData + ".log"
#Configuracao basica do logging, o nivel de logging vai ser INFO, caso seja preciso mais informacao podemos colocar DEBUG
logging.basicConfig(filename=Log,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

#Inicio do Script, escrevo no arquivo log
logging.info('Inicio')
logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H%M%S"))

#Definicao dos nossos roteadores
radio_parua_01 =    { 'device_type': 'mikrotik_routeros', 'ip': '172.16.1.8', 'host':   'radio_parua_01', 'username': usuario, 'password': senha, 'port' : 2222, 'timeout': 10 }
roteador_ccr_1009 =    { 'device_type': 'mikrotik_routeros', 'ip': '172.16.1.1', 'host':   'roteador_ccr_1009', 'username': usuario, 'password': senha, 'port' : 2222, 'timeout': 10 }
roteador_ccr_1036 =    { 'device_type': 'mikrotik_routeros', 'ip': '172.16.5.2', 'host':   'roteador_ccr_1036', 'username': usuario, 'password': senha, 'port' : 2222, 'timeout': 10 }
systemnet_ptp_picodosol_ap =    { 'device_type': 'mikrotik_routeros', 'ip': '172.16.8.2', 'host':   'systemnet-ptp-picodosol-ap', 'username': usuario, 'password': senha, 'port' : 2222, 'timeout': 10 }
systemnet_painel_centro_02 =    { 'device_type': 'mikrotik_routeros', 'ip': '172.16.1.14', 'host':   'systemnet_painel_centro_02', 'username': usuario, 'password': senha, 'port' : 2222, 'timeout': 10 }


#Lista com os nossos roteadores
equipamentos=[radio_parua_01, roteador_ccr_1009, roteador_ccr_1036, systemnet_ptp_picodosol_ap,systemnet_painel_centro_02]

#Laco para executar o comando sh run roteador por roteador
for device in equipamentos:
 try:
  #Abrindo uma conexao SSH
  net_connect=ConnectHandler(**device)
  #Trocando para enable
  net_connect.enable()
  #Executando o comando sh run
  output=net_connect.send_command('/export terse')
  #Nome do arquivo de backup no formato hostname.YYYY-MM-DD-HH:MM:SS
  BackupNameOfFile=BackupDir + "/" + timestamp + "_" + device['host']
  #Escrevendo no arquivo a saida do comando sh run
  with open(BackupNameOfFile,'w') as fh:
   fh.write(output)
  #Saindo do enable
  net_connect.exit_enable_mode()
  #Fechando a sessao SSH
  net_connect.disconnect()
 except:
  logging.info("Erro de conexao ao roteador %s" % device['ip'])





#Escrevendo lo log a palavra Fim e colocando a hora que finalizou
logging.info('Fim')
logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H%M%S"))
