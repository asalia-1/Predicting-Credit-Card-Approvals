import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV

# Load dataset
cc_apps = pd.read_csv('datasets/cc_approvals.data', header = None)

# Inspect data
print(cc_apps.head())
cc_apps_description = cc_apps.describe()
print(cc_apps_description)
print("\n")
# Print DataFrame information
cc_apps_info = cc_apps.info()
print(cc_apps_info)
print("\n")

# Inspect missing values in the dataset
print(cc_apps.tail())

#HANDLING MISSING DATA
# Check to identify missing values in the dataset
print(cc_apps.tail(17))

# Replace the '?'s with NaN and inspect the missing values again
cc_apps = cc_apps.replace('?', np.nan)
print(cc_apps.tail(17))

# Impute the missing values with mean and count number of NaNs in dataset to verify
cc_apps.fillna(cc_apps.mean(), inplace=True)
print(cc_apps.isnull().sum())

for col in cc_apps:
    if cc_apps[col].dtypes == 'object':
        # Impute with the most frequent value
        cc_apps = cc_apps.fillna(cc_apps[col].value_counts().index[0])

# Count the number of NaNs in the dataset and print the counts to verify
print(cc_apps.isnull().sum())


#PREPROCESSING
le = LabelEncoder()

# Iterate over all the values of each column and extract their dtypes
for col in cc_apps:
    if cc_apps[col].dtypes =='object':
    # Use LabelEncoder to do the numeric transformation
        cc_apps[col]=le.fit_transform(cc_apps[col])

#SPLITTING THE DATASET
# Drop the features 11 and 13 and convert the DataFrame to a NumPy array
cc_apps = cc_apps.drop([11, 13], axis=1)
cc_apps = cc_apps.values

# Segregate features and labels into separate variables
X,y = cc_apps[:,0:13] , cc_apps[:,13]
# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X,
                                y,
                                test_size=0.33,
                                random_state=42)


# NORMALIZATION OF DATA VALUES
# Instantiate MinMaxScaler and use it to rescale X_train and X_test
scaler = MinMaxScaler(feature_range=(0,1))
rescaledX_train = scaler.fit_transform(X_train)
rescaledX_test = scaler.fit_transform(X_test)

#FIT THE DATA
logreg = LogisticRegression()
logreg.fit(rescaledX_train, y_train)


#EVALUATE PERFORMANCE
y_pred = logreg.predict(rescaledX_test)
# Get the accuracy score of logreg model and print it
print("Accuracy of logistic regression classifier: ", logreg.score(rescaledX_test, y_test))
confusion_matrix(y_test, y_pred)

#TUNE PARAMETERS
# Parameter ranges
tol = [0.01, 0.001, 0.0001]
max_iter = [100, 150, 200]

# Create a parameter grid
param_grid = {'tol':tol, 'max_iter':max_iter}

grid_model = GridSearchCV(estimator=logreg, param_grid=param_grid, cv=5)
rescaledX = scaler.fit_transform(X)
grid_model_result = grid_model.fit(rescaledX, y)

# Summarize results
best_score, best_params = grid_model_result.best_score_, grid_model_result.best_params_
print("Best: %f using %s" % (best_score, best_params))