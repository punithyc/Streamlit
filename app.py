import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='StartUp Analysis')
df=pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year


def load_overall_analysis():
    st.title('Overall Analysis')
    #total invested amount
    total=round(df['amount'].sum(), 2)
    # max_funding
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    #average funding
    avg_funding=df.groupby('startup')['amount'].sum().mean()
    # Total funded startups
    num_startups=df['startup'].nunique()
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total',str(total)+'Cr')
    with col2:
        st.metric('Total',str(max_funding)+'Cr')
    with col3:
        st.metric('Avg',str(round(avg_funding))+'Cr')
    with col4:
        st.metric('Funded Startups',str(num_startups))

    st.header('MOM graph')
    selected_option=st.selectbox('select type',['Total','Count'])
    if selected_option=='Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig3)

def load_investor_details(investor):
    st.title(selected_investor)
    #load the recent 5 investments
    last5_df=df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most recent Investments')
    st.dataframe(last5_df)

    col1,col2=st.columns(2)
    #biggest investments
    with col1:
        big_series=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig,ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    with col2:
        vertical_series=df[df['investors'].str.contains(investorc)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="0.01f")
        st.pyplot(fig1)
#year over year investments
    df['year']=df['date'].dt.year
    year_series=df[df['investors'].str.contains(' IDG Ventures')].groupby('year')['amount'].sum()
    st.subheader('YOY Investments')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)
    st.pyplot(fig2)

st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('select one',['overall analysis','startup','investor'])

if option=='overall analysis':
        load_overall_analysis()
elif option=='startup':
    st.sidebar.selectbox('select startup',df['startup'].unique().tolist())
    btn1=st.sidebar.button('Find startup details')
    st.title('Startup Analysis')
else:
    selected_investor=st.sidebar.selectbox('select startup',sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Investor details')
    if btn2:
        load_investor_details(selected_investor)

    st.title('Investor Analysis')