import sklearn
import numpy as np
import statsmodels.api as sm

#Conducts logistic regression on the given split
def log_regression(X_train, X_test, y_train, y_test):
    # Normalize the data, fitting the scaler only to train and transforming both train and test
    scaler = sklearn.preprocessing.StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    
    #Add constants
    X_train = sm.add_constant(X_train)
    X_test = sm.add_constant(X_test)
    
    model = sm.Logit(y_train, X_train)
    return model.fit()


def evaluate_predictions(y_test, output):
    print('Accuracy:', sklearn.metrics.accuracy_score(y_test, output))
    print('Precision:', sklearn.metrics.precision_score(y_test, output))
    print('Recall:', sklearn.metrics.recall_score(y_test, output))
    print('F1:', sklearn.metrics.f1_score(y_test, output))

def find_optimal_cutoff(y_test, output, cutoffs = np.linspace(0.1,1,10)):
    best_f1 = 0
    best_threshold = 0

    for cutoff in cutoffs:
        predictions = output > cutoff
        temp_f1 = sklearn.metrics.f1_score(y_test, predictions)
        if temp_f1 > best_f1:
            best_f1 = temp_f1
            best_threshold = cutoff
    print('Best threshold:', best_threshold)
    print('Best F1:', best_f1)

    predictions = output > best_threshold
    
    accuracy = sklearn.metrics.accuracy_score(y_test, predictions)
    print('Accuracy:', accuracy)
    precision = sklearn.metrics.precision_score(y_test, predictions)
    print('Precision:', precision)
    recall = sklearn.metrics.recall_score(y_test, predictions)
    print('Recall:', recall)