#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  v1.2: 반복의 미학 - 이터레이터(Iterators)와 메모리 효율성                    ║
║  [Iterators and Lazy Evaluation - The Art of Deferred Computation]           ║
║                                                                               ║
║  철학: "고교 시절 Gogs-Lang에서 우리는 인덱스와 메모리 주소를 직접 다루었다면, ║
║        파이썬의 대학 과정에서 '반복'은 단순한 루프가 아니라              ║
║        '필요할 때만 생성하는 지능형 흐름'입니다."                         ║
║                                                                               ║
║  새로운 사고:                                                                ║
║  1억 개의 숫자가 필요할 때, 1억 개의 방을 미리 만드는 것은 낭비입니다.      ║
║  대신, "다음 숫자가 뭐야?"라고 물을 때마다                               ║
║  하나씩 대답해주는 '공장'을 만들 수 있습니다.                            ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs                                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import time
import gc
from typing import Iterator, Generator, Any, List

print("=" * 80)
print("v1.2: 반복의 미학 - 이터레이터와 메모리 효율성")
print("=" * 80)

# ============================================================================
# 파트 1: 탐구(대학) - "모든 데이터를 메모리에 올릴 필요가 있는가?"
# ============================================================================

print("\n【 파트 1: 탐구 - 새로운 사고의 시작 】")
print("고교(Gogs-Lang): 루프 = 인덱스와 메모리 주소의 직접 제어")
print("대학(Python):   루프 = '필요할 때만 생성하는 지능형 흐름'")

print("\n" + "-" * 80)
print("탐구 1-1: 리스트(Eager List) vs 제너레이터(Lazy Generator)")
print("-" * 80)

# Eager: 모든 데이터를 미리 메모리에 할당
print("\n[Eager Evaluation] - 100만 개 숫자를 미리 생성")
eager_start = time.time()
eager_list = [i for i in range(1000000)]
eager_time = time.time() - eager_start
eager_size = sys.getsizeof(eager_list)

print(f"  생성 시간: {eager_time:.6f}초")
print(f"  메모리 크기: {eager_size:,} bytes ({eager_size / 1024 / 1024:.2f} MB)")

# Lazy: 필요할 때만 하나씩 생성
print("\n[Lazy Evaluation] - 제너레이터로 '규칙'만 저장")
lazy_start = time.time()
lazy_gen = (i for i in range(1000000))
lazy_time = time.time() - lazy_start
lazy_size = sys.getsizeof(lazy_gen)

print(f"  생성 시간: {lazy_time:.6f}초")
print(f"  메모리 크기: {lazy_size:,} bytes")

print(f"\n【 증명 1-1 】")
print(f"  메모리 절약율: {(1 - lazy_size/eager_size) * 100:.2f}%")
print(f"  시간 절약: {eager_time / lazy_time:.0f}배 빠름")
print(f"\n해석:")
print(f"  - 리스트: 100만 개 정수를 모두 메모리에 저장 (약 {eager_size / 1024 / 1024:.1f}MB)")
print(f"  - 제너레이터: 현재 상태와 규칙만 저장 (단 {lazy_size} bytes)")
print(f"  - '필요할 때만'이라는 원칙의 위력!")

# ============================================================================
# 파트 2: yield 키워드와 코루틴의 기초
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 2: yield와 코루틴 - 상태를 정지시키는 마법 】")
print("=" * 80)

print("\ntarget는 Gogs의 '포인터'처럼 상태를 기억하는 생명체입니다:")

def count_generator(n: int) -> Generator[int, None, None]:
    """
    제너레이터 함수: yield를 만날 때마다 값을 반환하고 상태를 정지(Suspend)
    다음 next() 호출 시 정지된 지점에서 다시 시작(Resume)
    """
    print("  [Generator 시작]")
    for i in range(n):
        print(f"    내부 상태: i={i}, 다음 yield 대기중...")
        yield i  # 값을 반환하고 상태를 저장한 뒤 정지
        # 다음 next()가 호출될 때까지 여기서 대기

def fibonacci_generator(max_count: int) -> Generator[int, None, None]:
    """
    무한 수열의 예: 피보나치 수열
    리스트로는 불가능하지만, 제너레이터는 논리적으로 '무한'을 담을 수 있음
    """
    a, b = 0, 1
    count = 0
    while count < max_count:
        yield a
        a, b = b, a + b
        count += 1

print("\n【 탐구 2-1: 제너레이터의 코루틴 동작 】")
gen = count_generator(3)

print("\n첫 번째 next() 호출:")
val1 = next(gen)
print(f"  반환값: {val1}")

print("\n두 번째 next() 호출:")
val2 = next(gen)
print(f"  반환값: {val2}")

print("\n세 번째 next() 호출:")
val3 = next(gen)
print(f"  반환값: {val3}")

print("\n【 해석 】")
print("  제너레이터는 다음과 같이 작동합니다:")
print("  1. yield에서 값을 반환")
print("  2. 함수의 상태(로컬 변수, 실행 위치)를 메모리에 저장")
print("  3. next() 호출까지 대기(Suspend)")
print("  4. 다음 next() 호출 시 정지된 지점에서 계속 실행(Resume)")
print("  → 이것이 코루틴의 기초입니다!")

print("\n【 탐구 2-2: 무한 수열의 표현 】")
print("\nFibonacci 수열 생성 (제너레이터로 무한 표현 가능):")
fib_gen = fibonacci_generator(10)
fib_values = list(fib_gen)
print(f"  첫 10개: {fib_values}")

# ============================================================================
# 파트 3: 증명(대학원) - "메모리 점유율의 극적 차이"
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 3: 증명 - 메모리 점유율의 극적 차이 】")
print("=" * 80)

print("\n【 증명 3-1: 스케일 테스트 】")

test_sizes = [100, 1000, 10000, 100000, 1000000]

print(f"\n{'크기':<12} {'List (MB)':<15} {'Gen (bytes)':<15} {'절약율':<10}")
print("-" * 55)

for size in test_sizes:
    # List 메모리
    list_obj = [i for i in range(size)]
    list_mem = sys.getsizeof(list_obj)

    # Generator 메모리
    gen_obj = (i for i in range(size))
    gen_mem = sys.getsizeof(gen_obj)

    # 계산
    list_mb = list_mem / (1024 * 1024)
    savings = (1 - gen_mem / list_mem) * 100

    print(f"{size:<12} {list_mb:<15.2f} {gen_mem:<15} {savings:<10.1f}%")

    # 메모리 해제
    del list_obj, gen_obj
    gc.collect()

print("\n【 증명 3-2: 리스트 컴프리헨션 vs 제너레이터 표현식 】")
print("\nSyntax 비교:")
print("  List Comprehension:    [i for i in range(1000000)]")
print("  Generator Expression:  (i for i in range(1000000))")
print("  → 단 괄호 하나의 차이가 메모리의 운명을 결정합니다!")

# 실제 비교
list_comp = [i for i in range(100000)]
gen_expr = (i for i in range(100000))

print(f"\nList Comprehension 메모리: {sys.getsizeof(list_comp):,} bytes")
print(f"Generator Expression 메모리: {sys.getsizeof(gen_expr):,} bytes")
print(f"메모리 절약: {(1 - sys.getsizeof(gen_expr) / sys.getsizeof(list_comp)) * 100:.1f}%")

# ============================================================================
# 파트 4: 시간과 공간의 트레이드오프
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 4: 설계의 핵심 - 시간과 공간의 트레이드오프 】")
print("=" * 80)

print("\n새로운 사고: '무엇을 미리 계산하고, 무엇을 나중에 계산할 것인가?'")

print("\n【 트레이드오프 1: 임의 접근(Random Access) 】")
print("\n시나리오: 500만 번째 숫자를 보고 싶다면?")

# Eager: O(1) 접근
list_data = [i for i in range(10000000)]
eager_access_start = time.time()
value = list_data[5000000]
eager_access_time = time.time() - eager_access_start

print(f"  [List] 즉시 접근: {eager_access_time * 1000:.6f}ms")

# Lazy: O(n) 계산
gen_data = (i for i in range(10000000))
lazy_access_start = time.time()
for _ in range(5000000):
    value = next(gen_data)
lazy_access_time = time.time() - lazy_access_start

print(f"  [Generator] 순차 계산: {lazy_access_time:.3f}초")
print(f"  → Generator는 {'약 ' + str(int(lazy_access_time / eager_access_time)) + '배 느림'}")

print("\n【 트레이드오프 분석 】")
print("  List:       메모리 많이 사용 ✗, 빠른 접근 ✓")
print("  Generator:  메모리 절약 ✓, 느린 순차 접근 ✗")
print("\n→ 무엇이 필요한가? 그것이 설계의 기준입니다!")

# ============================================================================
# 파트 5: 무한 수열의 증명
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 5: 무한 수열의 증명 - Generator의 진정한 능력 】")
print("=" * 80)

print("\n리스트는 끝이 있어야 하지만, 제너레이터는 논리적으로 '무한'을 담을 수 있습니다:")

def infinite_counter() -> Generator[int, None, None]:
    """
    무한 카운터: 영원히 멈추지 않는 수열
    리스트로는 불가능하지만, 제너레이터는 논리적으로 정의 가능
    """
    count = 0
    while True:  # 끝나지 않음!
        yield count
        count += 1

def infinite_powers_of_two() -> Generator[int, None, None]:
    """
    2의 무한 거듭제곱: 1, 2, 4, 8, 16, ...
    """
    power = 0
    while True:
        yield 2 ** power
        power += 1

print("\n【 증명 5-1: 무한 카운터 】")
counter = infinite_counter()
print("처음 10개 값:")
values = [next(counter) for _ in range(10)]
print(f"  {values}")

print("\n【 증명 5-2: 2의 무한 거듭제곱 】")
powers = infinite_powers_of_two()
print("처음 10개 값:")
values = [next(powers) for _ in range(10)]
print(f"  {values}")

print("\n【 해석 】")
print("  리스트: [1, 2, 4, 8, ...] 를 모두 저장할 수 없음 (메모리 부족)")
print("  제너레이터: (2**n for n in range(...)) 로 무한을 논리적으로 표현")
print("  → '기록'된 규칙이 정해진 패턴을 영원히 생성합니다!")

# ============================================================================
# 파트 6: Iterator Protocol과 Gogs의 포인터
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 6: Iterator Protocol - Gogs 포인터와의 연결 】")
print("=" * 80)

print("\nGogs-Lang의 포인터: 메모리 주소를 저장하고 추적")
print("Python의 Iterator: 상태와 '다음'을 저장하고 추적")

class BiologicalSignalIterator:
    """
    Gogs의 신경신호를 생성하는 이터레이터
    내부적으로 상태를 유지하며, 매번 '다음 신호'를 생성
    """
    def __init__(self, signal_count: int):
        self.count = 0
        self.max = signal_count
        self.voltage = -70.0  # 초기 휴지 전위

    def __iter__(self):
        """이터레이터 프로토콜: 자신을 반환"""
        return self

    def __next__(self):
        """이터레이터 프로토콜: 다음 값을 반환"""
        if self.count >= self.max:
            raise StopIteration

        # 신경신호 생성 (시뮬레이션)
        self.voltage += 5.0  # 활동 전위로 증가
        signal = {
            'signal_id': self.count,
            'voltage': self.voltage,
            'timestamp': self.count * 0.001  # 1ms 간격
        }
        self.count += 1
        return signal

print("\n【 증명 6: 신경신호 이터레이터 】")
print("\nBiologicalSignalIterator로 신호를 하나씩 생성:")

signal_iter = BiologicalSignalIterator(5)
print("\n신경신호 5개:")
for signal in signal_iter:
    print(f"  Signal {signal['signal_id']}: V={signal['voltage']:6.1f}mV, T={signal['timestamp']:.3f}s")

print("\n【 해석 】")
print("  Iterator = '상태를 유지하는 객체'")
print("  Generator = '상태를 자동으로 유지하는 Iterator'")
print("  → Gogs의 포인터가 메모리 주소를 추적하듯,")
print("    Python의 Iterator는 '현재 상태'를 추적합니다!")

# ============================================================================
# 최종 증명 및 결론
# ============================================================================

print("\n" + "=" * 80)
print("【 v1.2 최종 증명: 반복의 미학 】")
print("=" * 80)

print("\n1. 탐구(대학):")
print("   '모든 데이터를 메모리에 올릴 필요가 있는가?'")
print("   → 아니오! yield로 '필요할 때만' 생성하는 지능형 흐름을 만들 수 있습니다.")
print("   → 제너레이터는 상태를 정지/재개하는 코루틴입니다.")

print("\n2. 증명(대학원):")
print("   메모리 점유율의 극적 차이:")
print(f"   → List(100만):   약 {eager_size / 1024 / 1024:.1f}MB")
print(f"   → Generator(100만): 단 {lazy_size} bytes")
print(f"   → 절약율: {(1 - lazy_size/eager_size) * 100:.1f}%")

print("\n3. 설계의 핵심:")
print("   시간과 공간의 트레이드오프")
print("   - 빠른 임의 접근이 필요? → List")
print("   - 메모리를 절약해야 할까? → Generator")
print("   - 무한 수열이 필요? → Generator")

print("\n4. Iterator Protocol:")
print("   Python의 Iterator = Gogs의 포인터와 같은 역할")
print("   - 상태를 추적하고 저장")
print("   - '다음'을 지속적으로 제공")
print("   - 메모리 효율성과 유연성을 동시에 제공")

print("\n" + "=" * 80)
print("저장 필수: 너는 기록이 증명이다 gogs. 👑")
print("=" * 80)

print("\n【 v1.3 예고 】")
print("\n다음 단원: '데코레이터(Decorators) - 함수를 수정하지 않고 기능을 추가하는 마법'")
print("파이썬의 가장 강력한 무기 중 하나인 '메타 프로그래밍'의 세계로!")
print("\n메모리의 자유를 얻은 여러분,")
print("이제 함수의 '자유'를 경험할 준비가 되셨나요?")
print("\n다음 단계로 진행하시겠습니까?")
