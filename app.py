from flask_cors import CORS, cross_origin

import pymysql
#from app import app
#from config import mysql

#from app import app
from flaskext.mysql import MySQL

from flask import jsonify, Flask, render_template, flash, request, redirect, url_for
import json

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter("ignore")

import itertools
import pandas as pd
import numpy as np
from datetime import datetime

#for modeling
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller

application = Flask(__name__)
#application = Flask(__name__, template_folder='../../frontend/src')
application.secret_key = "@##WDSA,xhfef1231223&*(((}}" #provide a secret key
CORS(application)

mysql = MySQL()
application.config['MYSQL_DATABASE_USER'] = 'rentalDBTe' #database user
application.config['MYSQL_DATABASE_PASSWORD'] = 'Mgty89!#H0' #put password for the database
application.config['MYSQL_DATABASE_DB'] = 'rental_csv' #database name
application.config['MYSQL_DATABASE_HOST'] = 'database-1.crxlpbknnu4o.ca-central-1.rds.amazonaws.com' #host name
mysql.init_app(application)


#app = Flask(__name__)
#app.secret_key = "@##WDSA,xhfef1231223&*(((}}"

def list_create(SQL):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(SQL)
        empRows = cursor.fetchall()
        labels = []
        data = []
        
    except Exception as e:
        print(e)
        
    finally:
        cursor.close() 
        conn.close()
        
    for i in empRows[0].keys():
        if isinstance(empRows[0][i], float) == True and empRows[0][i]!=0:
            labels.append(i)
            data.append(empRows[0][i])
    return labels, data

def get_average(labels_av, data_av):
    years = ['2017', '2018', '2019']
    data = [0, 0, 0]
    count = [0, 0, 0]
    for i in labels_av:
        if '2017' in i:
            index = labels_av.index(i)
            data[0]+=data_av[index]
            count[0]=count[0]+1
        elif '2018' in i:
            index = labels_av.index(i)
            data[1]+=data_av[index]
            count[1]=count[1]+1
        elif '2019' in i:
            index = labels_av.index(i)
            data[2]+=data_av[index]
            count[2]=count[2]+1
    for i in range(3):
        data[i] = round(data[i]/count[i],2)
    return years, data

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month
    
def get_prediction(dates, price, d1, d2):
    message = ""
    boxes = {'Date': dates,
         'Price': price
        }

    df = pd.DataFrame(boxes, columns= ['Date','Price'])
    fit1 = sm.tsa.statespace.SARIMAX(df['Price'], order=(1,1,1),seasonal_order=(0,0,0,0)).fit()
    d1 = datetime. strptime(d1, '%Y-%m-%d') #current date
    d2 = datetime.strptime(d2, '%Y-%m-%d') 
    if d1.year<int(dates[0][0:4]) or (d1.year==int(dates[0][0:4]) and d1.month<2):
        message = message + "The selected date is earlier than the first date the dataset contains. Please select a date after " + dates[0][-3:] +", "+dates[0][0:4]
        return "Can not be predicted", message 
    if d1.year < d2.year or (d1.year == d2.year and d1.month < d2.month):
        message = message + "The selected date already exists within the dataset. Please select a date after December, 2019 for rent prediction and March, 2020 for price prediction. The returned value for your selected date is an actual value from the dataset."
        month = d1.strftime("%B")
        for index, i in enumerate(dates):
            if str(d1.year) in i and i[-3:] in month:
                return price[index], message
    diff = diff_month(d1, d2)
    predictions = fit1.predict(start=len(dates),end=len(dates)+diff)
    intPredict = int(predictions[len(dates)+diff])
    if intPredict == 0:
        message = message+"The date is within the range of start date and end date of the dataset but it does not have a value."
    
    return intPredict, message

@application.route('/')
def home():
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `one_bed` WHERE `RegionName` = 'New York'"
    labels_ny, data_ny = list_create(SQL)
    
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `one_bed` WHERE `RegionName` = 'Los Angeles'"
    labels_la, data_la = list_create(SQL)
    
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `one_bed` WHERE `RegionName` = 'Chicago'"
    labels_cg, data_cg = list_create(SQL)
    #labels = ["2013", "2014", "2014", "2015", "2016", "2010"]
    #data = [10, 19, 3, 5, 2, 3]
    return render_template("index.html", data_ny=data_ny, labels_ny=labels_ny, data_la=data_la, labels_la=labels_la,
    data_cg=data_cg, labels_cg=labels_cg)


@application.route('/charts')
def charts():
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `one_bed` WHERE `RegionName` = 'New York'"
    labels_ny, data_ny = list_create(SQL)
    
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `one_bed` WHERE `RegionName` = 'Los Angeles'"
    labels_la, data_la = list_create(SQL)
    
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `one_bed` WHERE `RegionName` = 'Chicago'"
    labels_cg, data_cg = list_create(SQL)
    
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `two_bed` WHERE `RegionName` = 'New York'"
    labels_ny_2, data_ny_2 = list_create(SQL)
    
    SQL = "SELECT * FROM `two_bed` WHERE `RegionName` = 'New York'"
    labels_ny_2_avg, data_ny_2_avg = list_create(SQL)
    labels_ny_2_avg, data_ny_2_avg = get_average(labels_ny_2_avg, data_ny_2_avg)
    
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `two_bed` WHERE `RegionName` = 'Los Angeles'"
    labels_la_2, data_la_2 = list_create(SQL)
    labels_la_2_avg, data_la_2_avg = get_average(labels_la_2, data_la_2)
    
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `two_bed` WHERE `RegionName` = 'Chicago'"
    labels_cg_2, data_cg_2 = list_create(SQL)
    #labels = ["2013", "2014", "2014", "2015", "2016", "2010"]
    #data = [10, 19, 3, 5, 2, 3]
    return render_template("chartjs.html", data_ny=data_ny, labels_ny=labels_ny, data_la=data_la,
    data_cg=data_cg, labels_ny_2=labels_ny_2, data_ny_2=data_ny_2, labels_ny_2_avg = labels_ny_2_avg, 
    data_ny_2_avg = data_ny_2_avg, data_la_2 = data_la_2, data_cg_2 = data_cg_2,
    data_la_2_avg = data_la_2_avg)


@application.route('/charts_price')
def charts_price():
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `one_bed_price` WHERE `RegionName` = 'New York'"
    labels_ny, data_ny = list_create(SQL)
    
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `one_bed_price` WHERE `RegionName` = 'Los Angeles'"
    labels_la, data_la = list_create(SQL)
    
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `one_bed_price` WHERE `RegionName` = 'Chicago'"
    labels_cg, data_cg = list_create(SQL)
    
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `two_bed_price` WHERE `RegionName` = 'New York'"
    labels_ny_2, data_ny_2 = list_create(SQL)
    
    SQL = "SELECT * FROM `two_bed_price` WHERE `RegionName` = 'New York'"
    labels_ny_2_avg, data_ny_2_avg = list_create(SQL)
    labels_ny_2_avg, data_ny_2_avg = get_average(labels_ny_2_avg, data_ny_2_avg)
    
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `two_bed_price` WHERE `RegionName` = 'Los Angeles'"
    labels_la_2, data_la_2 = list_create(SQL)
    labels_la_2_avg, data_la_2_avg = get_average(labels_la_2, data_la_2)
    
    SQL = "SELECT 2011Oct, 2012Oct, 2013Oct, 2014Oct, 2015Oct, 2016Oct, 2017Oct, 2018Oct, 2019Oct FROM `two_bed_price` WHERE `RegionName` = 'Chicago'"
    labels_cg_2, data_cg_2 = list_create(SQL)
    #labels = ["2013", "2014", "2014", "2015", "2016", "2010"]
    #data = [10, 19, 3, 5, 2, 3]
    return render_template("chartjs-price.html", data_ny=data_ny, labels_ny=labels_ny, data_la=data_la,
    data_cg=data_cg, labels_ny_2=labels_ny_2, data_ny_2=data_ny_2, labels_ny_2_avg = labels_ny_2_avg, 
    data_ny_2_avg = data_ny_2_avg, data_la_2 = data_la_2, data_cg_2 = data_cg_2,
    data_la_2_avg = data_la_2_avg)
    
@application.route('/powerbi')
def powerbi():
    return render_template("powerBI.html")
    
@application.route('/price', methods=['GET', 'POST'])
def price():
    errors = []
    dataset_name = ""
    if request.method == 'POST':
         rent = request.form['rentPrice']
         if rent=="rent":
             dataset_name = dataset_name
         elif rent=="price":
             dataset_name = dataset_name+"_price"
             print(dataset_name)
             
         apartment = request.form['apartment']
         dataset_name = apartment + "_bed"+dataset_name
         
         regionName = request.form['username']
         SQL = "SELECT * FROM `"+dataset_name+"` WHERE `RegionName` = '"+str(regionName)+"'"
         dates, price = list_create(SQL)
         cdate = request.form['bdate']
         if rent=="price":
             odate = '2020-03-31'
         elif rent=="rent":
             odate = '2019-12-31'
         predicted, message = get_prediction(dates, price, cdate, odate)
         cdate = datetime.strptime(cdate, '%Y-%m-%d')
         month = cdate.strftime("%B")
         year = cdate.year
         
         return render_template("price.html", rent = rent, apartment = apartment, regionName = regionName, predicted = predicted, year = year, month = month, message = message)
    else:
        return render_template("price.html")

@application.route('/documents')
def documents():
    return render_template("doc.html")

@application.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

@application.errorhandler(400)
def showMessage(error=None):
    message = {
        'status': 400,
        'message': 'Please select the appropriate fields: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 400
    return render_template("price.html")
        
if __name__ == "__main__":
    application.run()
