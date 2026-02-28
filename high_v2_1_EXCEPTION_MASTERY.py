#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
파이썬 고등학교 1학년 - v2.1-Advanced: 예외 처리 마스터리
    — 실패를 데이터로 전환하는 기술
================================================================================

【 이 파일의 목표 】
v2.1을 다시 깊게 파고들어서, '완전 마스터'가 되기

v2.1 (기초)은 try-except의 개념을 배웠습니다.
v2.1-Advanced (심화)는:
  - 예외 처리의 철학을 이해합니다
  - 7가지 Exception 타입을 깊게 알아봅니다
  - 사용자 정의 예외를 설계합니다
  - 에러 로깅 시스템을 구축합니다
  - LBYL vs EAFP를 비교합니다

결과:
  "코드가 실패했을 때"를 "기록이 남은 성공"으로 전환하는 능력


================================================================================
【 파트 1: 예외 처리의 철학 — "실패는 정보다" 】
================================================================================

【 핵심 질문 】
당신의 프로그램이 실패했을 때, 당신은 뭘 합니까?

❌ 나쁜 선택:
  시스템이 갑자기 꺼집니다 (Crash)
  → 데이터 손실
  → 사용자 신뢰 상실
  → 무슨 문제인지 알 수 없음

✅ 좋은 선택:
  실패를 감지하고 기록합니다
  → 데이터 보존
  → 사용자에게 친절한 메시지
  → 문제를 분석할 수 있음

【 예시 】

나쁜 설계:
  파일을 읽으려고 시도
  → 파일이 없음 (에러!)
  → 프로그램 강제 종료
  → 사용자: "뭐야?!"

좋은 설계:
  파일을 읽으려고 시도
  → 파일이 없음 (에러 감지!)
  → except 구간에서 처리
  → "파일을 찾을 수 없습니다. 기본값을 사용합니다"
  → 프로그램 계속 실행
  → 에러를 로그 파일에 기록

이것이 "전문가의 설계"입니다.


================================================================================
【 파트 2: 4단계 예외 처리 구조 깊게 이해 】
================================================================================

【 구조 1: try-except 】

기본:
  try:
      (위험할 수 있는 코드)
  except SpecificError:
      (에러 처리)

예시:
  try:
      result = 10 / 0
  except ZeroDivisionError:
      print("0으로 나눌 수 없습니다")

의미:
  - try 블록에서 에러 발생 가능성 있는 코드 실행
  - 에러 발생 시 except 블록으로 즉시 점프
  - except 블록에서 처리 후 프로그램 계속


【 구조 2: try-except-else 】

확장:
  try:
      (위험할 수 있는 코드)
  except SpecificError:
      (에러 처리)
  else:
      (에러가 없을 때만 실행)

의미:
  - else는 try가 성공했을 때만 실행
  - 성공한 경우와 실패한 경우를 명확히 분리
  - "축하 구간"

예시:
  try:
      file = open("data.txt", "r")
      content = file.read()
  except FileNotFoundError:
      print("파일을 찾을 수 없습니다")
  else:
      print(f"파일 읽기 성공! 크기: {len(content)} 바이트")


【 구조 3: try-except-finally 】

최고 권장:
  try:
      (위험할 수 있는 코드)
  except SpecificError:
      (에러 처리)
  finally:
      (성공하든 실패하든 반드시 실행)

의미:
  - finally는 무조건 실행됨
  - 정리(Cleanup) 작업에 사용
  - 리소스 해제, 파일 닫기, DB 연결 종료 등

예시:
  try:
      file = open("data.txt", "r")
      content = file.read()
  except FileNotFoundError:
      print("파일을 찾을 수 없습니다")
  finally:
      print("파일 처리 완료")
      if 'file' in locals():
          file.close()


【 구조 4: try-except-else-finally (완전한 형태) 】

전체:
  try:
      (위험할 수 있는 코드)
  except SpecificError:
      (에러 처리)
  else:
      (성공했을 때만)
  finally:
      (항상 정리)

흐름:
  성공 경로:
    try 실행 → except 스킵 → else 실행 → finally 실행

  실패 경로:
    try 에러 발생 → except 실행 → else 스킵 → finally 실행


================================================================================
【 파트 3: 7가지 Exception 타입 깊게 파기 】
================================================================================

파이썬이 제공하는 기본 Exception들:

【 1️⃣ ValueError 】
의미: 값이 잘못되었을 때

예시:
  try:
      age = int("twenty")
  except ValueError:
      print("숫자가 아닙니다")

언제 발생:
  - int("abc") ← 정수가 아닌 문자열
  - float("hello") ← 실수가 아닌 문자열


【 2️⃣ ZeroDivisionError 】
의미: 0으로 나누었을 때

예시:
  try:
      result = 100 / 0
  except ZeroDivisionError:
      print("0으로 나눌 수 없습니다")

언제 발생:
  - a / 0
  - a // 0
  - a % 0


【 3️⃣ FileNotFoundError 】
의미: 파일이 없을 때

예시:
  try:
      with open("missing.txt", "r") as f:
          content = f.read()
  except FileNotFoundError:
      print("파일이 없습니다")

언제 발생:
  - open("존재하지않는파일.txt")
  - os.remove("없는파일.txt")


【 4️⃣ TypeError 】
의미: 타입이 맞지 않을 때

예시:
  try:
      result = "Hello" + 5
  except TypeError:
      print("문자열과 숫자를 더할 수 없습니다")

언제 발생:
  - "string" + 123
  - len(123)
  - 호출할 수 없는 것을 호출할 때


【 5️⃣ IndexError 】
의미: 인덱스가 범위를 벗어났을 때

예시:
  try:
      lst = [1, 2, 3]
      item = lst[10]
  except IndexError:
      print("인덱스 범위를 벗어났습니다")

언제 발생:
  - list[100] (리스트 길이 초과)
  - tuple[-999] (음수 인덱스 범위 초과)


【 6️⃣ KeyError 】
의미: 딕셔너리 키가 없을 때

예시:
  try:
      data = {"name": "Alice"}
      value = data["age"]
  except KeyError:
      print("키가 없습니다")

언제 발생:
  - dict["없는키"]
  - student["email"] (email 키가 없을 때)


【 7️⃣ AttributeError 】
의미: 객체에 속성이 없을 때

예시:
  try:
      class Dog:
          def bark(self):
              print("멍멍")

      dog = Dog()
      dog.fly()
  except AttributeError:
      print("객체에 그 메서드/속성이 없습니다")

언제 발생:
  - obj.없는속성
  - module.없는함수


================================================================================
【 파트 4: 다중 Exception 처리 (여러 에러 한 번에) 】
================================================================================

【 방법 1: 여러 except 사용 】

구조:
  try:
      (코드)
  except ValueError:
      (ValueError 처리)
  except ZeroDivisionError:
      (ZeroDivisionError 처리)
  except TypeError:
      (TypeError 처리)

의미:
  - 각 Exception마다 다르게 처리
  - 첫 번째 매칭되는 except 실행 후 다음으로 이동

예시 (데이터 입력 검증):
  try:
      age = int(input("나이: "))
      result = 100 / age
  except ValueError:
      print("숫자를 입력하세요")
  except ZeroDivisionError:
      print("0이 아닌 숫자를 입력하세요")


【 방법 2: 튜플로 여러 Exception 한 번에 】

구조:
  try:
      (코드)
  except (ValueError, TypeError):
      (같은 처리)

의미:
  - 두 Exception을 같은 방식으로 처리할 때 효율적

예시:
  try:
      data = input("데이터: ")
      result = int(data) / 5
  except (ValueError, TypeError):
      print("올바른 숫자를 입력하세요")


【 방법 3: Exception 객체 접근 】

구조:
  try:
      (코드)
  except ValueError as e:
      print(f"에러 메시지: {e}")

의미:
  - 에러 자체에 대한 정보를 얻음
  - as 키워드로 Exception 객체를 변수에 저장

예시:
  try:
      age = int("hello")
  except ValueError as error:
      print(f"에러 타입: {type(error)}")
      print(f"에러 메시지: {error}")

출력:
  에러 타입: <class 'ValueError'>
  에러 메시지: invalid literal for int() with base 10: 'hello'


【 방법 4: 모든 Exception 잡기 】

구조:
  try:
      (코드)
  except Exception as e:
      print(f"뭔가 잘못됐습니다: {e}")

주의:
  - Exception은 모든 에러의 부모 클래스
  - 너무 포괄적이라 권장하지 않음
  - 항상 구체적인 Exception을 명시하세요!

나쁜 예:
  try:
      data = process()
  except:
      print("에러 발생")
  (어떤 에러인지 모름, 디버깅 어려움)

좋은 예:
  try:
      data = process()
  except ValueError as e:
      print(f"값 에러: {e}")
  except FileNotFoundError as e:
      print(f"파일 에러: {e}")


================================================================================
【 파트 5: 사용자 정의 Exception (Custom Exception) 】
================================================================================

【 왜 필요한가? 】

파이썬의 기본 Exception만으로는 부족할 때:
  - 우리 시스템만의 규칙을 정의하고 싶을 때
  - 특정 비즈니스 로직에 맞는 에러가 필요할 때

예시:
  은행 시스템에서 "잔액 부족" 에러는 파이썬에 없음
  → 우리가 만들어야 함: InsufficientBalanceError


【 사용자 정의 Exception 만들기 】

구조:
  class CustomError(Exception):
      pass

또는 메시지 포함:
  class CustomError(Exception):
      def __init__(self, message):
          self.message = message
          super().__init__(self.message)

예시:
  class GogsExperimentError(Exception):
      "Gogs 연구실에서 발생하는 에러"
      pass

  class InsufficientBalanceError(Exception):
      "잔액 부족 에러"
      def __init__(self, balance, required):
          self.balance = balance
          self.required = required
          message = f"잔액 부족. 현재: {balance}, 필요: {required}"
          super().__init__(message)


【 사용자 정의 Exception 사용 】

구조:
  try:
      if 조건:
          raise CustomError("에러 메시지")
  except CustomError as e:
      print(f"처리: {e}")

예시:
  def withdraw(account_balance, amount):
      if amount > account_balance:
          raise InsufficientBalanceError(account_balance, amount)
      return account_balance - amount

  try:
      result = withdraw(1000, 5000)
  except InsufficientBalanceError as e:
      print(f"트랜잭션 실패: {e}")


【 Exception 상속 계층 】

기본 구조:
  BaseException
    ├─ Exception (대부분의 에러)
    │   ├─ ValueError
    │   ├─ TypeError
    │   ├─ FileNotFoundError
    │   └─ ... (파이썬 기본 Exception들)
    │
    ├─ GogsExperimentError (우리가 만든 에러)
    │   ├─ DataValidationError
    │   ├─ ConfigurationError
    │   └─ ProcessingError
    │
    └─ KeyboardInterrupt (Ctrl+C)

의미:
  - 우리가 만든 Exception도 Exception의 자식
  - 따라서 except Exception으로도 잡을 수 있음
  - 하지만 구체적으로 명시하는 게 좋음


================================================================================
【 파트 6: 로깅 시스템 구축 (기록이 증명) 】
================================================================================

【 왜 로깅이 필요한가? 】

상황 1: 프로그램이 실패했다
→ 언제? 어디서? 왜?를 알아야 함
→ print()로는 부족함 (휘발성)
→ 파일에 기록해야 함

상황 2: 프로그램이 성공했다
→ 무엇을 했는가?
→ 얼마나 걸렸는가?
→ 기록이 필요함


【 간단한 로깅 시스템 만들기 】

구조:
  import datetime

  def log_error(error_type, error_message):
      timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      log_entry = f"[{timestamp}] {error_type}: {error_message}\n"

      with open("error_log.txt", "a", encoding="utf-8") as f:
          f.write(log_entry)

사용:
  try:
      age = int("hello")
  except ValueError as e:
      log_error("ValueError", str(e))
      print("올바른 숫자를 입력하세요")

결과 (error_log.txt):
  [2026-02-24 15:30:45] ValueError: invalid literal for int() with base 10: 'hello'
  [2026-02-24 15:31:12] ValueError: invalid literal for int() with base 10: 'abc'


【 Python 표준 logging 모듈 】

더 전문적으로:
  import logging

  logging.basicConfig(
      filename="app.log",
      level=logging.INFO,
      format="%(asctime)s - %(levelname)s - %(message)s"
  )

사용:
  try:
      data = process()
  except ValueError as e:
      logging.error(f"처리 실패: {e}")
  except Exception as e:
      logging.critical(f"심각한 에러: {e}")

로그 레벨:
  - DEBUG: 상세한 정보
  - INFO: 일반 정보
  - WARNING: 경고
  - ERROR: 에러
  - CRITICAL: 심각한 에러


================================================================================
【 파트 7: LBYL vs EAFP — 파이썬의 철학 】
================================================================================

【 LBYL: Look Before You Leap 】

의미: "뛰기 전에 살펴라"
방식: if 문으로 미리 체크

예시:
  # LBYL 방식
  if len(my_list) > 0:
      first = my_list[0]
  else:
      print("리스트가 비어있습니다")

장점:
  - 예측 가능함
  - 명확한 의도

단점:
  - 코드가 길어짐
  - 모든 경우를 다 체크해야 함


【 EAFP: Easier to Ask for Forgiveness than Permission 】

의미: "허락보다 용서를 구하기가 쉽다"
방식: try-except로 에러를 처리

예시:
  # EAFP 방식 (파이썬 권장)
  try:
      first = my_list[0]
  except IndexError:
      print("리스트가 비어있습니다")

장점:
  - 코드가 짧음
  - 파이썬다움 (Pythonic)
  - 일반적인 경우는 빠름

단점:
  - 에러 발생 시 약간의 오버헤드


【 파이썬의 권장 사항 】

파이썬은 EAFP를 권장합니다!

좋은 코드:
  try:
      file = open("data.txt", "r")
  except FileNotFoundError:
      file = open("default.txt", "r")

나쁜 코드:
  import os
  if os.path.exists("data.txt"):
      file = open("data.txt", "r")
  else:
      file = open("default.txt", "r")

(첫 번째가 더 파이썬다움)


================================================================================
【 파트 8: 실전 프로젝트 — 안전한 데이터 처리 시스템 】
================================================================================

【 프로젝트 개요 】

목표: 사용자 입력을 받아서 검증하고 저장하는 시스템
특징: 모든 에러를 처리하고 기록함

구조:
  1. 사용자 입력받기
  2. 데이터 검증
  3. 파일에 저장
  4. 모든 과정에 예외 처리 + 로깅


【 코드 구조 설명 】

Step 1: 사용자 정의 Exception 만들기

class ValidationError(Exception):
    "데이터 검증 에러"
    pass

class StorageError(Exception):
    "파일 저장 에러"
    pass


Step 2: 검증 함수 만들기

def validate_age(age_str):
    try:
        age = int(age_str)
        if age < 0 or age > 150:
            raise ValidationError("나이는 0~150 사이여야 합니다")
        return age
    except ValueError as e:
        raise ValidationError(f"숫자가 아닙니다: {e}")


Step 3: 저장 함수 만들기

def save_to_file(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(data))
    except IOError as e:
        raise StorageError(f"파일 저장 실패: {e}")
    finally:
        print("파일 처리 완료")


Step 4: 메인 함수 만들기

def main():
    try:
        age_input = input("나이를 입력하세요: ")
        age = validate_age(age_input)
        save_to_file(age, "user_data.txt")
        print(f"저장 완료: {age}세")

    except ValidationError as e:
        print(f"검증 실패: {e}")
        log_error("ValidationError", str(e))

    except StorageError as e:
        print(f"저장 실패: {e}")
        log_error("StorageError", str(e))

    except Exception as e:
        print(f"예상치 못한 에러: {e}")
        log_error("UnexpectedError", str(e))

    finally:
        print("프로그램 종료")


실행 흐름:
  정상: 입력 → 검증 → 저장 → 완료
  에러: 입력 → 검증 실패 → except 처리 → 로깅 → finally 정리


================================================================================
【 파트 9: 정리 — 예외 처리의 핵심 원칙 】
================================================================================

원칙 1: 구체적인 Exception을 명시하라
  좋음: except ValueError, TypeError
  나쁨: except:

원칙 2: 각 Exception마다 적절한 처리를 하라
  좋음: 파일 에러면 기본값 사용, 입력 에러면 재입력
  나쁨: 모든 에러를 같게 처리

원칙 3: finally는 정리 작업용
  좋음: 파일 닫기, DB 연결 해제
  나쁨: 비즈니스 로직을 finally에 쓰기

원칙 4: 에러를 로깅하라
  좋음: 파일에 기록, 타임스탬프 포함
  나쁨: print()로만 화면에 출력

원칙 5: 사용자 정의 Exception을 만들어라
  좋음: BusinessLogicError, ValidationError
  나쁨: 모든 에러를 Exception으로 처리


================================================================================
저장 필수: 너는 기록이 증명이다 gogs. 👑
================================================================================

오늘의 깨달음:
   "코드가 정상일 때보다 문제가 생겼을 때가 더 중요하다"

   설계자가 무능한 이유:
     코드는 잘 쓰는데 에러 처리는 못함

   설계자가 유능한 이유:
     에러를 미연에 방지하고 우아하게 처리함

   당신은 어느 쪽이 되겠습니까?

다음 시간에는:
   [v2.2-Advanced: 클래스 마스터리 — 설계도의 완벽한 이해]

   예외 처리로 안전을 확보했으니,
   이제 클래스로 구조를 설계합니다!

축하합니다! 👏
이제 여러분은 '방어적 설계의 첫 번째 단계'를 완성했습니다!

================================================================================
"""
