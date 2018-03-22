__author__ = 'Peter Cybriwsky & Winston Frick'

import re

# This snippet gets the final verdict of a bill in gettting passed or not
bill_actions_csv = open("states/virginia/va_bill_actions.csv", "r")
output_csv = open("states/virginia/final_bill_wordage.txt", "w")
bill_sponsors_csv = open("states/virginia/va_bill_sponsors.csv", "r")
legislators_csv = open("states/virginia/va_legislators.csv", "r")


legislators = {}
# bill_id : legislator_id
bill_sponsor = {}
legislators_bills = {}

legislators_csv.readline()

class bills:
	def __init__ (self):
		self.bill_number = '0'
		self.date = ''
		self.primary_sponsor = 'None'
		self.sponsors_ID = 'None'
		self.stages = [1,0,0,0,0]
		self.significance = False

def fill_out():
	bill_sponsors_csv = open("states/virginia/va_bill_sponsors.csv", "r")
	bill_objects = {}

	for line in bill_sponsors_csv:
		attributes = line.strip().split(',')
		legislator_type = attributes[4]
		if legislator_type != 'primary':
			continue
		bill_id = attributes[3]
		if bill_id in bill_objects:
			continue
		leg_id = attributes[6]
		bill_sponsor[bill_id] = leg_id
		bill = bills()
		bill.bill_number = bill_id
		bill.primary_sponsor = attributes[5]
		if attributes[6] == ' Jr."' or attributes[6] == ' Sr."' or attributes[6] == ' III"' or attributes[6] == ' II"':
			bill.primary_sponsor = attributes[5] + attributes[6]
			bill.sponsors_ID = attributes[7]
		else:
			bill.sponsors_ID = attributes[6]

		bill_objects[bill_id] = bill
	bill_sponsors_csv.close()

	bill_actions_csv = open("states/virginia/va_bill_actions.csv", "r")
	bill_value = [1,0,0,0,0]
	first_line = bill_actions_csv.readline()
	first_line = line.strip().split(',')
	curr_id = first_line[3]

	for line in bill_actions_csv:
		attributes = line.strip().split(',')
		bill_id = attributes[3]
		bill_action = attributes[5]

		if bill_id in bill_objects:
			current_bill = bill_objects[bill_id]
		else:
			bill = bills()
			bill.bill_number = bill_id
			bill_objects[bill_id] = bill

		current_bill = bill_objects[bill_id]

		if current_bill.date == '':
			current_bill.date = attributes[4]

		if bill_id != curr_id:
			bill_value = [1,0,0,0,0]
			current_bill = bill_objects[curr_id]
			current_bill.stages = bill_value
			curr_id = bill_id

		regex5 = re.compile(r"signed by president",flags=re.IGNORECASE)
		results5 = regex5.findall(bill_action)

		if results5 or bill_value[4] == 1:
			bill_value[4] = 1 
			continue

		regex4 = re.compile(r"enrolled",flags=re.IGNORECASE)
		regex_4 = re.compile(r"VOTE: --- PASSAGE",flags=re.IGNORECASE)
		regex4_4 = re.compile(r"VOTE: PASSAGE",flags=re.IGNORECASE)
		results4 = regex4.findall(bill_action)
		results_4 = regex_4.findall(bill_action)
		results4_4 = regex4_4.findall(bill_action)

		if results4 or results_4 or results4_4 or bill_value[3] == 1:
			bill_value[3] = 1
			continue

		regex3 = re.compile(r"Committee substitute agreed .+")
		results3 = regex3.findall(bill_action)
		regex_3 = re.compile(r"engrossed",flags=re.IGNORECASE)
		results_3 = regex_3.findall(bill_action)

		if results3 or results_3 or bill_value[2] == 1:
			bill_value[2] = 1
			continue

		regex2 = re.compile(r"Subcommittee recommends .+")
		results2 = regex2.findall(bill_action)

		if results2:
			bill_value[1] = 1
			continue	

	return bill_objects	
	bill_actions_csv.close()

def significance(bills_list):
	significant_bills = set()
	featured_bills = open("states/virginia/VA_SS_BILLS_2017.csv", "r")
	for line in featured_bills:
		attributes = line.strip().split(',')
		significant_bills.add(attributes[0])
	for a_bill in bills_list:
		if a_bill in significant_bills:
			bills_list[a_bill].significance = True
		else:
			continue 
	return bills_list


bill_objects = fill_out()
bill_objects = significance(bill_objects)

output2 = open("bills_final.csv", "w")
line = ""
line += "bill_number, introduction date, primary sponsor, sponsor_id, stages, , , , ,significance"
output2.write(line + "\n")
for bill_IDS, final_bill in bill_objects.items():
	lines = ""
	lines += str(final_bill.bill_number) + "," + str(final_bill.date) + "," + str(final_bill.primary_sponsor.strip('"')) + "," +  str(final_bill.sponsors_ID) + "," + str(final_bill.stages[0]) + "," + str(final_bill.stages[1]) + "," + str(final_bill.stages[2]) + "," + str(final_bill.stages[3]) + "," + str(final_bill.stages[4]) + "," + str(final_bill.significance) + ","
	output2.write(lines + "\n")

output2.close()





