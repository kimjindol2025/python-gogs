#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  🏫 파이썬 고등학교 1학년 - v2.2: 클래스와 객체 지향 —                       ║
║                    나만의 데이터 타입과 객체 설계하기                         ║
║  [High School Python: Class and OOP - Designing Your Own Data Types]         ║
║                                                                               ║
║  지금까지 우리는 파이썬이 제공하는 '기본' 타입들을 사용했습니다.            ║
║    • int, float, str (숫자, 문자)                                           ║
║    • list, dict, tuple, set (컨테이너)                                      ║
║                                                                               ║
║  하지만 우리만의 타입을 만들 수는 없을까요?                                  ║
║                                                                               ║
║  예를 들어:                                                                  ║
║    • 학생이라는 새로운 타입                                                  ║
║    • 은행 계좌라는 새로운 타입                                              ║
║    • 우주선이라는 새로운 타입                                                ║
║                                                                               ║
║  현실의 것들을 코드로 표현하고 싶다면?                                       ║
║  그것이 바로 "클래스(Class)"입니다! 🎯                                      ║
║                                                                               ║
║  클래스는:                                                                   ║
║    ✅ 현실의 것들을 코드로 모델링                                           ║
║    ✅ 자신의 속성(데이터)과 메서드(행동)를 가짐                            ║
║    ✅ 거대한 시스템을 작고 관리 가능한 조각으로 나눔                       ║
║    ✅ 코드 재사용을 극대화                                                  ║
║    ✅ 프로의 세계로 가는 첫걸음                                              ║
║                                                                               ║
║  파이썬의 철학: "모든 것이 객체다!"                                          ║
║  이제 우리도 우리만의 객체를 만들 차례입니다!                               ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs. 👑                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

print("=" * 80)
print("🏫 파이썬 고등학교 1학년 - v2.2: 클래스와 객체 지향 — 나만의 데이터 타입 설계하기")
print("=" * 80)

# ============================================================================
# 파트 1: 객체 지향 프로그래밍이란? — 현실을 코드로 표현하다
# ============================================================================

print("\n【 파트 1: 객체 지향 프로그래밍이란? — 현실을 코드로 표현하다 】")
print("\n객체 지향 프로그래밍(OOP)의 핵심을 이해해봅시다!\n")

print("문제: 학생을 표현해야 해요!")
print("-" * 60)

print("\n방법 1: 중학교 방식 (번거로움)")
print("""
# 각각을 따로 관리해야 함
name1 = "Alice"
age1 = 17
grade1 = 3.8
phone1 = "010-1234-5678"

name2 = "Bob"
age2 = 17
grade2 = 3.5
phone2 = "010-2345-6789"

# 학생이 100명이면? 😱
""")

print("\n방법 2: 고등학교 방식 (우아함) — 클래스 사용!")
print("""
class Student:
    def __init__(self, name, age, grade, phone):
        self.name = name
        self.age = age
        self.grade = grade
        self.phone = phone

    def introduce(self):
        return f"안녕, 나는 {self.name}이고 학점은 {self.grade}입니다!"

alice = Student("Alice", 17, 3.8, "010-1234-5678")
bob = Student("Bob", 17, 3.5, "010-2345-6789")

# 학생 100명도 같은 방식으로!
""")

print("✅ 클래스는 현실의 것들을 코드로 우아하게 표현합니다!")

# ============================================================================
# 파트 2: 클래스 기본 — class로 시작하기
# ============================================================================

print("\n【 파트 2: 클래스 기본 — class로 시작하기 】")
print("\n가장 간단한 클래스부터 시작해봅시다!\n")

print("기본 형식:")
print("-" * 60)
print("""
class 클래스이름:
    def __init__(self, 속성1, 속성2):
        self.속성1 = 속성1
        self.속성2 = 속성2

    def 메서드이름(self):
        # 객체가 할 수 있는 행동
        pass
""")

print("\n예시: 가장 간단한 강아지 클래스")
print("-" * 60)

print("\n코드:")
print("""
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name}가 멍멍 합니다!"

# 강아지 객체 생성
my_dog = Dog("뽀삐", 3)
print(my_dog.bark())
""")

print("\n실행:")

class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name}가 멍멍 합니다!"

my_dog = Dog("뽀삐", 3)
print(f"  {my_dog.bark()}")
print(f"  강아지 이름: {my_dog.name}")
print(f"  강아지 나이: {my_dog.age}")

# ============================================================================
# 파트 3: 생성자 (__init__) — 객체 초기화
# ============================================================================

print("\n【 파트 3: 생성자 (__init__) — 객체 초기화 】")
print("\n모든 객체는 '태어나는 순간'이 있습니다!\n")

print("생성자(Constructor)란?")
print("-" * 60)
print("""
__init__은 객체가 생성될 때 자동으로 호출되는 특별한 메서드입니다.

class Student:
    def __init__(self, name, student_id):
        # 여기서 초기화!
        self.name = name
        self.student_id = student_id

# 객체 생성 → __init__ 자동 호출
student = Student("Alice", 12345)
""")

print("\n예시: 학생 클래스")
print("-" * 60)

print("\n코드:")
print("""
class Student:
    def __init__(self, name, student_id, major):
        self.name = name
        self.student_id = student_id
        self.major = major
        self.gpa = 0.0  # 기본값

alice = Student("Alice", 001, "Computer Science")
bob = Student("Bob", 002, "Mathematics")
""")

print("\n실행:")

class Student:
    def __init__(self, name, student_id, major):
        self.name = name
        self.student_id = student_id
        self.major = major
        self.gpa = 0.0

alice = Student("Alice", 1001, "Computer Science")
bob = Student("Bob", 1002, "Mathematics")

print(f"  학생 1: {alice.name} ({alice.major})")
print(f"  학생 2: {bob.name} ({bob.major})")

# ============================================================================
# 파트 4: 메서드 — 객체의 행동
# ============================================================================

print("\n【 파트 4: 메서드 — 객체의 행동 】")
print("\n객체가 할 수 있는 행동(메서드)을 정의해봅시다!\n")

print("메서드란?")
print("-" * 60)
print("""
메서드는 클래스 내부의 함수입니다.
객체가 할 수 있는 행동을 정의합니다.

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        # 입금 행동
        self.balance += amount
        return f"{amount}원 입금 완료"

    def withdraw(self, amount):
        # 출금 행동
        if amount <= self.balance:
            self.balance -= amount
            return f"{amount}원 출금 완료"
        return "잔액 부족"
""")

print("\n실행:")

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return f"✅ {amount}원 입금 완료! (잔액: {self.balance}원)"

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return f"✅ {amount}원 출금 완료! (잔액: {self.balance}원)"
        return f"❌ 잔액 부족 (현재: {self.balance}원)"

    def check_balance(self):
        return f"현재 잔액: {self.balance}원"

account = BankAccount("Alice", 10000)
print(f"  {account.deposit(5000)}")
print(f"  {account.withdraw(3000)}")
print(f"  {account.withdraw(20000)}")

# ============================================================================
# 파트 5: 속성과 메서드 — 데이터와 행동의 조화
# ============================================================================

print("\n【 파트 5: 속성과 메서드 — 데이터와 행동의 조화 】")
print("\n객체의 '특성'과 '행동'을 구분해봅시다!\n")

print("개념 정리:")
print("-" * 60)
print("""
속성 (Attribute): 객체의 '특성'
  • self.name = "Alice"
  • self.age = 17
  • self.balance = 10000

메서드 (Method): 객체의 '행동'
  • def introduce(self): ...
  • def bark(self): ...
  • def deposit(self, amount): ...
""")

print("\n예시: 자동차 클래스")
print("-" * 60)

print("\n코드:")
print("""
class Car:
    def __init__(self, brand, model, speed):
        # 속성들
        self.brand = brand
        self.model = model
        self.speed = speed
        self.is_running = False

    def start(self):
        # 행동 1: 시동 걸기
        self.is_running = True
        return f"{self.brand} {self.model}이 시동되었습니다!"

    def accelerate(self):
        # 행동 2: 가속하기
        if self.is_running:
            return f"{self.speed}km/h로 가속합니다!"
        return "먼저 시동을 걸어주세요!"

    def stop(self):
        # 행동 3: 멈추기
        self.is_running = False
        return "자동차가 멈췄습니다!"
""")

print("\n실행:")

class Car:
    def __init__(self, brand, model, speed):
        self.brand = brand
        self.model = model
        self.speed = speed
        self.is_running = False

    def start(self):
        self.is_running = True
        return f"🚗 {self.brand} {self.model}이 시동되었습니다!"

    def accelerate(self):
        if self.is_running:
            return f"⚡ {self.speed}km/h로 가속합니다!"
        return "❌ 먼저 시동을 걸어주세요!"

    def stop(self):
        self.is_running = False
        return "🛑 자동차가 멈췄습니다!"

my_car = Car("현대", "쏘나타", 200)
print(f"  {my_car.start()}")
print(f"  {my_car.accelerate()}")
print(f"  {my_car.stop()}")

# ============================================================================
# 파트 6: self — 자기 자신을 가리키는 마법 변수
# ============================================================================

print("\n【 파트 6: self — 자기 자신을 가리키는 마법 변수 】")
print("\nself의 의미를 완벽하게 이해해봅시다!\n")

print("self란?")
print("-" * 60)
print("""
self는 '자기 자신의 객체'를 가리킵니다.

class Person:
    def __init__(self, name):
        self.name = name  # 이 객체의 name

    def greet(self):
        return f"안녕, 나는 {self.name}입니다!"  # 이 객체의 name

alice = Person("Alice")
bob = Person("Bob")

alice.greet()  # alice의 self → alice.name ("Alice")
bob.greet()    # bob의 self → bob.name ("Bob")
""")

print("\n쉬운 비유:")
print("-" * 60)
print("""
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def info(self):
        return f"'{self.title}'는 {self.author}이 쓴 책입니다."

book1 = Book("Python Guide", "Guido")
book2 = Book("Clean Code", "Robert")

book1.info()  # "book1의 제목"과 "book1의 저자"를 사용
book2.info()  # "book2의 제목"과 "book2의 저자"를 사용
""")

print("\n실행:")

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def info(self):
        return f"📖 '{self.title}'는 {self.author}이 쓴 책입니다."

book1 = Book("Python Guide", "Guido")
book2 = Book("Clean Code", "Robert")

print(f"  {book1.info()}")
print(f"  {book2.info()}")

# ============================================================================
# 파트 7: 캡슐화 — 데이터 보호
# ============================================================================

print("\n【 파트 7: 캡슐화 — 데이터 보호 】")
print("\n객체의 내부 데이터를 보호하는 방법!\n")

print("문제: 계좌에서 돈을 음수로 설정할 수 있어요!")
print("-" * 60)

print("\n나쁜 예시:")
print("""
account = BankAccount("Alice", 10000)
account.balance = -100000  # 음수로 설정 가능 (위험!)
""")

print("\n해결책: 메서드로만 수정하게 하기")
print("-" * 60)

print("\n코드:")
print("""
class SecureAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance  # _를 앞에 붙여 '내부용'임을 표시

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def get_balance(self):
        return self._balance
""")

print("\n실행:")

class SecureAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return f"✅ {amount}원 입금 (잔액: {self._balance}원)"
        return "❌ 양수만 입금 가능"

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return f"✅ {amount}원 출금 (잔액: {self._balance}원)"
        return "❌ 출금 불가"

    def get_balance(self):
        return f"현재 잔액: {self._balance}원"

acc = SecureAccount("Alice", 10000)
print(f"  {acc.deposit(5000)}")
print(f"  {acc.withdraw(3000)}")
print(f"  {acc.get_balance()}")

# ============================================================================
# 파트 8: 상속 — 클래스 재사용
# ============================================================================

print("\n【 파트 8: 상속 — 클래스 재사용 】")
print("\n기존 클래스를 상속해서 새로운 클래스를 만들어봅시다!\n")

print("상속이란?")
print("-" * 60)
print("""
부모 클래스의 모든 속성과 메서드를 물려받은 후,
필요한 것만 추가로 정의하는 방법입니다.

class Animal:  # 부모 클래스
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name}가 소리를 냅니다!"

class Dog(Animal):  # 자식 클래스 (Animal을 상속)
    def speak(self):
        return f"{self.name}가 멍멍 합니다!"

class Cat(Animal):  # 자식 클래스 (Animal을 상속)
    def speak(self):
        return f"{self.name}가 야옹 합니다!"
""")

print("\n실행:")

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name}가 소리를 냅니다!"

class Dog(Animal):
    def speak(self):
        return f"🐕 {self.name}가 멍멍 합니다!"

class Cat(Animal):
    def speak(self):
        return f"🐱 {self.name}가 야옹 합니다!"

dog = Dog("뽀삐")
cat = Cat("나비")

print(f"  {dog.speak()}")
print(f"  {cat.speak()}")

# ============================================================================
# 파트 9: 다형성 — 같은 이름, 다른 행동
# ============================================================================

print("\n【 파트 9: 다형성 — 같은 이름, 다른 행동 】")
print("\n같은 메서드 이름인데 다르게 동작하는 마법!\n")

print("다형성이란?")
print("-" * 60)
print("""
부모 클래스의 메서드를 자식 클래스에서 재정의하여
같은 이름이지만 다르게 동작하게 하는 것입니다.

# 모든 도형이 area() 메서드를 가지지만
# 각각 다르게 계산합니다!

class Circle:
    def area(self):
        return f"원의 넓이: π × r²"

class Rectangle:
    def area(self):
        return f"직사각형의 넓이: w × h"

class Triangle:
    def area(self):
        return f"삼각형의 넓이: w × h / 2"
""")

print("\n실행:")

import math

class Shape:
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Triangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height / 2

circle = Circle(5)
rect = Rectangle(4, 3)
triangle = Triangle(4, 3)

print(f"  원의 넓이: {circle.area():.2f}")
print(f"  직사각형의 넓이: {rect.area()}")
print(f"  삼각형의 넓이: {triangle.area()}")

# ============================================================================
# 파트 10: 실제 응용 1 — 게임 캐릭터 시스템
# ============================================================================

print("\n【 파트 10: 실제 응용 1 — 게임 캐릭터 시스템 】")
print("\n RPG 게임의 캐릭터를 설계해봅시다!\n")

print("요구사항:")
print("-" * 60)
print("""
• 캐릭터는 이름, 직업, 체력, 마나를 가짐
• attack() 메서드로 공격
• heal() 메서드로 치유
• level_up() 메서드로 레벨 상승
• status() 메서드로 상태 확인
""")

print("\n코드:")
print("""
class Character:
    def __init__(self, name, job, hp, mana):
        self.name = name
        self.job = job
        self.hp = hp
        self.max_hp = hp
        self.mana = mana
        self.level = 1

    def attack(self, damage):
        self.mana -= 10
        if self.mana < 0:
            return "❌ 마나 부족"
        return f"⚔️  {damage} 데미지 공격!"

    def heal(self):
        self.hp = min(self.hp + 50, self.max_hp)
        return f"💚 {self.hp}까지 회복!"

    def level_up(self):
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        return f"🆙 레벨 {self.level}로 상승!"

    def status(self):
        return f"{self.name} [{self.job}] Lv.{self.level} | HP:{self.hp}/{self.max_hp} | MP:{self.mana}"
""")

print("\n실행:")

class Character:
    def __init__(self, name, job, hp, mana):
        self.name = name
        self.job = job
        self.hp = hp
        self.max_hp = hp
        self.mana = mana
        self.level = 1

    def attack(self, damage):
        if self.mana < 10:
            return "❌ 마나 부족"
        self.mana -= 10
        return f"⚔️  {damage} 데미지 공격!"

    def heal(self):
        heal_amount = 50
        self.hp = min(self.hp + heal_amount, self.max_hp)
        return f"💚 {heal_amount} 회복 (현재 HP: {self.hp})"

    def level_up(self):
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        return f"🆙 레벨 {self.level}로 상승! (최대 HP: {self.max_hp})"

    def status(self):
        return f"{self.name} [{self.job}] Lv.{self.level} | HP:{self.hp}/{self.max_hp} | MP:{self.mana}"

warrior = Character("Conan", "Warrior", 100, 30)
print(f"  {warrior.status()}")
print(f"  {warrior.attack(25)}")
print(f"  {warrior.heal()}")
print(f"  {warrior.level_up()}")
print(f"  {warrior.status()}")

# ============================================================================
# 파트 11: 실제 응용 2 — 학교 관리 시스템
# ============================================================================

print("\n【 파트 11: 실제 응용 2 — 학교 관리 시스템 】")
print("\n학교의 학생과 교수를 관리하는 시스템!\n")

print("설계:")
print("-" * 60)

print("\n코드:")
print("""
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Student(Person):
    def __init__(self, name, age, student_id, major):
        super().__init__(name, age)
        self.student_id = student_id
        self.major = major
        self.gpa = 4.0

    def register_course(self, course):
        return f"✅ {course} 수강 등록"

    def update_gpa(self, gpa):
        self.gpa = gpa
        return f"📊 GPA 업데이트: {self.gpa}"

class Professor(Person):
    def __init__(self, name, age, employee_id, department):
        super().__init__(name, age)
        self.employee_id = employee_id
        self.department = department
        self.courses = []

    def teach(self, course):
        self.courses.append(course)
        return f"📚 {course} 강의 시작"
""")

print("\n실행:")

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class StudentPerson(Person):
    def __init__(self, name, age, student_id, major):
        super().__init__(name, age)
        self.student_id = student_id
        self.major = major
        self.gpa = 4.0

    def register_course(self, course):
        return f"✅ {course} 수강 등록"

    def update_gpa(self, gpa):
        self.gpa = gpa
        return f"📊 GPA 업데이트: {self.gpa:.1f}"

class Professor(Person):
    def __init__(self, name, age, employee_id, department):
        super().__init__(name, age)
        self.employee_id = employee_id
        self.department = department
        self.courses = []

    def teach(self, course):
        self.courses.append(course)
        return f"📚 {course} 강의 시작"

alice = StudentPerson("Alice", 20, 1001, "Computer Science")
prof_kim = Professor("Kim", 45, 5001, "Computer Science")

print(f"  학생: {alice.name} ({alice.major})")
print(f"  {alice.register_course('Python Programming')}")
print(f"  {alice.update_gpa(3.8)}")

print(f"\n  교수: {prof_kim.name} ({prof_kim.department})")
print(f"  {prof_kim.teach('Data Structure')}")
print(f"  {prof_kim.teach('Algorithm')}")

# ============================================================================
# 파트 12: 객체 지향의 철학 — SOLID 원칙 소개
# ============================================================================

print("\n【 파트 12: 객체 지향의 철학 — 설계 원칙 】")
print("\n프로가 지켜야 할 객체 지향 설계의 원칙들!\n")

print("【 좋은 클래스 설계의 특징 】")
print("-" * 60)
print("""
1. 단일 책임 원칙 (Single Responsibility)
   하나의 클래스는 하나의 책임만 가진다.

   ❌ 나쁜 예:
   class Student:
       def study(self): ...
       def eat(self): ...          # 식사는 학생의 책임?
       def manage_database(self): ... # DB 관리는?

   ✅ 좋은 예:
   class Student:
       def study(self): ...
       def get_gpa(self): ...

2. 개방-폐쇄 원칙 (Open-Closed)
   확장에는 열려있고, 수정에는 닫혀있다.

   → 새로운 형태의 동물을 추가할 때
     기존 코드를 수정하지 않고 상속으로 확장

3. 리스코프 치환 원칙 (Liskov Substitution)
   자식 클래스는 부모 클래스로 대체 가능해야 한다.

   → Dog은 Animal의 모든 기능을 사용 가능해야 함

4. 인터페이스 분리 원칙 (Interface Segregation)
   불필요한 메서드를 강제하지 않는다.

   → 필요한 메서드만 구현

5. 의존성 역전 원칙 (Dependency Inversion)
   구체적 구현이 아닌 추상화에 의존한다.

   → 특정 DB 클래스가 아닌 '저장소' 인터페이스에 의존
""")

print("\n【 클래스 설계 체크리스트 】")
print("-" * 60)
print("""
  ✅ 클래스는 현실의 개념을 표현하는가?
  ✅ 속성과 메서드가 서로 관련이 있는가?
  ✅ 메서드는 자신의 책임을 명확히 하는가?
  ✅ 외부에 노출할 것과 숨길 것을 구분했는가?
  ✅ 상속과 다형성을 적절히 활용했는가?
  ✅ 코드가 읽기 쉽고 이해하기 쉬운가?
""")

# ============================================================================
# 최종 정리 및 축하
# ============================================================================

print("\n" + "=" * 80)
print("【 고등학교 1학년: 객체 지향 마스터! 】")
print("=" * 80)

print("""
이제 여러분은 '자신의 데이터 타입을 설계하는' 프로그래머입니다! 🏛️

✅ 배운 개념:
   • 클래스와 객체의 차이
   • __init__ 생성자
   • 속성 (Attribute)
   • 메서드 (Method)
   • self의 의미
   • 캡슐화 (Data Hiding)
   • 상속 (Inheritance)
   • 다형성 (Polymorphism)
   • SOLID 원칙

✅ 이해한 철학:
   • 현실의 것들을 코드로 표현
   • 거대한 시스템을 작은 조각으로 분해
   • 코드의 재사용성 극대화
   • 유지보수 가능한 설계

✅ 설계한 시스템:
   • 게임 캐릭터 시스템
   • 학교 관리 시스템
   • 은행 계좌 시스템

이제 여러분의 프로그래밍은:
   ✨ 단순 명령의 집합이 아닌 '시스템 설계'
   ✨ 작은 단위의 조합으로 큰 것을 만드는 능력
   ✨ 현실 문제를 코드로 우아하게 해결
   ✨ 대규모 프로젝트를 관리할 역량
""")

print("\n" + "=" * 80)
print("저장 필수: 너는 기록이 증명이다 gogs. 👑")
print("=" * 80)

print("""
💡 오늘의 깨달음:
   프로그래밍의 진정한 능력은 새로운 문법을 배우는 것이 아닙니다.
   현실의 복잡한 것들을 단순하고 우아한 코드로 표현하는 것입니다.

   클래스는 그런 능력의 핵심입니다.
   이제 여러분은 '설계자'입니다!

🎓 축하합니다!
   고등학교 1학년 두 번째 단원을 완수했습니다!
   이제 여러분은 '객체 지향'의 참된 의미를 알았습니다!

🎒 다음 단계:
   [고등학교 v2.3: 모듈과 패키지 — 남의 강력한 도구 가져오기]
   표준 라이브러리와 외부 라이브러리를 활용하는 법을 배웁니다!

축하합니다! 👏
이제 여러분은 '자신의 데이터 타입을 설계하는' 파이썬 개발자입니다!
현실을 코드로 표현하는 것이 프로의 증명입니다! 👑
""")
