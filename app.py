import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import seaborn as sns

st.set_option('deprecation.showPyplotGlobalUse', False)

sns.set()

DATA_URL = (
    "fatal-police-shootings-data.csv"
)

st.title("Exploratory Data Analysis: Fatal Police Shootings in US")

st.sidebar.title("EDA: Fatal Police Shootings in the US")

st.markdown("This application is a Streamlit dashboard used "
            "to analyze Fatal Polce Shootings in US")
st.sidebar.markdown("This application is a Streamlit dashboard used "
            "to analyze Fatal Polce Shootings in US")


@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    
    return data

data = load_data()


if st.checkbox("Preview DataFrame"):
    if st.button("Head"):
        st.write(data.head())
    if st.button("Tail"):
        st.write(data.tail())
    else:
         st.write(data.head(2))

    # Show Entire Dataframe
if st.checkbox("Show All DataFrame"):
    st.dataframe(data)

    # Show All Column Names
if st.checkbox("Show All Column Name"):
    st.text("Columns:")
    st.write(data.columns)

    # Show Dimensions and Shape of Dataset
data_dim = st.radio('What Dimension Do You Want to Show',('Rows','Columns'))
if data_dim == 'Rows':
    st.text("Showing Length of Rows")
    st.write(len(data))
if data_dim == 'Columns':
    st.text("Showing Length of Columns")
    st.write(data.shape[1])

    # Show Summary of Dataset
if st.checkbox("Show Summary of Dataset"):
    st.write(data.describe())


st.sidebar.markdown("### Select the Column to Visualize")


each_airline = st.sidebar.selectbox('Attributes', ['Manner of Death', 'Gender', 'Armed', 'Age', 'Race', 'State'], key='2')

if each_airline == 'Manner of Death':
    st.subheader("Manner of Death")
    
    ax = sns.countplot(x='manner_of_death', data=data)
    for p in ax.patches:
        x = p.get_bbox().get_points()[:,0]
        y = p.get_bbox().get_points()[1,1]

        ax.annotate('{:.2g}%'.format(100.*y/len(data)), (x.mean(), y), ha='center', va='bottom')

    plt.title('Manner of death')
    plt.show()
    st.pyplot()
    st.subheader('Observation:\nIn **95%** of the cases, the individual was shot and killed and in **5%** of the total cases he/she was tasered and shot dead')

        
        
if each_airline == 'Gender':
    st.subheader("Gender")
    
    # Plot police killings by gender
    ax = sns.countplot(x = "gender", data = data,
                   order = data.gender.value_counts().index)
    for p in ax.patches:
        x = p.get_bbox().get_points()[:,0]
        y = p.get_bbox().get_points()[1,1]
        ax.annotate('{:.2g}%'.format(100.*y/len(data)), (x.mean(), y), ha='center', va='bottom')
    plt.title('Police Killings by Gender')
    plt.show()
    st.pyplot()
    st.subheader('Observation:\nMost of the individuals shot by police were male \n This is expected because females commit less crimes comparative to males')



#Weapons Use by Victims

if each_airline == 'Armed':
    st.subheader("Armed")
    # Plot the 20 most common weapons used by individuals shot
    ax = sns.countplot(y='armed', data=data,
                   order = data.armed.value_counts().iloc[:20].index)
    plt.title('Weapon used by person shot')
    plt.show()
    st.pyplot()
    st.subheader('Observation:\n Most of the victims had a **Gun** or a **Knife** at time of incident')
    st.subheader('An alarmingly high proportion of individuals shot by police were either **Unarmed** or **Armed** with a **Toy Weapon**')


if each_airline == 'Age':
    st.subheader("Age")
    
    sns.distplot(data.age[~np.isnan(data.age)])
    plt.title('Age of individuals shot by police')
    plt.show()
    st.pyplot()
    st.subheader('Observation:\n Most of the individuals shot and killed by police were between the ages of 20 and 40, with very few older than 80 or younger than 16')





def ActualVsPopulation(df, pop, group):
    """Get dataframe with actual per-group percentage vs population group percentage"""
    d = {group: [], 'type': [], 'percent': []}
    tot_pop = float(sum(pop.values()))
    for g in df[group].dropna().unique(): #for each group

        # Actual percentages
        d[group].append(g)
        d['type'].append('Killings')
        d['percent'].append(100*df[df[group]==g].id.count()/df.id.count())

        # Percentages if statistic followed population distribution
        d[group].append(g)
        d['type'].append('Population') #based on population percentage
        d['percent'].append(100*pop[g]/tot_pop)
        
    return pd.DataFrame(data=d)


if each_airline == 'Race':
    st.subheader("Race")
    # Plot percent police killings by race vs population percentages

#Population (%) by race gathered from https://www.census.gov/quickfacts/fact/table/US

    pop_r = {'W': 60.1, # White  
         'B': 13.4, # Black or African american
         'H': 18.5, # Hispanic or Latino
         'A': 5.9,  # Asian
         'N': 1.5,  # American indian, Alaska Native, Native Hawaian, and Other Pacific Islander
         'O': 0.6}  # other



    df = ActualVsPopulation(data, pop_r, 'race')

    sns.barplot(x="race", y="percent", hue="type", data=df,
            order = data.race.value_counts().index, palette=["r", "C0"])
    plt.title('Actual Police Killings vs Population Distribution (by Race)')
    plt.show()
    st.pyplot()
    st.subheader('Observation:\n Although half of the people shot and killed by police are **White**, **Black Americans** are shot at a disproportionate rate. They account for less than **14** percent of the U.S. population, but are killed by police at more than twice the rate of white Americans')



if each_airline == 'State':
    st.subheader("State Wise Analysis")
    plt.figure(figsize = (12,10))
    
    sns.countplot(y="state", 
              data=data,
              order=data.state.value_counts().index)
    plt.title('Police Killings By State')
    plt.show()
    st.pyplot()
    st.subheader('Observation:\nCalifornia is the state with the Highest Number of Killings followed by Texas, Florida, Arizona, and so on')









