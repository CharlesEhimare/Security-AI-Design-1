"""export_to_csv.py
Usage: python export_to_csv.py <input_json> <output_csv>
Reads a Prometheus API single query result file and writes timestamp,value CSV
"""
import sys, json, csv
def main():
    if len(sys.argv) < 3:
        print('Usage: python export_to_csv.py <metrics.json> <metrics.csv>')
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2]
    with open(inp) as f:
        data = json.load(f)
    results = data.get('data', {}).get('result', [])
    with open(out, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['timestamp', 'value'])
        for r in results:
            if 'value' in r:
                ts, val = r['value']
                writer.writerow([ts, val])
            elif 'values' in r:
                for ts, val in r['values']:
                    writer.writerow([ts, val])
    print(f'Wrote {out}')
if __name__ == "__main__":
    main()
