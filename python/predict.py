import joblib, pandas as pd, sys, argparse
p = argparse.ArgumentParser()
p.add_argument('--model', default='data/cpu_model.pkl')
p.add_argument('values', nargs='*', help='numeric values to predict', default=[])
args = p.parse_args()
model = joblib.load(args.model)
if args.values:
    vals = [float(v) for v in args.values]
else:
    vals = [0.001]
df = pd.DataFrame({'value': vals})
pred = model.predict(df[['value']].values)
print('Predictions (1=inlier, -1=outlier):', pred)
