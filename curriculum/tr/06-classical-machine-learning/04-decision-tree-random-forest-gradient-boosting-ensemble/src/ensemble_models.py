"""Bagging, random forest, boosting, voting, and stacking helpers."""
from __future__ import annotations
import numpy as np
from sklearn.ensemble import (
    AdaBoostClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier,
    RandomForestClassifier, RandomForestRegressor, VotingClassifier, StackingClassifier
)
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance

def build_random_forest_classifier(**kwargs):
    defaults=dict(n_estimators=100,random_state=42,n_jobs=1,oob_score=True,bootstrap=True)
    defaults.update(kwargs); return RandomForestClassifier(**defaults)

def build_random_forest_regressor(**kwargs):
    defaults=dict(n_estimators=100,random_state=42,n_jobs=1,oob_score=True,bootstrap=True)
    defaults.update(kwargs); return RandomForestRegressor(**defaults)

def build_gradient_boosting(**kwargs):
    defaults=dict(random_state=42); defaults.update(kwargs)
    return GradientBoostingClassifier(**defaults)

def build_hist_gradient_boosting(**kwargs):
    defaults=dict(random_state=42); defaults.update(kwargs)
    return HistGradientBoostingClassifier(**defaults)

def build_adaboost(**kwargs):
    defaults=dict(random_state=42); defaults.update(kwargs)
    return AdaBoostClassifier(**defaults)

def build_soft_voting(estimators):
    return VotingClassifier(estimators=estimators,voting="soft")

def build_stacking(estimators):
    final=Pipeline([("scale",StandardScaler()),("model",LogisticRegression(max_iter=1000))])
    return StackingClassifier(estimators=estimators,final_estimator=final,stack_method="predict_proba")

def normalized_feature_importance(model):
    values=np.asarray(model.feature_importances_,dtype=float)
    total=values.sum()
    return values if total==0 else values/total

def permutation_importance_table(model,X,y,feature_names,scoring=None,n_repeats=5):
    result=permutation_importance(model,X,y,scoring=scoring,n_repeats=n_repeats,random_state=42,n_jobs=1)
    rows=[{"feature":str(n),"importance_mean":float(m),"importance_std":float(s)}
          for n,m,s in zip(feature_names,result.importances_mean,result.importances_std)]
    return sorted(rows,key=lambda r:r["importance_mean"],reverse=True)
