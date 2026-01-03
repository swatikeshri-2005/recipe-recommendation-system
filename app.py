import streamlit as st # type: ignore
from openai import OpenAI # type: ignore

st.set_page_config(page_title="GeekCook", page_icon="🍳")

st.title("🍽️ GeekCook || Recipe Recommendation System")

# Sidebar for API Key
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

def generate_recipe(ingredients):
    client = OpenAI(api_key=api_key)
    prompt = f"""
    Given the following ingredients:
    {ingredients}

    Suggest an easy-to-cook recipe with:
    - Recipe name
    - Ingredients list
    - Step-by-step instructions
    """

    response = client.chat.completions.create(  # noqa: F841
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content  # type: ignore # noqa: F706, F821

with st.form("recipe_form"):
    user_input = st.text_area(
        "Enter ingredients (comma-separated):",
        placeholder="eg: potato, onion, tomato, cheese"
    )
    submit = st.form_submit_button("Get Recipe 🍲")

if submit:
    if not api_key.startswith("sk-"):
        st.error("❌ Please enter a valid OpenAI API key.")
    elif user_input.strip() == "":
        st.warning("⚠️ Please enter at least one ingredient.")
    else:
        with st.spinner("Cooking up something delicious..."):
            recipe = generate_recipe(user_input)
            st.success("✅ Recipe Generated!")
            st.markdown(recipe)


