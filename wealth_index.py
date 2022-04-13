#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 21:56:54 2022

@author: janinedevera
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import fiona

path = '/Users/janinedevera/Documents/School/MDS 2021-2023/Semester 2/3 Machine Learning/Project/Poverty/Data/DHS/Malawi_2015-16_DHS/'
dhs_dict_file  = path+'DHS/MWHR7AFL.DO' # DHS data dictionary (use as column name)
dhs_file = path+'MWHR7ADT/MWHR7AFL.DTA'  # household record data
dhs_geo = path+'MWGE7AFL/MWGE7AFL.shp'

ml = pd.read_stata(dhs_file)
ml_clus = ml.iloc[:, 1:9]
ml_wealth = ml[["hv270", "hv271", "hv270a", "hv271a"]]
ml_sample = pd.merge(ml_clus, ml_wealth, left_index=True, right_index=True)

shape = gpd.read_file(dhs_geo)
print(shape)

# merge wealth data with geodata
ml_gdf = shape.merge(ml_sample, left_on = 'DHSCLUST', right_on='hv001')
print(ml_gdf)

# create geoid
ml_gdf = ml_gdf[["DHSID", "LATNUM", "LONGNUM", "geometry", "hv271"]]
ml_gdf['hv271'] = (ml_gdf['hv271'] / 100000)
ml_gdf['geoid'] = (~ml_gdf.geometry.duplicated()).cumsum()

ml_gdf.to_file("ml_gdf.shp")

# cluster dataset
ml_geo = ml_gdf[["geoid", "geometry"]]
ml_plot = ml_gdf.groupby(["geoid"]).mean().reset_index()
ml_plot = pd.merge(ml_geo, ml_plot).drop_duplicates()


##### 

mapspath = '/Users/janinedevera/Documents/School/MDS 2021-2023/Semester 2/3 Machine Learning/Project/Poverty/Data/Maps/Malawi/'
mlpath = mapspath+'mwi_admbnda_adm3_nso_20181016.shp'

ml_map = gpd.read_file(mlpath)

ml_join = gpd.sjoin(ml_plot, ml_map, how = 'right', op='within')
ml_join = ml_join[ml_join['hv271'].notna()]

#####

img = ml_join.plot(alpha=0.7, column = "hv271", cmap = "OrRd", legend=True, figsize=(6,8),
             legend_kwds={'label': "Wealth Index"})
img.set_axis_off();

img.figure.savefig('Malawi.png')