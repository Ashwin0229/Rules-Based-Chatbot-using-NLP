'''
Name   : Ashwin Sai C
Course : NLP - CS6320-001
Title  : Project 1b : Chatbot
Term   : Spring 2024

'''

from   autocorrect import Speller
import os
import re
import pickle
import nltk
from   nltk.util import ngrams
from   nltk.corpus import stopwords
from   nltk.stem   import WordNetLemmatizer
from   nltk.corpus import wordnet
import Levenshtein
from   nltk.chunk import ne_chunk
from   sklearn.feature_extraction.text import TfidfVectorizer
from   sklearn.metrics.pairwise import cosine_similarity
from   nltk.sentiment import SentimentIntensityAnalyzer
import random

bot_name          = "BlackBot"
spell             = Speller(lang='en')
stop_words        = set(stopwords.words('english'))
sia_handle        = SentimentIntensityAnalyzer()
positive_comments = ["Thats wonderful!", "Reallyy great!", "Wow, thats cool!", "Awe struck! I am happyyy."]
negative_comments = ["Ah dont worry!", "You will like it as time progresses", "I got it, Astronomy is not for everyone!", "I will teach you, dont worry!"]
neutral_comments  = ["OK", "Its a tie, balance between both", "Not positive nor negative!"]

def Response_Parsing(user_response,knowledge_base_data,user):
	'''
		parameters  : user_response, knowledge_base_data, user 
		Description : This function is used to compare the user response with standard questions
					  and if no match is found, it parses the user response and performs NLP 
					  techniques and returns the best fit response

		return      : model response
	'''
	user_data        = Load_User_Model(user)
	response_list    = []
	user_response    = user_response.lower().replace("blackhole","black hole")
	response_output  = "" 
	random_greeting  = ["Howdyy!","Good day!","Yo man!", "Good day ladies and gentlemen!", "Welcome to Space!"]

	if "hey" in user_response.split(" ") or "greetings" in user_response.split(" ") or "hi" in user_response.split(" ") or "whats up" in user_response.split(" "):
		response_output += str(random_greeting[random.randint(0,4)])
		response_output += "\nHey!! I am "+bot_name

	elif ("who am i" in user_response.lower()) or ("what is my name" in user_response.lower()) :
		response_output += "How can I forget "+user+", ;)"
		
	elif "what is your name" in user_response or "can you tell me your name" in user_response:
		response_output += "My name is "+bot_name

	elif "my name is" in user_response:
		response_output += "Ofcourse! I know you. (See the chat name)"

	elif "about me" in user_response or Cosine_Simmilarity_Function("what do you know about me", user_response) >= 0.25:
		response_output += "\nYour name is "+user_data['Name']
		response_output += "You like "+user_data['FavColor'].replace("\n","")+" color right?"
		response_output += "You stay in "+user_data['Location']
		response_output += "The weather there is "+user_data['weather']
		response_output += "You are currently "+str("Single" if user_data["Marital"].lower() == "yes" else "Married")
		response_output += " And you are a " +str("Student" if user_data["Job"].lower() == "yes" else "Working")

	elif "fav color" in user_response or Cosine_Simmilarity_Function("favourite color", user_response) >= 0.25:
		response_output += "\nYou like "+user_data['FavColor'].replace("\n","")+" color right?"

	elif "where do I stay" in user_response or Cosine_Simmilarity_Function("where am I", user_response) >= 0.25:
		response_output += "\nYou stay in "+user_data['Location']

	elif "how is the weather" in user_response:
		response_output += "\nThe weather there is "+user_data['weather']

	elif "what am I" in user_response:
		response_output += "\nYou are currently "+user_data['Marital']
		response_output += "\nAnd you are a " +str("Student" if user_data["Job"].lower() == "yes" else "Working")	

	elif "who built you" in user_response or "owner" in user_response or "author" in user_response:
		response_output += "Ashwin Sai is the one!"

	elif "do you believe in god" in user_response:
		response_output += "Ashwin Sai created me, so yes!"

	elif "thank you" in user_response:
		response_output += "Sure Glad, I could help you! Anytime!"

	elif "what do you know" == user_response:
		response_output += "Hmm, to be honest I know only about Black Holes right now. I can help you with that."

	elif "bye" in user_response or "see you soon" in user_response:
		print("\n"+bot_name+": Did you learn something today?\n")
		end_senti = input(user+":")
		sentiment_score = sia_handle.polarity_scores(end_senti)

		if sentiment_score['compound'] >= 0.05:
			response_output += positive_comments[random.randint(0,3)]+"\nSee you soon! "+str(user)
		elif sentiment_score['compound'] <= 0.05:
			response_output += negative_comments[random.randint(0,3)]+"\nSee you soon! "+str(user)
		else:
			response_output += neutral_comments[random.randint(0,2)]+"\nSee you soon! "+str(user)

	elif "how can you help me" in user_response:
		response_output += "I cant fix your car nor cook food, but I can help you about the topic 'Black hole' ;)"

	elif "What is the gravitational force at the event horizon of a black hole?".lower() in user_response:
		response_output += "Its veryyy Strong at the event horizon."

	elif "What is the point of no return around a black hole?".lower() in user_response:
		response_output += "Event Horizon, after which you can say bye-bye to the known world!"

	elif "What is the dense core of a black hole called?".lower() in user_response:
		response_output += "Singularity"

	elif "What is the boundary surrounding a black hole where light cannot escape?".lower() in user_response:
		response_output += "Photon Sphere"

	elif "What theory describes black holes as objects with zero volume and infinite density?".lower() in user_response:
		response_output += "Theory of General Relativity"

	elif "who founded theory of general relativity" in user_response:
		response_output += "I want to say "+bot_name+", but no, Dr. Albert Einstein found it."

	elif "What is the area surrounding a black hole where gravitational effects are significant?".lower() in user_response:
		response_output += "Ergosphere"

	elif "What is the process by which a black hole emits radiation?".lower() in user_response:
		response_output += "Hawking Radiation"

	elif "What is the region where matter spirals into a black hole?".lower() in user_response:
		response_output += "Accretion Disk"

	elif "What type of black hole is formed by the collapse of massive stars? ".lower() in user_response:
		response_output += "Stellar type of black holes"

	elif "What is the phenomenon where a black hole emits powerful jets of particles?".lower() in user_response:
		response_output += "Jet"

	elif "What type of black hole is believed to exist at the centers of galaxies? ".lower() in user_response:
		response_output += "Supermassive Black holes"

	elif Cosine_Simmilarity_Function("what is inifinite density", user_response) >= 0.25:
		response_output += "A black hole's mass is concentrated into a single point of infinite density known as a singularity"

	elif Cosine_Simmilarity_Function("what is event horizon", user_response) >= 0.25:
		response_output += "The boundary surrounding a black hole where escape velocity equals the speed of light, beyond which nothing can escape"

	elif Cosine_Simmilarity_Function("what is formation", user_response) >= 0.35 or Cosine_Simmilarity_Function("how are black holes formed", user_response) >= 0.35:
		response_output += "Black holes can form from the remnants of massive stars collapsing under their own gravity."

	elif Cosine_Simmilarity_Function("what is no light", user_response) >= 0.25:
		response_output += "Due to their immense gravity, black holes trap light within their event horizon, making them invisible"

	elif Cosine_Simmilarity_Function("what is time dilation", user_response) >= 0.25:
		response_output += "Time near a black hole passes more slowly than in the rest of the universe due to gravitational time dilation"

	elif Cosine_Simmilarity_Function("what is hawking radiation", user_response) >= 0.25:
		response_output += "Black holes can emit radiation known as Hawking radiation, causing them to lose mass over time"

	elif Cosine_Simmilarity_Function("what is spaghettification", user_response) >= 0.25:
		response_output += "Near a black hole, tidal forces can stretch objects into long, thin shapes in a process called spaghettification"

	elif Cosine_Simmilarity_Function("what is size", user_response) >= 0.25:
		response_output += "Black holes can vary in size, from stellar-mass black holes with a few times the mass of the Sun to supermassive black holes millions or even billions of times more massive"

	elif Cosine_Simmilarity_Function("what is jet formation",user_response) >= 0.25:
		response_output += "Some black holes emit powerful jets of particles and radiation from their poles, called relativistic jets"

	elif Cosine_Simmilarity_Function("what is cosimic influence",user_response) >= 0.25:
		response_output += "Black holes play a crucial role in shaping the evolution of galaxies and the distribution of matter in the universe"


	else:
		response_output = Parse_user_response(user_response,knowledge_base_data)
		
		return response_output

	return response_output

def Parse_user_response(user_response,knowledge_base_data):
	'''
		parameters  : user_response, knowledge base data 
		Description : This function is used to tokenize, lemmatize, pos_tag, auto spell correct the words
					  stores only Nouns and Adjectives and perform sentence similarity

		return      : best fit sentence 
	'''

	word_list            = []
	corpus_sentence_list = []
	result               = ""
	for word in nltk.word_tokenize(user_response):
			if word.lower().isalpha() and word.lower() not in stop_words :
				word_list.append(word.lower())

	lemmatized_text        = [WordNetLemmatizer().lemmatize(word.lower()) for word in word_list]
	pos_tagged_lemma       = nltk.pos_tag(lemmatized_text)
	pos_tagged_lemma       = [word for word,tag in pos_tagged_lemma if tag.startswith("NN") or tag.startswith("JJ")]

	for word in pos_tagged_lemma:
		# print("Getting results for ",spell(word))		
		temp = []
		temp = Get_Corpus_Data(spell(word),knowledge_base_data)
		if temp != None:
			corpus_sentence_list.append(temp)

	if len(corpus_sentence_list) > 0:
		result = Find_Similarity_Sentence(user_response,corpus_sentence_list,pos_tagged_lemma)

		return result

	return result

def Words_Presence(sentence,pos_tagged_lemma):
	'''
		parameters  : sentence, pos tagged user response 
		Description : This function is used to check if all the important words from the user response are present
		              in the Model parsed response.

		return      : True  - if all important words is present in the model response
					  False - otherwise  
	'''

	count     = 0
	sent_list = nltk.word_tokenize(sentence)
	for word in pos_tagged_lemma:
		if word in sent_list:
			count += 1

	if count == len(pos_tagged_lemma):
		return True
	else:
		return False

def Find_Similarity_Sentence(user_response,corpus_sentence_list,pos_tagged_lemma):
	'''
		parameters  : user_response, corpus_sentence list, pos tagged user response 
		Description : This function is used to process the corpus using the following techniques,
							i.   Presence of Bigrams
							ii.  Cosine Similarity
							iii. Overlap Coefficiant

		return      : model's response after NLP techniques 
	'''

	unigram_list             = nltk.word_tokenize(user_response)
	bigram_list              = list(ngrams(unigram_list,2))
	bigram_detection_list    = set()
	cosine_similarity_list   = []
	sentence_similarity_list = []
	n_lines                  = 1
	pair_dict                = {}
	overlapcoeff_dict        = {}
	result                   = ""
	backup_list              = set()

	#bigram detection
	for sent in sum(corpus_sentence_list,[]):
		for bigram in bigram_list:
			if bigram[0]+" "+bigram[1] in sent and Words_Presence(sent, pos_tagged_lemma):
				bigram_detection_list.add(sent)

			if bigram[0]+" "+bigram[1] in sent :
				backup_list.add(sent)

	if len(bigram_detection_list) == 0:
		bigram_detection_list = backup_list.copy()

	#cosine similarity
	for sent in bigram_detection_list:
		cosine_similarity_list.append(Cosine_Simmilarity_Function(user_response, sent))
		pair_dict[sent] = Cosine_Simmilarity_Function(user_response, sent)

	# for line,score in zip(sum(corpus_sentence_list,[]),cosine_similarity_list):
	# 	pair_dict[line] = score

	sorted_pair_dict = dict(sorted(pair_dict.items(), key=lambda item: item[1], reverse=True))
	punc_str         = r'[^\'\",?/\\{}[];:!@#$%^&*\(\)-=*-+_]'

	#overlap coefficiant
	if len(sorted_pair_dict)>=50:
		for line in list(sorted_pair_dict.keys())[0:50]:
			overlapcoeff_dict[line] = Overlap_Coefficiant(user_response,line)
	else:
		for line in list(sorted_pair_dict.keys())[0:len(sorted_pair_dict)]:
			overlapcoeff_dict[line] = Overlap_Coefficiant(user_response,line)

	sorted_pair_dict = dict(sorted(overlapcoeff_dict.items(), key=lambda item: item[1], reverse=True))
	result_list      = []

	for index,key in enumerate(sorted_pair_dict):
		result_list.append(key.replace("\n","").replace(",","").replace(")","").replace("(","").strip())

		if index == n_lines:
			break

	for sent in result_list:
		result += sent.capitalize()+". "

	return result

def Overlap_Coefficiant(user_response, sentence):
	'''
		parameters  : user_response, sentence
		Description : This function is used to calculate the overlap coefficiant between two sentences

		return      : overlap coefficiant 
	'''

	tokens_user = set(nltk.word_tokenize(user_response))
	tokens_sent = set(nltk.word_tokenize(sentence))

	common_words = len(tokens_user.intersection(tokens_sent))
	min_size     = min(len(tokens_user),len(tokens_sent))

	if min_size == 0:
		return 0
	else:
		return common_words / min_size

def Cosine_Simmilarity_Function(user_response,sentence):
	'''
		parameters  : user_response, sentence 
		Description : This function is used to calculate the cosine similarity between two sentences

		return      : cosine similarity
	'''

	tokens       = nltk.word_tokenize(sentence)
	tokens       = [word.lower() for word in tokens if word.isalpha()]
	tokens       = [word for word in tokens if word not in stop_words]

	tokens1      = nltk.word_tokenize(user_response)
	tokens1      = [word.lower() for word in tokens1 if word.isalpha()]
	tokens1      = [word for word in tokens1 if word not in stop_words]

	preproc_sent = " ".join(tokens)
	preproc_user = " ".join(tokens1)

	vectorizer   = TfidfVectorizer()
	tfidf_matrix = vectorizer.fit_transform([preproc_sent, preproc_user])

	# Calculate cosine similarity
	cosine_sim   = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])


	return cosine_sim[0][0]

def Get_Corpus_Data(word, knowledge_base_data):
	'''
		parameters  : word knowledge_base data dict 
		Description : This function is used to read and return the domain data for the word

		return      : list of sentences from corpus for the given word 
	'''

	try:		

		return knowledge_base_data[word]

	except Exception as e:
		pass

def Load_Pickle(filename):
	'''
		parameters  : filename 
		Description : This function is used to read the given filename using pickle and return the file data

		return      : data 
	'''

	file_handle = open(filename,"rb")
	data        = pickle.load(file_handle)
	file_handle.close()

	return data

def Initial_User_Data(name):
	'''
		parameters  : user name 
		Description : This function is used to gather initial details about the user for creating user model

		return      : user name 
	'''

	colors            = ["red","blue","white","grey","green"]
	stayy             = {"chatham":"Holy coww! A brave person!!","northside":"Lucky!!"}
	weather           = ["hot","cold"]
	current_weather   = "warmyy"
	flag              = 0	

	print("---------------------------------------------------")
	print("          Black Coffee with the Black Bot          ")
	print("---------------------------------------------------")
	print("Greetings!\nHowwdyy my name is "+bot_name+", Let me explain about myself,")
	print("I am studying my M.S. about Black Hole at Hogwarts.")
	print("I am good with Information but at the same time terrible at Informationnn tooo !!!!")
	print("Please dont get angry about how this convoo goesss.")
	
	print("\n"+bot_name+": Now Lets start with you, What is your good name?\n")
	user_name = input(name+": ")
	if user_name.lower() == "q":
		print(bot_name+": Ahh too soon! bye-bye")
		exit(0)
	user = user_name

	if os.path.exists("user_model_"+user_name.replace(" ","_").lower()+".txt"):
		print("Welcome back ",user_name)
		flag = 1
	else:
		print("\n"+bot_name+": What is your favourite color?\n")
		user_color = input(user+":")
		if user_color.lower() == "q":
			print(bot_name+":Ahh too soon! bye-bye")
			exit(0)
		if user_color.lower() in colors:
			print(bot_name+": ",user_color," is an awesome color!")
		elif user_color.lower() == "black":
			print(bot_name+": Thatss my fav color too yayy!!")
		else:
			print(bot_name+": Not bad, good choice!")

		print("\n"+bot_name+": Where do you stay currently?\n")
		user_loc = input(user+":")
		if user_loc.lower() == "q":
			print(bot_name+": Ahh too soon! bye-bye")
			exit(0)
		try:
			print(bot_name+": ",stayy[user_loc.lower()])
		except Exception as e:
			print(bot_name+": ",user_loc," is a popular place!")

		print("\n"+bot_name+": How is the weather outside?\n")
		user_weather = input(user+":")
		if user_weather.lower() == "q":
			print(bot_name+":Ahh I just askedd the weatherrr! bye-bye")
			exit(0)
		if user_weather in weather:
			print(bot_name+": Damm, its extreme right?")
		else:
			print(bot_name+": hmm, must be a nice weather!")

		print("\n"+bot_name+": Are you single? :)\n")
		user_marital = input(user+":")
		if user_marital.lower() == "q":
			print(bot_name+": Nooooo! Dont gooo yet! :(")
			exit(0)
		if user_marital.lower() == "yes":
			print(bot_name+": Awesome! Me too!!")
		else:
			print(bot_name+": Woww, thats cool, have fun together!")

		print("\n"+bot_name+": Are you a student?\n")
		user_job = input(user+":")
		if user_job.lower() == "q":
			print(bot_name+": bye-bye")
			exit(0)
		if user_job.lower() == "yes":
			print(bot_name+": Studyy well, All the best!")
		else:
			print(bot_name+": Go become a student, its fun!")

		print("\n"+bot_name+": How much do you like about space (galaxy, stars, astronomical objects)?\n")
		user_likes = input(user+":")
		sentiment_score = sia_handle.polarity_scores(user_likes)

		if sentiment_score['compound'] >= 0.05:
			print(positive_comments[random.randint(0,3)])
		elif sentiment_score['compound'] <= 0.05:
			print(negative_comments[random.randint(0,3)])
		else:
			print(neutral_comments[random.randint(0,2)])



	print("\n"+bot_name+": Now lets get down to business, How can I help you?")

	if flag == 0:
		User_Model_Creation(user_name,user_color,user_loc,user_weather,user_marital,user_job,user_likes)

	return user_name

def User_Model_Creation(user_name,user_color,user_loc,user_weather,user_marital,user_job,user_likes):
	'''
		parameters  : user_name,user_color,user_loc,user_weather,user_marital,user_job 
		Description : This function is used to create a useer model

		return      : None 
	'''	

	file_handle = open("user_model_"+user_name.replace(" ","_").lower()+".txt","w")

	file_handle.write("Name : "+str(user_name)+"\n")
	file_handle.write("FavColor : "+str(user_color)+"\n")
	file_handle.write("Location : "+str(user_loc)+"\n")
	file_handle.write("weather : "+str(user_weather)+"\n")
	file_handle.write("Marital : "+str(user_marital)+"\n")
	file_handle.write("Job : "+str(user_job)+"\n")
	file_handle.write("Likiness_about_Space : "+str(user_likes)+"\n")

	file_handle.close()

	user = user_name
	print("User Model created!")

def User_Model_Updation(data,user):
	'''
		parameters  : data , user 
		Description : This function is used to update the user model with the uesr's chat history

		return      : None 
	'''	

	file_handle = open("user_model_"+user+".txt","a", encoding='utf-8')
	file_handle.write("\n")
	for item in data:
		file_handle.write(item)
		file_handle.write("\n")

	file_handle.close()

	print("User model updated!")
	print("Name : ",user)

def Load_User_Model(user):
	'''
		parameters  : user 
		Description : This function is load the user model

		return      : user model data 
	'''	
	data_dict    = {}
	try:
		file_handle = open("user_model_"+user.replace(" ","_").lower()+".txt","r", encoding='utf-8')
		data        = file_handle.readlines()
		file_handle.close()

		for line in data:
			try:
				data_dict[line.split(":")[0].replace(" ","")] = line.split(":")[1]
			except Exception as e:
				pass

		return data_dict

	except Exception as e:
		#print(e)
		print("User "+user+" profile not present!")

def Chatbot():
	'''
		parameters  : None
		Description : This function is initiates the Chatbot

		return      : None 
	'''	

	knowledge_base_data = Load_Pickle("DK_Base.pickle")
	user                = "unknown"
	user                = Initial_User_Data(user)	
	user_interactions   = []
	few_topics          = ["Infinite Density", "Event Horizon", "Formation","No Light", "Time Dilation", "Hawking Radiation",\
						   "Spaghettification", "Size", "Jet Formation", "Cosmis influence", "Black Hole"]

	while True:
		try:
			user_input     = input(user+": ")
			if user_input.lower() == "q":
				print("Thank you for chatting, See you soon!")
				break

			model_response = Response_Parsing(user_input,knowledge_base_data,user)

			if user_input != "" and model_response == "":
				model_response = "Thats, interesting. Please go on. I can only help you about Black holes."
				model_response += "I can help you out with these topics too, " + "\n".join(few_topics) +" \n"
			elif user_input == "" and model_response == "":
				model_response = "Gosh, you dont want to speak with me? :("		

			print(bot_name,": ",model_response)
			user_interactions.append(user+": "+user_input)
			user_interactions.append(bot_name+": "+model_response)
			print("\n")

			if "see you soon!" in model_response.lower():
				break
		except Exception as e:
			# print(e)
			print("I can help you out with these topics too, " + "\n".join(few_topics) +" \n")

	User_Model_Updation(user_interactions,user)

if __name__ == "__main__":
	'''
		parameters  : None
		Description : This function is the main function

		return      : None
	'''

	print("hi")

	try:
		Chatbot()
	except Exception as e:
		print(e)



