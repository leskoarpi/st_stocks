import streamlit as st
import yfinance as fn
import csv

#using session state variables to initialize the dictionary
if 'ticker_dict' not in st.session_state:
    st.session_state.ticker_dict = {}
file_path = './nasdaq.csv'

# Reading the CSV file and store Ticker: Name pairs in the dictionary
with open(file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        st.session_state.ticker_dict[row['Symbol']] = row['Name']


#dropdown menu for stock selection and data display options

with st.sidebar:
    st.title("Select company info")
    selected_ticker = st.selectbox('Select Ticker', options=list(st.session_state.ticker_dict.keys()))
    def getticker(selected_ticker):
        ticker = fn.ticker(selected_ticker)
        return ticker
    if selected_ticker:
        company = st.session_state.ticker_dict[selected_ticker]
        st.write(f"Name: {company}")

    #select info to download and display about stock
    select_period = st.selectbox('select prefered time period',('1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max'))
    select_interval = st.selectbox('select prefered time interval',('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'))
    start_date =  st.date_input('Select starting date')
    end_date = st.date_input('Select ending date')
    select_prepost = st.selectbox('Include Pre and Post regular market data in results?', (True, False))
    select_auto_adjust = st.selectbox('Adjust all OHLC (Open/High/Low/Close prices) automatically?', (True, False))
    


#fetching data
    

tab = st.empty()
tab_i = st.empty()

with st.sidebar:
    if st.button("Show me"):
        with tab:
            fetch = fn.download(tickers=selected_ticker, start=start_date, end=end_date, period=select_period, interval=select_interval, prepost=select_prepost, auto_adjust=select_auto_adjust)
            
            st.line_chart(fetch.values)
        with tab_i:
            st.write(fetch.info)
