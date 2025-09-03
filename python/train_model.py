"""train_model.py
Train One-Class SVM on metrics.csv (value column). Usage:
python train_model.py --csv data/metrics.csv --model data/cpu_model.pkl --nu 0.1
"""
import pandas as pd, joblib, argparse, os, sys
from sklearn.svm import OneClassSVM

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--csv', required=True)
    p.add_argument('--model', required=True)
    p.add_argument('--nu', type=float, default=0.1)
    args = p.parse_args()
    if not os.path.exists(args.csv):
        print('CSV not found:', args.csv); sys.exit(1)
    df = pd.read_csv(args.csv)
    if 'value' not in df.columns:
        print('value column missing'); sys.exit(1)
    X = df[['value']].values
    model = OneClassSVM(kernel='rbf', gamma='scale', nu=args.nu)
    model.fit(X)
    joblib.dump(model, args.model)
    print('✅ One-Class SVM model trained and saved as', args.model)

if __name__ == '__main__':
    main()
