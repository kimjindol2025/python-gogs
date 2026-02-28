"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║             🏛️  Python 대학교 2학년 (v4.1 Sophomore)                          ║
║                                                                                ║
║     [v4.1: 비동기 프로그래밍 (Asyncio) — 멈추지 않는 시스템]                 ║
║                                                                                ║
║                    ★ 기다림을 효율로 바꾸는 기술 ★                           ║
║                                                                                ║
║  지금까지의 코드는 한 작업이 끝날 때까지 다음 코드가 기다리는                  ║
║  동기(Synchronous) 방식이었습니다.                                            ║
║                                                                                ║
║  이제 데이터가 오기를 기다리는 동안 다른 일을 처리하는                        ║
║  비동기(Asynchronous) 설계를 배웁니다.                                        ║
║                                                                                ║
║  철학: "기록이 증명이다 — gogs"                                               ║
║  성능의 비약적 증명: 동기 대비 N배 빠름!                                      ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import time
from typing import List, Coroutine
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════════
# 📚 Part 1: 비동기 프로그래밍의 철학
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║              📚 Part 1: 비동기 프로그래밍의 철학                               ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

PHILOSOPHY = """
🔷 동기(Synchronous) vs 비동기(Asynchronous)

【 동기 (기다리는 방식) 】
작업1: 데이터 수신 (3초)    [████ 3초 기다림]
작업2: 데이터 수신 (2초)                    [███ 2초 기다림]
작업3: 데이터 수신 (1초)                              [█ 1초 기다림]
─────────────────────────────────────────
총 시간: 3 + 2 + 1 = 6초

【 비동기 (효율적인 방식) 】
작업1: 데이터 수신 (3초)    [████─────────]
작업2: 데이터 수신 (2초)    [───███──────]
작업3: 데이터 수신 (1초)    [───────█────]
─────────────────────────────────────────
총 시간: max(3, 2, 1) = 3초 ← 2배 빠름!

🔷 핵심 개념: 이벤트 루프 (Event Loop)

이벤트 루프는 지휘자와 같습니다.
- "작업A, 데이터 기다려?"
  → "네, 기다리고 있어요"
  → "그럼 그동안 작업B 해!"
- "작업B, 계산 끝났어?"
  → "네, 끝났어요!"
  → "그럼 작업C 해!"
- "작업A, 데이터 왔어?"
  → "네, 방금 왔어요!"
  → "그럼 처리해!"

🔷 왜 사용하나? (성능의 비약적 증명)

1. I/O 바운드 작업 최적화
   - 웹사이트에서 데이터 긁기 (I/O 대기 시간 > CPU 시간)
   - 데이터베이스 쿼리 (네트워크 왕복 시간이 주요 소비)
   - 파일 읽기/쓰기 (디스크 I/O 시간이 주요 소비)

2. 싱글 스레드의 마법
   - 멀티스레딩의 복잡성 없음 (동시성 버그 감소)
   - GIL(Global Interpreter Lock) 문제 없음
   - 데이터 경합 문제 없음

3. 수천 개 동시 연결
   - 웹 서버에서 수만 명 사용자 동시 처리
   - 채팅 애플리케이션에서 모든 연결 유지
   - 실시간 업데이트 시스템 구축

🔷 키워드의 의미

async def: "이 함수는 비동기로 작동하며, 실행 중에 잠시 멈출 수 있음"
await:   "이 작업이 끝날 때까지 기다릴 건데, 그동안 CPU는 다른 일을 해!"
"""

print(PHILOSOPHY)


# ═══════════════════════════════════════════════════════════════════════════════
# 🔷 Part 2: async/await의 기초
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                 🔷 Part 2: async/await의 기초                                 ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 기본 형태 】")

async def simple_async():
    """간단한 비동기 함수"""
    print(f"  [시작] {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
    await asyncio.sleep(0.5)
    print(f"  [종료] {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
    return "완료"

# 실행
print("  asyncio.run() 사용:")
result = asyncio.run(simple_async())
print(f"  결과: {result}")


# ═══════════════════════════════════════════════════════════════════════════════
# ⚡ Part 3: 동기 vs 비동기 비교
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║               ⚡ Part 3: 동기 vs 비동기 비교 (성능 측정!)                     ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 시나리오: 3개의 데이터 수집 (각각 2초, 1초, 3초) 】")

# 동기 방식
print("\n동기 방식 (Synchronous):")

def sync_fetch(node_id, delay):
    """동기 데이터 수집"""
    print(f"  📡 NODE-{node_id} 시작 ({delay}초)")
    time.sleep(delay)
    print(f"  ✅ NODE-{node_id} 완료")
    return f"Data-{node_id}"

start = time.time()
print("  [동기 시작]")
sync_fetch("A", 2)
sync_fetch("B", 1)
sync_fetch("C", 3)
sync_time = time.time() - start
print(f"  [동기 종료] 소요시간: {sync_time:.2f}초")


# 비동기 방식
print("\n비동기 방식 (Asynchronous):")

async def async_fetch(node_id, delay):
    """비동기 데이터 수집"""
    print(f"  📡 NODE-{node_id} 시작 ({delay}초)")
    await asyncio.sleep(delay)
    print(f"  ✅ NODE-{node_id} 완료")
    return f"Data-{node_id}"

async def async_main():
    print("  [비동기 시작]")
    # asyncio.gather로 모두 동시에 실행
    results = await asyncio.gather(
        async_fetch("A", 2),
        async_fetch("B", 1),
        async_fetch("C", 3)
    )
    return results

start = time.time()
results = asyncio.run(async_main())
async_time = time.time() - start
print(f"  [비동기 종료] 소요시간: {async_time:.2f}초")

# 성능 비교
print(f"\n【 성능 비교 】")
print(f"  동기: {sync_time:.2f}초")
print(f"  비동기: {async_time:.2f}초")
print(f"  ⭐ 속도 향상: {sync_time/async_time:.1f}배!")


# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 Part 4: asyncio.gather() — 여러 작업 동시 실행
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║             🎯 Part 4: asyncio.gather() — 여러 작업 동시 실행                ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 asyncio.gather 기본 사용 】")

async def task(name, duration):
    """작업 시뮬레이션"""
    print(f"    [{name}] 시작")
    await asyncio.sleep(duration)
    print(f"    [{name}] 완료")
    return f"{name}-result"

async def gather_demo():
    print("  gather로 3개 작업 동시 실행:")
    results = await asyncio.gather(
        task("작업1", 1),
        task("작업2", 2),
        task("작업3", 0.5)
    )
    print(f"  결과: {results}")

asyncio.run(gather_demo())


# ═══════════════════════════════════════════════════════════════════════════════
# 📋 Part 5: asyncio.create_task() — 개별 작업 관리
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║            📋 Part 5: asyncio.create_task() — 개별 작업 관리                 ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 create_task 기본 사용 】")

async def worker(name):
    """워커 작업"""
    print(f"    [{name}] 시작")
    await asyncio.sleep(1)
    print(f"    [{name}] 완료")

async def create_task_demo():
    print("  create_task로 여러 작업 생성:")

    # 작업 생성
    task1 = asyncio.create_task(worker("워커1"))
    task2 = asyncio.create_task(worker("워커2"))
    task3 = asyncio.create_task(worker("워커3"))

    # 모든 작업 완료 대기
    await asyncio.gather(task1, task2, task3)
    print("  모든 작업 완료!")

asyncio.run(create_task_demo())


# ═══════════════════════════════════════════════════════════════════════════════
# 🏗️  Part 6: 실전 프로젝트 — 연구실 데이터 수집 엔진
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║           🏗️  Part 6: 실전 프로젝트 — 연구실 데이터 수집 엔진              ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 센서 네트워크 데이터 수집 시뮬레이션 】")

class SensorNode:
    """센서 노드"""
    def __init__(self, node_id, response_time):
        self.node_id = node_id
        self.response_time = response_time
        self.data_count = 0

    async def fetch_data(self, batch_id):
        """데이터 수집"""
        await asyncio.sleep(self.response_time)
        self.data_count += 1
        return {
            'node': self.node_id,
            'batch': batch_id,
            'data_points': 1000,
            'quality': 0.95
        }

async def collect_from_network(nodes: List[SensorNode]) -> dict:
    """센서 네트워크에서 데이터 수집"""
    start = time.time()
    print(f"  [수집 시작] {len(nodes)}개 센서에서 동시 수집")

    # 모든 센서에서 동시에 데이터 수집
    results = await asyncio.gather(
        *[node.fetch_data(1) for node in nodes]
    )

    elapsed = time.time() - start
    total_data = sum(r['data_points'] for r in results)

    return {
        'total_data_points': total_data,
        'elapsed_time': elapsed,
        'throughput': total_data / elapsed
    }

# 센서 네트워크 생성
sensors = [
    SensorNode("SENSOR-A", 2.0),
    SensorNode("SENSOR-B", 1.5),
    SensorNode("SENSOR-C", 2.5),
    SensorNode("SENSOR-D", 1.0)
]

# 수집 실행
result = asyncio.run(collect_from_network(sensors))
print(f"\n  수집 결과:")
print(f"    총 데이터포인트: {result['total_data_points']:,}개")
print(f"    소요시간: {result['elapsed_time']:.2f}초")
print(f"    처리량: {result['throughput']:.0f} 포인트/초")


# ═══════════════════════════════════════════════════════════════════════════════
# 🛡️  Part 7: 에러 처리 및 타임아웃
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                🛡️  Part 7: 에러 처리 및 타임아웃                             ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 타임아웃 처리 】")

async def long_operation():
    """오래 걸리는 작업"""
    try:
        print(f"  작업 시작")
        await asyncio.sleep(5)
        print(f"  작업 완료")
    except asyncio.TimeoutError:
        print(f"  ⚠️  타임아웃 발생!")

async def timeout_demo():
    try:
        # 2초의 타임아웃으로 설정
        await asyncio.wait_for(long_operation(), timeout=2.0)
    except asyncio.TimeoutError:
        print(f"  처리됨: 작업이 너무 오래 걸림")

asyncio.run(timeout_demo())


print("\n【 예외 처리 】")

async def failing_task(name):
    """실패할 수 있는 작업"""
    await asyncio.sleep(0.1)
    if name == "작업2":
        raise ValueError(f"{name}이 실패했습니다!")
    return f"{name} 성공"

async def exception_demo():
    print("  예외 처리 데모:")
    tasks = [
        failing_task("작업1"),
        failing_task("작업2"),
        failing_task("작업3")
    ]

    # return_exceptions=True로 예외를 결과로 반환
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print(f"    작업{i}: ❌ {result}")
        else:
            print(f"    작업{i}: ✅ {result}")

asyncio.run(exception_demo())


# ═══════════════════════════════════════════════════════════════════════════════
# ✅ Part 8: 최종 테스트 및 검증
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                   ✅ Part 8: 최종 테스트 및 검증                             ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

test_results = []

# Test 1: 기본 async/await
print("\n【 Test 1: 기본 async/await 】")
try:
    async def test_basic():
        await asyncio.sleep(0.01)
        return "success"

    result = asyncio.run(test_basic())
    assert result == "success", "반환값 오류"
    test_results.append(("Test 1: 기본 async/await", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 1: 기본 async/await", False))
    print(f"  ✗ FAIL: {e}")


# Test 2: asyncio.gather()
print("\n【 Test 2: asyncio.gather() 】")
try:
    async def test_gather():
        async def task(n):
            await asyncio.sleep(0.01)
            return n * 2

        results = await asyncio.gather(task(1), task(2), task(3))
        return results

    results = asyncio.run(test_gather())
    assert results == [2, 4, 6], f"결과 오류: {results}"
    test_results.append(("Test 2: asyncio.gather()", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 2: asyncio.gather()", False))
    print(f"  ✗ FAIL: {e}")


# Test 3: 비동기가 동기보다 빠른가?
print("\n【 Test 3: 비동기 성능 (동기 대비) 】")
try:
    # 동기 방식
    def sync_test():
        start = time.time()
        time.sleep(0.1)
        time.sleep(0.1)
        time.sleep(0.1)
        return time.time() - start

    # 비동기 방식
    async def async_test():
        start = time.time()
        await asyncio.gather(
            asyncio.sleep(0.1),
            asyncio.sleep(0.1),
            asyncio.sleep(0.1)
        )
        return time.time() - start

    sync_time = sync_test()
    async_time = asyncio.run(async_test())

    # 비동기가 동기보다 최소 2배 빨아야 함
    assert async_time < sync_time / 2, f"성능 부족: async={async_time}, sync={sync_time}"
    test_results.append(("Test 3: 비동기 성능", True))
    print(f"  ✓ PASS (동기: {sync_time:.2f}s vs 비동기: {async_time:.2f}s)")
except AssertionError as e:
    test_results.append(("Test 3: 비동기 성능", False))
    print(f"  ✗ FAIL: {e}")


# Test 4: 타임아웃
print("\n【 Test 4: 타임아웃 처리 】")
try:
    async def test_timeout():
        try:
            await asyncio.wait_for(asyncio.sleep(1), timeout=0.1)
            return "not timeout"
        except asyncio.TimeoutError:
            return "timeout"

    result = asyncio.run(test_timeout())
    assert result == "timeout", "타임아웃 미작동"
    test_results.append(("Test 4: 타임아웃", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 4: 타임아웃", False))
    print(f"  ✗ FAIL: {e}")


# Test 5: 예외 처리
print("\n【 Test 5: 예외 처리 】")
try:
    async def test_exception():
        async def fail():
            raise ValueError("error")

        results = await asyncio.gather(
            asyncio.sleep(0.01),
            fail(),
            asyncio.sleep(0.01),
            return_exceptions=True
        )
        return results

    results = asyncio.run(test_exception())
    assert len(results) == 3, "결과 개수 오류"
    assert isinstance(results[1], ValueError), "예외 미처리"
    test_results.append(("Test 5: 예외 처리", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 5: 예외 처리", False))
    print(f"  ✗ FAIL: {e}")


# 테스트 결과 요약
print(f"\n{'='*60}")
print("【 테스트 요약 】")
for test_name, result in test_results:
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"  {test_name}: {status}")

passed = sum(1 for _, result in test_results if result)
total = len(test_results)
print(f"\n  총점: {passed}/{total} ({100*passed//total}%)")
print(f"{'='*60}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🎓 Part 9: 최종 메시지
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║       🎓 Python 대학교 2학년 v4.1 완료 축하합니다!                           ║
╚════════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 v4.1에서 배운 것:

   ✓ 동기(Synchronous) vs 비동기(Asynchronous)
     기다림을 효율로 바꾸는 설계

   ✓ async/await 키워드
     비동기 함수 정의와 대기점 지정

   ✓ 이벤트 루프 (Event Loop)
     여러 작업을 효율적으로 관리하는 지휘자

   ✓ asyncio.gather()
     여러 코루틴을 동시에 실행

   ✓ asyncio.create_task()
     개별 작업 관리 및 추적

   ✓ I/O 바운드 작업 최적화
     네트워크, 파일 I/O 작업 고속화

   ✓ 타임아웃과 예외 처리
     안정적인 비동기 시스템 설계

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 핵심 인사이트:

   "기다림을 효율로 바꾼다"

   동기: 3 + 1 + 2 = 6초
   비동기: max(3, 1, 2) = 3초

   ⭐ 2배 빠른 성능!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 다음: [v4.2: 멀티프로세싱(Multiprocessing) — 진짜로 동시에 연산하기]

   비동기: I/O 대기 시간 활용 (싱글 코어)
   멀티프로세싱: CPU 연산 병렬화 (멀티 코어)

   즉, v4.1은 "I/O를 효율화"하는 것이고,
   v4.2는 "CPU를 분산"하는 것입니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

질문: 다음 전공 수업으로 진행하시겠습니까?

저장 필수 너는 기록이 증명이다 gogs
╚════════════════════════════════════════════════════════════════════════════════╝
""")
