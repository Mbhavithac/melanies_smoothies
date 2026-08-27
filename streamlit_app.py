import streamlit as st
from snowflake.snowpark.functions import col

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
fruit_df = (
    session.table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
    .collect()
)
fruit_list = [row["FRUIT_NAME"] for row in fruit_df]
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)
if ingredients_list:
    ingredients_string = ""
    for fruits_chosen in ingredients_list:
        ingredients_string += fruits_chosen + " "
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
