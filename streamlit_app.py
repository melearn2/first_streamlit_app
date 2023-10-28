import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title("My Mom's New Healthy Diner")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Oatmeal with warm milk')
streamlit.text('🍞🐔 Bread & Omlette')
streamlit.text('🥗 Veg Paratha & Tea')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Apple','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#new section to display FruitVicy API response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if no fruit_choice:
    streamlit.error('Please select a fruit to get information.')
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    # get response in variable to write in tabular format
    #streamlit.text(fruityvice_response.json())
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # write response in tabular format
    streamlit.dataframe(fruityvice_normalized)
except:
  URLError as e:
  streamlit.error()
#stop running below steps till we troubleshoot
streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

#2nd option for fruit choice
fruit_choice2 = streamlit.text_input('What fruit would you like information about?','Cherry')
streamlit.write('The user entered ', fruit_choice2)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice2)
# get response in variable to write in tabular format
#streamlit.text(fruityvice_response.json())
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write response in tabular format
streamlit.dataframe(fruityvice_normalized)

streamlit.write('Thanks for adding ', fruit_choice , fruit_choice2)
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
