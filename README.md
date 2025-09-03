# Kubernetes Monitoring + ML Anomaly Detection

This project contains scripts and manifests used to reproduce the monitoring + ML anomaly detection pipeline:
- k6 load generation
- Kubernetes manifests for a small CPU-bound Flask app (optional) and nginx example
- Python scripts to collect Prometheus metrics, export to CSV, train a One-Class SVM and detect anomalies

## Quickstart (assumes Kubernetes + Prometheus stack)

1. Build & deploy CPU-heavy Flask app (optional)
   ```bash
   docker build -t your-docker-repo/cpu-app:latest ./k8s/flask-cpu-app
   docker push your-docker-repo/cpu-app:latest
   kubectl apply -f k8s/flask-cpu-app/deployment.yaml
   kubectl apply -f k8s/flask-cpu-app/service.yaml
   ```
2. Or use the nginx pod manifest and expose NodePort for testing:
   ```bash
   kubectl apply -f k8s/nginx/nginx-pod.yaml
   kubectl expose pod nginx-server --type=NodePort --name=nginx-service --port=80 --target-port=80 --node-port=30080
   ```
3. Run your k6 test to generate traffic:
   ```bash
   cd k6
   VUS=50 DURATION=2m TARGET="http://<NODE_IP>:30080" k6 run k6_test.js
   ```
4. Port-forward Prometheus and collect metrics:
   ```bash
   kubectl port-forward -n monitoring prometheus-prometheus-stack-kube-prom-prometheus-0 9090
   curl --globoff "http://localhost:9090/api/v1/query?query=rate(container_cpu_usage_seconds_total{container=\"curl\"}[1m])" -o data/metrics.json
   python3 python/export_to_csv.py data/metrics.json data/metrics.csv
   ```
5. Or collect many samples automatically:
   ```bash
   python3 python/collect_metrics.py --samples 30 --interval 5 --out data/metrics.csv
   ```
6. Train and detect:
   ```bash
   python3 -m pip install -r requirements.txt --user
   python3 python/train_model.py --csv data/metrics.csv --model data/cpu_model.pkl
   python3 python/detect_anomalies.py --csv data/metrics.csv --model data/cpu_model.pkl --out data/metrics_with_anomalies.csv
   ```
