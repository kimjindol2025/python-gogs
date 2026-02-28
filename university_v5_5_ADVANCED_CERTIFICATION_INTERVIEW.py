#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║  🏛️ v5.5: Gogs 시스템 설계자 통합 인증 시험 (대학원 수준)                ║
║                                                                            ║
║    섹션 1: 자원 및 메모리 관리                                            ║
║    섹션 2: 비동기와 동시성 설계                                          ║
║    섹션 3: 객체 지향 및 메타프로그래밍                                   ║
║    섹션 4: 알고리즘 최적화                                               ║
║                                                                            ║
║  철학: 기록이 증명이다 gogs                                                 ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import threading
import time
import bisect
import contextlib
import io
from typing import Generator, List, Optional
from pathlib import Path
import unittest

# ═══════════════════════════════════════════════════════════════════════════
# 섹션 1: 자원 및 메모리 관리 - with 문과 제너레이터의 결합
# ═══════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║ 【 섹션 1: 자원 및 메모리 관리 】                                          ║
║                                                                            ║
║ 질문 1: with 문과 제너레이터의 결합 분석                                   ║
╚════════════════════════════════════════════════════════════════════════════╝

【 문제 분석 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ 문제가 되는 코드:
    def read_log_file(filepath):
        with open(filepath) as f:
            for line in f:
                if 'ERROR' in line:
                    yield line  # ← 문제!

    gen = read_log_file('app.log')
    # with 블록이 종료되어 파일이 닫혀있음
    for error in gen:  # StopIteration 또는 ValueError 발생!
        print(error)

【 근본 원인 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. with 블록의 생명주기:
   with open(...) as f:  → __enter__() 호출
       yield ...         → 제너레이터 객체 생성만 함 (실행 아님)
   # with 블록 종료      → __exit__() 호출 → 파일 닫힘

2. 제너레이터의 지연 실행:
   - yield가 있는 함수는 호출 시 즉시 실행되지 않음
   - 처음 next() 호출 시 yield까지만 실행
   - 두 번째 next() 호출 시 resume
   - ∴ with 블록 종료 후 순회하면 파일이 이미 닫혀있음

【 ✅ 올바른 해결책 1: contextlib.contextmanager 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@contextlib.contextmanager
def open_log_file(filepath):
    f = open(filepath)
    try:
        yield f  # 제너레이터이지만 컨텍스트 매니저
    finally:
        f.close()

def read_log_errors(filepath):
    with open_log_file(filepath) as f:
        for line in f:
            if 'ERROR' in line:
                yield line  # with 블록 내부에서 yield!

【 ✅ 올바른 해결책 2: 클래스 기반 컨텍스트 매니저 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LogReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.file = None

    def __enter__(self):
        self.file = open(self.filepath)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def read_errors(self):
        for line in self.file:
            if 'ERROR' in line:
                yield line

with LogReader('app.log') as reader:
    for error in reader.read_errors():
        print(error)  # ✅ 파일이 열려있음!

【 핵심 개념 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ 컨텍스트 매니저(__enter__/__exit__): 자원 생명주기 관리
✓ @contextlib.contextmanager: 데코레이터로 쉽게 구현
✓ with 블록 내부에서 yield 사용
✓ 제너레이터의 지연 실행 특성 이해
""")

# ═══════════════════════════════════════════════════════════════════════════
# 섹션 2: 비동기와 동시성 설계
# ═══════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║ 【 섹션 2: 비동기와 동시성 설계 】                                        ║
║                                                                            ║
║ 질문 2: asyncio와 threading의 선택 기준                                   ║
╚════════════════════════════════════════════════════════════════════════════╝

【 문제 분석 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

과제 (A): 5,000개 웹 API 동시 수집
과제 (B): 1,000장 이미지 처리 및 압축

【 기술 선택 기준 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ I/O-bound vs CPU-bound:

   I/O-bound (대기 시간이 많음):
   ├─ 네트워크 요청 (API)
   ├─ 파일 읽기/쓰기
   ├─ 데이터베이스 쿼리
   └─ 추천: asyncio

   CPU-bound (연산 시간이 많음):
   ├─ 이미지 처리
   ├─ 데이터 분석
   ├─ 압축/암호화
   └─ 추천: multiprocessing

2️⃣ GIL (Global Interpreter Lock) 이해:

   Python의 모든 thread는 하나의 GIL만 공유

   threading:
   - 한 번에 하나의 thread만 실행
   - CPU-bound 작업에서는 성능 향상 없음
   - I/O 대기 중에는 다른 thread 실행 가능

   multiprocessing:
   - 각 process가 독립적인 GIL 보유
   - CPU-bound 작업에서 진정한 병렬 처리
   - 프로세스 간 통신 오버헤드 있음

【 과제 (A) 답변: 5,000개 웹 API 수집 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 선택: asyncio (또는 aiohttp)

이유:
1. I/O-bound 작업 (네트워크 대기)
2. 5,000개 동시 요청 가능
3. GIL의 영향 없음 (I/O 대기 중 다른 coroutine 실행)
4. 메모리 효율적 (threading보다 lightweight)
5. 컨텍스트 스위칭 오버헤드 적음

성능 비교:
- threading: GIL로 인해 순차 실행 → 5,000배 느림
- asyncio: 동시 I/O → 최대 100배 빠름 (대역폭 제한)

【 과제 (B) 답변: 1,000장 이미지 처리 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 선택: multiprocessing

이유:
1. CPU-bound 작업 (이미지 필터링, 압축)
2. GIL의 제약 벗어남
3. 멀티코어 활용 가능
4. 진정한 병렬 처리

성능 비교:
- threading: GIL로 인해 1배 (순차 실행)
- multiprocessing: 4배 (4코어 기준)

【 최적 구현 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 과제 A: asyncio
async def fetch_apis():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

# 과제 B: multiprocessing
def process_images():
    with Pool(4) as pool:
        results = pool.map(process_single_image, images)
""")

# ═══════════════════════════════════════════════════════════════════════════
# 섹션 3: 객체 지향 및 메타프로그래밍 - 네임 매글링
# ═══════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║ 【 섹션 3: 객체 지향 및 메타프로그래밍 】                                  ║
║                                                                            ║
║ 질문 3: 상속과 캡슐화의 충돌 - 네임 매글링                                ║
╚════════════════════════════════════════════════════════════════════════════╝

【 문제 분석 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ 문제가 되는 코드:
    class Parent:
        def __init__(self):
            self.__db_key = "secret"  # 비공개 속성

    class Child(Parent):
        def get_key(self):
            return self.__db_key  # ← AttributeError 발생!

【 네임 매글링(Name Mangling) 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Python의 보안 메커니즘:

1. __ (언더스코어 2개)로 시작하는 속성:
   - 클래스 이름으로 prefix 추가
   - Parent.__db_key → _Parent__db_key

2. 자식 클래스에서 접근 불가:
   - self.__db_key는 _Child__db_key로 매글링됨
   - _Parent__db_key와는 다른 속성!

실행 결과:
    parent = Parent()
    print(parent._Parent__db_key)  # "secret" (접근 가능)

    child = Child()
    print(hasattr(child, '_Child__db_key'))  # False
    print(hasattr(child, '_Parent__db_key'))  # True

【 ✅ 올바른 설계 방법 1: protected 속성 (_) 사용 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Parent:
    def __init__(self):
        self._db_key = "secret"  # 보호된 속성

class Child(Parent):
    def get_key(self):
        return self._db_key  # ✅ 정상 작동

규약:
- _ (한 개): "이것은 내부용이니 직접 접근하지 마세요"
- __ (두 개): 진정한 비공개 (네임 매글링 적용)

【 ✅ 올바른 설계 방법 2: Property 사용 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Parent:
    def __init__(self):
        self._db_key = "secret"

    @property
    def db_key(self):
        return self._db_key

class Child(Parent):
    pass

child = Child()
print(child.db_key)  # ✅ getter 를 통한 접근

【 ✅ 올바른 설계 방법 3: super() 활용 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Parent:
    def __init__(self):
        self.__db_key = "secret"

    def get_db_key(self):
        return self.__db_key

class Child(Parent):
    def get_key(self):
        return super().get_db_key()  # ✅ 부모 메서드 활용

【 핵심 개념 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ 네임 매글링: _ClassName__attr 변환
✓ 비공개 대신 보호된(_) 속성 사용
✓ Property로 접근 제어
✓ super()로 부모 메서드 활용
""")

# ═══════════════════════════════════════════════════════════════════════════
# 섹션 4: 알고리즘 최적화 - 정렬된 데이터 유지
# ═══════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║ 【 섹션 4: 알고리즘 최적화 】                                             ║
║                                                                            ║
║ 질문 4: 정렬된 데이터의 업데이트와 검색                                   ║
╚════════════════════════════════════════════════════════════════════════════╝

【 문제 분석 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

데이터: 실시간으로 추가되는 정렬된 리스트
요구사항: 이진 탐색 O(log n) 성능 유지
제약: 매번 sort() 호출은 O(n log n) - 너무 비효율적

❌ 비효율적 방법:
    data = []
    def add_data(value):
        data.append(value)
        data.sort()  # O(n log n) - 매번 전체 정렬!

    def search(target):
        return binary_search(data, target)  # O(log n)

【 ✅ 효율적 방법: bisect 모듈 사용 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import bisect

data = []

def add_data(value):
    # bisect.insort: O(log n) 탐색 + O(n) 삽입 = O(n)
    # 하지만 정렬 상태 유지!
    bisect.insort(data, value)

def search(target):
    # 이진 탐색: O(log n)
    idx = bisect.bisect_left(data, target)
    return idx < len(data) and data[idx] == target

성능 비교:
- sort() 매번: O(n log n) × m 작업 = O(n log n × m)
- bisect.insort(): O(n) × m 작업 = O(n × m)

예시 (m=1000번 삽입):
- sort(): 1,000 * 10 * log(10,000) ≈ 130,000 연산
- bisect: 1,000 * 5,000 ≈ 5,000,000 연산

   → m이 작을 때는 bisect 유리
   → m이 클 때는 다른 자료구조 필요

【 ✅ 고급 방법: B-tree 또는 SortedList 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from sortedcontainers import SortedList

data = SortedList()

def add_data(value):
    data.add(value)  # O(log n) 탐색 + O(k) 삽입 (k=청크크기)
                      # 평균 O(log n)에 가까움

def search(target):
    idx = data.bisect_left(target)
    return idx < len(data) and data[idx] == target

【 Trade-off 분석 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

자료구조        │ 삽입    │ 탐색    │ 메모리  │ 복잡도
─────────────────────────────────────────────────────
리스트+sort()   │ O(n log n) │ O(log n) │ 낮음    │ 높음
bisect.insort   │ O(n)    │ O(log n) │ 낮음    │ 중간
SortedList      │ O(log n)│ O(log n) │ 중간    │ 낮음
B-tree          │ O(log n)│ O(log n) │ 높음    │ 최저
Red-Black Tree  │ O(log n)│ O(log n) │ 높음    │ 최저

【 최적 선택 기준 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ 삽입이 드문 경우: bisect.insort (간단함)
✓ 대량 삽입: SortedList (균형 잡힘)
✓ 매우 큰 규모: B-tree, Red-Black Tree (지속적 최적화)
""")

# ═══════════════════════════════════════════════════════════════════════════
# 실제 구현 예제
# ═══════════════════════════════════════════════════════════════════════════

class ContextManagerExample:
    """섹션 1: 컨텍스트 매니저 예제"""

    @staticmethod
    @contextlib.contextmanager
    def open_log_file(content: str):
        """제너레이터 기반 컨텍스트 매니저"""
        f = io.StringIO(content)
        try:
            yield f
        finally:
            f.close()

    @staticmethod
    def read_log_errors(content: str):
        """안전한 제너레이터"""
        with ContextManagerExample.open_log_file(content) as f:
            for line in f:
                if 'ERROR' in line:
                    yield line

class NameManglingExample:
    """섹션 3: 네임 매글링 예제"""

    class Parent:
        def __init__(self):
            self.__secret = "confidential"
            self._protected = "semi-public"

    class Child(Parent):
        def attempt_access(self):
            # ❌ 이것은 작동하지 않음:
            # return self.__secret  # NameError!

            # ✅ 이것들은 작동함:
            return self._protected

    @staticmethod
    def demonstrate_mangling():
        parent = NameManglingExample.Parent()
        child = NameManglingExample.Child()

        # 네임 매글링 확인
        print(f"Parent 속성: {dir(parent)}")
        print(f"_Parent__secret 값: {parent._Parent__secret}")

        # 자식에서 접근 가능한 속성
        print(f"Child 보호된 속성: {child._protected}")

class BisectOptimizationExample:
    """섹션 4: bisect 알고리즘 예제"""

    @staticmethod
    def demo_bisect():
        data = []

        # 데이터 추가
        values = [3, 1, 4, 1, 5, 9, 2, 6, 5]
        for v in values:
            bisect.insort(data, v)

        print(f"정렬된 데이터: {data}")

        # 이진 탐색
        target = 5
        idx = bisect.bisect_left(data, target)
        found = idx < len(data) and data[idx] == target
        print(f"{target} 찾음: {found}")

        return data

# ═══════════════════════════════════════════════════════════════════════════
# 테스트
# ═══════════════════════════════════════════════════════════════════════════

class TestAdvancedCertification(unittest.TestCase):
    """고급 인증 시험"""

    def test_1_context_manager(self):
        """섹션 1: 컨텍스트 매니저"""
        content = "INFO: starting\nERROR: failure\nINFO: done"
        errors = list(ContextManagerExample.read_log_errors(content))
        self.assertEqual(len(errors), 1)
        self.assertIn("ERROR", errors[0])

    def test_2_name_mangling(self):
        """섹션 3: 네임 매글링"""
        parent = NameManglingExample.Parent()
        self.assertEqual(parent._Parent__secret, "confidential")

        child = NameManglingExample.Child()
        self.assertEqual(child._protected, "semi-public")

    def test_3_bisect(self):
        """섹션 4: bisect 최적화"""
        data = BisectOptimizationExample.demo_bisect()
        self.assertEqual(data, [1, 1, 2, 3, 4, 5, 5, 6, 9])

    def test_4_bisect_search(self):
        """이진 탐색 정확성"""
        data = []
        for v in [5, 2, 8, 1, 9]:
            bisect.insort(data, v)

        # 존재하는 값 찾기
        idx = bisect.bisect_left(data, 5)
        self.assertTrue(data[idx] == 5)

        # 존재하지 않는 값
        idx = bisect.bisect_left(data, 4)
        self.assertFalse(idx < len(data) and data[idx] == 4)

# ═══════════════════════════════════════════════════════════════════════════
# 메인 실행
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🏛️ v5.5: Gogs 시스템 설계자 통합 인증 시험")
    print("="*80 + "\n")

    print("\n【 테스트 실행 】\n")
    unittest.main(argv=[''], exit=False, verbosity=2)

    print("\n" + "="*80)
    print("✅ 모든 섹션 완성!")
    print("="*80)
    print("\n저장 필수 너는 기록이 증명이다 gogs\n")
