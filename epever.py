# https://diysolarforum.com/threads/setting-registers-in-epever-controller-with-python.25406/
import minimalmodbus
import serial
from math import log10
from time import sleep


class TracerAN:

	def __init__(self,device='/dev/ttyUSB0',addr=1):
	
		print("init start")
		
		
		try:
			self.epever = minimalmodbus.Instrument(device, addr) # port name, slave address (in decimal)
		except Exception as e:
			print(e)
			quit()


			
		self.epever.serial.baudrate = 115200		 # Baud
		self.epever.serial.bytesize = 8
		self.epever.serial.parity   = serial.PARITY_NONE
		self.epever.serial.stopbits = 1
		self.epever.serial.timeout  = 0.2		  # seconds

		# epever.mode = minimalmodbus.MODE_ASCII
		self.epever.mode = minimalmodbus.MODE_RTU
		# print(epever)


		self.params={
				0x2000:{'group':'fucked','param':'A1','desc':'Over temperature inside the device','fcr':4,'fcw':None,'unit':'','scale':1},   # no reponse
				0x200c:{'group':'fucked','param':'A2','desc':'day or night','fcr':2,'fcw':None,'unit':'','scale':1},    # no reponse
				0x3100:{'group':'vitals','param':'A3','desc':'PV array input voltage','fcr':4,'fcw':None,'unit':'V','scale':100},
				0x3101:{'group':'vitals','param':'A4','desc':'PV array input current','fcr':4,'fcw':None,'unit':'A','scale':100},
				0x3102:{'group':'vitals','param':'A5','desc':'PV array input power L','fcr':4,'fcw':None,'unit':'W','scale':100},
				0x3103:{'group':'vitals','param':'A6','desc':'PV array input power H','fcr':4,'fcw':None,'unit':'W','scale':100},
				0x3110:{'group':'vitals','param':'A11','desc':'Battery temperature','fcr':4,'fcw':None,'unit':'C','scale':100},
				0x3111:{'group':'vitals','param':'A12','desc':'Device temperature','fcr':4,'fcw':None,'unit':'C','scale':100},
				0x331A:{'group':'vitals','param':'A36','desc':'Battery voltage','fcr':4,'fcw':None,'unit':'V','scale':100},
				0x331B:{'group':'vitals','param':'A37','desc':'Battery current L','fcr':4,'fcw':None,'unit':'A','scale':100},
				0x331C:{'group':'vitals','param':'A38','desc':'Battery current H','fcr':4,'fcw':None,'unit':'A','scale':100},
				0x310C:{'group':'load','param':'A7','desc':'Load voltage','fcr':4,'fcw':None,'unit':'V','scale':100},
				0x310D:{'group':'load','param':'A8','desc':'Load current','fcr':4,'fcw':None,'unit':'A','scale':100},
				0x310E:{'group':'load','param':'A9','desc':'Load power L','fcr':4,'fcw':None,'unit':'W','scale':100},
				0x310F:{'group':'load','param':'A10','desc':'Load power H','fcr':4,'fcw':None,'unit':'W','scale':100},
				0x311A:{'group':'g1','param':'A13','desc':'Battery SOC','fcr':4,'fcw':None,'unit':'%','scale':1},
				0x311D:{'group':'g1','param':'A14','desc':'Battery real rated voltage','fcr':4,'fcw':None,'unit':'V','scale':100},
				0x3200:{'group':'g1','param':'A15','desc':'Battery status','fcr':4,'fcw':None,'unit':'','scale':100},
				0x3201:{'group':'g1','param':'A16','desc':'Charging equipment status','fcr':4,'fcw':None,'unit':'','scale':100},
				0x3202:{'group':'g1','param':'A17','desc':'Discharging equipment status','fcr':4,'fcw':None,'unit':'','scale':100},
				0x3302:{'group':'g1','param':'A18','desc':'voltage today','fcr':4,'fcw':None,'unit':'V','scale':100},
				0x3303:{'group':'g1','param':'A19','desc':'Minimum battery voltage today','fcr':4,'fcw':None,'unit':'V','scale':100},
				0x3304:{'group':'g1','param':'A20','desc':'Consumed energy today L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3305:{'group':'g1','param':'A21','desc':'Consumed energy today H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3306:{'group':'g1','param':'A22','desc':'Consumed energy this month L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3307:{'group':'g1','param':'A23','desc':'Consumed energy this month H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3308:{'group':'g1','param':'A24','desc':'Consumed energy this year L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3309:{'group':'g1','param':'A25','desc':'Consumed energy this year H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x330A:{'group':'g1','param':'A26','desc':'Total consumed energy L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x330B:{'group':'g1','param':'A27','desc':'Total consumed energy H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x330C:{'group':'g1','param':'A28','desc':'Generated energy today L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x330D:{'group':'g1','param':'A29','desc':'Generated energy today H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x330E:{'group':'g1','param':'A30','desc':'Generated energy this month L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x330F:{'group':'g1','param':'A31','desc':'Generated energy this month H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3310:{'group':'g1','param':'A32','desc':'Generated energy this year L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3311:{'group':'g1','param':'A33','desc':'Generated energy this year H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3312:{'group':'g1','param':'A34','desc':'Total generated energy L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3313:{'group':'g1','param':'A35','desc':'Total generated energy H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				
				0x3005:{'group':'g1','param':'B1','desc':'Rated charging current','fcr':4,'fcw':None,'unit':'A','scale':100},
				0x300E:{'group':'g1','param':'B2','desc':'Rated load current','fcr':4,'fcw':None,'unit':'A','scale':100},
				0x311D:{'group':'g1','param':'B3','desc':'Battery real rated voltage','fcr':4,'fcw':None,'unit':'V','scale':100},
				
				0x9000:{'group':'charge1','param':'B4','desc':'Battery type','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9001:{'group':'charge1','param':'B5','desc':'Battery Capacity','fcr':3,'fcw':0x10,'unit':'Ah','scale':1},
				0x9002:{'group':'charge1','param':'B6','desc':'Temperature compensation coefficient','fcr':3,'fcw':0x10,'unit':'mVpC','scale':100},
				0x9003:{'group':'charge1','param':'B7','desc':'Over voltage disconnect voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x9004:{'group':'charge1','param':'B8','desc':'Charging limit voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x9005:{'group':'charge1','param':'B9','desc':'Over voltage reconnect voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x9006:{'group':'charge1','param':'B10','desc':'Equalize charging voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x9007:{'group':'charge1','param':'B11','desc':'Boost charging voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x9008:{'group':'charge1','param':'B12','desc':'Float charging voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x9009:{'group':'charge1','param':'B13','desc':'Boost reconnect charging voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x900A:{'group':'charge1','param':'B14','desc':'Low voltage reconnect voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x900B:{'group':'charge1','param':'B15','desc':'Under voltage warning recover voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x900C:{'group':'charge1','param':'B16','desc':'Under voltage warning voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x900D:{'group':'charge1','param':'B17','desc':'Low voltage disconnect voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x900E:{'group':'charge1','param':'B18','desc':'Discharging limit voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				#0x900F:{'group':'charge1','param':'B??','desc':'unknown','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9067:{'group':'charge','param':'B19','desc':'Battery rated voltage level','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x906A:{'group':'charge','param':'B20','desc':'Default load On/Off in manual mode','fcr':3,'fcw':0x10,'unit':'','scale':100},
				0x906B:{'group':'charge','param':'B21','desc':'Equalize duration','fcr':3,'fcw':0x10,'unit':'','scale':100},
				0x906C:{'group':'charge','param':'B22','desc':'Boost duration','fcr':3,'fcw':0x10,'unit':'','scale':100},
				0x906D:{'group':'charge','param':'B23','desc':'Battery discharge','fcr':3,'fcw':0x10,'unit':'','scale':100},
				0x906E:{'group':'charge','param':'B24','desc':'Battery charge','fcr':3,'fcw':0x10,'unit':'','scale':100},
				0x9070:{'group':'charge','param':'B25','desc':'Charging mode','fcr':3,'fcw':0x10,'unit':'','scale':100},
				#0x9107:{'group':'charge','param':'B26','desc':'Li Battery Protection &  Over Temp. Drop Power','fcr':3,'fcw':0x10,'unit':'','scale':100},
				0x0002:{'group':'load','param':'C1','desc':'Manual control the load','fcr':None,'fcw':0x10,'unit':'','scale':1},
				0x901E:{'group':'load','param':'C2','desc':'Night time threshold voltage(NTTV)','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x901F:{'group':'load','param':'C3','desc':'Light signal startup (night) delay time','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9020:{'group':'load','param':'C4','desc':'Day time threshold voltage(DTTV)','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x9021:{'group':'load','param':'C5','desc':'Light signal close (day) delay time','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x903D:{'group':'load','param':'C6','desc':'Load control mode','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x903E:{'group':'load','param':'C7','desc':'Light on + time(time1)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x903F:{'group':'load','param':'C8','desc':'Light on + time(time2)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9042:{'group':'load','param':'C9','desc':'Timing control (turn on time1)','fcr':3,'fcw':0x10,'unit':'S','scale':1},
				0x9043:{'group':'load','param':'C10','desc':'Timing control (turn on time1)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9044:{'group':'load','param':'C11','desc':'','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9045:{'group':'load','param':'C12','desc':'Timing control (turn off time1)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9046:{'group':'load','param':'C13','desc':'','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9047:{'group':'load','param':'C14','desc':'','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9048:{'group':'load','param':'C15','desc':'Timing control (turn on time2)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9049:{'group':'load','param':'C16','desc':'','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x904A:{'group':'load','param':'C17','desc':'Timing control (time choose)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x904B:{'group':'load','param':'C18','desc':'Default','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x904C:{'group':'load','param':'C19','desc':'Timing control (turn off time2)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x904D:{'group':'load','param':'C20','desc':'','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9065:{'group':'load','param':'C21','desc':'','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9069:{'group':'load','param':'C22','desc':'Night time','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x906A:{'group':'load','param':'C23','desc':'Timing control (time choose)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9013:{'group':'realTimeClock','param':'D1','desc':'Real time clock: D7-0 Sec, D15-8Min','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9014:{'group':'realTimeClock','param':'D2','desc':'Real time clock: D7-0 Hour, D15-8 Day','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9015:{'group':'realTimeClock','param':'D3','desc':'Real time clock: D7-0 Month, D15-8 Year','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9010:{'group':'device','param':'E1','desc':'Lower Temperature Charging Limit','fcr':3,'fcw':0x10,'unit':'C','scale':100},
				0x9011:{'group':'device','param':'E2','desc':'Lower Temperature Discharging Limit','fcr':3,'fcw':0x10,'unit':'C','scale':100},
				0x9017:{'group':'device','param':'E3','desc':'Battery upper temperature limit','fcr':3,'fcw':16,'unit':'C','scale':100},
				0x9018:{'group':'device','param':'E4','desc':'Battery lower temperature limit','fcr':3,'fcw':0x10,'unit':'C','scale':100},
				0x9019:{'group':'device','param':'E5','desc':'Device over temperature','fcr':3,'fcw':0x10,'unit':'C','scale':100},
				0x901A:{'group':'device','param':'E6','desc':'Device recovery temperature','fcr':3,'fcw':0x10,'unit':'C','scale':100},
				0x9063:{'group':'device','param':'E7','desc':'Backlight time','fcr':3,'fcw':0x10,'unit':'S','scale':1},
				}



		self.paramsAN={
				0x2000:{'group':'fucked','param':'A1','desc':'Over temperature inside the device','fcr':4,'fcw':None,'unit':'','scale':1},   # no reponse
				0x200c:{'group':'fucked','param':'A2','desc':'day or night','fcr':2,'fcw':None,'unit':'','scale':1},    # no reponse
				0x3100:{'group':'vitals','param':'A3','desc':'PV array input voltage','fcr':4,'fcw':None,'unit':'V','scale':100},
				0x3101:{'group':'vitals','param':'A4','desc':'PV array input current','fcr':4,'fcw':None,'unit':'A','scale':100},
				0x3102:{'group':'vitals','param':'A5','desc':'PV array input power L','fcr':4,'fcw':None,'unit':'W','scale':100},
				0x3103:{'group':'vitals','param':'A6','desc':'PV array input power H','fcr':4,'fcw':None,'unit':'W','scale':100},
				0x3110:{'group':'vitals','param':'A11','desc':'Battery temperature','fcr':4,'fcw':None,'unit':'C','scale':100},
				0x3111:{'group':'vitals','param':'A12','desc':'Device temperature','fcr':4,'fcw':None,'unit':'C','scale':100},
				0x331A:{'group':'vitals','param':'A36','desc':'Battery voltage','fcr':4,'fcw':None,'unit':'V','scale':100},
				0x331B:{'group':'vitals','param':'A37','desc':'Battery current L','fcr':4,'fcw':None,'unit':'A','scale':100},
				0x331C:{'group':'vitals','param':'A38','desc':'Battery current H','fcr':4,'fcw':None,'unit':'A','scale':100},
				0x310C:{'group':'load','param':'A7','desc':'Load voltage','fcr':4,'fcw':None,'unit':'V','scale':100},
				0x310D:{'group':'load','param':'A8','desc':'Load current','fcr':4,'fcw':None,'unit':'A','scale':100},
				0x310E:{'group':'load','param':'A9','desc':'Load power L','fcr':4,'fcw':None,'unit':'W','scale':100},
				0x310F:{'group':'load','param':'A10','desc':'Load power H','fcr':4,'fcw':None,'unit':'W','scale':100},
				0x311A:{'group':'g1','param':'A13','desc':'Battery SOC','fcr':4,'fcw':None,'unit':'%','scale':1},
				0x311D:{'group':'g1','param':'A14','desc':'Battery real rated voltage','fcr':4,'fcw':None,'unit':'V','scale':100},
				0x3200:{'group':'g1','param':'A15','desc':'Battery status','fcr':4,'fcw':None,'unit':'','scale':100},
				0x3201:{'group':'g1','param':'A16','desc':'Charging equipment status','fcr':4,'fcw':None,'unit':'','scale':100},
				0x3202:{'group':'g1','param':'A17','desc':'Discharging equipment status','fcr':4,'fcw':None,'unit':'','scale':100},
				0x3302:{'group':'g1','param':'A18','desc':'voltage today','fcr':4,'fcw':None,'unit':'V','scale':100},
				0x3303:{'group':'g1','param':'A19','desc':'Minimum battery voltage today','fcr':4,'fcw':None,'unit':'V','scale':100},
				0x3304:{'group':'g1','param':'A20','desc':'Consumed energy today L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3305:{'group':'g1','param':'A21','desc':'Consumed energy today H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3306:{'group':'g1','param':'A22','desc':'Consumed energy this month L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3307:{'group':'g1','param':'A23','desc':'Consumed energy this month H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3308:{'group':'g1','param':'A24','desc':'Consumed energy this year L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3309:{'group':'g1','param':'A25','desc':'Consumed energy this year H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x330A:{'group':'g1','param':'A26','desc':'Total consumed energy L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x330B:{'group':'g1','param':'A27','desc':'Total consumed energy H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x330C:{'group':'g1','param':'A28','desc':'Generated energy today L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x330D:{'group':'g1','param':'A29','desc':'Generated energy today H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x330E:{'group':'g1','param':'A30','desc':'Generated energy this month L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x330F:{'group':'g1','param':'A31','desc':'Generated energy this month H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3310:{'group':'g1','param':'A32','desc':'Generated energy this year L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3311:{'group':'g1','param':'A33','desc':'Generated energy this year H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3312:{'group':'g1','param':'A34','desc':'Total generated energy L','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				0x3313:{'group':'g1','param':'A35','desc':'Total generated energy H','fcr':4,'fcw':None,'unit':'kWh','scale':100},
				
				0x3005:{'group':'g1','param':'B1','desc':'Rated charging current','fcr':4,'fcw':None,'unit':'A','scale':100},
				0x300E:{'group':'g1','param':'B2','desc':'Rated load current','fcr':4,'fcw':None,'unit':'A','scale':100},
				0x311D:{'group':'g1','param':'B3','desc':'Battery real rated voltage','fcr':4,'fcw':None,'unit':'V','scale':100},
				
				0x9000:{'group':'charge1','param':'B4','desc':'Battery type','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9001:{'group':'charge1','param':'B5','desc':'Battery Capacity','fcr':3,'fcw':0x10,'unit':'Ah','scale':1},
				0x9002:{'group':'charge1','param':'B6','desc':'Temperature compensation coefficient','fcr':3,'fcw':0x10,'unit':'mVpC','scale':100},
				0x9003:{'group':'charge1','param':'B7','desc':'Over voltage disconnect voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x9004:{'group':'charge1','param':'B8','desc':'Charging limit voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x9005:{'group':'charge1','param':'B9','desc':'Over voltage reconnect voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x9006:{'group':'charge1','param':'B10','desc':'Equalize charging voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x9007:{'group':'charge1','param':'B11','desc':'Boost charging voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x9008:{'group':'charge1','param':'B12','desc':'Float charging voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x9009:{'group':'charge1','param':'B13','desc':'Boost reconnect charging voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x900A:{'group':'charge1','param':'B14','desc':'Low voltage reconnect voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x900B:{'group':'charge1','param':'B15','desc':'Under voltage warning recover voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x900C:{'group':'charge1','param':'B16','desc':'Under voltage warning voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x900D:{'group':'charge1','param':'B17','desc':'Low voltage disconnect voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x900E:{'group':'charge1','param':'B18','desc':'Discharging limit voltage','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x900F:{'group':'charge1','param':'B??','desc':'unknown','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9067:{'group':'charge','param':'B19','desc':'Battery rated voltage level','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x906A:{'group':'charge','param':'B20','desc':'Default load On/Off in manual mode','fcr':3,'fcw':0x10,'unit':'','scale':100},
				0x906B:{'group':'charge','param':'B21','desc':'Equalize duration','fcr':3,'fcw':0x10,'unit':'','scale':100},
				0x906C:{'group':'charge','param':'B22','desc':'Boost duration','fcr':3,'fcw':0x10,'unit':'','scale':100},
				0x906D:{'group':'charge','param':'B23','desc':'Battery discharge','fcr':3,'fcw':0x10,'unit':'','scale':100},
				0x906E:{'group':'charge','param':'B24','desc':'Battery charge','fcr':3,'fcw':0x10,'unit':'','scale':100},
				0x9070:{'group':'charge','param':'B25','desc':'Charging mode','fcr':3,'fcw':0x10,'unit':'','scale':100},
				0x9107:{'group':'charge','param':'B26','desc':'Li Battery Protection &  Over Temp. Drop Power','fcr':3,'fcw':0x10,'unit':'','scale':100},
				0x0002:{'group':'load','param':'C1','desc':'Manual control the load','fcr':None,'fcw':0x10,'unit':'','scale':1},
				0x901E:{'group':'load','param':'C2','desc':'Night time threshold voltage(NTTV)','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x901F:{'group':'load','param':'C3','desc':'Light signal startup (night) delay time','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9020:{'group':'load','param':'C4','desc':'Day time threshold voltage(DTTV)','fcr':3,'fcw':0x10,'unit':'V','scale':100},
				0x9021:{'group':'load','param':'C5','desc':'Light signal close (day) delay time','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x903D:{'group':'load','param':'C6','desc':'Load control mode','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x903E:{'group':'load','param':'C7','desc':'Light on + time(time1)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x903F:{'group':'load','param':'C8','desc':'Light on + time(time2)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9042:{'group':'load','param':'C9','desc':'Timing control (turn on time1)','fcr':3,'fcw':0x10,'unit':'S','scale':1},
				0x9043:{'group':'load','param':'C10','desc':'Timing control (turn on time1)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9044:{'group':'load','param':'C11','desc':'','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9045:{'group':'load','param':'C12','desc':'Timing control (turn off time1)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9046:{'group':'load','param':'C13','desc':'','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9047:{'group':'load','param':'C14','desc':'','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9048:{'group':'load','param':'C15','desc':'Timing control (turn on time2)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9049:{'group':'load','param':'C16','desc':'','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x904A:{'group':'load','param':'C17','desc':'Timing control (time choose)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x904B:{'group':'load','param':'C18','desc':'Default','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x904C:{'group':'load','param':'C19','desc':'Timing control (turn off time2)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x904D:{'group':'load','param':'C20','desc':'','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9065:{'group':'load','param':'C21','desc':'','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9069:{'group':'load','param':'C22','desc':'Night time','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x906A:{'group':'load','param':'C23','desc':'Timing control (time choose)','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9013:{'group':'realTimeClock','param':'D1','desc':'Real time clock: D7-0 Sec, D15-8Min','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9014:{'group':'realTimeClock','param':'D2','desc':'Real time clock: D7-0 Hour, D15-8 Day','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9015:{'group':'realTimeClock','param':'D3','desc':'Real time clock: D7-0 Month, D15-8 Year','fcr':3,'fcw':0x10,'unit':'','scale':1},
				0x9010:{'group':'device','param':'E1','desc':'Lower Temperature Charging Limit','fcr':3,'fcw':0x10,'unit':'C','scale':100},
				0x9011:{'group':'device','param':'E2','desc':'Lower Temperature Discharging Limit','fcr':3,'fcw':0x10,'unit':'C','scale':100},
				0x9017:{'group':'device','param':'E3','desc':'Battery upper temperature limit','fcr':3,'fcw':16,'unit':'C','scale':100},
				0x9018:{'group':'device','param':'E4','desc':'Battery lower temperature limit','fcr':3,'fcw':0x10,'unit':'C','scale':100},
				0x9019:{'group':'device','param':'E5','desc':'Device over temperature','fcr':3,'fcw':0x10,'unit':'C','scale':100},
				0x901A:{'group':'device','param':'E6','desc':'Device recovery temperature','fcr':3,'fcw':0x10,'unit':'C','scale':100},
				0x9063:{'group':'device','param':'E7','desc':'Backlight time','fcr':3,'fcw':0x10,'unit':'S','scale':1},
				}


		self.read_error_counter=0

	def print_group(self,group):

		for p in self.params:
		
			reg=self.params[p]
			if reg['group']==group:
				try:
					numDecimals=int(log10(reg['scale']))
					
					print(hex(p),self.epever.read_register(p,numDecimals,reg['fcr']),reg['unit'],'\t',reg['desc'])

				except Exception as e:
					print('error when reading register',hex(p),':',e)
		
	def print_params(self,paramgroup):

		for p in self.params:
		
			reg=self.params[p]
			if paramgroup in reg['param']:
				try:
					numDecimals=int(log10(reg['scale']))
					print(reg['param'],'\t',hex(p),'\t',self.epever.read_register(p,numDecimals,reg['fcr']),reg['unit'],'\t',reg['desc'])

				except Exception as e:
					print('error when reading register',hex(p),':',e)
				
	def print_clock(self):

		for p in self.params:
		
			reg=self.params[p]
			if 'D' in reg['param']:
				try:
					numDecimals=int(log10(reg['scale']))
					r=self.epever.read_register(p,numDecimals,reg['fcr'])
					print(reg['param'],'\t',r,hex(r),reg['desc'])

				except Exception as e:
					print('error when reading register',hex(p),':',e)
		
			
	def __str__(self):
		# return str(self.d) + " modules"
		# self.readModuleData()
		self.print_group_parameters('vitals')
	
		
	def write(self,addr,val):
		c=1
		reg=self.params[addr]
		try:
			scale=reg['scale']
			funCode=reg['fcw']
			numDecimals=int(log10(reg['scale']))
			# val = int(scale*val)
			# print('val',val)
			return self.epever.write_register(addr,val,numDecimals,funCode)
		except Exception as e:
			print('write exception',hex(addr),":",e)
			c+=1
			self.read_error_counter+=1
			
		
	def read(self,addr,verbosity=''):
		c=1
		reg=self.params[addr]
		# print('addr',addr,'reg',reg)
		retry=3
		debug=False
		if verbosity=='d': debug=True

		while c<=retry:
		
			try:
				numDecimals=int(log10(reg['scale']))
				funCode=reg['fcr']
				if debug:
					print('addr',addr,'decimals',numDecimals,'funcCode',funCode)
				r = self.epever.read_register(addr,numDecimals,funCode)		# read_register(addr,decimals,funcode,signed)
				if debug: print('register =',str(r),'type',type(r))	
				if verbosity=='re' and c<5: raise Exception("fuck")
				if verbosity=="v": u=reg['unit']
				elif verbosity=="vv" or verbosity=='d': 

					u=" " + reg['unit'] + "\t(" + reg['desc'] + ")"
					return hex(addr) + '\t' + str(r) + u  
				else:
					return r	
			except Exception as e:
				print('failed to read',hex(addr),":",e,'(attempt',c,'of',retry,')')
				c+=1
				self.read_error_counter+=1
				sleep(1)
		
		return None
		
	def read_register(self,addr):

		try:
			r = self.epever.read_register(addr,0,4)
			return r
		except Exception as e:
			print('failed to read:',e)

		return None
			
	def read32(self,addr):
		# r = self.epever.read_long(addr,4,False, minimalmodbus.BYTEORDER_LITTLE)
		# r = self.epever.read_long(addr,4,False, minimalmodbus.BYTEORDER_BIG)
		
		r = self.epever.read_long(addr,4,False, minimalmodbus.BYTEORDER_LITTLE_SWAP)
		print(r,r/100,hex(r))
		
		
		return r
			
	def set_limits(self,series_count):
	# https://diysolarforum.com/threads/setting-registers-in-epever-controller-with-python.25406/
		# rr=self.epever.read_registers(0x9000,15,3)
		# print(rr)
		
		s=series_count
		rr= [
			
			0,			# 0x9000	Battery type
			3,			# 0x9001	Battery Capacity
			0,			# 0x9002	Temperature compensation coefficient
			s*4+0.2,	# 0x9003	OVDV Over voltage (load) disconnect voltage
			s*4,		# 0x9004	CLV Charging limit voltage
			s*4,		# 0x9005	OVRV Over voltage reconnect voltage
			s*4,		# 0x9006	ECV Equalize charging voltage
			s*4,		# 0x9007	BCV Boost charging voltage
			s*4,		# 0x9008	FCV Float charging voltage
			s*4-0.2,	# 0x9009	BRCV Boost reconnect charging voltage
			s*3.3,		# 0x900A	LVR Low voltage reconnect voltage
			s*3.2,		# 0x900B	UVWR Under voltage warning recover voltage
			s*3.0+0.1,	# 0x900C	UVW Under voltage warning voltage
			s*3.0,		# 0x900D	LVD Low voltage disconnect voltage
			s*3.0,		# 0x900E	DLV Discharging limit voltage (warning)
			
			]
			
						# OVDV > OVRV = CLV >= ECV = BCV >= FCV > BRCV
						# Over Voltage Disconnect Voltage>Over Voltage Reconnect Voltage＝Charging Limit Voltage ≥ Equalize Charging Voltage＝Boost Charging Voltage ≥ Float Charging Voltage>Boost Reconnect Charging Voltage;
						
						# LVR > LVD >= DLV
						# Low Voltage Reconnect Voltage>Low Voltage Disconnect Voltage ≥ Discharging Limit Voltage;

						# UVWR > UVW >= DLV
						# Under Voltage Warning Reconnect Voltage>Under Voltage Warning Voltage≥ Discharging Limit Voltage;

						# BRCV > LVR
						# Boost Reconnect Charging voltage> Low Voltage Reconnect Voltage;
		
		# rr= [
			
			# 0,		# 0x9000	Battery type
			# 3,	# 0x9001	Battery Capacity
			# 0,		# 0x9002	Temperature compensation coefficient
			# 48,		# 0x9003	OVDV Over voltage disconnect voltage 
			# 47.9,	# 0x9004	CLV Charging limit voltage
			# 47.9,	# 0x9005	OVRV Over voltage reconnect voltage (load related)
			# 47.9,	# 0x9006	ECV Equalize charging voltage
			# 47.9,	# 0x9007	BCV Boost charging voltage
			# 47.9,	# 0x9008	FCV Float charging voltage
			# 47.8,	# 0x9009	BRCV Boost reconnect charging voltage (load related)
			# 39.0,	# 0x900A	LVR Low voltage reconnect voltage (load related)
			# 40.0,	# 0x900B	UVWR Under voltage warning recover voltage
			# 39.9,	# 0x900C	UVW Under voltage warning voltage
			# 38.0,	# 0x900D	LVD Low voltage disconnect voltage  (load related)
			# 38.0,	# 0x900E	DLV Discharging limit voltage
			
			# ]
				
		# rr = rr
		rr = [int(100*x) for x in rr]
		# print(rr)
	
		self.epever.write_registers(0x9000,rr)
		sleep(0.5)
		rr=self.epever.read_registers(0x9000,15,3)
		# print(rr)


	# https://diysolarforum.com/threads/struggling-with-basic-lifepo4-settings-in-epever-tracer.17785/
	# Over volts disconnect : if the battery volts exceed this , the load outputs disconnect from the load from the battery.

	# Charging limit voltage: if the battery volts exceed this, charging the battery from solar is stopped.

	# Over Voltage reconnect: if the load outputs have been disconnected due to the battery exceeding over voltage a reconnect will occur at this value.

	# Equalize charge voltage: used for lead acid batteries where a higher voltage is applied every 28 days for a duration to equalise the cells. Normally only used with flooded batteries. Use with sealed, AGM and GEL lead batteries only with manufactures approval.

	# Boost charge voltage: under the boost mode, the controller will charge the battery at maximum power from the solar panels until this value is reached. At all times before this 'target' voltage is reached the maximum power control process will will try to 'pull' maximum power from the panels. This is the bulk stage of charging where most of the battery capacity is restored.

	# Float charge voltage: once the boost duration has been completed the controller will modify the maximum power search and load the panels to produce a constant float voltage at the battery. Typically used for lead acid batteries to compensate for the self discharge. With lead acid batteries it may also 'top up' the battery. Where lithium batteries are charged setting to the resting voltage of the battery may be used.

	# Boost reconnect voltage: once the unit is in float mode the voltage may vary due to solar conditions and any load on the battery. If the battery voltage falls to this value the controller re enters the Boost stage.

	# Low voltage reconnect: if the load outputs have been disconnected due to a low battery, this voltage is the turn on value.

	# Under voltage warning re connect: warning turned off at this voltage.

	# Under voltage warning: warning set at this voltage.

	# Low voltage disconnect: load outputs are disconnected from the battery at this voltage.

	# Discharging limit voltage: other than issuing a warning at the set voltage the stand alone unit cannot do anything about this.

	# Equalize Duration: the time duration where the voltage is held constant with equalisation for lead acid batteries

	# Boost Duration: once the boost voltage has been reached the voltage will be held constant for this period. This is the absorption period where the battery is completely charged.

	def power_pv(self):
		L=int(self.read(0x3102))
		H=int(self.read(0x3103))
		p=((H<<16) + L)

		return round(p,1)
		
		
	def battv(self):
		# return self.read(0x331A,'re')
		return self.read(0x331A)
		
	
	def temp(self):
		a=0x3110
		c=float(self.read(a))
		return round(c*1.8+32)
		
		
	def rr(self):
		print(self.epever.read_registers(0x9000,15,3))
		
	
