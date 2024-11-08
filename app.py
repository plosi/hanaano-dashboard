from shiny import App, render, reactive, ui
from shiny.types import FileInfo
from shinywidgets import output_widget, render_widget, render_plotly

import faicons as fa
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

from load_data import df, seasons
import load_text

MONTHS = ['J','F','M','A','M','J','J','A','S','O','N','D']
YEARS = [str(yr) for yr in df.year.unique()]

app_ui = ui.page_navbar(
    ui.nav_panel(
        'Rainfall',
        # 'Analysis of historical climate data',
        ui.layout_sidebar(
            ui.sidebar(
                ui.markdown("""Explore annual precipitations. 
                            Use the slider to select the year range, rainfall mean is calculated 
                            accordingly. The plots will update automatically."""),
                ui.input_slider(
                    id='year_slide', label='Year range', min=df.year.min(), max=df.year.max(), value=[df.year.min(),df.year.max()]
                ),
                # ui.input_selectize(
                #     id='year', label='Year', choices=YEARS, selected=YEARS[-1]
                # ),
                open='open',
            ),
            ui.layout_columns(
                ui.card(
                    output_widget('plot_rainfall'),
                    full_screen=True
                ),
                ui.card(
                    ui.div(load_text.annual_prec),
                ),
                ui.card(
                    output_widget('plot_rainfall_distribution'),
                    full_screen=True
                ),
                ui.card(
                    ui.div(load_text.rainfall_distr),
                ),
                # ui.card(
                #     output_widget('plot_rainfall_vs_mean'),
                #     full_screen=True
                # ),
                # col_widths=(12,6,6,12)
                col_widths=(12)
            )
        ),
    ),
    ui.nav_panel(
        'ENSO & IOD',
        ui.layout_sidebar(
            ui.sidebar(
                ui.markdown("""Explore interconnection with El Nino Southern Oscillation and Indian Ocean Dipole. 
                            Use the slider to select the year range and the dropdown to select the year.
                            The plots will update automatically."""),
                ui.input_slider(
                    id='year_slide_enso', label='Year range', min=df.year.min(), max=df.year.max(), value=[df.year.min(),df.year.max()]
                ),
                ui.input_selectize(
                    id='year_enso', label='Year', choices=YEARS, selected=YEARS[-1]
                ),
                open='open',
            ),
            ui.layout_columns(
                ui.card(
                    output_widget('plot_enso_iod'),
                    full_screen=True
                ),
                ui.card(
                    ui.div(load_text.enso_iod_interconn),
                ),
                ui.card(
                    output_widget('plot_rainfall_vs_mean'),
                    full_screen=True
                ),
                ui.card(
                    output_widget('plot_enso_iod_by_year'),
                    full_screen=True
                ),
                # ui.card(
                #     # output_widget('plot_corr_matrix'),
                #     ui.output_plot('plot_corr_matrix'),
                #     full_screen=True
                # ),
                # ui.card(
                #     ui.div(load_text.corr)
                # ),
                col_widths=(12,12,6,6)
            )
        ),
    ),
    ui.nav_panel(
        'Rainy Seasons',
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_slider(
                    id='season_threshold', label='Threshold', min=0, max=100, value=70, post='%'
                ),
            ),
            ui.layout_columns(
                ui.card(
                    ui.div(load_text.failed_season),
                ),
                ui.card(
                    output_widget('plot_failed_rains'),
                    full_screen=True
                ),
                col_widths=(12,12)
            )
        ),
    ),
    title='Hanaano Dashboard',
)

def server(input, output, session):
    # Reactive values to store parameter information
    clim_param = reactive.value()
    
    @reactive.calc
    def load_data():
        return df
    
    @reactive.calc
    def load_season_df():
        return seasons

    @render_widget
    def plot_rainfall():
        df = load_data()
        df = df.groupby(['year']).agg({'rain':'sum'}).reset_index()
        df = df[(df.year>=input.year_slide()[0]) & (df.year<=input.year_slide()[1])]
        title = f'Annual Precipitations | {min(df.year)} - {max(df.year)}'

        bar_chart = go.Bar(
            x=df.year,
            y=df.rain,
            name='Rainfall'
        )

        help_fig = px.scatter(df, x='year', y='rain', trendline='lowess')
        trendline = go.Scatter(
            x=help_fig['data'][1]['x'],
            y=help_fig['data'][1]['y'],
            mode='lines',
            name='Best-Fit'
        )

        fig = go.Figure(data=[bar_chart,trendline])
        fig.update_layout(title=title,xaxis_title=None,yaxis_title='Rainfall [mm/year]')

        return fig
    
    @render_widget
    def plot_rainfall_distribution():
        df = load_data()
        df = df[(df.year>=input.year_slide()[0]) & (df.year<=input.year_slide()[1])]
        title = f'Rainfall Distribution | Monthly Mean {min(df.year)} - {max(df.year)}'

        fig = px.box(
            data_frame=df,
            x='month',
            y='rain',
            title=title
        )

        fig.update_xaxes(title=None, labelalias=dict(zip([1,2,3,4,5,6,7,8,9,10,11,12], MONTHS)), tickmode='linear', nticks=len(df.month.unique()))
        fig.update_yaxes(title='Rainfall [mm/month]')

        return fig

    @render_widget
    def plot_rainfall_vs_mean():
        df = load_data()
        # df = df[(df.year>=input.year_slide_enso()[0]) & (df.year<=input.year_slide_enso()[1])]
        title = f'Monthly Rainfall ({input.year_enso()}) Vs. Mean ({min(df.year)} - {max(df.year)})'

        df_melted = df[df.year==int(input.year_enso())].melt(id_vars='month', value_vars=['rain', 'rain_mean'])
        df_melted['variable'] = df_melted['variable'].replace({'rain':'Rainfall', 'rain_mean':'Rainfall Mean'})

        fig = px.bar(
            data_frame=df_melted,
            x='month',
            y='value',
            barmode='group',
            color='variable',
            color_discrete_sequence=['blue','grey'],
            labels={'variable':''},
            opacity=.7,
            title=title
        )

        fig.update_xaxes(title=None, labelalias=dict(zip([1,2,3,4,5,6,7,8,9,10,11,12], MONTHS)), tickmode='linear', nticks=len(df.month.unique()))
        fig.update_yaxes(title='Rainfall [mm/month]')

        return fig
    
    @render_widget
    def plot_enso_iod_by_year():
        df = load_data()
        df_melted = df[df.year==int(input.year_enso())].melt(id_vars='month', value_vars=['enso', 'iod'])
        df_melted['variable'] = df_melted['variable'].replace({'enso':'ENSO', 'iod':'IOD'})
        title = f'Trend of ENSO and IOD Indices ({input.year_enso()})'

        fig = px.bar(
            data_frame=df_melted,
            x='month',
            y='value',
            barmode='group',
            color='variable',
            color_discrete_sequence=['lightgreen', 'orange'],
            labels={'variable':''},
            opacity=.7,
            title=title,
        )

        fig.update_xaxes(title=None, labelalias=dict(zip([1,2,3,4,5,6,7,8,9,10,11,12], MONTHS)), tickmode='linear', nticks=len(df.month.unique()))
        fig.update_yaxes(title='ENSO/IOD [degC]')
        return fig
    
    @render_widget
    def plot_enso_iod():
        df = load_data()
        df = df[(df.year>=input.year_slide_enso()[0]) & (df.year<=input.year_slide_enso()[1])]
        df['date'] = df.year.astype(str)+'-'+df.month.astype(str)
        df.index=pd.to_datetime(df.date)
        df.resample('ME').last()
        df = df.rename(columns={'enso':'ENSO', 'iod':'IOD'})
        title = f'Trend of ENSO and IOD Indices | {min(df.year)} - {max(df.year)}'

        fig = px.bar(
            data_frame=df,
            y=['ENSO','IOD'],
            barmode='group',
            color_discrete_sequence=['lightgreen', 'orange'],
            labels={'variable':''},
            title=title,
        )

        fig.update_layout(xaxis_title=None,yaxis_title='ENSO/IOD [degC]')
        return fig
    
    @render_widget
    def plot_failed_rains():
        def failed_rainy_season(data_frame):
            return True if data_frame.rain < input.season_threshold()/100. * data_frame.rain_mean else False
        
        seasons = load_season_df()
        seasons['failed'] = seasons.apply(failed_rainy_season, axis=1)
        df = seasons[seasons.failed]
        title=f'Failed Rainy Seasons [<{input.season_threshold()}% of the mean] ({min(seasons.year)}-{max(seasons.year)})'

        fig = px.bar(
            data_frame=df,
            x='year',
            y='rain',
            barmode='group',
            color='season',
        )

        fig.update_layout(title=title,xaxis_title=None,yaxis_title='Rainfall [mm/season]')
        return fig
    
    @render.plot
    def plot_corr_matrix():
        def failed_rainy_season(data_frame):
            return True if data_frame.rain < input.season_threshold()/100. * data_frame.rain_mean else False
        
        seasons = load_season_df()
        seasons['failed'] = seasons.apply(failed_rainy_season, axis=1)
        
        pi = pd.pivot(seasons, index='year', columns='season', values=['rain', 'enso', 'iod', 'failed'])
        # fig = px.imshow(
        #     pi.corr(),
        #     text_auto=True
        # )
        fig = sns.heatmap(
            pi.corr(),
            annot=True
        )

        return fig
    
app = App(app_ui,server)
