#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  🎒 파이썬 초등학교 1학년 - v1.6: 함수(Function) — 마법 주문 만들기         ║
║  [Elementary Python: Functions - Creating Magic Spells]                      ║
║                                                                               ║
║  지금까지 우리는 변수(v1.1), 연산(v1.2), 리스트(v1.3),                     ║
║  반복(v1.4), 조건(v1.5)을 배웠습니다.                                       ║
║                                                                               ║
║  하지만 자주 사용하는 코드를 매번 다시 쓰는 것은 너무 번거로워요!          ║
║  "온도를 확인하는 코드"를 매번 5줄씩 써야 할까요?                         ║
║  아니면 check_temperature()라고 한 번만 부르면 될까요?                    ║
║                                                                               ║
║  그래서 파이썬은 '함수(Function)'라는 마법 주문을 제공합니다!             ║
║  자주 쓰는 코드를 하나의 이름으로 정의해서,                                ║
║  필요할 때마다 그 이름을 부르기만 하면 됩니다!                             ║
║                                                                               ║
║  함수 = 코드의 저장소, 마법 주문의 정의서 📜                               ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs. 👑                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

print("=" * 80)
print("🎒 파이썬 초등학교 1학년 - v1.6: 함수(Function) — 마법 주문 만들기")
print("=" * 80)

# ============================================================================
# 파트 1: 함수가 필요한 이유
# ============================================================================

print("\n【 파트 1: 문제 상황 - 반복되는 코드 】")
print("\n상황: '환영 인사'를 3번 하고 싶어요!\n")

print("방법 1: 같은 코드를 3번 반복 (비효율적)")
print("---")
print("print('어서오세요!')")
print("print('프로그래밍을 배우러 오셨나요?')")
print("print()")
print()
print("print('어서오세요!')")
print("print('프로그래밍을 배우러 오셨나요?')")
print("print()")
print()
print("print('어서오세요!')")
print("print('프로그래밍을 배우러 오셨나요?')")
print("print()")
print("---\n")

print("실제 실행 결과:")
print("어서오세요!")
print("프로그래밍을 배우러 오셨나요?")
print()
print("어서오세요!")
print("프로그래밍을 배우러 오셨나요?")
print()
print("어서오세요!")
print("프로그래밍을 배우러 오셨나요?")
print()

print("\n방법 2: 함수로 만들기 (우아함!)")
print("---")
print("def welcome():")
print("    print('어서오세요!')")
print("    print('프로그래밍을 배우러 오셨나요?')")
print()
print("welcome()")
print("welcome()")
print("welcome()")
print("---")
print("\n같은 결과를 얻으면서도 코드가 훨씬 깔끔해요! ✨")

# ============================================================================
# 파트 2: 함수의 기본 구조
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 2: 함수의 구조 】")
print("=" * 80)

print("\n함수를 만드는 방법:\n")
print("def 함수이름():")
print("    함수가 할 일들")
print()

print("함수를 사용하는 방법:\n")
print("함수이름()  # 함수를 '호출'한다고 말합니다\n")

print("예시: 간단한 인사 함수\n")

def greet():
    print("안녕하세요!")
    print("만나서 반갑습니다!")

print("코드:")
print("def greet():")
print("    print('안녕하세요!')")
print("    print('만나서 반갑습니다!')")
print()
print("greet()\n")

print("실행 결과:")
greet()

print("\n【 중요한 규칙 】")
print("  • def: 함수를 '정의'한다는 신호")
print("  • 함수이름(): 마법 주문의 이름")
print("  • 들여쓰기: 함수의 몸통(함수가 할 일)")
print("  • 함수이름(): 함수를 '호출'해서 실행")

# ============================================================================
# 파트 3: 함수를 여러 번 호출하기
# ============================================================================

print("\n" + "-" * 80)
print("파트 3: 함수를 여러 번 호출하기")
print("-" * 80)

print("\n함수의 가장 큰 장점: 필요할 때마다 재사용할 수 있다는 것!\n")

def print_box():
    print("┌─────────────────┐")
    print("│   마법 상자!    │")
    print("└─────────────────┘")

print("코드:")
print("def print_box():")
print("    print('┌─────────────────┐')")
print("    print('│   마법 상자!    │')")
print("    print('└─────────────────┘')")
print()
print("print_box()")
print("print_box()")
print("print_box()\n")

print("실행 결과:\n")
print_box()
print()
print_box()
print()
print_box()

# ============================================================================
# 파트 4: 함수에 정보 주기 (매개변수)
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 4: 함수에 정보 전달하기 — 매개변수(Parameter) 】")
print("=" * 80)

print("\n문제: 인사말을 다르게 하고 싶은데, 함수는 같은 말만 해요!\n")

print("해결책: 함수에 '정보'를 건넬 수 있어요!\n")

def greet_person(name):
    print(f"안녕하세요, {name}님!")
    print("프로그래밍 배우러 왔어요?")

print("코드:")
print("def greet_person(name):")
print("    print(f'안녕하세요, {name}님!')")
print("    print('프로그래밍 배우러 왔어요?')")
print()
print("greet_person('Alice')")
print("greet_person('Bob')")
print("greet_person('Charlie')\n")

print("실행 결과:\n")
greet_person("Alice")
print()
greet_person("Bob")
print()
greet_person("Charlie")

print("\n【 설명 】")
print("  • name: 함수가 받을 정보의 이름 (매개변수)")
print("  • 'Alice': 함수를 호출할 때 실제로 보내는 정보 (인자)")

# ============================================================================
# 파트 5: 함수가 결과를 돌려주기 (반환값)
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 5: 함수가 결과를 돌려주기 — return 문 】")
print("=" * 80)

print("\n문제: 함수가 단순히 출력만 하는 게 아니라 결과를 알려줄 수 있을까?\n")

print("예: 두 수를 더해서 결과를 받고 싶어요!\n")

def add_numbers(a, b):
    result = a + b
    return result

print("코드:")
print("def add_numbers(a, b):")
print("    result = a + b")
print("    return result")
print()
print("sum1 = add_numbers(10, 20)")
print("print(f'10 + 20 = {sum1}')\n")

print("실행 결과:\n")

sum1 = add_numbers(10, 20)
print(f"10 + 20 = {sum1}")

print("\n다른 예시들:\n")

def multiply(a, b):
    return a * b

def is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False

result1 = multiply(5, 3)
result2 = is_even(10)
result3 = is_even(7)

print(f"5 × 3 = {result1}")
print(f"10은 짝수인가? {result2}")
print(f"7은 짝수인가? {result3}")

print("\n【 return의 의미 】")
print("  • return: 함수가 '값'을 돌려준다")
print("  • 이 값을 변수에 저장하거나 바로 사용할 수 있다")

# ============================================================================
# 파트 6: 함수로 조건문과 반복문 활용하기
# ============================================================================

print("\n" + "-" * 80)
print("파트 6: 함수 안에 조건문과 반복문 넣기")
print("-" * 80)

print("\n상황 1: 함수 안에 조건문\n")

def check_grade(score):
    if score >= 90:
        return "A 등급"
    elif score >= 80:
        return "B 등급"
    elif score >= 70:
        return "C 등급"
    else:
        return "D 등급"

print("코드:")
print("def check_grade(score):")
print("    if score >= 90:")
print("        return 'A 등급'")
print("    elif score >= 80:")
print("        return 'B 등급'")
print("    # ... 등등\n")

print("실행 결과:\n")

scores = [95, 85, 75, 65]
for score in scores:
    grade = check_grade(score)
    print(f"점수: {score} → {grade}")

print("\n\n상황 2: 함수 안에 반복문\n")

def print_stars(count):
    for i in range(count):
        print("⭐", end=" ")
    print()

print("코드:")
print("def print_stars(count):")
print("    for i in range(count):")
print("        print('⭐', end=' ')")
print("    print()\n")

print("실행 결과:\n")

print_stars(3)
print_stars(5)
print_stars(7)

# ============================================================================
# 파트 7: 함수의 실제 응용 — 온도 감지 시스템
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 7: 실제 응용 — 온도 감지 시스템 】")
print("=" * 80)

print("\n상황: 온도를 입력받으면 적절한 메시지를 돌려주는 함수\n")

def check_temperature(temp):
    if temp >= 30:
        return "경고: 너무 덥습니다! 에어컨을 켜세요. 🌡️"
    elif temp >= 20:
        return "좋아요: 활동하기 좋은 온도입니다. 😊"
    elif temp >= 10:
        return "알림: 좀 쌀쌀합니다. 외투를 챙기세요. 🧥"
    else:
        return "경고: 매우 춥습니다! 따뜻하게 입으세요. ❄️"

print("코드:")
print("def check_temperature(temp):")
print("    if temp >= 30:")
print("        return '경고: 너무 덥습니다!'")
print("    elif temp >= 20:")
print("        return '좋아요: 활동하기 좋은 온도'")
print("    # ... 등등\n")

print("실행 결과:\n")

temperatures = [35, 25, 15, 5]
for t in temperatures:
    message = check_temperature(t)
    print(f"온도: {t}°C → {message}")

# ============================================================================
# 파트 8: 함수와 리스트 활용
# ============================================================================

print("\n" + "-" * 80)
print("파트 8: 함수와 리스트로 여러 데이터 처리하기")
print("-" * 80)

print("\n상황: 리스트의 모든 숫자에 대해 함수를 적용하고 싶어요!\n")

def is_even(num):
    return num % 2 == 0

def classify_numbers(numbers):
    even_list = []
    odd_list = []
    for num in numbers:
        if is_even(num):
            even_list.append(num)
        else:
            odd_list.append(num)
    return even_list, odd_list

print("코드:")
print("def classify_numbers(numbers):")
print("    even_list = []")
print("    odd_list = []")
print("    for num in numbers:")
print("        if is_even(num):")
print("            even_list.append(num)")
print("        else:")
print("            odd_list.append(num)")
print("    return even_list, odd_list\n")

print("실행 결과:\n")

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even, odd = classify_numbers(numbers)

print(f"숫자 리스트: {numbers}")
print(f"짝수: {even}")
print(f"홀수: {odd}")

# ============================================================================
# 파트 9: 함수의 장점 정리
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 9: 함수의 장점 】")
print("=" * 80)

print("\n1️⃣ 코드 재사용 (DRY: Don't Repeat Yourself)")
print("   같은 코드를 여러 번 쓰지 않아도 된다!")

print("\n2️⃣ 가독성 향상")
print("   add_numbers(10, 20)은 10 + 20보다 의도가 명확하다!")

print("\n3️⃣ 유지보수 용이")
print("   함수의 내용을 수정하면 모든 호출 부분이 자동으로 수정된다!")

print("\n4️⃣ 복잡한 코드 단순화")
print("   긴 코드를 한 줄로 부를 수 있다!")

print("\n5️⃣ 프로그램의 구조화")
print("   큰 프로그램을 여러 함수로 나누어 만들 수 있다!")

# ============================================================================
# 파트 10: 함수 만들기 연습
# ============================================================================

print("\n" + "-" * 80)
print("파트 10: 함수 만들기 연습")
print("-" * 80)

print("\n연습 1: 인사 함수\n")

def say_hello(name, age):
    print(f"안녕하세요! 저는 {name}이고, {age}살입니다.")

say_hello("파이썬", 10)
say_hello("코드", 15)

print("\n연습 2: 비용 계산 함수\n")

def calculate_total_cost(price, quantity):
    total = price * quantity
    tax = total * 0.1
    return total + tax

cost1 = calculate_total_cost(1000, 3)
cost2 = calculate_total_cost(5000, 2)

print(f"3개 × 1,000원 = {cost1:.0f}원 (세금 포함)")
print(f"2개 × 5,000원 = {cost2:.0f}원 (세금 포함)")

print("\n연습 3: 리스트 처리 함수\n")

def find_fruit(basket, target):
    for fruit in basket:
        if fruit == target:
            return f"찾았습니다! {target}이(가) 바구니에 있어요!"
    return f"죄송합니다. {target}은(는) 바구니에 없습니다."

my_basket = ["사과", "바나나", "포도", "딸기"]

print(find_fruit(my_basket, "포도"))
print(find_fruit(my_basket, "망고"))

# ============================================================================
# 최종 정리
# ============================================================================

print("\n" + "=" * 80)
print("【 오늘의 학습 정리 】")
print("=" * 80)

print("\n함수의 기본 구조:")
print("  def 함수이름(매개변수):")
print("      함수가 할 일")
print("      return 결과값  # 선택사항")

print("\n함수의 호출:")
print("  함수이름(인자)")
print("  결과 = 함수이름(인자)")

print("\n함수의 특징:")
print("  • 코드 재사용: 같은 코드를 반복해서 쓰지 않아도 됨")
print("  • 매개변수: 함수에 정보를 전달")
print("  • 반환값(return): 함수가 결과를 돌려줌")
print("  • 조건/반복: 함수 안에서도 if/for 사용 가능")

print("\n함수로 만들 수 있는 것들:")
print("  • 반복되는 작업 간단하게")
print("  • 복잡한 계산 단순화")
print("  • 리스트 처리 자동화")
print("  • 조건 판단 함수화")
print("  • 게임이나 프로그램의 기능 모듈화")

print("\n【 v1.1~v1.6 전체 관계 】")
print("  변수(v1.1) → 데이터를 저장")
print("  연산(v1.2) → 데이터를 계산")
print("  리스트(v1.3) → 여러 데이터를 묶음")
print("  반복(v1.4) → 여러 데이터를 자동 처리")
print("  조건(v1.5) → 상황에 따라 판단")
print("  함수(v1.6) → 반복되는 코드를 '주문'으로! ✨")

# ============================================================================
# 마법의 말
# ============================================================================

print("\n" + "=" * 80)
print("저장 필수: 너는 기록이 증명이다 gogs. 👑")
print("=" * 80)

print("\n💡 오늘의 깨달음:")
print("   함수는 프로그래밍의 '마법'입니다!")
print("   복잡한 명령을 한 단어로 만들고,")
print("   그 단어를 부르기만 하면 된다는 것이지요.")
print("   이것이 바로 프로그래밍을 '재사용 가능'하게 만드는 힘입니다! 🪄")

print("\n🎒 다음 시간에는:")
print("   [v1.7: 문자열의 마법 — 텍스트 처리하기]")
print("   텍스트(문자열)로 할 수 있는 신기한 일들을 배워요!")
print("   v1.2에서 배운 문자열을 더 깊이 있게 다루어봅니다.")

print("\n축하합니다! 👏")
print("이제 여러분은 반복되는 코드를 '마법 주문'으로 만들 수 있습니다!")
