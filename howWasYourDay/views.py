from flask import render_template
from howWasYourDay import app
import json
from watson_developer_cloud import AlchemyLanguageV1
alchemy_language = AlchemyLanguageV1(api_key="cbef99146639642b05117516a24952154ed215ad")

@app.route('/')
@app.route('/index')
#@app.route('from_hit',methods=['METH'])
def index():
	return render_template("index.html")

def form_handle():
	rantText = request.form['rant_text']
	respone_file = alchemy_language.emotion(text=rantText)
	anger = response_file['docEmotions']['fear']
	disgust = response_file['docEmotions']['disgust']
	fear = response_file['docEmotions']['fear']
	joy = response_file['docEmotions']['joy']
	sadness = response_file['docEmotions']['sadness']
	topEmotion = max(anger,disgust,fear,joy,sadness)
	botEmotion = min(anger,disgust,fear,joy,sadness)
	response = ""
	if topEmotion == anger:
		response = "I'm sorry your day was filled some anger"

	if topEmotion == disgust:
		response = "Ew! That day sounds pretty disgusting!"
	
	if topEmotion == fear:
		response = "That sounds like a pretty scary day!"

	if topEmotion == joy:
		response = "I'm glad your day was pretty good!" 
	
	if topEmotion == sadness:
		response = "I'm sorry your day was filled with sadness :("

	
	
	
	

