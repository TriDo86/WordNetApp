import streamlit as st

# Create columns
col1, col2 = st.columns([1, 3])

# Place the toggle in the first column
with col1:
    toggle = st.toggle('Toggle')

# Place the radio button in the second column
with col2:
    option = st.radio(
        "Choose an option",
        ('Option 1', 'Option 2', 'Option 3'),
        horizontal=True,
        label_visibility='collapsed'
    )

# Display selected values
st.write("Toggle is:", toggle)
st.write("Selected option:", option)
