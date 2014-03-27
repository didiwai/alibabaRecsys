import csv

def csvToTxt(csvname, txtname):
	with open(csvname, "rb") as readfile:
		reader = csv.reader(readfile)
		writefile = open(txtname, "w")
		for r in reader:
			if r[1] != "":
				templist = r[1].split('|')
				writefile.writelines(r[0] + "\t" + ','.join(templist) + "\n")




if __name__ == "__main__":
	csvToTxt("UserItemIntersectPopRecommend.csv", "UserItemIntersectPopRecommend.txt")