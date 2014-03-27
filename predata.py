import csv

def predata():
	with open("predata.csv", "wb") as f:
		writer = csv.writer(f)
		with open("t_alibaba_data.csv", "rb") as csvfile:
			spamreader = csv.reader(csvfile)
			header = 1
			for row in spamreader:
				if header == 1:
					print "throw header"
					header += 1
				else:
					writer.writerow([row[0], row[1], row[2], row[3][0]])
					

def decomFour():
	with open("oneToSeven.csv", "wb") as ft:
		writert = csv.writer(ft)
		with open("eight.csv", "wb") as f:
			writer = csv.writer(f)
			with open("predata.csv", "rb") as csvfile:
				reader = csv.reader(csvfile)
				for row in reader:
					if int(row[3]) == 8:
						writer.writerow(row)
					else:
						writert.writerow(row)

def decomThree():
	with open("oneToSix.csv", "wb") as ft:
		writert = csv.writer(ft)
		with open("sevenToEight.csv", "wb") as f:
			writer = csv.writer(f)
			with open("predata.csv", "rb") as csvfile:
				reader = csv.reader(csvfile)
				for row in reader:
					if (int(row[3]) == 8) or (int(row[3]) == 7):
						writer.writerow(row)
					else:
						writert.writerow(row)
				



#def createTestFile():



if __name__ == "__main__":
	print "Run...."
	#predata()
	decomThree()
	#decomFour()