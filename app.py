import os
import streamlit as st # type: ignore
from openai import OpenAI # type: ignore

st.set_page_config(page_title="GeekCook", page_icon="🍳")
st.title("🍽️ GeekCook || Recipe Recommendation System")

# Read API key from Streamlit Cloud Secrets
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OpenAI API key not found. Please set it in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)


def generate_recipe(ingredients):
    prompt = f"""
    Given the following ingredients:
    {ingredients}

    Suggest an easy-to-cook recipe with:
    - Recipe name
    - Ingredients list
    - Step-by-step instructions
    """

    response = client.responses.create(
        model="gpt-4o-mini",  # If this fails, change to "gpt-4o-mini"
        input=prompt
    )

    return response.output_text


with st.form("recipe_form"):
    user_input = st.text_area(
        "Enter ingredients (comma-separated):",
        placeholder="potato, onion, tomato, cheese"
    )
    submit = st.form_submit_button("Get Recipe 🍲")

if submit:
    if user_input.strip() == "":
        st.warning("⚠️ Please enter at least one ingredient.")
    else:
        with st.spinner("Cooking up something delicious..."):
            recipe = generate_recipe(user_input)
            st.success("✅ Recipe Generated!")
            st.markdown(recipe)
