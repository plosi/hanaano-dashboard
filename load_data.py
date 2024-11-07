from pathlib import Path
import pandas as pd
import numpy as np

from shiny import ui

app_dir = Path(__file__).parent

clim_df = pd.read_csv(app_dir/'data\\climate_all.csv')
enso_df = pd.read_csv(app_dir/'data\\enso.csv')
iod_df = pd.read_csv(app_dir/'data\\dmi_iod_v01.csv')

enso_full = pd.merge(
    left=enso_df,
    right=iod_df,
    how='left',
    on='date'
)

tmp = pd.merge(
    left=clim_df,
    right=enso_full,
    how='left',
    on='date'
).drop(['year_y', 'month_y', 'clim_adjust', 'total'], axis=1).rename(columns={'year_x':'year', 'month_x':'month', 'anom':'enso', 'dmi_iod':'iod'})

avged = tmp.groupby(['month']).agg({'rain':['mean','std']}).reset_index()
avged.columns = avged.columns.droplevel(0)
avged.columns = ['month','rain_mean','rain_std']

df = pd.merge(
    left=tmp,
    right=avged,
    on='month',
    how='inner'
)

LONG_RAINS = [3,4,5]
SHORT_RAINS = [10,11,12]

def create_season_col(series):
    if series in LONG_RAINS:
        return 'long rains'
    elif series in SHORT_RAINS:
        return 'short rains'
    else:
        return np.nan

tmp = df.copy()
tmp['season'] = tmp.month.apply(create_season_col)

seasons = tmp.groupby(['year','season']).agg({'rain':'mean', 'enso':'mean', 'iod':'mean'}).reset_index()
monthly_avged_seasons = tmp.groupby(['season']).agg({'rain':['mean','std']}).reset_index()
monthly_avged_seasons.columns = monthly_avged_seasons.columns.droplevel(0)
monthly_avged_seasons.columns = ['season', 'rain_mean', 'rain_std']

seasons = pd.merge(
    left=seasons,
    right=monthly_avged_seasons,
    on='season',
    how='inner'
)