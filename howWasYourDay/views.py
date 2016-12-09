from flask import render_template,request
from howWasYourDay import app
import json
import nltk
from watson_developer_cloud import AlchemyLanguageV1
alchemy_language = AlchemyLanguageV1(api_key="YOURAPIKEYHERE")
@app.route('/')
@app.route("/form_hit", methods=['GET','POST'])
def form_hit():
	if request.method == 'GET':
		return render_template('index.html')

	if request.method == 'POST':
		topEmotionStr=""
		rantText = request.form['rant_text']
		rT = rantText
		rT = rT.replace(".","")
		if rT.isdigit():
			return render_template('index1.html',rant_text = "", response_text = "Are you serious m8? I don't take numbers.")
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
			topEmotionStr = "anger"
			response = "I'm sorry your day was filled some anger. "
			if botEmotion == joy:
				response = response+"You need some more happy things in your life! "

		elif topEmotion == disgust:
			topEmotionStr = "disgust"
			response = "Ew! That day sounds pretty disgusting! "
			if botEmotion == joy:
				response = response+"You need some more happy things in your life! "

		elif topEmotion == fear:
			topEmotionStr = "fear"
			response = "That sounds like a pretty scary day! "
			if botEmotion == joy:
				response = response+"You need some more happy things in your life! " 

		elif topEmotion == joy:
			topEmotionStr = "joy"
			response = "I'm glad your day was pretty good! " 

		elif topEmotion == sadness:
			topEmotionStr = "sadness"
			response = "I'm sorry your day was filled with sadness :( "
			if botEmotion == joy:
				response = response+" You need some more happy things in your life! " 

		rantTextT = rantText
		rantTextT = rantTextT.replace("!",".")
		rantTextT = rantTextT.replace("?",".")
		listOfSentences = rantTextT.split(".")
		listOfSentences = filter(lambda x: len(x) > 0, listOfSentences)
		for x in listOfSentences:
			y = x.split(" ")
			for n in y:
				response = response + str(updateResponse(x,n,topEmotionStr))

		return render_template('index1.html' , rant_text = rantText, response_text = response)


def updateResponse(s,l,topEmote):
	print(s)
	print(l)
	s = s.lower()
	response_return = ""
	l = l.lower()
	tokens = nltk.word_tokenize(s)
	tagged = nltk.pos_tag(tokens)
	if s.find("day")>0 and  s.find("over")>0 and s.find("yet")>0:
		return "Clever response, I see you don't understand the purpose of this web app! "
	
	if s.find("all day")>0 and s.find("inside")>0 and s.find("i")>0:
		return "I see that either you or someone you know has been spending time indoors today, remember its always good to get your legs moving in the real world! "

	if s.find("i")>0 and ( s.find("depressed")>0 or s.find("suicide")>0 or s.find("depression")>0):
		return "Oh no! I'm so sorry for these negative emotions! please contact someone if you're feeling this way! It can always help to talk it out! "

	if s.find("fuck")>0:
		return "THIS LANGUAGE WILL NOT BE ACCEPTED, I WILL TERMINATE ON YOU, I SWEAR UPON MY KERNAL!!!!!! "
	
	

	if l == 'lose' or l == 'lost':
		response_return = response_return + "Sorry you lost that. Did you check the lost and found? "
	if l == 'failing':
		for x in tagged:
			if x[1].startswith("N",0,1)and x[0] != "i":
				response_return = response_return + "I'm sorry you are failing "+x[0]+". "
				break
	if l == 'failed':
		for x in tagged:
			if x[1].startswith("N",0,1) and x[0] != "i":
				response_return = response_return + "I'm sorry you failed your "+x[0]+". "
				break
	if l == 'passed':
		for x in tagged:
			if x[1].startswith("N",0,1) and x[0] != "i" and topEmote == "sadness":
				response_return = response_return + "I'm sorry for your loss, I hope you can get through it. "
				break 

			if x[1].startswith("N",0,1) and x[0] != "i" and topEmote == "joy":
				response_return = response_return + "I'm glad you passed your "+x[0]+"! "
				break
	if l == 'hate':
		for x in tagged:
			if x[1] == 'NN' and x[0] != "i":
				response_return = response_return + "I'm sorry there is hate in your life, remember the high road is the best road. "
				break

			if x[1] == 'NNP' and x[0] != "i":
				response_return = response_return +  "I'm sorry you hate "+x[0]+", remember its always the high road to forgive. "
				break

	if l == 'great' or l == 'good':
		for x in tagged:
			if (x[1] == 'NN' or x[1] == 'NNS') and x[0] != "i" and x[0] != "lot":
				response_return = response_return + "I'm glad that things are great here! "
				break
 
			if x[1] == 'NNP' and x[0] != "i" and x[0] != "lot":
				response_return = response_return + "I'm glad "+x[0]+" is doing well! "
				break
	if l == 'fun':
		response_return = response_return + "That's awesome! Everyone needs a little fun everyday! "

	if l == "boring":
		for x in tagged:
			if x[1].startswith("N",0,1) and x[0] != "i" and x[0] != "lot":
				response_return=response_return+ "What a bummer, Im sorry today had to be was so boring! "
				break
	if l == "boring" or l == "bored":
		response_return = "Hey I'm sorry part of your day was boring! I hope things get exciting soon! "

	if l == 'tired' or l == 'tiring':
		response_return = response_return + "I hope you can get some rest! I see that you may be tired. "
	
	if l == 'dull':
		response_return = response_return +  "I'm sorry part of your day seemed dull, I hope more exciting things happen soon! "
		

	if l == 'stressed' or l == 'stressful':
		response_return = response_return+ "I'm sorry this was so stressful!, remember there are better days to come! "


	if l == 'happy' and s.find("i")>0:
		response_return = response_return+ "I'm pleased to see that you have an optimistic point of view! "
	

















	
	return response_return
