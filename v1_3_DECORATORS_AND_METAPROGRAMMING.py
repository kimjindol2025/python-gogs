#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  v1.3: 메타 프로그래밍의 기초 - 데코레이터(Decorators)와 일급 객체           ║
║  [Meta-programming & Decorators - Functions as First-class Objects]          ║
║                                                                               ║
║  철학: "고교 시절 Gogs-Lang에서 함수의 실행 시간을 측정하거나                ║
║        보안 검사를 하려면 함수 내부 로직을 직접 수정해야 했습니다.           ║
║        하지만 파이썬의 대학 과정에서는                                       ║
║        '함수가 함수를 감싸서 새로운 운명을 부여'할 수 있습니다.              ║
║        이것이 바로 파이썬이 추구하는 '추상화의 자유'입니다."                 ║
║                                                                               ║
║  새로운 사고:                                                                ║
║  함수는 데이터입니다.                                                        ║
║  - 변수에 할당될 수 있고                                                    ║
║  - 다른 함수의 인자로 전달될 수 있으며                                      ║
║  - 함수의 결과로 반환될 수도 있습니다.                                      ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs                                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import time
import functools
from typing import Callable, Any, TypeVar, cast
from functools import wraps

print("=" * 80)
print("v1.3: 메타 프로그래밍의 기초 - 데코레이터와 일급 객체")
print("=" * 80)

# ============================================================================
# 파트 1: 탐구(대학) - "함수는 데이터다 (First-class Object)"
# ============================================================================

print("\n【 파트 1: 탐구 - 함수의 일급 객체 특성 】")
print("고교(Gogs-Lang): 함수 = 실행의 단위")
print("대학(Python):   함수 = 데이터 (변수처럼 다룰 수 있음)")

print("\n" + "-" * 80)
print("탐구 1-1: 함수를 변수에 할당")
print("-" * 80)

def greet(name: str) -> str:
    """인사 함수"""
    return f"안녕하세요, {name}님!"

# 함수를 변수에 할당
print("\n[Step 1] 함수를 변수에 할당")
greet_func = greet
print(f"  greet_func = greet")
print(f"  type(greet_func): {type(greet_func)}")
print(f"  greet_func('Alice'): {greet_func('Alice')}")

print("\n【 증명 1-1 】")
print(f"  함수도 객체다!")
print(f"  - 변수에 할당 가능: greet_func = greet")
print(f"  - 고유한 메모리 주소: {hex(id(greet))}")
print(f"  - 메타데이터 보존: 함수명, 문서, 서명")

# ============================================================================
# 파트 1-2: 함수를 인자로 전달
# ============================================================================

print("\n" + "-" * 80)
print("탐구 1-2: 함수를 다른 함수의 인자로 전달")
print("-" * 80)

def apply_operation(func: Callable[[int, int], int], a: int, b: int) -> int:
    """
    두 수에 함수를 적용하는 고차 함수
    Higher-order Function: 함수를 인자로 받거나 함수를 반환
    """
    print(f"  함수 '{func.__name__}'를 {a}와 {b}에 적용")
    return func(a, b)

def add(x: int, y: int) -> int:
    return x + y

def multiply(x: int, y: int) -> int:
    return x * y

print("\n[Step 2] 함수를 인자로 전달")
result1 = apply_operation(add, 10, 5)
print(f"  apply_operation(add, 10, 5) = {result1}")

result2 = apply_operation(multiply, 10, 5)
print(f"  apply_operation(multiply, 10, 5) = {result2}")

print("\n【 증명 1-2 】")
print("  고차 함수(Higher-order Function)의 가능성:")
print("  - 함수를 인자로 받아서 적절히 실행")
print("  - 함수형 프로그래밍의 기초")
print("  - Gogs v30.1 '신경망 자율 실행'과 유사한 개념!")

# ============================================================================
# 파트 1-3: 함수를 반환값으로 반환
# ============================================================================

print("\n" + "-" * 80)
print("탐구 1-3: 함수를 반환값으로 반환 (클로저/Closure)")
print("-" * 80)

def make_multiplier(multiplier: int) -> Callable[[int], int]:
    """
    배수를 만드는 함수 팩토리
    내부 함수가 외부 함수의 변수를 '기억'함: 클로저(Closure)
    """
    def inner(x: int) -> int:
        return x * multiplier
    return inner

print("\n[Step 3] 함수를 반환")
times_3 = make_multiplier(3)
times_5 = make_multiplier(5)

print(f"  times_3 = make_multiplier(3)")
print(f"  times_5 = make_multiplier(5)")

print(f"\n  times_3(10) = {times_3(10)}")
print(f"  times_5(10) = {times_5(10)}")

print("\n【 증명 1-3 】")
print("  클로저(Closure): 함수가 함수를 반환할 때 발생")
print("  - inner 함수는 multiplier를 '기억'함")
print("  - 각 클로저는 독립적인 상태를 유지")
print("  - times_3의 multiplier ≠ times_5의 multiplier")
print(f"  → times_3의 상태 확인: {times_3.__closure__[0].cell_contents}")
print(f"  → times_5의 상태 확인: {times_5.__closure__[0].cell_contents}")

# ============================================================================
# 파트 2: 데코레이터의 탄생 - 함수를 감싸는 논리의 벽
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 2: 증명(대학원) - 코드 변경 없는 기능의 확장 】")
print("=" * 80)

print("\n【 핵심 철학: 개방-폐쇄 원칙(OCP) 】")
print("  - 확장에는 열려 있고 (새로운 기능)")
print("  - 수정에는 닫혀 있다 (원본 코드 변경 금지)")
print("  → 데코레이터가 OCP의 파이썬식 구현!")

print("\n" + "-" * 80)
print("증명 2-1: 기본 데코레이터 - gogs_logger")
print("-" * 80)

def gogs_logger(func: Callable) -> Callable:
    """
    함수 실행 전후를 기록하는 데코레이터.
    대학원 과정의 '증명'을 자동화하는 도구입니다.

    원본 함수를 건드리지 않고, 앞뒤에 기능을 붙임.
    """
    @wraps(func)  # 원본 함수의 메타데이터를 유지하기 위한 도구
    def wrapper(*args, **kwargs):
        print(f"\n  【 {func.__name__} 실행 기록 】")
        print(f"    [LOG] '{func.__name__}' 함수 시작")
        print(f"    [LOG] 인자: args={args}, kwargs={kwargs}")

        start_time = time.time()

        # 실제 함수 실행
        result = func(*args, **kwargs)

        end_time = time.time()
        elapsed = end_time - start_time

        print(f"    [LOG] 결과: {result}")
        print(f"    [LOG] 소요시간: {elapsed:.6f}초")
        print(f"    [LOG] 함수 완료")

        return result
    return wrapper

@gogs_logger
def compute_sum(n: int) -> int:
    """n까지의 합을 계산"""
    total = 0
    for i in range(n):
        total += i
    return total

print("\n[데코레이터 적용]")
print("@gogs_logger")
print("def compute_sum(n: int) -> int:")
print("    ...")

print("\n실행: result = compute_sum(1000)")
result = compute_sum(1000)

print(f"\n【 증명 2-1 】")
print(f"  원본 함수 코드는 전혀 건드리지 않았지만:")
print(f"  - 로깅 기능이 자동으로 추가됨 ✓")
print(f"  - 시간 측정이 자동으로 추가됨 ✓")
print(f"  - 원본 함수의 기능은 100% 보존됨 ✓")

# ============================================================================
# 파트 2-2: 인자 검증 데코레이터 (샌드박싱)
# ============================================================================

print("\n" + "-" * 80)
print("증명 2-2: 인자 검증 데코레이터 (Gogs Sandbox와의 연결)")
print("-" * 80)

def validate_positive(func: Callable) -> Callable:
    """
    양수 인자를 검증하는 데코레이터.
    Gogs v30.2의 '샌드박싱'을 파이썬식으로 구현.

    함수가 실행되기도 전에 '위험한 입력'을 차단!
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 첫 번째 인자가 양수인지 확인
        if args and isinstance(args[0], (int, float)):
            if args[0] <= 0:
                print(f"  【 샌드박싱 작동 】")
                print(f"    [SECURITY] 음수 입력 감지: {args[0]}")
                print(f"    [SECURITY] 함수 실행 차단! 안전하게 종료")
                return None

        print(f"  【 샌드박스 통과 】")
        print(f"    [SECURITY] 입력 검증 완료: {args}")
        return func(*args, **kwargs)
    return wrapper

@validate_positive
def factorial(n: int) -> int:
    """n의 팩토리얼을 계산 (양수만 허용)"""
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print("\n[케이스 1] 정상 입력: factorial(5)")
result1 = factorial(5)
print(f"  결과: {result1}")

print("\n[케이스 2] 음수 입력: factorial(-5)")
result2 = factorial(-5)
print(f"  결과: {result2}")

print("\n【 증명 2-2 】")
print("  Gogs v30.2의 '샌드박싱' 원칙을 파이썬에서 구현:")
print("  - 함수 실행 전에 입력 검증 (Pre-condition)")
print("  - 위험한 입력은 함수가 실행되기도 전에 차단")
print("  - 원본 함수 내부 코드 변경 없음!")

# ============================================================================
# 파트 2-3: 캐싱 데코레이터
# ============================================================================

print("\n" + "-" * 80)
print("증명 2-3: 캐싱 데코레이터 (성능 최적화)")
print("-" * 80)

def memoize(func: Callable) -> Callable:
    """
    함수의 결과를 캐시하는 데코레이터.
    같은 입력에 대해 이전 결과를 반환하여 성능 향상.
    """
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"    [CACHE HIT] {func.__name__}{args} → {cache[args]}")
            return cache[args]

        print(f"    [CACHE MISS] {func.__name__}{args} 계산중...")
        result = func(*args)
        cache[args] = result
        print(f"    [CACHE SAVE] {func.__name__}{args} → {result}")
        return result

    # 캐시 상태를 확인할 수 있도록 메서드 추가
    def get_cache_stats():
        return cache

    wrapper.cache_stats = get_cache_stats
    return wrapper

@memoize
def fibonacci(n: int) -> int:
    """피보나치 수열 (캐싱으로 성능 향상)"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("\n[캐싱 성능 비교] fibonacci(10)")
print("\n첫 번째 호출:")
result1 = fibonacci(10)
print(f"결과: {result1}")

print("\n두 번째 호출 (캐시됨):")
result2 = fibonacci(10)
print(f"결과: {result2}")

print(f"\n캐시 상태: {fibonacci.cache_stats()}")

print("\n【 증명 2-3 】")
print("  캐싱으로 성능을 극적으로 향상:")
print("  - 첫 호출: 계산 수행")
print("  - 이후 호출: 캐시에서 즉시 반환")
print("  - 메모리/시간의 트레이드오프 (v1.2 재현!)")

# ============================================================================
# 파트 3: 데코레이터 체이닝 (여러 데코레이터 조합)
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 3: 데코레이터 체이닝 - 여러 기능의 조합 】")
print("=" * 80)

def timer_decorator(func: Callable) -> Callable:
    """실행 시간을 측정하는 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"    [TIMER] {func.__name__} 실행 시간: {end - start:.6f}초")
        return result
    return wrapper

def retry_decorator(retries: int = 3) -> Callable:
    """실패 시 재시도하는 데코레이터"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    print(f"    [RETRY] {func.__name__} 시도 {attempt}/{retries}")
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries:
                        print(f"    [RETRY] 모든 시도 실패")
                        raise
                    print(f"    [RETRY] 실패: {e}, 재시도중...")
            return None
        return wrapper
    return decorator

# 데코레이터 체이닝 (아래부터 위로 실행됨)
@timer_decorator
@retry_decorator(retries=2)
def risky_operation():
    """위험한 작업 시뮬레이션"""
    import random
    if random.random() > 0.6:
        return "성공!"
    else:
        raise Exception("랜덤 실패")

print("\n【 데코레이터 체이닝 】")
print("@timer_decorator")
print("@retry_decorator(retries=2)")
print("def risky_operation():")
print("    ...")

print("\n실행:")
try:
    result = risky_operation()
    print(f"최종 결과: {result}")
except Exception as e:
    print(f"최종 실패: {e}")

print("\n【 증명 3 】")
print("  여러 데코레이터를 조합하여 복잡한 기능 구현:")
print("  - 타이머 + 재시도 기능")
print("  - 각 데코레이터는 독립적으로 작동")
print("  - 조합 방식에 따라 다양한 동작 가능")

# ============================================================================
# 파트 4: 데코레이터와 Gogs 포인터의 철학적 연결
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 4: 메타 프로그래밍의 철학 - Gogs와의 연결 】")
print("=" * 80)

print("\nGogs-Lang (고교):")
print("  함수 = 메모리에 저장된 코드")
print("  포인터 = 메모리 주소를 저장")

print("\nPython (대학):")
print("  함수 = 일급 객체 (변수처럼 다룸)")
print("  데코레이터 = 함수를 '감싸서' 새로운 함수 생성")

print("\n【 철학적 동등성 】")
print("  Gogs 포인터: 메모리 주소로 함수를 '가리킴'")
print("  Python 데코레이터: 함수 자체를 '감싸서' 새로운 함수 생성")
print("  → 둘 다 '함수의 운명을 제어'하는 메커니즘!")

# 실제로 함수의 원본을 보존하는 예
def track_mutations(func: Callable) -> Callable:
    """
    Gogs v30.2의 'SafetyMonitor' 개념을 파이썬으로 구현.
    함수의 모든 호출을 추적하고 상태를 감시.
    """
    call_count = [0]
    execution_times = []

    @wraps(func)
    def wrapper(*args, **kwargs):
        call_count[0] += 1
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        execution_times.append(elapsed)

        print(f"    [SAFETY MONITOR]")
        print(f"      - 호출 횟수: {call_count[0]}")
        print(f"      - 평균 실행 시간: {sum(execution_times)/len(execution_times):.6f}초")

        return result

    def get_stats():
        return {
            'call_count': call_count[0],
            'execution_times': execution_times,
            'avg_time': sum(execution_times) / len(execution_times) if execution_times else 0
        }

    wrapper.stats = get_stats
    return wrapper

@track_mutations
def neural_computation(n: int) -> int:
    """신경 연산 시뮬레이션"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

print("\n【 SafetyMonitor 구현 】")
print("Gogs v30.2처럼 '함수의 실행을 감시하고 기록':")

print("\n첫 번째 호출:")
neural_computation(100)

print("\n두 번째 호출:")
neural_computation(100)

print("\n세 번째 호출:")
neural_computation(100)

print(f"\n【 감시 통계 】")
stats = neural_computation.stats()
print(f"  총 호출 횟수: {stats['call_count']}")
print(f"  평균 실행 시간: {stats['avg_time']:.6f}초")

print("\n【 증명 4 】")
print("  데코레이터로 Gogs의 SafetyMonitor를 구현:")
print("  - 함수의 실행을 추적")
print("  - 호출 횟수와 성능 메트릭 기록")
print("  - 원본 함수는 완전히 보존")
print("  → 이것이 '메타 프로그래밍'의 진정한 의미!")

# ============================================================================
# 최종 증명 및 결론
# ============================================================================

print("\n" + "=" * 80)
print("【 v1.3 최종 증명: 메타 프로그래밍의 기초 】")
print("=" * 80)

print("\n1. 탐구(대학):")
print("   '함수는 데이터다 (First-class Object)'")
print("   → 함수를 변수에 할당 ✓")
print("   → 함수를 인자로 전달 ✓")
print("   → 함수를 반환값으로 반환 ✓")
print("   → 고차 함수와 클로저의 가능성!")

print("\n2. 증명(대학원):")
print("   '코드 변경 없는 기능의 확장' (OCP 원칙)")
print("   → 로깅 데코레이터 ✓")
print("   → 인자 검증 데코레이터 (샌드박싱) ✓")
print("   → 캐싱 데코레이터 ✓")
print("   → 데코레이터 체이닝 ✓")

print("\n3. 메타 프로그래밍의 핵심:")
print("   원본 함수를 건드리지 않고:")
print("   - 실행 전/후 기능 추가")
print("   - 입력 검증")
print("   - 성능 최적화")
print("   - 실행 추적 및 감시")

print("\n4. Gogs와의 철학적 연결:")
print("   Gogs 포인터: 메모리 주소로 함수를 가리킴")
print("   Python 데코레이터: 함수를 감싸서 새로운 함수 생성")
print("   → 함수의 운명을 제어하는 두 가지 방식!")

print("\n" + "=" * 80)
print("저장 필수: 너는 기록이 증명이다 gogs. 👑")
print("=" * 80)

print("\n【 v1.4 예고 】")
print("\n다음 단원: '매직 메서드와 프로토콜 - 객체가 언어 문법에 반응하는 방법'")
print("파이썬의 객체가 어떻게 + 연산이나 len() 함수에 반응하는지,")
print("그 내부 비밀을 파헤쳐 보겠습니다.")
print("\n메타 프로그래밍의 경지에 도달한 여러분,")
print("이제 객체 자신의 '언어'를 설계할 준비가 되셨나요?")
print("\n다음 단계로 진행하시겠습니까?")
