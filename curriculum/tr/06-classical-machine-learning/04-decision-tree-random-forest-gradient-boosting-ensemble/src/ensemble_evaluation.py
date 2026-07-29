"""Evaluation helpers for tree ensembles."""
from __future__ import annotations
import numpy as np
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss, roc_auc_score, mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.model_selection import cross_validate, StratifiedKFold

def classification_report(y_true,probability,threshold=0.5):
    p=np.asarray(probability,float); pred=(p>=threshold).astype(int)
    return {
      "accuracy":float(accuracy_score(y_true,pred)),
      "balanced_accuracy":float(balanced_accuracy_score(y_true,pred)),
      "f1":float(f1_score(y_true,pred,zero_division=0)),
      "roc_auc":float(roc_auc_score(y_true,p)),
      "log_loss":float(log_loss(y_true,p,labels=[0,1])),
    }

def regression_report(y_true,prediction):
    return {"mae":float(mean_absolute_error(y_true,prediction)),
            "rmse":float(root_mean_squared_error(y_true,prediction)),
            "r2":float(r2_score(y_true,prediction))}

def cross_validation_report(model,X,y,scoring=("roc_auc","balanced_accuracy"),folds=5):
    cv=StratifiedKFold(n_splits=folds,shuffle=True,random_state=42)
    result=cross_validate(model,X,y,cv=cv,scoring=list(scoring),return_train_score=True,n_jobs=1)
    return {k:float(np.mean(v)) for k,v in result.items() if k.startswith("train_") or k.startswith("test_")}

def generalization_gap(cv_report,metric):
    return float(cv_report[f"train_{metric}"]-cv_report[f"test_{metric}"])
