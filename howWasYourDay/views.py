from flask import render_template,request
from howWasYourDay import app
import json
import nltk
from watson_developer_cloud import AlchemyLanguageV1
alchemy_language = AlchemyLanguageV1(api_key="cbef99146639642b05117516a24952154ed215ad")
@app.route('/')
@app.route("/form_hit", methods=['GET','POST'])
def form_hit():
	if request.method == 'GET':
		return render_template('index.html')

	if request.method == 'POST':
		rantText = request.form['rant_text']
		response_file = alchemy_language.emotion(text=rantText)
		anger = response_file['docEmotions']['fear']
		disgust = response_file['docEmotions']['disgust']
		fear = response_file['docEmotions']['fear']
		joy = response_file['docEmotions']['joy']
		sadness = response_file['docEmotions']['sadness']
		topEmotion = max(anger,disgust,fear,joy,sadness)
		botEmotion = min(anger,disgust,fear,joy,sadness)
		response = ""
		if topEmotion == anger:
			response = "I'm sorry your day was filled some anger."
			if botEmotion == joy:
				response = response+" You need some more happy things in your life!"

		if topEmotion == disgust:
			response = "Ew! That day sounds pretty disgusting!"
			if botEmotion == joy:
				response = response+" You need some more happy things in your life!"

		if topEmotion == fear:
			response = "That sounds like a pretty scary day!"
			if botEmotion == joy:
				response = response+" You need some more happy things in your life!"

		if topEmotion == joy:
			response = "I'm glad your day was pretty good!"

		if topEmotion == sadness:
			response = "I'm sorry your day was filled with sadness :("
			if botEmotion == joy:
				response = response+" You need some more happy things in your life!"

		rantTextT = rantText
		rantTextT = rantTextT.replace("!",".")
		rantTextT = rantTextT.replace("?",".")
		listOfSentences = rantTextT.split(".")
		listOfSentences = filter(lambda x: len(x) > 0, listOfSentences)
		for x in listOfSentences:
			y = x.split(" ")
			for n in y:
				response = response + str(updateResponse(x,n))

		return render_template('index1.html' , rant_text = rantText, response_text = response)


def updateResponse(s,l):
	print(s)
	print(l)
	tokens = nltk.word_tokenize(s)
	tagged = nltk.pos_tag(tokens)
	if l == 'lose' or l == 'lost':
		for x in tagged:
			print(x)
			if x[1].startswith("N",0,1):
				print(x[1])
				return " I'm sorry you lost your "+x[0]+"."
	if l == 'failing':
		for x in tagged:
			if x[1].startswith("N",0,1):
				return " I'm sorry you are failing your "+x[0]+"."
	if l == 'failed':
		for x in tagged:
			if x[1].startswith("N",0,1):
				return " I'm sorry you failed your "+x[0]+"."
	if l == 'passed':
		for x in tagged:
			if x[1].startswith("N",0,1):
				return " I'm glad you passed your "+x[0]++"!"
	if l == 'hate':
		for x in tagged:
			if x[1] == 'NN':
				return " I'm sorry you hate your "+x[0]+"."
			if x[1] == 'NNP':
				return " I'm sorry you hate "+x[0]+"."

	if l == 'good' or l == 'well' or l == 'great':
		for x in tagged:
			if x[1] == 'NN' or x[1] == 'NNS':
				return " I'm glad your "+x[0]+" went well!"
			if x[1] == 'NNP':
				return " I'm glad "+x[0]+" is doing well!"
	return ""
