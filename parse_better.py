'''
File to process the data in new csv
'''

import csv
import indicoio
import operator
from time import time

def cons():
	global personality 
	personality["conscientiousness"] += 1
	#print("in")

def ope():
	global personality
	personality["openness"] += 1
	#print("in")

def agr():
	global personality
	personality["agreeableness"] += 1
	#print("in")

def extra():
	global personality
	personality["extraversion"] += 1
	#print("in")


indicoio.config.api_key = 'a70776a16ea44fe661bbb0e2aaec1e12'
data = []
#print_count = 0
with open('uzair99__tweets.csv') as file:
	reader = csv.reader(file)

	count = 0

	
	for row in reader:
		if len(row) > 0:
			text = row[2][2:-1]
			print(text)
			if "https" in text:
				continue

			data.append(text)
			count +=1
		if count > 50:
			break
			

personality =  {'conscientiousness': 0, 'openness': 0, 'agreeableness': 0, 'extraversion':0} 
options = {'conscientiousness': cons, 'openness': ope, 'agreeableness': agr, 'extraversion':extra}
#print(count,len(data))
#print(data)
t0= time()
for i in data:
	#try:
	#print(i)
	mini_dic = indicoio.personality(i)
	#except indicoio.utils.errors.IndicoError:
	#continue
	#print(mini_dic)
	result = max(mini_dic.keys(), key=(lambda k: mini_dic[k]))
	if result in options:
		options[result]()
		#options.get(result, lambda: 'Invalid')()
	else:
		pass
print("Time taken to run: {} in ms.".format(time()-t0))
print(personality)
print("person is a {} person".format(max(personality.keys(), key=(lambda k: personality[k]))))

