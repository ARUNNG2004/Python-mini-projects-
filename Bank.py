import streamlit as st
import hashlib
import json

# Initialize session state for users if not exists
if 'users' not in st.session_state:
    st.session_state.users = {}

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def register_user(username, password):
    if username in st.session_state.users:
        return False, "Username already exists!"

    hashed_pwd = hash_password(password)
    st.session_state.users[username] = {
        'password': hashed_pwd,
        'balance': 0.0,
        'transactions': []
    }
    return True, "Registration successful!"

def authenticate(username, password):
    if username not in st.session_state.users:
        return False, "User does not exist!"

    user = st.session_state.users[username]
    if user['password'] == hash_password(password):
        return True, "Login successful!"
    return False, "Incorrect password!"

# Streamlit app layout
st.title("Secure Banking App")

# Tab selection
tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.header("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if login_username and login_password:
            success, message = authenticate(login_username, login_password)
            if success:
                st.session_state.username = login_username
                st.success(message)
            else:
                st.error(message)
        else:
            st.error("Please enter both username and password.")

with tab2:
    st.header("Register")
    reg_username = st.text_input("Username", key="reg_username")
    reg_password = st.text_input("Password", type="password", key="reg_password")
    reg_password2 = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if reg_username and reg_password and reg_password2:
            if reg_password == reg_password2:
                success, message = register_user(reg_username, reg_password)
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.error("Passwords do not match!")
        else:
            st.error("Please fill all fields!")

# Check if user is authenticated
if 'username' in st.session_state:
    current_user = st.session_state.users[st.session_state.username]

    if st.button("Logout"):
        del st.session_state.username
        st.success("Logged out successfully!")
        st.rerun()

    # Display balance
    st.header("View Balance")
    st.write(f"Your current balance is: ${current_user['balance']:.2f}")

    # Deposit section
    st.header("Deposit")
    deposit_amount = st.number_input("Enter amount to deposit", min_value=0.0, step=0.01)
    if st.button("Deposit"):
        current_user['balance'] += deposit_amount
        current_user['transactions'].append(f"Deposited ${deposit_amount:.2f}")
        st.success(f"${deposit_amount:.2f} deposited successfully!")

    # Withdraw section
    st.header("Withdraw")
    withdraw_amount = st.number_input("Enter amount to withdraw", min_value=0.0, step=0.01)
    if st.button("Withdraw"):
        if withdraw_amount <= current_user['balance']:
            current_user['balance'] -= withdraw_amount
            current_user['transactions'].append(f"Withdrawn ${withdraw_amount:.2f}")
            st.success(f"${withdraw_amount:.2f} withdrawn successfully!")
        else:
            st.error("Insufficient funds!")

    # Transaction History section
    st.header("Transaction History")
    if current_user['transactions']:
        for idx, transaction in enumerate(reversed(current_user['transactions']), 1):
            st.text(f"{idx}. {transaction}")
    else:
        st.info("No transactions yet")
