from flask import render_template
from howWasYourDay import app
import json
from watson_developer_cloud import AlchemyLanguageV1
@app.route('/')
@app.route('/index')
#@app.route('from_hit',methods=['METH'])
def index():
	print('Hello!')
	return render_template("index.html")
#def form_handle():
#	alchemy_language - AlchemyLanguageV1(api_key="key")
#	rantText = request.form['rant_text']
#	responseText = request.form['response_text']
#	respone_file = alchemy_language.emotion(text=rantText)
#	return 'Hello!'
	
	

