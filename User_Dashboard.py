import streamlit as st
import src.database as db
import src.llm as llm
import time

# Page Config
st.set_page_config(
    page_title="Feedback System",
    page_icon="⭐",
    layout="centered"
)

# Initialize DB
db.init_db()

# Main Interface
st.title("We value your feedback! ⭐")
st.markdown("Please rate your experience and leave a short review.")

with st.form("feedback_form"):
    rating = st.slider("How would you rate your experience?", 1, 5, 5)
    review = st.text_area("Tell us more about it...", height=150, placeholder="Type your review here...")
    submit_button = st.form_submit_button("Submit Feedback")

if submit_button:
    if not review.strip():
        st.error("Please enter a review before submitting.")
    else:
        with st.status("Processing your feedback...", expanded=True) as status:
            # 1. Generate User Response
            st.write("Generating AI response...")
            user_response = llm.generate_user_response(rating, review)
            
            # 2. Analyze for Admin (Async-ish simulation)
            st.write("Analyzing sentiment for internal review...")
            summary, recommendations = llm.analyze_submission(rating, review)
            
            # 3. Save to DB
            st.write("Saving to database...")
            db.save_submission(rating, review, user_response, summary, recommendations)
            
            status.update(label="Feedback received!", state="complete", expanded=False)

        # Display result
        st.divider()
        st.success("Thank you! Your feedback has been recorded.")
        st.subheader("Our Response:")
        st.info(user_response)
