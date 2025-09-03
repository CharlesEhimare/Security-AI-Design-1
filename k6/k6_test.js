import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: __ENV.VUS ? parseInt(__ENV.VUS) : 20,
  duration: __ENV.DURATION ? __ENV.DURATION : '1m',
};

const TARGET = __ENV.TARGET || 'http://127.0.0.1:30080/';

export default function () {
  const res = http.get(TARGET);
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
  sleep(1);
}
