# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

name_on_order = st.text_input("Name on smoothies")
st.write("The name on your smoothies will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients?",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen) 
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) 
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    # st.stop()
    
    time_to_insert = st.button('Submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order)
