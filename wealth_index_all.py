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

main = '/Users/janinedevera/Documents/School/MDS 2021-2023/Semester 2/3 Machine Learning/Project/Poverty/'
repo = main + 'ML-SS22/'
maps = main + 'Data/Maps/'
gdrive = '/Volumes/GoogleDrive/Shared drives/ML Project_Satellite Images and Poverty/'
dhs_vars = 'Outcome/Wealth Index/'
dhs_geo = 'Outcome/Geo Data/'
final_out = 'Outcome/Final Outcome/'

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

    # read final outcome geodf 
eth_gdf = gpd.read_file(gdrive + final_out + 'eth_gdf.shp')
mlw_gdf = gpd.read_file(gdrive + final_out + 'mlw_gdf.shp')
mli_gdf = gpd.read_file(gdrive + final_out + 'mli_gdf.shp')
ngr_gdf = gpd.read_file(gdrive + final_out + 'ngr_gdf.shp')

    # read country map
mlw_map = gpd.read_file(maps + 'Malawi/mwi_admbnda_adm3_nso_20181016.shp')
eth_map = gpd.read_file(maps + 'Ethiopia/eth_admbnda_adm2_csa_bofedb_2021.shp')
mli_map = gpd.read_file(maps + 'Mali/mli_admbnda_adm3_1m_gov_20211220.shp')
ngr_map = gpd.read_file(maps + 'Nigeria/NER_adm02_feb2018.shp')


    # gdf set up 
def genid (geodf):
    geodf['geoid'] = (~geodf.geometry.duplicated()).cumsum()
    return geodf

    # map function 
def genmaps (geodf, shp):
    coord = geodf[["geoid", "geometry"]]
    clus = geodf.groupby(["geoid"]).mean().reset_index()
    clus = pd.merge(coord, clus).drop_duplicates()
    join = gpd.sjoin(clus, shp, how = 'right', predicate = 'within')
    join = join[join['wealth'].notna()]
    img = join.plot(alpha=0.7, column = "wealth", cmap = "RdYlGn", legend=True, figsize=(6,8),
                 legend_kwds={'label': "Wealth Index"})
    img.set_axis_off();
    return img


    ## malawi
mlw_gdf = genid(mlw_gdf)
mlw_img = genmaps(mlw_gdf, mlw_map)

    ## ethiopia
eth_gdf = genid(eth_gdf)
eth_img = genmaps(eth_gdf, eth_map)

    ## mali
mli_gdf = genid(mli_gdf)
mli_img = genmaps(mli_gdf, mli_map)

    ## nigeria
ngr_gdf = genid(ngr_gdf)
ngr_img = genmaps(ngr_gdf, ngr_map)





    
    
    
    

