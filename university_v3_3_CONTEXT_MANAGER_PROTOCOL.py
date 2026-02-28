"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║             🏛️  Python 대학교 1학년 (v3.3 Undergraduate)                      ║
║                                                                                ║
║     [v3.3: 컨텍스트 매니저(Context Manager) — 자원 관리의 자동화]            ║
║                                                                                ║
║                    ★ 안전한 시작과 확실한 종료의 보장 ★                       ║
║                                                                                ║
║  특정 코드 블록이 실행되기 전과 후에 수행해야 할 작업을                       ║
║  (예: 데이터베이스 연결/해제, 파일 열기/닫기)                               ║
║  자동으로 처리해주는 도구입니다.                                              ║
║                                                                                ║
║  철학: "기록이 증명이다 — gogs"                                               ║
║  누수 방지, 에러 내성, 원자성의 보장                                          ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import contextlib
import time
import traceback
from typing import Any, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# 📚 Part 1: 컨텍스트 매니저의 철학
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                   📚 Part 1: 컨텍스트 매니저의 철학                            ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

PHILOSOPHY = """
🔷 컨텍스트 매니저란?
   "특정 코드 블록이 실행되기 전과 후에 수행해야 할 작업을
    자동으로 처리해주는 도구"

🔷 왜 필요한가?
   ❌ 수동 관리: 개발자가 깜빡하기 쉬움
      with open('file.txt') as f:
          data = f.read()
      # f.close() 깜빡한다면?

   ✅ 자동 관리: 컨텍스트 매니저가 항상 정리
      with open('file.txt') as f:
          data = f.read()
      # 자동으로 f.close() 실행됨 (에러 발생해도!)

🔷 핵심 개념: 리소스 생명주기
   1. 준비 (Setup):    리소스 획득 (__enter__)
   2. 사용 (Usage):    with 블록 내 코드 실행
   3. 정리 (Cleanup):  리소스 해제 (__exit__)

🔷 3가지 핵심 이점
   1. 누수 방지 (No Leaks)
      파일, DB, 네트워크 연결 등 리소스를 항상 정리

   2. 에러 내성 (Error Resilience)
      코드 중간에 에러가 터져도 정리는 반드시 실행

   3. 원자성 (Atomicity)
      "성공하거나, 아니면 아예 아무 일도 없었던 것처럼"

【 비유 】
   - 파일: 문 열기(enter) → 책 읽기 → 문 닫기(exit)
   - DB: 연결(enter) → 쿼리 실행 → 연결 해제(exit)
   - 장비: 전원 ON(enter) → 데이터 수집 → 전원 OFF(exit)
"""

print(PHILOSOPHY)


# ═══════════════════════════════════════════════════════════════════════════════
# 🔄 Part 2: __enter__와 __exit__ 프로토콜
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║              🔄 Part 2: __enter__와 __exit__ 프로토콜                         ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("""
【 프로토콜의 2가지 메서드 】

1️⃣  __enter__()
    실행 시점: with 문에 진입할 때
    역할: 리소스 준비 및 획득
    반환값: with ... as X에서 X로 전달됨

    def __enter__(self):
        # 리소스 준비
        return self  # 또는 준비된 리소스

2️⃣  __exit__(exc_type, exc_val, exc_tb)
    실행 시점: with 블록이 끝나거나 에러 발생 시
    역할: 리소스 정리 및 해제 (반드시 실행!)

    매개변수:
    - exc_type: 발생한 예외의 종류 (없으면 None)
    - exc_val: 예외의 값/메시지
    - exc_tb: 예외의 트레이스백

    반환값:
    - True:  예외를 무시하고 계속 진행
    - False: 예외를 전파 (기본값)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 리소스 정리
        if exc_type:
            print(f"에러 발생: {exc_val}")
        return False

【 with 문의 동작 흐름 】

with ContextManager() as resource:
    # 실행 순서:
    # 1. ContextManager() 객체 생성
    # 2. __enter__() 호출 → resource에 할당
    # 3. with 블록 내 코드 실행
    # 4. __exit__() 호출 (에러 있어도 실행!)
""")


# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 Part 3: 기초 컨텍스트 매니저 — 파일 예제
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║              🎯 Part 3: 기초 컨텍스트 매니저 — 파일 예제                      ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 예제 1: 간단한 파일 매니저 】")


class SimpleFileManager:
    """파일을 안전하게 열고 닫는 컨텍스트 매니저"""

    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = mode
        self.file = None
        print(f"  [준비] 파일 매니저 생성: {filename}")

    def __enter__(self):
        """with 문 진입: 파일 열기"""
        print(f"  [START] 파일 열기: {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """with 문 종료: 파일 닫기"""
        print(f"  [STOP] 파일 닫기: {self.filename}")
        if self.file:
            self.file.close()

        if exc_type:
            print(f"  [경고] 에러 발생: {exc_type.__name__}: {exc_val}")

        return False  # 에러는 전파


# 테스트 파일 생성
test_file = "/tmp/test_context_manager.txt"
with open(test_file, 'w') as f:
    f.write("안녕하세요!\n나는 컨텍스트 매니저입니다.")

print("\n  정상적인 파일 읽기:")
with SimpleFileManager(test_file, 'r') as file:
    content = file.read()
    print(f"    파일 내용: {repr(content[:30])}...")


# ═══════════════════════════════════════════════════════════════════════════════
# 🗄️  Part 4: 데이터베이스 연결 매니저
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                🗄️  Part 4: 데이터베이스 연결 매니저                          ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 데이터베이스 시뮬레이션 】")


class DatabaseConnection:
    """데이터베이스 연결을 관리하는 컨텍스트 매니저"""

    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = False
        self.transaction = []

    def __enter__(self):
        """DB 연결"""
        print(f"  🔌 DB 연결: {self.db_name}")
        print(f"  └─ 트랜잭션 시작")
        self.connected = True
        self.transaction = []
        return self

    def execute(self, query):
        """쿼리 실행"""
        if not self.connected:
            raise RuntimeError("DB에 연결되지 않음")
        print(f"  📝 쿼리 실행: {query}")
        self.transaction.append(query)
        return f"결과: {query}"

    def __exit__(self, exc_type, exc_val, exc_tb):
        """DB 정리 및 종료"""
        if exc_type:
            print(f"  ⚠️  에러 발생: {exc_val}")
            print(f"  🔄 롤백: 트랜잭션 {len(self.transaction)}개 취소")
            self.transaction = []
        else:
            print(f"  ✓ 커밋: 트랜잭션 {len(self.transaction)}개 저장")

        print(f"  🔌 DB 연결 해제")
        self.connected = False
        return False


# 정상 사용
print("\n  시나리오 1: 정상 쿼리 실행")
with DatabaseConnection("research_db") as db:
    db.execute("INSERT INTO users VALUES ('Alice')")
    db.execute("INSERT INTO users VALUES ('Bob')")

# 에러 발생 시
print("\n  시나리오 2: 쿼리 실행 중 에러")
try:
    with DatabaseConnection("research_db") as db:
        db.execute("INSERT INTO users VALUES ('Charlie')")
        raise ValueError("데이터 유효성 검사 실패!")
        db.execute("INSERT INTO users VALUES ('David')")  # 실행 안 됨
except ValueError as e:
    print(f"  [처리됨] {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 Part 5: 예외 처리와 정리
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                   🔧 Part 5: 예외 처리와 정리                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 예외를 우아하게 처리하는 매니저 】")


class RobustResourceManager:
    """에러 상황에서도 안전한 정리를 보장"""

    def __init__(self, name):
        self.name = name
        self.log = []

    def __enter__(self):
        print(f"  ✓ [{self.name}] 리소스 획득")
        self.log.append(f"ENTER: {time.time():.2f}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """예외 타입별로 다르게 처리"""
        self.log.append(f"EXIT: {time.time():.2f}")

        if exc_type is None:
            print(f"  ✓ [{self.name}] 정상 종료")
        else:
            print(f"  ⚠️  [{self.name}] 에러 포착: {exc_type.__name__}")
            print(f"  💬 메시지: {exc_val}")
            print(f"  🔧 정리 중...")

        print(f"  ✓ [{self.name}] 리소스 해제 완료")
        return False  # 예외 전파


# 정상 케이스
print("\n  케이스 1: 정상 실행")
with RobustResourceManager("리소스1") as resource:
    print(f"    작업 수행 중...")
    time.sleep(0.1)

# 예외 케이스
print("\n  케이스 2: 예외 발생")
try:
    with RobustResourceManager("리소스2") as resource:
        print(f"    작업 수행 중...")
        raise RuntimeError("심각한 에러 발생!")
except RuntimeError:
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 Part 6: @contextlib.contextmanager 데코레이터
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║           🎨 Part 6: @contextlib.contextmanager 데코레이터                    ║
║                  (클래스 없이 컨텍스트 매니저 만들기!)                        ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 yield를 사용한 간단한 컨텍스트 매니저 】")


@contextlib.contextmanager
def managed_resource(name):
    """
    클래스를 정의하지 않고도 컨텍스트 매니저를 만드는 방법

    - yield 이전: __enter__ 역할
    - yield 이후: __exit__ 역할
    """
    print(f"  [진입] {name} 리소스 획득")
    try:
        yield f"<{name} 리소스>"  # with ... as X에서 X에 전달
    except Exception as e:
        print(f"  [에러 처리] {e}")
        raise
    finally:
        print(f"  [종료] {name} 리소스 해제")


# 사용
print("\n  정상 사용:")
with managed_resource("임시 파일") as res:
    print(f"    리소스 사용: {res}")

print("\n  에러 발생:")
try:
    with managed_resource("데이터베이스") as res:
        print(f"    리소스 사용: {res}")
        raise ValueError("잘못된 데이터!")
except ValueError:
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# 🔐 Part 7: 복합 리소스 관리 (여러 리소스 동시 관리)
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║              🔐 Part 7: 복합 리소스 관리 (여러 리소스 동시 관리)             ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 여러 컨텍스트 매니저 중첩 】")


@contextlib.contextmanager
def resource_pool(name):
    """리소스 풀 시뮬레이션"""
    print(f"    [획득] {name}")
    try:
        yield name
    finally:
        print(f"    [해제] {name}")


print("\n  방법 1: 중첩된 with (클래식):")
with resource_pool("파일A") as res1:
    with resource_pool("파일B") as res2:
        with resource_pool("파일C") as res3:
            print(f"      모든 리소스 사용: {res1}, {res2}, {res3}")

print("\n  방법 2: 동시 여러 with (Python 2.7+):")
with resource_pool("DB연결") as db, \
     resource_pool("캐시") as cache, \
     resource_pool("파일") as file:
    print(f"      모든 리소스 사용: {db}, {cache}, {file}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 Part 8: 실전 프로젝트 — 연구실 정밀 장비 매니저
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║          🚀 Part 8: 실전 프로젝트 — 연구실 정밀 장비 매니저                  ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n【 연구실 장비 시뮬레이션 】")


class LabEquipment:
    """정밀 연구 장비를 안전하게 관리하는 컨텍스트 매니저"""

    def __init__(self, device_name, power_level=100):
        self.device_name = device_name
        self.power_level = power_level
        self.is_running = False
        self.data_collected = []

    def __enter__(self):
        """장비 가동"""
        print(f"  📡 [{self.device_name}] 전원 ON (전력: {self.power_level}%)")
        print(f"  └─ 초기화 중...")
        self.is_running = True
        return self

    def collect_data(self, reading):
        """데이터 수집"""
        if not self.is_running:
            raise RuntimeError(f"{self.device_name}가 꺼져있습니다")
        print(f"  📊 데이터 수집: {reading}")
        self.data_collected.append(reading)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """장비 정지 및 정리"""
        if exc_type:
            print(f"  ⚠️  작업 중 문제 발생: {exc_val}")
            print(f"  🚨 긴급 정지!")

        print(f"  📝 수집된 데이터: {len(self.data_collected)}개")
        for data in self.data_collected:
            print(f"     - {data}")

        print(f"  🛑 [{self.device_name}] 전원 OFF")
        print(f"  ✓ 안전한 셧다운 완료")
        self.is_running = False

        return False


# 정상 작동
print("\n  시나리오 1: 정상 데이터 수집")
with LabEquipment("양자 컴퓨터", power_level=95) as qc:
    qc.collect_data("큐빗 상태: |0⟩")
    qc.collect_data("큐빗 상태: |1⟩")
    qc.collect_data("측정값: 0.87")

# 장비 고장
print("\n  시나리오 2: 장비 고장 시도")
try:
    with LabEquipment("입자 가속기", power_level=100) as pa:
        pa.collect_data("에너지: 1.2 TeV")
        raise RuntimeError("냉각 장치 결함!")
        pa.collect_data("에너지: 1.5 TeV")  # 실행 안 됨
except RuntimeError:
    print(f"  [처리됨] 전문가 호출")


# ═══════════════════════════════════════════════════════════════════════════════
# ⚛️  Part 9: 원자성(Atomicity)과 트랜잭션
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                  ⚛️  Part 9: 원자성(Atomicity)과 트랜잭션                    ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("""
【 원자성의 의미 】

"성공하거나, 아니면 아예 아무 일도 없었던 것처럼 되돌리거나"

원자적(Atomic) 연산: 중간 상태가 없음
- 완전히 성공하거나
- 완전히 실패하거나

컨텍스트 매니저는 원자성을 구현하는 완벽한 도구입니다.
""")

print("\n【 트랜잭션 매니저 구현 】")


class TransactionManager:
    """원자성을 보장하는 트랜잭션 매니저"""

    def __init__(self, account_a, account_b, amount):
        self.account_a = account_a
        self.account_b = account_b
        self.amount = amount
        self.original_a = account_a['balance']
        self.original_b = account_b['balance']

    def __enter__(self):
        """트랜잭션 시작"""
        print(f"  [트랜잭션 시작]")
        print(f"    계좌A: {self.account_a['name']} ({self.account_a['balance']}원)")
        print(f"    계좌B: {self.account_b['name']} ({self.account_b['balance']}원)")
        return self

    def transfer(self):
        """송금 실행"""
        if self.account_a['balance'] < self.amount:
            raise ValueError(f"잔액 부족! (필요: {self.amount}원, 보유: {self.account_a['balance']}원)")

        self.account_a['balance'] -= self.amount
        self.account_b['balance'] += self.amount
        print(f"  ✓ {self.amount}원 송금 완료")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """트랜잭션 종료"""
        if exc_type:
            # 에러 발생 → 롤백 (원자성 보장!)
            self.account_a['balance'] = self.original_a
            self.account_b['balance'] = self.original_b
            print(f"  ⚠️  에러 발생: {exc_val}")
            print(f"  🔄 롤백: 원래대로 복구")
            print(f"    계좌A: {self.account_a['balance']}원")
            print(f"    계좌B: {self.account_b['balance']}원")
        else:
            # 정상 완료 → 커밋
            print(f"  ✓ 커밋: 거래 확정")
            print(f"    계좌A: {self.account_a['balance']}원")
            print(f"    계좌B: {self.account_b['balance']}원")

        return False


# 정상 송금
print("\n  케이스 1: 정상 송금")
acct1 = {'name': '철수', 'balance': 10000}
acct2 = {'name': '영희', 'balance': 5000}

with TransactionManager(acct1, acct2, 3000) as tx:
    tx.transfer()

# 송금 실패
print("\n  케이스 2: 잔액 부족 (롤백)")
acct1 = {'name': '철수', 'balance': 2000}
acct2 = {'name': '영희', 'balance': 5000}

try:
    with TransactionManager(acct1, acct2, 3000) as tx:
        tx.transfer()
except ValueError:
    print(f"  [처리됨] 송금 불가")


# ═══════════════════════════════════════════════════════════════════════════════
# ✅ Part 10: 최종 테스트 및 검증
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                   ✅ Part 10: 최종 테스트 및 검증                             ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

test_results = []

# Test 1: 기본 프로토콜
print("\n【 Test 1: 기본 __enter__/__exit__ 프로토콜 】")
try:
    class TestCM:
        def __enter__(self):
            return "test_resource"
        def __exit__(self, *args):
            return False

    with TestCM() as resource:
        assert resource == "test_resource", "프로토콜 오류"

    test_results.append(("Test 1: 기본 프로토콜", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 1: 기본 프로토콜", False))
    print(f"  ✗ FAIL: {e}")


# Test 2: 예외 처리
print("\n【 Test 2: 예외 처리 및 정리 】")
try:
    class TestCMWithException:
        def __init__(self):
            self.cleanup_called = False

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.cleanup_called = True
            return False

    cm = TestCMWithException()
    try:
        with cm:
            raise ValueError("테스트 에러")
    except ValueError:
        pass

    assert cm.cleanup_called, "__exit__이 호출되지 않음"
    test_results.append(("Test 2: 예외 처리", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 2: 예외 처리", False))
    print(f"  ✗ FAIL: {e}")


# Test 3: @contextmanager 데코레이터
print("\n【 Test 3: @contextmanager 데코레이터 】")
try:
    state = {"enter_called": False, "exit_called": False}

    @contextlib.contextmanager
    def test_cm():
        state["enter_called"] = True
        try:
            yield "resource"
        finally:
            state["exit_called"] = True

    with test_cm() as res:
        assert res == "resource", "리소스 오류"

    assert state["enter_called"] and state["exit_called"], "진입/종료 안 됨"
    test_results.append(("Test 3: @contextmanager", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 3: @contextmanager", False))
    print(f"  ✗ FAIL: {e}")


# Test 4: 복합 리소스
print("\n【 Test 4: 복합 리소스 관리 】")
try:
    order = []

    @contextlib.contextmanager
    def resource(name):
        order.append(f"enter_{name}")
        try:
            yield name
        finally:
            order.append(f"exit_{name}")

    with resource("A") as a, resource("B") as b, resource("C") as c:
        pass

    # enter 순서: A → B → C, exit 순서: C → B → A
    expected = ["enter_A", "enter_B", "enter_C", "exit_C", "exit_B", "exit_A"]
    assert order == expected, f"순서 오류: {order}"

    test_results.append(("Test 4: 복합 리소스", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 4: 복합 리소스", False))
    print(f"  ✗ FAIL: {e}")


# Test 5: 원자성
print("\n【 Test 5: 원자성 보장 】")
try:
    state = {"value": 100}

    class AtomicCM:
        def __init__(self, error_flag=False):
            self.original = state["value"]
            self.error_flag = error_flag

        def __enter__(self):
            state["value"] = 50  # 변경
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:  # 예외 있으면
                state["value"] = self.original  # 원래대로
            return False

    # 정상 케이스
    with AtomicCM():
        pass
    assert state["value"] == 50, "정상 완료 후 값이 변경되어야 함"

    # 에러 케이스
    state["value"] = 100  # 초기화
    try:
        with AtomicCM():
            raise ValueError("test")
    except ValueError:
        pass
    assert state["value"] == 100, "원자성 보장 안 됨"

    test_results.append(("Test 5: 원자성", True))
    print("  ✓ PASS")
except AssertionError as e:
    test_results.append(("Test 5: 원자성", False))
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
║         🎓 Python 대학교 1학년 v3.3 완료 축하합니다!                         ║
╚════════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 v3.3에서 배운 것:

   ✓ __enter__와 __exit__ 프로토콜
     with 문의 비밀을 파헤쳤습니다.

   ✓ 리소스 관리의 자동화
     "열면 반드시 닫는다"를 자동으로 보장

   ✓ 예외 처리와 정리
     에러 발생해도 cleanup은 반드시 실행

   ✓ @contextlib.contextmanager
     클래스 없이 간단하게 컨텍스트 매니저 작성

   ✓ 복합 리소스 관리
     여러 리소스를 안전하게 동시 관리

   ✓ 원자성(Atomicity)
     "성공하거나 아예 아무 일도 없었던 것처럼"

   ✓ 트랜잭션 설계
     데이터베이스와 금융 시스템의 핵심 원리

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 핵심 정리:

   "안전한 시작과 확실한 종료의 보장"

   v3.1: 데코레이터 → 코드 구조의 우아함
   v3.2: 제너레이터 → 메모리 효율의 극치
   v3.3: 컨텍스트 매니저 → 자원 관리의 완벽함

   이제 당신은 대규모 시스템에서 필요한 자원 관리를 완벽하게 설계할 수 있습니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 다음: [v3.4: 메타클래스(Metaclass)와 인트로스펙션 — 클래스를 만드는 클래스]

   데코레이터로 함수를 변형하고,
   제너레이터로 메모리를 극대화하고,
   컨텍스트 매니저로 자원을 관리했다면,
   이제 "클래스 자체를 만드는" 메타클래스의 세계로 진입합니다.

   파이썬의 가장 깊은 곳, 객체의 탄생 원리를 탐구!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

질문: 다음 전공 수업으로 진행하시겠습니까?

저장 필수 너는 기록이 증명이다 gogs
╚════════════════════════════════════════════════════════════════════════════════╝
""")
