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
wealth = wealth_all[["hv000", "hv001", "hv007", "hv270", "hv271", "hv270a", "hv271a"]]
wealth['hv000'] = wealth['hv000'].str.replace('7', '')
wealth['mergeid'] = wealth['hv000'] + '-' + wealth['hv001'].map(str)

    # geotags
os.chdir(gdrive + dhs_geo)

extension = 'shp'
geo_filenames = [i for i in glob.glob('*.{}'.format(extension))]

geo_all = pd.concat([gpd.read_file(f) for f in geo_filenames])
geo_all['mergeid'] = geo_all['DHSCC'] + '-' + geo_all['DHSCLUST'].astype(int).astype(str)

    # merge wealth data with geodata
outcome_gdf = geo_all.merge(wealth, left_on = 'mergeid', right_on='mergeid')

    # create geoid
outcome_gdf = outcome_gdf[["DHSID", "hv000", "LATNUM", "LONGNUM", "geometry", "hv270a", "hv271"]]
outcome_gdf['hv271'] = (outcome_gdf['hv271'] / 100000)
outcome_gdf.rename(columns = {'hv000':'country', 'hv270a':'category', 'hv271':'wealth'}, inplace = True)
outcome_gdf['category'] = outcome_gdf['category'].astype(str)

    # save
os.chdir(repo)
outcome_gdf.to_file("outcome_gdf.shp")

    # ethiopia
eth_gdf = outcome_gdf[outcome_gdf['country'] == 'ET']
eth_gdf.to_file("eth_gdf.shp")

    # malawi
mlw_gdf = outcome_gdf[outcome_gdf['country'] == 'MW']
mlw_gdf.to_file("mlw_gdf.shp")

    # mali
mli_gdf = outcome_gdf[outcome_gdf['country'] == 'ML']
mli_gdf.to_file("mli_gdf.shp")

    # nigeria
ngr_gdf = outcome_gdf[outcome_gdf['country'] == 'NG']
ngr_gdf.to_file("ngr_gdf.shp")



####### MAPS

#outcome_gdf['geoid'] = (~outcome_gdf.geometry.duplicated()).cumsum()


    # cluster dataset
ml_geo = ml_gdf[["geoid", "geometry"]]
ml_plot = ml_gdf.groupby(["geoid"]).mean().reset_index()
ml_plot = pd.merge(ml_geo, ml_plot).drop_duplicates()



    
    
    
    

