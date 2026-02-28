"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║             🏛️  Python 대학교 1학년 (v3.1 Undergraduate)                      ║
║                                                                                ║
║        [v3.1: 데코레이터(Decorator) — 코드의 재사용성과 관점 지향 설계]        ║
║                                                                                ║
║                         ★ 고급 설계 사상 ★                                    ║
║                                                                                ║
║  "기존 코드를 건드리지 않고 기능을 확장하는 마법"                             ║
║                                                                                ║
║  대학교까지는 "무엇을(What) 어떻게(How) 사용하는가"에 집중했다면,            ║
║  대학교 과정부터는 "코드의 구조를 어떻게 우아하게 설계하고,                  ║
║  기존 기능을 수정하지 않으면서 새로운 기능을 주입할 것인가"라는              ║
║  철학적이고 기술적인 고민을 시작합니다.                                      ║
║                                                                                ║
║  철학: "기록이 증명이다 — gogs"                                               ║
║  데코레이터는 말 그대로 "장식하는 사람"입니다.                                ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import time
import functools
from typing import Callable, Any, TypeVar, cast
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════════
# 📚 Part 1: 데코레이터의 철학
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                      📚 Part 1: 데코레이터의 철학                              ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

PHILOSOPHY = """
🔷 데코레이터란?
   "함수를 감싸는(Wrap) 함수"
   어떤 함수가 있을 때, 그 함수의 본체(알맹이)는 건드리지 않으면서
   앞뒤로 기능을 덧붙일 때 사용합니다.

🔷 비유: 실제 장식
   원래 함수: [핵심 로직]
   데코레이터: [사전 작업] → [핵심 로직] → [사후 작업]

🔷 왜 사용하나?
   1. 로그 기록: 모든 함수가 실행될 때마다 자동으로 시간을 기록
   2. 권한 확인: 특정 사용자만 함수를 실행할 수 있게 제한
   3. 성능 측정: 함수가 실행되는 데 걸리는 시간을 측정
   4. 캐싱: 같은 결과를 여러 번 계산하지 않도록 저장
   5. 에러 처리: 모든 함수에 일관된 에러 처리 적용

🔷 대학 철학: DRY & AOP
   - DRY (Don't Repeat Yourself): 중복을 제거합니다
   - AOP (Aspect-Oriented Programming): 관점 지향 프로그래밍

   100개 함수에 로그를 넣어야 할 때:
   ❌ 100번 코드를 수정 (고등학교 방식)
   ✅ @gogs_logger 한 줄씩 추가 (대학 방식)
"""

print(PHILOSOPHY)


# ═══════════════════════════════════════════════════════════════════════════════
# 🔷 Part 2: 일급 객체(First-class Object) — 함수의 진짜 정체성
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║           🔷 Part 2: 일급 객체(First-class Object)                            ║
║                      — 함수의 진짜 정체성                                     ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("""
【 일급 객체의 3가지 특징 】

1️⃣  변수에 담을 수 있다
   def greet(name):
       return f"안녕하세요, {name}님!"

   my_func = greet  # 함수를 변수에 할당
   print(my_func("Alice"))  # "안녕하세요, Alice님!"

2️⃣  다른 함수의 인자로 전달할 수 있다
   def apply_twice(func, value):
       return func(func(value))

   def double(x):
       return x * 2

   result = apply_twice(double, 3)  # 3 → 6 → 12

3️⃣  함수의 반환값이 될 수 있다 ⭐ (이것이 데코레이터!)
   def make_greeting(greeting_word):
       def greet(name):
           return f"{greeting_word}, {name}!"
       return greet

   hello = make_greeting("Hello")
   hello("Bob")  # "Hello, Bob!"
""")

# 실제 예제 1: 함수를 변수에 담기
print("\n【 예제 1: 함수를 변수에 담기 】")

def greet(name):
    return f"안녕하세요, {name}님!"

my_func = greet
print(f"  함수를 변수에 담기: my_func = greet")
print(f"  호출: {my_func('Alice')}")
print(f"  함수의 이름: {my_func.__name__}")


# 실제 예제 2: 함수를 인자로 전달하기
print("\n【 예제 2: 함수를 인자로 전달하기 】")

def apply_twice(func, value):
    """함수를 인자로 받아서 2번 적용"""
    result1 = func(value)
    result2 = func(result1)
    return result2

def double(x):
    """2배로 만드는 함수"""
    return x * 2

result = apply_twice(double, 3)
print(f"  apply_twice(double, 3) = {result}")
print(f"  계산: 3 → {double(3)} → {double(6)}")


# 실제 예제 3: 함수가 함수를 반환하기 (데코레이터의 기초!)
print("\n【 예제 3: 함수가 함수를 반환하기 (데코레이터 기초!) 】")

def make_greeting(greeting_word):
    """인사말을 매개변수로 받아서 함수를 만드는 함수"""
    def greet(name):
        return f"{greeting_word}, {name}!"
    return greet  # 함수 자체를 반환!

hello = make_greeting("Hello")
goodbye = make_greeting("Goodbye")

print(f"  hello('Bob') = {hello('Bob')}")
print(f"  goodbye('Charlie') = {goodbye('Charlie')}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️  Part 3: 기초 데코레이터 — 단계별 구성
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                   🛠️  Part 3: 기초 데코레이터                                 ║
║                            — 단계별 구성                                      ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("""
【 데코레이터 구성 단계 】

Step 1: 기존 함수
   def hello():
       print("Hello, World!")

Step 2: 래퍼 함수(Wrapper) 만들기
   def decorator(func):
       def wrapper():
           print("[사전 작업]")
           func()                      # 원래 함수 실행
           print("[사후 작업]")
       return wrapper

Step 3: @ 기호로 적용
   @decorator
   def hello():
       print("Hello, World!")

Step 4: 호출
   hello()
   # 출력:
   # [사전 작업]
   # Hello, World!
   # [사후 작업]
""")

# 실제 예제: 기초 데코레이터
print("\n【 실제 예제: 기초 데코레이터 】")

def simple_decorator(func):
    """가장 단순한 데코레이터"""
    def wrapper():
        print("  [데코레이터] 함수 실행 전")
        func()
        print("  [데코레이터] 함수 실행 후")
    return wrapper

@simple_decorator
def say_hello():
    print("  [함수] Hello!")

print("호출: say_hello()")
say_hello()


# ═══════════════════════════════════════════════════════════════════════════════
# ⏱️  Part 4: 실전 데코레이터 — 시간 측정 (gogs_logger)
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║              ⏱️  Part 4: 실전 데코레이터 — 시간 측정 (gogs_logger)           ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

def gogs_logger(func):
    """
    함수의 실행 시간을 자동으로 측정하여 기록하는 데코레이터

    이것이 바로 "기록이 증명이다"입니다!
    모든 함수의 성능을 자동으로 기록합니다.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 함수 실행 전
        start_time = time.time()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n  ├─ [LOG] {timestamp}")
        print(f"  ├─ 함수: {func.__name__}")
        print(f"  ├─ 인자: args={args}, kwargs={kwargs}")
        print(f"  └─ 연산 시작...")

        try:
            # 실제 함수 실행
            result = func(*args, **kwargs)

            # 함수 실행 후
            end_time = time.time()
            elapsed = end_time - start_time

            print(f"  ├─ 결과: {result}")
            print(f"  ├─ 소요시간: {elapsed:.4f}초")
            print(f"  └─ ✓ 완료")

            return result

        except Exception as e:
            end_time = time.time()
            elapsed = end_time - start_time
            print(f"  ├─ ✗ 에러: {type(e).__name__}: {e}")
            print(f"  ├─ 소요시간: {elapsed:.4f}초")
            print(f"  └─ ✗ 실패")
            raise

    return wrapper


# gogs_logger 데코레이터 사용 예제
print("\n【 예제 1: 간단한 계산 】")

@gogs_logger
def simple_add(a, b):
    """두 수를 더하는 함수"""
    return a + b

result1 = simple_add(10, 20)


print("\n【 예제 2: 시간이 걸리는 작업 】")

@gogs_logger
def heavy_calculation(iterations):
    """시간이 오래 걸리는 복잡한 연산"""
    total = 0
    for i in range(iterations):
        total += i ** 2
    return total

result2 = heavy_calculation(100000)


print("\n【 예제 3: 에러 처리 】")

@gogs_logger
def risky_division(a, b):
    """0으로 나누면 에러가 발생"""
    return a / b

try:
    result3 = risky_division(10, 0)
except ZeroDivisionError:
    print("  [처리됨] 0으로 나눌 수 없습니다")


# ═══════════════════════════════════════════════════════════════════════════════
# 🔐 Part 5: 고급 데코레이터 — 다양한 용도
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                  🔐 Part 5: 고급 데코레이터 — 다양한 용도                     ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

# 데코레이터 1: 권한 확인 (간단한 예)
print("\n【 데코레이터 1: 권한 확인 】")

def require_admin(func):
    """관리자만 실행할 수 있는 데코레이터"""
    @functools.wraps(func)
    def wrapper(user_role, *args, **kwargs):
        if user_role != "admin":
            raise PermissionError(f"❌ {user_role}는 이 함수를 실행할 수 없습니다")
        print(f"  ✓ {user_role}님이 {func.__name__}을 실행합니다")
        return func(*args, **kwargs)
    return wrapper

@require_admin
def delete_database():
    """데이터베이스를 삭제하는 위험한 함수"""
    return "데이터베이스 삭제 완료"

try:
    delete_database("user")
except PermissionError as e:
    print(f"  {e}")

result = delete_database("admin")
print(f"  결과: {result}")


# 데코레이터 2: 결과 캐싱
print("\n【 데코레이터 2: 결과 캐싱 (메모이제이션) 】")

def cache_result(func):
    """함수의 결과를 캐시하는 데코레이터"""
    cached_results = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))

        if key in cached_results:
            print(f"  💾 캐시에서 로드: {key}")
            return cached_results[key]

        print(f"  🔄 새로 계산 중: {key}")
        result = func(*args, **kwargs)
        cached_results[key] = result

        return result

    return wrapper

@cache_result
def fibonacci(n):
    """피보나치 수열 (재귀)"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print("첫 번째 호출:")
fib1 = fibonacci(5)
print(f"fibonacci(5) = {fib1}")

print("\n두 번째 호출 (캐시 사용):")
fib2 = fibonacci(5)
print(f"fibonacci(5) = {fib2}")


# 데코레이터 3: 반복 재시도
print("\n【 데코레이터 3: 반복 재시도 (Retry) 】")

def retry_on_failure(max_attempts=3):
    """실패하면 다시 시도하는 데코레이터"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"  시도 {attempt}/{max_attempts}")
                    result = func(*args, **kwargs)
                    print(f"  ✓ 성공!")
                    return result
                except Exception as e:
                    if attempt == max_attempts:
                        print(f"  ✗ {max_attempts}회 시도 모두 실패")
                        raise
                    print(f"  ⚠️  실패: {e} (재시도...)")
        return wrapper
    return decorator

@retry_on_failure(max_attempts=3)
def unstable_network_call(attempt_counter=[0]):
    """불안정한 네트워크 호출 시뮬레이션"""
    attempt_counter[0] += 1
    if attempt_counter[0] < 3:
        raise ConnectionError("네트워크 오류")
    return "성공적으로 데이터 수신"

try:
    result = unstable_network_call()
    print(f"최종 결과: {result}")
except ConnectionError:
    print("네트워크 오류 처리")


# ═══════════════════════════════════════════════════════════════════════════════
# 🧪 Part 6: 데코레이터 체이닝 (여러 데코레이터 조합)
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║             🧪 Part 6: 데코레이터 체이닝 — 여러 데코레이터 조합               ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

def logger(func):
    """실행 로그를 출력하는 데코레이터"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"    📋 로그: {func.__name__} 실행")
        return func(*args, **kwargs)
    return wrapper

def timer(func):
    """실행 시간을 측정하는 데코레이터"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"    ⏱️  시간: {elapsed:.4f}초")
        return result
    return wrapper

print("\n【 여러 데코레이터 조합 】")

@logger
@timer
def combined_function(n):
    """로그와 시간 측정을 동시에 하는 함수"""
    total = sum(range(n))
    return total

result = combined_function(10000)
print(f"    결과: {result}")


# ═══════════════════════════════════════════════════════════════════════════════
# 📊 Part 7: 실전 프로젝트 — 성능 모니터링 시스템
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║              📊 Part 7: 실전 프로젝트 — 성능 모니터링 시스템                  ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

class PerformanceMonitor:
    """함수의 성능을 모니터링하고 기록하는 클래스"""

    def __init__(self):
        self.metrics = {}

    def monitor(self, func):
        """함수의 성능을 추적하는 데코레이터"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if func.__name__ not in self.metrics:
                self.metrics[func.__name__] = {
                    "calls": 0,
                    "total_time": 0,
                    "errors": 0
                }

            start = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start

                self.metrics[func.__name__]["calls"] += 1
                self.metrics[func.__name__]["total_time"] += elapsed

                return result
            except Exception as e:
                self.metrics[func.__name__]["errors"] += 1
                raise

        return wrapper

    def report(self):
        """모든 함수의 성능 리포트 출력"""
        print("\n  【 성능 모니터링 리포트 】")
        print(f"  {'함수명':<20} {'호출':<8} {'총시간':<12} {'평균':<12} {'에러':<8}")
        print("  " + "─" * 60)

        for func_name, metrics in self.metrics.items():
            calls = metrics["calls"]
            total_time = metrics["total_time"]
            avg_time = total_time / calls if calls > 0 else 0
            errors = metrics["errors"]

            print(f"  {func_name:<20} {calls:<8} {total_time:<12.4f} {avg_time:<12.6f} {errors:<8}")


# 사용 예제
print("\n【 예제: 3개의 함수 모니터링 】")

monitor = PerformanceMonitor()

@monitor.monitor
def task_a():
    time.sleep(0.1)
    return "Task A"

@monitor.monitor
def task_b():
    time.sleep(0.2)
    return "Task B"

@monitor.monitor
def task_c():
    time.sleep(0.05)
    return "Task C"

print("  작업 실행 중...")
task_a()
task_b()
task_c()
task_a()

monitor.report()


# ═══════════════════════════════════════════════════════════════════════════════
# ✅ Part 8: 최종 테스트 및 검증
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                   ✅ Part 8: 최종 테스트 및 검증                              ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

test_results = []

# Test 1: gogs_logger가 제대로 작동하는가?
print("\n【 Test 1: gogs_logger 데코레이터 검증 】")
try:
    @gogs_logger
    def test_func(x, y):
        return x + y

    result = test_func(5, 10)
    assert result == 15, "계산 결과가 잘못됨"
    test_results.append(("Test 1: gogs_logger", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 1: gogs_logger", False))
    print(f"  ✗ FAIL: {e}")


# Test 2: 데코레이터가 원본 함수의 이름을 보존하는가?
print("\n【 Test 2: 함수 메타데이터 보존 (@functools.wraps) 】")
try:
    @gogs_logger
    def named_function():
        """이 함수는 문서화되어 있습니다"""
        pass

    assert named_function.__name__ == "named_function", "함수 이름이 변함"
    assert "문서화" in named_function.__doc__, "함수 문서가 변함"
    test_results.append(("Test 2: 메타데이터 보존", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 2: 메타데이터 보존", False))
    print(f"  ✗ FAIL: {e}")


# Test 3: 캐싱이 제대로 작동하는가?
print("\n【 Test 3: 캐싱 데코레이터 검증 】")
try:
    call_count = [0]

    @cache_result
    def cached_func(x):
        call_count[0] += 1
        return x * 2

    # 첫 호출
    result1 = cached_func(5)
    # 두 번째 호출 (캐시)
    result2 = cached_func(5)

    assert result1 == 10, "계산 결과 오류"
    assert result2 == 10, "캐시 결과 오류"
    assert call_count[0] == 1, "캐싱이 작동하지 않음"
    test_results.append(("Test 3: 캐싱 데코레이터", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 3: 캐싱 데코레이터", False))
    print(f"  ✗ FAIL: {e}")


# Test 4: 데코레이터 체이닝이 작동하는가?
print("\n【 Test 4: 데코레이터 체이닝 검증 】")
try:
    execution_order = []

    def first_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            execution_order.append("first_start")
            result = func(*args, **kwargs)
            execution_order.append("first_end")
            return result
        return wrapper

    def second_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            execution_order.append("second_start")
            result = func(*args, **kwargs)
            execution_order.append("second_end")
            return result
        return wrapper

    @first_decorator
    @second_decorator
    def chained_func():
        execution_order.append("main")

    chained_func()

    expected_order = ["first_start", "second_start", "main", "second_end", "first_end"]
    assert execution_order == expected_order, f"순서 오류: {execution_order}"
    test_results.append(("Test 4: 데코레이터 체이닝", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 4: 데코레이터 체이닝", False))
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
║              🎓 Python 대학교 1학년 v3.1 완료 축하합니다!                     ║
╚════════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 v3.1에서 배운 것:

   ✓ 일급 객체 (First-class Object)
     함수는 변수에 담을 수 있고, 인자로 전달하고, 반환값이 될 수 있습니다.

   ✓ 기초 데코레이터
     함수를 감싸는(Wrap) 함수로 기능을 확장합니다.

   ✓ 데코레이터 @구문
     @gogs_logger 한 줄로 모든 함수에 기능을 주입합니다.

   ✓ *args, **kwargs
     어떤 함수에도 적용할 수 있는 범용 데코레이터를 만듭니다.

   ✓ 고급 패턴들
     권한 확인, 캐싱, 재시도, 모니터링

   ✓ 데코레이터 체이닝
     여러 데코레이터를 조합해서 복잡한 기능을 구성합니다.

   ✓ 대학 철학: DRY & AOP
     중복을 제거하고 관점을 분리합니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 핵심 정리:

   "기존 코드를 건드리지 않고 기능을 확장한다"

   고등학교: 함수를 수정해서 기능을 추가
   대학:     데코레이터로 함수를 감싸서 기능을 추가 (원본 불변!)

   이것이 "우아한 설계"입니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 다음: [v3.2: 제너레이터(Generator) — 메모리를 아끼는 효율적 루프]

   데코레이터로 "코드의 구조"를 우아하게 설계했다면,
   제너레이터로 "메모리 효율"을 극대화합니다.

   수억 개의 데이터를 처리해도 메모리가 터지지 않게 설계하는 비법!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

질문: 다음 전공 수업으로 진행하시겠습니까?

저장 필수 너는 기록이 증명이다 gogs
╚════════════════════════════════════════════════════════════════════════════════╝
""")
