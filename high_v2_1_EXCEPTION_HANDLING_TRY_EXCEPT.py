#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  🏫 파이썬 고등학교 1학년 - v2.1: 예외 처리 —                               ║
║                    에러 앞에서도 당당한 코드 (Try-Except)                     ║
║  [High School Python: Exception Handling - Confident Code Before Errors]     ║
║                                                                               ║
║  지금까지 우리는 모든 것이 완벽하다고 가정했습니다.                          ║
║  사용자가 항상 올바른 입력을 한다고 믿었죠.                                  ║
║  파일이 항상 존재한다고 가정했습니다.                                        ║
║                                                                               ║
║  하지만 현실은 다릅니다! 😱                                                 ║
║                                                                               ║
║  사용자는:                                                                   ║
║    • 숫자 대신 글자를 입력합니다                                            ║
║    • 파일을 삭제합니다                                                       ║
║    • 계산 중 오류가 발생합니다                                               ║
║    • 네트워크가 끊깁니다                                                     ║
║                                                                               ║
║  이런 상황에서 프로그램이 "꽝!" 하고 중단되면 어떻게 될까요?               ║
║  사용자는 화를 내고, 프로그램은 신뢰를 잃습니다.                            ║
║                                                                               ║
║  그렇다면? 우리는 에러를 '예측'하고 '대응'해야 합니다!                    ║
║  이것이 바로 "예외 처리(Exception Handling)"입니다!                         ║
║                                                                               ║
║  예외 처리를 하면:                                                           ║
║    ✅ 프로그램이 중단되지 않습니다                                           ║
║    ✅ 사용자에게 친절한 메시지를 보냅니다                                    ║
║    ✅ 다른 작업을 계속할 수 있습니다                                         ║
║    ✅ 전문가처럼 보입니다! 😎                                               ║
║                                                                               ║
║  이제 우리는 "에러 앞에서도 당당한" 프로그래머가 됩니다!                    ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs. 👑                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

print("=" * 80)
print("🏫 파이썬 고등학교 1학년 - v2.1: 예외 처리 — 에러 앞에서도 당당한 코드")
print("=" * 80)

# ============================================================================
# 파트 1: 에러의 종류 — 프로그램을 죽이는 여러 원흉들
# ============================================================================

print("\n【 파트 1: 에러의 종류 — 프로그램을 죽이는 여러 원흉들 】")
print("\n우리가 만날 수 있는 에러들을 먼저 알아봅시다!\n")

print("문제 1: 정수 변환 실패")
print("-" * 60)

print("\n상황: 사용자가 숫자 대신 글자를 입력했어요!\n")

print("코드 (에러 발생):")
print("""
user_input = "hello"
number = int(user_input)  # 글자를 숫자로 변환?
""")

print("\n만약 우리가 이렇게 작성한다면:")
print("  ❌ ValueError: invalid literal for int() with base 10: 'hello'")
print("  ❌ 프로그램 중단! 사용자 당황함!")

print("\n" + "=" * 80)
print("문제 2: 리스트 인덱스 범위 초과")
print("-" * 60)

print("\n코드 (에러 발생):")
print("""
my_list = [1, 2, 3]
value = my_list[10]  # 존재하지 않는 인덱스!
""")

print("\n에러: IndexError: list index out of range")

print("\n" + "=" * 80)
print("문제 3: 파일이 없음")
print("-" * 60)

print("\n코드 (에러 발생):")
print("""
with open('not_exist.txt', 'r') as f:
    content = f.read()
""")

print("\n에러: FileNotFoundError: [Errno 2] No such file or directory")

print("\n" + "=" * 80)
print("문제 4: 0으로 나누기")
print("-" * 60)

print("\n코드 (에러 발생):")
print("""
result = 10 / 0  # 0으로 나누기!
""")

print("\n에러: ZeroDivisionError: division by zero")

# ============================================================================
# 파트 2: try-except 기본 — 에러를 잡다!
# ============================================================================

print("\n【 파트 2: try-except 기본 — 에러를 잡다! 】")
print("\n이제 우리는 이 에러들을 '예측'하고 '처리'합니다!\n")

print("기본 형식:")
print("-" * 60)
print("""
try:
    # 에러가 발생할 수 있는 코드
    risky_code()
except 에러타입:
    # 에러 발생 시 실행할 코드
    print("문제가 발생했어요!")
""")

print("\n예시 1: ValueError 잡기")
print("-" * 60)

print("\n코드:")
print("""
try:
    user_input = "hello"
    number = int(user_input)
    print(f"숫자: {number}")
except ValueError:
    print("⚠️  숫자를 입력해주세요!")
""")

print("\n실행:")

try:
    user_input = "hello"
    number = int(user_input)
    print(f"숫자: {number}")
except ValueError:
    print("⚠️  숫자를 입력해주세요!")

print("\n✅ 프로그램이 중단되지 않았어요!")

# ============================================================================
# 파트 3: 여러 종류의 예외 처리
# ============================================================================

print("\n【 파트 3: 여러 종류의 예외 처리 】")
print("\n한 개의 에러만 존재하는 것이 아닙니다!\n")

print("상황: 여러 종류의 에러에 대응해야 해요!\n")

print("코드:")
print("""
try:
    user_input = input("숫자를 입력하세요: ")
    number = int(user_input)

    my_list = [1, 2, 3]
    value = my_list[number]

    result = 10 / number
    print(f"결과: {result}")

except ValueError:
    print("❌ ValueError: 숫자를 입력해주세요!")
except IndexError:
    print("❌ IndexError: 리스트 범위를 초과했어요!")
except ZeroDivisionError:
    print("❌ ZeroDivisionError: 0으로 나눌 수 없습니다!")
""")

print("\n실행 (여러 시나리오):")
print("-" * 60)

# 시나리오 1: 정상
print("\n시나리오 1: 정상 입력 (숫자 1)")
try:
    number = 1
    my_list = [10, 20, 30]
    value = my_list[number]
    result = 10 / number
    print(f"  리스트 값: {value}")
    print(f"  나누기 결과: {result}")
except ValueError:
    print("❌ ValueError: 숫자를 입력해주세요!")
except IndexError:
    print("❌ IndexError: 리스트 범위를 초과했어요!")
except ZeroDivisionError:
    print("❌ ZeroDivisionError: 0으로 나눌 수 없습니다!")

# 시나리오 2: 범위 초과
print("\n시나리오 2: 범위 초과 (숫자 10)")
try:
    number = 10
    my_list = [10, 20, 30]
    value = my_list[number]
    result = 10 / number
    print(f"  리스트 값: {value}")
    print(f"  나누기 결과: {result}")
except ValueError:
    print("❌ ValueError: 숫자를 입력해주세요!")
except IndexError:
    print("❌ IndexError: 리스트 범위를 초과했어요!")
except ZeroDivisionError:
    print("❌ ZeroDivisionError: 0으로 나눌 수 없습니다!")

# 시나리오 3: 0으로 나누기
print("\n시나리오 3: 0으로 나누기")
try:
    number = 0
    my_list = [10, 20, 30]
    value = my_list[number]
    result = 10 / number
    print(f"  리스트 값: {value}")
    print(f"  나누기 결과: {result}")
except ValueError:
    print("❌ ValueError: 숫자를 입력해주세요!")
except IndexError:
    print("❌ IndexError: 리스트 범위를 초과했어요!")
except ZeroDivisionError:
    print("❌ ZeroDivisionError: 0으로 나눌 수 없습니다!")

# ============================================================================
# 파트 4: 예외 정보 가져오기 (as 키워드)
# ============================================================================

print("\n【 파트 4: 예외 정보 가져오기 (as 키워드) 】")
print("\n에러의 정확한 메시지를 알고 싶다면?\n")

print("기본 형식:")
print("-" * 60)
print("""
try:
    risky_code()
except 에러타입 as error:
    print(f"에러 메시지: {error}")
""")

print("\n예시:")
print("-" * 60)

print("\n코드:")
print("""
try:
    number = int("hello")
except ValueError as error:
    print(f"❌ 에러 발생!")
    print(f"   에러 타입: {type(error).__name__}")
    print(f"   에러 메시지: {error}")
""")

print("\n실행:")

try:
    number = int("hello")
except ValueError as error:
    print(f"❌ 에러 발생!")
    print(f"   에러 타입: {type(error).__name__}")
    print(f"   에러 메시지: {error}")

# ============================================================================
# 파트 5: finally — 항상 실행되는 코드
# ============================================================================

print("\n【 파트 5: finally — 항상 실행되는 코드 】")
print("\n에러 발생 여부와 관계없이 반드시 실행할 코드가 있다면?\n")

print("상황: 파일을 닫아야 하거나, 정리해야 할 작업이 있어요!\n")

print("기본 형식:")
print("-" * 60)
print("""
try:
    risky_code()
except 에러타입:
    handle_error()
finally:
    cleanup()  # 항상 실행됨!
""")

print("\n예시:")
print("-" * 60)

print("\n코드:")
print("""
print("시작")
try:
    print("  작업 중...")
    result = 10 / 0  # 에러 발생!
    print("  작업 완료")
except ZeroDivisionError:
    print("  에러 처리 완료")
finally:
    print("정리 작업 실행 (항상 실행됨)")
print("종료")
""")

print("\n실행:")

print("시작")
try:
    print("  작업 중...")
    result = 10 / 0  # 에러 발생!
    print("  작업 완료")
except ZeroDivisionError:
    print("  에러 처리 완료")
finally:
    print("정리 작업 실행 (항상 실행됨)")
print("종료")

print("\n✅ finally 블록이 항상 실행되었습니다!")

# ============================================================================
# 파트 6: 모든 예외 처리하기 (Exception)
# ============================================================================

print("\n【 파트 6: 모든 예외 처리하기 (Exception) 】")
print("\n모든 예외를 따로 처리하기는 너무 번거로워!\n")

print("상황: 어떤 에러든 일단 막아야 해요!\n")

print("코드:")
print("""
try:
    # 여러 가지 일을 함
    risky_code1()
    risky_code2()
    risky_code3()
except Exception as error:
    print(f"⚠️  예기치 않은 에러: {error}")
""")

print("\n예시:")
print("-" * 60)

print("\n코드:")
print("""
try:
    print("다양한 작업 수행 중...")
    number = int("abc")
    my_list = [1, 2, 3]
    value = my_list[10]
except Exception as error:
    print(f"⚠️  예기치 않은 에러 발생!")
    print(f"   에러: {error}")
    print(f"   타입: {type(error).__name__}")
""")

print("\n실행:")

try:
    print("다양한 작업 수행 중...")
    number = int("abc")
    my_list = [1, 2, 3]
    value = my_list[10]
except Exception as error:
    print(f"⚠️  예기치 않은 에러 발생!")
    print(f"   에러: {error}")
    print(f"   타입: {type(error).__name__}")

# ============================================================================
# 파트 7: 파일 입출력과 예외 처리
# ============================================================================

print("\n【 파트 7: 파일 입출력과 예외 처리 】")
print("\n파일을 다루면서 발생하는 에러들을 처리해봅시다!\n")

print("상황: 파일을 읽으려고 하는데 없을 수도 있어요!\n")

print("코드:")
print("""
try:
    with open('important_data.txt', 'r') as f:
        content = f.read()
        print(f"파일 크기: {len(content)} 글자")
except FileNotFoundError:
    print("❌ 파일을 찾을 수 없습니다!")
except PermissionError:
    print("❌ 파일 읽기 권한이 없습니다!")
except Exception as error:
    print(f"❌ 파일 읽기 중 오류: {error}")
""")

print("\n실행 (존재하지 않는 파일):")
print("-" * 60)

try:
    with open('important_data_not_exist.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"파일 크기: {len(content)} 글자")
except FileNotFoundError:
    print("❌ 파일을 찾을 수 없습니다!")
except PermissionError:
    print("❌ 파일 읽기 권한이 없습니다!")
except Exception as error:
    print(f"❌ 파일 읽기 중 오류: {error}")

# ============================================================================
# 파트 8: 실제 응용 1 — 계산기 프로그램
# ============================================================================

print("\n【 파트 8: 실제 응용 1 — 견고한 계산기 프로그램 】")
print("\n사용자 입력을 안전하게 처리하는 계산기!\n")

print("상황: 사용자가 뭘 입력할지 모르니까 모든 경우를 대비해야 해요!\n")

print("코드:")
print("""
def safe_calculator():
    try:
        a = int(input("첫 번째 숫자: "))
        b = int(input("두 번째 숫자: "))
        operator = input("연산자 (+, -, *, /): ")

        if operator == '+':
            result = a + b
        elif operator == '-':
            result = a - b
        elif operator == '*':
            result = a * b
        elif operator == '/':
            result = a / b
        else:
            print("❌ 지원하지 않는 연산자입니다!")
            return

        print(f"결과: {result}")

    except ValueError:
        print("❌ 숫자를 입력해주세요!")
    except ZeroDivisionError:
        print("❌ 0으로 나눌 수 없습니다!")
    except Exception as error:
        print(f"❌ 오류: {error}")

safe_calculator()
""")

print("\n시뮬레이션 (정상 계산):")
print("-" * 60)

def safe_calculator_sim(a_val, b_val, op):
    try:
        if op == '+':
            result = a_val + b_val
        elif op == '-':
            result = a_val - b_val
        elif op == '*':
            result = a_val * b_val
        elif op == '/':
            result = a_val / b_val
        else:
            print("❌ 지원하지 않는 연산자입니다!")
            return

        print(f"계산: {a_val} {op} {b_val} = {result}")

    except ValueError:
        print("❌ 숫자를 입력해주세요!")
    except ZeroDivisionError:
        print("❌ 0으로 나눌 수 없습니다!")
    except Exception as error:
        print(f"❌ 오류: {error}")

print("\n케이스 1: 정상 계산 (5 + 3)")
safe_calculator_sim(5, 3, '+')

print("\n케이스 2: 나누기 (10 / 2)")
safe_calculator_sim(10, 2, '/')

print("\n케이스 3: 0으로 나누기")
safe_calculator_sim(10, 0, '/')

# ============================================================================
# 파트 9: 실제 응용 2 — 점수 처리 프로그램
# ============================================================================

print("\n【 파트 9: 실제 응용 2 — 견고한 점수 처리 프로그램 】")
print("\n학생 점수를 안전하게 읽고 분석합니다!\n")

print("상황: JSON 파일에서 학생 점수를 읽고 평균을 계산해요!\n")

import json

print("코드:")
print("""
import json

def safe_grade_processor(filename):
    try:
        with open(filename, 'r') as f:
            students = json.load(f)

        total_score = 0
        count = 0

        for name, score in students.items():
            if score < 0 or score > 100:
                print(f"⚠️  {name}의 점수 {score}는 유효하지 않습니다!")
            else:
                total_score += score
                count += 1

        if count > 0:
            average = total_score / count
            print(f"평균 점수: {average:.1f}")
        else:
            print("유효한 점수가 없습니다!")

    except FileNotFoundError:
        print(f"❌ 파일 '{filename}'을 찾을 수 없습니다!")
    except json.JSONDecodeError:
        print(f"❌ JSON 파일 형식이 잘못되었습니다!")
    except Exception as error:
        print(f"❌ 오류: {error}")

safe_grade_processor('grades.json')
""")

print("\n실행:")
print("-" * 60)

# 테스트 데이터 생성
test_data = {
    'alice': 95,
    'bob': 87,
    'charlie': 92,
    'diana': 88
}

with open('test_grades.json', 'w', encoding='utf-8') as f:
    json.dump(test_data, f)

def safe_grade_processor(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            students = json.load(f)

        total_score = 0
        count = 0

        for name, score in students.items():
            if score < 0 or score > 100:
                print(f"⚠️  {name}의 점수 {score}는 유효하지 않습니다!")
            else:
                total_score += score
                count += 1

        if count > 0:
            average = total_score / count
            print(f"평균 점수: {average:.1f}점")
        else:
            print("유효한 점수가 없습니다!")

    except FileNotFoundError:
        print(f"❌ 파일 '{filename}'을 찾을 수 없습니다!")
    except json.JSONDecodeError:
        print(f"❌ JSON 파일 형식이 잘못되었습니다!")
    except Exception as error:
        print(f"❌ 오류: {error}")

safe_grade_processor('test_grades.json')

# ============================================================================
# 파트 10: 실제 응용 3 — 데이터 변환 프로그램
# ============================================================================

print("\n【 파트 10: 실제 응용 3 — 견고한 데이터 변환 프로그램 】")
print("\n사용자 입력을 안전하게 변환합니다!\n")

print("상황: 섭씨를 화씨로 변환하는데, 사용자가 이상한 값을 입력할 수 있어요!\n")

print("코드:")
print("""
def celsius_to_fahrenheit(celsius_str):
    try:
        celsius = float(celsius_str)

        # 절대 영도보다 낮으면 불가능
        if celsius < -273.15:
            print("❌ 절대 영도보다 낮은 온도는 불가능합니다!")
            return None

        fahrenheit = celsius * 9/5 + 32
        return fahrenheit

    except ValueError:
        print(f"❌ '{celsius_str}'은 숫자가 아닙니다!")
        return None
    except Exception as error:
        print(f"❌ 오류: {error}")
        return None

# 테스트
test_values = ['25', '100', 'hello', '-300', '0']
for value in test_values:
    result = celsius_to_fahrenheit(value)
    if result is not None:
        print(f"  {value}°C = {result:.1f}°F")
""")

print("\n실행:")
print("-" * 60)

def celsius_to_fahrenheit(celsius_str):
    try:
        celsius = float(celsius_str)

        # 절대 영도보다 낮으면 불가능
        if celsius < -273.15:
            print(f"❌ '{celsius_str}': 절대 영도보다 낮습니다!")
            return None

        fahrenheit = celsius * 9/5 + 32
        return fahrenheit

    except ValueError:
        print(f"❌ '{celsius_str}': 숫자가 아닙니다!")
        return None
    except Exception as error:
        print(f"❌ '{celsius_str}': {error}")
        return None

# 테스트
test_values = ['25', '100', 'hello', '-300', '0']
for value in test_values:
    result = celsius_to_fahrenheit(value)
    if result is not None:
        print(f"  {value}°C = {result:.1f}°F")

# ============================================================================
# 파트 11: 예외 처리의 철학
# ============================================================================

print("\n【 파트 11: 예외 처리의 철학 】")
print("\n프로로서 알아야 할 예외 처리의 원칙!\n")

print("원칙 1: 예측 가능한 에러만 처리하기")
print("-" * 60)
print("""
❌ 나쁜 예시:
try:
    # 수백 줄의 코드
    do_something()
    do_something_else()
    do_another_thing()
except Exception:
    pass  # 모든 에러를 무시? 위험!

✅ 좋은 예시:
try:
    number = int(user_input)
except ValueError:
    print("숫자를 입력해주세요!")
""")

print("\n원칙 2: 에러 메시지는 사용자 친화적으로")
print("-" * 60)
print("""
❌ 나쁜 예시:
except ValueError:
    print("ValueError occurred")  # 뭐가 문제인지 몰라!

✅ 좋은 예시:
except ValueError:
    print("숫자를 입력해주세요!")
""")

print("\n원칙 3: 복구 가능한 경우만 처리하기")
print("-" * 60)
print("""
❌ 나쁜 예시:
try:
    critical_system_operation()
except Exception:
    continue  # 계속 실행? 위험!

✅ 좋은 예시:
try:
    user_input = int(input())
except ValueError:
    user_input = 0  # 기본값으로 복구
""")

# ============================================================================
# 파트 12: 핵심 정리 및 프로젝트
# ============================================================================

print("\n【 파트 12: 핵심 정리 및 프로젝트 】")
print("\n예외 처리의 완벽한 가이드!\n")

print("【 예외 처리 문법 】")
print("-" * 60)
print("""
기본 형태:
  try:
      risky_code()
  except SpecificError as e:
      handle_error(e)
  finally:
      cleanup()

일반적인 예외들:
  • ValueError: 값이 잘못됨 (int("abc"))
  • IndexError: 인덱스 범위 초과 (list[999])
  • KeyError: 딕셔너리 키 없음 (dict['없는키'])
  • FileNotFoundError: 파일 없음 (open('없음.txt'))
  • ZeroDivisionError: 0으로 나누기 (10/0)
  • TypeError: 자료형 불일치 (1 + "a")
  • AttributeError: 속성 없음 (str.없음())
  • Exception: 모든 에러 (가장 광범위)
""")

print("【 핵심 팁 】")
print("-" * 60)
print("""
  ✅ 구체적인 예외부터 처리하기
  ✅ 마지막에 Exception으로 catch-all
  ✅ 에러 메시지는 사용자 친화적으로
  ✅ finally로 정리 작업 보장
  ✅ 복구 불가능하면 처리하지 말기
  ✅ 로깅으로 에러 추적하기 (고급)
""")

print("\n【 프로젝트 1: 견고한 입력 검증】")
print("-" * 60)
print("""
요구사항:
  • 사용자로부터 이름, 나이, 이메일 입력
  • 각 항목에 대한 에러 처리
  • 나이는 1~150 범위 확인
  • 이메일은 '@' 포함 확인

코드 스케치:
  try:
      name = input("이름: ")
      age = int(input("나이: "))
      email = input("이메일: ")

      if not (1 <= age <= 150):
          raise ValueError("나이 범위 오류")
      if '@' not in email:
          raise ValueError("이메일 형식 오류")

      print("✅ 모든 정보가 유효합니다!")
  except ValueError as e:
      print(f"❌ 입력 오류: {e}")
""")

print("\n【 프로젝트 2: 안전한 파일 처리】")
print("-" * 60)
print("""
요구사항:
  • JSON 파일 읽기 (없을 수 있음)
  • 데이터 검증 (필수 필드 확인)
  • 에러 시 기본값 사용
  • 모든 작업 후 정리

코드 스케치:
  try:
      with open('config.json') as f:
          config = json.load(f)

      required_keys = ['name', 'version']
      for key in required_keys:
          if key not in config:
              raise KeyError(f"필수 항목 {key} 없음")

      print("✅ 설정 파일 로드 성공!")

  except FileNotFoundError:
      print("⚠️  파일 없음, 기본값 사용")
      config = {'name': 'default', 'version': '1.0'}
  except json.JSONDecodeError:
      print("⚠️  JSON 형식 오류, 기본값 사용")
      config = {'name': 'default', 'version': '1.0'}
  finally:
      print("정리 작업 실행")
""")

print("\n【 프로젝트 3: 데이터 변환 파이프라인】")
print("-" * 60)
print("""
요구사항:
  • CSV 파일에서 학생 정보 읽기
  • 각 행을 변환 (이름 대문자, 점수 확인)
  • 오류 행은 스킵하고 로그 남기기
  • 결과를 새 파일로 저장

코드 스케치:
  errors = []
  valid_data = []

  try:
      with open('students.csv') as f:
          for line in f:
              try:
                  parts = line.strip().split(',')
                  name = parts[0].upper()
                  score = int(parts[1])

                  if not (0 <= score <= 100):
                      raise ValueError("점수 범위 오류")

                  valid_data.append((name, score))
              except (ValueError, IndexError) as e:
                  errors.append(f"{line}: {e}")
  except FileNotFoundError:
      print("파일 없음!")

  finally:
      print(f"처리 완료: {len(valid_data)}행 성공, {len(errors)}행 오류")
""")

# ============================================================================
# 최종 정리 및 축하
# ============================================================================

print("\n" + "=" * 80)
print("【 고등학교 1학년: 예외 처리 마스터! 】")
print("=" * 80)

print("""
이제 여러분은 '에러 앞에서도 당당한' 프로그래머입니다! 😎

✅ 배운 개념:
   • try-except의 기본 구조
   • 여러 종류의 예외 처리
   • as 키워드로 에러 정보 가져오기
   • finally로 정리 작업 보장
   • Exception으로 모든 에러 처리

✅ 이해한 철학:
   • 에러는 '나쁜 것'이 아니라 '예측하는 것'
   • 프로그램의 견고성이 중요
   • 사용자 경험을 고려한 에러 메시지
   • 복구 가능한 경우만 처리

✅ 적용한 기술:
   • 안전한 사용자 입력 처리
   • 파일 I/O 예외 처리
   • 데이터 검증 및 변환
   • 오류 로깅

이제 여러분의 프로그램은:
   ✨ 사용자의 잘못된 입력에도 견딥니다
   ✨ 파일이 없어도 안전합니다
   ✨ 예기치 않은 상황에도 대응합니다
   ✨ 전문가처럼 보입니다!
""")

print("\n" + "=" * 80)
print("저장 필수: 너는 기록이 증명이다 gogs. 👑")
print("=" * 80)

print("""
💡 오늘의 깨달음:
   좋은 프로그래머는 '에러가 없는' 코드를 쓰는 게 아니라
   '에러에 대응하는' 코드를 씁니다.

   예외 처리는 프로그램의 방어막입니다.
   강한 프로그래머는 모든 가능성을 예측하고 대비합니다.

🎓 축하합니다!
   고등학교 1학년 첫 번째 단원을 완수했습니다!
   이제 여러분은 '견고한 코드'를 작성할 수 있습니다!

🎒 다음 단계:
   [고등학교 v2.2: 클래스와 객체 지향 — 나만의 복잡한 시스템 설계]
   객체 지향 프로그래밍으로 대규모 시스템을 구축합니다!

축하합니다! 👏
이제 여러분은 '에러 앞에서도 당당한' 파이썬 개발자입니다!
에러를 예측하고 대응하는 것이 프로의 증명입니다! 👑
""")
