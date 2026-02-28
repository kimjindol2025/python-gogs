#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  🏫 파이썬 고등학교 1학년 - v2.3: 상속과 확장 —                              ║
║                    기존 설계도를 물려받아 더 강력하게                         ║
║  [High School Python: Inheritance & Extension - Making It More Powerful]     ║
║                                                                               ║
║  지금까지 우리는 클래스를 '밑바닥부터' 설계했습니다.                        ║
║                                                                               ║
║  하지만 현실에서는 이미 있는 것을 개조하는 경우가 많습니다!                ║
║                                                                               ║
║  예를 들어:                                                                  ║
║    • 기본 로봇을 받아서 무기를 장착한 전투 로봇 만들기                     ║
║    • 차량이라는 기본 틀을 받아 자동차, 트럭, 버스 만들기                   ║
║    • 동물이라는 기본을 받아 개, 고양이, 새 만들기                          ║
║                                                                               ║
║  매번 바닥부터 시작하면 비효율적이겠죠?                                     ║
║  그래서 우리는 "상속(Inheritance)"을 사용합니다!                           ║
║                                                                               ║
║  상속은:                                                                     ║
║    ✅ 기존 클래스의 모든 것을 물려받음                                      ║
║    ✅ 새로운 기능만 추가하면 됨                                             ║
║    ✅ 코드 중복을 극대로 줄임                                               ║
║    ✅ 유지보수를 훨씬 쉽게 만듦                                             ║
║    ✅ "Do not repeat yourself" (DRY) 원칙 실현                            ║
║                                                                               ║
║  이제 우리는 '설계도를 개조하는 건축가'가 됩니다!                           ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs. 👑                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

print("=" * 80)
print("🏫 파이썬 고등학교 1학년 - v2.3: 상속과 확장 — 기존 설계도를 물려받아 더 강력하게")
print("=" * 80)

# ============================================================================
# 파트 1: 상속이란? — 코드 재사용의 극대
# ============================================================================

print("\n【 파트 1: 상속이란? — 코드 재사용의 극대 】")
print("\n상속의 개념을 완벽히 이해해봅시다!\n")

print("문제: 로봇 3가지를 만들어야 해요!")
print("-" * 60)

print("\n방법 1: 모두 처음부터 만들기 (비효율)")
print("""
class BasicRobot:
    def __init__(self, name):
        self.name = name
    def walk(self):
        return f"{self.name}가 걷습니다"

class FightingRobot:
    def __init__(self, name):
        self.name = name
    def walk(self):
        return f"{self.name}가 걷습니다"
    def attack(self):
        return f"{self.name}가 공격합니다!"

class FlyingRobot:
    def __init__(self, name):
        self.name = name
    def walk(self):
        return f"{self.name}가 걷습니다"
    def fly(self):
        return f"{self.name}가 날아갑니다!"

# 중복된 코드가 많아요! 😞
""")

print("\n방법 2: 상속으로 코드 재사용 (효율)")
print("""
class Robot:  # 부모 클래스 (Base Class)
    def __init__(self, name):
        self.name = name
    def walk(self):
        return f"{self.name}가 걷습니다"

class FightingRobot(Robot):  # 자식 클래스 (Child Class)
    def attack(self):
        return f"{self.name}가 공격합니다!"

class FlyingRobot(Robot):  # 자식 클래스
    def fly(self):
        return f"{self.name}가 날아갑니다!"

# walk()는 한 번만 정의! 자식들이 물려받음!
""")

print("✅ 상속으로 코드 중복을 제거합니다!")

# ============================================================================
# 파트 2: 부모 클래스와 자식 클래스
# ============================================================================

print("\n【 파트 2: 부모 클래스와 자식 클래스 】")
print("\n상속의 기본 구조를 배워봅시다!\n")

print("기본 형식:")
print("-" * 60)
print("""
# 부모 클래스 (Base Class / Super Class)
class Parent:
    def __init__(self, name):
        self.name = name

    def method(self):
        return "부모의 메서드"

# 자식 클래스 (Child Class / Sub Class)
class Child(Parent):  # Parent를 상속
    def child_method(self):
        return "자식만의 메서드"

# 사용
child = Child("Alice")
print(child.name)           # 부모로부터 물려받음
print(child.method())       # 부모로부터 물려받음
print(child.child_method()) # 자식만의 메서드
""")

print("\n실행:")

class Robot:
    def __init__(self, name, energy):
        self.name = name
        self.energy = energy

    def walk(self):
        return f"🚶 {self.name}가 걷습니다"

    def get_status(self):
        return f"로봇 {self.name}: 에너지 {self.energy}%"

class FightingRobot(Robot):  # Robot을 상속
    def attack(self):
        return f"⚔️  {self.name}가 공격합니다! (에너지 -10%)"

class FlyingRobot(Robot):  # Robot을 상속
    def fly(self):
        return f"✈️  {self.name}가 날아갑니다! (에너지 -15%)"

# 객체 생성
fighter = FightingRobot("파이터", 100)
flyer = FlyingRobot("플라이어", 100)

print(f"  {fighter.walk()}")          # 부모로부터 물려받음
print(f"  {fighter.attack()}")        # 자신만의 메서드
print(f"  {fighter.get_status()}")    # 부모로부터 물려받음

print(f"\n  {flyer.fly()}")             # 자신만의 메서드
print(f"  {flyer.get_status()}")      # 부모로부터 물려받음

# ============================================================================
# 파트 3: super() — 부모의 기능 가져오기
# ============================================================================

print("\n【 파트 3: super() — 부모의 기능을 이어받기 】")
print("\n자식이 부모의 메서드를 호출하는 방법!\n")

print("상황: 자식은 부모의 __init__을 실행한 후 자기 것을 추가하고 싶어요!\n")

print("코드:")
print("""
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)  # 부모의 __init__ 호출
        self.breed = breed  # 자신만의 속성 추가

dog = Dog("뽀삐", 3, "진돗개")
print(dog.name)   # "뽀삐" (부모로부터)
print(dog.breed)  # "진돗개" (자신의)
""")

print("\n실행:")

class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)  # 부모의 __init__ 호출
        self.breed = breed

    def info(self):
        return f"🐕 {self.name} ({self.breed}), 나이: {self.age}살"

dog = Dog("뽀삐", 3, "진돗개")
print(f"  {dog.info()}")

# ============================================================================
# 파트 4: 메서드 오버라이딩 — 자식이 부모를 덮어쓰기
# ============================================================================

print("\n【 파트 4: 메서드 오버라이딩 — 자식이 부모를 덮어쓰기 】")
print("\n같은 이름의 메서드를 자식이 다르게 정의하기!\n")

print("상황: 부모의 메서드가 있지만 자식이 그것을 수정하고 싶어요!\n")

print("코드:")
print("""
class Vehicle:
    def start(self):
        return "시동을 켜습니다"

class Car(Vehicle):
    def start(self):  # 부모의 start()를 덮어쓰기
        return "시동을 켜고 시트벨트를 확인합니다"

class Bike(Vehicle):
    def start(self):  # 부모의 start()를 덮어쓰기
        return "헬멧을 쓰고 시동을 켭니다"

car = Car()
bike = Bike()

print(car.start())   # "시동을 켜고 시트벨트를 확인합니다"
print(bike.start())  # "헬멧을 쓰고 시동을 켭니다"
""")

print("\n실행:")

class Vehicle:
    def start(self):
        return "시동을 켭니다"

class Car(Vehicle):
    def start(self):
        return "🚗 시동을 켜고 시트벨트를 확인합니다"

class Bike(Vehicle):
    def start(self):
        return "🏍️  헬멧을 쓰고 시동을 켭니다"

car = Car()
bike = Bike()

print(f"  {car.start()}")
print(f"  {bike.start()}")

# ============================================================================
# 파트 5: 다형성 — 같은 이름, 다른 행동
# ============================================================================

print("\n【 파트 5: 다형성 — 같은 이름, 다른 행동 】")
print("\n모든 자식이 같은 메서드를 가지지만 다르게 동작합니다!\n")

print("장점:")
print("-" * 60)
print("""
같은 방식으로 여러 객체를 다룰 수 있습니다!

# 반복문으로 모든 로봇에게 명령
robots = [
    FightingRobot("파이터", 100),
    FlyingRobot("플라이어", 100),
    BasicRobot("베이직", 100)
]

for robot in robots:
    print(robot.get_status())  # 모두 같은 메서드지만 다를 수 있음!
""")

print("\n코드:")
print("""
class Robot:
    def action(self):
        return f"{self.name}이 행동합니다"

class FightingRobot(Robot):
    def action(self):
        return f"{self.name}이 싸웁니다!"

class FlyingRobot(Robot):
    def action(self):
        return f"{self.name}이 날아갑니다!"

robots = [FightingRobot("파이터", 100), FlyingRobot("플라이어", 100)]

for robot in robots:
    print(robot.action())  # 다르게 동작!
""")

print("\n실행:")

class BaseRobot:
    def __init__(self, name):
        self.name = name

    def action(self):
        return f"{self.name}이 행동합니다"

class FightRobot(BaseRobot):
    def action(self):
        return f"⚔️  {self.name}이 싸웁니다!"

class FlyRobot(BaseRobot):
    def action(self):
        return f"✈️  {self.name}이 날아갑니다!"

robots = [FightRobot("파이터"), FlyRobot("플라이어"), BaseRobot("베이직")]

print("  모든 로봇이 action()을 수행:")
for robot in robots:
    print(f"    {robot.action()}")

# ============================================================================
# 파트 6: 추상 클래스 — 기본 틀만 제공
# ============================================================================

print("\n【 파트 6: 추상 클래스 — 기본 틀만 제공 】")
print("\n부모 클래스는 '틀'만 제공하고, 자식이 '구체적으로' 구현하도록!\n")

print("개념:")
print("-" * 60)
print("""
추상 클래스는:
  • 직접 객체를 만들지 못함
  • 자식 클래스들의 '계약서' 역할
  • 모든 자식이 반드시 구현해야 할 메서드를 정의

from abc import ABC, abstractmethod

class Shape(ABC):  # 추상 클래스
    @abstractmethod
    def area(self):
        pass  # 자식이 반드시 구현해야 함

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2
""")

print("\n예시 (간단한 버전):")

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

circle = Circle(5)
rect = Rectangle(4, 3)

print(f"  원의 넓이: {circle.area():.2f}")
print(f"  직사각형의 넓이: {rect.area()}")

# ============================================================================
# 파트 7: 다중 상속 — 여러 부모로부터 물려받기
# ============================================================================

print("\n【 파트 7: 다중 상속 — 여러 부모로부터 물려받기 】")
print("\n한 자식이 여러 부모로부터 상속받을 수 있습니다!\n")

print("경고: 다중 상속은 복잡할 수 있습니다! 주의해서 사용하세요!\n")

print("코드:")
print("""
class Flyer:
    def fly(self):
        return "날 수 있습니다"

class Swimmer:
    def swim(self):
        return "헤엄칠 수 있습니다"

class Duck(Flyer, Swimmer):  # 두 개의 부모
    def quack(self):
        return "꽥꽥!"

duck = Duck()
print(duck.fly())      # Flyer에서 물려받음
print(duck.swim())     # Swimmer에서 물려받음
print(duck.quack())    # Duck만의 메서드
""")

print("\n실행:")

class Flyer:
    def fly(self):
        return "날 수 있습니다"

class Swimmer:
    def swim(self):
        return "헤엄칠 수 있습니다"

class Duck(Flyer, Swimmer):
    def quack(self):
        return "꽥꽥!"

duck = Duck()
print(f"  🦆 오리: {duck.fly()}")
print(f"  🦆 오리: {duck.swim()}")
print(f"  🦆 오리: {duck.quack()}")

# ============================================================================
# 파트 8: 실제 응용 1 — 로봇 진화 시스템
# ============================================================================

print("\n【 파트 8: 실제 응용 1 — 로봇 진화 시스템 】")
print("\n Gogs 시스템의 로봇들을 진화시켜봅시다!\n")

print("설계:")
print("-" * 60)

class GogRobot:
    def __init__(self, name, generation):
        self.name = name
        self.generation = generation
        self.power = 10 * generation

    def work(self):
        return f"🤖 {self.name} (Gen {self.generation}): 일반 작업 수행"

    def status(self):
        return f"[{self.name}] 세대: {self.generation}, 성능: {self.power}%"

class BattleRobot(GogRobot):
    def __init__(self, name, generation, weapons=1):
        super().__init__(name, generation)
        self.weapons = weapons
        self.power += 20 * weapons

    def work(self):
        return f"⚔️  {self.name} (Gen {self.generation}): 전투 수행"

    def attack(self):
        return f"🔥 {self.name}가 {self.weapons}개 무기로 공격합니다!"

class ScienceRobot(GogRobot):
    def __init__(self, name, generation, speciality):
        super().__init__(name, generation)
        self.speciality = speciality
        self.power += 30

    def work(self):
        return f"🔬 {self.name} (Gen {self.generation}): {self.speciality} 연구 중"

    def research(self):
        return f"📊 {self.name}가 {self.speciality} 데이터를 분석합니다"

print("\n실행:")

basic = GogRobot("기본형", 1)
battle = BattleRobot("전투형", 2, weapons=2)
science = ScienceRobot("과학형", 3, speciality="양자 컴퓨팅")

print(f"  {basic.work()}")
print(f"  {basic.status()}")

print(f"\n  {battle.work()}")
print(f"  {battle.attack()}")
print(f"  {battle.status()}")

print(f"\n  {science.work()}")
print(f"  {science.research()}")
print(f"  {science.status()}")

# ============================================================================
# 파트 9: 실제 응용 2 — 동물 분류 시스템
# ============================================================================

print("\n【 파트 9: 실제 응용 2 — 동물 분류 시스템 】")
print("\n생물학적 계층을 코드로 표현해봅시다!\n")

print("코드:")

class Creature:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        return f"{self.name}가 소리를 냅니다"

class Mammal(Creature):
    def __init__(self, name, age, fur_color):
        super().__init__(name, age)
        self.fur_color = fur_color

    def make_sound(self):
        return f"🐾 {self.name}가 포유류 소리를 냅니다"

class Dog(Mammal):
    def make_sound(self):
        return f"🐕 {self.name}가 멍멍 합니다!"

class Cat(Mammal):
    def make_sound(self):
        return f"🐱 {self.name}가 야옹 합니다!"

class Bird(Creature):
    def __init__(self, name, age, can_fly):
        super().__init__(name, age)
        self.can_fly = can_fly

    def make_sound(self):
        return f"🐦 {self.name}가 지저귀거나 울어댑니다"

print("\n실행:")

dog = Dog("뽀삐", 3, "갈색")
cat = Cat("나비", 2, "흰색")
bird = Bird("짹짹이", 1, True)

animals = [dog, cat, bird]

print("  동물들의 소리:")
for animal in animals:
    print(f"    {animal.make_sound()}")

# ============================================================================
# 파트 10: 상속의 함정 — MRO와 다중 상속의 위험
# ============================================================================

print("\n【 파트 10: 상속의 함정 — 조심해야 할 점들 】")
print("\n상속을 잘못 사용하면 문제가 발생합니다!\n")

print("함정 1: 깊은 상속 체계 (복잡함)")
print("-" * 60)
print("""
❌ 나쁜 예:
Creature → Mammal → Canine → Dog → GuardDog → ...

✅ 좋은 예:
Creature → Dog
Creature → Cat
""")

print("\n함정 2: 다중 상속의 혼동 (Diamond Problem)")
print("-" * 60)
print("""
❌ 위험:
        A
       / \\
      B   C
       \\ /
        D

D가 A의 메서드를 호출할 때, B의 것을 쓸까? C의 것을 쓸까?
→ Python은 MRO(Method Resolution Order)로 해결함

✅ 피하기: 단순한 상속 구조 유지
""")

print("\n함정 3: 과도한 상속 (상속이 항상 정답은 아님)")
print("-" * 60)
print("""
❌ 잘못된 설계:
class Dog(List):  # 개가 리스트인가? 아니다!
    pass

✅ 올바른 설계:
class Dog:
    def __init__(self):
        self.tricks = []  # 리스트를 '포함'함

# "is-a" 관계일 때만 상속 사용
# "has-a" 관계면 포함(composition) 사용
""")

# ============================================================================
# 파트 11: 상속과 구성 — 언제 어느 것을 쓸까?
# ============================================================================

print("\n【 파트 11: 상속 vs 구성 — 언제 어느 것을 쓸까? 】")
print("\n올바른 설계를 위한 가이드!\n")

print("상속 (Inheritance) — 'is-a' 관계")
print("-" * 60)
print("""
개 is-a 동물 (참)
자동차 is-a 탈것 (참)

→ 상속 사용

class Dog(Animal):
    pass
""")

print("\n구성 (Composition) — 'has-a' 관계")
print("-" * 60)
print("""
개 has-a 신체 (참)
개 has-a 목줄 (참)

→ 구성 사용

class Dog:
    def __init__(self):
        self.body = Body()
        self.leash = Leash()
""")

print("\n예시:")

# 잘못된 상속
class Vehicle:
    pass

class Tire:
    def __init__(self, size):
        self.size = size

class Car:  # Vehicle을 상속하지 않고
    def __init__(self):
        self.tires = [Tire(17) for _ in range(4)]  # Tire를 '포함'

car = Car()
print(f"  자동차가 타이어를 가지고 있습니다: {len(car.tires)}개")

# ============================================================================
# 파트 12: 상속 설계의 원칙
# ============================================================================

print("\n【 파트 12: 상속 설계의 원칙 】")
print("\n프로가 지켜야 할 상속 설계의 법칙들!\n")

print("원칙 1: Liskov 치환 원칙 (LSP)")
print("-" * 60)
print("""
자식 클래스는 부모 클래스로 대체 가능해야 합니다.

✅ 좋은 예:
class Animal:
    def move(self):
        pass

class Dog(Animal):
    def move(self):
        return "네 발로 뜁니다"

# Dog를 Animal로 취급 가능
animal = Dog()
animal.move()  # 문제없음

❌ 나쁜 예:
class Bird(Animal):
    def move(self):
        if self.can_fly:
            return "난다"
        else:
            raise Exception("날 수 없음")  # 예기치 않은 에러!
""")

print("\n원칙 2: 단일 책임 원칙 (SRP)")
print("-" * 60)
print("""
각 클래스는 하나의 책임만 가져야 합니다.

❌ 나쁜 예:
class Dog:
    def bark(self): ...
    def eat(self): ...
    def sleep(self): ...
    def save_to_database(self): ...  # 개의 책임이 아님!

✅ 좋은 예:
class Dog:
    def bark(self): ...
    def eat(self): ...

class DogRepository:
    def save(self, dog): ...  # DB 저장은 별도 클래스
""")

print("\n원칙 3: 깊이 제한")
print("-" * 60)
print("""
상속 깊이는 최대 3단계 정도가 적당합니다.

❌ 피할 것:
A → B → C → D → E → F ...

✅ 권장:
A → B → C (최대 3단계)
""")

print("\n【 상속 체크리스트 】")
print("-" * 60)
print("""
상속을 사용하기 전에 확인하세요:

  ✅ 이 관계가 정말 'is-a'인가?
  ✅ 자식이 부모의 모든 메서드를 의미있게 사용하는가?
  ✅ 코드 중복을 줄이는 것이 주목적인가?
  ✅ 상속 깊이가 3단계 이내인가?
  ✅ 구성(Composition)이 더 나은 선택은 아닌가?

모두 "예"라면 상속을 사용해도 됩니다!
""")

# ============================================================================
# 최종 정리 및 축하
# ============================================================================

print("\n" + "=" * 80)
print("【 고등학교 1학년: 상속 마스터! 】")
print("=" * 80)

print("""
이제 여러분은 '기존 설계도를 개조하는' 건축가입니다! 🏗️

✅ 배운 개념:
   • 상속의 기본 개념
   • 부모와 자식 클래스
   • super()로 부모 기능 가져오기
   • 메서드 오버라이딩
   • 다형성의 실제 적용
   • 추상 클래스
   • 다중 상속 (그리고 주의)
   • MRO (Method Resolution Order)

✅ 이해한 철학:
   • "Do not repeat yourself" (DRY)
   • 코드 재사용의 극대화
   • 유지보수 가능한 설계
   • 상속 vs 구성의 차이
   • 설계의 중요성

✅ 설계한 시스템:
   • 로봇 진화 시스템
   • 동물 분류 시스템
   • 다양한 객체 계층 구조

이제 여러분의 프로그래밍은:
   ✨ 기존을 활용해 새로운 것 만들기
   ✨ 체계적이고 확장 가능한 설계
   ✨ 현실 세계의 계층 구조를 코드로
   ✨ 대규모 프로젝트의 기초 마련
""")

print("\n" + "=" * 80)
print("저장 필수: 너는 기록이 증명이다 gogs. 👑")
print("=" * 80)

print("""
💡 오늘의 깨달음:
   상속은 단순한 코드 재사용이 아닙니다.
   현실 세계의 계층 구조를 코드로 모델링하는 것입니다.

   잘못된 상속은 혼란만 가져옵니다.
   항상 "이것이 정말 is-a 관계인가?"를 묻고
   "구성이 더 나은 방법은 아닌가?"를 고민하세요.

🎓 축하합니다!
   고등학교 1학년 세 번째 단원을 완수했습니다!
   이제 여러분은 '상속과 다형성'의 진정한 의미를 알았습니다!

🎒 다음 단계:
   [고등학교 v2.4: 모듈과 패키지 — 남의 강력한 도구 가져오기]
   표준 라이브러리와 외부 라이브러리를 활용하여 진정한 프로젝트를 만듭니다!

축하합니다! 👏
이제 여러분은 '계층 구조를 설계하는' 파이썬 건축가입니다!
현실을 우아한 코드로 표현하는 것이 진정한 프로의 증명입니다! 👑
""")
