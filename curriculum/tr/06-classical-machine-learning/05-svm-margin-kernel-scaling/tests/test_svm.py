"""Tests for SVM kernels, models, and pipelines."""

from __future__ import annotations
import importlib.util, sys
from pathlib import Path
import numpy as np, pandas as pd, pytest
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

def load(name):
    spec = importlib.util.spec_from_file_location(name, SRC / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

kernels, models, pipelines = load("kernel_functions"), load("svm_models"), load("svm_pipeline")

@pytest.fixture
def binary_data():
    return make_classification(n_samples=320, n_features=5, n_informative=5, n_redundant=0, n_clusters_per_class=1, class_sep=2.5, flip_y=0.0, random_state=42)

@pytest.fixture
def mixed_frame():
    rng=np.random.default_rng(8); n=220
    age=rng.normal(40,9,n); spend=rng.normal(110,24,n); region=rng.choice(["north","south","west"],n)
    logits=-4.5+0.065*age+0.02*spend+(region=="south")*0.9
    y=rng.binomial(1,1/(1+np.exp(-logits)))
    x=pd.DataFrame({"age":age,"spend":spend,"region":region}); x.loc[0,"age"]=np.nan; x.loc[1,"region"]=None
    return x,y

def test_01(): assert kernels.linear_kernel([[1,2]],[[3,4]]).item()==pytest.approx(11)
def test_02(): assert kernels.linear_kernel(np.ones((3,2)),np.ones((4,2))).shape==(3,4)
def test_03():
    with pytest.raises(ValueError): kernels.linear_kernel([[1,2]],[[1,2,3]])
def test_04(): assert kernels.polynomial_kernel([[1,2]],[[3,4]],degree=1,gamma=2,coef0=1).item()==pytest.approx(23)
def test_05():
    with pytest.raises(ValueError): kernels.polynomial_kernel([[1]],[[1]],degree=0)
def test_06():
    with pytest.raises(ValueError): kernels.polynomial_kernel([[1]],[[1]],gamma=0)
def test_07(): assert kernels.rbf_kernel([[1,2]],[[1,2]],gamma=.5).item()==pytest.approx(1)
def test_08():
    x=np.array([[0.,1.],[2.,3.]]); k=kernels.rbf_kernel(x,x,gamma=.3); assert np.allclose(k,k.T)
def test_09():
    k=kernels.rbf_kernel([[0],[2]],[[1],[3]],gamma=.4); assert np.all((k>0)&(k<=1))
def test_10():
    with pytest.raises(ValueError): kernels.rbf_kernel([[1]],[[1]],gamma=-1)
def test_11(): assert kernels.hinge_loss([-1,1],[-2,2])==pytest.approx(0)
def test_12(): assert kernels.hinge_loss([1,-1],[.5,.25])==pytest.approx(.875)
def test_13():
    with pytest.raises(ValueError): kernels.hinge_loss([0,1],[.1,.9])
def test_14():
    with pytest.raises(ValueError): kernels.hinge_loss([1],[.1,.2])
def test_15(): assert kernels.svm_primal_objective([1,0],[1],[.5],c=2)==pytest.approx(1.5)
def test_16():
    with pytest.raises(ValueError): kernels.svm_primal_objective([1],[1],[1],c=0)
def test_17(): assert kernels.margin_width([3,4])==pytest.approx(.4)
def test_18():
    with pytest.raises(ValueError): kernels.margin_width([0,0])
def test_19():
    with pytest.raises(ValueError): models.build_linear_svm(c=0)
def test_20():
    with pytest.raises(ValueError): models.build_kernel_svm(kernel="bad")
def test_21():
    with pytest.raises(ValueError): models.build_kernel_svm(gamma=0)
def test_22(binary_data):
    x,y=binary_data; m=models.build_linear_svm().fit(x,y); assert m.score(x,y)>.9
def test_23(binary_data):
    x,y=binary_data; m=models.build_kernel_svm(c=2).fit(x,y); assert m.score(x,y)>.95
def test_24(binary_data):
    x,y=binary_data; m=models.build_kernel_svm().fit(x,y); assert 0<models.support_vector_fraction(m,len(y))<=1
def test_25():
    with pytest.raises(ValueError): models.support_vector_fraction(models.build_kernel_svm(),10)
def test_26(binary_data):
    x,y=binary_data; m=models.build_kernel_svm().fit(x,y)
    with pytest.raises(ValueError): models.support_vector_fraction(m,0)
def test_27():
    with pytest.raises(ValueError): models.calibrate_svm(models.build_linear_svm(),method="bad")
def test_28(binary_data):
    x,y=binary_data; m=models.calibrate_svm(models.build_linear_svm(),cv=2).fit(x,y); assert m.predict_proba(x[:5]).shape==(5,2)
def test_29(): assert models.predict_with_threshold([.2,.5,.9],.5).tolist()==[0,1,1]
def test_30():
    with pytest.raises(ValueError): models.predict_with_threshold([.5],1.1)
def test_31(binary_data):
    x,y=binary_data; xt,xv,yt,yv=train_test_split(x,y,test_size=.3,stratify=y,random_state=42)
    m=models.build_kernel_svm(probability=True).fit(xt,yt); pr=m.predict_proba(xv)[:,1]
    r=models.evaluate_classifier(yv,scores=m.decision_function(xv),predictions=m.predict(xv),probabilities=pr)
    assert r.roc_auc>.9 and r.brier is not None
def test_32(): assert len(pipelines.build_preprocessor(["age"],["region"]).transformers)==2
def test_33(mixed_frame):
    x,y=mixed_frame; p=pipelines.build_svm_pipeline(["age","spend"],["region"],kernel="linear").fit(x,y)
    assert p.predict(pd.DataFrame({"age":[np.nan],"spend":[120.],"region":["east"]})).shape==(1,)
def test_34():
    with pytest.raises(ValueError): pipelines.build_svm_pipeline([],[],c=0)
def test_35(mixed_frame):
    x,y=mixed_frame; p=pipelines.build_svm_pipeline(["age","spend"],["region"])
    s=pipelines.build_svm_grid_search(p,cv=2,n_jobs=1).fit(x,y); assert "model__C" in s.best_params_
