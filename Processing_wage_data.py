# Processing_wage_data.py
import pandas
from constant import abbrevs

# abbrevs['DC'] = 'Washington'

abbrevs_inverted = dict((v,k) for k,v in abbrevs.iteritems())

state_gas = {}
cities = pandas.read_csv('State_average_wage.csv') 
for index, row in cities.iterrows():
	# state = state[7:state.index("Total")-1]
	state = row['area_title']
	wage = float(row['avg_wkly_wage'])/34
	# print wage
	try:
		state = state[:(state.index('--')-1)]
	except Exception as e:
		pass

	try:
		state = abbrevs_inverted[state]
		state_gas[state] = wage
	except Exception as e:
		print state
	# break

# print state_gas
# avg_wkly_wage

wage_list = []
# def write_gas_data():
cities = pandas.read_csv('cities.csv') 
# counter = 0	

for index, row in cities.iterrows():

	state = row.state

	wage_list.append(state_gas[state])
	# counter += 1
	# if counter > 10:
	# 	break



cities['avg_wkly_wage'] = pandas.Series(wage_list, index=cities.index)
cities.to_csv('cities.csv')



