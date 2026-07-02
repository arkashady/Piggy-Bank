import streamlit as st

# Set page configuration
st.set_page_config(page_title="Piggy Bank", page_icon="🐷", layout="centered")

st.title("🐷 Interactive Piggy Bank")

# --- SIDEBAR: Goal Setting ---
st.sidebar.header("🎯 Target Settings")
goal = st.sidebar.number_input("Set your target goal amount (₹):", min_value=1, value=100, step=10)

# Initialize the current balance in session state
if "balance" not in st.session_state:
    st.session_state.balance = 0

# Reset button in the sidebar
if st.sidebar.button("Reset Tracker"):
    st.session_state.balance = 0
    st.rerun()

# --- MAIN PAGE: Deposits & Progress ---

# Display the target goal
st.write(f"### Target Goal: **₹{goal}**")

# Calculate remaining and progress percentage
remaining = goal - st.session_state.balance
progress_percentage = min(st.session_state.balance / goal, 1.0)

# Display Progress Bar
st.progress(progress_percentage)
st.write(f"Progress: **{int(progress_percentage * 100)}%** completed")

st.markdown("---")

# Deposit Section (Using a Form so it only updates when the button is clicked)
if remaining > 0:
    st.subheader("📥 Make a Deposit")

    with st.form(key="deposit_form", clear_on_submit=True):
        # Using a slider for quick money selection, capped at the remaining amount needed
        deposit_amount = st.slider(
            "Select amount to deposit:",
            min_value=1,
            max_value=int(remaining),
            value=min(10, int(remaining))
        )

        submit_button = st.form_submit_button(label="Deposit Money")

        if submit_button:
            st.session_state.balance += deposit_amount
            st.rerun()  # Refresh immediately to update the progress bar

# --- STATUS MESSAGES ---
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Total Balance", value=f"₹{st.session_state.balance}")

with col2:
    if remaining > 0:
        st.metric(label="Still Needed", value=f"₹{remaining}", delta=f"-₹{remaining}", delta_color="inverse")
    else:
        st.metric(label="Still Needed", value="₹0")

# Check if goal is reached
if st.session_state.balance >= goal:
    st.balloons()
    st.success(f"🎉 **Congratulations!** You hit your goal of **₹{goal}**!")
    st.confetti = True  # Fun visual cue