# parsing the csv file

import csv
import indicoio
import operator
indicoio.config.api_key = ''
data = []
print_count = 0
with open('realDonaldTrump_tweets.csv') as file:
	reader = csv.reader(file)

	count = 0


	for row in reader:
		if len(row) > 0:
			text = row[2][2:-1]
			#print(text)

			data.append(text)
			count +=1
			
		

		if count > 8:
			break

personality =  {'conscientiousness': 0, 'openness': 0, 'agreeableness': 0, 'extraversion':0} 
options = {'conscientiousness': cons, 'openness': ope, 'agreeableness': agr, 'extraversion':extra} 
for i in data:
	mini_dic = indicoio.personality(i)
 	#result = max(mini_dic)
 	if result in options:
 		options[result]()
    else:
    	pass
	#print('\n')
	print_count += 1

	if print_count > 5:
		break

print("Trump is a {} person".format(max(personality)))
		
def cons():
	global personality 
	personality["conscientiousness"] += 1

def ope():
	global personality
	personality["openness"] += 1

def agr():
	global personality
	personality["agreeableness"] += 1

def extra():
	global personality
	personality["extraversion"] += 1
























