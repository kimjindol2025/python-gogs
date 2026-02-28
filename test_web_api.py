"""웹 서버 API 테스트"""

import sys
sys.path.insert(0, '.')

from university_v7_app import app, init_db
import json

# DB 초기화
init_db()

# 테스트 클라이언트
client = app.test_client()

print("\n" + "="*80)
print("【 Python University v7 - 웹 API 테스트 】")
print("="*80)

# Test 1: 학생 목록 조회
print("\n【 Test 1: 학생 목록 조회 】")
response = client.get('/api/students')
data = json.loads(response.data)
print(f"✅ 학생 {len(data)}명 조회 완료")
for s in data[:3]:
    print(f"   - {s['student_id']}: {s['name']} ({s['department_name']})")

# Test 2: 학과 정보 조회
print("\n【 Test 2: 학과 정보 조회 】")
response = client.get('/api/departments')
data = json.loads(response.data)
print(f"✅ 학과 {len(data)}개 조회 완료")
for d in data:
    print(f"   - {d['name']}: {d['student_count']}명, 평균 GPA {(d['avg_gpa'] or 0):.2f}")

# Test 3: 교과목 조회
print("\n【 Test 3: 교과목 조회 】")
response = client.get('/api/courses')
data = json.loads(response.data)
print(f"✅ 교과목 {len(data)}개 조회 완료")
for c in data[:3]:
    print(f"   - {c['code']}: {c['name']} ({c['credits']}학점)")

# Test 4: 학생 상세 정보
print("\n【 Test 4: 학생 상세 정보 】")
response = client.get('/api/student/1')
data = json.loads(response.data)
print(f"✅ {data['student']['name']} 학생 정보 조회")
print(f"   - 학번: {data['student']['student_id']}")
print(f"   - 학과: {data['student']['department_name']}")
print(f"   - GPA: {data['student']['gpa']}")
print(f"   - 수강 과목: {len(data['grades'])}개")
for g in data['grades']:
    print(f"     • {g['code']}: {g['score']} ({g['grade']})")

# Test 5: 학생 추가
print("\n【 Test 5: 학생 추가 】")
response = client.post('/api/add_student',
    json={'student_id': '2024099', 'name': 'Test Student', 'department_id': 1},
    content_type='application/json')
data = json.loads(response.data)
if data['success']:
    print(f"✅ 신규 학생 추가 성공 (ID: {data['id']})")
else:
    print(f"❌ 실패: {data['error']}")

# Test 6: 성적 추가
print("\n【 Test 6: 성적 추가 】")
response = client.post('/api/add_grade',
    json={'student_id': 1, 'course_id': 1, 'score': 98.0, 'grade': 'A+'},
    content_type='application/json')
data = json.loads(response.data)
if data['success']:
    print(f"✅ 성적 추가 성공")
else:
    print(f"❌ 실패: {data['error']}")

# Test 7: 출석 기록
print("\n【 Test 7: 출석 기록 】")
response = client.post('/api/mark_attendance',
    json={'student_id': 1, 'status': 'present'},
    content_type='application/json')
data = json.loads(response.data)
if data['success']:
    print(f"✅ 출석 기록 성공")
else:
    print(f"❌ 실패: {data['error']}")

# Test 8: 메인 페이지
print("\n【 Test 8: 메인 대시보드 】")
response = client.get('/')
if response.status_code == 200:
    print(f"✅ 메인 페이지 정상 작동 ({len(response.data)} bytes)")
else:
    print(f"❌ 실패 (상태코드: {response.status_code})")

print("\n" + "="*80)
print("✅ 모든 API 테스트 완료!")
print("="*80)
print("\n【 웹 서버 실행 방법 】")
print("  $ ./RUN_WEB_SERVER.sh")
print("  또는")
print("  $ python3 university_v7_app.py")
print("\n【 접속 주소 】")
print("  🌐 http://localhost:5000")
print("\n저장 필수 너는 기록이 증명이다 gogs")
print("="*80 + "\n")
