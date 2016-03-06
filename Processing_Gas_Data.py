import xlrd
import pandas
from constant import abbrevs
from math import radians, sin, cos, asin, sqrt

def dist(a1, b1, a2, b2):
	point1 = (a1,b1)
	point2 = (a2,b2)
	earth_radius_miles = 3956
	lat1, lon1 = (radians(coord) for coord in point1)
	lat2, lon2 = (radians(coord) for coord in point2)
	dlat, dlon = (lat2 - lat1, lon2 - lon1)
	a = sin(dlat/2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon/2.0)**2
	great_circle_distance = 2 * asin(min(1,sqrt(a)))
	d = earth_radius_miles * great_circle_distance
	return d

def adding_gas_price():
	workbook = xlrd.open_workbook("PET_PRI_ALLMG_A_EPM0_PWA_DPGAL_M.xls")
	worksheet = workbook.sheet_by_name('Data 1')

	state_gas_dict = {}
	gas_price_list = worksheet.row(worksheet.nrows - 1)
	state_list = worksheet.row(2)
	counter = 0

	for index in range(2, len(state_list)):
		state = str(state_list[index])
		price = str(gas_price_list[index])

		price = float(price[7:])
		state = state[7:state.index("Total")-1]
		state_gas_dict[state] = price


	gas_list = []


	for index, row in cities.iterrows():

		state = abbrevs[row.state]
		gas_list.append(state_gas_dict[state])



	cities['gasprice'] = pandas.Series(gas_list, index=cities.index)
	cities.to_csv('cities.csv')


def add_driving_dst():
	dst_list = []

	for index, row in cities.iterrows():

		lat1 =  row['lat']
		lng1 = row['lng']
		lat2 =  row['cliniclat']
		lng2 = row['cliniclng']
		d = dist(lat1, lng1, lat2, lng2)
		dst_list.append(d)

	cities['dst_to_clinic'] = pandas.Series(dst_list, index=cities.index)
	cities.to_csv('cities1.csv')
	print "finish"
if __name__ == "__main__":
	cities = pandas.read_csv('cities.csv') 
	add_driving_dst()
	# adding_gas_price()