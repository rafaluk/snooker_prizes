from DataPrepare import DataPrepare
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import explained_variance_score, mean_absolute_error

seasons = ['2017-2018']

# dataPrepare = DataPrepare(seasons)
# dataPrepare.get_csv_file()

df = pd.read_csv("snooker_data.csv", sep=";")
df = df.set_index(df['Name'])
df = df.drop('Name', axis=1)
# print(df.head(20))

df['Centuries'].fillna(0, inplace=True)
df['Titles'].fillna(0, inplace=True)

# ideas
# feature engeenering - jedna kolumna matches won percentage zamiast dwoch
# titles - binarna
# centuries asymetria. moze log?
# standaryzacja


# IMPUTATIONS
# print(df.isna().sum())

# fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
#
# ax1.hist(df['Centuries'], bins=40)
# ax1.set_title("Centuries")
#
# ax2.hist(df['AST'], bins=40)
# ax2.set_title("Average shot time")
#
# ax3.hist(df['Titles'], bins=10)
# ax3.set_title("Titles")

# plt.show()
corr_matrix = np.round_(np.corrcoef(df.T), 2)
# print(corr_matrix)


# , kind='hist', bins=40

import seaborn as sns
# Compute the correlation matrix
corr = df.corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
# f, ax = plt.subplots(figsize=(11, 9))
#
# # Generate a custom diverging colormap
# cmap = sns.diverging_palette(220, 10, as_cmap=True)
#
# # Draw the heatmap with the mask and correct aspect ratio
# sns.heatmap(corr, mask=mask, center=0, cmap=cmap, square=True,
#             linewidths=.5, cbar_kws={"shrink": .7})

# plt.show()

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

X = df.drop('Money_Prizes', axis=1)
y = df['Money_Prizes']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25)

randomForest = RandomForestRegressor()
from pprint import pprint
print('Parameters currently in use:\n')
pprint(randomForest.get_params())

estimators = np.arange(10, 200, 10)

scores = []
for n in estimators:
    randomForest.set_params(n_estimators=n)
    randomForest.fit(X_train, y_train)
    scores.append(randomForest.score(X_test, y_test))

plt.title("Effect of n_estimators")
plt.xlabel("n_estimator")
plt.ylabel("score")
plt.ylim(0, 1)
plt.yticks(np.arange(0,1,0.1))
plt.plot(estimators, scores)
# plt.show()

features = X.columns
# print(features)

feature_importance = pd.Series(randomForest.feature_importances_,
                               index=features).sort_values(ascending=False)

print(feature_importance)

y_pred = randomForest.predict(X_test)
y_pred = np.round_(y_pred, 0)

df2 = pd.DataFrame({'real': y_test, 'predicted': y_pred},
                   columns=['real', 'predicted'])

df2['error'] = np.abs(df2['real'] - df2['predicted'])

print(df2)
print('error sum:')
print(df2['error'].sum())
print('error avf:')
print(np.average(df2['error']))
fig, ax = plt.subplots()

plt.scatter(x=df2.index, y=df2['predicted'])

plt.scatter(x=df2.index, y=df2['real'])
plt.grid(linestyle='-', linewidth=.3)
plt.xticks(np.arange(len(df2['predicted'])), rotation=90)
ax.set_yticklabels(['{:,}'.format(int(x)) for x in ax.get_yticks().tolist()])
plt.show()
print(randomForest.score(X_test, y_test))

print(mean_absolute_error(y_test, y_pred))

