import streamlit as st
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Generate random data
st.title('Precision Calculation for Random Data')

# User input for the size of the dataset
data_size = st.slider('Select the size of the dataset', 100, 1000, 200)

# Generate random features and target
X = np.random.rand(data_size, 5)  # 5 random features
y = np.random.randint(0, 2, size=data_size)  # binary target (0 or 1)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Fit a simple logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate precision
precision = precision_score(y_test, y_pred)

# Display the precision
st.write(f'Precision: {precision:.2f}')

# Display the dataset if the user wants to see it
if st.checkbox('Show dataset'):
    st.write(pd.DataFrame(X, columns=[f'Feature {i+1}' for i in range(X.shape[1])]))

