"""Decision tree utilities and diagnostics."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

def gini_impurity(labels):
    y=np.asarray(labels)
    if y.size==0: return 0.0
    _,c=np.unique(y,return_counts=True); p=c/y.size
    return float(1.0-np.sum(p*p))

def entropy(labels):
    y=np.asarray(labels)
    if y.size==0: return 0.0
    _,c=np.unique(y,return_counts=True); p=c/y.size
    return float(-np.sum(p*np.log2(p)))

def weighted_impurity(left,right,criterion="gini"):
    total=len(left)+len(right)
    if total==0: return 0.0
    fn=gini_impurity if criterion=="gini" else entropy
    return (len(left)*fn(left)+len(right)*fn(right))/total

def information_gain(parent,left,right,criterion="gini"):
    fn=gini_impurity if criterion=="gini" else entropy
    return float(fn(parent)-weighted_impurity(left,right,criterion))

@dataclass(frozen=True)
class TreeSummary:
    depth:int
    leaves:int
    nodes:int

def summarize_tree(model):
    if not hasattr(model,"tree_"): raise RuntimeError("model must be fitted")
    return TreeSummary(model.get_depth(),model.get_n_leaves(),model.tree_.node_count)

def build_classifier(**kwargs):
    return DecisionTreeClassifier(random_state=42,**kwargs)

def build_regressor(**kwargs):
    return DecisionTreeRegressor(random_state=42,**kwargs)

def pruning_path(model,X,y):
    path=model.cost_complexity_pruning_path(X,y)
    return path.ccp_alphas,path.impurities
