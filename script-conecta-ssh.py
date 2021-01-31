# -*- coding: utf-8 -*-
from netmiko import ConnectHandler                                                                                                         
import time, datetime

#crie um arquivo com os endereços ip  em varias linhas, é possivel tbm usar dictionary.
enderecos = open('ipaddress.txt')

for ip in enderecos:
	cisco = { 
   		'device_type': 'cisco_ios', 
   		'host': ip, 
   		'username': 'admin', 
   		'password': 'senha',
   		'port': 22, 
   		}  
	net_connect = ConnectHandler(**cisco)
	#output = net_connect.send_command("show running-config")
	configshow = net_connect.send_command("show running-config")
	net_connect.disconnect()
	print(configshow)
	save_config = open('backup-{}'.format(ip.strip())+'.txt', '+w')
	save_config.write(configshow)
	save_config.close()




