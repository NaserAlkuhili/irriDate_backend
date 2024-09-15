from sklearn.linear_model import LogisticRegression
import numpy as np

# Example training data (X and y)
X = np.array([[0.2], [0.8], [0.5], [0.3], [0.7], [0.1]])
y = np.array([0, 1, 0, 0, 1, 0])

# Create and train the model
model = LogisticRegression()
model.fit(X, y)

# Function to predict 0 or 1
def predict(input_value):
    prediction = model.predict(np.array([[input_value]]))
    
    # Ensure the prediction is returned as a native Python int type
    return int(prediction[0])
