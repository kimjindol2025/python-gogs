#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  🎒 파이썬 중학교 1학년 - v1.9: 리스트 컴프리헨션 —                         ║
║                    파이썬답게 한 줄로 처리하기                               ║
║  [Middle School Python: List Comprehension - Elegant One-Liners]             ║
║                                                                               ║
║  지금까지 우리는 많은 반복문을 작성했습니다.                                ║
║  리스트를 만들기 위해, 딕셔너리를 만들기 위해...                           ║
║                                                                               ║
║  예를 들어:                                                                  ║
║  ```                                                                         ║
║  squares = []                                                                ║
║  for i in range(10):                                                        ║
║      squares.append(i * i)                                                  ║
║  ```                                                                         ║
║                                                                               ║
║  이 3줄을 단 1줄로 쓸 수 있다면?                                            ║
║  ```                                                                         ║
║  squares = [i * i for i in range(10)]                                       ║
║  ```                                                                         ║
║                                                                               ║
║  이것이 바로 '리스트 컴프리헨션(List Comprehension)'입니다!                 ║
║  파이썬의 철학인 "우아함(elegance)"과 "간결함(simplicity)"을                ║
║  구현한 가장 우아한 기술입니다! ✨                                          ║
║                                                                               ║
║  ["한 줄의 코드에 모든 것이 담겨있다"]                                      ║
║  이것이 바로 파이썬의 매력입니다! 🐍                                        ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs. 👑                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

print("=" * 80)
print("🎒 파이썬 중학교 1학년 - v1.9: 리스트 컴프리헨션 — 파이썬답게 한 줄로 처리하기")
print("=" * 80)

# ============================================================================
# 파트 1: 반복문의 한계와 컴프리헨션의 필요성
# ============================================================================

print("\n【 파트 1: 문제 상황 - 반복문의 비효율성 】")
print("\n상황: 1부터 10까지의 제곱수를 구해야 해요!\n")

print("방법 1: 전통적인 방법 (3줄)\n")

print("코드:")
print("squares_old = []")
print("for i in range(1, 11):")
print("    squares_old.append(i * i)\n")

print("실행 결과:")
squares_old = []
for i in range(1, 11):
    squares_old.append(i * i)

print(f"squares_old = {squares_old}\n")

print("방법 2: 리스트 컴프리헨션 (1줄!)\n")

print("코드:")
print("squares_new = [i * i for i in range(1, 11)]\n")

print("실행 결과:")
squares_new = [i * i for i in range(1, 11)]
print(f"squares_new = {squares_new}\n")

print("같은 결과를 얻으면서도 코드가 훨씬 간결해요! 🎉")
print("이것이 바로 '파이썬다운' 코드입니다!")

# ============================================================================
# 파트 2: 리스트 컴프리헨션의 기본 구조
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 2: 리스트 컴프리헨션의 구조 】")
print("=" * 80)

print("\n리스트 컴프리헨션의 기본 형식:\n")
print("[표현식 for 변수 in 반복가능한객체]")
print()
print("풀어서 설명하면:")
print("  • [  ]: 리스트를 만든다")
print("  • 표현식: 각 항목을 어떻게 변형할 것인가")
print("  • for 변수 in 객체: 어떤 항목들을 반복하는가")

print("\n\n예시 1: 간단한 변환\n")

print("코드: numbers = [1, 2, 3, 4, 5]")
numbers = [1, 2, 3, 4, 5]
print("      doubled = [n * 2 for n in numbers]\n")

doubled = [n * 2 for n in numbers]
print(f"결과: doubled = {doubled}\n")

print("풀이:")
print("  • 각 숫자 n을")
print("  • 2배로 변형해서 (n * 2)")
print("  • 새 리스트에 넣는다\n")

print("예시 2: 문자열 변환\n")

print("코드: names = ['alice', 'bob', 'charlie']")
names = ['alice', 'bob', 'charlie']
print("      capitalized = [name.upper() for name in names]\n")

capitalized = [name.upper() for name in names]
print(f"결과: capitalized = {capitalized}\n")

# ============================================================================
# 파트 3: 조건이 있는 컴프리헨션
# ============================================================================

print("\n" + "-" * 80)
print("파트 3: 조건을 포함한 컴프리헨션")
print("-" * 80)

print("\n상황: 1부터 20까지의 수 중에서 짝수만 원해요!\n")

print("방법 1: 전통적인 방법\n")

print("코드:")
print("evens = []")
print("for i in range(1, 21):")
print("    if i % 2 == 0:")
print("        evens.append(i)\n")

evens = []
for i in range(1, 21):
    if i % 2 == 0:
        evens.append(i)

print(f"결과: {evens}\n")

print("방법 2: 조건을 포함한 컴프리헨션\n")

print("코드: evens = [i for i in range(1, 21) if i % 2 == 0]\n")

evens = [i for i in range(1, 21) if i % 2 == 0]
print(f"결과: {evens}\n")

print("훨씬 간결하죠?")
print("형식: [표현식 for 변수 in 객체 if 조건]\n")

print("다른 예시들:\n")

print("• 5 이상 15 이하인 수들:")
filtered = [n for n in range(1, 20) if 5 <= n <= 15]
print(f"  {filtered}\n")

print("• 3의 배수:")
multiples_of_3 = [n for n in range(1, 20) if n % 3 == 0]
print(f"  {multiples_of_3}\n")

print("• 문자 길이가 5 이상인 이름:")
long_names = [name for name in ['alice', 'bob', 'charlie', 'diana'] if len(name) >= 5]
print(f"  {long_names}")

# ============================================================================
# 파트 4: 여러 조건 결합하기
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 4: 여러 조건을 결합하기 】")
print("=" * 80)

print("\n상황: 더 복잡한 조건을 적용하고 싶어요!\n")

print("조건: 10 이상 50 이하의 짝수\n")

print("코드:")
print("numbers = [n for n in range(1, 100) if n >= 10 if n <= 50 if n % 2 == 0]\n")

numbers = [n for n in range(1, 100) if n >= 10 if n <= 50 if n % 2 == 0]
print(f"결과: {numbers}\n")

print("또는 and를 사용할 수도 있어요:\n")

print("코드:")
print("numbers = [n for n in range(1, 100) if 10 <= n <= 50 and n % 2 == 0]\n")

numbers = [n for n in range(1, 100) if 10 <= n <= 50 and n % 2 == 0]
print(f"결과: {numbers}\n")

print("팁: 여러 if를 쓸 때는 AND 관계입니다.")
print("    모든 조건을 만족해야 리스트에 포함돼요!")

# ============================================================================
# 파트 5: 중첩된 반복문 컴프리헨션
# ============================================================================

print("\n" + "-" * 80)
print("파트 5: 중첩 반복문 컴프리헨션")
print("-" * 80)

print("\n상황: 곱셈표를 만들고 싶어요! (2단 × 3단)\n")

print("방법 1: 전통적인 중첩 반복\n")

print("코드:")
print("result = []")
print("for i in range(2, 4):")
print("    for j in range(1, 6):")
print("        result.append(i * j)\n")

result = []
for i in range(2, 4):
    for j in range(1, 6):
        result.append(i * j)

print(f"결과: {result}\n")

print("방법 2: 중첩 컴프리헨션\n")

print("코드: result = [i * j for i in range(2, 4) for j in range(1, 6)]\n")

result = [i * j for i in range(2, 4) for j in range(1, 6)]
print(f"결과: {result}\n")

print("더 유용한 예시: 좌표 쌍\n")

print("코드: coords = [(x, y) for x in range(1, 4) for y in range(1, 3)]\n")

coords = [(x, y) for x in range(1, 4) for y in range(1, 3)]
print(f"결과:")
for coord in coords:
    print(f"  {coord}")

# ============================================================================
# 파트 6: 딕셔너리 컴프리헨션
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 6: 딕셔너리 컴프리헨션 】")
print("=" * 80)

print("\n리스트뿐만 아니라 딕셔너리도 컴프리헨션으로 만들 수 있어요!\n")

print("형식: {키 표현식: 값 표현식 for 변수 in 객체}\n")

print("예시 1: 숫자의 제곱\n")

print("코드: squares = {n: n*n for n in range(1, 6)}\n")

squares = {n: n*n for n in range(1, 6)}
print(f"결과: {squares}\n")

print("예시 2: 단어 길이 매핑\n")

print("코드: words = ['apple', 'banana', 'cherry']")
print("      word_lengths = {word: len(word) for word in words}\n")

words = ['apple', 'banana', 'cherry']
word_lengths = {word: len(word) for word in words}
print(f"결과: {word_lengths}\n")

print("예시 3: 조건이 있는 딕셔너리\n")

print("코드: numbers = range(1, 11)")
print("      evens_squared = {n: n**2 for n in numbers if n % 2 == 0}\n")

numbers = range(1, 11)
evens_squared = {n: n**2 for n in numbers if n % 2 == 0}
print(f"결과: {evens_squared}")

# ============================================================================
# 파트 7: 집합 컴프리헨션
# ============================================================================

print("\n" + "-" * 80)
print("파트 7: 집합 컴프리헨션")
print("-" * 80)

print("\n집합도 컴프리헨션으로 만들 수 있어요!\n")

print("형식: {표현식 for 변수 in 객체}\n")

print("예시 1: 제곱수의 집합\n")

print("코드: squares_set = {n*n for n in range(1, 6)}\n")

squares_set = {n*n for n in range(1, 6)}
print(f"결과: {squares_set}\n")

print("예시 2: 단어의 첫 글자들\n")

print("코드: words = ['apple', 'ant', 'banana', 'bear']")
print("      first_letters = {word[0] for word in words}\n")

words = ['apple', 'ant', 'banana', 'bear']
first_letters = {word[0] for word in words}
print(f"결과: {first_letters}\n")

print("(집합이므로 중복이 자동으로 제거되었어요!)")

# ============================================================================
# 파트 8: 실제 응용 — 데이터 처리
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 8: 실제 응용 — 데이터 처리 】")
print("=" * 80)

print("\n응용 1: 학생 성적 처리\n")

scores = [85, 92, 78, 95, 88, 76, 91, 89]
print(f"성적: {scores}\n")

print("합격한 학생 (80점 이상):")
passed = [score for score in scores if score >= 80]
print(f"  {passed}\n")

print("성적을 10점 단위로 올림:")
boosted = [score + (10 - score % 10) if score % 10 != 0 else score for score in scores]
print(f"  {boosted}\n")

print("응용 2: 텍스트 처리\n")

sentence = "Hello World Python Programming"
print(f"문장: {sentence}\n")

print("대문자만 추출:")
capitals = [char for char in sentence if char.isupper()]
print(f"  {capitals}\n")

print("단어 길이 리스트:")
words = sentence.split()
lengths = [len(word) for word in words]
print(f"  단어: {words}")
print(f"  길이: {lengths}\n")

print("응용 3: 리스트 평탄화 (2D → 1D)\n")

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(f"행렬: {matrix}\n")

print("코드: flattened = [num for row in matrix for num in row]\n")

flattened = [num for row in matrix for num in row]
print(f"결과: {flattened}\n")

# ============================================================================
# 파트 9: 성능 비교
# ============================================================================

print("\n" + "-" * 80)
print("파트 9: 성능 비교")
print("-" * 80)

print("\n큰 데이터셋에서 컴프리헨션이 더 빠릅니다!\n")

import time

# 전통적인 방법
start = time.time()
result1 = []
for i in range(100000):
    result1.append(i * 2)
time1 = time.time() - start

# 컴프리헨션
start = time.time()
result2 = [i * 2 for i in range(100000)]
time2 = time.time() - start

print(f"전통적인 반복문: {time1*1000:.3f}ms")
print(f"리스트 컴프리헨션: {time2*1000:.3f}ms")
print(f"속도 향상: {time1/time2:.1f}배 빠름")

print("\n→ 컴프리헨션이 더 빠르고 메모리 효율적입니다!")

# ============================================================================
# 파트 10: 가독성과 최적화
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 10: 가독성과 최적화 】")
print("=" * 80)

print("\n간단함과 복잡함의 균형:\n")

print("【 좋은 예시 1 】")
print("squares = [x**2 for x in range(10)]")
print("→ 명확하고 읽기 쉬움\n")

print("【 좋은 예시 2 】")
print("evens = [x for x in range(100) if x % 2 == 0]")
print("→ 한눈에 의도가 보임\n")

print("【 나쁜 예시 】")
print("result = [y for x in matrix for y in x if y > 0 and y < 100 and y % 2 == 0]")
print("→ 너무 복잡해서 읽기 어려움\n")

print("팁: 컴프리헨션은 강력하지만,")
print("    너무 복잡하면 전통적인 반복문을 사용하세요!")
print("    코드는 결국 '인간이 읽기 위한 것'입니다! 🤝")

# ============================================================================
# 최종 정리
# ============================================================================

print("\n" + "=" * 80)
print("【 오늘의 학습 정리 】")
print("=" * 80)

print("\n리스트 컴프리헨션:")
print("  • 형식: [표현식 for 변수 in 객체]")
print("  • 조건: [표현식 for 변수 in 객체 if 조건]")
print("  • 중첩: [표현식 for 변수1 in 객체1 for 변수2 in 객체2]")

print("\n딕셔너리 컴프리헨션:")
print("  • 형식: {키:값 for 변수 in 객체}")
print("  • 조건: {키:값 for 변수 in 객체 if 조건}")

print("\n집합 컴프리헨션:")
print("  • 형식: {표현식 for 변수 in 객체}")
print("  • 중복 자동 제거")

print("\n장점:")
print("  ✅ 간결한 코드")
print("  ✅ 더 빠른 성능")
print("  ✅ 메모리 효율적")
print("  ✅ '파이썬다운' 스타일")

print("\n주의사항:")
print("  ⚠️  너무 복잡하면 가독성이 떨어짐")
print("  ⚠️  1~2줄의 조건이 적당")
print("  ⚠️  과도하게 복잡하면 전통 반복문을 선택")

print("\n【 중학교 1학년 3단계 완료! 】")
print("  v1.7: 딕셔너리 ✓")
print("  v1.8: 튜플/집합 ✓")
print("  v1.9: 컴프리헨션 ✓")
print("  = 파이썬 데이터 처리의 대가 탄생! 🎓")

# ============================================================================
# 마법의 말
# ============================================================================

print("\n" + "=" * 80)
print("저장 필수: 너는 기록이 증명이다 gogs. 👑")
print("=" * 80)

print("\n💡 오늘의 깨달음:")
print("   리스트 컴프리헨션은 '우아한 코드'의 상징입니다!")
print("   프로그래밍은 단순히 '동작하는 코드'가 아니라")
print("   '아름다운 코드'를 작성하는 예술입니다.")
print("   이제 여러분은 파이썬의 철학을 이해했습니다! 🐍✨")

print("\n🎒 다음 시간에는:")
print("   [v1.10: 함수형 프로그래밍 — map, filter, reduce]")
print("   컴프리헨션보다 더 추상적이고 강력한")
print("   함수형 패러다임의 세계로 들어갑니다!")

print("\n축하합니다! 👏")
print("이제 여러분은 '한 줄의 코드로 마법을 부리는' 파이썬 프로그래머입니다!")
