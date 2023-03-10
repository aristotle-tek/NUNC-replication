# NUNC Dashboard

import os
import streamlit as st

import numpy as np
import pandas as pd
#import plotly.figure_factory as ff
#import plotly.graph_objects as go

import warnings



import requests
import os
import json
import pandas as pd
import csv
import datetime
import dateutil.parser
import unicodedata
import datetime


# Note: Twitter API token is stored as a secret --
# this explains how to store secrets:
# https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management

bearer_token = st.secrets["bearer_token"]


#---------------------------------------
def create_headers(bearer_token):
	headers = {"Authorization": "Bearer {}".format(bearer_token)}
	return headers
#---------------------------------------

#---------------------------------------
def create_url_recent(keyword, max_results = 10):
	search_url = "https://api.twitter.com/2/tweets/search/recent"
	query_params = {'query': keyword,
	#'end_time': end_date, -optional
	'max_results': max_results,
	'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
	'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
	'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
	'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
	}
	return (search_url, query_params)
#---------------------------------------

#---------------------------------------
def connect_to_endpoint(url, headers, params, next_token = None):
	params['next_token'] = next_token   #params object received from create_url function
	response = requests.request("GET", url, headers = headers, params = params)
	print("Endpoint Response Code: " + str(response.status_code))
	if response.status_code != 200:
		raise Exception(response.status_code, response.text)
	return response.json()
#---------------------------------------

#---------------------------------------
#@st.cache(allow_output_mutation=True, hash_funcs={dict: lambda _: None}) # the database connection is created once and stored in the cache. Then, every subsequent time get_database_conection is called, the already-created connection object is reused automatically. In other words, it becomes a singleton.
def get_recent_tweets(keyword, bearer_token):
	#bearer_token = auth()
	headers = create_headers(bearer_token)
	max_results = 10
	url = create_url_recent(keyword, max_results)
	#url = create_url(keyword, start_list[i],end_list[i], max_results)
	next_token=None
	json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
	return(json_response)
#-----------------------------------

#-----------------------------------
def df_rel_info(json_response):
	tweetinfo = []
	for tweet in json_response['data']:
		author_id = tweet['author_id']
		created_at = dateutil.parser.parse(tweet['created_at'])
		text = tweet['text']
		tweetinfo.append([author_id, created_at, text])
	df = pd.DataFrame(tweetinfo, columns=['author_id','created_at','text'])
	return(df)
#-----------------------------------

#-----------------------------------


st.set_page_config(
	page_title="NUNC! Analyse Automatis??e des Alertes",
	page_icon="???????????", # :woman_student:
)


st.title('NUNC! Analyse Automatis??e des Alertes')


top_container  = st.container()
with top_container:
	col1, col2 = st.columns(2)
	with col1:
		placeholder = st.empty()
		st.markdown("""Laboratoire Techn??""")
		st.markdown("""[https://techne.labo.univ-poitiers.fr/nunc/](https://techne.labo.univ-poitiers.fr/nunc/)""") # spherical variagram...

	with col2:
		placeholder2 = st.empty()
		placeholder2.markdown("""Projet financ?? par la [Fondation Maison des Sciences de l???Homme](https://www.fmsh.fr/fr/projets-soutenus/nouveaux-usages-du-numerique-et-continuites-analyse-automatisee-des-alertes)""") # spherical variagram...



st.header("""Qu'est-ce que c'est le \"Sentiment Twitter???\" """)
st.markdown("""Les r??sultats du sentiment Twitter pr??sent??s en (2) sont bas??s sur une 
analyse automatis??e des textes dans le but de comprendre s'ils sont positifs 
(applaudissants, optimistes) ou n??gatifs (critiques, cyniques, en col??re).""")

st.markdown("""L'analyse des sentiments des tweets est r??alis??e sur la base d'un mod??le de langage
bas?? sur Transformer form?? sp??cifiquement sur les textes fran??ais. 
Le mod??le de sentiment est ensuite form?? sur 200 000 critiques de films positives et n??gatives extrait d'allocine.fr """)

st.markdown("""
Sources:
* [CamemBERT; A Tasty French Language Model](https://camembert-model.fr/)]

* Th??ophile Blard, French sentiment analysis with BERT, (2020), [GitHub repository ici](https://github.com/TheophileBlard/french-sentiment-analysis-with-bert)

""")

#-----------------------
st.header("Exemples avec le sentiment tel que pr??dit par le mod??le ")

st.markdown("""**Tweet 1:** @BastienJoseph @kahinasekkai Excellente vid??o, d??j?? vue plusieurs fois, hyper p??dagogique""")
st.markdown(""" POSITIVE, 'score': 0.996""")
st.markdown("---")
st.markdown("""**Tweet 2:**@zouzoubchka Sauf que, quand des journalistes (la plupart), relaient une propagande sans rien observer et sans rien analyser, ce n???est pas un simple probl??me p??dagogique, c???est un ??chec d??mocratique.""")
st.markdown(""" NEGATIVE, 'score': 0.982""")
st.markdown("---")


time_last_got_tweets = 0 # this does nothing

#-----------------------
st.header("Voir quelques exemples de tweets r??cents")
keyword = st.selectbox(
	'veuillez choisir un terme de recherche:',
	('pedagogique', 'ecole maison','formation distance','continuitepedagogique')
)

if st.button('Cliquez ici pour voir les tweets r??cents.'):
	st.write('ils sont en route...')
	if time_last_got_tweets ==0:
		tweet_json = get_recent_tweets(keyword, bearer_token)

		n_tweets = len(tweet_json)
		twdf = df_rel_info(tweet_json)
		twnd = twdf.drop_duplicates('text', inplace=False)
		num_to_display = min(len(twnd), 3)
		for i, row in twnd.iterrows():
			st.markdown("---")
			tweet = row['text']
			st.markdown(tweet)
			st.markdown("publi?? ?? " + str(row.created_at)[:19] )
		# dataframe print - ugly -st.dataframe(twdf.iloc[0:num_to_display]) # display up to first 3



else:
	st.write('(les tweets ne sont affich??s que pour les 7 derniers jours)')
