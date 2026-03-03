import streamlit as st
import numpy as np
import random

# -----------------------------
# Platforms
# -----------------------------
platforms = ["Amazon", "Flipkart", "AJIO", "Myntra", "Shoppers Stop"]

# -----------------------------
# Categories & Subcategories
# -----------------------------
categories = {
    "Fashion": {
        "Shoes": ["Nike", "Adidas"],
        "Clothing": ["Levis", "TommyHilfiger"]
    },
    "Beauty": {
        "Cosmetics": ["Maybelline"],
        "Fragrance": ["Titan"]
    },
    "Accessories": {
        "Watches": ["Casio"],
        "Sunglasses": ["RayBan"]
    },
    "Travel & Lifestyle": {
        "Bags": ["AmericanTourister"],
        "Backpacks": ["Skybags"]
    }
}

# -----------------------------
# Marketplace Dataset
# -----------------------------
marketplace = {
    "Nike": {
        "Amazon": {"price": 5000, "rating": 4.4},
        "Flipkart": {"price": 4800, "rating": 4.2},
        "AJIO": {"price": 4700, "rating": 4.3},
        "Myntra": {"price": 4600, "rating": 4.5},
        "Shoppers Stop": {"price": 4900, "rating": 4.3}
    },
    "Adidas": {
        "Amazon": {"price": 4500, "rating": 4.3},
        "Flipkart": {"price": 4300, "rating": 4.1},
        "AJIO": {"price": 4200, "rating": 4.2},
        "Myntra": {"price": 4100, "rating": 4.4},
        "Shoppers Stop": {"price": 4400, "rating": 4.2}
    },
    "Levis": {
        "Amazon": {"price": 2500, "rating": 4.4},
        "Flipkart": {"price": 2400, "rating": 4.2},
        "AJIO": {"price": 2300, "rating": 4.3},
        "Myntra": {"price": 2200, "rating": 4.5},
        "Shoppers Stop": {"price": 2450, "rating": 4.3}
    },
    "TommyHilfiger": {
        "Amazon": {"price": 3500, "rating": 4.5},
        "Flipkart": {"price": 3400, "rating": 4.3},
        "AJIO": {"price": 3300, "rating": 4.4},
        "Myntra": {"price": 3200, "rating": 4.6},
        "Shoppers Stop": {"price": 3450, "rating": 4.4}
    },
    "Maybelline": {
        "Amazon": {"price": 800, "rating": 4.4},
        "Flipkart": {"price": 750, "rating": 4.2},
        "AJIO": {"price": 720, "rating": 4.3},
        "Myntra": {"price": 700, "rating": 4.5},
        "Shoppers Stop": {"price": 780, "rating": 4.3}
    },
    "Titan": {
        "Amazon": {"price": 5000, "rating": 4.6},
        "Flipkart": {"price": 4800, "rating": 4.4},
        "AJIO": {"price": 4700, "rating": 4.5},
        "Myntra": {"price": 4600, "rating": 4.6},
        "Shoppers Stop": {"price": 4900, "rating": 4.5}
    },
    "Casio": {
        "Amazon": {"price": 3000, "rating": 4.5},
        "Flipkart": {"price": 2900, "rating": 4.3},
        "AJIO": {"price": 2800, "rating": 4.2},
        "Myntra": {"price": 2750, "rating": 4.4},
        "Shoppers Stop": {"price": 2950, "rating": 4.3}
    },
    "RayBan": {
        "Amazon": {"price": 6000, "rating": 4.6},
        "Flipkart": {"price": 5800, "rating": 4.4},
        "AJIO": {"price": 5700, "rating": 4.5},
        "Myntra": {"price": 5600, "rating": 4.6},
        "Shoppers Stop": {"price": 5900, "rating": 4.5}
    },
    "AmericanTourister": {
        "Amazon": {"price": 2500, "rating": 4.4},
        "Flipkart": {"price": 2400, "rating": 4.3},
        "AJIO": {"price": 2300, "rating": 4.2},
        "Myntra": {"price": 2200, "rating": 4.4},
        "Shoppers Stop": {"price": 2450, "rating": 4.3}
    },
    "Skybags": {
        "Amazon": {"price": 1800, "rating": 4.3},
        "Flipkart": {"price": 1700, "rating": 4.2},
        "AJIO": {"price": 1600, "rating": 4.1},
        "Myntra": {"price": 1500, "rating": 4.4},
        "Shoppers Stop": {"price": 1750, "rating": 4.2}
    }
}

# -----------------------------
# Q-Table (Session State)
# -----------------------------
if "q_table" not in st.session_state:
    st.session_state.q_table = {}

learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.3

def initialize_state(brand):
    if brand not in st.session_state.q_table:
        st.session_state.q_table[brand] = {}
        for p in platforms:
            st.session_state.q_table[brand][p] = [0]

def recommend(brand):
    initialize_state(brand)
    latest_q = {p: st.session_state.q_table[brand][p][-1] for p in platforms}
    if random.uniform(0,1) < epsilon:
        return random.choice(platforms)
    return max(latest_q, key=latest_q.get)

def update_q(brand, platform, reward):
    current_q = st.session_state.q_table[brand][platform][-1]
    max_future_q = max([st.session_state.q_table[brand][p][-1] for p in platforms])
    new_q = current_q + learning_rate * (reward + discount_factor * max_future_q - current_q)
    st.session_state.q_table[brand][platform].append(new_q)

# -----------------------------
# UI
# -----------------------------
st.title("🛒 Smart RL E-Commerce Recommender")

category = st.selectbox("Select Category", list(categories.keys()))
subcategory = st.selectbox("Select Subcategory", list(categories[category].keys()))
brand = st.selectbox("Select Brand", categories[category][subcategory])

st.subheader("📊 Price Comparison")

data = marketplace[brand]

for p in platforms:
    st.write(f"**{p}** → ₹{data[p]['price']} | ⭐ {data[p]['rating']}")

cheapest = min(platforms, key=lambda p: data[p]["price"])
st.success(f"💰 Cheapest Platform: {cheapest}")

suggested = recommend(brand)
st.info(f"🤖 RL Suggested Platform: {suggested}")

if st.button("Buy from Cheapest"):
    reward = 10
    update_q(brand, cheapest, reward)
    st.success("Purchase Recorded & Q-Table Updated")

if st.button("View Q-Table"):
    st.write(st.session_state.q_table)
