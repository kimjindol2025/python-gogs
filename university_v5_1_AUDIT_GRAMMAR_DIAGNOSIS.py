#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║  🔍 v5.1-Audit: 파이썬 통합 문법 정밀 진단 & 교정                       ║
║                                                                            ║
║    클래스(v2.2), 데코레이터(v3.1), 제너레이터(v3.2),                    ║
║    비동기(v4.1)가 얽혀 있을 때의 논리적 허점 찾아내기                    ║
║                                                                            ║
║  철학: 기록이 증명이다 gogs                                                 ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import time
import functools
from typing import AsyncGenerator, Generator, List
from datetime import datetime
import unittest

# ═══════════════════════════════════════════════════════════════════════════
# PART 1: 오류 분석 문서화
# ═══════════════════════════════════════════════════════════════════════════

ERROR_ANALYSIS = """
【 3가지 핵심 오류 분석 】

【 오류 1: 데코레이터 + 비동기 결합 오류 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ 원본 코드:
    def gogs_timer(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)  # ← 치명적 오류!
            print(f"소요 시간: {time.time() - start:.4f}s")
            return result
        return wrapper

    @gogs_timer
    async def analyze_node(self, node_id):
        await asyncio.sleep(0.5)

📌 문제점:
   1. `func(*args, **kwargs)`는 코루틴 객체만 생성, 실행 안 됨
   2. 데코레이터의 wrapper가 동기 함수이므로 await 불가
   3. 결과: 비동기 함수가 실행되지 않고 코루틴 객체만 반환

🔧 해결책:
   ✓ wrapper를 async def로 선언
   ✓ await func(*args, **kwargs) 사용
   ✓ @functools.wraps로 메타데이터 보존

등급: ⭐⭐⭐⭐⭐ (상급 - 비동기 데코레이터 이해 필수)

【 오류 2: 제너레이터의 소모성(Exhaustion) 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ 원본 코드:
    nodes = data_generator(5)  # 제너레이터 객체 생성
    system = GogsDataSystem(nodes)
    tasks = [system.analyze_node(n) for n in nodes]  # ← 제너레이터 소모!
    results = await asyncio.gather(*tasks)

📌 문제점:
   1. 제너레이터는 한 번 순회하면 완전히 비워짐
   2. 리스트 컴프리헨션에서 nodes를 순회
   3. 그 다음에는 nodes가 비어있음 (다시 순회 불가)
   4. tasks 리스트가 비어있거나 불완전함

실제 흐름:
   순회 1: [system.analyze_node(0), .analyze_node(1), ..., .analyze_node(4)]
   순회 2: [] (제너레이터 소진됨)

🔧 해결책 (3가지):
   ✓ list(data_generator(5)) - 미리 리스트로 변환
   ✓ 제너레이터를 여러 번 호출: data_generator(5)를 반복
   ✓ tee() 사용: itertools.tee(nodes, 2)

등급: ⭐⭐⭐⭐ (중급 - 제너레이터 특성 이해)

【 오류 3: 비동기 환경에서 time.time() 부정확성 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ 원본 코드:
    start = time.time()
    result = func(*args, **kwargs)  # await 없으므로 즉시 반환
    print(f"소요 시간: {time.time() - start:.4f}s")

📌 문제점:
   1. time.time()은 wall-clock time (벽시계 시간) 측정
   2. 비동기 함수가 실제로 await되지 않으면 거의 즉시 반환
   3. 측정되는 시간 ≈ 0.0001초 (컨텍스트 스위칭 오버헤드)
   4. 실제 함수 실행 시간 미측정

비동기 환경 타이밍 문제:
   Task A: ▁▂▃▂▁▂▃ (중단됨)
   Task B:  ▁▂▃▂▁▂ (중단됨)
   Task C:   ▁▂▃▂▁▂

   time.time()은 전체 wall-clock 시간만 측정
   개별 작업의 실제 CPU 시간은 측정 불가

🔧 해결책:
   ✓ asyncio.wait_for(func(), timeout=...)로 감싸기
   ✓ 별도의 event loop 시간 계산
   ✓ 또는 함수 내부에서 시간 측정

등급: ⭐⭐⭐ (초급~중급 - 비동기 타이밍 이해)
"""

# ═══════════════════════════════════════════════════════════════════════════
# PART 2: 교정된 코드 - 올바른 구현
# ═══════════════════════════════════════════════════════════════════════════

# 【 교정 1: 비동기 데코레이터 】
def async_timer(func):
    """
    【 교정됨 】
    비동기 함수 전용 데코레이터
    - wrapper를 async def로 선언
    - await func() 사용
    - @functools.wraps로 메타데이터 보존
    """
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.time()
        start_time = datetime.now().isoformat()

        try:
            result = await func(*args, **kwargs)  # ← 핵심: await 사용!
            elapsed = time.time() - start

            print(
                f"[{start_time}] ⏱️  {func.__name__} 완료: {elapsed*1000:.2f}ms"
            )
            return result

        except Exception as e:
            elapsed = time.time() - start
            print(
                f"[{start_time}] ❌ {func.__name__} 오류: {elapsed*1000:.2f}ms - {e}"
            )
            raise

    return async_wrapper

# 【 교정 2: 비동기 제너레이터 】
async def async_data_generator(limit: int) -> AsyncGenerator[int, None]:
    """
    【 교정됨 】
    비동기 제너레이터
    - 제너레이터의 소모성 해결
    - 필요할 때마다 새로 생성
    """
    for i in range(limit):
        await asyncio.sleep(0.01)  # 비동기 수집 시뮬레이션
        yield i

# 【 교정 3: 동기 제너레이터 (필요시) 】
def data_generator(limit: int) -> Generator[int, None, None]:
    """
    【 교정됨 】
    동기 제너레이터
    - yield 이후에 자동으로 다음 반복 준비
    - yield는 return과 다르게 함수 상태를 유지
    """
    for i in range(limit):
        # 【 핵심 개념 】
        # yield: 값을 반환하되 함수의 실행 상태를 보존
        # 다음 next() 호출 시 yield 직후부터 재개
        yield i

# ═══════════════════════════════════════════════════════════════════════════
# PART 3: 교정된 시스템
# ═══════════════════════════════════════════════════════════════════════════

class GogsDataSystem:
    """
    【 교정된 버전 】
    실험 데이터 스트리밍 시스템
    """

    def __init__(self):
        self.processed_count = 0
        self.processed_nodes: List[str] = []

    @async_timer  # ← 이제 정상 작동!
    async def analyze_node(self, node_id: int) -> str:
        """
        【 v4.1 비동기 + v3.1 데코레이터 】
        노드 분석 (비동기)

        Args:
            node_id: 노드 ID

        Returns:
            분석 결과
        """
        await asyncio.sleep(0.5)  # 분석 시뮬레이션
        self.processed_count += 1
        result = f"Node-{node_id} Complete"
        self.processed_nodes.append(result)
        return result

# ═══════════════════════════════════════════════════════════════════════════
# PART 4: 올바른 실행 예제
# ═══════════════════════════════════════════════════════════════════════════

async def demo_correct_implementation():
    """
    【 올바른 구현 】
    """
    print("\n【 올바른 구현: 비동기 데코레이터 + 제너레이터 】\n")

    system = GogsDataSystem()

    # 【 방법 1: 리스트로 변환 】
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("방법 1: 동기 제너레이터를 리스트로 변환")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    nodes = list(data_generator(3))  # ✅ 리스트로 변환!
    print(f"변환된 노드: {nodes}")

    tasks = [system.analyze_node(n) for n in nodes]  # ✅ 정상 순회!
    results = await asyncio.gather(*tasks)

    print(f"\n결과: {results}")
    print(f"처리된 노드 수: {system.processed_count}")

    # 【 방법 2: 비동기 제너레이터 】
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("방법 2: 비동기 제너레이터")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    system2 = GogsDataSystem()
    nodes_async = async_data_generator(3)

    # 비동기 제너레이터를 리스트로 변환
    async def async_list(async_gen):
        result = []
        async for item in async_gen:
            result.append(item)
        return result

    nodes_list = await async_list(nodes_async)
    print(f"비동기 제너레이터 결과: {nodes_list}")

    tasks2 = [system2.analyze_node(n) for n in nodes_list]
    results2 = await asyncio.gather(*tasks2)

    print(f"\n결과: {results2}")
    print(f"처리된 노드 수: {system2.processed_count}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 5: 비교 분석
# ═══════════════════════════════════════════════════════════════════════════

class AnalysisComparison:
    """
    오류 vs 교정 비교 분석
    """

    @staticmethod
    def print_comparison():
        """비교표 출력"""
        print("\n" + "="*80)
        print("【 오류 vs 교정 비교 분석 】")
        print("="*80)

        comparison = """
【 오류 1: 데코레이터 + 비동기 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ 오류 코드:
   def wrapper(*args, **kwargs):
       result = func(*args, **kwargs)  # 코루틴만 반환, 실행 안 됨!

✅ 교정 코드:
   async def async_wrapper(*args, **kwargs):
       result = await func(*args, **kwargs)  # await로 실행!

결과:
   ❌ 오류: RuntimeWarning: coroutine was never awaited
   ✅ 교정: 정상 실행, 시간 측정 가능

【 오류 2: 제너레이터 소모성 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ 오류 코드:
   nodes = data_generator(5)
   tasks = [system.analyze_node(n) for n in nodes]  # 제너레이터 소모!

✅ 교정 코드:
   nodes = list(data_generator(5))  # 리스트로 변환
   tasks = [system.analyze_node(n) for n in nodes]  # 정상 순회

결과:
   ❌ 오류: tasks = [] (비어있음)
   ✅ 교정: tasks = [Task, Task, Task, ...] (정상)

【 오류 3: time.time() 타이밍 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ 오류 코드:
   start = time.time()
   result = func(*args, **kwargs)  # await 없으면 즉시 반환
   elapsed = time.time() - start  # 거의 0.0000초

✅ 교정 코드:
   start = time.time()
   result = await func(*args, **kwargs)  # await로 실제 실행
   elapsed = time.time() - start  # 정확한 시간 측정

결과:
   ❌ 오류: 소요 시간: 0.0001s (부정확)
   ✅ 교정: 소요 시간: 500.1234ms (정확)
"""
        print(comparison)

# ═══════════════════════════════════════════════════════════════════════════
# PART 6: 테스트
# ═══════════════════════════════════════════════════════════════════════════

class TestGrammarCorrection(unittest.TestCase):
    """문법 교정 테스트"""

    def test_1_async_decorator(self):
        """테스트 1: 비동기 데코레이터"""
        async def test():
            system = GogsDataSystem()
            result = await system.analyze_node(1)
            self.assertIn("Complete", result)

        asyncio.run(test())

    def test_2_generator_consumption(self):
        """테스트 2: 제너레이터 소모성"""
        # ❌ 오류: 제너레이터는 한 번 소모
        gen1 = data_generator(3)
        list1 = list(gen1)
        list2 = list(gen1)  # 비어있음

        self.assertEqual(len(list1), 3)
        self.assertEqual(len(list2), 0)  # 증명됨

        # ✅ 교정: 새로 생성
        list3 = list(data_generator(3))
        list4 = list(data_generator(3))

        self.assertEqual(len(list3), 3)
        self.assertEqual(len(list4), 3)  # 정상

    def test_3_list_conversion(self):
        """테스트 3: 리스트 변환"""
        nodes = list(data_generator(5))
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes, [0, 1, 2, 3, 4])

    def test_4_async_list_conversion(self):
        """테스트 4: 비동기 리스트 변환"""
        async def test():
            async def async_list(async_gen):
                result = []
                async for item in async_gen:
                    result.append(item)
                return result

            result = await async_list(async_data_generator(3))
            self.assertEqual(len(result), 3)

        asyncio.run(test())

    def test_5_integration(self):
        """테스트 5: 완전 통합"""
        async def test():
            system = GogsDataSystem()
            nodes = list(data_generator(3))
            tasks = [system.analyze_node(n) for n in nodes]
            results = await asyncio.gather(*tasks)

            self.assertEqual(len(results), 3)
            self.assertEqual(system.processed_count, 3)

        asyncio.run(test())

# ═══════════════════════════════════════════════════════════════════════════
# 메인 실행
# ═══════════════════════════════════════════════════════════════════════════

async def main():
    """메인 실행"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*15 + "🔍 v5.1-Audit: 파이썬 통합 문법 정밀 진단 & 교정" + " "*14 + "║")
    print("╚" + "="*78 + "╝")

    # 오류 분석 출력
    print(ERROR_ANALYSIS)

    # 비교 분석 출력
    AnalysisComparison.print_comparison()

    # 올바른 구현 실행
    await demo_correct_implementation()

    print("\n" + "="*80)
    print("✅ 문법 진단 및 교정 완료!")
    print("="*80)
    print("\n저장 필수 너는 기록이 증명이다 gogs\n")

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*10 + "v5.1-Audit: 파이썬 통합 문법 정밀 진단 & 교정 보고서" + " "*12 + "║")
    print("║" + " "*20 + "클래스, 데코레이터, 제너레이터, 비동기" + " "*18 + "║")
    print("╚" + "="*78 + "╝")

    # 단위 테스트
    print("\n【 단위 테스트 실행 】\n")
    unittest.main(argv=[''], exit=False, verbosity=2)

    # 완전 분석 및 교정
    print("\n【 완전 분석 및 교정 】")
    asyncio.run(main())
