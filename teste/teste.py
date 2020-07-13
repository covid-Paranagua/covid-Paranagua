import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point, Polygon

sf_path = "pr_municipios/41MUE250GC_SIR.shp"
sf = gpd.read_file(sf_path, encoding='utf-8')
sf_pgua = sf[sf.NM_MUNICIP == 'PARANAGUÁ']
#shape_pgua = sf_pgua.to_crs({'init': 'epsg:4326'})
#shape_pgua.plot()
sf_pgua.plot()
