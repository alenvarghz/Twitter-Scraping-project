import streamlit as st
import pandas as pd
import datetime
import snscrape.modules.twitter as sntwitter
st.header(':blue[_TWEETY_]')
st.subheader(':blue[_lets scrape some data_]')




st.image("twitterrr.jpg")

with st.form(key='twitter_form'):
    search_term = st.text_input('What do you want to search for?')
    limit = st.slider('How many tweets do you want to get?', 0, 1000, step=20)
   
    file_name = st.text_input('Name the CSV file:')
   
    start_date=st.date_input("starting date",datetime.date(2000,1,1))
    end_date=st.date_input("ending date",datetime.date(2020,1,1))
    submit_button = st.form_submit_button(label='display')
    
    if submit_button:
        
        query = f"(from:{search_term}) until:{end_date} since:{start_date}"
        tweets = []
        limit = limit
        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            if len(tweets) == limit:
                break
            else:
                tweets.append([tweet.date, tweet.user, tweet.content, tweet.url, tweet.id, tweet.replyCount, tweet.retweetCount,
                       tweet.source, tweet.likeCount])
        df = pd.DataFrame(tweets,
                  columns=['Date', 'User', 'Tweet', 'Url', 'Id', 'Replycount', 'Retweetcount', 'Source', 'Likecount'])
        
        df.to_csv(f'{file_name}.csv')
        data=pd.read_csv(f'{file_name}.csv')
        st.dataframe(data)
        

try:
    def convert_df(df):
        return df.to_csv().encode()
    st.download_button(label="Download data as CSV",data=convert_df(data) ,file_name='tweets.csv',mime='text/csv')
except:
    pass
try:
    st.button("Upload to Database")
    if st.button:
        import pymongo
        client = pymongo.MongoClient("mongodb+srv://alen:1234@cluster0.yrmsenw.mongodb.net/?retryWrites=true&w=majority")
        db = client.test1
        x=db.twitter
        
        import pandas as pd
        df=pd.read_csv(f"{file_name}.csv")
        dataa=df.to_dict('records')
        x.insert_many(dataa)
        
        
except :
    pass
