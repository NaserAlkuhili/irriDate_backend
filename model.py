import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

df = pd.read_csv('./data.csv')

# Dropping the date feature
df = df.drop(columns=['date'])

X_train = df.drop('pump', axis=1)
y_train = df['pump']

# Standardizing the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)


best_mlp = MLPClassifier(
    activation='relu',
    alpha=0.0001,
    early_stopping=False,
    hidden_layer_sizes=(50, 50),
    learning_rate='constant',
    max_iter=1000,
    solver='adam',
    random_state=42
)

best_mlp.fit(X_train_scaled, y_train)

# Function to predict 0 or 1 based on input features
def predict(input_value):
    
    input_value_scaled = scaler.transform(np.array([input_value]))
    
    
    prediction = best_mlp.predict(input_value_scaled)
    
    
    return int(prediction[0])

