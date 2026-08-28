import streamlit as st
from snowflake.snowpark.functions import col
import requests  

conn = st.connection("snowflake")
session = conn.session()

st.title(':cup_with_straw: Customize Your Smoothie :cup_with_straw:')
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)
name_on_order = st.text_input("Name on Smoothie")
st.write(
    "The name on your smoothie will be",
    name_on_order
)
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'),col('SEARCH_ON'))
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe]
# st.dataframe(data=my_dataframe,use_container_width=True)
# st.stop()
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)
if ingredients_list:
    ingredients_string = ""
    for fruits_chosen in ingredients_list:
        ingredients_string += fruits_chosen + " "
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruits_chosen, 'SEARCH_ON'].iloc[0]
        st.subheader(fruits_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(
            """
            INSERT INTO smoothies.public.orders
            (INGREDIENTS, NAME_ON_ORDER)
            VALUES (?, ?)
            """,
            params=[ingredients_string.strip(), name_on_order]
        ).collect()

        st.success(
            f"Your Smoothie is ordered, {name_on_order}!",
            icon="✅"
        )
# st.text(smoothiefroot_response.json())
