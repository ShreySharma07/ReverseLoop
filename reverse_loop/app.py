import streamlit as st
import os
from pathlib import Path

# Import our components
from reverse_loop.agents.vision import ADKVisionAgent
from reverse_loop.agents.market import ADKMarketAgent
from reverse_loop.tools.calculator import ProfitCalculator

# Page Config
st.set_page_config(page_title="ReverseLoop Triage", layout="wide")

# --- 1. Header ---
st.title("ReverseLoop: Autonomous Returns Triage")
st.markdown("### Agent Swarm: Vision + Market + Finance")

# --- 2. Initialize Agents (Cached) ---
@st.cache_resource
def load_agents():
    # st.spinner because initialization takes a second
    return ADKVisionAgent(), ADKMarketAgent()

vision_bot, market_bot = load_agents()

# --- 3. UI Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Ingest Item")
    uploaded_file = st.file_uploader("Upload Return Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        # Display the image
        st.image(uploaded_file, caption="Item on Conveyor", use_container_width=True)
        
        # Save temp file for the agent to read
        temp_path = Path("temp_upload.jpg")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

with col2:
    st.subheader("2. Agent Decision")
    
    if uploaded_file and st.button("RUN TRIAGE ANALYSIS", type="primary"):
        status_container = st.container()
        
        with status_container:
            # --- STEP 1: VISION ---
            with st.status("Step 1: Inspecting Visual Condition...", expanded=True) as status:
                st.write("🤖 Vision Agent looking at pixels...")
                vision_data = vision_bot.analyze_image("temp_upload.jpg")
                
                # Check for errors
                if "error" in vision_data:
                    st.error(vision_data["error"])
                    st.stop()
                    
                st.success(f"Identified: {vision_data.get('item_name', 'Unknown')}")
                st.json(vision_data, expanded=False)
                
                # --- STEP 2: MARKET ---
                st.write("Market Agent checking eBay...")
                item_name = vision_data.get("item_name", "Unknown Item")
                market_data = market_bot.analyze_market_value(item_name)
                
                st.success(f"Valuation: ${market_data.get('average_market_price', 0)}")
                st.json(market_data, expanded=False)
                
                status.update(label="Analysis Complete!", state="complete", expanded=False)

        # --- STEP 3: FINANCE (The Verdict) ---
        st.divider()
        
        price = market_data.get("average_market_price", 0)
        # Default weight 1.5lbs for clothing
        financials = ProfitCalculator.calculate_net_profit(price, weight_lbs=1.5)
        
        profit = financials["net_profit"]
        
        if financials["is_profitable"]:
            st.success(f"## ✅ DECISION: RESELL")
            st.metric(label="Projected Profit", value=f"${profit:.2f}", delta="Arbitrage Opportunity")
            st.balloons()
        else:
            st.error(f"## ❌ DECISION: RECYCLE")
            st.metric(label="Net Loss if Resold", value=f"${profit:.2f}", delta="-Loss", delta_color="inverse")
            
        # Show Ledger
        with st.expander("See Financial Ledger"):
            st.table([financials])

        # Cleanup
        if os.path.exists("temp_upload.jpg"):
            os.remove("temp_upload.jpg")