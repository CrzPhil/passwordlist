
'''
	User can enter Keywords, from which a passwordlist will be generated with common combinations.
	Add Upper & Lowercase concatenations
	Add number combinations
'''

# Input Keywords:

incoming = True
keywords = [] 
outlist = []
testlist = ['one', 'two', 'three', 'four', 'five', 'password']

outname = input("[+] Enter name of your output file: ")

name = input("[+] Add the Target's first name: ")
lastname = input("[+] Add the Target's last name: ")
birthdate = input("[+] Add the Target's birthdate (DDMMYYYY): ")

while len(birthdate) != 8:
	birthdate = input("Please add exactly eight digits: ")

while incoming:
	keyword = input("Add a keyword: ")
	if keyword != "q":
		keywords.append(keyword)
		print("\nAdded " + keyword + " to the list.")
		print("\nIf you're done type 'q'\n")
	else:
		incoming = False

print("Your queries are: ")
print(keywords)
keywords.append(name)
keywords.append(lastname)

# Load PresetFile:

with open("presetlist.txt") as f:
	prelist = f.read().splitlines()

# Create Combos:

for i in keywords:
	outlist.append(i)


def preparedate(date):		# Slices up the date into nice feasible password appendages
	out = [date, date[-4:], date[-2:]]

	if date[0] == "0":
		if date[2] == "0":
			slice1 = date[1]+date[3:]  # 01032002 --> 132002
			out.append(slice1)
		else:
			slice2 = date[1:]  # 01102002 --> 1102002
			out.append(slice2)

	if date[6] == "0":
		slice2 = date[0:6]+date[7]
		out.append(slice2)

	return out


def datescramble(inlist):		# Appends the date-slices prepared in preparedate() to the keywords
	out = []
	for i in inlist:
		dateslice = preparedate(birthdate)[1]
		otherslice = preparedate(birthdate)[2]
		mid = i + dateslice
		other = i + otherslice
		out.append(mid)
		out.append(other)
		rev = dateslice + i
		revother = otherslice + i
		out.append(rev)
		out.append(revother)
		if len(preparedate(birthdate)) >= 3:
			out.append(i + preparedate(birthdate)[3])
			out.append(preparedate(birthdate)[3] + i)
			if len(preparedate(birthdate)) > 3:
				out.append(i + preparedate(birthdate)[4])
				out.append(preparedate(birthdate)[4] + i)
	return out


def scramble(inlist):		# Concatenates all keywords with each other
	out = []
	for i in range(len(inlist)):
		for j in range(len(inlist)):
			if inlist[i] != inlist[j] and inlist[i] != inlist[j].upper() and inlist[i] != inlist[j].lower():
				if inlist[i] != inlist[i].lower() and inlist[j] != inlist[j].lower():
					mid = inlist[i] + inlist[j]
					out.append(mid)
				mid = inlist[i].lower()+inlist[j].lower()
				out.append(mid)
				mid = inlist[i].upper()+inlist[j].upper()
				out.append(mid)
	return out


def unify(inlist):		# Concatenates the elements of our preset list with the keywords- Front and Back
	out = []
	for i in inlist:
		for j in prelist:
			x = j + i
			y = i + j
			out.append(x)
			out.append(y)
	return out


def cases(inlist):		# Sets the first character of each word to Uppercase
	for m in range(len(inlist)):
		inlist[m] = inlist[m][0].upper() + inlist[m][1:]
	return inlist


output = scramble(keywords)
for i in unify(keywords):
	output.append(i)
print("[+] Unifying keywords . . .")

for i in cases(keywords):
	output.append(i)
print("[+] Tuning case-sensitivity . . .")

preparedate(birthdate)
for i in datescramble(output):
	output.append(i)
print("[+] Finishing wordlist . . .")

# Generate & Write to File:
file = open(outname, "a")
for i in output:
	file.write(i)
	file.write("\n")
file.close()
