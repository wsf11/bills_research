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
        self.veto = 0
        self.overriden_veto = 0

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
    veto = False
    overriden_veto = False
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
            veto = 0
            overriden_veto = 0

        regex_veto = re.compile(r"Vetoed by Governor", flags=re.IGNORECASE)
        results_veto = regex_veto.findall(bill_action)

        if results_veto:
        	veto = 1
        	current_bill.veto = 1
        	continue

        if veto:
        	regex_overriden = re.compile(r"Governor's veto overridden",flags=re.IGNORECASE)
        	regex_overriden2 = re.compile(r"Bill became law",flags=re.IGNORECASE)
        	regex_overriden3 = re.compile(r"VOTE: OVERRIDE GOVERNOR'S VETO",flags=re.IGNORECASE)
 
    		results_over = regex_overriden.findall(bill_action)
    		results_over2 = regex_overriden2.findall(bill_action)
    		results_over3 = regex_overriden3.findall(bill_action)

    		if results_over or results_over2 or results_over3:
    			overriden_veto = 1
    			current_bill.overriden_veto = 1
    			continue


        regex5 = re.compile(r"enacted",flags=re.IGNORECASE)
        regex6 = re.compile(r"approved by governor",flags=re.IGNORECASE)
        results5 = regex5.findall(bill_action)
        results6 = regex5.findall(bill_action)

        if results5 or bill_value[4] == 1 or results6:
            bill_value[4] = 1 
            continue

        regex4 = re.compile(r"enrolled",flags=re.IGNORECASE)
        regex_4 = re.compile(r"VOTE: --- PASSAGE",flags=re.IGNORECASE)
        regex4_4 = re.compile(r"VOTE: PASSAGE",flags=re.IGNORECASE)
        regex4_5 = re.compile(r"Passed House",flags=re.IGNORECASE)
        regex4_6 = re.compile(r"Agreed to by House",flags=re.IGNORECASE)
        regex4_7 = re.compile(r"VOTE: ADOPTION",flags=re.IGNORECASE)
        regex4_8 = re.compile(r"Passed Senate",flags=re.IGNORECASE)
        regex4_9 = re.compile(r"Read third time and passed senate",flags=re.IGNORECASE)
        regex4_10 = re.compile(r"Agreed to by Senate",flags=re.IGNORECASE)
        regex4_11 = re.compile(r"Enrolled",flags=re.IGNORECASE)
        regex4_12 = re.compile(r"Signed by Speaker",flags=re.IGNORECASE)
        regex4_13 = re.compile(r"Signed by President",flags=re.IGNORECASE)
        regex4_14 = re.compile(r"Conferees appointed",flags=re.IGNORECASE)
        results4 = regex4.findall(bill_action)
        results_4 = regex_4.findall(bill_action)
        results4_4 = regex4_4.findall(bill_action)
        results4_5 = regex4_5.findall(bill_action)
        results4_6 = regex4_6.findall(bill_action)
        results4_7 = regex4_7.findall(bill_action)
        results4_8 = regex4_8.findall(bill_action)
        results4_9 = regex4_9.findall(bill_action)
        results4_10 = regex4_10.findall(bill_action)
        results4_11 = regex4_11.findall(bill_action)
        results4_12 = regex4_12.findall(bill_action)
        results4_13 = regex4_13.findall(bill_action)
        results4_14 = regex4_14.findall(bill_action)

        if results4 or results_4 or results4_4 or results4_5 or results4_6 or results4_7 or results4_8 or results4_9 or results4_10 or results4_11 or results4_12 or results4_13 or results4_14 or bill_value[3] == 1:
            bill_value[3] = 1
            continue

        regex3 = re.compile(r"Committee substitute agreed .+")
        regex_3 = re.compile(r"engrossed",flags=re.IGNORECASE)
        regex_31 = re.compile(r"Reported from", flags=re.IGNORECASE)
        regex_32 = re.compile(r"Rereferred from", flags= re.IGNORECASE)
        regex_33 = re.compile(r"Read second time", flags = re.IGNORECASE)
        regex_34 = re.compile(r"Constitutional reading dispensed", flags = re.IGNORECASE)
        regex_35 = re.compile(r"Committee amendment agreed to", flags = re.IGNORECASE)
        regex_36 = re.compile(r"Committee substitute agreed to", flags = re.IGNORECASE)
        regex_37 = re.compile(r"Engrossed", flags = re.IGNORECASE)
        regex_38 = re.compile(r"Taken up", flags = re.IGNORECASE)

        regex_39 = re.compile(r"Laid on Speaker", flags = re.IGNORECASE)

        regex_30 = re.compile(r"Discharged from", flags = re.IGNORECASE)

        results3 = regex3.findall(bill_action)
        results_3 = regex_3.findall(bill_action)
        results_31 = regex_31.findall(bill_action)
        results_32 = regex_32.findall(bill_action)
        results_33 = regex_33.findall(bill_action)
        results_34 = regex_34.findall(bill_action)
        results_35 = regex_35.findall(bill_action)
        results_36 = regex_36.findall(bill_action)
        results_37 = regex_37.findall(bill_action)
        results_38 = regex_38.findall(bill_action)
        results_39 = regex_39.findall(bill_action)
        results_30 = regex_30.findall(bill_action)

        if results3 or results_3 or results_31 or results_30 or results_39 or results_38 or results_37 or results_36 or results_35 or results_34 or results_33 or results_32 or bill_value[2] == 1:
		    bill_value[2] = 1
		    continue

        regex2 = re.compile(r"Subcommittee recommends")
        regex2_2 = re.compile(r"Left in")
        regex2_3 = re.compile(r"Continued to")
        results2 = regex2.findall(bill_action)
        results2_2 = regex2_2.findall(bill_action)
        results2_3 = regex2_3.findall(bill_action)

        if results2 or results2_2 or results2_3:
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
line += "bill_number, introduction date, primary sponsor, sponsor_id, introduced, action in committee, action beyond committee, passed chamber, becomes law, vetoed, veto overridden, significance"
output2.write(line + "\n")
for bill_IDS, final_bill in bill_objects.items():
    lines = ""
    lines += str(final_bill.bill_number) + "," + str(final_bill.date) + "," + str(final_bill.primary_sponsor.strip('"')) + "," +  str(final_bill.sponsors_ID) + "," + str(final_bill.stages[0]) + "," + str(final_bill.stages[1]) + "," + str(final_bill.stages[2]) + "," + str(final_bill.stages[3]) + "," + str(final_bill.stages[4]) + "," +  str(final_bill.veto) + "," + str(final_bill.overriden_veto) + "," + str(final_bill.significance) + ","
    output2.write(lines + "\n")

output2.close()





