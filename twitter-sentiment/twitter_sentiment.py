

# Basé sur:
# Théophile Blard, French sentiment analysis with BERT, (2020), GitHub repository, https://github.com/TheophileBlard/french-sentiment-analysis-with-bert
# https://github.com/TheophileBlard/french-sentiment-analysis-with-bert#hugging-face-integration

# pip install sentencepiece


import os
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline
import pandas as pd
import numpy as np
from time import gmtime, strftime


tokenizer = AutoTokenizer.from_pretrained("tblard/tf-allocine")
model = TFAutoModelForSequenceClassification.from_pretrained("tblard/tf-allocine")


nlp = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)
#--------------------------------------------

#--------------------------------------------
def sentim_posneg_score(text, nlpipeline=nlp):
	res = nlpipeline(text).pop()
	if res['label'] == 'NEGATIVE':
		PNscore = - res['score']
	else:
		PNscore = res['score']
	return(PNscore)
#--------------------------------------------

#--------------------------------------------

print(nlp("Alad'2 est clairement le meilleur film de l'année 2018.")) # POSITIVE



#--------------------------------
# estim sentim in chunks write append to csv as you go
#--------------------------------

chunksize = 10**3

whichdata =  "pedag"

data_folder = " (enter path) "

year = '2022'

for i in range(12):
	print("starting new file: ", str(i))
	df = pd.read_csv(data_folder + str(year) +"/tw_"+ whichdata + "_"+ str(year) +"_mth_" + str(i) + ".csv")#, nrows=50)
	print(strftime("new file time %H:%M:%S", gmtime()))

	how_many_split_into = int(np.ceil(df.shape[0]/chunksize))
	print("splitting into %d files." % how_many_split_into )
	dfchunks = np.array_split(df, how_many_split_into) # split into 3

	for chunk_i in range(how_many_split_into):
		print("chunk ", str(chunk_i))
		print(strftime("currently %H:%M:%S", gmtime()))
		currdf = dfchunks[chunk_i]
		currdf['sentim'] = currdf['tweet'].apply(sentim_posneg_score)
		print('saving...')
		if chunk_i ==0:
			currdf.to_csv(data_folder + str(year) +"/twsent_"+ whichdata + "_"+ str(year) +"_mth_"+str(i) + ".csv", index=False)
		else:
			currdf.to_csv(data_folder + str(year) +"/twsent_"+ whichdata + "_"+ str(year) +"_mth_"+str(i) + ".csv", \
				mode='a', header=False, index=False)
	print("done for this file.")







""" exemples -- 

@BastienJoseph @kahinasekkai Excellente vidéo, déjà vue plusieurs fois, hyper pédagogique
[{'label': 'POSITIVE', 'score': 0.9969581365585327}]

@zouzoubchka Sauf que, quand des journalistes (la plupart), relaient une propagande sans rien observer et sans rien analyser, ce n’est pas un simple problème pédagogique, c’est un échec démocratique.
[{'label': 'NEGATIVE', 'score': 0.9821135401725769}]

"""
