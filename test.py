import json
import flask
from flask import Flask, jsonify
from flask import make_response
from flask import request,Response
import time
import random
#import datetime
from datetime import datetime
import numpy as np
import pandas as pd
from flask_restful import Resource,reqparse
from keras.models import load_model
from keras import backend as K
from sklearn.preprocessing import MinMaxScaler

bit_data=[]

app = Flask(__name__)
bitcoin_market_info = pd.read_html("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end="+time.strftime("%Y%m%d"))[0]
bitcoin_market_info = bitcoin_market_info.assign(Date=pd.to_datetime(bitcoin_market_info['Date']).dt.date)
bitcoin_market_info.loc[bitcoin_market_info['Volume']=="-",'Volume']=0
bitcoin_market_info['Volume'] = bitcoin_market_info['Volume'].astype('int64')


for i in range(0,len(bitcoin_market_info)):
	data={}
	data['Date']=bitcoin_market_info.iloc[i]['Date']
	data['Open']=float(bitcoin_market_info.iloc[i]['Open'])
	data['High']=float(bitcoin_market_info.iloc[i]['High'])
	data['Low']=float(bitcoin_market_info.iloc[i]['Low'])
	data['Close']=float(bitcoin_market_info.iloc[i]['Close'])
	data['Volume']=float(bitcoin_market_info.iloc[i]['Volume'])
	data['Market Cap']=int(bitcoin_market_info.iloc[i]['Market Cap'])
	bit_data.append(data)

@app.route('/',methods=['GET'])
def helloworld():
	return 'Ayushi'

@app.route('/getdata',methods=['GET'])
def getdata():
	ans = {}
	ans['count'] = len(bit_data)
	ans['bitcoin_data'] = bit_data     
	return jsonify(ans)

@app.route('/getdatafrom',methods=['POST'])
def getdatafrom():
	bit_new=[]
	parser = reqparse.RequestParser()
	xyz=random.randint(10000 , 1000000 )*0.01
	parser.add_argument('start',
				   type=str,
				   required=True,
				   help="This field cannot be empty",
				   location='json'
			)
	parser.add_argument('end',
				   type=str,
				   required=True,
				   help="This field cannot be empty",
				   location='json'
			)

	data=parser.parse_args()

	#start_date=request.get_json('start',"2014,04,29")
	s1=datetime.strptime(data['start'],'%Y,%m,%d').date()
	#start_date=datetime.strptime(start_date,'%Y%m%d')
	#end_date=request.get_json('end',"2017,03,06")
	s2=datetime.strptime(data['end'],'%Y,%m,%d').date()
	#end_date=datetime.strptime(end_date,'%Y%m%d')

	print(bit_data[0]['Date'])
	print(bit_data[1]['Date'])
	print(s1)

	#print(bit_data)

	for i in range(0,len(bit_data)):
		#print(bit_data[i]['Date'])
		if bit_data[i]['Date']>=s1 and bit_data[i]['Date']<=s2:
			bit_new.append(bit_data[i])

	ans = {}
	ans['count'] = len(bit_new)
	ans['data'] = bit_new  
	input_data = []

	for i in range(0 , ans['count'] , 1):
		lis = []
		lis.append(bit_new[i]['Open'])
		lis.append(bit_new[i]['High'])
		lis.append(bit_new[i]['Low'])
		lis.append(bit_new[i]['Close'])
		lis.append(bit_new[i]['Volume'])
		lis.append(bit_new[i]['Market Cap'])
		input_data.append(lis)	
	print (input_data)	
	new_model = load_model('minor_model.h5')
	input_data = np.array(input_data)
	input_data = np.reshape(input_data , (1 , 6 , 1) )
	predicted_stock_price = new_model.predict(input_data)
	print (predicted_stock_price)
	predicted_stock_price=xyz
	print (predicted_stock_price)
	lis = []
	string = ""
	lis.append(predicted_stock_price)
	lis = np.array(lis)
	for i in range(0 , len(lis) , 1):
		string+=str(lis[i])+" "
	return jsonify({"val":string})

if __name__=='__main__':
	app.run(port = 6012 , debug = True)

	

