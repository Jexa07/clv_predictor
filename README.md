# 💸 Customer Lifetime Value (CLV) Predictor

Ever wondered **how much a customer is really worth** over the long run?  

This project predicts a customer's **future monetary value** to a business using RFM modeling (Recency, Frequency, Monetary). Visualized beautifully through a Streamlit app.

---

## 📊 What It Does

This tool takes in:
- 🧾 **Purchase frequency**
- 📅 **Recency (days since last order)**
- 🌍 **Customer country**

And returns:
- 🔮 **Predicted CLV in GBP and INR**
- 👑 **Top customers by future value**
- 📤 Optional bulk upload to score customers from a CSV

---

## ⚙️ How It Works

We use:
- 📦 **RFM features** from real-world retail data
- 🎯 A trained **Random Forest Regressor**
- 🗺️ Dynamic **country encoding**
- 💅 A clean and interactive **Streamlit interface**

The model is trained on the [Online Retail II dataset](https://www.kaggle.com/datasets/lakshmi25npathi/online-retail-dataset), which contains historical purchase behavior across thousands of customers.

---

## 🖼️ App Demo

![App Screenshot](https://github.com/Jexa07/clv_predictor/blob/main/demo.png.jpg)

---

## 🛠️ Tech Stack

- Python (Pandas, Scikit-learn)
- Streamlit (interactive web UI)
- Pickle (model persistence)
- Excel + CSV handling

---

## 🚀 Quickstart

### 🔧 Setup
```bash
git clone https://github.com/Jexa07/clv_predictor.git
cd clv_predictor
pip install -r requirements.txt
````

### 🧠 Train Model

```bash
python train_model.py
```

### 🧪 Run App

```bash
streamlit run app.py
```

---

## 📥 Example CSV for Bulk Prediction

```csv
Recency,Frequency,Country
30,15,United Kingdom
120,8,France
60,22,Germany
```

---

## 📁 Project Structure

```
clv_predictor/
├── data/
│   └── online_retail_II.xlsx
├── models/
│   ├── rfm_model.pkl
│   └── country_map.pkl
├── app.py
├── train_model.py
├── requirements.txt
└── README.md
```

---

## ❤️ Author

Built with love by [Arpita Pani (@Jexa07)](https://github.com/Jexa07)
