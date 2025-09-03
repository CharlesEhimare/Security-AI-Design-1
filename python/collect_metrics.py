"""collect_metrics.py
Poll Prometheus repeatedly and create a CSV with timestamp,value rows.
Example: python collect_metrics.py --samples 20 --interval 5 --out data/metrics.csv
"""
import requests, csv, time, argparse, sys
PROM_URL = 'http://localhost:9090/api/v1/query'
DEFAULT_QUERY = 'rate(container_cpu_usage_seconds_total{container="curl"}[1m])'

def get_metric(query):
    r = requests.get(PROM_URL, params={'query': query}, timeout=10)
    r.raise_for_status()
    return r.json()

def parse_first(json_data):
    results = json_data.get('data', {}).get('result', [])
    if not results:
        return None, None
    ts, val = results[0]['value']
    return ts, float(val)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--samples', type=int, default=20)
    p.add_argument('--interval', type=int, default=5)
    p.add_argument('--out', default='data/metrics.csv')
    p.add_argument('--query', default=DEFAULT_QUERY)
    args = p.parse_args()

    with open(args.out, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['timestamp', 'value'])

    print(f"Collecting {args.samples} samples every {args.interval}s to {args.out}")
    for i in range(args.samples):
        try:
            j = get_metric(args.query)
            ts, val = parse_first(j)
            if ts is not None:
                with open(args.out, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([ts, val])
                print(f"Sample {i+1}/{args.samples}: {ts}, {val}")
            else:
                print(f"Sample {i+1}/{args.samples}: no data returned")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(args.interval)

if __name__ == '__main__':
    main()
