# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

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

ingredient_list = st.multiselect(
    'Choose up to 5 Ingrediants',
    my_dataframe, max_selections = 5
)

if ingredient_list:
    # st.text(ingredient_list)

    ingredients_string = ""
    for fruit_choosen in ingredient_list:
        ingredients_string += fruit_choosen + " "

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Button")

    if time_to_insert:
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")

 
