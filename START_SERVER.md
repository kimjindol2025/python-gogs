# Python University v7 - 웹 서버 실행 가이드

## 🚀 서버 실행 방법

### 옵션 1: 간단한 테스트 서버 (권장)
```bash
python3 simple_server.py
```

### 옵션 2: 전체 기능 서버
```bash
python3 university_v7_app.py
```

### 옵션 3: 스크립트로 실행
```bash
./RUN_WEB_SERVER.sh
```

---

## 🌐 접속 주소

브라우저에서 다음 주소로 접속하세요:

**http://localhost:5000**

---

## 🔧 포트 변경 (연결 안 될 경우)

### 다른 포트로 변경하려면:

```bash
# 포트 8000으로 실행
export FLASK_ENV=development
python3 -c "
from simple_server import app
app.run(debug=False, host='127.0.0.1', port=8000)
"
```

그 후 브라우저에서: **http://localhost:8000**

---

## ✅ 확인 사항

1. ✓ Flask가 설치되어 있는가?
   ```bash
   pip3 install flask
   ```

2. ✓ 포트 5000이 사용 가능한가?
   ```bash
   netstat -tuln | grep 5000
   ```

3. ✓ 파일이 현재 디렉토리에 있는가?
   ```bash
   ls -la *.py
   ```

---

## 📊 테스트 기능

웹 페이지에서:
- ✅ 학생 목록 조회 버튼 클릭
- ✅ 학과 정보 조회 버튼 클릭
- ✅ 교과목 조회 버튼 클릭

모든 데이터가 실시간으로 로드됩니다!

---

## 🛑 서버 종료

터미널에서 **Ctrl+C** 누르기

---

## 💡 문제 해결

### 연결 거부됨
```bash
# 방화벽 확인
sudo ufw allow 5000
```

### Address already in use
```bash
# 다른 프로세스가 포트 점유
lsof -i :5000
kill -9 <PID>
```

### ModuleNotFoundError: No module named 'flask'
```bash
pip3 install flask --upgrade
```

---

## 기록이 증명이다 gogs

서버가 실제로 작동하면 축하합니다! 🎉
