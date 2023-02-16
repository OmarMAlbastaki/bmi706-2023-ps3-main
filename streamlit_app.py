import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###

# `load_data` function {{ # }}

#@st.cache


def load_data():
    cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(  # type: ignore
        id_vars=["Country", "Year", "Cancer", "Sex"],
        var_name="Age",
        value_name="Deaths",
)

    pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
        id_vars=["Country", "Year", "Sex"],
        var_name="Age",
        value_name="Pop",
)

    df = pd.merge(left=cancer_df, right=pop_df, how="left")
    df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
    df.dropna(inplace=True)

    df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
    df["Rate"] = df["Deaths"] / df["Pop"] * 100_000
    return df
    


# Uncomment the next line when finished
df = load_data()

### P1.2 ###

st.write("## Age-specific cancer mortality rates")

### P2.1 ###
# replace with st.slider
#year = 2012
#subset = df[df["Year"] == year]
### P2.1 ###

o=st.slider("Year",
            min_value=df["Year"].min(),    ### minimum Year
            max_value=df["Year"].max(),    ### Maximum Year 
            value=2012 ### default Year
            )


## Sources Consulted: 
## https://docs.streamlit.io/library/api-reference/widgets/st.slider


### P2.2 ###
# replace with st.radio
#sex = "M"
#subset = subset[subset["Sex"] == sex]
### P2.2 ###


radio=st.radio("Sex",
                options=list((df["Sex"].unique()[-1], df["Sex"].unique()[0])),  ### [M, F]
                index=0 ### Setting first element as default, like in the provided demo
                )

### Sources Consulted:
### https://docs.streamlit.io/library/api-reference/widgets/st.radio




### P2.3 ###
# replace with st.multiselect
# (hint: can use current hard-coded values below as as `default` for selector)
countries = [
    "Austria",
    "Germany",
    "Iceland",
    "Spain",
    "Sweden",
    "Thailand",
    "Turkey",
]
#subset = subset[subset["Country"].isin(countries)]
### P2.3 ###

countries_select=st.multiselect("Countries",    
                                options=df["Country"].unique(),  
                                default=countries ## hard-coded values below as as `default` for selector
                                )


### Sources Consulted:
#https://docs.streamlit.io/library/api-reference/widgets/st.multiselect


### P2.4 ###
# replace with st.selectbox
#cancer = "Malignant neoplasm of stomach"
#subset = subset[subset["Cancer"] == cancer]
### P2.4 ###

select_box=st.selectbox("Cancer", 
                        options=df["Cancer"].unique()
                        )


### Sources Consulted:
### https://docs.streamlit.io/library/api-reference/widgets/st.selectbox

### P2.5 ###
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]


### Creating Subset Data Frame to account for all the filters done above from P2.1 to P2.4:

subset=df[(df["Country"].isin(countries_select)) & (df["Year"]==(o)) & (df["Cancer"]==(select_box)) & (df["Sex"]==(radio)) ]

## Source Consulted:https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html

### Creating P2.5 Heatmap:

chart = alt.Chart(subset).mark_rect().encode(
    x=alt.X("Age:O", sort=ages, axis=alt.Axis(grid=False, domain=False)), ### X Axis 
    color=alt.Color("Rate:Q",title="Mortality rate per 100k", scale=alt.Scale(type='log', domain=(0.01, 100), clamp=True), legend=alt.Legend()), ### Adapted from Problem Set 3 Notes
    y=alt.Y("Country:N", title="Country:N", axis=alt.Axis(grid=False,  domain=False)), ### Y axis 
    tooltip=["Rate:Q"], ### tolltip
   # stroke=alt.Stroke("Rate:Q",title="Mortality rate per 100k", scale=alt.Scale(type='log', domain=(0.01, 100), clamp=True),   fi)
   # fill=alt.Fill("Rate:Q", title="Mortality rate per 100k", scale=alt.Scale(type='log', domain=(0.01, 100), clamp=True)),
).properties(
    title=f"{select_box} mortality rates for {'males' if radio == 'M' else 'females'} in {o}",
).configure_axis(
    grid=False, domainOpacity=0
).configure_view(
    strokeWidth=0
).configure_scale(
    bandPaddingInner=0
).configure_mark(
    strokeOpacity=1,
    strokeWidth=0,
    stroke="blank",
    filled=True
)

### Sources Consulted for Above Plot:
### https://towardsdatascience.com/altair-plot-deconstruction-visualizing-the-correlation-structure-of-weather-data-38fb5668c5b1 
## https://stackoverflow.com/questions/65043393/how-to-remove-white-border-line-of-rectangles-in-altair-heatmap-mark-rect-plots
### https://groups.google.com/g/altair-viz/c/Vd3p6N0NScw?pli=1
## https://github.com/altair-viz/altair/issues/976 
## https://stackoverflow.com/questions/61142744/is-it-possible-to-add-black-grid-lines-to-python-altair-heatmap-plots



#### Note: I am not sure if the barplot in the demo is part of P2.5 or demo. The language in the bonus question was very confusing for me.
#### Just to be safe, I will add it as part of P2.5. 

### Creating P2.5 barplot of population size by selected country:


chart2 = alt.Chart(subset).mark_bar().encode(
    x=alt.X("sum(Pop):Q",title="Sum of Population Size"), ### X axis
    y=alt.Y("Country", sort="-x", title="Country", axis=alt.Axis(grid=False,  domain=False)), #### Y Axis 
    tooltip=[alt.Tooltip("sum(Pop):Q",  title="Sum of Population Size"), ## Toltip as shown in Demo
    "Country"]
)


### Sources Consulted for Above Plot:
## https://altair-viz.github.io/gallery/simple_heatmap.html
## https://github.com/altair-viz/altair/issues/1770#issuecomment-695751795
## https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html
## https://stackoverflow.com/questions/66347857/sort-a-normalized-stacked-bar-chart-with-altair
## https://vega.github.io/vega/docs/schemes/
## https://altair-viz.github.io/user_guide/customization.html




##### BONUS #####:

#### a bar chart which shows the population size by country for a selected age group would provide useful context when examining the normalized mortality rates in the heatmap.

chart3 = alt.Chart(subset).mark_bar().encode(
    x=alt.X("sum(Pop):Q",title="Percentage of Population Size (%)",  stack="normalize"), ### Normalized X Xais
    y=alt.Y("Country", sort="-x", title="Country", axis=alt.Axis(grid=False,  domain=False)), ### Y Axis 
    color=alt.Color("Age", sort=ages, scale=alt.Scale(scheme='set3')), ### Color by Age 
    order=alt.Order("color_Age_sort_index:Q") ### order by age groups
    ).configure_axis(
    grid=False, domainOpacity=0
).transform_joinaggregate( ### calculate percentage of population size for each group per country
    total='sum(Pop):Q',
    groupby=['Country']  
).transform_calculate(
    perc=alt.datum.Pop / alt.datum.total ### calculate percentage of population size for each group per country
).encode(tooltip=
         [alt.Tooltip("sum(Pop):Q",  title="Sum of Population Size"),
         alt.Tooltip("perc:Q",  title="\% of Population Size",  format='.0%'),
          "Country", 
          "Year", 
          "Age:O"]
)



### Sources Consulted for Above Plot:
### https://altair-viz.github.io/gallery/normalized_stacked_bar_chart.html
## https://stackoverflow.com/questions/66347857/sort-a-normalized-stacked-bar-chart-with-altair
## https://stackoverflow.com/questions/65206783/how-to-display-normalized-categories-in-altair-stacked-bar-chart-tooltip


#### Plotting All Plots ### 

st.altair_chart(chart, use_container_width=True)
st.altair_chart(chart2, use_container_width=True)
st.altair_chart(chart3, use_container_width=True)


countries_in_subset = subset["Country"].unique()
if len(countries_in_subset) != len(countries_select):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries_select) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")
