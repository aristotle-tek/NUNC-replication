# NUNC-replication
Fichiers réplication pour le projet Nouveaux Usages du Numérique et Continuités


## Introduction

Ce dépôt github est constitué de fichiers de réplication du projet NUNC! Analyse Automatisée des Alertes, de la [Laboratoire Techné](https://techne.labo.univ-poitiers.fr/nunc/), financé par la [Fondation Maison des Sciences de l’Homme](https://www.fmsh.fr/fr/projets-soutenus/nouveaux-usages-du-numerique-et-continuites-analyse-automatisee-des-alertes)
.

## Aperçu

Le code est basé sur trois aspects principaux, basés dans les dossiers correspondants :

1. Collecter des Tweets et effectuer une analyse des sentiments des données Twitter (nécessite un bearer token pour le [Twitter API v2 - gratuit pour les chercheurs](https://developer.twitter.com/en/products/twitter-api/academic-research) ).


2. Collecter de données sur les données de recherche Google (basé sur le travail "Predicting Initial Unemployment Insurance Claims Using Google Trends" de Paul Goldsmith-Pinkham et Aaron Sojourner)

3. Présenter ces informations dans une application Web interactive à l'aide de Streamlit.

Pour voir la webapp, [cliquez ici : https://aristotle-tek-nunc-multipageaccueil-0q1uwk.streamlit.app/](https://aristotle-tek-nunc-multipageaccueil-0q1uwk.streamlit.app/){:target="_blank"}




## Modèle d'analyse des sentiments

Le sentiment des tweets est analysé sur la base du [modèle CamemBERT](https://camembert-model.fr/), qui utilise l'architecture d'un Transformer. Pour plus de détailles en français, [voir un tutoriel de base ici](https://camembert-model.fr/posts/tutorial/)

CamemBERT est une adaptation de l'architecture RoBERTa, entraînée sur un corpus français pour fournir de meilleurs résultats en français. En plus du modèle CamemBERT, Theophile Blard a formé un modèle spécifiquement destiné à analyser les sentiments, basé sur des critiques de films. [Son code est disponible ici.](https://github.com/TheophileBlard/french-sentiment-analysis-with-bert)


