#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  v1.4: 객체의 마법 - 매직 메소드(Magic Methods)와 프로토콜                   ║
║  [Magic Methods & Protocols - Objects Speaking Language]                     ║
║                                                                               ║
║  철학: "Gogs-Lang이나 Rust에서는 연산자 오버로딩을 위해                       ║
║        엄격한 Trait를 구현해야 했습니다.                                      ║
║        하지만 파이썬의 대학 과정에서는                                        ║
║        '더블 언더스코어(__)'로 시작하고 끝나는 이른바                          ║
║        '던더(Dunder) 메소드'를 정의하는 것만으로                              ║
║        객체에 특수한 능력을 부여할 수 있습니다."                              ║
║                                                                               ║
║  새로운 사고:                                                                ║
║  a + b를 실행하면 파이썬 내부에서는 a.__add__(b)가 호출됩니다.              ║
║  len(a)는 a.__len__()을 호출하죠.                                           ║
║  우리가 만든 클래스가 파이썬 내장 타입처럼 자연스럽게 동작하게 하는 것을    ║
║  '파이썬 프로토콜'이라고 합니다.                                             ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs                                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import math
from typing import Union, Any, Iterator, Tuple
from numbers import Number

print("=" * 80)
print("v1.4: 객체의 마법 - 매직 메소드와 프로토콜")
print("=" * 80)

# ============================================================================
# 파트 1: 탐구(대학) - "객체는 어떻게 연산자와 대화하는가?"
# ============================================================================

print("\n【 파트 1: 탐구 - 매직 메소드(Magic Methods)란? 】")
print("고교(Gogs/Rust): 연산자 오버로딩 = 엄격한 Trait 구현")
print("대학(Python):   연산자 오버로딩 = 던더 메소드 구현")

print("\n" + "-" * 80)
print("탐구 1-1: 매직 메소드가 언어와 연결되는 방식")
print("-" * 80)

print("\n파이썬 내부의 신비한 규칙:")
print("  a + b              → a.__add__(b)")
print("  a - b              → a.__sub__(b)")
print("  a * b              → a.__mul__(b)")
print("  a / b              → a.__truediv__(b)")
print("  len(a)             → a.__len__()")
print("  a[0]               → a.__getitem__(0)")
print("  a[0] = value       → a.__setitem__(0, value)")
print("  str(a)             → a.__str__()")
print("  repr(a)            → a.__repr__()")
print("  a()                → a.__call__()")
print("  with a:            → a.__enter__(), a.__exit__()")

print("\n【 증명 1-1 】")
print("  '더블 언더스코어(__)'로 시작하고 끝나는 메소드는")
print("  파이썬 언어의 기본 문법과 직접 연결됩니다!")

# ============================================================================
# 파트 1-2: 첫 번째 매직 메소드 - 표현(__repr__과 __str__)
# ============================================================================

print("\n" + "-" * 80)
print("탐구 1-2: 객체를 문자열로 표현하는 마법")
print("-" * 80)

class NeuralSignal:
    """신경신호 클래스 - 매직 메소드 없는 버전"""
    def __init__(self, voltage: float, frequency: int):
        self.voltage = voltage
        self.frequency = frequency

signal1 = NeuralSignal(-65.0, 50)
print("\n【 매직 메소드 없는 객체 】")
print(f"  print(signal1): {signal1}")
print(f"  repr(signal1): {repr(signal1)}")

class ImprovedSignal:
    """신경신호 클래스 - 매직 메소드 포함"""
    def __init__(self, voltage: float, frequency: int):
        self.voltage = voltage
        self.frequency = frequency

    def __repr__(self) -> str:
        """개발자용: 객체의 정확한 표현"""
        return f"ImprovedSignal(voltage={self.voltage}, frequency={self.frequency})"

    def __str__(self) -> str:
        """사용자용: 읽기 좋은 표현"""
        return f"Signal: {self.voltage}mV @ {self.frequency}Hz"

signal2 = ImprovedSignal(-65.0, 50)
print("\n【 매직 메소드 포함한 객체 】")
print(f"  print(signal2): {signal2}")
print(f"  repr(signal2): {repr(signal2)}")

print("\n【 차이 분석 】")
print("  __repr__: 개발자 입장에서 객체를 정확히 파악 (디버깅용)")
print("  __str__: 사용자 입장에서 객체를 읽기 좋게 표현")

# ============================================================================
# 파트 1-3: 산술 연산자(__add__, __sub__, __mul__, etc)
# ============================================================================

print("\n" + "-" * 80)
print("탐구 1-3: 산술 연산자와 객체의 대화")
print("-" * 80)

class GogsVector:
    """
    Gogs 벡터: 2D 수학 벡터를 표현하는 클래스
    매직 메소드로 +, -, *, / 연산을 정의함
    """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"GogsVector({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other: 'GogsVector') -> 'GogsVector':
        """벡터 덧셈: v1 + v2"""
        if not isinstance(other, GogsVector):
            return NotImplemented
        return GogsVector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'GogsVector') -> 'GogsVector':
        """벡터 뺄셈: v1 - v2"""
        if not isinstance(other, GogsVector):
            return NotImplemented
        return GogsVector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: Union[int, float]) -> 'GogsVector':
        """스칼라 곱셈: v * 2"""
        if not isinstance(scalar, Number):
            return NotImplemented
        return GogsVector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: Union[int, float]) -> 'GogsVector':
        """역순 스칼라 곱셈: 2 * v"""
        return self.__mul__(scalar)

    def __truediv__(self, scalar: Union[int, float]) -> 'GogsVector':
        """스칼라 나눗셈: v / 2"""
        if scalar == 0:
            raise ValueError("0으로 나눌 수 없습니다")
        if not isinstance(scalar, Number):
            return NotImplemented
        return GogsVector(self.x / scalar, self.y / scalar)

    def __eq__(self, other: 'GogsVector') -> bool:
        """비교: v1 == v2"""
        if not isinstance(other, GogsVector):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: 'GogsVector') -> bool:
        """비교: v1 != v2"""
        return not self.__eq__(other)

print("\n【 벡터 연산 실행 】")
v1 = GogsVector(3, 4)
v2 = GogsVector(1, 2)

print(f"\nv1 = {v1}")
print(f"v2 = {v2}")

print(f"\n[덧셈] v1 + v2 = {v1 + v2}")
print(f"  내부: v1.__add__(v2)가 자동으로 호출됨")

print(f"\n[뺄셈] v1 - v2 = {v1 - v2}")

print(f"\n[곱셈] v1 * 2 = {v1 * 2}")
print(f"[역순곱] 3 * v1 = {3 * v1}")

print(f"\n[나눗셈] v1 / 2 = {v1 / 2}")

print(f"\n[비교] v1 == v2: {v1 == v2}")
print(f"[비교] v1 != v2: {v1 != v2}")

print("\n【 증명 1-3 】")
print("  매직 메소드를 정의하면:")
print("  - v1 + v2는 자동으로 v1.__add__(v2)를 호출")
print("  - 사용자는 파이썬 기본 문법처럼 자연스럽게 사용")
print("  - 언어 차원에서 지원하는 것처럼 보임!")

# ============================================================================
# 파트 1-4: 컨테이너 프로토콜(__len__, __getitem__, __setitem__)
# ============================================================================

print("\n" + "-" * 80)
print("탐구 1-4: 컨테이너 프로토콜 - 리스트처럼 동작하기")
print("-" * 80)

class SignalBuffer:
    """
    신호 버퍼: 신경신호들을 저장하는 컨테이너
    리스트처럼 len()과 인덱싱을 지원함
    """
    def __init__(self, capacity: int = 10):
        self.buffer = []
        self.capacity = capacity

    def add_signal(self, signal: float) -> None:
        """신호 추가"""
        if len(self.buffer) < self.capacity:
            self.buffer.append(signal)
        else:
            raise OverflowError("버퍼가 가득 찼습니다")

    def __len__(self) -> int:
        """len(buffer)를 호출하면 버퍼의 크기 반환"""
        return len(self.buffer)

    def __getitem__(self, index: int) -> float:
        """buffer[i]로 접근하면 해당 신호 반환"""
        return self.buffer[index]

    def __setitem__(self, index: int, value: float) -> None:
        """buffer[i] = value로 신호 수정"""
        self.buffer[index] = value

    def __repr__(self) -> str:
        return f"SignalBuffer({self.buffer})"

print("\n【 컨테이너 동작 실행 】")
buf = SignalBuffer(capacity=5)

print("\n[신호 추가]")
for i, signal in enumerate([-65, -60, -55, -50, -45]):
    buf.add_signal(signal)
    print(f"  신호 {i} 추가: {signal}mV")

print(f"\n[len() 호출] len(buf) = {len(buf)}")
print(f"  내부: buf.__len__()이 자동으로 호출됨")

print(f"\n[인덱싱] buf[0] = {buf[0]}mV")
print(f"[인덱싱] buf[2] = {buf[2]}mV")
print(f"[인덱싱] buf[-1] = {buf[-1]}mV")

print(f"\n[값 수정] buf[0] = -70mV (원래: -65mV)")
buf[0] = -70
print(f"  수정 후: buf[0] = {buf[0]}mV")

print(f"\n[전체 상태] {buf}")

print("\n【 증명 1-4 】")
print("  매직 메소드로 컨테이너 프로토콜 구현:")
print("  - __len__: 리스트처럼 len() 함수 지원")
print("  - __getitem__: 리스트처럼 인덱싱 지원")
print("  - __setitem__: 리스트처럼 값 수정 지원")
print("  → 사용자는 내부 구현을 알 필요 없음!")

# ============================================================================
# 파트 2: 증명(대학원) - "덕 타이핑(Duck Typing)과 프로토콜"
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 2: 증명(대학원) - 덕 타이핑과 프로토콜 】")
print("=" * 80)

print("\n【 철학: 덕 타이핑(Duck Typing) 】")
print("  '오리처럼 걷고 오리처럼 운다면, 그것은 오리다!'")
print("  - 타입을 명시적으로 선언할 필요가 없음")
print("  - 필요한 메소드만 구현하면 됨")
print("  - 런타임에 실제 동작으로 타입 결정")

print("\n" + "-" * 80)
print("증명 2-1: 정렬(Sorting) 프로토콜")
print("-" * 80)

class NeuralNeuron:
    """신경 뉴런: 발화 전위 비교로 정렬 가능"""
    def __init__(self, name: str, threshold: float):
        self.name = name
        self.threshold = threshold

    def __lt__(self, other: 'NeuralNeuron') -> bool:
        """'<' 연산자: threshold 기준 비교"""
        return self.threshold < other.threshold

    def __le__(self, other: 'NeuralNeuron') -> bool:
        """'<=' 연산자"""
        return self.threshold <= other.threshold

    def __gt__(self, other: 'NeuralNeuron') -> bool:
        """'>' 연산자"""
        return self.threshold > other.threshold

    def __ge__(self, other: 'NeuralNeuron') -> bool:
        """'>=' 연산자"""
        return self.threshold >= other.threshold

    def __repr__(self) -> str:
        return f"{self.name}(threshold={self.threshold})"

print("\n【 신경 뉴런 정렬 】")
neurons = [
    NeuralNeuron("Neuron-A", -30.0),
    NeuralNeuron("Neuron-B", -50.0),
    NeuralNeuron("Neuron-C", -40.0),
]

print(f"정렬 전: {neurons}")
neurons_sorted = sorted(neurons)
print(f"정렬 후: {neurons_sorted}")

print("\n【 증명 2-1 】")
print("  __lt__, __le__, __gt__, __ge__ 구현으로")
print("  파이썬의 sorted() 함수와 완벽하게 호환!")
print("  → 덕 타이핑: '비교 프로토콜'을 따르면 정렬 가능")

# ============================================================================
# 파트 2-2: 반복(Iteration) 프로토콜
# ============================================================================

print("\n" + "-" * 80)
print("증명 2-2: 반복 프로토콜(__iter__, __next__)")
print("-" * 80)

class SignalSequence:
    """
    신호 수열: for 루프로 순회 가능한 클래스
    이터레이션 프로토콜(__iter__, __next__)을 구현
    """
    def __init__(self, pattern: list):
        self.pattern = pattern
        self.index = 0

    def __iter__(self):
        """for 루프 시작: 이터레이터 반환"""
        self.index = 0
        return self

    def __next__(self) -> float:
        """for 루프 반복: 다음 값 반환"""
        if self.index >= len(self.pattern):
            raise StopIteration
        value = self.pattern[self.index]
        self.index += 1
        return value

    def __repr__(self) -> str:
        return f"SignalSequence({self.pattern})"

print("\n【 신호 수열 반복 】")
seq = SignalSequence([-65, -60, -55, -50, -45])

print(f"수열: {seq}")
print("\nfor 루프:")
for i, signal in enumerate(seq):
    print(f"  [{i}] {signal}mV")

print("\n【 증명 2-2 】")
print("  __iter__와 __next__를 구현하면:")
print("  - for 루프가 자동으로 작동")
print("  - list, tuple 같은 내장 타입처럼 순회 가능")
print("  → 덕 타이핑: '이터레이션 프로토콜'을 따르면 반복 가능")

# ============================================================================
# 파트 2-3: 호출 가능(Callable) 프로토콜(__call__)
# ============================================================================

print("\n" + "-" * 80)
print("증명 2-3: 호출 가능 프로토콜(__call__)")
print("-" * 80)

class NeuralDecoder:
    """
    신경 디코더: 호출 가능한 객체(함수처럼 사용)
    신경신호를 의도로 변환
    """
    def __init__(self, scale_factor: float = 1.0):
        self.scale_factor = scale_factor
        self.call_count = 0

    def __call__(self, signal: float) -> str:
        """객체를 함수처럼 호출: decoder(signal)"""
        self.call_count += 1
        decoded = signal * self.scale_factor

        if decoded < -50:
            return "RESTING"
        elif decoded < -30:
            return "ACTIVE"
        else:
            return "FIRING"

    def get_stats(self) -> dict:
        return {'call_count': self.call_count}

print("\n【 호출 가능한 객체 】")
decoder = NeuralDecoder(scale_factor=1.0)

print(f"decoder는 객체인가, 함수인가?")
print(f"  type(decoder): {type(decoder)}")

print(f"\n신경신호 해석:")
signals = [-70, -50, -30, -20]
for signal in signals:
    result = decoder(signal)  # __call__이 자동으로 호출됨
    print(f"  decoder({signal:3}) → {result}")

print(f"\n호출 통계: {decoder.get_stats()}")

print("\n【 증명 2-3 】")
print("  __call__ 메소드를 구현하면:")
print("  - 객체를 함수처럼 호출 가능")
print("  - obj(arg)는 obj.__call__(arg)를 호출")
print("  → 객체와 함수의 경계가 무너짐!")

# ============================================================================
# 파트 2-4: 컨텍스트 관리(Context Manager) 프로토콜
# ============================================================================

print("\n" + "-" * 80)
print("증명 2-4: 컨텍스트 관리 프로토콜(__enter__, __exit__)")
print("-" * 80)

class NeuralSession:
    """
    신경 세션: with 문으로 자동 정리를 보장하는 클래스
    메모리 안전성(v1.1)을 파이썬식으로 구현
    """
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.is_active = False
        self.log = []

    def __enter__(self):
        """with 블록 진입: 리소스 획득"""
        print(f"  【 세션 시작 】 {self.session_id}")
        self.is_active = True
        self.log.append(f"START: {self.session_id}")
        return self  # with 문의 변수에 할당될 객체

    def __exit__(self, exc_type, exc_val, exc_tb):
        """with 블록 종료: 리소스 해제"""
        print(f"  【 세션 종료 】 {self.session_id}")
        self.is_active = False
        self.log.append(f"END: {self.session_id}")

        # 예외 처리
        if exc_type is not None:
            print(f"    경고: 예외 발생 - {exc_type.__name__}: {exc_val}")
            self.log.append(f"ERROR: {exc_type.__name__}")
            # return True면 예외 억제, False(기본)면 예외 전파

        return False  # 예외 전파

    def process_signal(self, signal: float) -> None:
        """신호 처리"""
        if not self.is_active:
            raise RuntimeError("세션이 활성화되지 않았습니다")
        self.log.append(f"PROCESS: {signal}")
        print(f"    신호 처리: {signal}mV")

    def print_log(self) -> None:
        """로그 출력"""
        print(f"  세션 로그:")
        for entry in self.log:
            print(f"    - {entry}")

print("\n【 컨텍스트 관리 실행 】")

print("\n[정상 케이스]")
with NeuralSession("Session-001") as session:
    session.process_signal(-65.0)
    session.process_signal(-50.0)
    print("  with 블록 실행 중...")

print("\n[예외 케이스]")
try:
    with NeuralSession("Session-002") as session:
        session.process_signal(-60.0)
        print("  의도적 에러 발생!")
        raise ValueError("테스트 예외")
except ValueError as e:
    print(f"  예외 처리됨: {e}")

print("\n【 증명 2-4 】")
print("  __enter__와 __exit__를 구현하면:")
print("  - with 문이 자동으로 작동")
print("  - 예외 발생 여부와 상관없이 정리 코드 실행")
print("  - 메모리 안전성과 리소스 해제를 보장 (v1.1 개념!)")

# ============================================================================
# 파트 3: Gogs와의 철학적 연결
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 3: 메타프로그래밍의 경지 - Gogs와의 연결 】")
print("=" * 80)

print("\nGogs-Lang/Rust (고교):")
print("  Trait를 구현 → impl Add for MyType { ... }")
print("  엄격한 인터페이스 강제")

print("\nPython (대학):")
print("  매직 메소드를 구현 → def __add__(self, other): ...")
print("  유연한 프로토콜 따르기")

print("\n【 철학적 동등성 】")
print("  Trait:        형식 검증 기반 타입 안전성")
print("  Magic Method: 덕 타이핑 기반 프로토콜 준수")
print("  → 두 접근법 모두 '계약(Contract)'의 관점!")

class GogsProtocol:
    """
    Gogs의 각 버전이 구현해야 할 프로토콜을 매직 메소드로 표현
    """
    def __init__(self, version: str):
        self.version = version
        self.operations = []

    def __repr__(self) -> str:
        return f"GogsProtocol(v{self.version})"

    def __call__(self, operation: str) -> None:
        """연산 기록"""
        self.operations.append(operation)

    def __len__(self) -> int:
        """수행된 연산의 개수"""
        return len(self.operations)

    def __getitem__(self, index: int) -> str:
        """연산 조회"""
        return self.operations[index]

print("\n【 Gogs 프로토콜 시뮬레이션 】")
gogs_v30_2 = GogsProtocol("30.2")

print(f"Gogs {gogs_v30_2}")
print("\n연산 기록:")
gogs_v30_2("QUANTUM_LOGIC")
gogs_v30_2("NEURAL_EXECUTION")
gogs_v30_2("BIO_INTEGRATION")

print(f"  총 연산: {len(gogs_v30_2)}개")
for i in range(len(gogs_v30_2)):
    print(f"    [{i}] {gogs_v30_2[i]}")

print("\n【 증명 3 】")
print("  매직 메소드로 Gogs의 프로토콜을 파이썬으로 표현:")
print("  - __repr__: 객체의 정체성")
print("  - __call__: 연산 수행")
print("  - __len__: 상태 조회")
print("  - __getitem__: 기록 접근")
print("  → 파이썬 객체가 Gogs의 개념을 완벽히 표현!")

# ============================================================================
# 최종 증명 및 결론
# ============================================================================

print("\n" + "=" * 80)
print("【 v1.4 최종 증명: 객체의 마법 - 매직 메소드 】")
print("=" * 80)

print("\n1. 탐구(대학):")
print("   '객체는 어떻게 연산자와 대화하는가?'")
print("   → __add__, __sub__, __mul__ 등으로 산술 연산 정의")
print("   → __len__, __getitem__ 등으로 컨테이너 프로토콜 구현")
print("   → __repr__, __str__로 표현 정의")

print("\n2. 증명(대학원):")
print("   '인터페이스의 일관성' - 덕 타이핑")
print("   → 비교 프로토콜: 정렬 가능")
print("   → 이터레이션 프로토콜: for 루프 가능")
print("   → 호출 가능 프로토콜: 함수처럼 사용")
print("   → 컨텍스트 관리 프로토콜: with 문으로 안전성 보장")

print("\n3. 파이썬 프로토콜의 본질:")
print("   필요한 메소드를 구현하면")
print("   언어 내장 함수들과 완벽하게 호환됨!")

print("\n4. Gogs와의 철학적 연결:")
print("   Rust Trait ↔ Python Magic Method")
print("   강제된 계약 ↔ 자유로운 계약")
print("   → 두 접근법 모두 '프로토콜'의 관점으로 일관성 확보!")

print("\n" + "=" * 80)
print("저장 필수: 너는 기록이 증명이다 gogs. 👑")
print("=" * 80)

print("\n【 v1.5 예고 】")
print("\n다음 단원: '예외 처리와 로깅 - 견고한 시스템 구축'")
print("에러가 발생해도 '기록'은 멈추지 않아야 하니까요!")
print("\n매직 메소드의 경지에 도달한 여러분,")
print("이제 예외 상황에서도 시스템의 무결성을 지키는 법을 배울 준비가 되셨나요?")
print("\n다음 단계로 진행하시겠습니까?")
