import xlrd
import pandas
from constant import abbrevs


workbook = xlrd.open_workbook("PET_PRI_ALLMG_A_EPM0_PWA_DPGAL_M.xls")
worksheet = workbook.sheet_by_name('Data 1')

# print worksheet.nrows
# for i in range(worksheet.nrows):
# 	print worksheet.row(i)
# 	break
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

# print state_gas_dict

gas_list = []

# def write_gas_data():
cities = pandas.read_csv('cities.csv') 
# counter = 0	

for index, row in cities.iterrows():

	state = abbrevs[row.state]
	# print state
	# break
	gas_list.append(state_gas_dict[state])
	# counter += 1
	# if counter > 10:
	# 	break



cities['gasprice'] = pandas.Series(gas_list, index=cities.index)
cities.to_csv('cities.csv')

