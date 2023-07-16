# import numpy as np
import pandas as pd
import psycopg2
# import matplotlib
# import matplotlib.pyplot as plt
# import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# from sklearn.model_selection import KFold
import mlflow
import mlflow.sklearn

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="credit_card",
    user="postgres",
    password=1978
)

# Create a cursor object
cursor = conn.cursor()

# Execute a query to retrieve the data
query = "SELECT * FROM credit_card"
cursor.execute(query)

# Fetch all the rows returned by the query
rows = cursor.fetchall()

# Get the column names
columns = [desc[0] for desc in cursor.description]

# Create a pandas DataFrame from the rows and columns
df = pd.DataFrame(rows, columns=columns)

# Close the cursor and connection
cursor.close()
conn.close()


d = df.drop("Time", axis=1)

# Separate the features from the target
X = df.iloc[:, :-1]  # all features
y = df['Class']  # target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Set the experiment name to an experiment with a descriptive name
mlflow.set_experiment('fraud_detection_experiment')

# Start a new run in this experiment
with mlflow.start_run():
    # Define the model 
    clf = LogisticRegression(random_state=42)

    # Train the model
    clf.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = clf.predict(X_test)
    
    # Log model
    mlflow.sklearn.log_model(clf, "model")
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy_score(y_test, predictions))
    
    # Print out metrics
    print("Model accuracy: ", accuracy_score(y_test, predictions))
    print("Confusion Matrix: \n", confusion_matrix(y_test, predictions))
    print("Classification Report: \n", classification_report(y_test, predictions))
