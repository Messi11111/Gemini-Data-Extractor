import streamlit as st
import pandas as pd

st.set_page_config(page_title="Voter AI Pro", layout="wide")

# High-Contrast Futuristic CSS
st.markdown("""
    <style>
    .stApp { background: #0b0e1a; color: #00f2fe; }
    p, span, label { color: #ffffff !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(0, 242, 254, 0.1);
        border: 1px solid #00f2fe;
        color: #00f2fe !important;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #00f2fe !important; color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ NEURAL VOTER HUB: BOOTH COMMAND")

files = st.file_uploader("UPLOAD EXCEL FILES", type=["xlsx"], accept_multiple_files=True)

if files:
    # Merge and initialize missing columns
    all_data = pd.concat([pd.read_excel(f) for f in files], ignore_index=True)
    if "Caste" not in all_data.columns:
        all_data["Caste"] = ""
    
    # Logic to show data Booth-wise
    if "Polling Booth" in all_data.columns:
        booths = all_data["Polling Booth"].unique()
        st.subheader("🛰️ BOOTH-WISE SEGMENTATION")
        tabs = st.tabs([f"📍 {b}" for b in booths])

        for i, booth in enumerate(booths):
            with tabs[i]:
                booth_df = all_data[all_data["Polling Booth"] == booth]
                st.write(f"Voters in {booth}: {len(booth_df)}")
                edited_df = st.data_editor(booth_df, num_rows="dynamic", key=f"edit_{i}")
                
                st.download_button(f"Export {booth} List", 
                                 data=edited_df.to_csv(index=False).encode('utf-8-sig'),
                                 file_name=f"{booth}_export.csv")
    else:
        st.error("No 'Polling Booth' column found. Please use the updated Data Extractor.")
else:
    st.info("Awaiting Data Feed. Polling Booth tabs will appear automatically.")