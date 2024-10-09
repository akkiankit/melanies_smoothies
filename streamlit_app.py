# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

# Write directly to the app
st.title(":cup_with_straw: Custom Smoothie Order Form :cup_with_straw:")
st.write(
    """
    Choose the Fruits you want in your Smoothie
    """
)

name_on_order = st.text_input("Name on Smoothie")
# st.write("The Current Order is :", name_on_order)

# session = get_active_session()
cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredient_list = st.multiselect(
    'Choose up to 5 Ingrediants',
    my_dataframe, max_selections = 5
)

if ingredient_list:
    # st.text(ingredient_list)

    ingredients_string = ""
    for fruit_choosen in ingredient_list:
        ingredients_string += fruit_choosen + " "
        st.subheader(fruit_choosen + "Nutrition Information")
        fruityvice_response = requests.get("https://www.themealdb.com/api/json/v1/1/search.php?s=" + fruit_choosen)
        fv_df = st.dataframe(fruityvice_response.json(), use_container_width=True)
        

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Button")

    if time_to_insert:
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")

            


 
