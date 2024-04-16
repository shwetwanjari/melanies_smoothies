# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write(
    """Choose your Fruit You want in your Custom Smoothie!""")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The Name on your Smoothie will be:', name_on_order)

conn = st.connection("snowflake")
session = conn.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('SEARCH_ON')
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()
                                                                      
ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)
if ingredients_list:
    ingredients_string=''

    for fruit_chosen in ingredients_list:
     ingredients_string+=fruit_chosen + ' '
     st.subheader(fruit_chosen+'Nutrition Information')
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon"+fruit_chosen)
     fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width= True)

    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    #st.write(my_insert_stmt)
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")





