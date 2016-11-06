from flask import render_template,request
from howWasYourDay import app
import json
from watson_developer_cloud import AlchemyLanguageV1
alchemy_language = AlchemyLanguageV1(api_key="cbef99146639642b05117516a24952154ed215ad")
@app.route('/')
@app.route("/form_hit", methods=['GET','POST'])
def form_hit():
	if request.method == 'GET':
		return render_template('index.html')

	if request.method == 'POST':
		rantText = request.form['rant_text']
		print(rantText)
		response_file = alchemy_language.emotion(text=rantText)
		print(rantText)
		anger = response_file['docEmotions']['fear']
		disgust = response_file['docEmotions']['disgust']
		fear = response_file['docEmotions']['fear']
		joy = response_file['docEmotions']['joy']
		sadness = response_file['docEmotions']['sadness']
		topEmotion = max(anger,disgust,fear,joy,sadness)
		botEmotion = min(anger,disgust,fear,joy,sadness)
		response = "test"
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
		print(rantText)

		return render_template('index1.html' , rant_text = rantText, response_text = response)
	
	
	
