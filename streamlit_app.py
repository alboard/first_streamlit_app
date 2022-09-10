import streamlit as st
import pandas as pd
import requests
import snowflake.connector as snow    
from urllib.error import URLError

st.header('🍌🥭 Breakfast Favourites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie')
my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected=st.multiselect('Pick some fruits:', list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
st.dataframe(fruits_to_show)

st.header('🍌🥭 Fruityvice Fruit Advice!')
def get_fv_api_date (this_fruit_choice):
   fvr=requests.get('https://fruityvice.com/api/fruit/' + this_fruit_choice)
   fvrn=pd.json_normalize(fvr.json())    
   return fvrn

try:
    fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
    st.write('The user entered ', fruit_choice)
    if not fruit_choice:
        st.error('Select a fruit to get inf')
    else:
        r=get_fv_api_date(fruit_choice)
        st.dataframe(r)
except URLError as e:
    st.error()

st.header('🍌🥭Fruit load list contains')
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

if st.button('Get fruit load list'):
    my_cnx = snowflake.connect(**st.secrets['snowflake'])
    st.dataframe(get_fruit_load_list())
    my_cnx.close()

st.header('🍌🥭Add Fruit header')
def add_fruit_function(add_fruit_local_var):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into PUBLIC.FRUIT_LOAD_LIST values ('" + add_fruit_local_var + "')")
        return 'Thank you for adding ' + add_fruit_local_var

add_fruit_var = st.text_input('add fruit text')

if st.button('add fruit button'):
    my_cnx = snowflake.connect(**st.secrets['snowflake'])
    st.text(add_fruit_function(add_fruit_var))
    my_cnx.close()