Files in this folder are related to the KDD paper:

Mayank Kejriwal, Haotian Zhang,
Pedro Szekely and Michael Tamayo. 2017. THOR: Text-enabled Humanitarian
Operations in Real Time. In Proceedings of ACM KDD conference,
Halifax, Nova Scotia, Canada, August 2017 (KDD’17), 10 pages.
DOI: 10.475/123 4

Here is a general description of the scripts:

PlotThree.py: 
It plots the three plots: timestamp only, jaccard and tfidf. Each plot contains results of precision and recall evaluation for next doc prediction experiments based on entity field and word cloud field of the documents. 

KDDDataPrep.py: 
It prepares all the data, and calculates basic statistics like word count, entity count, time span calculaton, etc.

GenNext.py: 
APIs used to generate next document prediction in time series and perform related evaluations and plots. This is still ongoing and not a stable release. 

tf_idf.py: 
An efficient TF-IDF library. Credit: https://github.com/hrs/python-tf-idf.

GroundTruth.py: 
Simple code snippets to generate ground truth.

I am not allowed to reveal data here, so the dataset is not posted.
