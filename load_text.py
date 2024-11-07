from shiny import ui

annual_prec = ui.markdown(
    """
    #### Annual Precipitations

    1.	**General Rainfall Pattern**: The annual rainfall varies significantly from year to year, indicating fluctuations in precipitation. Some years show notably higher rainfall peaks, such as around the mid-1990s and early 2020s, while others are much lower.
    2.	**Long-term Trend**: The best-fit line (red) shows a slight upward trend over the period from 1980 to 2024. This suggests a potential increase in average annual rainfall in the study area over time, although the variability around this trend is quite high.
    3.	**Recent Variability**: From the late 2010s into the 2020s, rainfall seems to have increased, with some of the highest values recorded in the early 2020s. This recent rise could be due to various factors, including natural climate variability, regional climate changes, or global climate influences.
    4.	**Partial Data for 2024**: Since 2024 data only extends to April, its rainfall appears lower than full-year values. This partial data may impact the trend interpretation if analyzed without adjustment for seasonality or partial year effects.

    In summary, while there is considerable inter-annual variability, the general trend indicates a slight increase in precipitation over the decades. The peaks and fluctuations suggest a potential influence from regional or global climate phenomena, which could be further explored in relation to events like ENSO and IOD.
    """
)

rainfall_distr = ui.markdown(
    """
    #### Rainfall Distribution

    1.	**Seasonal Variation**: The plot shows a clear seasonal pattern, with distinct rainy months and dry months. April and November experience the highest rainfall, indicated by their higher median and wider interquartile range (IQR), suggesting these months are part of the main rainy seasons.
    2.	**Rainfall Peaks and Outliers**: April has the most significant rainfall variability, shown by a wide spread of data points and several outliers that reach much higher levels. Similarly, October and November have notable outliers, indicating occasional peaks in rainfall that deviate from typical monthly values.
    3.	**Drier Months**: The months from June to September show consistently low rainfall, with relatively compact box plots and few outliers. This suggests a dry season, with rainfall generally low and less variable during these months.
    4.	**Data Dispersion and Consistency**: January, February, and December show moderate rainfall with some outliers, indicating occasional spikes. However, these months are less variable than the peak months of April and November.
    5.	**Long Rains (MAM - March, April, May)**: The months of March, April, and May show higher median rainfall compared to other months, with April displaying the highest median and widest interquartile range (IQR). This suggests a pronounced rainy season during these months, which is consistent with what is typically referred to as the "long rains" season in many East African regions.
    6.	**Short Rains (OND - October, November, December)**: October, November, and December also exhibit elevated rainfall, with November showing a significant median and a wide spread of values. This pattern aligns with the "short rains" season. Notably, the box plots for these months contain more outliers and wider IQRs, especially in November, indicating greater variability in rainfall amounts during the short rains.
    7.	**Higher Variability in Short Rains**: The short rains (OND) indeed display more variability, as shown by the numerous outliers and the wider spread of values in the box plots for October and November. This variability suggests that the short rains are less consistent in intensity and duration compared to the long rains, potentially due to influences from large-scale climate phenomena like the Indian Ocean Dipole (IOD) or El Niño-Southern Oscillation (ENSO), which are known to affect the short rains in this region.

    """
)

enso_iod_interconn = ui.markdown(
    """
    ### Exploring the impact of ENSO and IOD
    Remote teleconnections, namely the El Nino-Southern Oscillation and the Indian Ocean Dipole, exert a dominant influence on interannual variability of rainfall in the area of study.
    The IOD and ENSO physically influence Eastern African short rains by modifying regional atmospheric circulation features.

    The positive IOD is linked with wetter short rains over Eastern Africa. In contrast, the negative IOD (defined by a sustained negative SST difference of at least 0.4 degC) is associated with weaker short rains.
    El Nino conditions (positive ENSO), associated with warmer SST anomalies over the central and eastern Pacific, typically result in wetter short rains, whereas La Nina conditions (negative ENSO), associated with cooler SST anomalies, result in drier short rains.
    """
)

failed_season = ui.markdown(
    """
    ### Failed Rainy Seasons
    Use the slider to set an arbitrary threshold to define a failed rainy season. For instance, if the total amount of precipitation is below a certain percentage of the mean seasonal rainfall, then the rainy season is considered as *failed*.
    The chart shows only the rainy seasons that are deemed *failed* according to this arbitrary definition, categorized by long and short.

    This is an arbitrary definition and needs to be confirmed against historical observations from literature sources (e.g. droughts, crop fail, etc.).
    """
)

corr = ui.markdown(
    """
    #### Impact of ENSO/IOD on rainy seasons
    - Rainfall during the long rains seasons seem to be little influenced by ENSO and IOD.
    - Rainfall during the short rains seasons seem to be influenced by both ENSO (Pearson 0.46) and IOD (Pearson 0.72).
    - Failed long rains seasons seem to be weakly influenced by IOD (Pearson 0.3): positive IOD can result in failed season.
    - Failed short rains seasons seem to be influenced by both ENSO (Pearson -0.39) and IOD (Pearson -0.46): negative ENSO/IOD can result in faild season.
    """
)