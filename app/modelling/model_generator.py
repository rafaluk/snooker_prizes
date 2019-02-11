from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV
from sklearn.metrics import explained_variance_score, mean_absolute_error, median_absolute_error
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time


class ModelGenerator:

    def __init__(self, df):
        # applicable only for snooker data
        self._df = df
        self._y = df['Money_Prizes']
        self._X = df.drop('Money_Prizes', axis=1)
        self._x_train = 0
        self._X_test = 0
        self._y_train = 0
        self._y_test = 0
        self._error = 0
        self._model = RandomForestRegressor()

    def perform_rf_own_params(self, split, n_estimators, max_features, max_depth,
                              min_samples_split, min_samples_leaf, bootstrap):
        split = int(split)/100
        X = self._X
        y = self._y

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split)

        rfr = RandomForestRegressor(n_estimators=n_estimators, max_features=max_features, max_depth=max_depth,
                                    min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
                                    bootstrap=bootstrap)
        rfr.fit(X_train, y_train)
        self._model = rfr
        predictions = rfr.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        # dupa = pd.DataFrame({'y_test': y_test, 'predictions': predictions})
        # print(dupa)
        evs = explained_variance_score(y_test, predictions)
        cv_score = cross_val_score(rfr, X, y, cv=5)

        importances = list(rfr.feature_importances_)
        feature_list = list(X.columns)




        mae_str = str(np.round_(mae, 2))
        evs_str = str(np.round_(evs*100, 2)) + "%"
        avg_cv  = str(np.round_(np.mean(cv_score)*100, 2)) + "%"

        results = {'Mean Absolute Error': mae_str,
                   'Explained Variance Score': evs_str,
                   'Cross Validation Score': avg_cv}

        return results

    def perform_rf_with_random_params(self):
        startes = time.time()
        X = self._X
        y = self._y
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        self._x_train = X_train
        self._X_test = X_test
        self._y_train = y_train
        self._y_test = y_test
        n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num=10)]
        max_features = ['auto', 'sqrt']
        max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
        max_depth.append(None)
        min_samples_split = [2, 5, 10]
        min_samples_leaf = [1, 2, 4]
        bootstrap = [True, False]

        random_grid = {'n_estimators': n_estimators,
                       'max_features': max_features,
                       'max_depth': max_depth,
                       'min_samples_split': min_samples_split,
                       'min_samples_leaf': min_samples_leaf,
                       'bootstrap': bootstrap}

        rfr = RandomForestRegressor()


        # TODO change to: cv=3
        rfr_random = RandomizedSearchCV(estimator=rfr, param_distributions=random_grid,
                                        cv=2, verbose=2, n_jobs=-1)
        rfr_random.fit(X_train, y_train)
        self._model = rfr_random
        predictions = rfr_random.predict(X_test)
        mean_ae = mean_absolute_error(y_test, predictions)
        median_ae = median_absolute_error(y_test, predictions)
        evs = explained_variance_score(y_test, predictions)
        # cv_results = rfr_random.cv_results_
        best_params = rfr_random.best_params_

        dupa = pd.DataFrame({'y_test': y_test, 'predictions': predictions})
        dupa['error'] = dupa['y_test'] - dupa['predictions']
        print(dupa)

        mean_ae_str = str('{:,.2f}'.format(np.round_(mean_ae, 2)))
        median_ae_str = str('{:,.2f}'.format(np.round_(median_ae, 2)))
        evs_str = str(np.round_(evs * 100, 2)) + "%"

        end = time.time()
        rand_time = str(np.round_((end - startes), 2)) + "s"

        results = {"Prediction vector length": len(y_test),
                   "Best params": best_params,
                   'Explained Variance Score': evs_str,
                   'Mean Absolute Error': mean_ae_str,
                   "Median Absolute Error": median_ae_str,
                   "Execution time": rand_time}

        return results

    def create_graphs(self):
        model = self._model
        y_test = self._y_test
        X_test = self._X_test
        predictions = model.predict(X_test)

        fig, ax = plt.subplots()
        range_len = np.arange(0, stop=len(y_test))
        ax.scatter(range_len, y_test, label='Real')
        ax.scatter(range_len, predictions, label='Predicted')
        ax.legend(loc='upper right', shadow=True)
        plt.grid(linestyle='-', linewidth=.3)
        ax.set_xlabel('Measured')
        plt.xticks(range_len)

        ax.set_yticklabels(['{:,}'.format(int(x)) for x in ax.get_yticks().tolist()])

        ax.set_ylabel('Predicted')
        plt.title('Random Forest Predictions')
        plt.savefig('app/static/images/predictions.png')
        print("predictions plot genereted")
        return

    def get_importances(self):
        model = self._model
        X = self._X
        importances = list(model.feature_importances_)
        feature_list = list(X.columns)

        print("feature_list:")
        print(feature_list)

        feature_importances = [(feature, str(np.round(importance*100, 2)) + "%") for feature, importance in
                               zip(feature_list, importances)]

        feature_importances = sorted(feature_importances, key=lambda x: x[1], reverse=True)

        return feature_importances
