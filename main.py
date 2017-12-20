__author__ = 'Peter Cybriwsky & Winston Frick'

import re

# This snippet gets the final verdict of a bill in gettting passed or not
bill_actions_csv = open("states/virginia/va_bill_actions.csv", "r")
output_csv = open("states/virginia/final_bill_wordage.txt", "w")
bill_sponsors_csv = open("states/virginia/va_bill_sponsors.csv", "r")
legislators_csv = open("states/virginia/va_legislators.csv", "r")

legislators = {}
bill_sponsor = {}
legislators_bills = {}

legislators_csv.readline()
# key value of leg_id and name 
for line in legislators_csv:
	attributes = line.strip().split(',')
	leg_id = attributes[0]
	full_name = attributes[1]
	legislators[leg_id] = full_name
	legislators_bills[leg_id] = []

# key value of bill_id and corresponding leg_id
# key value of a leg and a list of all of his bill_ids
for line in bill_sponsors_csv:
	attributes = line.strip().split(',')
	legislator_type = attributes[4]
	if legislator_type != 'primary':
		continue
	bill_id = attributes[3]
	leg_id = attributes[6]
	bill_sponsor[bill_id] = leg_id
	if leg_id in legislators_bills:
		legislators_bills[leg_id].append(bill_id)
	else:
		legislators_bills[leg_id] = [bill_id]

bill_weight = {}
bill_value = 1
first_line = bill_actions_csv.readline()
first_line = line.strip().split(',')
curr_id = first_line[3]
# each bill ID is given a number 1-5 based on which stage it got to 
# bill weight is each bill and it's corresponding weight
for line in bill_actions_csv:
	attributes = line.strip().split(',')
	bill_id = attributes[3]
	bill_action = attributes[5]


	if bill_id != curr_id:
		bill_weight[curr_id] = bill_value
		bill_value = 1
		curr_id = bill_id

	regex5 = re.compile(r"signed by president",flags=re.IGNORECASE)
	results5 = regex5.findall(bill_action)

	if results5 or bill_value == 5:
		bill_value = 5
		continue

	regex4 = re.compile(r"enrolled",flags=re.IGNORECASE)
	regex_4 = re.compile(r"VOTE: --- PASSAGE",flags=re.IGNORECASE)
	regex4_4 = re.compile(r"VOTE: PASSAGE",flags=re.IGNORECASE)
	results4 = regex4.findall(bill_action)
	results_4 = regex_4.findall(bill_action)
	results4_4 = regex4_4.findall(bill_action)

	if results4 or results_4 or results4_4 or bill_value == 4:
		bill_value = 4
		continue

	regex3 = re.compile(r"Committee substitute agreed .+")
	results3 = regex3.findall(bill_action)
	regex_3 = re.compile(r"engrossed",flags=re.IGNORECASE)
	results_3 = regex_3.findall(bill_action)

	if results3 or results_3 or bill_value == 3:
		bill_value = 3
		continue

	regex2 =re.compile(r"Subcommittee recommends .+")
	results2 = regex2.findall(bill_action)

	if results2:
		bill_value = 2
		continue


final = {}
# fill final with every leg_id and all of his bills weights in list form [0,0,0,0,0]
for bill,weight in bill_weight.items():
	# check this if statement
	if bill in bill_sponsor:
		leg = bill_sponsor[bill]
		if leg == '':
			# print("----------- " + bill + "----------")
	else:
		continue
	if leg not in final:
		final[leg] = [0,0,0,0,0]

	weight = int(weight)
	final[leg][weight -1] = final[leg][weight-1] + 1

output = open("virginia_final.csv","w")

line = ""
line += "Name, leg_id, bill introduced, bill received action, bill approved, bill passed, bill become law"
output.write(line + "\n")
# write to a file final plus the leg_id's name
for leg,weight in final.items():
	line = ""
	if leg in legislators:
		line+= legislators[leg] + "," + leg + "," + str(weight[0]) + "," + str(weight[1]) + "," + str(weight[2]) + "," + str(weight[3]) + "," + str(weight[4])
	else:
		continue
	output.write(line + "\n")

output.close()
