import streamlit as st
import json


def calculate_ghROT(ghN, ghRFD):
    return (ghN + ghRFD) / 2

def calculate_hROT(hN, hRFD):
    return (hN + hRFD) / 2

def calculate_tROT(ghROT, hROT):
    return (ghROT + hROT) / 2

def calculate_ntROT(tROT):
    return (tROT - 1) / (80000 - 1)

def calculate_vPOW(CMJ, mRSIp, mRSId):
    return (CMJ + mRSIp + mRSId) / 3

def calculate_nvPOW(vPOW):
    return (vPOW - 1) / (13 - 1)

def calculate_mPR(nvPOW, ntROT):
    return (nvPOW * 0.4) + (ntROT * 0.6)

def calculate_PRO(TSER, TSIR, mPR, vPOW, tROT, MTP, Age):
    return (((TSER + TSIR + mPR + vPOW + tROT + MTP) / 6) / 100) / Age

def calculate_nPRO(PRO):
    return (PRO - 0.01) / (250 - 1)

def calculate_nMEC(MEC):
    return (MEC - 0.077) / (1 - 0.077)

def calculate_mGRADE(MEC, TSER, TSIR, CMJ, mRSIp, mRSId, ghN, ghRFD, hN, hRFD, MTP, Age, precision=4):
    ghROT = calculate_ghROT(ghN, ghRFD)
    hROT = calculate_hROT(hN, hRFD)
    tROT = calculate_tROT(ghROT, hROT)
    ntROT = calculate_ntROT(tROT)
    vPOW = calculate_vPOW(CMJ, mRSIp, mRSId)
    nvPOW = calculate_nvPOW(vPOW)
    mPR = calculate_mPR(nvPOW, ntROT)
    PRO = calculate_PRO(TSER, TSIR, mPR, vPOW, tROT, MTP, Age)
    nPRO = calculate_nPRO(PRO)
    nMEC = calculate_nMEC(MEC)
    mGRADE = (nMEC * 0.6) + (nPRO * 0.4)
    return round(mGRADE, precision)

def save_profile(data, filename):
    if not filename.endswith(".json"):
        filename += ".json"
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
        st.success(f"Profile successfully saved to {filename}")
    except Exception as e:
        st.error(f"Error saving profile: {e}")

def load_profile(filename):
    if not filename.endswith(".json"):
        filename += ".json"
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"File '{filename}' not found. Please enter a valid file name.")
    except json.JSONDecodeError:
        st.error("Error loading profile. The file is corrupted or not in JSON format.")
    except Exception as e:
        st.error(f"An unexpected error occurred while loading the profile: {e}")

# Streamlit App Interface
st.set_page_config(page_title="mGRADE Calculator", layout="wide")
st.title("📊 mGRADE Calculator")
st.markdown("Enter the required values below to calculate mGRADE.")

col1, col2, col3 = st.columns(3)

with col1:
    MEC = st.number_input("Enter MEC:", min_value=0.0, help="Mechanical Score (0 to 1)")
    TSER = st.number_input("Enter TSER:", min_value=0.0, help="TrueStrength ER")
    TSIR = st.number_input("Enter TSIR:", min_value=0.0, help="TrueStrength IR")
    CMJ = st.number_input("Enter CMJ:", min_value=0.0, help="Counter Movement Jump")

with col2:
    mRSIp = st.number_input("Enter mRSIp:", min_value=0.0, help="Modified Reactive Strength Index - Positive")
    mRSId = st.number_input("Enter mRSId:", min_value=0.0, help="Modified Reactive Strength Index - Drop")
    ghN = st.number_input("Enter ghN:", min_value=0.0, help="Glenohumeral Neutral")
    ghRFD = st.number_input("Enter ghRFD:", min_value=0.0, help="Glenohumeral Rate of Force Development")

with col3:
    hN = st.number_input("Enter hN:", min_value=0.0, help="Hip Neutral")
    hRFD = st.number_input("Enter hRFD:", min_value=0.0, help="Hip Rate of Force Development")
    MTP = st.number_input("Enter MTP:", min_value=0.0, help="Maximal Torque Production")
    Age = st.number_input("Enter Age:", min_value=1, format="%d", help="Age of the individual")

filename = st.text_input("Enter file name for saving/loading:")

if st.button("💾 Save Profile"):
    data = {"MEC": MEC, "TSER": TSER, "TSIR": TSIR, "CMJ": CMJ, "mRSIp": mRSIp, "mRSId": mRSId, "ghN": ghN, "ghRFD": ghRFD, "hN": hN, "hRFD": hRFD, "MTP": MTP, "Age": Age}
    save_profile(data, filename)

if st.button("📂 Load Profile"):
    data = load_profile(filename)
    if data:
        MEC, TSER, TSIR, CMJ, mRSIp, mRSId = data['MEC'], data['TSER'], data['TSIR'], data['CMJ'], data['mRSIp'], data['mRSId']
        ghN, ghRFD, hN, hRFD, MTP, Age = data['ghN'], data['ghRFD'], data['hN'], data['hRFD'], data['MTP'], data['Age']

if st.button("💡 Calculate mGRADE"):
    try:
        result = calculate_mGRADE(MEC, TSER, TSIR, CMJ, mRSIp, mRSId, ghN, ghRFD, hN, hRFD, MTP, Age)
        st.success(f"### ✅ Calculated mGRADE: {result:.4f}")
    except Exception as e:
        st.error(f"❌ Calculation failed. Error: {str(e)}")

