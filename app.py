import numpy as np
import pandas as pd
import pickle

import datetime
from flask import Flask, url_for, redirect, jsonify, request,render_template


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
        trainName=""
        for i in dataset["TrainNo"]:
            if i == trainNo and dataset["Day"][ind] == day:
                t,dist,region = dataset["Type"][ind],dataset["Distance"][ind],dataset["Region"][ind]
                trainName = dataset["TrainName"][ind]
                l.append(t)
                l.append(dist)
                l.append(region)
                l.append(day)
                break
            ind += 1


        if len(l)==0:
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
            else:
                time = str(predictedTime) + " mins"
            message = trainName + " (" + str(trainNo) + ") will be " + time + " late." + "\n Sorry for the inconivence."

        return render_template ("predict.html",msg = message,t=predictedTime,tm = time)







  
    
    # final_features = [np.array(int_features)]

    # return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)