from sklearn.ensemble import RandomForestClassifier

class Estimator:
    @staticmethod
    def fit(train_x, train_y):
        return RandomForestClassifier(n_estimators=55).fit(train_x, train_y)

    @staticmethod
    def predict(trained, test_x):
        return trained.predict(test_x)