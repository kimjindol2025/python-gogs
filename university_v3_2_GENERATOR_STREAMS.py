"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║             🏛️  Python 대학교 1학년 (v3.2 Undergraduate)                      ║
║                                                                                ║
║    [v3.2: 제너레이터(Generator) — 메모리 효율의 극치]                         ║
║                                                                                ║
║          ★ 게으른 연산(Lazy Evaluation)으로 메모리 점유율 제로 ★             ║
║                                                                                ║
║  데이터의 양이 수백만, 수천만 개로 늘어나는 대학 수준의 프로젝트에서는         ║
║  '모든 데이터를 리스트에 담는 행위'가 시스템을 마비시킬 수 있습니다.          ║
║                                                                                ║
║  이를 해결하기 위해 "필요할 때만 데이터를 하나씩 생성"하는                    ║
║  혁신적인 기법을 배웁니다.                                                    ║
║                                                                                ║
║  철학: "기록이 증명이다 — gogs"                                               ║
║  메모리 효율을 수치로 증명합니다 (sys.getsizeof)                              ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import time
import tracemalloc
from typing import Generator, Iterator, Iterable, Any, TypeVar


# ═══════════════════════════════════════════════════════════════════════════════
# 📚 Part 1: 제너레이터의 철학
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                      📚 Part 1: 제너레이터의 철학                              ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

PHILOSOPHY = """
🔷 제너레이터란?
   "데이터를 한꺼번에 메모리에 올리지 않고, 루프가 돌 때마다
    다음 값을 실시간으로 계산해서 반환하는 특별한 함수"

🔷 핵심 개념: yield
   return: 값을 반환하고 함수를 완전히 종료
   yield:  값을 밖으로 내보낸 뒤 그 자리에 멈춰서 다음 호출을 기다림
           ⭐ 함수의 상태를 기억합니다!

🔷 왜 사용하나? (증명을 위한 효율성)
   1. 메모리 절약
      ❌ 리스트: 10억 개 숫자 = 수 GB 메모리 필요
      ✅ 제너레이터: 숫자 1개 = 메모리 수십 바이트

   2. 무한 수열
      ❌ 리스트: 끝이 있어야 만들 수 있음
      ✅ 제너레이터: 끝이 없는 수열도 표현 가능

   3. 성능
      ❌ 리스트: 모든 데이터 생성 후 반환 (대기 시간 길음)
      ✅ 제너레이터: 필요한 순간에 바로 생성 (대기 시간 짧음)

🔷 게으른 평가 (Lazy Evaluation)
   제너레이터는 "정말 필요할 때까지 계산을 미룬다"는 뜻입니다.

【 비유 】
   리스트:     도서관에서 책 1,000권을 한번에 가져온 후 읽기 시작
   제너레이터: 필요한 책 1권씩 받아서 읽으며 진행
"""

print(PHILOSOPHY)


# ═══════════════════════════════════════════════════════════════════════════════
# 🔄 Part 2: yield vs return — 함수의 상태 기억
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║             🔄 Part 2: yield vs return — 함수의 상태 기억                      ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 return: 완전히 종료 】")

def return_example(n):
    """return을 사용한 함수"""
    result = []
    for i in range(n):
        result.append(i)
    return result  # 이 순간 함수는 완전히 종료

print("  return_example(5) 호출:")
result = return_example(5)
print(f"    결과: {result}")
print(f"    함수는 완전히 종료됨")


print("\n【 yield: 일시정지하고 상태 기억 】")

def yield_example(n):
    """yield를 사용한 함수 (제너레이터)"""
    i = 0
    while i < n:
        print(f"    [제너레이터 내부] i={i} 계산")
        yield i  # 값을 내보내고 이 자리에서 일시정지!
        print(f"    [제너레이터 내부] 다시 재개됨")
        i += 1


print("  yield_example(3) 호출:")
gen = yield_example(3)
print(f"    제너레이터 객체: {gen}")

print("\n  첫 번째 next() 호출:")
val1 = next(gen)
print(f"    값: {val1}")

print("\n  두 번째 next() 호출:")
val2 = next(gen)
print(f"    값: {val2}")

print("\n  세 번째 next() 호출:")
val3 = next(gen)
print(f"    값: {val3}")

print("\n  네 번째 next() 호출 (더 이상 데이터 없음):")
try:
    val4 = next(gen)
except StopIteration:
    print(f"    ✗ StopIteration 예외 발생 (제너레이터 종료)")


# ═══════════════════════════════════════════════════════════════════════════════
# 📊 Part 3: 리스트 vs 제너레이터 — 메모리 사용량 비교
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║           📊 Part 3: 리스트 vs 제너레이터 — 메모리 사용량 비교               ║
║                       (증명: sys.getsizeof)                                   ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 작은 규모 (100개 데이터) 】")

# 리스트 방식
def create_list(n):
    return [i for i in range(n)]

# 제너레이터 방식
def create_generator(n):
    for i in range(n):
        yield i


n = 100
list_data = create_list(n)
gen_data = create_generator(n)

list_size = sys.getsizeof(list_data)
gen_size = sys.getsizeof(gen_data)

print(f"  리스트 크기:      {list_size:,} 바이트")
print(f"  제너레이터 크기:  {gen_size:,} 바이트")
print(f"  절약률:           {(1 - gen_size/list_size)*100:.1f}%")


print("\n【 중간 규모 (100,000개 데이터) 】")

n = 100_000
list_data = create_list(n)
gen_data = create_generator(n)

list_size = sys.getsizeof(list_data)
gen_size = sys.getsizeof(gen_data)

print(f"  리스트 크기:      {list_size:,} 바이트 ({list_size / 1024 / 1024:.2f} MB)")
print(f"  제너레이터 크기:  {gen_size:,} 바이트")
print(f"  절약률:           {(1 - gen_size/list_size)*100:.1f}%")
print(f"  ⭐ {list_size // gen_size}배 이상의 메모리 절약!")


print("\n【 대규모 시뮬레이션 (1,000,000개 데이터) 】")

n = 1_000_000

# 리스트 생성 (시간 측정)
start = time.time()
list_data = create_list(n)
list_time = time.time() - start
list_size = sys.getsizeof(list_data)

# 제너레이터 생성 (시간 측정)
start = time.time()
gen_data = create_generator(n)
gen_time = time.time() - start
gen_size = sys.getsizeof(gen_data)

print(f"  리스트:")
print(f"    크기:      {list_size:,} 바이트 ({list_size / 1024 / 1024:.2f} MB)")
print(f"    생성 시간: {list_time:.4f}초")

print(f"  제너레이터:")
print(f"    크기:      {gen_size:,} 바이트")
print(f"    생성 시간: {gen_time:.6f}초")

print(f"  ⭐ 메모리 절약: {(1 - gen_size/list_size)*100:.1f}%")
print(f"  ⭐ 생성 속도: {list_time/gen_time:.0f}배 빠름!")


# ═══════════════════════════════════════════════════════════════════════════════
# 🔷 Part 4: 기초 제너레이터 — 다양한 패턴
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                  🔷 Part 4: 기초 제너레이터 — 다양한 패턴                     ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

# 제너레이터 1: 범위 생성기
print("\n【 제너레이터 1: 범위 생성기 】")

def gogs_range(start, end, step=1):
    """Python의 range()를 제너레이터로 구현"""
    current = start
    while current < end:
        yield current
        current += step


print("  gogs_range(0, 5) 사용:")
for num in gogs_range(0, 5):
    print(f"    {num}")


# 제너레이터 2: 조건 필터링
print("\n【 제너레이터 2: 조건 필터링 】")

def even_numbers(n):
    """n 이하의 짝수만 생성"""
    for i in range(n):
        if i % 2 == 0:
            yield i


print("  even_numbers(10):")
print(f"    {list(even_numbers(10))}")


# 제너레이터 3: 데이터 변환
print("\n【 제너레이터 3: 데이터 변환 】")

def square_numbers(n):
    """n 이하의 수들의 제곱값 생성"""
    for i in range(1, n + 1):
        yield i ** 2


print("  square_numbers(5):")
for sq in square_numbers(5):
    print(f"    {sq}", end=" ")
print()


# 제너레이터 4: 문자열 처리
print("\n【 제너레이터 4: 문자열 처리 】")

def character_generator(text):
    """문자열을 한 글자씩 생성"""
    for char in text:
        yield char.upper()


print("  character_generator('hello'):")
result = ''.join(character_generator('hello'))
print(f"    {result}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 Part 5: 이터러블과 이터레이터 — 대학 시험 핵심 개념
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║          🎯 Part 5: 이터러블과 이터레이터 — 대학 시험 핵심 개념              ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("""
【 3가지 개념의 차이 】

1️⃣  이터러블 (Iterable)
    - for 루프에 들어갈 수 있는 객체
    - __iter__() 메서드를 가짐
    - 예: list, tuple, dict, str, range, 제너레이터

2️⃣  이터레이터 (Iterator)
    - next()를 통해 다음 값을 꺼낼 수 있는 상태의 객체
    - __iter__()와 __next__() 메서드를 모두 가짐
    - 예: 제너레이터

3️⃣  제너레이터 (Generator)
    - 이터러블과 이터레이터를 동시에 가짐 ⭐
    - yield를 사용한 함수
    - for 루프도 가능하고 next()도 가능
""")

print("\n【 예제: 직접 구현한 이터레이터 클래스 】")

class CountUp:
    """1부터 n까지 세는 이터레이터"""

    def __init__(self, n):
        self.n = n
        self.current = 1

    def __iter__(self):
        """이터러블 프로토콜: iter() 호출 시"""
        return self

    def __next__(self):
        """이터레이터 프로토콜: next() 호출 시"""
        if self.current <= self.n:
            result = self.current
            self.current += 1
            return result
        else:
            raise StopIteration


print("  CountUp(3) 사용:")
counter = CountUp(3)
print(f"    next(): {next(counter)}")
print(f"    next(): {next(counter)}")
print(f"    next(): {next(counter)}")

try:
    print(f"    next(): {next(counter)}")
except StopIteration:
    print(f"    StopIteration 발생")

print("\n  for 루프와도 호환:")
for num in CountUp(3):
    print(f"    {num}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 Part 6: 제너레이터 표현식 — 한 줄로 쓰는 제너레이터
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║           🎨 Part 6: 제너레이터 표현식 — 한 줄로 쓰는 제너레이터            ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 리스트 컴프리헨션 vs 제너레이터 표현식 】")

print("\n  리스트 컴프리헨션 (메모리 많음):")
list_comp = [x**2 for x in range(5)]
print(f"    [x**2 for x in range(5)]")
print(f"    크기: {sys.getsizeof(list_comp)} 바이트")
print(f"    결과: {list_comp}")

print("\n  제너레이터 표현식 (메모리 적음):")
gen_expr = (x**2 for x in range(5))
print(f"    (x**2 for x in range(5))")
print(f"    크기: {sys.getsizeof(gen_expr)} 바이트")
print(f"    결과: {list(gen_expr)}")


print("\n【 제너레이터 표현식 예제들 】")

# 1. 조건 필터링
print("\n  조건 필터링:")
evens = (x for x in range(10) if x % 2 == 0)
print(f"    (x for x in range(10) if x % 2 == 0)")
print(f"    = {list(evens)}")

# 2. 중첩 변환
print("\n  중첩 변환:")
pairs = ((x, y) for x in range(2) for y in range(2))
print(f"    ((x, y) for x in range(2) for y in range(2))")
print(f"    = {list(pairs)}")

# 3. 문자열 변환
print("\n  문자열 변환:")
chars = (c.upper() for c in "hello")
print(f"    (c.upper() for c in 'hello')")
print(f"    = {''.join(chars)}")


# ═══════════════════════════════════════════════════════════════════════════════
# ♾️  Part 7: 무한 수열 — 제너레이터의 진정한 강력함
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║            ♾️  Part 7: 무한 수열 — 제너레이터의 진정한 강력함                ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 무한 자연수 생성기 】")

def infinite_counter(start=0):
    """끝이 없는 자연수를 생성하는 제너레이터"""
    current = start
    while True:
        yield current
        current += 1


print("  첫 10개의 자연수:")
counter = infinite_counter(1)
print(f"    {[next(counter) for _ in range(10)]}")


print("\n【 피보나치 수열 (무한) 】")

def fibonacci():
    """피보나치 수열을 무한히 생성"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


print("  첫 10개의 피보나치 수:")
fib = fibonacci()
print(f"    {[next(fib) for _ in range(10)]}")


print("\n【 무한 반복 】")

def repeat(value):
    """같은 값을 무한히 반복하는 제너레이터"""
    while True:
        yield value


print("  무한 반복 예제:")
rep = repeat("X")
print(f"    [repeat('X') 첫 5개]: {[next(rep) for _ in range(5)]}")


# ═══════════════════════════════════════════════════════════════════════════════
# 📈 Part 8: 실전 프로젝트 — 대용량 데이터 처리
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║             📈 Part 8: 실전 프로젝트 — 대용량 데이터 처리                     ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 시뮬레이션: 센서에서 100만 개의 데이터 수신 】")

def sensor_data_stream(num_readings, anomaly_rate=0.05):
    """
    센서에서 실시간으로 데이터를 수신하는 시뮬레이션

    Args:
        num_readings: 총 데이터 수
        anomaly_rate: 이상값 발생 확률
    """
    import random

    for i in range(num_readings):
        # 정상 데이터 (평균 50, 표준편차 5)
        if random.random() > anomaly_rate:
            value = 50 + random.gauss(0, 5)
        else:
            # 이상값 (매우 큰 수)
            value = random.uniform(100, 200)

        yield {
            "id": i,
            "timestamp": time.time(),
            "value": value,
            "anomaly": value > 100
        }


# 제너레이터 사용: 메모리 효율적
print("\n  메모리 효율적 처리 (제너레이터):")

start_time = time.time()
anomaly_count = 0
processed = 0

stream = sensor_data_stream(100_000, anomaly_rate=0.02)
for reading in stream:
    if reading["anomaly"]:
        anomaly_count += 1
    processed += 1

    if processed % 20_000 == 0:
        elapsed = time.time() - start_time
        print(f"    처리됨: {processed:,}개 | 이상값: {anomaly_count} | 경과시간: {elapsed:.2f}초")

print(f"\n  최종 결과:")
print(f"    총 처리: {processed:,}개")
print(f"    이상값: {anomaly_count}개 ({anomaly_count/processed*100:.2f}%)")


# ═══════════════════════════════════════════════════════════════════════════════
# 💾 Part 9: 메모리 프로파일링 — 증명!
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║              💾 Part 9: 메모리 프로파일링 — 증명!                             ║
║                   (tracemalloc으로 정확한 메모리 측정)                         ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 리스트 방식 메모리 사용 】")

tracemalloc.start()

# 리스트로 100만 개 데이터 생성
list_data = [i**2 for i in range(1_000_000)]

current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"  현재 사용: {current / 1024 / 1024:.2f} MB")
print(f"  피크 사용: {peak / 1024 / 1024:.2f} MB")


print("\n【 제너레이터 방식 메모리 사용 】")

tracemalloc.start()

# 제너레이터로 100만 개 데이터 생성 (실제로 사용하지 않으면 메모리 미사용)
gen_data = (i**2 for i in range(1_000_000))

current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"  현재 사용: {current / 1024 / 1024:.2f} MB")
print(f"  피크 사용: {peak / 1024 / 1024:.2f} MB")
print(f"  ⭐ 거의 0에 가까운 메모리 사용!")


# ═══════════════════════════════════════════════════════════════════════════════
# ✅ Part 10: 최종 테스트 및 검증
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                   ✅ Part 10: 최종 테스트 및 검증                             ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

test_results = []

# Test 1: 기본 제너레이터 작동
print("\n【 Test 1: 기본 제너레이터 작동 】")
try:
    def test_gen():
        for i in range(3):
            yield i

    gen = test_gen()
    values = [next(gen) for _ in range(3)]
    assert values == [0, 1, 2], "값 오류"
    test_results.append(("Test 1: 기본 제너레이터", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 1: 기본 제너레이터", False))
    print(f"  ✗ FAIL: {e}")


# Test 2: 제너레이터 표현식
print("\n【 Test 2: 제너레이터 표현식 】")
try:
    gen_expr = (x * 2 for x in range(4))
    values = list(gen_expr)
    assert values == [0, 2, 4, 6], "표현식 오류"
    test_results.append(("Test 2: 제너레이터 표현식", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 2: 제너레이터 표현식", False))
    print(f"  ✗ FAIL: {e}")


# Test 3: 무한 제너레이터
print("\n【 Test 3: 무한 제너레이터 】")
try:
    def infinite():
        i = 0
        while True:
            yield i
            i += 1

    gen = infinite()
    first_five = [next(gen) for _ in range(5)]
    assert first_five == [0, 1, 2, 3, 4], "무한 제너레이터 오류"
    test_results.append(("Test 3: 무한 제너레이터", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 3: 무한 제너레이터", False))
    print(f"  ✗ FAIL: {e}")


# Test 4: 이터레이터 프로토콜
print("\n【 Test 4: 이터레이터 프로토콜 】")
try:
    class SimpleIterator:
        def __init__(self):
            self.count = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.count < 3:
                self.count += 1
                return self.count
            raise StopIteration

    it = SimpleIterator()
    values = list(it)
    assert values == [1, 2, 3], "이터레이터 오류"
    test_results.append(("Test 4: 이터레이터 프로토콜", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 4: 이터레이터 프로토콜", False))
    print(f"  ✗ FAIL: {e}")


# Test 5: 메모리 효율성
print("\n【 Test 5: 메모리 효율성 】")
try:
    list_size = sys.getsizeof([i for i in range(100_000)])
    gen_size = sys.getsizeof((i for i in range(100_000)))

    # 제너레이터가 리스트보다 최소 100배 작아야 함
    assert list_size > gen_size * 100, f"메모리 효율 오류: {list_size} vs {gen_size}"
    test_results.append(("Test 5: 메모리 효율성", True))
    print("  ✓ PASS")
    print(f"    리스트: {list_size:,} 바이트")
    print(f"    제너레이터: {gen_size:,} 바이트")
    print(f"    효율: {list_size // gen_size}배 이상")
except AssertionError as e:
    test_results.append(("Test 5: 메모리 효율성", False))
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
# 🎓 Part 11: 최종 메시지
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║           🎓 Python 대학교 1학년 v3.2 완료 축하합니다!                       ║
╚════════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 v3.2에서 배운 것:

   ✓ yield vs return
     yield는 함수를 일시정지하고 상태를 기억합니다.

   ✓ 게으른 평가 (Lazy Evaluation)
     필요할 때만 데이터를 생성해서 메모리 절약

   ✓ 이터러블과 이터레이터
     이터러블: for 루프 가능
     이터레이터: next() 사용 가능
     제너레이터: 둘 다 가능!

   ✓ 제너레이터 표현식
     한 줄로 제너레이터를 작성

   ✓ 무한 수열
     while True와 yield로 끝이 없는 데이터 표현

   ✓ 실전 대용량 처리
     100만 개 데이터를 메모리 부하 없이 처리

   ✓ 메모리 프로파일링
     sys.getsizeof()와 tracemalloc으로 증명

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 핵심 정리:

   "필요할 때만 데이터를 생성한다"

   v3.1: 데코레이터 → 코드 구조의 우아함
   v3.2: 제너레이터 → 메모리 효율의 극치

   이제 당신은 수십 기가바이트의 데이터를 메모리 부하 없이 처리할 수 있습니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 다음: [v3.3: 컨텍스트 매니저(Context Manager) — with문의 내부 구조]

   데코레이터로 "코드의 구조"를 설계하고,
   제너레이터로 "메모리 효율"을 극대화했다면,
   컨텍스트 매니저로 "자원 관리"의 완벽함을 배웁니다.

   with 문을 직접 설계하여 완벽한 자원 해제 시스템을 구축!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

질문: 다음 전공 수업으로 진행하시겠습니까?

저장 필수 너는 기록이 증명이다 gogs
╚════════════════════════════════════════════════════════════════════════════════╝
""")
