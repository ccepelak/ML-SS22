#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 14:47:41 2022

@author: janinedevera
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import fiona
import os, glob


## DIRECTORIES

repo = '/Users/janinedevera/Documents/School/MDS 2021-2023/Semester 2/3 Machine Learning/Project/Poverty/ML-SS22'
gdrive = '/Volumes/GoogleDrive/Shared drives/ML Project_Satellite Images and Poverty/'
dhs_vars = 'Outcome/Wealth Index/'
dhs_geo = 'Outcome/Geo Data'

## OUTCOME VARIABLES

    # wealth index

os.chdir(gdrive + dhs_vars)

extension = 'DTA'
wealth_filenames = [i for i in glob.glob('*.{}'.format(extension))]

wealth_all = pd.concat([pd.read_stata(f) for f in wealth_filenames])
wealth_clusters = wealth_all.iloc[:, 1:9]
wealth_index = wealth_all[["hv270", "hv271", "hv270a", "hv271a"]]
wealth = pd.merge(wealth_clusters, wealth_index, left_index = True, right_index = True)

    # geotags
os.chdir(gdrive + dhs_geo)

extension = 'shp'
geo_filenames = [i for i in glob.glob('*.{}'.format(extension))]

geo_all = pd.concat([gpd.read_file(f) for f in geo_filenames])

    # merge wealth data with geodata
outcome_gdf = geo_all.merge(wealth, left_on = 'DHSCLUST', right_on='hv001')

    # create geoid
outcome_gdf = outcome_gdf[["DHSID", "LATNUM", "LONGNUM", "geometry", "hv271"]]
outcome_gdf['hv271'] = (outcome_gdf['hv271'] / 100000)
#outcome_gdf['geoid'] = (~outcome_gdf.geometry.duplicated()).cumsum()

os.chdir(repo)

outcome_gdf.to_file("ml_gdf.shp")

    # cluster dataset
ml_geo = ml_gdf[["geoid", "geometry"]]
ml_plot = ml_gdf.groupby(["geoid"]).mean().reset_index()
ml_plot = pd.merge(ml_geo, ml_plot).drop_duplicates()



    
    
    
    

