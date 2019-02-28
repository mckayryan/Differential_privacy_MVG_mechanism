import numpy
import operator
import random

from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.kernel_ridge import KernelRidge
from scipy.stats import uniform


def kernel_ridge_param_search(
        X, y,
        scoring,
        kernel,
        cv_folds=5,
        random=True,
        max_alpha=3,
        max_gamma=3,
        random_iters=20):

    krr = KernelRidge(kernel=kernel)

    if random is True:
        # Randomised parameter search
        param_dist = dict(alpha=uniform(0.0001, max_alpha),
                          gamma=uniform(0.0001, max_gamma))
        n_iter_randomised = random_iters

        param_search = RandomizedSearchCV(
            estimator=krr,
            param_distributions=param_dist,
            n_iter=n_iter_randomised,
            scoring=scoring,
            cv=cv_folds)
    else:
        # Grid parameter search
        param_grid = dict(alpha=numpy.arange(0.1, max_alpha, 0.1),
                          gamma=numpy.arange(0.1, max_gamma, 0.1))

        param_search = GridSearchCV(
            estimator=krr,
            param_grid=param_grid,
            scoring=scoring,
            cv=cv_folds)

    return param_search.fit(X, y).best_params_


def kernel_ridge_cv(X, y, scoring, cv_folds, **kwargs):

    # Apply Kernel Ridge Regression with empirically selected parameters
    KRR = KernelRidge(**kwargs)

    # Calculate metric RMSE using
    cv_score = cross_val_score(
        estimator=KRR,
        X=X,
        y=y,
        scoring=scoring,
        cv=cv_folds)

    return numpy.array(abs(cv_score))


def krr_private_cross_validate(train_X,
                               train_y,
                               test_X,
                               test_y,
                               krr,
                               scoring_function,
                               score_summary_function=None,
                               cv_folds=5):

    train_selected = range(len(train_y))
    fold_sample_size = int(len(train_y) / cv_folds)

    res = numpy.empty(cv_folds)

    for fold in xrange(cv_folds):

        fold_sample = [
            train_selected.pop(random.randrange(len(train_selected)))
            for _ in xrange(fold_sample_size)]

        krr.fit(train_X[fold_sample],
                train_y[fold_sample])

        y_hat = krr.predict(test_X[fold_sample])

        res[fold] = scoring_function(y_true=test_y[fold_sample],
                                     y_pred=y_hat)

    if score_summary_function is not None:
        summary_res = score_summary_function(res)
    else:
        summary_res = res

    return summary_res


def krr_private_param_rand_search(train_X,
                                  train_y,
                                  test_X,
                                  test_y,
                                  rand_iters,
                                  krr_kernel,
                                  scoring_function,
                                  train_split=0.8):

    # Randomised parameter search
    param_selections = dict()
    param_dist = dict(alpha=uniform(0.0001, 4),
                      gamma=uniform(0.0001, 4))

    for _ in range(rand_iters):

        a = round(param_dist['alpha'].rvs(1)[0], 4)
        g = round(param_dist['gamma'].rvs(1)[0], 4)

        model = KernelRidge(kernel=krr_kernel, alpha=a, gamma=g)

        param_selections[(a, g)] = krr_private_cross_validate(
            train_X=train_X,
            train_y=train_y,
            test_X=test_X,
            test_y=test_y,
            krr=model,
            score_summary_function=numpy.mean,
            scoring_function=scoring_function)

    best_alpha, best_gamma = \
        min(param_selections.iteritems(), key=operator.itemgetter(1))[0]

    return dict(
        best_alpha=best_alpha,
        best_gamma=best_gamma,
        best_rmse=min(param_selections.values()),
        results=param_selections)
