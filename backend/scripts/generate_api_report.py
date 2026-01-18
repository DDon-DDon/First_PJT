
import asyncio
import json
import sys
import os
import httpx
from datetime import datetime
from uuid import uuid4
import time

# Configuration
BASE_URL = "http://localhost:8000"
MAX_RETRIES = 5
RETRY_DELAY = 1

async def wait_for_server(client):
    print("Waiting for server to be ready...")
    for i in range(MAX_RETRIES):
        try:
            resp = await client.get("/health")
            if resp.status_code == 200:
                print("Server is ready!")
                return True
        except httpx.ConnectError:
            print(f"Server not ready, retrying ({i+1}/{MAX_RETRIES})...")
            await asyncio.sleep(RETRY_DELAY)
    return False

async def format_response(response):
    try:
        data = response.json()
        return json.dumps(data, indent=2, ensure_ascii=False)
    except:
        return response.text

async def run_test_scenario():
    print(f"# API Test & Log Report")
    print(f"Generated at: {datetime.now().isoformat()}\n")
    print(f"Target Server: {BASE_URL}\n")

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        
        # 1. Wait for Server
        if not await wait_for_server(client):
            print("Error: Could not connect to server.")
            return

        # 2. Health Check
        print("## 1. System Health")
        print("### GET /health")
        response = await client.get("/health")
        print(f"**Status Code**: {response.status_code}")
        print("```json")
        print(await format_response(response))
        print("```\n")

        # 3. Store Management
        print("## 2. Store Management")
        print("### Check Existing Stores (GET /api/v1/stores)")
        
        print("### POST /api/v1/stores (Create Store)")
        store_code = f"STORE-{uuid4().hex[:8]}"
        store_data = {
            "code": store_code,
            "name": f"테스트매장-{store_code}",
            "address": "서울시 강남구 테헤란로",
            "phone": "02-555-0000"
        }
        res = await client.post("/api/v1/stores", json=store_data)
        print(f"**Request Body**: \n```json\n{json.dumps(store_data, indent=2, ensure_ascii=False)}\n```")
        print(f"**Status Code**: {res.status_code}")
        print("```json")
        print(await format_response(res))
        print("```\n")
        
        if res.status_code in (200, 201):
            store_id = res.json()['id']
        else:
            print("Failed to create store. Cannot proceed with inventory tests.")
            return

        # 4. Category Management
        print("## 3. Product Management")
        print("### POST /api/v1/categories (Create Category)")
        cat_code = f"CAT-{uuid4().hex[:4]}"
        cat_data = {
            "code": cat_code,
            "name": f"테스트카테고리-{cat_code}",
            "sort_order": 1
        }
        res = await client.post("/api/v1/categories", json=cat_data)
        print(f"**Request Body**: \n```json\n{json.dumps(cat_data, indent=2, ensure_ascii=False)}\n```")
        print(f"**Status Code**: {res.status_code}")
        print("```json")
        print(await format_response(res))
        print("```\n")

        if res.status_code in (200, 201):
            category_id = res.json()['id']
        else:
            print("Failed to create category.")
            category_id = None

        # 5. Product Creation
        if category_id:
            print("### POST /api/v1/products (Create Product)")
            prod_data = {
                "barcode": f"880{uuid4().int}"[:13],
                "name": "테스트제품-SAMPLE",
                "category_id": category_id,
                "safety_stock": 50
            }
            res = await client.post("/api/v1/products", json=prod_data)
            print(f"**Request Body**: \n```json\n{json.dumps(prod_data, indent=2, ensure_ascii=False)}\n```")
            print(f"**Status Code**: {res.status_code}")
            print("```json")
            print(await format_response(res))
            print("```\n")

            if res.status_code in (200, 201):
                product_id = res.json()['id']
            else:
                product_id = None
        else:
            product_id = None

        # 6. Inventory Transaction (Fixed payload format)
        if store_id and product_id:
            print("## 4. Inventory Transaction")
            print("### POST /api/v1/transactions/inbound (Inbound Stock)")
            # 수정: API는 items 배열이 아닌 flat structure를 기대함
            inbound_data = {
                "product_id": product_id,
                "store_id": store_id,
                "quantity": 100,
                "note": "API 테스트 입고"
            }
            res = await client.post("/api/v1/transactions/inbound", json=inbound_data)
            print(f"**Request Body**: \n```json\n{json.dumps(inbound_data, indent=2, ensure_ascii=False)}\n```")
            print(f"**Status Code**: {res.status_code}")
            print("```json")
            print(await format_response(res))
            print("```\n")

            # 7. Inventory Check (Fixed endpoint path)
            print("## 5. Inventory Check")
            print(f"### GET /api/v1/inventory/stocks?store_id={store_id}")
            res = await client.get(f"/api/v1/inventory/stocks?store_id={store_id}")
            print(f"**Status Code**: {res.status_code}")
            print("```json")
            print(await format_response(res))
            print("```\n")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_test_scenario())
