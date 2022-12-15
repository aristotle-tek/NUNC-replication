# NUNC Dashboard

import os
import streamlit as st

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px

from scipy import signal

import warnings


#-----------------------------------

#-----------------------------------
@st.cache
def load_all_data_regions(fpath, keyword):
	"""Retrieve dataframe, cache it.
	returns a DataFrame. Mutating it won't affect
	the cache.
	"""
	alldf = pd.DataFrame()
	for year in [2019,2020,2021,2022]:
		currfile = fpath + "gtrends_" + str(year)+ "_"+ keyword +"_regions.csv"
		currdf = pd.read_csv(currfile)
		alldf = pd.concat([alldf, currdf])
	return(alldf)
#-----------------------------------

#-----------------------------------
@st.cache
def load_data(filepath):
	df = pd.read_csv(filepath)
	return(df)
#-----------------------------------

#-----------------------------------

st.set_page_config(
    page_title="NUNC! Analyse Automatisée des Alertes",
    page_icon="👩‍🎓", # :woman_student:
)



st.title('NUNC! Analyse Automatisée des Alertes')


top_container  = st.container()
with top_container:
	col1, col2 = st.columns(2)
	with col1:
		placeholder = st.empty()

		st.markdown("""*Laboratoire Techné*""") # spherical variagram...
		st.markdown("""[https://techne.labo.univ-poitiers.fr/nunc/](https://techne.labo.univ-poitiers.fr/nunc/)""") # spherical variagram...

	with col2:
		placeholder2 = st.empty()
		placeholder2.markdown("Projet financé par la [Fondation Maison des Sciences de l’Homme](https://www.fmsh.fr/fr/projets-soutenus/nouveaux-usages-du-numerique-et-continuites-analyse-automatisee-des-alertes)")



mid_container = st.container()
with mid_container:

	keyword = st.selectbox(
		'Choisissez une terme de recherche',
		("pédagogique", "continuité pédagogique", "enseignement à distance")
	)
	st.header("Google Trends (tendences recherche) for " + keyword)

	region_selected = st.selectbox(
    'Choisissez une région',
		("Alsace", "Aquitaine", "Auvergne","Basse-Normandie","Bourgogne",
		"Bretagne","Centre","Champagne-Ardenne","Franche-Comté",
		"Haute-Normandie","Île-de-France","Languedoc-Roussillon","Limousin",
		"Lorraine","Midi-Pyrénées","Nord-Pas-de-Calais","Pays-de-la-Loire",
		"Picardie","Poitou-Charentes","Provence-Alpes-Côte-dAzur","Rhône-Alpes")
	)
	lissage = st.selectbox(
		'Lissage?',
		("Savitzky-Golay", "aucun")
	)


	currwd = os.path.dirname(os.path.realpath(__file__))
	fpath = currwd + "/data/"

	if keyword == "pédagogique":
		whichdata = 'pedag'
	elif keyword == "continuité pédagogique":
		whichdata = "cont_pedag"
	elif keyword == "enseignement à distance":
		whichdata = "enseignement_distance"
	else:
		print('error - unidentified data')

	gtreg = load_all_data_regions(fpath, whichdata)
	rel_reg = gtreg[['date', region_selected]]
	rel_reg.columns = ['date', 'hits']
	rel_reg.index= range(len(rel_reg))

	if lissage == 'Savitzky-Golay':
		windowsize = min(23, len(rel_reg))
		poly_order = 3
		rel_reg = rel_reg.sort_values('date')

		rel_reg['smoothed'] = signal.savgol_filter(rel_reg['hits'], windowsize, poly_order)
		fig = px.line(rel_reg, x="date", y="smoothed", title='')
		st.plotly_chart(fig, use_container_width=True)
	else:
		st.line_chart(rel_reg[['date','hits']], x='date', y='hits')