from waitingtime import waitingtime

# drive time in hours
def get_total_times(drivetime, clinictime):
	if clinictime == 0:
		return drivetime*2, 0, drivetime*2
	elif drivetime < 5:
		if drivetime > 3 and drivetime < 5 and clinictime==18:
			return drivetime*2+clinictime, 1, drivetime*2
		else:
			return drivetime*2+clinictime, 0, drivetime*4
	elif clinictime < 48:
		return drivetime*2+clinictime, 1, drivetime*2
	elif drivetime < 9:
		return drivetime*2+clinictime, 0, drivetime*4
	elif clinictime == 48:
		return drivetime*2+clinictime, 2, drivetime*2
	else:
		return drivetime*2+clinictime, 3, drivetime*2

# drivetimes = [1,2,4,6,8,10,12]
# clinictimes = [0,18,24,48,72]

# for dt in drivetimes:
# 	for ct in clinictimes:
# 		print "Drivetime:", dt, "Clinictime:", ct
# 		print get_total_times(dt,ct)

# import pandas
# cities = pandas.read_csv('cities.csv')
