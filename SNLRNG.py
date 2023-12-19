import streamlit as st
import pandas as pd
import random

import os 

if os.path.exists('./data.csv'): 
    df = pd.read_csv('data.csv', index_col=None)

# Create a Streamlit app
st.title("Snake and Ladder RNG")

# Initialize session state variables
if 'question_generated' not in st.session_state:
    st.session_state.question_generated = False

if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

if 'show_answer_and_explanation' not in st.session_state:
    st.session_state.show_answer_and_explanation = False

if 'current_question' not in st.session_state:
    st.session_state.current_question = ""

# Prompt user for difficulty level
difficulty = st.selectbox("Select  Level", df['Level'].unique())

# Filter data based on difficulty level
filtered_df = df[df['Level'] == difficulty]

# Prompt user for category
category = st.selectbox("Select Topic", filtered_df['Topic'].unique())

# Button to generate question
if st.button("Generate Question"):
    # Filter data based on category
    filtered_df = filtered_df[filtered_df['Topic'] == category]

    # Generate a random question index
    st.session_state.question_index = random.randint(0, filtered_df.shape[0] - 1)

    # Update session state variables
    st.session_state.question_generated = True
    st.session_state.show_answer_and_explanation = False

    # Format and display the random question
    question_number = filtered_df.iloc[st.session_state.question_index]['No.']
    question_text = filtered_df.iloc[st.session_state.question_index]['True or False - Question']
    st.session_state.current_question = f"{question_number} - {question_text}"
    st.write("Question:")
    st.write(st.session_state.current_question)

# Button to show answer and explanation
show_answer_button = st.button("Show Answer and Explanation")

# Display answer and explanation if the button is clicked
if show_answer_button and st.session_state.question_generated:
    # Update session state variable
    st.session_state.show_answer_and_explanation = True

    # Display the answer
    st.write("Answer:")
    st.write(filtered_df.iloc[st.session_state.question_index]['T/F'])

    # Display the explanation
    st.write("Explanation:")
    st.write(filtered_df.iloc[st.session_state.question_index]['Answer'])

# Button to reset
if st.button("Reset"):
    # Reset session state variables
    st.session_state.question_generated = False
    st.session_state.question_index = 0
    st.session_state.show_answer_and_explanation = False
    st.session_state.current_question = ""
