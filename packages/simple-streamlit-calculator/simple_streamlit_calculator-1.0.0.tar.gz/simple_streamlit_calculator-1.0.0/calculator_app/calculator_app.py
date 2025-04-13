# calculator_app.py

import streamlit as st

st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")

st.title("🧮 Simple Calculator")

if "expression" not in st.session_state:
    st.session_state.expression = ""

def append_to_expression(value):
    st.session_state.expression += str(value)

def calculate_result():
    try:
        # Replace symbols for eval compatibility
        expression = st.session_state.expression.replace("×", "*").replace("÷", "/")
        result = eval(expression)
        st.session_state.expression = str(result)
    except Exception:
        st.session_state.expression = "Error"

def clear_expression():
    st.session_state.expression = ""

st.text_input("Result", value=st.session_state.expression, key="display", disabled=True)

# Layout buttons
cols = st.columns(4)
buttons = ["7", "8", "9", "÷",
           "4", "5", "6", "×",
           "1", "2", "3", "-",
           "0", "C", "=", "+"]

for i, button in enumerate(buttons):
    if cols[i % 4].button(button):
        if button == "=":
            calculate_result()
        elif button == "C":
            clear_expression()
        else:
            append_to_expression(button)

# Add at the bottom of calculator_app.py
def main():
    import os
    os.system("streamlit run " + __file__)
