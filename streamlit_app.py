import streamlit
import pandas
import requests
import snowflake.connector    
from urllib.error import URLError

# static body
streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# pull api data direct
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# help function
def get_fv_api_date (this_fruit_choice):
   fvr=requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
   fvrn=pandas.json_normalize(fvr.json())    
   return fvrn

# Let's Call the Fruityvice API from Our Streamlit App!
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    streamlit.write('The user entered ', fruit_choice)
    if not fruit_choice:
        streamlit.error("Select a fruit to get inf")
    else:
        r=get_fv_api_date(fruit_choice)
        streamlit.dataframe(r)
except URLError as e:
    streamlit.error()

# blank out rest
streamlit.stop()   

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
'''
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)
'''
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
my_data_rows.append 
streamlit.header("fruit_load_list ...")
streamlit.dataframe(my_data_rows)

# Add fruit
add_my_fruit=streamlit.text_input('Add a fruit', 'Jackfruit')
my_cur.execute("insert into PUBLIC.FRUIT_LOAD_LIST values ('" + add_my_fruit + "')")
streamlit.write('Thank you for adding ', add_my_fruit)