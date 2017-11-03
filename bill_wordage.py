__author__ = 'Winston Frick & Peter Cybriwsky'
# This snippet gets the final verdict of a bill in gettting passed or not
file = open("va_bill_actions.csv", "r")
file2 = open("final_bill_wordage.txt", "w")
file3 = open("va_bill_sponsors.csv", "r")
file4 = open("va_legislators.csv", "r")
totalbills = open("legislator_counts.txt", "w")
bill = 0
print(file.readline())
legislators = {}
IDs = []

output = ""
for line in file:
    attributes = line.split(",")
    current_bill = attributes[3]
    if current_bill != bill:
        file2.write(output + "\n")
    output = attributes[5] + " " + attributes[6]
    bill = current_bill

for line in file4:
    attributes = line.split(",")
    legislators[attributes[0]] = 0
    IDs.append(attributes[0])

print(IDs)

for line in file3:
    attributes = line.strip().split(",")
    bill = attributes[3]
    sponsor = attributes[5]
    if sponsor in legislators.keys():
        legislators[sponsor] += 1

for k, v in legislators.items():
    print(k, v)

print(legislators)

file2.close()
