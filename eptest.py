import requests, json
import minimalmodbus
import serial
from os import system
import sys
from time import gmtime, strftime, sleep
from datetime import datetime
from prometheus_client import start_http_server, Gauge, Counter
from epever import TracerAN


start_http_server(62442)



Martinsville_EP1_power= Gauge('Martinsville_EP1_solar_power', 'power')
Martinsville_EP1_voltage= Gauge('Martinsville_EP1_voltage', 'voltage')
Martinsville_EP1_temp= Gauge('Martinsville_EP1_temp', 'voltage')

print("Jut's EPEVER Model: Tracer 6415AN (3000W/48V/60A battery current")
print("Ron's EPEVER Model: Tracer 4215BN")


def manual_mode(epever):

	while 1:

		# try:
			i = input("command or address?  ")
			
			if i=='q' or i=="":
				break
				
			elif 'A' in i: print(epever.print_params('A'))
			elif 'B' in i: print(epever.print_params('B'))
			elif 'C' in i: print(epever.print_params('C'))
			elif 'D' in i: print(epever.print_params('D'))
			elif 'E' in i: print(epever.print_params('E'))
			elif 'F' in i: print(epever.print_params('F'))
			
			elif 'clock' in i: print(epever.print_clock())
					
			elif i=='v':
				print(epever.battv())
				
			elif 'r' in i:
				a = i.replace('r','')
				a = int(a,16)
				print(epever.read_register(a))

					
			elif 'l' in i:
				a = i.replace('l','')
				a = int(a,16)
				print(epever.read32(a))
				
				
			elif 'w' in i:
			
				a = i.replace('w','')
				a = int(a,16)
				
				print(epever.read(a))
					
				val = int(input("write value?  "),10)
				epever.write(a,val)
				sleep(0.5)
				print(epever.read(a))

			else:
				addr = int(i,16)
				print(epever.read(addr,'d'))
				
		# except Exception as e:
		# except:
			# print('manual mode exception:',e)




# myep = epever('/dev/ttyUSB0')
myep = TracerAN('/dev/ttyUSB1')

# myep.set_limits(12)
# myep.print_group('charge1')
# myep.print_group('device')
# myep.print_params('B')

manual_mode(myep)


print('logging')
while 1:
	dt = strftime("%b %d %Y  %I:%M:%S %p %Z")

	avgs=1000

	c=0
	vt=0
	tt=0
	pt=0
	
	while c<=avgs:
	
		try:
			p=myep.power_pv()
			v=myep.battv()
			t=myep.temp()
			ec=myep.read_error_counter
			pt+=p
			vt+=v
			tt+=t
			print("%.1fV\t%.1fF\t%.1fW\t%dReadErros\t%d of %d" % (v,t,p,ec,c,avgs))
			c+=1
			# print(".",end='')
		except Exception as e:
			print(e,'\t',c,'of',avgs)
			sleep(2)

	pt/=avgs
	vt/=avgs
	tt/=avgs
	
	Martinsville_EP1_power.set(pt)
	Martinsville_EP1_voltage.set(vt)
	Martinsville_EP1_temp.set(tt)
	print("%s\t%.1fV\t%.1fF\t%.1fW\t%dReadErros" % (dt,v,t,p,ec))


	
