import mlflow
import psycopg2
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

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

df = df.drop("Time", axis=1)

# Separate the features from the target
X = df.iloc[:, :-1]  # all features
y = df['Class']  # target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# replace with your run_id
run_id = "5d93a67d2daa40c6925c3d4eb2b667ea"

model_uri = f"runs:/{run_id}/model"
model = mlflow.pyfunc.load_model(model_uri)

predictions = model.predict(X_test)
print(classification_report(y_test, predictions))
