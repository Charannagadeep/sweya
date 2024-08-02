import streamlit as st
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

st.set_page_config(page_title="Precision App", page_icon=":bar_chart:")
st.sidebar.image("Unknown.png", width=500)

st.title('Precision Calculation and Visualization for Random Data')

data_size = st.slider('Select the size of the dataset', 100, 1000, 200)

X = np.random.rand(data_size, 5)
y = np.random.randint(0, 2, size=data_size)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

precision = precision_score(y_test, y_pred)

st.subheader(f'Precision: {precision:.2f}')

st.subheader('Data Visualization')

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

plt.figure(figsize=(8, 5))
plt.scatter(X_pca[:, 0], X_pca[:, 1], cmap='coolwarm', alpha=0.7)
plt.title('Random Data (Reduced to 2D using PCA)')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
st.pyplot(plt)

st.subheader('Confusion Matrix')
conf_matrix = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 4))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
st.pyplot(plt)

if st.checkbox('Show dataset'):
    st.write(pd.DataFrame(X, columns=[f'Feature {i+1}' for i in range(X.shape[1])]))

st.subheader('Feature Importance')
importance = model.coef_[0]

plt.figure(figsize=(8, 4))
sns.barplot(x=[f'Feature {i+1}' for i in range(len(importance))], y=importance, palette='viridis')
plt.title('Feature Importance')
plt.xlabel('Feature')
plt.ylabel('Importance')
st.pyplot(plt)
