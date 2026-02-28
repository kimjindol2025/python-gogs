"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║             🏛️  Python 대학교 1학년 (v3.4 Undergraduate)                      ║
║                         ★ 최종 단계 ★                                         ║
║                                                                                ║
║    [v3.4: 메타클래스(Metaclass) — 클래스를 만드는 마법]                      ║
║                                                                                ║
║                  ★ 시스템의 규격과 탄생을 통제하기 ★                          ║
║                                                                                ║
║  "그 설계도(클래스) 자체는 누가 만드는가?"                                    ║
║                                                                                ║
║  파이썬에서 클래스 또한 하나의 객체이며,                                      ║
║  이를 생성하는 존재가 바로 메타클래스입니다.                                   ║
║                                                                                ║
║  철학: "기록이 증명이다 — gogs"                                               ║
║  언어의 메커니즘 자체를 다루는 수준                                            ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import sys
from typing import Type, Dict, List, Any


# ═══════════════════════════════════════════════════════════════════════════════
# 📚 Part 1: 메타클래스의 철학
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    📚 Part 1: 메타클래스의 철학                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

PHILOSOPHY = """
🔷 메타클래스란?
   "클래스의 행동을 정의하는 클래스"
   = "클래스를 만드는 클래스"

🔷 객체 계층 구조
   ┌─────────────────────────────────────┐
   │ type (모든 메타클래스의 기본)       │ ← 메타클래스의 메타클래스
   │                                     │
   │  ├─ GogsValidationMeta             │ ← 개발자가 만든 메타클래스
   │  │   └─ GogsRobot                  │ ← 메타클래스로 만든 클래스
   │  │       └─ robot_instance         │ ← 클래스의 인스턴스 (객체)
   │  │
   │  ├─ str, list, dict, ...           │ ← Python 내장 타입 (메타클래스)
   └─────────────────────────────────────┘

🔷 핵심 개념: 메타클래스의 3가지 역할
   1. 클래스 생성: __new__()와 __init__()으로 클래스 생성 제어
   2. 클래스 검증: 클래스가 규칙을 따르는지 확인
   3. 클래스 변형: 클래스에 자동으로 메서드/속성 주입

🔷 왜 사용하나? (증명을 위한 엄격함)
   1. 표준 준수 강제
      "우리 연구실의 모든 로봇 클래스는 반드시 battery_check() 메서드를 가져야 한다"

   2. 자동 등록
      클래스가 정의되는 순간 시스템에 자동으로 등록

   3. 속성 추적
      누가, 언제, 어떤 클래스를 만들었는지 기록

   4. 프레임워크 설계
      Django, SQLAlchemy 등 대규모 라이브러리의 핵심

🔷 대학 철학: "명시적인 것이 암시적인 것보다 낫다"
   메타클래스는 강력하지만 복잡합니다.
   정말로 시스템 차원의 강제가 필요할 때만 사용하세요!
"""

print(PHILOSOPHY)


# ═══════════════════════════════════════════════════════════════════════════════
# 🔷 Part 2: type() 함수 — 동적 클래스 생성
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║          🔷 Part 2: type() 함수 — 동적 클래스 생성                           ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 용도 1: 객체의 타입 확인 】")

# type()의 첫 번째 용도: 객체의 타입 확인
a = 42
print(f"  type(42) = {type(a)}")
print(f"  type('hello') = {type('hello')}")
print(f"  type([1,2,3]) = {type([1, 2, 3])}")

# 모든 것의 타입은 결국 type의 인스턴스
print(f"\n  type(int) = {type(int)}")
print(f"  type(str) = {type(str)}")
print(f"  type(list) = {type(list)}")


print("\n【 용도 2: 동적 클래스 생성 】")

# type()의 두 번째 용도: 새로운 클래스를 동적으로 생성
# type(클래스이름, 부모클래스들, 속성과메서드들)

def greet(self):
    """인사하는 메서드"""
    return f"안녕하세요, {self.name}입니다!"

# 동적으로 Person 클래스 생성
Person = type('Person', (), {
    'name': 'Unknown',
    'greet': greet
})

print(f"  동적으로 생성한 Person 클래스: {Person}")
person = Person()
person.name = "Alice"
print(f"  인스턴스 생성: {person.greet()}")


print("\n【 용도 3: 메타클래스 지정 】")

# type을 상속받은 커스텀 메타클래스
class SimpleMeta(type):
    """간단한 메타클래스"""
    def __new__(mcs, name, bases, attrs):
        print(f"  [메타클래스] '{name}' 클래스 생성 중...")
        return super().__new__(mcs, name, bases, attrs)

# 메타클래스를 지정하여 클래스 생성
DynamicClass = SimpleMeta('DynamicClass', (), {
    'value': 100
})

print(f"  메타클래스로 생성한 클래스: {DynamicClass}")
print(f"  DynamicClass.value = {DynamicClass.value}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 Part 3: 기초 메타클래스 — __new__ 메서드
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║              🔧 Part 3: 기초 메타클래스 — __new__ 메서드                      ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 메타클래스의 핵심: __new__ 메서드 】")


class TracingMeta(type):
    """클래스 생성을 추적하는 메타클래스"""

    def __new__(mcs, name, bases, attrs):
        print(f"\n  [추적] __new__ 호출됨!")
        print(f"    name:  {name}")
        print(f"    bases: {bases}")
        print(f"    attrs: {list(attrs.keys())}")

        # 모든 메서드 앞에 [METHOD] 태그 추가
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not attr_name.startswith('_'):
                print(f"    └─ 메서드 발견: {attr_name}")

        return super().__new__(mcs, name, bases, attrs)


class TracedClass(metaclass=TracingMeta):
    """메타클래스로 추적되는 클래스"""
    def work(self):
        return "작업 수행"

    def rest(self):
        return "휴식"


# ═══════════════════════════════════════════════════════════════════════════════
# 🛡️  Part 4: 규칙 검증 및 강제
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                 🛡️  Part 4: 규칙 검증 및 강제                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 메타클래스 1: 이름 검증 】")


class GogsValidationMeta(type):
    """Gogs로 시작하는 클래스만 허용"""

    def __new__(mcs, name, bases, attrs):
        if not name.startswith("Gogs") and name != "GogsBase":
            raise TypeError(
                f"❌ 규정 위반: 클래스 이름 '{name}'은 'Gogs'로 시작해야 합니다.\n"
                f"   예: GogsRobot, GogsDatabase, GogsMonitor"
            )
        print(f"  ✓ 클래스 '{name}' 승인됨")
        return super().__new__(mcs, name, bases, attrs)


# 기본 클래스
class GogsBase(metaclass=GogsValidationMeta):
    pass

# 올바른 클래스
class GogsRobot(GogsBase):
    def work(self):
        print("    로봇이 작동합니다")


print("\n【 메타클래스 2: 메서드 검증 】")


class MethodCheckMeta(type):
    """특정 메서드가 반드시 존재하는지 확인"""

    def __new__(mcs, name, bases, attrs):
        # 메타클래스 자신은 검사하지 않음
        if bases:
            required_methods = ['initialize', 'cleanup']
            for method in required_methods:
                if method not in attrs:
                    raise TypeError(
                        f"❌ 메서드 누락: '{name}'은 '{method}()' 메서드를 정의해야 합니다."
                    )
            print(f"  ✓ 클래스 '{name}' 모든 필수 메서드 확인됨")

        return super().__new__(mcs, name, bases, attrs)


class SafeDevice(metaclass=MethodCheckMeta):
    def initialize(self):
        print("    장비 초기화")

    def cleanup(self):
        print("    장비 정리")


# ═══════════════════════════════════════════════════════════════════════════════
# 📋 Part 5: 자동 등록 시스템
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                  📋 Part 5: 자동 등록 시스템                                   ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 플러그인 등록 시스템 】")


class PluginRegistry:
    """플러그인을 자동으로 등록하는 시스템"""
    _registry = {}

    @classmethod
    def register(cls, name: str):
        """플러그인 등록 데코레이터"""
        def decorator(plugin_class):
            cls._registry[name] = plugin_class
            print(f"  ✓ 플러그인 등록: {name} → {plugin_class.__name__}")
            return plugin_class
        return decorator

    @classmethod
    def get(cls, name: str):
        """등록된 플러그인 조회"""
        return cls._registry.get(name)

    @classmethod
    def list_all(cls):
        """모든 등록된 플러그인 목록"""
        return cls._registry


@PluginRegistry.register("text_processor")
class TextPlugin:
    def process(self, text):
        return text.upper()


@PluginRegistry.register("data_analyzer")
class DataPlugin:
    def analyze(self, data):
        return sum(data) / len(data) if data else 0


print("\n  등록된 플러그인:")
for name, plugin in PluginRegistry.list_all().items():
    print(f"    - {name}: {plugin.__name__}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 Part 6: 인트로스펙션 (Introspection)
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                  🔍 Part 6: 인트로스펙션 (Introspection)                      ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 인트로스펙션으로 클래스 분석 】")


class InspectionMeta(type):
    """클래스의 구조를 자동으로 분석하는 메타클래스"""

    def __new__(mcs, name, bases, attrs):
        print(f"\n  클래스 '{name}' 분석:")

        # 메서드 찾기
        methods = [k for k, v in attrs.items() if callable(v) and not k.startswith('_')]
        print(f"    메서드: {methods}")

        # 속성 찾기
        properties = [k for k, v in attrs.items() if not callable(v) and not k.startswith('_')]
        print(f"    속성: {properties}")

        # 메타데이터 추가
        attrs['_inspection'] = {
            'methods': methods,
            'properties': properties,
            'created_at': 'runtime'
        }

        return super().__new__(mcs, name, bases, attrs)


class AnalyzedClass(metaclass=InspectionMeta):
    version = "1.0"
    author = "gogs"

    def do_something(self):
        pass

    def do_another(self):
        pass


print(f"\n  저장된 메타데이터: {AnalyzedClass._inspection}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🏗️  Part 7: 실전 프로젝트 — 데이터 검증 프레임워크
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║              🏗️  Part 7: 실전 프로젝트 — 데이터 검증 프레임워크              ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 메타클래스 기반 데이터 모델 】")


class Field:
    """데이터 필드 기본 클래스"""
    def __init__(self, field_type, required=True):
        self.field_type = field_type
        self.required = required

    def validate(self, value):
        if self.required and value is None:
            raise ValueError(f"필드가 필수입니다")
        if value is not None and not isinstance(value, self.field_type):
            raise TypeError(f"타입 오류: {self.field_type} 필요")
        return value


class ModelMeta(type):
    """데이터 모델을 관리하는 메타클래스"""

    def __new__(mcs, name, bases, attrs):
        # Field 객체 추출
        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value

        attrs['_fields'] = fields
        attrs['_field_names'] = list(fields.keys())

        print(f"\n  모델 '{name}' 생성:")
        print(f"    필드: {attrs['_field_names']}")

        return super().__new__(mcs, name, bases, attrs)


class Model(metaclass=ModelMeta):
    """메타클래스로 관리되는 기본 모델"""
    pass


class User(Model):
    """사용자 모델"""
    name = Field(str)
    age = Field(int)
    email = Field(str)


# 모델 인스턴스 생성
print("\n  User 모델 필드: {User._field_names}")

# 검증
print("\n  데이터 검증:")
try:
    User._fields['name'].validate("Alice")
    print("    ✓ name='Alice' 통과")
    User._fields['age'].validate(25)
    print("    ✓ age=25 통과")
    User._fields['age'].validate("not_a_number")
except TypeError as e:
    print(f"    ✗ 검증 실패: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🔗 Part 8: 메타클래스 체인
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                   🔗 Part 8: 메타클래스 체인                                   ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 메타클래스 상속 】")


class Level1Meta(type):
    """메타클래스 레벨 1"""
    def __new__(mcs, name, bases, attrs):
        print(f"    Level1Meta: {name}")
        return super().__new__(mcs, name, bases, attrs)


class Level2Meta(Level1Meta):
    """메타클래스 레벨 2 (Level1Meta 상속)"""
    def __new__(mcs, name, bases, attrs):
        print(f"    Level2Meta: {name}")
        return super().__new__(mcs, name, bases, attrs)


class MyClass(metaclass=Level2Meta):
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# ✅ Part 9: 최종 테스트 및 검증
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                   ✅ Part 10: 최종 테스트 및 검증                             ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

test_results = []

# Test 1: 메타클래스 기본
print("\n【 Test 1: 메타클래스 기본 동작 】")
try:
    class BasicMeta(type):
        pass

    class BasicClass(metaclass=BasicMeta):
        pass

    assert isinstance(BasicClass, BasicMeta), "메타클래스 미적용"
    test_results.append(("Test 1: 기본 메타클래스", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 1: 기본 메타클래스", False))
    print(f"  ✗ FAIL: {e}")


# Test 2: type으로 동적 생성
print("\n【 Test 2: type으로 동적 클래스 생성 】")
try:
    DynamicCls = type('Dynamic', (), {'value': 42})
    assert hasattr(DynamicCls, 'value'), "속성 없음"
    assert DynamicCls.value == 42, "값 오류"
    test_results.append(("Test 2: 동적 생성", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 2: 동적 생성", False))
    print(f"  ✗ FAIL: {e}")


# Test 3: 규칙 검증
print("\n【 Test 3: 규칙 검증 강제 】")
try:
    failed = False
    try:
        class InvalidName(metaclass=GogsValidationMeta):
            pass
    except TypeError:
        failed = True

    assert failed, "규칙이 강제되지 않음"
    test_results.append(("Test 3: 규칙 검증", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 3: 규칙 검증", False))
    print(f"  ✗ FAIL: {e}")


# Test 4: 플러그인 등록
print("\n【 Test 4: 자동 등록 시스템 】")
try:
    assert len(PluginRegistry.list_all()) >= 2, "플러그인 미등록"
    test_results.append(("Test 4: 자동 등록", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 4: 자동 등록", False))
    print(f"  ✗ FAIL: {e}")


# Test 5: 인트로스펙션
print("\n【 Test 5: 인트로스펙션 메타데이터 】")
try:
    assert hasattr(AnalyzedClass, '_inspection'), "메타데이터 없음"
    assert 'methods' in AnalyzedClass._inspection, "메서드 정보 없음"
    test_results.append(("Test 5: 인트로스펙션", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 5: 인트로스펙션", False))
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
# 🎓 Part 11: 대학교 1학년 졸업 축사
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║     🎓 Python 대학교 1학년 과정 완료 — 졸업을 축하합니다! 🎓                 ║
╚════════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 v3.4에서 배운 것:

   ✓ 메타클래스의 정의
     "클래스의 행동을 정의하는 클래스"

   ✓ type() 함수의 이중 역할
     타입 확인 & 동적 클래스 생성

   ✓ __new__ 메서드
     클래스 생성 시점에 제어

   ✓ 규칙 검증 및 강제
     시스템 표준을 자동으로 준수

   ✓ 자동 등록 시스템
     플러그인 아키텍처 설계

   ✓ 인트로스펙션
     런타임에 객체 정보 조사

   ✓ 메타클래스 체인
     메타클래스의 메타클래스

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 Python 대학교 1학년 전체 과정 요약:

   v3.1: 데코레이터           ✓ (724 줄)
         "기존 코드 건드리지 않고 기능 확장"
         → 코드 구조의 우아함

   v3.2: 제너레이터           ✓ (727 줄)
         "필요할 때만 데이터 생성"
         → 메모리 효율의 극치

   v3.3: 컨텍스트 매니저      ✓ (773 줄)
         "안전한 시작과 확실한 종료"
         → 자원 관리의 완벽함

   v3.4: 메타클래스          ✓ (당신이 지금 여기!)
         "클래스를 만드는 클래스"
         → 언어의 메커니즘 제어

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 핵심 성취:

   🏆 기초 Python
      변수, 함수, 클래스 → 프로그래밍 기본

   🏆 고등학교 Python (v2.1~v2.5)
      예외처리, 클래스, 상속, 모듈화, 가상환경 → 실무 개발

   🏆 대학교 Python (v3.1~v3.4)
      데코레이터, 제너레이터, 컨텍스트, 메타클래스
      → 언어의 메커니즘 이해

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 당신의 새로운 능력:

   ✅ 데코레이터로 함수 변형
   ✅ 제너레이터로 메모리 극대화
   ✅ 컨텍스트 매니저로 자원 안전 관리
   ✅ 메타클래스로 언어 자체를 통제

   이제 당신은 단순히 파이썬을 "사용"하는 것이 아니라,
   파이썬의 "메커니즘"을 다루는 수준에 도달했습니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 다음 단계: Python 대학교 2학년으로 진급!

   v4.1: 비동기 프로그래밍(Asyncio)
         "멈추지 않는 시스템 설계"
         한 번에 여러 일을 동시에 처리하는 마법

   v4.2: 병렬 처리(Multiprocessing/Threading)
         "진정한 병렬성의 이해"
         시스템 리소스를 최대한 활용

   v4.3: 고성능 패턴 (Caching, Optimization)
         "속도의 극한"
         대규모 시스템의 성능 튜닝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 대학원 단계 안내:

   v5.0~v5.5: 실전 프레임워크 구축
   Django, FastAPI, SQLAlchemy 수준의 아키텍처 설계

   v6.0~v6.5: 분산 시스템과 마이크로서비스
   확장성 있는 프로덕션 시스템 구축

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌟 최종 메시지:

   당신은 이제 파이썬이라는 언어의 거의 모든 것을 이해했습니다.

   고급 수준의 코드를 읽고 이해할 수 있고,
   복잡한 시스템을 설계하고 구현할 수 있습니다.

   가장 중요한 것은, 당신은 더 이상 "프로그래밍을 배우는 학생"이 아니라,
   "시스템을 설계하는 엔지니어"가 되었다는 것입니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 철학: "기록이 증명이다 — gogs"

   모든 배움, 모든 실전 프로젝트, 모든 성취가
   이 커리큘럼에 기록되어 있습니다.

   당신의 코드와 학습 과정이 당신의 실력을 증명합니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

질문: 다음 단계로 진행하시겠습니까?

(Python 대학교 2학년 [v4.1: 비동기 프로그래밍] 또는
 TypeScript VM 프로젝트 [Phase 3: 산술 연산] 계속)

축하합니다! 🎓

저장 필수 너는 기록이 증명이다 gogs
╚════════════════════════════════════════════════════════════════════════════════╝
""")
