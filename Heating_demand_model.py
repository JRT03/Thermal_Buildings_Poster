import numpy as np
import matplotlib.pyplot as plt

#SAMPLING DATES
#Janurary 31st(1-2), 6th(3-6), 8th(7-10), 13th(11,15), 18th(16-20), 23rd(21-25), 28th(26-31) January is non standard as there is some data missing 

#Febuary - 3rd(1-5), 8th(6-10), 13th(11-15), 18th(16-20), 23rd(21-25), 28th(26-28) 

#30 day month - 3rd(1-5), 8th(6-10), 13th(11-15), 18th(16-20), 23rd(21-25), 28th(26-30) 

#31 day month - 3rd(1-5), 8th(6-10), 13th(11-15), 18th(16-20), 23rd(21-25), 28th(26-31)

#DAY SAMPLING
#15min (00:00 - 00:15), 30min(00:15-45:00)...30min....., 15min (23:45-23:59)

def getday(daytext):
    '''Function to read in dates'''
    with open(daytext,'r') as f:
        read = f.readlines()

    daytemp = np.zeros(len(read) - 8)
    
    for i in range(len(read)-8):
        daytemp[i] = float(read[i+8][6:10])
    
    try:
        assert(len(daytemp) == 49)
    except:
        print(daytext)
    return daytemp

daytemp = getday('2022temps/2022_01_20')
print(daytemp)
print(len(daytemp))

thermosetting = np.zeros(49)
thermosetting[:11] = 15
thermosetting[11:15] = 18
thermosetting[15:35] = 15
thermosetting[35:47] = 18
thermosetting[47:] = 15

def temprature_demand_day(thermosetting,daytemp):
    '''Find the temprature deamand of the day in degree minutes'''
    demand = (thermosetting[0] - daytemp[0]) * 0.0104167 #15 mins is 0.0104167 days
    for i in range(1,len(daytemp)-1):
        if thermosetting[i] > daytemp[i]:
            demand += (thermosetting[i] - daytemp[i]) * 0.0208333 #30 mins is 0.0208333 days
    demand += (thermosetting[-1] - daytemp[-1]) * 0.0104167 
    return demand

demand = temprature_demand_day(thermosetting,daytemp)

def average_temp(daytemp):
    '''Average temprature allows for testing of demand function.
    If the thermostat setting is constant the temprature demand (in degree days) is the difference in thermostat temprature to the average temprature'''
    atemp = 0.5*daytemp[0] 
    for i in range(1,len(daytemp)-1):
        atemp += daytemp[i]
    atemp += 0.5*daytemp[-1]
    atemp = atemp/48
    return atemp

def tempdemand_30daymonth(month,thermosetting):
    '''Find temprature demand for a month with 30 days'''
    monthdemand = 0
    month = str(month)
    if len(month) == 1:
        month = '0' + month
    for i in range(1,31):
        day = str(i)
        if len(day) == 1:
            day = '0' + day
        file = '2022temps/2022_' + str(month) + '_' + day 
        daytemp = getday(file)
        monthdemand += temprature_demand_day(thermosetting,daytemp)
    return monthdemand

def tempdemand_31daymonth(month,thermosetting):
    '''Find temprature demand for a month with 31 days'''
    monthdemand = 0
    month = str(month)
    if len(month) == 1:
        month = '0' + month
    for i in range(1,32):
        day = str(i)
        if len(day) == 1:
            day = '0' + day
        file = '2022temps/2022_' + str(month) + '_' + day 
        daytemp = getday(file)
        monthdemand += temprature_demand_day(thermosetting,daytemp)
    return monthdemand

def tempdemand_jan(thermosetting):
    '''Find temprature demand for Janurary which has data deficiency for the first 5 days'''
    monthdemand = 0
    month = '01'
    daytemp = getday('2022temps/2022_01_06')
    monthdemand += (temprature_demand_day(thermosetting,daytemp))*6 #Extrapolating the 6th day over the first 5 days to avoid deficency
    for i in range(7,32):
        day = str(i)
        if len(day) == 1:
            day = '0' + day
        file = '2022temps/2022_' + month + '_' + day 
        daytemp = getday(file)
        monthdemand += temprature_demand_day(thermosetting,daytemp)
    return monthdemand

def tempdemand_feb(thermosetting):
    '''Find temprature demand for Janurary which has data deficiency for the first 5 days'''
    monthdemand = 0
    month = '02'    
    for i in range(1,29):
        day = str(i)
        if len(day) == 1:
            day = '0' + day
        file = '2022temps/2022_' + month + '_' + day 
        daytemp = getday(file)
        monthdemand += temprature_demand_day(thermosetting,daytemp)
    return monthdemand
  

septdemand = tempdemand_30daymonth(9,thermosetting)
print(septdemand)

septdaytemp = getday('2022temps/2022_09_15')
septday = temprature_demand_day(thermosetting, septdaytemp)

print(septday)
print(septday*30)
print(septdaytemp)

#Find the year temprature demand per month
yeardemand = np.zeros(12)

yeardemand[0] = tempdemand_jan(thermosetting)
yeardemand[1] = tempdemand_feb(thermosetting)
daysinmonth = [True,False,True,False,True,True,False,True,False,True] #months march to decemeber True = 31 days False = 30 days
for i in range(3,13):
    if daysinmonth[i-3]:
        yeardemand[i-1] = tempdemand_31daymonth(i,thermosetting)
    else:
        yeardemand[i-1] = tempdemand_30daymonth(i,thermosetting)

print(yeardemand)
monthlables = ['Janurary', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
plt.bar(monthlables,yeardemand,color='#ee5656',zorder=3)
sub_title = '2022 Temprature Demand\nThermostat setting:(22:45-5:45 and 6:45-16:45)-15°C rest at 18°C\nTotal demand: ' + str(np.around(np.sum(yeardemand))) + ' degree-days'
plt.title(sub_title, fontsize=12)
plt.ylabel('Temprature Demand (degree-days)')
plt.xticks(rotation=45)
plt.grid(which='major', axis='y', zorder=0)
plt.show()
