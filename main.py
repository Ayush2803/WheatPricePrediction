import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
import csv

# Extract dataset for modal prices
dataset = pd.read_csv('modal_price_data.csv')
# Extract dataset for state names
state_df = pd.read_csv('state_names.csv')

# x- days, state id
# y- prices for corresponding x
x = dataset.iloc[:, 1:3].values
y = dataset.iloc[:, 3:].values

# Read the state csv file and map the states with their id's
with open('state_names.csv', newline='') as f:
    reader = csv.reader(f)
    states = list(reader)
state_mapping = []
for state in states:
    state_mapping.append(state[0])

# Determine all the states whose data we have and keep them in set
state_set = set()
for elem in x:
    state_set.add(elem[1])

# FEATURE SCALING - REMOVED FOR NOW DUE TO UNCERTAINITY
# st_x = StandardScaler()
# st_y = StandardScaler()
# x = st_x.fit_transform(x_)
# y = st_y.fit_transform(y_)

# Plot the training data
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(x[:, 0], x[:, 1], y, color='r')
# ax.set_xlabel('Days Scaled')
# ax.set_ylabel('States Scaled')
# ax.set_zlabel('Wheat Price Scaled')
# plt.savefig('train.png')


# Create an SVR regressor object and train it on train dataset
regressor = SVR(kernel='rbf')
regressor.fit(x, y)

# Plot the SVR surface and also the scattered data points
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(x[:, 0], x[:, 1], y, color='r')
ax.set_xlabel('Days Scaled')
ax.set_ylabel('States Scaled')
ax.set_zlabel('Wheat Price Scaled')
ax.plot_trisurf(x[:, 0], x[:, 1], regressor.predict(x), color='blue')
plt.savefig('svr.png')


# Create testing data- day 8 and state id as the state id in the set of states
test_data = []
for state in state_set:
    test_data.append([8, state])

# Obtain predictions for test data
predictions = regressor.predict(test_data)

# Print the predictions
for i in range(len(predictions)):
    print(state_mapping[test_data[i][1]], predictions[i])
