'''
Author: Akil Hamilton
Submit this one!

'''
import csv
import indicoio
import threading
import datetime

now = datetime.datetime.now()
small_list = []
bigger_list = []
event_names = []

indicoio.config.api_key = ''

with open('events.csv') as file:
	reader = csv.reader(file)

	count = 0

	
	for row in reader:
		if count == 0:
			count += 1
			continue
		#print(event_names)
		if len(row) > 0:
			category = row[5].replace('<p>', "").replace('</p>',"").replace("&quot","")
			description = row[7].replace('<p>', "").replace('</p>',"").replace("&quot","")
			name = row[13].replace('<p>', "").replace('</p>',"").replace("&quot","")
			date = row[2]
			date = date[:10]
			dateArr = date.split("/")
			#print(dateArr)
			Month = int(dateArr[0])
			Day = int(dateArr[1])
			Year = int(dateArr[2])
			Date = (Day, Month, Year)
			if not(Year>= now.year and Month>=now.month and Day>=now.day):
				continue
			try:
				small_list.append(name)
				small_list.append(category)
				small_list.append(description)
				small_list.append(Date)
				#print(name)

				if count != 0:
					if name in event_names:
						small_list = []
						pass
					else:
						event_names.append(name)
						bigger_list.append(small_list)
						small_list = []
				else:
					bigger_list.append(small_list)
					event_names.append(name)
					small_list = []

				count +=1

			except UnicodeEncodeError:
				pass

		if count > 600:
			break

processed =[]
for el in bigger_list:
	try:
		#print("THIS IS ITTTTT '" +str(el[2]) + "'")
		if el[2] == '':
			continue 
		mini_dic = indicoio.personality(str(el[2]))
		result = max(mini_dic.keys(), key=(lambda k: mini_dic[k]))
		#el.append[result]
		# eventName, emotion, type of event, description, date tuple(day month year)
		# index 0, 1, 2, 3, 4[0], 4[1], 4[2]
		_in = (el[0], result, el[1], el[2], el[3])
		# pairs.append(el[0])
		processed.append(_in)
		print(_in,'\n')
	except UnicodeEncodeError:
				pass

print(len(processed))

def createCSV():
	global processed, coae
	name = coae[-1]
	coae = coae[:-1]
	label = name + ".csv"
	with open(label,'w',newline = '') as f:
		thewriter = csv.writer(f)
		thewriter.writerow(["Event Name", "Personality Type", "Type of Event", "Description","Day","Month","Year"])
		for row in processed:
			if row[1] == name:
				thewriter.writerow([row[0],row[1],row[2],row[3],row[4][0], row[4][1], row[4][2]])

c = "conscientiousness"
o = "openness"
a = "agreeableness"
e = "extraversion"
coae = ["conscientiousness","openness","agreeableness","extraversion"]
t1 = threading.Thread(name='con', target=createCSV)
t2 = threading.Thread(name='open', target=createCSV)
t3 = threading.Thread(name='agre', target=createCSV)
t4 = threading.Thread(name='extra', target=createCSV)

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()
		