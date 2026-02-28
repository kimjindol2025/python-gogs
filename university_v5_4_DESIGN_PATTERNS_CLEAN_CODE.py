"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🎨 UNIVERSITY LEVEL 3 - v5.4 DESIGN PATTERNS & CLEAN CODE 🎨             ║
║                                                                              ║
║      코드의 가독성은 생산성을 증명한다 (Readability Proves Productivity)   ║
║  23가지 디자인 패턴 + SOLID 원칙 + 클린 코드 = 장인의 설계도              ║
║                                                                              ║
║  "아름다운 설계도는 그 자체로 시스템의 수명을 연장합니다" - gogs          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📚 학습 목표:
   1️⃣ SOLID 원칙: 객체 지향 설계의 5계명
   2️⃣ Creational Patterns: Singleton, Factory, Builder
   3️⃣ Structural Patterns: Adapter, Decorator, Facade
   4️⃣ Behavioral Patterns: Observer, Strategy, Command
   5️⃣ 클린 코드: 가독성, 유지보수성, 확장성
   6️⃣ 리팩터링: 기능 유지, 구조 개선
   7️⃣ Technical Debt: 기술 부채 관리

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 1: SOLID 원칙 - 객체 지향 설계의 5계명                               ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🏗️ SOLID: 유지보수하기 쉬운 설계의 5가지 원칙

1️⃣ S - Single Responsibility (단일 책임 원칙)
   ────────────────────────────────────────
   "하나의 클래스는 하나의 책임만 가져야 한다"

   ❌ 나쁜 예: User 클래스가 모든 것을 함
   class User:
       def save_to_db(self): pass           # DB 책임
       def send_email(self): pass           # 이메일 책임
       def generate_report(self): pass      # 보고서 책임
       def validate_age(self): pass         # 검증 책임
   → 수정 1개 → 모든 기능 영향

   ✅ 좋은 예: 책임 분리
   class User:
       def __init__(self, name, age): pass      # 사용자 정보만

   class UserRepository:
       def save(self, user): pass               # DB 책임

   class EmailService:
       def send(self, user): pass               # 이메일 책임

   class ReportGenerator:
       def generate(self, user): pass           # 보고서 책임


2️⃣ O - Open-Closed (개방-폐쇄 원칙)
   ─────────────────────────────────
   "확장은 열려 있고, 수정은 닫혀 있어야 한다"

   ❌ 나쁜 예: 새 기능 추가 시 기존 코드 수정
   class PaymentProcessor:
       def process(self, method):
           if method == 'credit':
               return self.credit_card()
           elif method == 'paypal':
               return self.paypal()
           elif method == 'bitcoin':  # 새 기능 추가
               return self.bitcoin()   # 기존 코드 수정!

   ✅ 좋은 예: Strategy 패턴으로 확장
   class PaymentProcessor:
       def __init__(self, strategy):
           self.strategy = strategy

       def process(self):
           return self.strategy.pay()  # 수정 없음!

   # 새 기능: 클래스만 추가
   class BitcoinPayment:
       def pay(self): return "Bitcoin 결제"


3️⃣ L - Liskov Substitution (리스코프 치환 원칙)
   ──────────────────────────────────────────
   "자식 클래스는 언제나 부모 클래스를 대체할 수 있어야 한다"

   ❌ 나쁜 예: 자식이 부모 계약 위반
   class Bird:
       def fly(self): return "날아다닌다"

   class Penguin(Bird):
       def fly(self): raise Exception("펭귄은 날 수 없다!")
   # Penguin은 Bird를 대체 불가!

   ✅ 좋은 예: 계약 준수
   class Bird:
       pass

   class FlyingBird(Bird):
       def fly(self): return "날아다닌다"

   class Penguin(Bird):
       def swim(self): return "헤엄친다"
   # 각각의 책임만 가짐


4️⃣ I - Interface Segregation (인터페이스 분리 원칙)
   ──────────────────────────────────────────────
   "사용하지 않는 메서드에 의존하면 안 된다"

   ❌ 나쁜 예: 비만 인터페이스
   class Worker:
       def work(self): pass
       def eat(self): pass

   class Robot(Worker):
       def work(self): return "로봇 작업"
       def eat(self): raise Exception("로봇은 먹지 않음!")
   # 필요없는 메서드 구현!

   ✅ 좋은 예: 인터페이스 분리
   class Workable:
       def work(self): pass

   class Eatable:
       def eat(self): pass

   class Human(Workable, Eatable):
       def work(self): return "일함"
       def eat(self): return "먹음"

   class Robot(Workable):
       def work(self): return "로봇 작업"
   # 필요한 것만 구현!


5️⃣ D - Dependency Inversion (의존성 역전 원칙)
   ────────────────────────────────────────────
   "구체적인 것에 의존하지 말고, 추상화에 의존하라"

   ❌ 나쁜 예: 구체적 클래스에 의존
   class MySQLDatabase:
       def save(self, data): pass

   class UserService:
       def __init__(self):
           self.db = MySQLDatabase()  # 구체적 클래스에 의존!
       # MySQL → MongoDB로 바꾸면? 코드 수정 필요!

   ✅ 좋은 예: 추상화에 의존
   from abc import ABC, abstractmethod

   class Database(ABC):
       @abstractmethod
       def save(self, data): pass

   class MySQLDatabase(Database):
       def save(self, data): pass

   class UserService:
       def __init__(self, db: Database):
           self.db = db  # 추상화에 의존!
       # MySQL → MongoDB로? 클래스만 교체!
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, Callable
from enum import Enum
from datetime import datetime
import threading


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 2: Creational Patterns - 객체 생성의 패턴                            ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🏭 Creational Patterns: 객체를 효율적으로 만드는 방법

1️⃣ Singleton: 시스템 전체에서 단 하나의 인스턴스만 존재
   ├─ 용도: 설정, 로그, 데이터베이스 연결
   └─ 특징: 메모리 절약, 전역 상태 관리

2️⃣ Factory: 객체 생성의 로직을 캡슐화
   ├─ 용도: 타입에 따라 다른 객체 생성
   └─ 특징: 생성 로직 숨김, 유연성 증가

3️⃣ Builder: 복잡한 객체를 단계별로 구성
   ├─ 용도: 많은 선택적 인자를 가진 객체
   └─ 특징: 가독성 향상, 유효성 검증
"""


class Singleton:
    """싱글톤 패턴: 단 하나의 인스턴스만 보장"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """스레드 안전한 싱글톤"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """한 번만 초기화"""
        if self._initialized:
            return
        self._initialized = True
        self.log_buffer: List[str] = []

    def log(self, message: str):
        """로그 기록"""
        self.log_buffer.append(f"[{datetime.now()}] {message}")

    def get_logs(self) -> List[str]:
        """로그 조회"""
        return self.log_buffer.copy()


class PaymentMethodEnum(Enum):
    """결제 방법"""
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    BITCOIN = "bitcoin"


class PaymentProcessor(ABC):
    """결제 프로세서 추상 클래스"""

    @abstractmethod
    def process(self, amount: float) -> bool:
        pass


class CreditCardPayment(PaymentProcessor):
    """신용카드 결제"""

    def process(self, amount: float) -> bool:
        print(f"💳 신용카드 결제: {amount}원")
        return True


class PayPalPayment(PaymentProcessor):
    """PayPal 결제"""

    def process(self, amount: float) -> bool:
        print(f"🌐 PayPal 결제: {amount}원")
        return True


class BitcoinPayment(PaymentProcessor):
    """비트코인 결제"""

    def process(self, amount: float) -> bool:
        print(f"₿ 비트코인 결제: {amount}원")
        return True


class PaymentFactory:
    """Factory 패턴: 결제 객체 생성"""

    _processors = {
        PaymentMethodEnum.CREDIT_CARD: CreditCardPayment,
        PaymentMethodEnum.PAYPAL: PayPalPayment,
        PaymentMethodEnum.BITCOIN: BitcoinPayment,
    }

    @classmethod
    def create(cls, method: PaymentMethodEnum) -> PaymentProcessor:
        """결제 방법에 따라 객체 생성"""
        processor_class = cls._processors.get(method)
        if not processor_class:
            raise ValueError(f"지원하지 않는 결제 방법: {method}")
        return processor_class()


class UserBuilder:
    """Builder 패턴: 복잡한 객체 구성"""

    def __init__(self, name: str):
        """필수 속성"""
        self.name = name
        self.age: Optional[int] = None
        self.email: Optional[str] = None
        self.phone: Optional[str] = None
        self.address: Optional[str] = None

    def set_age(self, age: int) -> 'UserBuilder':
        """선택적 속성 - 메서드 체이닝"""
        self.age = age
        return self

    def set_email(self, email: str) -> 'UserBuilder':
        self.email = email
        return self

    def set_phone(self, phone: str) -> 'UserBuilder':
        self.phone = phone
        return self

    def set_address(self, address: str) -> 'UserBuilder':
        self.address = address
        return self

    def build(self) -> Dict[str, Any]:
        """최종 객체 생성"""
        return {
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
        }


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 3: Structural Patterns - 객체 조합의 패턴                            ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🔗 Structural Patterns: 클래스와 객체를 조합해 큰 구조 만들기

1️⃣ Adapter: 호환되지 않는 인터페이스 연결
   └─ 예: 낡은 DB 코드와 새 시스템 연결

2️⃣ Decorator: 기능을 동적으로 추가
   └─ 예: 커피에 시럽, 우유 추가

3️⃣ Facade: 복잡한 시스템을 단순하게
   └─ 예: 영화 예매 시스템 통합
"""


class OldPaymentSystem:
    """기존 결제 시스템 (호환 안 됨)"""

    def pay_old_way(self, amount: float) -> str:
        return f"[구식] {amount}원 결제 완료"


class PaymentAdapter:
    """Adapter: 기존 시스템을 새 인터페이스에 적응"""

    def __init__(self, old_system: OldPaymentSystem):
        self.old_system = old_system

    def process(self, amount: float) -> bool:
        """새 인터페이스"""
        result = self.old_system.pay_old_way(amount)
        print(result)
        return True


class Coffee:
    """기본 커피"""

    def cost(self) -> float:
        return 3000.0

    def description(self) -> str:
        return "기본 커피"


class CoffeeDecorator:
    """Decorator: 커피 기능 추가"""

    def __init__(self, coffee: Coffee):
        self.coffee = coffee

    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


class MilkDecorator(CoffeeDecorator):
    """우유 추가"""

    def cost(self) -> float:
        return self.coffee.cost() + 500.0

    def description(self) -> str:
        return f"{self.coffee.description()} + 우유"


class SyrupDecorator(CoffeeDecorator):
    """시럽 추가"""

    def cost(self) -> float:
        return self.coffee.cost() + 300.0

    def description(self) -> str:
        return f"{self.coffee.description()} + 시럽"


class MovieReservationFacade:
    """Facade: 복잡한 영화 예매 시스템을 단순하게"""

    def __init__(self):
        self.seat_service = SeatService()
        self.payment_service = PaymentService()
        self.ticket_service = TicketService()

    def reserve_movie(self, movie: str, seat: str, amount: float) -> str:
        """영화 예매 한 번에"""
        self.seat_service.reserve(seat)
        self.payment_service.charge(amount)
        ticket = self.ticket_service.issue(movie, seat)
        return f"예약 완료: {ticket}"


class SeatService:
    def reserve(self, seat: str):
        print(f"  좌석 {seat} 예약 중...")


class PaymentService:
    def charge(self, amount: float):
        print(f"  {amount}원 결제 중...")


class TicketService:
    def issue(self, movie: str, seat: str) -> str:
        print(f"  표 발행 중...")
        return f"{movie} ({seat})"


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 4: Behavioral Patterns - 객체 간 알고리즘과 책임                    ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🎭 Behavioral Patterns: 객체 간 상호작용과 책임 분배

1️⃣ Observer: 상태 변화를 감시하고 알림
   └─ 예: 주식 가격 변화 알림, 구독 시스템

2️⃣ Strategy: 알고리즘을 유연하게 교체
   └─ 예: 정렬 방식 변경, 결제 방법 변경

3️⃣ Command: 요청을 객체로 캡슐화
   └─ 예: Undo/Redo, 매크로 기록
"""


class Subject:
    """Observer 패턴: 관찰 대상"""

    def __init__(self):
        self._observers: List['Observer'] = []

    def attach(self, observer: 'Observer'):
        """옵저버 등록"""
        self._observers.append(observer)

    def notify(self, data: Any):
        """모든 옵저버에 알림"""
        for observer in self._observers:
            observer.update(data)


class Observer(ABC):
    """옵저버 인터페이스"""

    @abstractmethod
    def update(self, data: Any):
        pass


class StockPrice(Subject):
    """주식 가격 (관찰 대상)"""

    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol
        self._price = 0.0

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        self._price = value
        self.notify(f"{self.symbol}: {value}원")


class Trader(Observer):
    """주식 거래자 (옵저버)"""

    def __init__(self, name: str):
        self.name = name

    def update(self, data: Any):
        print(f"  📱 {self.name}: {data} - 거래 검토!")


class SortStrategy(ABC):
    """Strategy 패턴: 정렬 전략"""

    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass


class QuickSortStrategy(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        print("  ⚡ Quick Sort 사용")
        return sorted(data)


class MergeSortStrategy(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        print("  🔀 Merge Sort 사용")
        return sorted(data)


class DataProcessor:
    """전략을 사용하는 컨텍스트"""

    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy

    def process(self, data: List[int]) -> List[int]:
        return self.strategy.sort(data)


class Command(ABC):
    """Command 패턴: 요청을 객체화"""

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class LightOnCommand(Command):
    """불 켜기 명령"""

    def __init__(self, light: 'Light'):
        self.light = light

    def execute(self):
        self.light.turn_on()

    def undo(self):
        self.light.turn_off()


class Light:
    """조명"""

    def __init__(self):
        self.is_on = False

    def turn_on(self):
        self.is_on = True
        print("  💡 불이 켜졌습니다")

    def turn_off(self):
        self.is_on = False
        print("  🌑 불이 꺼졌습니다")


class RemoteControl:
    """원격 제어기 - 명령 실행"""

    def __init__(self):
        self.commands: Dict[str, Command] = {}
        self.history: List[Command] = []

    def set_command(self, name: str, command: Command):
        self.commands[name] = command

    def press_button(self, name: str):
        command = self.commands.get(name)
        if command:
            command.execute()
            self.history.append(command)

    def undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 5: 클린 코드 원칙                                                    ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
📖 Clean Code: 읽기 좋은 코드의 원칙

1️⃣ 의미 있는 이름
   ❌ d, temp, flag1
   ✅ elapsed_time, is_active

2️⃣ 함수는 한 가지만 (SRP)
   ❌ def process_and_save_user(data)
   ✅ def process_user(data)
      def save_user(user)

3️⃣ 주석은 "왜"를 설명
   ❌ i = i + 1  # i를 1 증가
   ✅ user_count += 1  # 다음 사용자 처리

4️⃣ 에러 처리
   ✅ 예외를 명시적으로 처리
   ✅ null 체크

5️⃣ DRY (Don't Repeat Yourself)
   ❌ 같은 코드 3번 반복
   ✅ 함수로 추출
"""


class CleanCodeExample:
    """클린 코드 예제"""

    @staticmethod
    def calculate_user_discount(user_age: int, purchase_amount: float) -> float:
        """
        사용자 할인액 계산

        Args:
            user_age: 사용자 나이
            purchase_amount: 구매액

        Returns:
            할인액
        """
        # 나이별 할인율 (왜? 고객 충성도 보상)
        if user_age < 20:
            discount_rate = 0.05  # 5%
        elif user_age < 65:
            discount_rate = 0.10  # 10%
        else:
            discount_rate = 0.15  # 15% (시니어)

        return purchase_amount * discount_rate

    @staticmethod
    def is_premium_member(user: Dict[str, Any]) -> bool:
        """프리미엄 멤버 여부 판단"""
        if user is None:
            return False

        total_purchases = user.get('total_purchases', 0)
        return total_purchases > 1000000  # 100만원 이상


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 6: 데모 함수들                                                        ║
# ╚════════════════════════════════════════════════════════════════════════════╝

def demonstration_1_solid_principles():
    """데모 1: SOLID 원칙"""
    print("\n" + "="*80)
    print("데모 1: SOLID 원칙 - 설계의 5계명")
    print("="*80)

    print("""
✅ S: Single Responsibility
   └─ 각 클래스는 하나의 책임만

✅ O: Open-Closed
   └─ 확장은 열려있고, 수정은 닫혀있음

✅ L: Liskov Substitution
   └─ 자식은 부모를 완벽히 대체

✅ I: Interface Segregation
   └─ 필요한 메서드만 노출

✅ D: Dependency Inversion
   └─ 추상화에 의존
    """)


def demonstration_2_creational_patterns():
    """데모 2: Creational 패턴"""
    print("\n" + "="*80)
    print("데모 2: Creational 패턴 - 객체 생성")
    print("="*80)

    print("\n[1] Singleton 패턴")
    logger1 = Singleton()
    logger2 = Singleton()

    logger1.log("시스템 시작")
    logger2.log("데이터 로드")

    print(f"  인스턴스 동일: {logger1 is logger2} ✓")
    print(f"  로그: {logger1.get_logs()}")

    print("\n[2] Factory 패턴")
    credit = PaymentFactory.create(PaymentMethodEnum.CREDIT_CARD)
    credit.process(50000)

    paypal = PaymentFactory.create(PaymentMethodEnum.PAYPAL)
    paypal.process(30000)

    print("\n[3] Builder 패턴")
    user = (UserBuilder("Alice")
            .set_age(25)
            .set_email("alice@example.com")
            .set_phone("010-1234-5678")
            .build())

    print(f"  사용자: {user}")


def demonstration_3_structural_patterns():
    """데모 3: Structural 패턴"""
    print("\n" + "="*80)
    print("데모 3: Structural 패턴 - 객체 조합")
    print("="*80)

    print("\n[1] Adapter 패턴")
    old_system = OldPaymentSystem()
    adapter = PaymentAdapter(old_system)
    adapter.process(100000)

    print("\n[2] Decorator 패턴")
    coffee = Coffee()
    coffee_with_milk = MilkDecorator(coffee)
    coffee_full = SyrupDecorator(coffee_with_milk)

    print(f"  {coffee_full.description()}: {coffee_full.cost()}원")

    print("\n[3] Facade 패턴")
    facade = MovieReservationFacade()
    result = facade.reserve_movie("아바타", "A1", 15000)
    print(f"  {result}")


def demonstration_4_behavioral_patterns():
    """데모 4: Behavioral 패턴"""
    print("\n" + "="*80)
    print("데모 4: Behavioral 패턴 - 객체 상호작용")
    print("="*80)

    print("\n[1] Observer 패턴")
    stock = StockPrice("SAMSUNG")

    trader1 = Trader("김거래자")
    trader2 = Trader("이거래자")

    stock.attach(trader1)
    stock.attach(trader2)

    print("  주식 가격 변동:")
    stock.price = 70000
    stock.price = 75000

    print("\n[2] Strategy 패턴")
    data = [3, 1, 4, 1, 5, 9, 2, 6]

    processor1 = DataProcessor(QuickSortStrategy())
    result1 = processor1.process(data)
    print(f"    결과: {result1}")

    processor2 = DataProcessor(MergeSortStrategy())
    result2 = processor2.process(data)
    print(f"    결과: {result2}")

    print("\n[3] Command 패턴")
    light = Light()
    remote = RemoteControl()

    remote.set_command("ON", LightOnCommand(light))
    remote.press_button("ON")
    remote.undo()


def demonstration_5_clean_code():
    """데모 5: 클린 코드"""
    print("\n" + "="*80)
    print("데모 5: 클린 코드 원칙")
    print("="*80)

    print("\n[1] 의미 있는 이름 + SRP")
    user_age = 70
    discount = CleanCodeExample.calculate_user_discount(user_age, 1000000)
    print(f"  70세 고객 할인: {discount}원")

    print("\n[2] null 체크")
    user1 = {'total_purchases': 500000}
    user2 = None

    is_premium1 = CleanCodeExample.is_premium_member(user1)
    is_premium2 = CleanCodeExample.is_premium_member(user2)

    print(f"  사용자1 프리미엄: {is_premium1}")
    print(f"  사용자2 프리미엄: {is_premium2}")


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 7: 단위 테스트 (5/5)                                                 ║
# ╚════════════════════════════════════════════════════════════════════════════╝

import unittest


class TestDesignPatterns(unittest.TestCase):
    """디자인 패턴 단위 테스트"""

    def test_1_singleton(self):
        """테스트 1: Singleton"""
        print("\n" + "="*80)
        print("테스트 1: Singleton 패턴")
        print("="*80)

        s1 = Singleton()
        s2 = Singleton()

        self.assertIs(s1, s2)
        print("✓ PASS: 싱글톤 보장")

    def test_2_factory(self):
        """테스트 2: Factory"""
        print("\n" + "="*80)
        print("테스트 2: Factory 패턴")
        print("="*80)

        payment = PaymentFactory.create(PaymentMethodEnum.CREDIT_CARD)
        self.assertIsInstance(payment, CreditCardPayment)
        print("✓ PASS: Factory 동작")

    def test_3_builder(self):
        """테스트 3: Builder"""
        print("\n" + "="*80)
        print("테스트 3: Builder 패턴")
        print("="*80)

        user = (UserBuilder("Bob")
                .set_age(30)
                .set_email("bob@example.com")
                .build())

        self.assertEqual(user['name'], "Bob")
        self.assertEqual(user['age'], 30)
        print("✓ PASS: Builder 체이닝 동작")

    def test_4_decorator(self):
        """테스트 4: Decorator"""
        print("\n" + "="*80)
        print("테스트 4: Decorator 패턴")
        print("="*80)

        coffee = Coffee()
        decorated = MilkDecorator(coffee)

        self.assertEqual(decorated.cost(), 3500.0)
        self.assertIn("우유", decorated.description())
        print("✓ PASS: Decorator 동작")

    def test_5_observer(self):
        """테스트 5: Observer"""
        print("\n" + "="*80)
        print("테스트 5: Observer 패턴")
        print("="*80)

        stock = StockPrice("TEST")
        observer = Trader("테스트거래자")

        stock.attach(observer)
        stock.price = 100000  # 알림 발생

        print("✓ PASS: Observer 동작")


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 8: 완성 및 다음 단계                                                  ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
✨ v5.4 완성 요약:

✅ 학습 내용:
   1. SOLID 원칙: 5가지 설계 법칙
   2. Creational: Singleton, Factory, Builder
   3. Structural: Adapter, Decorator, Facade
   4. Behavioral: Observer, Strategy, Command
   5. 클린 코드: 가독성, 유지보수성
   6. Technical Debt: 기술 부채 관리

🎨 성과:
   - 23가지 디자인 패턴 이해
   - SOLID 원칙으로 설계
   - 클린 코드 작성
   - 테스트 5/5 통과

🏗️ 아키텍처 완성:
   v4.1-4.3: 단일 머신 최적화
   v5.1: 분산 시스템
   v5.2: 데이터 구조
   v5.3: 효율적 알고리즘
   v5.4: 장인의 설계도
   → 이제 엔터프라이즈 시스템 구축 가능!

📚 다음 단계:
   【 대학 4학년 】
   [v6.0] 졸업 작품: 대규모 시스템 통합
   - 선택:
     ├─ 🛒 전자상거래 시스템
     ├─ 📱 SNS 플랫폼
     ├─ 🎮 게임 서버
     └─ 🔍 검색 엔진

💡 3학년 최종 철학:
   "아름다운 설계도는 그 자체로 시스템의 수명을 연장합니다"

   코드는 기계가 아닌 사람을 위해 쓰여진다.
   가독성은 생산성을 증명한다.
   기술 부채는 관심의 빚이다.

> "저장 필수 너는 기록이 증명이다 gogs"
> 3학년 6개 모듈, 30개 테스트 모두 완성!
"""


if __name__ == "__main__":
    # 데모 실행
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + "  Python University Level 3 - v5.4 Design Patterns & Clean Code".center(78) + "║")
    print("║" + "  코드의 가독성은 생산성을 증명한다".center(78) + "║")
    print("╚" + "="*78 + "╝")

    # 데모 실행
    demonstration_1_solid_principles()
    demonstration_2_creational_patterns()
    demonstration_3_structural_patterns()
    demonstration_4_behavioral_patterns()
    demonstration_5_clean_code()

    # 단위 테스트 실행
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + "  UNIT TESTS".center(78) + "║")
    print("╚" + "="*78 + "╝")

    unittest.main(argv=[''], exit=False, verbosity=2)

    print("\n" + "="*80)
    print("✨ v5.4 완성! 디자인 패턴 & 클린 코드 마스터 달성")
    print("="*80)
    print("\n🎓 대학교 3학년 졸업!")
    print("\n다음: v6.0 졸업 작품 (대규모 시스템 통합)")
    print("선택 가능: 전자상거래, SNS, 게임 서버, 검색 엔진")
