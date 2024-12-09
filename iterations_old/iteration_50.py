import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

class FeatureImportance:
    def __init__(self):
        self.x = []
        self.y = []

    def load_data(self, file_name):
        try:
            data = np.loadtxt(file_name)
            self.x = data[:, 0]
            self.y = data[:, 1]
        except FileNotFoundError:
            print("File not found.")

    def save_data(self, file_name):
        with open(file_name, 'w') as f:
            f.write(str(self.x) + '\n' + str(self.y))

    def get_feature_importance(self, features):
        try:
            # Create a Permutation Tree Regressor
            X = self.x[features]
            y = self.y[features]

            model = DecisionTreeRegressor()
            model.fit(X.values.reshape(-1, 7), y)

            X_train_importance = model.predict(X.values.reshape(-1, 7))
            X_val_importance = model.predict(X[val].values.reshape(-1, 7))

            return X_train_importance, X_val_importance
        except Exception as e:
            print(f"Error: {e}")

    def split_data(self):
        try:
            features = np.arange(len(self.x))
            return train_test_split(features, test_size=0.2)
        except Exception as e:
            print(f"Error: {e}")


def load_data(file_name):
    data = {}
    with open(file_name, 'r') as f:
        for line in f.readlines():
            columns = line.strip().split(',')
            if len(columns) == 3:
                column_names = [columns[0], columns[1]]
                value = np.loadtxt(f'{file_name}.{column_names[1]}')
                data[column_names[0]] = value
    return FeatureImportance()


def save_data(file_name, features):
    feature_importance = []
    for i in range(len(features)):
        X = [features[j] for j in range(i+1)]
        y = [features[i]]
        model = DecisionTreeRegressor()
        model.fit(X, y)
        feature_importance.append(model.predict(X))

    with open(file_name, 'w') as f:
        for i in range(len(feature_importance)):
            for j in range(i+1):
                f.write(str(feature_importance[i][j]) + '\n')


def main():
    file_name = 'data.txt'
    features = load_data(file_name)
    print("Loaded Data:")
    print(features.x)
    print(features.y)

    # Feature importance calculation
    feature_importance = FeatureImportance()
    feature_importance.load_data(file_name)
    X_train_importance, X_val_importance = feature_importance.get_feature_importance(features.x)
    feature_importance.save_data('feature_importances.txt')

    if not np.isnan(X_train_importance).all():
        # Split the data into features and target
        train_idx, val_idx = feature_importance.split_data()
        features = np.concatenate((features.x[train_idx], features.x[val_idx]), axis=0)
        y = np.concatenate((features.y[train_idx], features.y[val_idx]))

        print("\nSplit Data:")
        print(features)
        print(y)

        # Train a model on the training data
        train_features = X_train_importance
        train_labels = y

        model = DecisionTreeRegressor()
        model.fit(train_features, train_labels)

        # Predict on the validation set and get the mean squared error
        predictions = model.predict(X_val_importance)
        mse = mean_squared_error(y, predictions)

        print(f"\nValidation Mean Squared Error: {mse:.2f}")


if __name__ == "__main__":
    main()