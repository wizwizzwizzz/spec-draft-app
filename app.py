import streamlit as st

def calculate_spec(H7, Q22, Q27, R22, R27, S22, S27, I9, I10, I11, C15, C17):
    Q28 = Q22 * Q27
    R28 = R22 * R27
    S28 = S22 * S27
    Q29 = I10 * 4
    R29 = I9 * 4
    Q30 = Q28 + Q29 + (5 if H7 in ["BC", "C"] else 2)
    R30 = R28 + R29 + (5 if H7 in ["BC", "C"] else 2)

    if I9 == 0 and I10 == 0 and I11 == 0:
        S30 = S28 + 4
    elif I9 > 0 and I10 > 0 and I11 > 0:
        S30 = S28 + (S27 * 3) + (I11 * 4) + 4
    elif I9 > 0 and I10 > 0 and I11 == 0:
        S30 = S28 + (S27 * 3) + 4
    elif I9 == 0 and I10 == 0 and I11 > 0:
        S30 = S28 + 4 + (I11 * 4)
    else:
        S30 = None

    S31 = {"BC": 24, "C": 16, "E": 6}.get(H7, 0)
    S32 = S30 + S31 + (2 if H7 == "E" else 3)

    S33 = {
        "1. single pallet": 1370,
        "2. loose load in container 20-40 ft": 2200,
        "3. loose load in container 40 ft HQ": 2500,
        "4. double stack pallet in container 20-40 ft": 950,
        "5. double stack pallet in container 40 ft HQ": 1100
    }.get(C15, 0)

    S34 = {"Column (SF3.5)": 3.5, "Interlock (SF5)": 5}.get(C17, 0)

    S35 = int(S33 / S32) if S32 else 0
    S36 = round(((S35 - 1) * S27 * S34) / 1000) if S35 else 0
    S37 = round(((((S35 - 1) * S27) + (S35 * S27) + 1000) * S34) / 1000) if S35 else 0

    return {
        "Q30": Q30, "R30": R30, "S30": S30,
        "S35": S35, "S36": S36, "S37": S37,
        "Layout": C17
    }

st.title("Spec Draft Calculation Web App")

material = st.selectbox("Material Type (H7)", ["BC", "C", "E"])
Q22 = st.number_input("Q22", value=1.0)
Q27 = st.number_input("Q27", value=1.0)
R22 = st.number_input("R22", value=1.0)
R27 = st.number_input("R27", value=1.0)
S22 = st.number_input("S22", value=1.0)
S27 = st.number_input("S27", value=1.0)
I9 = st.number_input("I9", value=0)
I10 = st.number_input("I10", value=0)
I11 = st.number_input("I11", value=0)
pallet = st.selectbox("Pallet Type (C15)", [
    "1. single pallet",
    "2. loose load in container 20-40 ft",
    "3. loose load in container 40 ft HQ",
    "4. double stack pallet in container 20-40 ft",
    "5. double stack pallet in container 40 ft HQ"
])
stacking = st.selectbox("Stacking Style (C17)", ["Column (SF3.5)", "Interlock (SF5)"])

if st.button("Calculate"):
    result = calculate_spec(material, Q22, Q27, R22, R27, S22, S27, I9, I10, I11, pallet, stacking)
    st.write("Results:", result)
