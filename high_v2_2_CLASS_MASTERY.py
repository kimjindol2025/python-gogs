#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
파이썬 고등학교 1학년 - v2.2-Advanced: 클래스 마스터리
    — 데이터와 기능의 완벽한 통합
================================================================================

【 이 파일의 목표 】
v2.2를 깊게 파고들어 객체 지향의 진정한 의미를 이해하기

v2.2 (기초)는 클래스의 개념을 배웠습니다.
v2.2-Advanced (심화)는:
  - 클래스가 왜 필요한지 철학을 이해합니다
  - self의 정체를 완벽히 파악합니다
  - 캡슐화로 데이터를 보호합니다
  - 메서드의 다양한 형태를 익힙니다
  - 복잡한 시스템을 객체로 설계합니다

결과:
  "좋은 설계"와 "나쁜 설계"를 구분할 수 있는 능력


================================================================================
【 파트 1: 클래스의 철학 — "왜 객체인가?" 】
================================================================================

【 문제: 변수만으로는 부족하다 】

상황: 학생 정보 관리

나쁜 방법 (변수만 사용):
  name1 = "Alice"
  age1 = 20
  grade1 = 4.8

  name2 = "Bob"
  age2 22
  grade2 = 3.5

  name3 = "Charlie"
  age3 = 21
  grade3 = 4.2

문제점:
  - 변수가 너무 많음
  - 관련된 데이터가 흩어져 있음
  - 실수로 age1을 삭제하면 name1과 분리됨
  - 학생 100명이면? 300개 변수!

좋은 방법 (리스트 사용):
  students = [
      ["Alice", 20, 4.8],
      ["Bob", 22, 3.5],
      ["Charlie", 21, 4.2]
  ]

개선점:
  - 변수 개수 줄음
  - 관련 데이터가 함께 있음

하지만 문제:
  - students[0][0]이 뭐지? (이름인가? 학번인가?)
  - students[0]을 수정할 때 규칙이 없음 (유효성 검사 불가)
  - 학생을 삭제하면서 "이전 기록 남기기" 같은 기능 못 함

최고의 방법 (클래스 사용):
  class Student:
      def __init__(self, name, age, grade):
          self.name = name
          self.age = age
          self.grade = grade

      def update_grade(self, new_grade):
          if 0 <= new_grade <= 4.5:
              self.grade = new_grade
          else:
              print("유효하지 않은 성적입니다")

  students = [
      Student("Alice", 20, 4.8),
      Student("Bob", 22, 3.5),
      Student("Charlie", 21, 4.2)
  ]

장점:
  - 코드의 의도가 명확함 (student.name은 뭐다, 확실함)
  - 데이터 검증 규칙을 한곳에서 관리
  - "학생 추가", "성적 업데이트" 같은 기능을 메서드로 구성
  - 나중에 "기록 남기기" 기능 추가 시 한 곳만 수정

결론:
  클래스 = "데이터 + 기능 + 규칙"을 하나로 묶은 단위


================================================================================
【 파트 2: 클래스의 3요소 심화 】
================================================================================

【 요소 1: __init__ (생성자) — DNA 부여 】

의미:
  객체가 태어날 때 실행되는 특수한 메서드
  객체의 초기 상태를 설정

구조:
  class ClassName:
      def __init__(self, param1, param2):
          self.attr1 = param1
          self.attr2 = param2

예시 (로봇 설계):
  class Robot:
      def __init__(self, name, battery):
          self.name = name
          self.battery = battery
          self.is_active = True
          print(f"로봇 {self.name}이 시작되었습니다")

  robot1 = Robot("R2D2", 100)
  → __init__이 자동으로 실행됨
  → 출력: "로봇 R2D2이 시작되었습니다"

심화 포인트:
  __init__은 객체 생성 시 단 한 번만 실행
  따라서 초기화 작업에만 사용
  메인 기능은 다른 메서드에 위임


【 요소 2: 속성 (Attributes) — 상태 기억 】

의미:
  객체가 가진 정보 (데이터)

종류:
  1) 인스턴스 속성 (Instance Attribute)
     - 객체마다 다름
     - self.name = "Alice"

  2) 클래스 속성 (Class Attribute)
     - 모든 객체가 공유
     - 클래스 정의에서 직접 설정

예시:
  class Student:
      school = "Gogs High School"  # 클래스 속성 (모두 같은 학교)

      def __init__(self, name, grade):
          self.name = name           # 인스턴스 속성 (각자 다른 이름)
          self.grade = grade         # 인스턴스 속성 (각자 다른 성적)

  alice = Student("Alice", 4.8)
  bob = Student("Bob", 3.5)

  print(alice.name)           # "Alice" (다름)
  print(bob.name)             # "Bob" (다름)
  print(alice.school)         # "Gogs High School" (같음)
  print(bob.school)           # "Gogs High School" (같음)

심화 포인트:
  인스턴스 속성과 클래스 속성의 우선순위:
    obj.attribute를 찾을 때:
    1) 먼저 인스턴스 속성에서 찾음
    2) 없으면 클래스 속성에서 찾음


【 요소 3: 메서드 (Methods) — 기능 수행 】

의미:
  객체가 스스로 수행하는 기능 (함수)

구조:
  class ClassName:
      def method_name(self, param1, param2):
          return something

예시:
  class Calculator:
      def add(self, a, b):
          return a + b

      def multiply(self, a, b):
          return a * b

  calc = Calculator()
  print(calc.add(5, 3))           # 8
  print(calc.multiply(5, 3))      # 15

심화 포인트:
  - self는 객체 자신을 가리킴
  - 모든 메서드는 첫 인자로 self를 받음
  - self.attribute로 객체의 속성에 접근
  - self.method()로 다른 메서드 호출


================================================================================
【 파트 3: self의 완벽한 이해 — "나는 누구인가?" 】
================================================================================

【 self란 무엇인가? 】

정의:
  self = "지금 이 메서드를 실행하고 있는 객체 자신"

비유:
  클래스 = "인간"이라는 설계도
  인스턴스 = 실제 사람 (Alice, Bob, Charlie)

  Alice가 자신을 가리키는 "나"
  Bob이 자신을 가리키는 "나"
  Charlie가 자신을 가리키는 "나"

  파이썬에서는 이 "나"를 self라고 부름

예시:
  class Person:
      def greet(self):
          print(f"안녕하세요, 저는 {self.name}입니다")

      def __init__(self, name):
          self.name = name

  alice = Person("Alice")
  bob = Person("Bob")

  alice.greet()
  → self = alice가 됨
  → 출력: "안녕하세요, 저는 Alice입니다"

  bob.greet()
  → self = bob가 됨
  → 출력: "안녕하세요, 저는 Bob입니다"

【 self가 없으면? 】

문제:
  class Person:
      def greet():
          print(f"안녕하세요, 저는 {name}입니다")

에러:
  TypeError: greet() takes 0 positional arguments but 1 was given

왜?
  alice.greet()을 호출하면:
  1) Python은 자동으로 alice를 첫 인자로 전달
  2) greet()이 인자를 받지 않으므로 에러!

따라서:
  모든 인스턴스 메서드는 self를 받아야 함


================================================================================
【 파트 4: 캡슐화 (Encapsulation) — 데이터 보호 】
================================================================================

【 캡슐화란 무엇인가? 】

의미:
  객체의 데이터를 직접 건드리지 않고,
  메서드를 통해서만 접근하게 하는 설계

비유:
  은행 계좌 = 캡슐화된 객체

  나쁜 방법:
    account.money = 1000000000  (직접 값 변경)
    → 아무도 규칙을 지키지 않음
    → 시스템 붕괴!

  좋은 방법:
    account.deposit(1000)  (메서드로만 접근)
    → 메서드 내에 검증 로직 있음
    → "실제로 돈이 있는가?" 확인
    → 안전함

【 Python의 캡슐화: Private 속성 】

방법:
  속성 이름 앞에 언더스코어(_)를 붙임

관례:
  _속성이름 = "protected" (건드리지 마세요 신호)
  __속성이름 = "private" (진짜 보호)

예시:
  class BankAccount:
      def __init__(self, owner, balance):
          self.owner = owner
          self.__balance = balance  # private

      def deposit(self, amount):
          if amount > 0:
              self.__balance += amount
              return f"입금 성공: {amount}원"
          else:
              return "입금 실패: 0보다 큰 금액만 가능"

      def get_balance(self):
          return self.__balance

  account = BankAccount("Alice", 10000)
  print(account.deposit(5000))        # "입금 성공: 5000원"
  print(account.get_balance())        # 15000

  account.__balance = 999999999       # 시도!
  → Python이 자동으로 __balance를 변환함
  → 실제로는 _BankAccount__balance로 저장됨
  → 직접 접근 불가!

심화 포인트:
  - Python은 진정한 private를 강제하지 않음
  - 대신 관례에 의존 (_는 건드리지 마, __는 정말 건드리지 마)
  - 이것이 Python의 철학: "성인의 판단에 의존"


================================================================================
【 파트 5: __str__과 __repr__ — 객체의 표현 】
================================================================================

【 __str__ 메서드 】

의미:
  print()로 객체를 출력할 때 호출되는 메서드
  사용자에게 "친절한" 문자열 반환

예시:
  class Person:
      def __init__(self, name, age):
          self.name = name
          self.age = age

      def __str__(self):
          return f"Person(이름: {self.name}, 나이: {self.age})"

  alice = Person("Alice", 20)
  print(alice)
  → __str__이 실행됨
  → 출력: "Person(이름: Alice, 나이: 20)"

없으면:
  print(alice)
  → 출력: "<__main__.Person object at 0x7f8b8c0b3f10>"
  (메모리 주소... 의미 없음)


【 __repr__ 메서드 】

의미:
  repr(객체)로 호출되는 메서드
  개발자 입장의 "정확한" 표현
  이상적으로는 이 문자열로 객체를 재구성할 수 있어야 함

예시:
  class Person:
      def __init__(self, name, age):
          self.name = name
          self.age = age

      def __repr__(self):
          return f"Person('{self.name}', {self.age})"

  alice = Person("Alice", 20)
  repr(alice)
  → "Person('Alice', 20)"
  → 이 문자열로 객체 재구성 가능: eval(repr(alice))

차이:
  __str__ = 사용자를 위한 예쁜 출력
  __repr__ = 개발자를 위한 정확한 표현


================================================================================
【 파트 6: 메서드의 종류 — 3가지 】
================================================================================

【 1️⃣ 인스턴스 메서드 (Instance Method) 】

의미:
  객체의 인스턴스에 작용하는 메서드
  self를 첫 인자로 받음

예시:
  class Dog:
      def __init__(self, name):
          self.name = name

      def bark(self):          # 인스턴스 메서드
          print(f"{self.name}가 멍멍합니다")

  dog = Dog("뽀삐")
  dog.bark()
  → self = dog


【 2️⃣ 클래스 메서드 (Class Method) 】

의미:
  클래스 자체에 작용하는 메서드
  첫 인자로 cls를 받음 (클래스를 가리킴)

사용 이유:
  - 모든 인스턴스가 공유하는 데이터 수정
  - 다른 형태의 인스턴스 생성 (@classmethod)

예시:
  class Dog:
      species = "Canis familiaris"
      count = 0

      def __init__(self, name):
          self.name = name
          Dog.count += 1

      @classmethod
      def get_count(cls):           # 클래스 메서드
          return f"지금까지 {cls.count}마리의 개가 생성되었습니다"

  dog1 = Dog("뽀삐")
  dog2 = Dog("뭉치")
  print(Dog.get_count())
  → "지금까지 2마리의 개가 생성되었습니다"


【 3️⃣ 정적 메서드 (Static Method) 】

의미:
  인스턴스나 클래스와 무관한 메서드
  self도 cls도 받지 않음

사용 이유:
  - 클래스와 관련된 유틸리티 함수
  - 데이터 변환, 검증 등

예시:
  class MathUtil:
      @staticmethod
      def add(a, b):
          return a + b

      @staticmethod
      def is_even(num):
          return num % 2 == 0

  print(MathUtil.add(5, 3))          # 8
  print(MathUtil.is_even(4))         # True

특징:
  - 인스턴스 생성 불필요
  - 순수 기능만 제공


================================================================================
【 파트 7: 클래스 변수와 인스턴스 변수 비교 】
================================================================================

【 클래스 변수 (Class Variable) 】

정의:
  클래스 정의 단계에서 만들어지는 변수
  모든 인스턴스가 공유

예시:
  class Student:
      school = "Gogs High"  # 클래스 변수
      count = 0

      def __init__(self, name):
          self.name = name
          Student.count += 1

  alice = Student("Alice")
  bob = Student("Bob")

  print(Student.school)      # "Gogs High"
  print(Student.count)       # 2
  print(alice.school)        # "Gogs High" (공유)
  print(bob.school)          # "Gogs High" (공유)

주의:
  alice.school = "Another"   # 인스턴스 속성 생성
  print(alice.school)        # "Another"
  print(bob.school)          # "Gogs High" (영향 없음)


【 인스턴스 변수 (Instance Variable) 】

정의:
  각 인스턴스마다 별도로 가지는 변수
  __init__에서 self.로 정의

예시:
  class Student:
      def __init__(self, name, grade):
          self.name = name     # 인스턴스 변수
          self.grade = grade   # 인스턴스 변수

  alice = Student("Alice", 4.8)
  bob = Student("Bob", 3.5)

  print(alice.name)      # "Alice"
  print(bob.name)        # "Bob" (다름!)
  print(alice.grade)     # 4.8
  print(bob.grade)       # 3.5 (다름!)


================================================================================
【 파트 8: 실전 프로젝트 — 계층적 객체 설계 】
================================================================================

【 프로젝트: 대학교 관리 시스템 】

구조:
  University
    ├─ School (단과대)
    │   ├─ Department (학과)
    │   └─ Professor (교수)
    └─ Student (학생)

Step 1: 기본 클래스 설계

class University:
    def __init__(self, name):
        self.name = name
        self.schools = []

    def add_school(self, school):
        self.schools.append(school)
        print(f"[학교 추가] {school.name}")

class School:
    def __init__(self, name, university):
        self.name = name
        self.university = university
        self.departments = []

    def add_department(self, department):
        self.departments.append(department)
        print(f"[학과 추가] {department.name}")

class Student:
    count = 0

    def __init__(self, name, department):
        self.name = name
        self.department = department
        Student.count += 1

    def __str__(self):
        return f"학생: {self.name} ({self.department.name})"

Step 2: 사용 예시

gogs_univ = University("Gogs University")

engineering = School("공과대", gogs_univ)
gogs_univ.add_school(engineering)

cs_dept = Department("컴퓨터과학", engineering)
engineering.add_department(cs_dept)

alice = Student("Alice", cs_dept)
bob = Student("Bob", cs_dept)

print(alice)
print(f"총 학생 수: {Student.count}")

Step 3: 심화 — 메서드 추가

class Department:
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.students = []

    def enroll_student(self, student):
        self.students.append(student)

    def list_students(self):
        print(f"\n[{self.name}의 학생 목록]")
        for student in self.students:
            print(f"  - {student.name}")

cs_dept.enroll_student(alice)
cs_dept.enroll_student(bob)
cs_dept.list_students()


================================================================================
【 파트 9: 설계 원칙과 안티패턴 】
================================================================================

【 좋은 설계 원칙 】

1) 단일 책임 원칙 (Single Responsibility)
   - 클래스는 한 가지 책임만 가짐
   - Student는 "학생"만 표현

2) 응집도 높음 (High Cohesion)
   - 관련된 데이터와 메서드가 함께 있음
   - Student 클래스에 name, age, grade가 함께 있음

3) 캡슐화 (Encapsulation)
   - 데이터를 메서드로 보호
   - 직접 접근 불가


【 안티패턴 】

❌ 나쁜 예시:

class MessyClass:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3
        self.user_name = "Alice"
        self.user_age = 20
        self.product_name = "Laptop"
        self.product_price = 1000000

문제:
  - 여러 개념이 섞여있음
  - 책임이 불명확
  - 나중에 유지보수 어려움

✅ 좋은 예시:

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Order:
    def __init__(self, user, product, quantity):
        self.user = user
        self.product = product
        self.quantity = quantity

    def total_price(self):
        return self.product.price * self.quantity

장점:
  - 각 클래스가 명확한 책임
  - 유지보수 용이
  - 재사용 가능


================================================================================
【 파트 10: 정리 — 클래스 마스터리의 핵심 】
================================================================================

【 클래스의 5가지 핵심 】

1) 데이터 + 기능의 통합
   상태(속성)과 행동(메서드)을 하나로

2) self의 이해
   "지금 이 메서드를 실행하는 객체"

3) 캡슐화
   데이터를 메서드로 보호

4) 메서드의 다양성
   인스턴스 / 클래스 / 정적 메서드

5) 설계 원칙
   단일 책임, 높은 응집도, 유지보수 용이


【 체크리스트: 당신의 클래스는 좋은가? 】

- 이 클래스는 한 가지 책임을 가지는가?
- 데이터에 직접 접근하도록 하는가? → 메서드를 통해 보호해야 함
- __str__이나 __repr__을 정의했는가?
- 관련된 데이터와 메서드가 함께 있는가?
- 클래스 변수와 인스턴스 변수를 올바르게 구분했는가?


================================================================================
저장 필수: 너는 기록이 증명이다 gogs. 👑
================================================================================

오늘의 깨달음:
   "클래스는 현실을 코드로 표현하는 방법"

   현실의 학생 → Student 클래스
   현실의 자동차 → Car 클래스
   현실의 은행 → Bank 클래스

   각 객체가 "자기 책임"을 가지고
   "자기 데이터"를 관리하고
   "자기 메서드"로 동작한다!

   이것이 객체 지향의 본질입니다.

다음 시간에는:
   [v2.3-Advanced: 상속 마스터리 — 설계도의 재사용과 확장]

   이미 만든 클래스를 상속받아
   새로운 기능을 추가하는 기술을 배웁니다!

축하합니다! 👏
이제 여러분은 '설계자'입니다!

각 객체의 역할이 명확하고
책임이 분명한 코드를 작성할 수 있습니다!

================================================================================
"""
