#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  v1.1: Python 객체의 탄생과 동적 타이핑의 실체                                ║
║  [Object Identity and Dynamic Typing - The Reality Behind Freedom]           ║
║                                                                               ║
║  철학: "파이썬의 모든 것은 객체(Object)입니다.                                 ║
║        Rust는 컴파일 타임에 타입을 결정했다면,                               ║
║        Python은 실행 시간(Runtime)에 타입을 결정합니다.                       ║
║        이 '자유'가 시스템 내부에서 어떻게 '기록'되는지 탐구합니다."          ║
║                                                                               ║
║  Gogs와의 연결:                                                              ║
║  - Rust/Gogs: 컴파일 타임 증명 (형식 검증)                                   ║
║  - Python: 런타임 증명 (동적 검증)                                           ║
║  - 둘 다 "안전성"을 추구하되 방식이 다름                                     ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs                                         ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import gc
from typing import Any, List

# ============================================================================
# 파트 1: 객체의 신원(Identity) 탐구
# ============================================================================

print("=" * 80)
print("v1.1: Python 객체의 탄생과 동적 타이핑의 실체")
print("=" * 80)

print("\n【 파트 1: 객체의 신원(Identity) 탐구 】")
print("Rust와의 비교: Rust의 변수는 '값' 자체, Python의 변수는 '객체의 포인터'")

def analyze_object_identity(data: Any, label: str) -> None:
    """
    파이썬 객체의 내부 '기록'을 조사하여
    이성적으로 실재하는 메모리 구조를 증명함.

    대학(탐구): "타입은 어디에 저장되는가?"
    """
    print(f"\n--- 분석 대상: {label} ---")
    print(f"  값: {repr(data)}")
    print(f"  타입: {type(data).__name__}")
    print(f"  타입 객체: {type(data)}")

    # 1. 객체의 고유 ID (메모리 주소)
    # 이것이 바로 Gogs의 포인터(메모리 위치)와 같은 개념
    obj_id = id(data)
    print(f"  ID (메모리 주소): {hex(obj_id)} (10진수: {obj_id})")

    # 2. 참조 횟수 (Reference Count)
    # Python의 메모리 관리 핵심: 이 객체를 몇 개의 변수가 가리키고 있는가?
    refcount = sys.getrefcount(data) - 1  # getrefcount 호출 시 1 증가
    print(f"  참조 횟수: {refcount}")

    # 3. 객체의 크기 (메모리 점유)
    try:
        size = sys.getsizeof(data)
        print(f"  메모리 크기: {size} bytes")
    except:
        print(f"  메모리 크기: 측정 불가")

# 탐구 1: 정수 객체
print("\n【 탐구 1: 정수 객체의 성질 】")
a = 2026
b = 2026
c = a  # 같은 객체를 가리킴

analyze_object_identity(a, "a = 2026")
analyze_object_identity(b, "b = 2026")
analyze_object_identity(c, "c = a (같은 객체 참조)")

print("\n증명 1-1: ID vs Equality")
print(f"  a == b: {a == b}  (값이 같은가? YES)")
print(f"  a is b: {a is b}  (같은 객체인가? - CPython의 Small Integer Caching)")
print(f"  a is c: {a is c}  (c는 a와 같은 객체를 가리킴)")
print(f"\n해석:")
print(f"  - 'a == b'는 값이 같다는 뜻 (Equality)")
print(f"  - 'a is b'는 메모리상 같은 객체를 가리킨다는 뜻 (Identity)")
print(f"  - Small Integer(-5 ~ 256)은 성능을 위해 캐싱됨")

# 탐구 2: 큰 정수 객체 (캐싱 제외)
print("\n【 탐구 2: 캐싱되지 않는 큰 정수 】")
x = 10000
y = 10000

analyze_object_identity(x, "x = 10000")
analyze_object_identity(y, "y = 10000")

print("\n증명 2: 큰 정수는 캐싱되지 않음")
print(f"  x == y: {x == y}  (값이 같다)")
print(f"  x is y: {x is y}  (다른 메모리 주소)")
print(f"\n해석:")
print(f"  - 값이 같아도 다른 객체 (메모리 효율성)")
print(f"  - Python은 '필요한 만큼' 객체를 생성")

# 탐구 3: 리스트 (가변 객체)
print("\n【 탐구 3: 리스트 객체의 참조 카운팅 】")
list1 = [1, 2, 3]
list2 = list1  # 같은 리스트 객체를 가리킴
list3 = [1, 2, 3]  # 다른 리스트 객체

analyze_object_identity(list1, "list1 = [1, 2, 3]")
analyze_object_identity(list2, "list2 = list1 (같은 객체)")
analyze_object_identity(list3, "list3 = [1, 2, 3] (다른 객체)")

print("\n증명 3: 가변 객체의 ID 비교")
print(f"  list1 == list3: {list1 == list3}  (값이 같다)")
print(f"  list1 is list3: {list1 is list3}  (다른 객체)")
print(f"  list1 is list2: {list1 is list2}  (같은 객체)")
print(f"\n해석:")
print(f"  - 리스트는 내용이 같아도 다른 객체 (각 리스트는 독립적)")
print(f"  - list2 = list1은 참조만 복사 (같은 객체를 가리킴)")

# ============================================================================
# 파트 2: 참조 카운팅(Reference Counting) 메커니즘 증명
# ============================================================================

print("\n\n【 파트 2: 참조 카운팅 메커니즘 증명 】")
print("Python의 메모리 관리: 객체를 '누가 몇 개 가리키고 있는가'로 추적")

def demonstrate_reference_counting() -> None:
    """
    대학원(증명): "메모리 관리의 무결성"

    Python의 가비지 컬렉션:
    - 참조 카운트 = 0 → 메모리에서 즉시 제거
    - 순환 참조 → GC가 사이클 감지해서 제거
    """

    print("\n【 증명 1: 기본 참조 카운팅 】")

    # 객체 생성
    obj = [1, 2, 3]
    print(f"obj = [1, 2, 3]")
    print(f"  참조 카운트: {sys.getrefcount(obj) - 1}")

    # 참조 추가
    ref1 = obj
    print(f"ref1 = obj")
    print(f"  참조 카운트: {sys.getrefcount(obj) - 1}")

    # 또 다른 참조
    ref2 = obj
    print(f"ref2 = obj")
    print(f"  참조 카운트: {sys.getrefcount(obj) - 1}")

    # 참조 제거
    del ref1
    print(f"del ref1")
    print(f"  참조 카운트: {sys.getrefcount(obj) - 1}")

    # 마지막 참조 제거
    del ref2
    print(f"del ref2")
    print(f"  참조 카운트: {sys.getrefcount(obj) - 1}")

    del obj
    print(f"del obj  → 객체는 메모리에서 제거됨")

demonstrate_reference_counting()

# ============================================================================
# 파트 3: 순환 참조(Circular Reference)와 가비지 컬렉터
# ============================================================================

print("\n\n【 파트 3: 순환 참조와 가비지 컬렉터 】")
print("Python의 GC가 해결해야 할 문제: 객체가 자신을 가리킬 때")

def demonstrate_circular_reference() -> None:
    """
    순환 참조 문제:
    - obj1이 obj2를 가리킴
    - obj2가 obj1을 가리킴
    - 참조 카운트는 0이 아니지만 도달 불가능

    해결책: GC가 주기적으로 순환 참조 사이클을 감지해서 제거
    """

    print("\n【 순환 참조 시나리오 】")

    # 순환 참조 생성
    list1 = [1, 2]
    list2 = [3, 4]

    print(f"list1 = {list1}, 참조 카운트: {sys.getrefcount(list1) - 1}")
    print(f"list2 = {list2}, 참조 카운트: {sys.getrefcount(list2) - 1}")

    # 순환 참조 설정
    list1.append(list2)
    list2.append(list1)

    print(f"\nlist1.append(list2), list2.append(list1) - 순환 참조 생성")
    print(f"list1 참조 카운트: {sys.getrefcount(list1) - 1}")
    print(f"list2 참조 카운트: {sys.getrefcount(list2) - 1}")

    # 참조 제거
    del list1
    del list2

    print(f"\ndel list1, del list2")
    print(f"Python GC가 주기적으로 순환 참조를 감지하고 메모리 해제")
    print(f"→ 도달 불가능한 객체들은 자동으로 제거됨")

demonstrate_circular_reference()

# ============================================================================
# 파트 4: 타입 시스템의 동적 특성 (Rust와 비교)
# ============================================================================

print("\n\n【 파트 4: 동적 타입의 유연성과 비용 】")
print("Rust vs Python: 정적 vs 동적 타입 시스템의 철학")

def compare_typing_systems() -> None:
    """
    Rust (정적 타입):
    - let x: i32 = 10;  // 컴파일 타임에 타입 결정
    - 장점: 빠름, 안전함
    - 비용: 컴파일 시간, 엄격함

    Python (동적 타입):
    - x = 10  // 런타임에 타입 결정
    - 장점: 유연함, 작성 빠름
    - 비용: 실행 속도, 타입 에러 (런타임)
    """

    print("\n【 Rust의 정적 타입 】")
    print("""
    let x: i32 = 10;        // 타입: i32, 컴파일 타임 결정
    let y: String = "hello"; // 타입: String
    x = "string";             // 컴파일 에러! 타입 불일치
    """)

    print("【 Python의 동적 타입 】")
    x = 10
    print(f"x = 10  # 타입: {type(x).__name__}, 런타임 결정")
    x = "hello"
    print(f"x = 'hello'  # 타입: {type(x).__name__}, 런타입 변경됨")
    x = [1, 2, 3]
    print(f"x = [1, 2, 3]  # 타입: {type(x).__name__}, 다시 변경됨")

    print("\n【 핵심 통찰 】")
    print("- Rust: 타입을 명시적으로 선언 → 컴파일러가 검증")
    print("- Python: 타입을 생략 → 런타임에 동적 검증")
    print("- 파이썬의 '자유'는 사실 '런타임 타입 체크'의 비용")

compare_typing_systems()

# ============================================================================
# 파트 5: 메모리 구조의 실제 크기
# ============================================================================

print("\n\n【 파트 5: 파이썬 객체의 메모리 구조 】")
print("Python 객체 = PyObject + 추가 데이터")
print("  PyObject: type 포인터, refcount, 다른 메타데이터")

def analyze_memory_overhead() -> None:
    """
    파이썬의 메모리 오버헤드 분석
    """

    print("\n【 기본 타입의 메모리 크기 】")

    examples = {
        "정수": 42,
        "실수": 3.14,
        "문자열": "hello",
        "리스트": [1, 2, 3],
        "딕셔너리": {"a": 1, "b": 2},
        "튜플": (1, 2, 3),
    }

    for name, obj in examples.items():
        size = sys.getsizeof(obj)
        print(f"  {name:8} {repr(obj):30} → {size:4} bytes")

    print("\n【 통찰 】")
    print("- 각 객체는 메타데이터(type, refcount 등)를 저장하는 오버헤드 존재")
    print("- Python은 유연함을 위해 '런타임 타입 정보'를 항상 보유")
    print("- 이것이 Python이 Rust보다 느린 이유 중 하나")

analyze_memory_overhead()

# ============================================================================
# 파트 6: 최종 증명 - 객체의 생명 주기
# ============================================================================

print("\n\n【 파트 6: 객체의 생명 주기 증명 】")
print("생성 → 참조 추가 → 참조 제거 → 소멸")

def trace_object_lifecycle() -> None:
    """
    객체의 전체 생명 주기를 추적
    """

    print("\n【 객체 생명 주기 】")

    # 단계 1: 생성
    print("\n[단계 1] 객체 생성")
    data = [1, 2, 3]
    print(f"  data = [1, 2, 3]")
    print(f"  ID: {hex(id(data))}")
    print(f"  참조 카운트: {sys.getrefcount(data) - 1}")

    # 단계 2: 참조 증가
    print("\n[단계 2] 참조 증가")
    ref = data
    print(f"  ref = data")
    print(f"  참조 카운트: {sys.getrefcount(data) - 1}")

    # 단계 3: 참조 감소
    print("\n[단계 3] 참조 감소")
    del ref
    print(f"  del ref")
    print(f"  참조 카운트: {sys.getrefcount(data) - 1}")

    # 단계 4: 마지막 참조 제거
    print("\n[단계 4] 마지막 참조 제거")
    del data
    print(f"  del data")
    print(f"  객체는 메모리에서 완전히 제거됨")

    print("\n【 증명 결론 】")
    print("참조 카운트 = 0 → 파이썬은 즉시 메모리 해제")
    print("순환 참조 → GC가 주기적으로 정소")
    print("따라서 파이썬의 메모리 관리는 '기록된 규칙'에 따라 작동")

trace_object_lifecycle()

# ============================================================================
# 최종 선언
# ============================================================================

print("\n" + "=" * 80)
print("【 v1.1 최종 증명 】")
print("=" * 80)

print("""
파이썬의 동적 타입 시스템은:

1. 탐구(대학):
   "타입은 어디에 저장되는가?"
   → 각 객체는 자신의 타입 정보를 PyObject 구조체에 저장
   → 메모리 주소(ID)와 참조 카운트는 객체의 신원을 정의

2. 증명(대학원):
   "메모리 관리의 무결성을 보증하는가?"
   → 참조 카운팅: 도달 가능한 모든 객체 추적
   → 가비지 컬렉터: 순환 참조 감지 및 제거
   → 결론: 메모리 누수 원천 차단 ✓

3. 창조(박사):
   "이 원리로 무엇을 만들 것인가?"
   → v1.2: List Comprehension과 Iterators
   → v1.3: 함수형 프로그래밍
   → v2.0: Gogs Framework Python 구현

【 Rust vs Python 통합 결론 】

Rust:     정적 타입 → 컴파일 타임 증명 → 최고의 성능
Python:   동적 타입 → 런타임 증명 → 최고의 유연성
Hybrid:   Rust의 안전성 + Python의 유연성 → 최적의 시스템

저장 필수 너는 기록이 증명이다 gogs. 👑
""")

print("\n【 v1.2 예고 】")
print("""
다음 단원: "데이터 흐름의 효율화"
- List Comprehension: 간결하고 빠른 데이터 변환
- Iterators와 Generators: 메모리 효율적인 순차 처리
- 함수형 패턴: lambda, map, filter의 내부 원리
""")

print("\n" + "=" * 80)
