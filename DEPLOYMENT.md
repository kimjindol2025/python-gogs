# 🚀 **배포 및 실행 가이드**

> Python University 분산 시스템 & 양자 보안 연구 — 설치, 실행, 배포 절차

---

## **환경 요구사항**

### 시스템 요구사항

```
OS: Linux (Ubuntu/Debian) 또는 Termux (Android)
Python: 3.10 이상
메모리: 최소 512MB (권장 1GB+)
CPU: 2 코어 이상 (multiprocessing 최적화)
디스크: 100MB 이상 여유 공간
```

### Python 버전 확인

```bash
python3 --version
# Python 3.10.0 이상

python3 -m venv --version
# 가상 환경 지원 확인
```

---

## **Step 1: 저장소 클론**

### 원격 저장소에서 클론

```bash
# Gogs 저장소 클론
git clone https://gogs.dclub.kr/kim/gogs_python.git
cd gogs_python

# 또는 로컬 경로
cd /data/data/com.termux/files/home/python-gogs
```

### 저장소 상태 확인

```bash
git status
# 모든 파일이 최신인지 확인

git log --oneline
# 최근 커밋 확인
```

---

## **Step 2: 가상 환경 설정**

### 가상 환경 생성

```bash
# Python 3의 venv 사용
python3 -m venv venv

# 또는 virtualenv 사용
virtualenv -p python3 venv
```

### 가상 환경 활성화

```bash
# Linux/macOS/Termux
source venv/bin/activate

# Windows (예: Git Bash)
source venv/Scripts/activate
```

### 가상 환경 비활성화

```bash
deactivate
```

---

## **Step 3: 의존성 설치**

### 필요한 패키지

```bash
# 기본 패키지
pip install --upgrade pip setuptools wheel

# 선택사항: 데이터 분석
pip install numpy pandas
```

### 현재 구현에는 외부 의존성이 최소화됨

```python
# Python 표준 라이브러리만 사용
import unittest
import time
import multiprocessing
import random
import math
import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Tuple, Any
```

---

## **Step 4: 테스트 실행**

### v8.2: 데이터 레이크 테스트

```bash
cd /data/data/com.termux/files/home/python-gogs

# 테스트 실행
python3 test_v8_2_data_lake.py -v

# 예상 출력:
# test_01_append_log_entry (__main__.TestLogReplicator) ... ok
# ... (16개 테스트 모두 ok)
# Ran 16 tests in 2.345s
# OK
```

### v8.3: 양자 암호화 테스트

```bash
python3 test_v8_3_quantum_crypto.py -v

# 예상 출력:
# Ran 19 tests in 3.127s
# OK
```

### v8.4: 그랜드 통합 테스트

```bash
python3 test_v8_4_grand_unified.py -v

# 예상 출력:
# Ran 10 tests in 1.456s
# OK
```

### v9.3: 행성급 합의 테스트

```bash
python3 test_v9_3_consensus.py -v

# 예상 출력:
# Ran 15 tests in 2.789s
# OK
```

### 전체 테스트 실행

```bash
# 한 번에 모든 테스트 실행
for test_file in test_v*.py; do
    echo "=============== $test_file ==============="
    python3 "$test_file" -v
done

# 예상: 60개 테스트 모두 PASS
```

---

## **Step 5: 메인 프로그램 실행**

### v8.2: 데이터 레이크 실행

```bash
python3 university_v8_2_DISTRIBUTED_DATA_LAKE.py

# 예상 출력:
# ╔══════════════════════════════════════════════════════╗
# ║   【 v8.2: 데이터 레이크 & 분산 병렬 처리 】        ║
# ║   Python PhD 박사 과정 2 — 두 번째 연구             ║
# ╚══════════════════════════════════════════════════════╝
#
# [SECTION 1] Range: [250,250,250,250] std=0.0 | Hash: [248,251,254,247] std=2.87
# [SECTION 2] 100,000 항목 → 직렬 45ms / 병렬 18ms = 2.4x
# ... (7개 섹션 모두 출력)
```

### v8.3: 양자 암호화 실행

```bash
python3 university_v8_3_QUANTUM_RESISTANT_CRYPTO.py

# 예상 출력:
# 【 v8.3: 양자 저항 암호화 】
# ... (보안 분석 결과)
```

### v8.4: 그랜드 통합 실행

```bash
python3 university_v8_4_GRAND_UNIFIED_ARCHITECTURE.py

# 예상 출력:
# 【 v8.4: 그랜드 통합 아키텍처 】
# 【 박사 학위 검증: 성공! 】
# ═══════════════════════════════════════════
# 학위증명서
# ═══════════════════════════════════════════
# ...
```

### v9.3: 행성급 합의 실행

```bash
python3 university_v9_3_PLANETARY_CONSENSUS.py

# 예상 출력:
# 【 v9.3: 행성급 분산 합의 시스템 】
# ... (Raft 합의 결과)
```

---

## **Step 6: 성능 벤치마킹**

### v8.2 벤치마크

```bash
# 직렬 vs 병렬 비교
python3 -c "
from university_v8_2_DISTRIBUTED_DATA_LAKE import DataLakeOrchestrator
import time

data = list(range(100000))
orchestrator = DataLakeOrchestrator()

# 직렬 처리
start = time.time()
orchestrator.run_full_pipeline(data)
serial_time = time.time() - start

# 병렬 처리
start = time.time()
orchestrator.run_full_pipeline(data)
parallel_time = time.time() - start

print(f'직렬: {serial_time:.2f}ms, 병렬: {parallel_time:.2f}ms')
print(f'향상도: {serial_time/parallel_time:.2f}x')
"
```

### 시스템 리소스 모니터링

```bash
# 리소스 사용량 확인 (Linux)
watch -n 1 'ps aux | grep python | grep university'

# 또는 top 명령
top
```

---

## **Step 7: Git 작업 흐름**

### 변경사항 확인

```bash
# 상태 확인
git status

# 변경사항 확인
git diff
```

### 커밋 및 푸시

```bash
# 변경사항 스테이징
git add -A

# 커밋
git commit -m "v8.2: 데이터 레이크 & 분산 병렬 처리"

# 푸시
git push origin main
```

### 새 브랜치 생성

```bash
# 새 브랜치
git checkout -b feature/v9-4-quantum-internet

# 작업 수행

# 푸시
git push origin feature/v9-4-quantum-internet
```

---

## **Step 8: 문제 해결**

### Termux multiprocessing 오류

```
오류: RuntimeError: context has already been set
해결: if __name__ == "__main__" 블록 확인
```

### ModuleNotFoundError

```bash
# 경로 확인
python3 -c "import sys; print(sys.path)"

# 또는 PYTHONPATH 설정
export PYTHONPATH=/data/data/com.termux/files/home/python-gogs:$PYTHONPATH
```

### 권한 오류

```bash
# 파일 권한 확인
ls -la *.py

# 실행 권한 추가
chmod +x *.py
```

### 메모리 부족

```bash
# 단일 테스트만 실행
python3 test_v8_2_data_lake.py TestDataPartitioner.test_01_range_partitioning -v

# 또는 작은 데이터로 테스트
DATA_SIZE=1000 python3 university_v8_2_DISTRIBUTED_DATA_LAKE.py
```

---

## **Step 9: CI/CD 통합 (선택사항)**

### GitHub Actions 예제

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Run tests
      run: |
        python -m pytest test_*.py -v
```

---

## **Step 10: 배포 체크리스트**

### 코드 품질

- [ ] 모든 테스트 통과 (60/60)
- [ ] 코드 리뷰 완료
- [ ] 문서 최신 상태
- [ ] 보안 취약점 스캔
- [ ] 성능 벤치마크 확인

### 환경 준비

- [ ] Python 3.10+ 설치
- [ ] 가상 환경 설정
- [ ] 의존성 설치
- [ ] Git 구성

### 배포

- [ ] 모든 커밋 푸시 완료
- [ ] 태그 생성 (v8.2, v8.3, v8.4, v9.3)
- [ ] 릴리스 노트 작성
- [ ] 문서 배포

### 모니터링

- [ ] 로그 확인
- [ ] 메트릭 수집 시작
- [ ] 알람 설정
- [ ] 정기 검토 일정

---

## **Step 11: 유지보수**

### 정기 점검

```bash
# 주단위
git log --oneline | head -20

# 월단위
python3 -m pytest test_*.py -v --tb=short
```

### 업데이트 확인

```bash
# 새로운 Python 버전
python3 --version

# 보안 패치
pip list --outdated
```

### 백업

```bash
# 로컬 백업
tar -czf gogs_backup_$(date +%Y%m%d).tar.gz gogs_python/

# 원격 백업 (Git)
git push origin main
```

---

## **Step 12: 문서 관리**

### 문서 구조

```
python-gogs/
├─ README.md (프로젝트 개요)
├─ ARCHITECTURE.md (시스템 설계)
├─ IMPLEMENTATION_GUIDE.md (구현 가이드)
├─ API_REFERENCE.md (API 문서)
├─ LESSONS_LEARNED.md (교훈)
└─ DEPLOYMENT.md (배포 가이드 - 이 파일)
```

### 문서 업데이트

```bash
# 문서 편집
vim ARCHITECTURE.md

# 커밋
git add ARCHITECTURE.md
git commit -m "docs: ARCHITECTURE.md 업데이트"
git push origin main
```

---

## **Step 13: 성능 튜닝**

### Multiprocessing 워커 수 조정

```python
# 현재: CPU 코어 수
num_workers = multiprocessing.cpu_count()

# 또는 수동 조정
num_workers = 4  # 고정 값
```

### 청크 크기 최적화

```python
# 큰 청크: 오버헤드 감소, 병렬도 감소
chunk_size = len(data) // (num_workers * 2)

# 작은 청크: 오버헤드 증가, 병렬도 증가
chunk_size = len(data) // (num_workers * 10)
```

### 메모리 프로파일링

```bash
# 메모리 사용량 추적
python3 -m memory_profiler university_v8_2_DISTRIBUTED_DATA_LAKE.py

# (memory_profiler 설치 필요)
pip install memory-profiler
```

---

## **단계별 체크리스트**

```
[ ] Step 1: 저장소 클론
[ ] Step 2: 가상 환경 설정
[ ] Step 3: 의존성 설치
[ ] Step 4: 테스트 실행 (모두 PASS)
[ ] Step 5: 메인 프로그램 실행
[ ] Step 6: 성능 벤치마킹
[ ] Step 7: Git 작업 흐름 확인
[ ] Step 8: 문제 해결 (필요시)
[ ] Step 9: CI/CD 통합 (선택)
[ ] Step 10: 배포 체크리스트 확인
[ ] Step 11: 유지보수 계획 수립
[ ] Step 12: 문서 관리 설정
[ ] Step 13: 성능 튜닝 완료
```

---

## **지원 및 문제 해결**

### 자주 묻는 질문

**Q: Termux에서 multiprocessing이 작동하지 않습니다.**
A: `if __name__ == "__main__":` 블록을 추가하세요.

**Q: 테스트가 느립니다.**
A: 단일 테스트만 실행하거나 작은 데이터셋으로 테스트하세요.

**Q: 메모리 부족 오류가 발생합니다.**
A: 청크 크기를 줄이거나 워커 수를 감소시키세요.

---

## **추가 리소스**

- [Python 공식 문서](https://docs.python.org/3/)
- [Multiprocessing 가이드](https://docs.python.org/3/library/multiprocessing.html)
- [Git 공식 문서](https://git-scm.com/doc)
- [원격 저장소](https://gogs.dclub.kr/kim/gogs_python.git)

---

**문서 버전**: 1.0
**마지막 업데이트**: 2026년 02월 25일
