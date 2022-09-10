import streamlit as st
import pandas as pd
import requests
import snowflake.connector as snow    
from urllib.error import URLError

# static body
st.header('Breakfast Favourites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado toast')
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# pull api dat
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)

def get_fv_api_date (this_fruit_choice):
   fvr=requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
   fvrn=pd.json_normalize(fvr.json())    
   return fvrn

# Let's Call the Fruityvice API from Our Streamlit App!
st.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
    st.write('The user entered ', fruit_choice)
    if not fruit_choice:
        st.error("Select a fruit to get inf")
    else:
        r=get_fv_api_date(fruit_choice)
        st.dataframe(r)
except URLError as e:
    st.error()

# button controlled block
st.header("Fruit load list contains")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

# add button to load fruit
if st.button('Get fruit load list'):
    my_cnx = snow.connect(**st.secrets["snowflake"])
    st.dataframe(get_fruit_load_list())


# add fruit
st.header("Add Fruit")
def add_fruit(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into PUBLIC.FRUIT_LOAD_LIST values ('" + new_fruit + "')")
        return 'Thank you for adding ' + new_fruit

add_fruit = st.text_input('add fruit')
# add button to add fruit
if st.button('add fruit'):
    my_cnx = snow.connect(**st.secrets["snowflake"])
    st.text(add_fruit(add_fruit))