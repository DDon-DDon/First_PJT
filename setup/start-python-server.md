### Step 1.
> Python 설치 확인

```bash
python --version
```

- 안 나오면 👉 https://www.python.org
- ✔ 설치할 때 “Add Python to PATH” 꼭 체크

### Step 2.  프로젝트 폴더로 이동
```bash
call cd backend
```

### Step 3. 가상환경 생성
```bash
python -m venv venv
```

### Step 4. 가상환경 활성화
```bash
call .venv/Scripts/activate.bat
```

### Step 5. 의존성 설치
```bash
pip install -r requirements.txt
```

### Step 6. DB 시작하기

```bash
call ./scripts/db-start.bat
```

### Step 7. 서버 시작하기

```bash
call ./scripts/dev-server.bat
```


### Step 8. DB 종료하기

```bash
call call ./scripts/db-stop.bat
```
