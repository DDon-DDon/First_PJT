# API Test & Log Report
Generated at: 2026-01-18T21:00:13.436424

Target Server: http://localhost:8000

Waiting for server to be ready...
Server is ready!
## 1. System Health
### GET /health
**Status Code**: 200
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

## 2. Store Management
### Check Existing Stores (GET /api/v1/stores)
### POST /api/v1/stores (Create Store)
**Request Body**: 
```json
{
  "code": "STORE-26ca51b2",
python.exe : Traceback (most recent call last):
위치 C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\scripts\run_api_test.ps1:70 문자:1
+ & $VenvPython $ReportScript 2>&1 | Out-File -Encoding UTF8 $ReportLog
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (most recent call last)::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
  "name": "테스트매장-STORE-26ca51b2",
  "address": "서울시 강남구 테헤란로",
  "phone": "02-555-0000"
}
```
**Status Code**: 201
```json
{
  "code": "STORE-26ca51b2",
  "name": "테스트매장-STORE-26ca51b2",
  "address": "서울시 강남구 테헤란로",
  "phone": "02-555-0000",
  "isActive": true,
  "id": "bdb1aa47-f2c8-41d9-909d-a2f8d7486ada"
}
```

## 3. Product Management
### POST /api/v1/categories (Create Category)
**Request Body**: 
```json
{
  "code": "CAT-ec11",
  "name": "테스트카테고리-CAT-ec11",
  "sort_order": 1
}
```
**Status Code**: 201
```json
{
  "id": "6659643f-df2c-4385-8f6a-82d1933e143c",
  "code": "CAT-ec11",
  "name": "테스트카테고리-CAT-ec11",
  "sortOrder": 1
}
```

### POST /api/v1/products (Create Product)
**Request Body**: 
```json
{
  "barcode": "8801239322395",
  "name": "테스트제품-SAMPLE",
  "category_id": "6659643f-df2c-4385-8f6a-82d1933e143c",
  "safety_stock": 50
}
```
**Status Code**: 201
```json
{
  "id": "4a788ff7-7f95-4486-ad1b-e2389125b473",
  "barcode": "8801239322395",
  "name": "테스트제품-SAMPLE",
  "categoryId": "6659643f-df2c-4385-8f6a-82d1933e143c",
  "safetyStock": 50,
  "imageUrl": null,
  "memo": null,
  "isActive": true,
  "createdAt": "2026-01-18T12:00:14.256798",
  "updatedAt": null
}
```

## 4. Inventory Transaction
### POST /api/v1/transactions/inbound (Inbound Stock)
**Request Body**: 
```json
{
  "product_id": "4a788ff7-7f95-4486-ad1b-e2389125b473",
  "store_id": "bdb1aa47-f2c8-41d9-909d-a2f8d7486ada",
  "quantity": 100,
  "note": "API 테스트 입고"
}
```
**Status Code**: 500
```json
Internal Server Error
```

## 5. Inventory Check
### GET /api/v1/inventory/stocks?store_id=bdb1aa47-f2c8-41d9-909d-a2f8d7486ada
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpx\_transports\default.py", line 67, in map_httpcore_exceptions
    yield
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpx\_transports\default.py", line 371, in handle_async_request
    resp = await self._pool.handle_async_request(req)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpcore\_async\connection_pool.py", line 256, in handle_async_requ
est
    raise exc from None
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpcore\_async\connection_pool.py", line 236, in handle_async_requ
est
    response = await connection.handle_async_request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpcore\_async\connection.py", line 103, in handle_async_request
    return await self._connection.handle_async_request(request)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpcore\_async\http11.py", line 136, in handle_async_request
    raise exc
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpcore\_async\http11.py", line 106, in handle_async_request
    ) = await self._receive_response_headers(**kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpcore\_async\http11.py", line 177, in _receive_response_headers
    event = await self._receive_event(timeout=timeout)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpcore\_async\http11.py", line 217, in _receive_event
    data = await self._network_stream.read(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpcore\_backends\anyio.py", line 32, in read
    with map_exceptions(exc_map):
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpcore\_exceptions.py", line 14, in map_exceptions
    raise to_exc(exc) from exc
httpcore.ReadError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\scripts\generate_api_report.py", line 157, in <module>
    asyncio.run(run_test_scenario())
  File "C:\Users\isakq\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\asyncio\runners.py", line 195, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\asyncio\base_events.py", line 691, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\scripts\generate_api_report.py", line 148, in run_test_scenario
    res = await client.get(f"/api/v1/inventory/stocks?store_id={store_id}")
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpx\_client.py", line 1786, in get
    return await self.request(
           ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpx\_client.py", line 1559, in request
    return await self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpx\_client.py", line 1646, in send
    response = await self._send_handling_auth(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpx\_client.py", line 1674, in _send_handling_auth
    response = await self._send_handling_redirects(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpx\_client.py", line 1711, in _send_handling_redirects
    response = await self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpx\_client.py", line 1748, in _send_single_request
    response = await transport.handle_async_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpx\_transports\default.py", line 370, in handle_async_request
    with map_httpcore_exceptions():
         ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\isakq\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "C:\Users\isakq\OneDrive\Desktop\my_github\First_PJT\backend\.venv\Lib\site-packages\httpx\_transports\default.py", line 84, in map_httpcore_exceptions
    raise mapped_exc(message) from exc
httpx.ReadError
