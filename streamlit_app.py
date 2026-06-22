# Import python packages
import streamlit as st
import os
from snowflake.snowpark.functions import col

import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)

# Write directly to the app
st.title(f"Cup With Straw:Customize your smoothie")
st.write(
  """Choose the fruits to go intoyour smoothie.
  """
)

name_on_order=st.text_input('Name on Smoothie')
st.write('Name on your smoothie will be :',name_on_order)


cnx=st.connection("snowflake");
session=cnx.session();
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
ingredients_list=st.multiselect('Chooseupto 5 ingredients:',my_dataframe,max_selections=5)

if ingredients_list:
    ingredients_string=''

    for fruit_name in ingredients_list:
        ingredients_string+=fruit_name +' '
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" +name_on_order+"""' )"""
               
    

    time_to_insert=st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
