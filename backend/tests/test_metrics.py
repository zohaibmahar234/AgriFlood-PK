import numpy as np
from scripts.evaluate_masks import metrics

def test_metric_math_with_synthetic_fixture_only():
    p=np.array([[1,1],[0,0]],dtype=bool); r=np.array([[1,0],[1,0]],dtype=bool)
    m=metrics(p,r)
    assert m['tp']==1 and m['fp']==1 and m['fn']==1 and m['tn']==1
    assert round(m['f1'],3)==0.5 and round(m['iou'],3)==0.333
