from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pytest
from sklearn.datasets import make_classification, make_regression
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
SRC=Path(__file__).resolve().parents[1]/"src"; sys.path.insert(0,str(SRC))
import tree_models as trees
import ensemble_models as ensembles
import ensemble_evaluation as evaluation

@pytest.fixture
def cls():
    return make_classification(n_samples=300,n_features=6,n_informative=4,n_redundant=0,class_sep=1.2,random_state=42)
@pytest.fixture
def reg():
    return make_regression(n_samples=250,n_features=5,noise=5,random_state=42)

def test_gini_pure(): assert trees.gini_impurity([1,1,1])==0
def test_gini_balanced(): assert trees.gini_impurity([0,0,1,1])==pytest.approx(.5)
def test_entropy_pure(): assert trees.entropy([0,0])==0
def test_entropy_balanced(): assert trees.entropy([0,1])==pytest.approx(1)
def test_empty_impurity(): assert trees.gini_impurity([])==0
def test_weighted_impurity(): assert trees.weighted_impurity([0,0],[1,1])==0
def test_information_gain_positive(): assert trees.information_gain([0,0,1,1],[0,0],[1,1])==pytest.approx(.5)
def test_tree_classifier_fit(cls):
    X,y=cls; m=trees.build_classifier(max_depth=3).fit(X,y); assert m.score(X,y)>.8
def test_tree_regressor_fit(reg):
    X,y=reg; m=trees.build_regressor(max_depth=4).fit(X,y); assert m.score(X,y)>.7
def test_tree_summary_requires_fit():
    with pytest.raises(RuntimeError): trees.summarize_tree(trees.build_classifier())
def test_tree_summary(cls):
    X,y=cls; s=trees.summarize_tree(trees.build_classifier(max_depth=2).fit(X,y)); assert s.depth<=2 and s.leaves>=2
def test_pruning_path(cls):
    X,y=cls; m=trees.build_classifier(); a,i=trees.pruning_path(m,X,y); assert len(a)==len(i) and np.all(a>=0)
def test_rf_classifier(cls):
    X,y=cls; m=ensembles.build_random_forest_classifier(n_estimators=30).fit(X,y); assert m.score(X,y)>.95
def test_rf_oob(cls):
    X,y=cls; m=ensembles.build_random_forest_classifier(n_estimators=50).fit(X,y); assert 0<=m.oob_score_<=1
def test_rf_regressor(reg):
    X,y=reg; m=ensembles.build_random_forest_regressor(n_estimators=30).fit(X,y); assert m.score(X,y)>.8
def test_gradient_boosting(cls):
    X,y=cls; m=ensembles.build_gradient_boosting(n_estimators=30).fit(X,y); assert m.score(X,y)>.85
def test_hist_gradient_boosting(cls):
    X,y=cls; m=ensembles.build_hist_gradient_boosting(max_iter=30).fit(X,y); assert m.score(X,y)>.85
def test_adaboost(cls):
    X,y=cls; m=ensembles.build_adaboost(n_estimators=30).fit(X,y); assert m.score(X,y)>.75
def test_normalized_importance(cls):
    X,y=cls; m=ensembles.build_random_forest_classifier(n_estimators=20).fit(X,y); assert ensembles.normalized_feature_importance(m).sum()==pytest.approx(1)
def test_permutation_table(cls):
    X,y=cls; m=ensembles.build_random_forest_classifier(n_estimators=20).fit(X,y); t=ensembles.permutation_importance_table(m,X,y,[f"x{i}" for i in range(X.shape[1])]); assert len(t)==6 and t[0]["importance_mean"]>=t[-1]["importance_mean"]
def test_soft_voting(cls):
    X,y=cls; m=ensembles.build_soft_voting([("lr",LogisticRegression(max_iter=1000)),("dt",DecisionTreeClassifier(max_depth=3,random_state=42))]).fit(X,y); assert hasattr(m,"predict_proba")
def test_stacking(cls):
    X,y=cls; m=ensembles.build_stacking([("lr",LogisticRegression(max_iter=1000)),("dt",DecisionTreeClassifier(max_depth=3,random_state=42))]).fit(X,y); assert m.score(X,y)>.8
def test_classification_report(cls):
    X,y=cls; m=ensembles.build_random_forest_classifier(n_estimators=20).fit(X,y); r=evaluation.classification_report(y,m.predict_proba(X)[:,1]); assert set(r)=={"accuracy","balanced_accuracy","f1","roc_auc","log_loss"}
def test_classification_report_range(cls):
    X,y=cls; m=ensembles.build_random_forest_classifier(n_estimators=20).fit(X,y); r=evaluation.classification_report(y,m.predict_proba(X)[:,1]); assert all(0<=r[k]<=1 for k in ["accuracy","balanced_accuracy","f1","roc_auc"])
def test_regression_report(reg):
    X,y=reg; m=ensembles.build_random_forest_regressor(n_estimators=20).fit(X,y); r=evaluation.regression_report(y,m.predict(X)); assert r["mae"]>=0 and r["rmse"]>=r["mae"] and r["r2"]>.7
def test_cross_validation_report(cls):
    X,y=cls; r=evaluation.cross_validation_report(ensembles.build_random_forest_classifier(n_estimators=15,oob_score=False),X,y,folds=3); assert "test_roc_auc" in r and "train_roc_auc" in r
def test_generalization_gap(): assert evaluation.generalization_gap({"train_auc":.9,"test_auc":.8},"auc")==pytest.approx(.1)
def test_random_state_reproducible(cls):
    X,y=cls; a=ensembles.build_random_forest_classifier(n_estimators=20).fit(X,y).predict(X); b=ensembles.build_random_forest_classifier(n_estimators=20).fit(X,y).predict(X); assert np.array_equal(a,b)
def test_depth_controls_complexity(cls):
    X,y=cls; a=trees.build_classifier(max_depth=1).fit(X,y); b=trees.build_classifier(max_depth=5).fit(X,y); assert b.get_n_leaves()>=a.get_n_leaves()
def test_min_samples_leaf_controls_complexity(cls):
    X,y=cls; a=trees.build_classifier(min_samples_leaf=1).fit(X,y); b=trees.build_classifier(min_samples_leaf=20).fit(X,y); assert b.get_n_leaves()<=a.get_n_leaves()
def test_bootstrap_required_for_oob():
    m=ensembles.build_random_forest_classifier(bootstrap=False,oob_score=False); assert not m.bootstrap
def test_threshold_changes_predictions(cls):
    X,y=cls; m=ensembles.build_random_forest_classifier(n_estimators=20).fit(X,y); p=m.predict_proba(X)[:,1]; assert (p>=.3).sum()>=(p>=.7).sum()
