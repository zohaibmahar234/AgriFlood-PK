import argparse, json
import numpy as np

def metrics(pred, ref, valid=None):
    pred=np.asarray(pred).astype(bool); ref=np.asarray(ref).astype(bool)
    if pred.shape!=ref.shape: raise ValueError('Prediction and reference shapes must match.')
    if valid is None: valid=np.ones(pred.shape,dtype=bool)
    else: valid=np.asarray(valid).astype(bool)
    p=pred[valid]; r=ref[valid]
    tp=int(np.sum(p & r)); fp=int(np.sum(p & ~r)); fn=int(np.sum(~p & r)); tn=int(np.sum(~p & ~r))
    precision=tp/(tp+fp) if tp+fp else None
    recall=tp/(tp+fn) if tp+fn else None
    f1=(2*precision*recall/(precision+recall)) if precision is not None and recall is not None and (precision+recall) else None
    iou=tp/(tp+fp+fn) if tp+fp+fn else None
    return {'tp':tp,'fp':fp,'fn':fn,'tn':tn,'precision':precision,'recall':recall,'f1':f1,'iou':iou}

def main():
    ap=argparse.ArgumentParser(description='Evaluate binary prediction/reference masks on a common grid.')
    ap.add_argument('prediction_npy'); ap.add_argument('reference_npy'); ap.add_argument('--valid-npy')
    a=ap.parse_args(); pred=np.load(a.prediction_npy); ref=np.load(a.reference_npy); valid=np.load(a.valid_npy) if a.valid_npy else None
    print(json.dumps(metrics(pred,ref,valid),indent=2))
if __name__=='__main__': main()
