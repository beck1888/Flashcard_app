## Imports
import os # Auto-launch the app
import streamlit as st # Web UI


## Recursion prevention: Check that the script is being run directly instead of by another instance (i.e Streamlit)
if __name__ == '__main__' and os.getenv("RUNNING_STREAMLIT_APP") != "TRUE": # Check env var
    # Tell the env variable that the script is running
    os.environ["RUNNING_STREAMLIT_APP"] = "TRUE"
    # If first spawn, then run the website launch code
    os.system("streamlit run /Users/beckorion/Documents/Python/Flashcards/gui.py")

## Main Code
st.header("Beck's Flashcard App")
st.subheader("Version 1.0")