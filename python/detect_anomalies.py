"""detect_anomalies.py
Run detection with trained model:
python detect_anomalies.py --csv data/metrics.csv --model data/cpu_model.pkl --out data/metrics_with_anomalies.csv
"""
import pandas as pd, joblib, argparse, os, sys
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--csv', required=True)
    p.add_argument('--model', required=True)
    p.add_argument('--out', default='data/metrics_with_anomalies.csv')
    args = p.parse_args()
    if not os.path.exists(args.csv) or not os.path.exists(args.model):
        print('Required file missing'); sys.exit(1)
    df = pd.read_csv(args.csv)
    X = df[['value']].values
    model = joblib.load(args.model)
    pred = model.predict(X)  # 1 = inlier, -1 = outlier
    df['predicted'] = pred
    df['anomaly'] = df['predicted'] == -1
    print('🔍 Detected Anomalies:')
    print(df[df['anomaly']])
    df.to_csv(args.out, index=False)
    print('Wrote', args.out)
if __name__ == '__main__':
    main()
