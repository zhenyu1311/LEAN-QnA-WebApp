import streamlit as st
import pandas as pd
import random

df = pd.read_csv('data.csv')

# Create a Streamlit app
st.title("🐍 Snake and Ladder RNG 🎲")

# Initialize session state variables
if 'question_generated' not in st.session_state:
    st.session_state.question_generated = False

if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

if 'show_answer_and_explanation' not in st.session_state:
    st.session_state.show_answer_and_explanation = False

if 'current_question' not in st.session_state:
    st.session_state.current_question = ""

if 'selected_level' not in st.session_state:
    st.session_state.selected_level = None

# Form to structure layout
with st.form("main_form"):
    # Prompt user for difficulty level
    selected_level = st.selectbox("Select Level", df['Level'].dropna().unique())

    # Save selected level in session state
    st.session_state.selected_level = selected_level

    # Filter data based on difficulty level
    filtered_df = df[df['Level'] == st.session_state.selected_level]

    # Prompt user for category
    category = st.selectbox("Select Topic", filtered_df['Topic'].unique())

    # Button to generate question
    generate_button = st.form_submit_button("Generate Question")

# Generate a new question when the "Generate Question" button is clicked
if generate_button:
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
    st.write("🤔 Question:")
    st.write(st.session_state.current_question)

# Buttons for user to answer the question
if st.session_state.question_generated:
    # Use columns to place buttons side by side
    col1, col2 = st.columns(2)

    # TRUE button
    with col1:
        true_button = st.button("TRUE ✅", key="true_button", help="Click for TRUE (Green)")
        if true_button:
            # Process user's answer
            user_answer = True
            correct_answer = str(filtered_df.iloc[st.session_state.question_index]['T/F'])

            # Convert both to lowercase for case-insensitive comparison
            user_answer_str = str(user_answer).lower()
            correct_answer_str = correct_answer.lower()

            # Display result
            if user_answer_str == correct_answer_str:
                result_message = "✅ Correct! Well done! 🎉"
            else:
                result_message = f"❌ Wrong. The correct answer is {correct_answer}."

            st.write(f"Your Answer: {user_answer}")
            st.write(result_message)

    # FALSE button
    with col2:
        false_button = st.button("FALSE ❌", key="false_button", help="Click for FALSE (Red)")
        if false_button:
            # Process user's answer
            user_answer = False
            correct_answer = str(filtered_df.iloc[st.session_state.question_index]['T/F'])

            # Convert both to lowercase for case-insensitive comparison
            user_answer_str = str(user_answer).lower()
            correct_answer_str = correct_answer.lower()

            # Display result
            if user_answer_str == correct_answer_str:
                result_message = "✅ Correct! Well done! 🎉"
            else:
                result_message = f"❌ Wrong. The correct answer is {correct_answer}."

            st.write(f"Your Answer: {user_answer}")
            st.write(result_message)

# Button to show answer and explanation
show_answer_button = st.button("Show Answer and Explanation")

# Display answer and explanation if the button is clicked
if show_answer_button and st.session_state.question_generated:
    # Update session state variable
    st.session_state.show_answer_and_explanation = True

    # Display the question
    st.write("🤔 Question:")
    st.write(st.session_state.current_question)

    # Display the answer
    st.markdown("📚 Answer:")
    st.markdown(filtered_df.iloc[st.session_state.question_index]['T/F'])

    # Display the explanation
    st.markdown("🔍 Explanation:")
    st.markdown(filtered_df.iloc[st.session_state.question_index]['Answer'])

# Button to reset
reset_button = st.button("Reset")
if reset_button:
    # Reset session state variables
    st.session_state.question_generated = False
    st.session_state.question_index = 0
    st.session_state.show_answer_and_explanation = False
    st.session_state.current_question = ""
