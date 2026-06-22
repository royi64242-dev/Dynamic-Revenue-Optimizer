import streamlit as st
import pandas as pd
import xgboost as xgb
from datetime import datetime

# מחירון
PRICE_LIST = {
    'sofa_2': 350, 'sofa_3': 450, 'sofa_l': 700,
    'mattress_single': 200, 'mattress_double': 350, 'carpet': 200
}


def calculate_order_total(order_dict):
    return sum(PRICE_LIST[item] * qty for item, qty in order_dict.items())


# הגדרות עמוד
st.set_page_config(page_title="Dynamic Pricing Optimizer", page_icon="🛋️")
st.title("🛋️ Dynamic Revenue Optimizer")


# טעינת מודל
@st.cache_resource
def load_model():
    model = xgb.XGBClassifier()
    model.load_model("pricing_model.json")
    return model


model = load_model()

# ממשק משתמש
st.subheader("1. Enter Service Details")
area = st.selectbox("Service Area", ['Center', 'North', 'South'])
demand = st.slider("Expected Demand (number of calls)", 5, 30, 15)

st.subheader("2. Select Services")
# חלוקה ל-2 עמודות כדי לחסוך מקום
cols = st.columns(2)
selected_services = {}

# מעבר על המחירון ושיוך לטורים לסירוגין
for i, (item, price) in enumerate(PRICE_LIST.items()):
    with cols[i % 2]: # פעם טור 0, פעם טור 1
        qty = st.number_input(f"{item.replace('_', ' ').title()}", min_value=0, step=1)
        if qty > 0:
            selected_services[item] = qty

# כפתור חיזוי
if st.button("🚀 Calculate Pricing"):
    if not selected_services:
        st.error("Please select at least one service!")
    else:
        # חישוב בסיס
        base_price = calculate_order_total(selected_services)

        # בניית ה-DataFrame לחיזוי
        input_data = pd.DataFrame({
            'demand': [demand],
            'base_price': [base_price],
            'month': [datetime.now().month],
            'is_weekend': [datetime.now().weekday() >= 5],
            'is_holiday': [0],
            'area': [area],
            'service_type': [list(selected_services.keys())[0]]  # שירות ראשון ברשימה
        })

        # התאמת עמודות (החלק הקריטי)
        input_encoded = pd.get_dummies(input_data)
        input_encoded = input_encoded.reindex(columns=model.feature_names_in_, fill_value=0)

        # חיזוי הסתברות
        prob = model.predict_proba(input_encoded)[0][1]

        # לוגיקה עסקית למחיר דינמי
        if demand > 20:
            dyn_price = base_price * 1.8
        elif demand < 8:
            dyn_price = base_price * 0.7
        else:
            dyn_price = base_price

        # תוצאות
        st.divider()
        st.subheader("📊 Prediction Results:")

        st.write(f"**Total Base Price:** ₪{base_price}")
        col1, col2 = st.columns(2)
        col1.metric("Closing Probability", f"{prob * 100:.1f}%")
        col2.metric("Recommended Price", f"₪{dyn_price:.0f}", f"{dyn_price - base_price:+.0f}")