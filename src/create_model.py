# import logging
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from src.LemmaTokenizer import *
import numpy

def get_topic_keywords(features, X):
	features_with_weights = sorted([ {"keyword":features[i], "count": X[0,i], "index":i} for i in range(len(features)) ], key=lambda x:-x["count"] )[:50]
	features = {}
	feature_indices = {}
	for fww in features_with_weights:
		features[fww["keyword"]] = fww["count"]
		feature_indices[fww["keyword"]] = fww["index"]
	return features, feature_indices


def create_and_save_model(subtopics, output_file):
	# Start New Code
	if not os.path.isdir('./log'):
		os.mkdir('./log')
	with open('./log/subtopics_with_text_from_google.json','w',encoding='utf-8') as f:
		json.dump(subtopics,f,ensure_ascii=False)
	# End New Code

	data = []
	model_to_print = []
	output = ()
	all_texts = []
	vec = TfidfVectorizer(ngram_range=(1,3), stop_words="english")

	# list with subtopics e.g: (Automation, Productivity and Skills)
	# and their corresponding retrieved text from Google
	subtopic_names = list(subtopics.keys())
	no_data_subtopic_names = []
	

	for topic in subtopic_names:
		text = subtopics[topic]	

		if len(text.strip()) >0 :
			all_texts.append(text)
		else:
			no_data_subtopic_names.append(topic)

	# X is a sparse term-document matrix of the learned vocabulary and idf
	X = vec.fit_transform(all_texts)
	global gX
	gX = X

	# Start New Code
	idf = vec.idf_
	with open('./log/idf.json','w',encoding='utf-8') as f:
		json.dump(dict(zip(vec.get_feature_names(),idf)),f,ensure_ascii=False)
	# End New Code

	# list of unigrams, bigrams and trigrams of all text
	features = vec.get_feature_names()

	# Start New Code
	if not os.path.isdir('./log'):
		os.mkdir('./log')
	with open('./log/features.txt','w',encoding='utf-8') as f:
		f.write(str(features))
	# End New Code

	# range(len(subtopic_names)) puede ser entre 1 o más de 3
	# dependiendo de la cantidad de subtópicos que el usuario
	# haya ingresado
	for i in range(len(subtopic_names)):
		if subtopic_names[i] not in no_data_subtopic_names:
			Xi = X[i, :]
			features_with_weights, feature_indices = get_topic_keywords(features, Xi)
			data.append({"subtopic":subtopic_names[i], \
				"keywords":features_with_weights, \
				"vectorizer":vec, \
				"feature_indices":feature_indices})
			# model_to_print is of type list
			model_to_print.append({"subtopic":subtopic_names[i], \
				"keywords":features_with_weights, \
				"feature_indices":feature_indices})
			print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX')
			print(type(model_to_print[0]))
			print(model_to_print[0])
			# try:
			# 	print(len(model_to_print))
			# except OSError as err:
			# 	print('OS error: {0}'.format(err))
			# except ValueError:
			# 	print("Could not print the length of this list")
			# except:
			# 	print("Unexpected error:",sys.exc_info()[0])
			# 	raise

				
	#print(model_to_print)
	#print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
	#print(type(model_to_print))
	#with open('./log/model.json','w',encoding='utf-8') as j:
		#json.dump(model_to_print,j,ensure_ascii=False)
			
			# output["keywords"] = features_with_weights
			# print(features_with_weights)
			# print(type(features_with_weights))
			# print(feature_indices)
			# output["feature_indices"] = feature_indices

	pickle.dump(data, open(output_file, "wb"))
	global gvec
	gvec = vec


def load_model(file_path):
	return pickle.load(open(file_path, "rb"))

gvec = None
gX = None
