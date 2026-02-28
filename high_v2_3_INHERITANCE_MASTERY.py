#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
파이썬 고등학교 1학년 - v2.3-Advanced: 상속 마스터리
    — 설계도의 계층적 진화
================================================================================

【 이 파일의 목표 】
v2.3를 깊게 파고들어 상속의 진정한 의미를 이해하기

v2.3 (기초)는 상속의 개념과 메서드 오버라이딩을 배웠습니다.
v2.3-Advanced (심화)는:
  - 상속이 왜 필요한지 철학을 이해합니다
  - 부모-자식 관계를 완벽히 설계합니다
  - 메서드 오버라이딩을 마스터합니다
  - super()의 진정한 활용을 배웁니다
  - 다중 상속과 계층 구조를 다룹니다
  - 추상 클래스로 템플릿을 만듭니다
  - 설계 원칙과 베스트 프랙티스를 학습합니다

결과:
  "재사용 가능하고 유지보수 쉬운 시스템" 설계 능력


================================================================================
【 파트 1: 상속의 철학 — "왜 상속인가?" 】
================================================================================

【 DRY 원칙 (Don't Repeat Yourself) 】

상황: 여러 저장소 클래스가 필요합니다

나쁜 방법 (코드 복사):
  class BasicStorage:
      def __init__(self, owner):
          self.owner = owner
          self.data = []

      def save(self, item):
          self.data.append(item)

      def clear(self):
          self.data = []

  class SecureStorage:
      def __init__(self, owner):
          self.owner = owner
          self.data = []

      def save(self, item):
          self.data.append(item)

      def clear(self):
          self.data = []

      def encrypt(self):
          pass

문제:
  - 코드가 중복됨
  - __init__와 clear가 똑같음
  - 나중에 버그 발견 시 모든 클래스를 수정해야 함

좋은 방법 (상속 사용):
  class Storage:
      def __init__(self, owner):
          self.owner = owner
          self.data = []

      def save(self, item):
          self.data.append(item)

      def clear(self):
          self.data = []

  class SecureStorage(Storage):
      def encrypt(self):
          pass

장점:
  - 공통 코드는 부모에만 있음
  - SecureStorage는 필요한 부분만 추가
  - 버그 수정 시 부모만 수정하면 자식도 자동 반영

결론:
  상속 = "중복 제거 + 코드 재사용"


【 is-a 관계 】

상속을 사용할 때 확인:
  "자식은 부모인가?"

예시:
  ✅ 올바른 상속:
    Dog is an Animal (개는 동물인가? 예!)
    SecureStorage is a Storage (보안 저장소는 저장소인가? 예!)
    Student is a Person (학생은 사람인가? 예!)

  ❌ 잘못된 상속:
    Car is a Engine (자동차는 엔진인가? 아니다, 포함관계)
    Teacher is a School (교사는 학교인가? 아니다, 소속관계)


================================================================================
【 파트 2: 부모 클래스와 자식 클래스 — 관계 설정 】
================================================================================

【 기본 구조 】

부모 클래스 (Parent Class):
  class Storage:
      def __init__(self, owner):
          self.owner = owner
          self.data = []

      def save(self, item):
          self.data.append(item)

자식 클래스 (Child Class):
  class SecureStorage(Storage):
      pass

의미:
  SecureStorage는 Storage를 상속받음
  → Storage의 모든 속성과 메서드를 물려받음


【 자식 클래스가 부모의 것을 물려받는 과정 】

자동 상속:
  secure_storage = SecureStorage("Alice")
  print(secure_storage.owner)     # "Alice" (부모의 __init__이 자동 실행)
  secure_storage.save("data")     # data 저장 (부모의 save 메서드 사용)

명시적 상속:
  class SecureStorage(Storage):
      def __init__(self, owner, password):
          super().__init__(owner)      # 부모의 __init__ 호출
          self.password = password

의미:
  super().__init__(owner)은 부모의 __init__을 호출
  → 부모의 초기화 작업을 먼저 수행
  → 그 다음 자신의 추가 작업 수행


================================================================================
【 파트 3: 메서드 오버라이딩 — "더 나은 방법" 】
================================================================================

【 메서드 오버라이딩이란 】

의미:
  부모가 만든 메서드를 자식이 다시 만드는 것
  같은 이름이지만 다른 기능

예시:
  부모의 save():
    def save(self, item):
        self.data.append(item)
        print(f"저장됨: {item}")

  자식의 save() (오버라이딩):
    def save(self, item):
        if len(self.data) < self.capacity:
            self.data.append(item)
            print(f"안전 저장됨: {item}")
        else:
            print("용량 초과!")

실행:
  storage = Storage("Alice")
  storage.save("data1")
  → 출력: "저장됨: data1" (부모의 메서드)

  secure_storage = SecureStorage("Alice", 100)
  secure_storage.save("data1")
  → 출력: "안전 저장됨: data1" (자식의 메서드)


【 메서드 오버라이딩의 규칙 】

1) 메서드 이름은 같아야 함
2) 매개변수는 같거나 compatible해야 함
3) 반환 타입도 일치하거나 호환돼야 함

좋은 예:
  부모:
    def process(self, data):
        return len(data)

  자식:
    def process(self, data):
        cleaned = data.strip()
        return len(cleaned)
  (같은 이름, 호환 가능한 매개변수)

나쁜 예:
  부모:
    def process(self, data):
        return len(data)

  자식:
    def process(self, data, extra):
        return len(data) + extra
  (매개변수 개수가 다름 - 호출 불가)


================================================================================
【 파트 4: super() 함수 — 부모에게 위임 】
================================================================================

【 super()의 의미 】

super() = "부모 클래스를 가리키는 특수 객체"

언제 사용:
  - 부모의 메서드를 호출하되 기능을 추가할 때
  - 부모의 초기화를 먼저 수행 후 자신의 초기화 추가

구조:
  class Child(Parent):
      def method(self):
          super().method()        # 부모의 method() 호출
          (자신의 추가 기능)


【 super().__init__() 예시 】

부모:
  class Animal:
      def __init__(self, name):
          self.name = name
          print(f"동물 {name}이 태어났습니다")

자식:
  class Dog(Animal):
      def __init__(self, name, breed):
          super().__init__(name)      # 부모의 __init__ 호출
          self.breed = breed
          print(f"{name}는 {breed} 견종입니다")

실행:
  dog = Dog("뽀삐", "푸들")
  → 출력:
    동물 뽀삐이 태어났습니다
    뽀삐는 푸들 견종입니다

실행 흐름:
  1) Dog.__init__() 시작
  2) super().__init__(name) → Animal.__init__() 호출
  3) Animal.__init__() 완료
  4) Dog.__init__()의 나머지 부분 수행


【 super().method() 예시 】

부모:
  class Vehicle:
      def start(self):
          print("엔진 시작!")

자식:
  class Car(Vehicle):
      def start(self):
          super().start()             # 부모의 start() 호출
          print("라디오 켜짐!")

실행:
  car = Car()
  car.start()
  → 출력:
    엔진 시작!
    라디오 켜짐!


================================================================================
【 파트 5: 다중 상속 — 여러 부모 】
================================================================================

【 다중 상속이란 】

의미:
  하나의 자식이 여러 부모를 가지는 것

구조:
  class Child(Parent1, Parent2, Parent3):
      pass

예시:
  class Flyer:
      def fly(self):
          print("날고 있습니다")

  class Swimmer:
      def swim(self):
          print("헤엄치고 있습니다")

  class Duck(Flyer, Swimmer):
      pass

  duck = Duck()
  duck.fly()     # 출력: "날고 있습니다"
  duck.swim()    # 출력: "헤엄치고 있습니다"


【 다중 상속의 문제: 다이아몬드 문제 】

상황:
  class A:
      def method(self):
          print("A의 method")

  class B(A):
      def method(self):
          print("B의 method")

  class C(A):
      def method(self):
          print("C의 method")

  class D(B, C):
      pass

  d = D()
  d.method()

질문: B의 method? C의 method? 어느 것을 호출?

답: MRO (Method Resolution Order)에 따름
  D → B → C → A

따라서:
  d.method() → B의 method 호출


【 MRO 확인 】

방법 1: mro() 메서드
  print(D.mro())
  또는
  print(D.__mro__)

결과:
  [<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>]

의미:
  메서드를 찾을 때 이 순서대로 탐색


================================================================================
【 파트 6: 추상 클래스 — 템플릿 역할 】
================================================================================

【 추상 클래스란 】

의미:
  직접 인스턴스를 만들지 않고, 상속의 템플릿 역할만 하는 클래스

사용 이유:
  - "모든 자식이 이 메서드를 반드시 가져야 한다"고 규정
  - 인터페이스 정의

구조:
  from abc import ABC, abstractmethod

  class Animal(ABC):
      @abstractmethod
      def make_sound(self):
          pass

  class Dog(Animal):
      def make_sound(self):
          print("멍멍")

실행:
  dog = Dog()
  dog.make_sound()    # OK: 출력 "멍멍"

  animal = Animal()   # 에러!
  (추상 클래스는 직접 만들 수 없음)


【 추상 메서드의 강제성 】

장점:
  class Cat(Animal):
      pass  # make_sound 구현 안 함

  cat = Cat()  # 에러!
  (Cat은 make_sound를 구현해야 함)

규칙:
  - 추상 클래스를 상속받는 클래스는
  - 모든 abstractmethod를 구현해야 함


================================================================================
【 파트 7: isinstance()와 issubclass() 】
================================================================================

【 isinstance(obj, Class) 】

의미:
  객체 obj가 클래스 Class의 인스턴스인가?
  또는 Class의 자식 클래스의 인스턴스인가?

예시:
  class Animal:
      pass

  class Dog(Animal):
      pass

  dog = Dog()
  print(isinstance(dog, Dog))      # True
  print(isinstance(dog, Animal))   # True (자식도 부모 인스턴스)
  print(isinstance(dog, str))      # False


【 issubclass(SubClass, SuperClass) 】

의미:
  SubClass가 SuperClass의 자식인가?

예시:
  print(issubclass(Dog, Animal))   # True
  print(issubclass(Animal, Dog))   # False
  print(issubclass(Dog, Dog))      # True (자신도 자식)


================================================================================
【 파트 8: 계층 구조 설계 — 실전 프로젝트 】
================================================================================

【 프로젝트: Storage 시스템의 계층적 설계 】

Level 1: 기본 저장소
  class Storage:
      def __init__(self, owner, capacity):
          self.owner = owner
          self.capacity = capacity
          self.data = []

      def save(self, item):
          if len(self.data) < self.capacity:
              self.data.append(item)
              return True
          return False


Level 2: 보안 저장소
  class SecureStorage(Storage):
      def __init__(self, owner, capacity, password):
          super().__init__(owner, capacity)
          self.password = password
          self.logs = []

      def save(self, item):
          self.logs.append(f"저장 시도: {item}")
          return super().save(item)

      def show_logs(self):
          for log in self.logs:
              print(log)


Level 3: 클라우드 저장소
  class CloudStorage(SecureStorage):
      def __init__(self, owner, capacity, password, cloud_url):
          super().__init__(owner, capacity, password)
          self.cloud_url = cloud_url
          self.synced = False

      def save(self, item):
          result = super().save(item)
          if result:
              self.sync_to_cloud()
          return result

      def sync_to_cloud(self):
          print(f"클라우드에 동기화: {self.cloud_url}")
          self.synced = True


【 사용 예시 】

storage = Storage("Alice", 10)
storage.save("data1")

secure = SecureStorage("Bob", 5, "pass123")
secure.save("important")
secure.show_logs()

cloud = CloudStorage("Charlie", 100, "pass456", "https://cloud.gogs")
cloud.save("backup")


================================================================================
【 파트 9: 설계 원칙과 베스트 프랙티스 】
================================================================================

【 원칙 1: Liskov Substitution Principle (LSP) 】

의미:
  자식 클래스는 부모 클래스를 완벽히 대체할 수 있어야 함

좋은 예:
  def process(storage):
      storage.save("data")

  storage = Storage("Alice", 10)
  process(storage)              # OK

  secure = SecureStorage("Bob", 5, "pass")
  process(secure)               # OK (완벽히 대체 가능)

나쁜 예:
  class BrokenStorage(Storage):
      def save(self, item):
          return 0              # 반환형이 다름 (부모는 bool)


【 원칙 2: 계층의 깊이 관리 】

좋은 설계:
  Level 1: Storage
  Level 2: SecureStorage, EncryptedStorage
  Level 3: CloudStorage

주의:
  Level 1 → Level 2 → Level 3 → Level 4 → ...
  (너무 깊으면 복잡해짐)

권장:
  보통 2-3 단계가 적당


【 원칙 3: 메서드 시그니처 유지 】

좋은 예:
  부모:
    def save(self, item):
        pass

  자식:
    def save(self, item):
        super().save(item)
        (추가 작업)

나쁜 예:
  자식:
    def save(self, item, extra=None):  # 매개변수 추가
        pass


================================================================================
【 파트 10: 일반적인 실수와 해결 】
================================================================================

【 실수 1: super() 호출 안 함 】

문제:
  class Child(Parent):
      def __init__(self, name, age):
          self.name = name
          self.age = age
          # super().__init__()을 안 함

  child = Child("Alice", 20)
  print(child.name)   # "Alice"
  print(child.parent_attr)  # 에러! (부모 속성 없음)

해결:
  def __init__(self, name, age):
      super().__init__()
      self.name = name
      self.age = age


【 실수 2: 메서드 오버라이딩 오타 】

문제:
  class Child(Parent):
      def sav(self, item):      # save가 아니라 sav (오타!)
          pass

  child = Child()
  child.save("data")  # 에러! save 메서드가 없음
  (오버라이딩 안 됨, 새로운 메서드 생성)

해결:
  def save(self, item):  # 정확한 이름


【 실수 3: 다중 상속 남용 】

문제:
  class A: pass
  class B: pass
  class C: pass
  class D: pass

  class Complex(A, B, C, D):  # 너무 많은 부모
      pass

해결:
  부모는 최대 2-3개 정도
  필요하면 컴포지션 사용


================================================================================
【 파트 11: 정리 — 상속 마스터리의 핵심 】
================================================================================

【 상속의 5가지 핵심 】

1) 코드 재사용 (DRY 원칙)
   부모의 코드를 자식이 물려받음

2) 메서드 오버라이딩
   부모의 메서드를 자식이 개선

3) super() 함수
   부모의 기능을 먼저 사용하고 추가

4) 계층 구조
   체계적이고 논리적인 설계

5) 다형성 (Polymorphism)
   같은 메서드가 객체에 따라 다르게 작동


【 체크리스트: 당신의 상속은 좋은가? 】

- 자식은 정말 부모인가? (is-a 관계)
- 코드 중복이 제거되었는가?
- super()를 적절히 사용했는가?
- 메서드 시그니처는 호환되는가?
- 계층의 깊이는 적당한가?
- 다중 상속은 필요한가?


================================================================================
저장 필수: 너는 기록이 증명이다 gogs. 👑
================================================================================

오늘의 깨달음:
   "상속은 코드 재사용이 아니라 설계 철학"

   하나의 설계도를 만들고
   그것을 물려받아 더 나은 설계도를 만드는 과정

   이 과정의 반복이 대규모 시스템을 만든다!

다음 시간에는:
   [v2.4-Advanced: 모듈 마스터리 — 설계도들의 조직화]

   만든 클래스들을 파일로 분리하고
   다른 사람의 도구를 가져와 연결하는
   진정한 시스템 설계의 경험!

축하합니다! 👏
이제 여러분은 '계층적 설계자'입니다!

복잡한 시스템도 체계적으로 설계할 수 있습니다!

================================================================================
"""
