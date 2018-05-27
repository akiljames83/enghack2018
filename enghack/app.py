import os
from final_script import *
import time
from flask import Flask, render_template, request
import csv

push = []
photos = [0,1,2,3]

def generateData(personality):
    global push
    with open("{}.csv".format(personality),'r') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            if count == 0:
                count +=1
                continue
            event, pers, typ, desc, date, image= row[0], row[1], row[2], row[3], str(row[4])+' '+str(row[5])+' '+str(row[6]), photos[count-1]
            count += 1
            _in = (event,pers,typ,desc,date,image)
            push.append(_in)
            if count == 5:
                break
            
        return push
        
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template ("index.html")
    
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method=="POST": 
        personality = main_func(request.form["twittername"])
        data = generateData(personality)
        return render_template ("results.html", personality=personality, data=data)
        
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))