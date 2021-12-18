import numpy as np
import pandas as pd
import pickle

import datetime
from flask import Flask, render_template, request


app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


@app.route("/")
def home():
    return render_template ("index.html")

@app.route('/predict',methods=['POST'])
def predict():
    # For rendering results on HTML GUI 
    if request.method == "POST":

        trainNo = int(request.form["train_no"])
        
        date_str = str(request.form["date"])
        format_str = '%Y-%m-%d'
        datetime_obj = datetime.datetime.strptime(date_str, format_str)
        
        day = datetime_obj.weekday() + 1
        
        dataset = pd.read_csv('unique.csv')

        ind = 0
        l=[]
        flag=False
        trainName=""
        for i in dataset["TrainNo"]:
            if i == trainNo:
                flag=True
                if dataset["Day"][ind] == day:
                    t,dist,region = dataset["Type"][ind],dataset["Distance"][ind],dataset["Region"][ind]
                    trainName = dataset["TrainName"][ind]
                    l.append(t)
                    l.append(dist)
                    l.append(region)
                    l.append(day)
                    break
            ind += 1
        if flag and len(l)==0:
            message = "Train does not run on the given date"
        elif flag==False:
            message = "Train Not Found"
        else :            
            final_features = [l]

            predictedTime = int(model.predict(final_features))

            time=""
            if predictedTime >=60:
                hrs = str(int(predictedTime/60))
                mins = int(predictedTime%60)
                if mins==0:
                    time = hrs + " hrs "
                else:
                    time = hrs + " hrs " + str(mins) + " mins" 

            elif predictedTime<0:
                message = "Your train is arriving on time"

            else :
                time = str(predictedTime) + " mins"
            message = trainName + " (" + str(trainNo) + ") will be " + time + " late." + "\n Sorry for the inconivence."
    

        return render_template ("predict.html",msg = message)



if __name__ == "__main__":
    app.run()