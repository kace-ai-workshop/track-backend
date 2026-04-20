#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://localhost"

echo "== 1) GET /health =="
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "== 2) POST /shorten =="
CREATE_RESPONSE=$(curl -sS -X POST "$BASE_URL/shorten" -H "Content-Type: application/json" -d '{"url": "https://example.com"}')
echo "$CREATE_RESPONSE" | python3 -m json.tool

SHORT_CODE=$(echo "$CREATE_RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('short_code') or d.get('code') or '')")
[ -n "$SHORT_CODE" ] || { echo "short_code not found"; exit 1; }

echo "== 3) GET /{code} (expect 302) =="
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/$SHORT_CODE")
echo "HTTP status: $HTTP_STATUS"

echo "== 4) GET /stats/{code} =="
curl -sS "$BASE_URL/stats/$SHORT_CODE" | python3 -m json.tool
