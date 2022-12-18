#!/usr/bin/python3

import sys
import telnetlib
import time
import datetime


user = 'admin'
password = 'password'

timestamp =  datetime.datetime.now().strftime("%Y%m%d%H%M%S")



#open the file that contains the devices IP address
file = open("/root/scripts/backup_ativos/telnet_devices")

def show_run():
  tel.read_until(b">")
  tel.write(b"enable\n")
  tel.write(b"show running-config\n")
  tel.read_until(b"--More--")
  tel.write(b"                                                                                                                      ")
  tel.write(b"exit\n")
  readoutput = tel.read_until(b">", timeout=5)
  saveoutput = open("/root/scripts/backup_ativos/dados/" + timestamp + "_running_config_" + HOST + ".txt", "w")
  saveoutput.write(readoutput.decode('ascii'))
  saveoutput.write("\n")


for IP in file:
  IP=IP.strip()
  print ('Get config from Switch ' + (IP))
  HOST = IP
  tel = telnetlib.Telnet(HOST,23, timeout=1)
  tel.read_until(b'Username: ')
  tel.write(user.encode('ascii') + b'\n')
  if password:
    tel.read_until(b'Password: ')
    tel.write(password.encode('ascii') + b'\n')
  else:
    print("Wrong Pass!!")
    tel.write(b"enable\n")
    tel.write(password.encode('ascii') + b'\n')
  show_run()
