# NUNC Dashboard


import os
import streamlit as st

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go

import datetime

import warnings


from scipy import signal

#-----------------------------------

#-----------------------------------
#@st.experimental_memo
@st.cache
def load_data(filepath):
	"""Retrieve DataFrame, cache it.
	returns a DataFrame. Mutating it won't affect
	the cache.
	"""
	df = pd.read_csv(filepath)
	return(df)
#-----------------------------------

#-----------------------------------


st.set_page_config(
    page_title="NUNC! Analyse Automatisée des Alertes",
    page_icon="👩‍🎓", # :woman_student:
)


st.title('NUNC! Analyse Automatisée des Alertes')



#-----------------------------------
#  col 1
#-----------------------------------


top_container  = st.container()
with top_container:
	col1, col2 = st.columns(2)
	with col1:
		placeholder = st.empty()
		st.markdown("""*Laboratoire Techné*""")
		st.markdown("""[https://techne.labo.univ-poitiers.fr/nunc/](https://techne.labo.univ-poitiers.fr/nunc/)""") # spherical variagram...
		


	with col2:
		placeholder2 = st.empty()
		st.markdown("""Projet financé par la [Fondation Maison des Sciences de l’Homme](https://www.fmsh.fr/fr/projets-soutenus/nouveaux-usages-du-numerique-et-continuites-analyse-automatisee-des-alertes)""") # spherical variagram...



mid_container = st.container()
with mid_container:
	keyword = st.selectbox(
		'Choisissez une terme de recherche',
		("pédagogique", "école maison")
	)

	startd = st.date_input(
	"Choisissez une date de début",
	value =datetime.date(2019, 1, 1),
	min_value=datetime.date(2019, 1, 1),
	max_value=datetime.date(2022, 12, 5))

	lissage = st.selectbox(
		'Lissage?',
		("Savitzky-Golay", "aucun")
	)
	st.header("Twitter sentiment pour " + keyword)


	currwd = os.path.dirname(os.path.realpath(__file__))
	if keyword == "pédagogique":
		fpath = currwd + "/data/" + "bootstrap_pedag_dec13.csv"
	elif keyword == "école maison":
		fpath = currwd + "/data/" + "bootstrap_ecolemaison_dec13.csv"

	df = load_data(fpath)

	df.columns = ['indx', 'date', 'lower_bound', 'median', 'upper_bound']
	df = df[pd.notnull(df.date)]
	df['date2'] = pd.to_datetime(df.date)

	#st.write('Date de début:', startd)

	
	start = pd.to_datetime(startd)
	dfrel = df[df.date2>start]
	df.index= range(len(df))

	if lissage == 'Savitzky-Golay':
		fig2 = go.Figure()

		windowsize = 53  # window size used for filtering
		poly_order = 3 # order of fitted polynomial
		trace1 = go.Scatter(x=dfrel['date'],
				y=signal.savgol_filter(dfrel['median'],
				windowsize,
				poly_order),
				marker=dict(color='#0099ff'),
				name='estimation bootstrap médiane,',
				xaxis='x2', yaxis='y2')

		trace2 = go.Scatter(x=dfrel['date'],
				y=signal.savgol_filter(dfrel['lower_bound'],
				windowsize,
				poly_order),
				marker=dict(color='#404040'),
				name='borne inférieure (5%),',
				xaxis='x2', yaxis='y2')

		trace3 = go.Scatter(x=dfrel['date'],
				y=signal.savgol_filter(dfrel['upper_bound'],
				windowsize,
				poly_order),
				marker=dict(color='#404040'),
				name='borne supérieure (95%)',
				xaxis='x2', yaxis='y2')


		fig2.add_traces([trace1, trace2, trace3])

		fig2.layout.update(legend=dict(orientation="h"))

		fig2['layout']['xaxis2'] = {}
		fig2['layout']['yaxis2'] = {}

		fig2.layout.xaxis2.update({'title': ''})
		fig2.layout.yaxis2.update({'anchor': 'x2'})
		fig2.layout.yaxis2.update({'title': 'Twitter Sentiment (lissage Savitzky-Golay)'}) # Bootstrap estimate of
		st.plotly_chart(fig2, use_container_width=True)
	else:

		fig = go.Figure()

		trace1 = go.Scatter(x=dfrel['date'], y=dfrel['median'],
				marker=dict(color='#0099ff'),
				name='estimation bootstrap médiane',
				xaxis='x2', yaxis='y2')

		trace2 = go.Scatter(x=dfrel['date'], y=dfrel['lower_bound'],
				marker=dict(color='#404040'),
				name='borne inférieure (5%)',
				xaxis='x2', yaxis='y2')

		trace3 = go.Scatter(x=dfrel['date'], y=dfrel['upper_bound'],
				marker=dict(color='#404040'),
				name='borne supérieure (95%) ',
				xaxis='x2', yaxis='y2')


		fig.add_traces([trace1, trace2, trace3])

		fig.layout.update(legend=dict(orientation="h"))

		fig['layout']['xaxis2'] = {}
		fig['layout']['yaxis2'] = {}
		fig.layout.xaxis2.update({'title': ''})
		fig.layout.yaxis2.update({'anchor': 'x2'})
		fig.layout.yaxis2.update({'title': 'Twitter Sentiment'}) # Bootstrap estimate of

		st.plotly_chart(fig, use_container_width=True)

