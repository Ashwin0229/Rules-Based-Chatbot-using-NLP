'''
Name   : Ashwin Sai C
Course : NLP - CS6320-001
Title  : Project 1a : Web Crawler
Term   : Spring 2024

'''

import re
import distance
import requests
from   bs4 import BeautifulSoup
import os
import nltk
import numpy as np
from   sklearn.feature_extraction.text import TfidfVectorizer
from   nltk.corpus import stopwords
import pickle
from   nltk.stem   import WordNetLemmatizer

n_files        = 25
url_dict       = {}
url_check_list = ["youtu.be","portal.dnb", "idref", "public","information-compliance", "research","wikidocumentaries","wikimedia",\
				  "firenze","cookies","automatic","youtube","facebook","support","instagram","twitter","wikiquote","donate","linkedin",\
				  	"auth",".pdf","developer","subscribe","royalsociety","policies","disney","Services","about","bbc","dnb.de",\
				  	"creativecommons","forbes","congress","semantic","github","news","brainpickings","privacy","policy","futureplc",\
				  	"awin1","newyorker","airspacemag","mediawiki","zh-","be-","d-nb","citeseerx","worldcat","gallery","galleries",\
				  	"nobelprize","bnf","handle", "leibniz", "Swartkolk", "bat-smg","wiktionary","Project:Main_Page", "zbmath","audio",\
				  	"amazon","podcasts","reviews","ghost"]
domain_list    = set()

def Scrap_Data(scrap_link, file_number):
	'''
		parameters  : web link to scrap, and the file name 
		Description : This function is used to scrap the data from the web link

		return      : scrapped data
	'''


	print("Scrapping data for ",scrap_link)
	page            = requests.get(scrap_link,timeout=20)
	soupdata        = BeautifulSoup(page.content, "html.parser")
	results         = soupdata.findAll('div', {'snippet-item r-snippetized'})
	scrap_data_var  = []

	for data in results:
		scrap_data_var.append(data.get_text())

	for text_data in soupdata.select('p'):
		scrap_data_var.append(text_data.get_text())

	for text_data in soupdata.select('div'):
		scrap_data_var.append(text_data.get_text())

	for text_data in soupdata.select('head'):
		scrap_data_var.append(text_data.get_text())

	for text_data in soupdata.select('table'):
		scrap_data_var.append(text_data.get_text())

	for text_data in soupdata.select('a'):
		scrap_data_var.append(text_data.get_text())


	return scrap_data_var

def Url_Check_Function(url_name, url_check):
	'''
		parameters  : url and list of banned urls
		Description : This function is used to check the presence of url in url_check list

		return      : True  - if not present
					  False - if present
	'''


	for url in url_check:
		if url.lower() in url_name.lower():
			return False

	return True

def Similarity_Check(url_name, url_check):
	'''
		parameters  : url and list of banned urls
		Description : This function is used to check the presence of url in url_check list

		return      : True  - if not present
					  False - if present
	'''


	for link in url_check:
		if link != url_name and distance.levenshtein(link,url_name) <= 4:
			# print("Similarity Failed! ",link," ",url_name)
			return False

	return True

def Get_Links(URL):	
	'''
		parameters  : url
		Description : This function is used to scrap the <a> href links from a url

		return      : set of links
	'''

	page      = requests.get(URL)
	soupdata  = BeautifulSoup(page.content, "html.parser")
	link_repo = set()	
	
	for link in soupdata.select('a'):
		try:	
			# print(link['href'])
			# print((Url_Check_Function(link['href'],url_check_list)))		
			if ("https" in link['href']) and (Url_Check_Function(link['href'],url_check_list)):
				try:
					url_dict[link['href'].split("/")[2]] += 1
				except Exception as e:
					url_dict[link['href'].split("/")[2]] = 1

				if url_dict[link['href'].split("/")[2]] <= 5 and Similarity_Check(link['href'].split("/")[2], domain_list):
					# print("<adding> ",link['href'].split("/")[2])
					link_repo.add(link['href'])
					domain_list.add(link['href'].split("/")[2])
		except Exception as e:
			pass

	# print("Total Links in "+URL+": ",len(link_repo))

	return link_repo

def Write_Scrap_Data(data,file_number):
	'''
		parameters  : data, file name
		Description : This function is used to write the scrapped data into the filename

		return      : None
	'''

	file_handle = open(str(file_number)+"_.txt", "w", encoding="utf-8")
	for d in data:
		file_handle.write(d+"\n")
	file_handle.close()

def Display_Links(queue):
	'''
		parameters  : list of url
		Description : This function is used to print the url give in the queue list

		return      : None
	'''

	print("\n\nx--------------------LINKS--------------------x")
	for link in queue:
		print(link)

def BFS_Links(source_link): 
	'''
		parameters  : source url
		Description : This function is used to perform Breadth First Search, Scrap data and store in files.

		return      : None
	'''
  
	# Create a queue for BFS 
	queue      = [] 
	visited    = []
	link_repo  = set()
	link_index = 0
	queue.append(source_link) 
	visited.append(source_link) 

	while queue: 

		if link_index == n_files:
			break
		
		s = queue.pop(0)
		try:
			return_list = Get_Links(s)			
			scrap_data_var = Scrap_Data(s,link_index)
			
			if len(scrap_data_var) > 50:
				Write_Scrap_Data(scrap_data_var,link_index)
				link_index += 1
				print("Link Count  : ",link_index)
				print("Adding Link : ",s)

		except Exception as e:
			print(e)			
			return_list = ""
		
		alread_visited_count = 0
		for i in return_list: 
			if i not in visited: 
				queue.append(i)
			else:
				alread_visited_count += 1
		
		visited.append(s) 

def Lower_Case_Function(n_files):
	'''
		parameters  : numebr of files
		Description : This function is used to lower case all the sentences in the file

		return      : None
	'''

	for i in range(n_files):
		file_handle = open(str(i)+"_.txt","r", encoding='utf-8')
		data        = file_handle.readlines()
		file_handle.close()

		file_handle = open(str(i)+"_.txt","w",encoding='utf-8')
		for line in data:
			new_line = line.lower()
			file_handle.write(new_line+"\n")

		file_handle.close()


def Strip_Blank_Lines_Function(n_files):
	'''
		parameters  : numebr of files
		Description : This function is used to remove all blank lines

		return      : None
	'''
	new_line_count = 0
	for i in range(n_files):
		file_handle = open(str(i)+"_.txt","r", encoding='utf-8')
		data        = file_handle.readlines()
		file_handle.close()

		file_handle = open(str(i)+"_.txt","w",encoding='utf-8')
		dataa       = [item for item in data if item != "\n"]
		for line in dataa:
			temp = line.strip()
			file_handle.write(" ".join(temp.split())+"\n")			

		file_handle.close()


def Remove_Short_Lines_Functions(n_files):
	'''
		parameters  : numebr of files
		Description : This function is used to remove the short lines from files

		return      : None
	'''

	for i in range(n_files):
		file_handle = open(str(i)+"_.txt","r", encoding='utf-8')
		data        = file_handle.readlines()
		file_handle.close()

		file_handle = open(str(i)+"_.txt","w",encoding='utf-8')
		for line in data:
			if len(line.split(" ")) > 5:
				file_handle.write(line+"\n")

		file_handle.close()


def Remove_Reference_Numbers(n_files):
	'''
		parameters  : numebr of files
		Description : This function is used to remove reference numbers from the files

		return      : None
	'''

	for i in range(n_files):
		file_handle = open(str(i)+"_.txt","r", encoding='utf-8')
		data        = file_handle.readlines()
		file_handle.close()

		file_handle = open(str(i)+"_.txt","w",encoding='utf-8')
		for line in data:
			text = re.sub(r'\[\d+\]', '',line)
			file_handle.write(text+"\n")

		file_handle.close()

def Remove_NonAlpha(n_files):
	'''
		parameters  : numebr of files
		Description : This function is used to remove all nonalpha from text files

		return      : None
	'''

	for i in range(n_files):
		file_handle = open(str(i)+"_.txt","r", encoding='utf-8')
		data        = file_handle.readlines()
		file_handle.close()

		file_handle = open(str(i)+"_.txt","w",encoding='utf-8')
		for line in data:
			if line.isalpha():
				file_handle.write(line+"\n")

		file_handle.close()

def Clean_Files(n_files):
	'''
		parameters  : numebr of files
		Description : This function is used to initiate the cleaning methods

		return      : None
	'''

	print("----Removing Lower Case----")
	Lower_Case_Function(n_files)	
	print("----Removing Short lines----")
	Remove_Short_Lines_Functions(n_files)
	print("----Removing Reference Nos. lines----")
	Remove_Reference_Numbers(n_files)
	print("----Removing Blank Lines----")
	Strip_Blank_Lines_Function(n_files)
	
def Filter_Stopwords(data_list):
	'''
		parameters  : numebr of files
		Description : This function is used to remove all the stopwords present in the corpus data

		return      : filtered list
	'''

	stop_words    = set(stopwords.words('english'))
	filtered_list = []

	for doc in data_list:
		tokens = nltk.word_tokenize(doc)
		temp   = []
		for word in tokens:
			if word not in stop_words and word.isalpha():
				temp.append(word)

		filtered_list.append(" ".join(temp))

	return filtered_list

def Filter_Punctuation(data_list):
	'''
		parameters  : numebr of files
		Description : This function is used to remove the punctuations from files

		return      : filtered list
	'''

	punc_list     = ["'",'"',',','.','?',"/","\\",'{','}',"[","]",";",":",'!',"@","#","$",'%',"^","&","*","(",")","-","+","_"]
	punc_str      = r'[^\'\",?/\\{}[];:!@#$%^&*\(\)-=*-+_]'
	filtered_list = []
	print(type(data_list))
	for doc in data_list:
		tokens = nltk.word_tokenize(doc)	

		clean_sentence = re.sub(r'[^a-zA-Z\s]', '', doc)
		clean_sentence = clean_sentence.replace(",","").replace('|',"").replace("\n",".").strip()
		clean_sentence = re.sub(punc_str, '', clean_sentence)


		filtered_list.append(clean_sentence)
	
	return filtered_list

def Filter_Function(total_file_data):
	'''
		parameters  : file data list
		Description : This function is used to initiate the preprocessing methods

		return      : filtered list
	'''

	filtered_stopwords = Filter_Stopwords(total_file_data)
	filtered_punc      = Filter_Punctuation(filtered_stopwords)

	return filtered_punc

def Get_Total_File_Data(n_files):
	'''
		parameters  : numebr of files
		Description : This function is used to return the total file data list

		return      : total file data list
	'''

	total_file_data = []

	for i in range(n_files):
		file_handle = open(str(i)+"_.txt","r", encoding='utf-8')
		data        = file_handle.readlines()
		file_handle.close()

		total_file_data.append(" ".join(data))
	
	print("Number of Files : ",len(total_file_data))

	return total_file_data

def Calculate_TF_IDF(n_files):
	'''
		parameters  : numebr of files
		Description : This function is used to calculate the tf-idf

		return      : list of top words
	'''

	total_file_data = Get_Total_File_Data(n_files)
	filtered_data   = Filter_Function(total_file_data)

	print("Length of filtered data : ",len(filtered_data))
	tfidf                    = TfidfVectorizer()
	result                   = tfidf.fit_transform(filtered_data)
	avg_tfidf                = np.mean(result, axis=0).tolist()[0]
	feature_names            = tfidf.get_feature_names_out()
	word_tfidf_scores        = list(zip(feature_names, avg_tfidf))
	sorted_word_tfidf_scores = sorted(word_tfidf_scores, key=lambda x: x[1], reverse=True)

	top_list                 = sorted_word_tfidf_scores[:40]
	top_dict                 = dict(top_list)

	print(top_dict.keys())

	return list(top_dict.keys())[:50]
	
def Build_Knowledge_Base(n_files, top_words):
	'''
		parameters  : numebr of files and top words list
		Description : This function is used to create a domain dictionary with the top words

		return      : domain dict
	'''

	total_file_data = Get_Total_File_Data(n_files)
	file_lines_list = []
	domain_dict     = {}
	top_words.append("singularity")
	top_words.append("radiation")
	top_words.append("neutron star")
	top_words.append("wormhole")
	top_words.append("space-time")
	top_words.append("supernova")

	for word in top_words:
		print("Building Domain dict for '",word,"'")
		word = WordNetLemmatizer().lemmatize(word.lower())
		for doc in total_file_data:
			temp = doc.split(".")
			for line in temp:
				# print(line)
				# a = input()
				if word.strip() in line.lower():
					try:								
						domain_dict[word.strip()].append(line)
					except Exception as e:
						domain_dict[word.strip()] = []
						domain_dict[word.strip()].append(line)

		print("Number of Sentences : ",len(domain_dict[word.strip()]))

	print("Length of keys in Domain Dict : ",len(domain_dict))


	return domain_dict

def Save_Dict_Pickle(dict_var, name):
	'''
		parameters  : ngrams dictionary, and name of file 
		Description : This function is used to write the ngrams dictionary into a pickle file

		return      : None
	'''

	file_handle = open(name+".pickle", "wb")
	pickle.dump(dict_var, file_handle, protocol=pickle.HIGHEST_PROTOCOL)
	file_handle.close()

	print("Pickle - ",name," saved!")

def Display_Pickle(filename):
	'''
		parameters  : filename 
		Description : This function is used to read the given filename using pickle and return the file data

		return      : data 
	'''

	file_handle = open(filename,"rb")
	data        = pickle.load(file_handle)
	file_handle.close()

	for key in data:
		print("Key : ",key, " : ",data[key][0:10])
		print("----------------------------------")

def Web_Crawler():
	'''
		parameters  : None
		Description : This is the crawling initiate function

		return      : None
	'''

	# URL       = "https://en.wikipedia.org/wiki/Black_hole#:~:text=A%20black%20hole%20is%20a,to%20form%20a%20black%20hole."
	# Get_Links(URL)
	# BFS_Links(URL)

	Clean_Files(n_files)
	top_words   = Calculate_TF_IDF(n_files)
	domain_dict = Build_Knowledge_Base(n_files, top_words)
	Save_Dict_Pickle(domain_dict,"DK_Base")

	#To display Knowledge Base
	# Display_Pickle("DK_Base.pickle")


if __name__ == "__main__":
	'''
		parameters  : None
		Description : This is the main function

		return      : None
	'''

	print("hi")
	try:
		Web_Crawler()
	except Exception as e:
		print(e)
	
	
