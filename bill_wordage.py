__author__ = 'Winston Frick & Peter Cybriwsky'
# This snippet gets the final verdict of a bill in gettting passed or not
file = open("va_bill_actions.csv")
file2 = open("final_bill_wordage.txt","w")
bill = 0
print(file.readline())

output = ""
for line in file:
	attributes = line.split(",")
	current_bill = attributes[3]
	if current_bill != bill:
		file2.write(output + "\n")
	output = attributes[5] + " " + attributes[6]
	bill = current_bill

file2.close()