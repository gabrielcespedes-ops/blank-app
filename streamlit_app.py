import streamlit as st
import pickle
import pandas as pd

# Cargar el modelo serializado
with open("modelo_retraso_olist.pkl", "rb") as f:
    model = pickle.load(f)

st.title("Predicción de retraso en entrega – Olist")
st.markdown("Ingrese los datos del pedido para estimar el riesgo de retraso en la entrega.")

# Inputs del usuario
price = st.number_input("Precio del producto", min_value=0.0, value=100.0)
freight = st.number_input("Costo de envío (freight_value)", min_value=0.0, value=20.0)
weight = st.number_input("Peso del producto (g)", min_value=0.0, value=500.0)
delivery_time = st.number_input("Días estimados de entrega", min_value=1, value=5)

# Botón de predicción
if st.button("Calcular riesgo de retraso"):
    data = pd.DataFrame({
        "price": [price],
        "freight_value": [freight],
        "product_weight_g": [weight],
        "delivery_time": [delivery_time]
    })

    pred = model.predict(data)[0]
    prob = model.predict_proba(data)[0][1]

    st.metric("Probabilidad de retraso", f"{prob*100:.1f}%")

    if pred == 1:
        st.warning("Alto riesgo de retraso. Se recomienda priorizar este pedido en la logística.")
    else:
        st.success("Riesgo bajo de retraso. Manejo estándar en la operación.")
