# Week 1-2: Python 기초 및 객체지향 프로그래밍
## From Rust Type Safety to Python Dynamic Flexibility

**기간:** 2026-02-23 ~ 2026-03-08 (2주)
**목표:** Python 기초 완전 숙달 + Rust와의 비교 학습
**철학:** "정적 타입의 안전성 vs 동적 타입의 유연성"

---

## 📚 학습 로드맵

### Day 1-2: 기본 문법 (Basic Syntax)

```python
# 1. 변수와 데이터 타입
print("="*50)
print("Day 1-2: 기본 문법")
print("="*50)

# Rust vs Python 비교
"""
Rust:
  let x: i32 = 10;  // 타입 명시
  let s = String::from("hello");  // 소유권 명시

Python:
  x = 10  # 타입 추론
  s = "hello"  # 동적 타입
"""

# Python 변수 할당
x = 10
y = 3.14
s = "hello"
is_true = True

print(f"정수: {x} (타입: {type(x).__name__})")
print(f"실수: {y} (타입: {type(y).__name__})")
print(f"문자열: {s} (타입: {type(s).__name__})")
print(f"불린: {is_true} (타입: {type(is_true).__name__})")

# 2. 연산자
print("\n연산자:")
print(f"10 + 3 = {10 + 3}")
print(f"10 - 3 = {10 - 3}")
print(f"10 * 3 = {10 * 3}")
print(f"10 / 3 = {10 / 3}")
print(f"10 // 3 = {10 // 3}")  # 정수 나눗셈
print(f"10 % 3 = {10 % 3}")   # 나머지
print(f"2 ** 3 = {2 ** 3}")    # 지수

# 3. 제어문
print("\nif-else:")
age = 25

if age >= 18:
    print("성인입니다")
else:
    print("미성년자입니다")

print("\nfor 루프:")
for i in range(5):
    print(f"i = {i}")

print("\nwhile 루프:")
count = 0
while count < 3:
    print(f"count = {count}")
    count += 1
```

**평가:** 기본 문법 퀴즈 (5개 문제)

---

### Day 3-4: 자료구조 (Data Structures)

```python
print("\n" + "="*50)
print("Day 3-4: 자료구조")
print("="*50)

# 1. 리스트 (List)
print("\n리스트 (가변, 순서 있음):")
numbers = [1, 2, 3, 4, 5]
print(f"리스트: {numbers}")
print(f"첫 번째 요소: {numbers[0]}")
print(f"마지막 요소: {numbers[-1]}")
print(f"슬라이싱: {numbers[1:4]}")

numbers.append(6)
print(f"append(6): {numbers}")

numbers.pop()
print(f"pop(): {numbers}")

# 2. 튜플 (Tuple)
print("\n튜플 (불변, 순서 있음):")
coords = (10, 20, 30)
print(f"튜플: {coords}")
print(f"언팩킹: x, y, z = {coords}")
x, y, z = coords
print(f"x={x}, y={y}, z={z}")

# 3. 딕셔너리 (Dictionary)
print("\n딕셔너리 (키-값 맵):")
person = {
    "name": "Alice",
    "age": 25,
    "city": "Seoul"
}
print(f"딕셔너리: {person}")
print(f"person['name']: {person['name']}")
print(f"person.get('age'): {person.get('age')}")

person['job'] = "Engineer"
print(f"추가 후: {person}")

# 4. 세트 (Set)
print("\n세트 (중복 없음):")
unique_nums = {1, 2, 3, 2, 1}
print(f"세트: {unique_nums}")  # {1, 2, 3}

# 5. 리스트 컴프리헨션
print("\n리스트 컴프리헨션:")
squares = [x**2 for x in range(5)]
print(f"제곱수: {squares}")

evens = [x for x in range(10) if x % 2 == 0]
print(f"짝수: {evens}")

# 6. 딕셔너리 컴프리헨션
print("\n딕셔너리 컴프리헨션:")
square_dict = {x: x**2 for x in range(5)}
print(f"제곱 딕셔너리: {square_dict}")
```

**평가:** 자료구조 실습 (간단한 계산기)

---

### Day 5-7: 함수와 객체지향 (Functions & OOP)

```python
print("\n" + "="*50)
print("Day 5-7: 함수와 객체지향")
print("="*50)

# 1. 함수 정의
def greet(name, greeting="안녕"):
    """인사 함수"""
    return f"{greeting}, {name}!"

print(greet("Alice"))
print(greet("Bob", "Hi"))

# 2. *args, **kwargs
def sum_all(*args):
    """가변 인자"""
    return sum(args)

print(f"sum_all(1, 2, 3, 4): {sum_all(1, 2, 3, 4)}")

def print_info(**kwargs):
    """키워드 인자"""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="Seoul")

# 3. 클래스 (Class) - OOP의 핵심
print("\n클래스 (객체지향):")

class NeuralSignal:
    """신경신호 클래스"""

    def __init__(self, voltage: float, frequency: int, amplitude: float):
        """초기화"""
        self.voltage = voltage
        self.frequency = frequency
        self.amplitude = amplitude

    def is_firing(self) -> bool:
        """발화 여부 확인"""
        return self.voltage > -30.0

    def extract_information(self) -> float:
        """정보량 추출"""
        return self.frequency * self.amplitude

    def __str__(self) -> str:
        """문자열 표현"""
        return f"Signal(V={self.voltage}mV, F={self.frequency}Hz, A={self.amplitude})"

# 객체 생성
signal = NeuralSignal(voltage=-20.0, frequency=50, amplitude=0.8)
print(f"신호: {signal}")
print(f"발화 중: {signal.is_firing()}")
print(f"정보량: {signal.extract_information()}")

# 4. 상속 (Inheritance)
print("\n상속:")

class GogsIntent:
    """Gogs 의도 기본 클래스"""

    def __init__(self, operation: str):
        self.operation = operation

    def execute(self):
        print(f"실행: {self.operation}")

class ComputeIntent(GogsIntent):
    """계산 의도"""

    def __init__(self, operation: str, operand1: float, operand2: float):
        super().__init__(operation)
        self.operand1 = operand1
        self.operand2 = operand2

    def execute(self):
        """오버라이드"""
        print(f"계산: {self.operand1} {self.operation} {self.operand2}")

class LearnIntent(GogsIntent):
    """학습 의도"""

    def __init__(self, pattern: list, feedback: float):
        super().__init__("LEARN")
        self.pattern = pattern
        self.feedback = feedback

    def execute(self):
        print(f"학습: 패턴 {self.pattern}, 피드백 {self.feedback}")

# 상속된 객체 사용
compute = ComputeIntent("+", 10, 5)
compute.execute()

learn = LearnIntent([1, 0, 1, 1, 0, 1], 0.9)
learn.execute()

# 5. 데코레이터 (Decorator)
print("\n데코레이터:")

def timer_decorator(func):
    """실행 시간 측정 데코레이터"""
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"실행 시간: {end - start:.6f}초")
        return result
    return wrapper

@timer_decorator
def slow_function():
    """느린 함수"""
    total = 0
    for i in range(1000000):
        total += i
    return total

slow_function()

# 6. 매직 메서드 (Magic Methods)
print("\n매직 메서드:")

class Vector:
    """벡터 클래스"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        """덧셈 오버로드"""
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        """문자열 표현"""
        return f"Vector({self.x}, {self.y})"

    def __len__(self):
        """길이 (크기)"""
        return (self.x**2 + self.y**2)**0.5

v1 = Vector(3, 4)
v2 = Vector(1, 2)
v3 = v1 + v2

print(f"v1: {v1}")
print(f"v2: {v2}")
print(f"v1 + v2: {v3}")
print(f"||v1||: {len(v1)}")
```

**평가:** 신경신호 처리 클래스 구현

---

## 🎯 Week 1-2 프로젝트

### 프로젝트: Simple Neural Signal Processor

```python
"""
목표:
1. NeuralSignal 클래스 구현
   - voltage, frequency, amplitude 속성
   - is_firing(), extract_information() 메서드

2. SynapticHandler 클래스 구현
   - 신호를 GogsIntent로 변환
   - 주파수 기반 명령어 매핑

3. SimpleNeuralNetwork 클래스 구현
   - 간단한 신경망 (입력층, 은닉층, 출력층)
   - forward() 메서드로 신호 처리

요구사항:
- 타입 힌팅 사용
- 클래스 상속 활용
- 리스트/딕셔너리 컴프리헨션 사용
- 데코레이터로 로깅 구현
"""
```

---

## ✅ 평가 기준

| 항목 | 점수 | 기준 |
|------|------|------|
| 문법 이해 | 20점 | 기본 문법 정확성 |
| 자료구조 | 20점 | 적절한 자료구조 선택 |
| 함수/클래스 | 30점 | OOP 설계 및 구현 |
| 프로젝트 | 30점 | 기능 완성도 |

**총점: 100점 / 합격선: 70점**

---

## 📖 참고 자료

- Python 공식 문서: https://docs.python.org/3/
- 타입 힌팅 가이드: https://docs.python.org/3/library/typing.html
- PEP 8 스타일 가이드: https://www.python.org/dev/peps/pep-0008/

---

## 🚀 다음 주 준비

Week 3-4에서는:
- 함수형 프로그래밍 (lambda, map, filter)
- 고급 타입 힌팅
- 에러 처리 및 로깅

기록이 증명이다 gogs. 👑
