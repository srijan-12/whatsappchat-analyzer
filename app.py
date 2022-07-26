import streamlit as st
import matplotlib.pyplot as plt
import helper
import preprocessor
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
     bytes_data = uploaded_file.getvalue()
     data=bytes_data.decode("utf-8")
     # st.text(data)
     df=preprocessor.preprocess(data)
     # st.dataframe(df)
     user_list=df['user'].unique().tolist()
     user_list.remove("group_notification")
     user_list.sort()
     user_list.insert(0,"Overall")
     selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

     if st.sidebar.button("Show Analysis"):
          # pass

          num_messages,words,num_media_messages,num_links= helper.fetch_stats(selected_user,df)
          st.title("Top Statistics")
          col1,col2,col3,col4=st.columns(4)

          with col1:
               st.header("Total Messages")
               st.title(num_messages)
          with col2:
               st.header("Total Words")
               st.title(words)
          with col3:
               st.header("Media Shared")
               st.title(num_media_messages)
          with col4:
               st.header("Links Shared")
               st.title(num_links)



          #Monthly_timeline
          st.title("Monthly Timeline")
          timeline=helper.monthly_timeline(selected_user,df)
          fig,ax=plt.subplots()
          ax.plot(timeline['time'], timeline['message'],color='green')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          # daily_timeline
          st.title("Daily Timeline")
          daily_timeline = helper.daily_timeline(selected_user, df)
          fig, ax = plt.subplots()
          ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)


          # activity_map
          st.title('Activity Map')
          col1,col2=st.columns(2)

          with col1:

              st.header('Most Busy Day')
              busy_day=helper.week_activity_map(selected_user,df)
              fig,ax=plt.subplots()
              ax.bar(busy_day.index,busy_day.values)
              plt.xticks(rotation='vertical')
              st.pyplot(fig)
          with col2:
               st.header('Most Busy Month')
               busy_month = helper.month_activity_map(selected_user, df)
               fig, ax = plt.subplots()
               ax.bar(busy_month.index, busy_month.values,color='orange')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)

          st.title('Weekly Activity Map')
          user_heat_map=helper.activity_heat_map(selected_user,df)
          fig,ax=plt.subplots()
          ax=sns.heatmap(user_heat_map)
          st.pyplot(fig)





          if selected_user=='Overall':
               st.title('Most Busy Users')
               x,new_df=helper.most_busy_users(df)
               fig,ax=plt.subplots()
               # ax.bar[x.index,x.values]
               # st.pyplot(fig)
               col1,col2=st.columns(2)

               with col1:
                    ax.bar(x.index, x.values,color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
               with col2:
                    st.dataframe(new_df)
#           word_cloud
          st.title("WordCloud")
          df_wc = helper.create_wordcloud(selected_user,df)
          fig,ax=plt.subplots()
          ax.imshow(df_wc)
          st.pyplot(fig)

#           most common words
          most_common_df=helper.most_common_words(selected_user,df)
          fig,ax=plt.subplots()
          ax.barh(most_common_df[0],most_common_df[1])
          plt.xticks(rotation='vertical')
          st.title('Most Common Words')
          st.pyplot(fig)


          # # emojii analysis
          # emoji_df=helper.emoji_helper(selected_user, df)
          # st.dataframe(emoji_df)


