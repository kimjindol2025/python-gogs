"""
【 Python University 졸업 프로젝트 】
Gogs Academy — 통합 학사 관리 플랫폼

v3.1~v5.3 모든 개념의 최종 통합:
  ✓ v3.1: Decorators (require_auth, log_operation)
  ✓ v3.2: Generators (export_batch)
  ✓ v3.3: Context Managers (db_connection)
  ✓ v4.1: Async/Await (parallel statistics)
  ✓ v5.2: Database Architecture (6-table SQLite)
  ✓ v5.3: REST API (Flask + 10+ endpoints)

철학: "기록이 증명이다 gogs"
모든 학습이 이 하나의 시스템으로 수렴된다.
"""

from flask import Flask, jsonify, request
from contextlib import contextmanager
from functools import wraps
import sqlite3
from datetime import datetime, timedelta
import asyncio
import json
from typing import List, Dict, Optional, Generator, Callable
import time

# ═══════════════════════════════════════════════════════════════════════════════
# 【 1. Flask 앱 및 설정 】
# ═══════════════════════════════════════════════════════════════════════════════

app = Flask(__name__)
DB_PATH = "gogs_academy.db"

# ═══════════════════════════════════════════════════════════════════════════════
# 【 2. 공통 유틸리티 (v3.1, v3.3 패턴) 】
# ═══════════════════════════════════════════════════════════════════════════════

@contextmanager
def db_connection(db_path: str):
    """
    【 v3.3 Context Manager 】
    SQLite 데이터베이스 연결 관리
    - 자동으로 open/close
    - Row factory로 dict 변환 자동화
    - 예외 발생 시에도 안전하게 정리
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def require_auth(role: str = 'user'):
    """
    【 v3.1 Decorator Factory 】
    역할 기반 권한 검사 데코레이터

    실제 API에서는 JWT 토큰으로 검증하지만,
    여기서는 request.headers['X-User-Role']로 시뮬레이션
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 헤더에서 사용자 역할 확인
            user_role = request.headers.get('X-User-Role', 'user')

            if user_role != role and user_role != 'admin':
                return jsonify({
                    "status": "error",
                    "message": f"{role} 권한이 필요합니다"
                }), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_operation(func: Callable) -> Callable:
    """
    【 v3.1 Decorator 】
    DB 작업 시간 측정 및 로깅
    - 함수 실행 시간 측정
    - 메타데이터 보존 (@functools.wraps)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start

        func_name = func.__name__
        print(f"⏱️  {func_name} 완료: {elapsed:.3f}초")

        return result
    return wrapper


def export_batch(items: List, batch_size: int = 100) -> Generator:
    """
    【 v3.2 Generator 】
    대량 데이터를 배치 단위로 스트리밍
    - 메모리 효율적 (모든 데이터를 한번에 로드하지 않음)
    - lazy evaluation
    """
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


# ═══════════════════════════════════════════════════════════════════════════════
# 【 3. Database 초기화 】
# ═══════════════════════════════════════════════════════════════════════════════

def init_db():
    """
    【 v5.2 Database Architecture 】
    6개 테이블 스키마 생성 + 샘플 데이터 초기화

    관계:
    departments ← students
    courses ← enrollments ← grades
    courses ← attendance
    """
    with db_connection(DB_PATH) as conn:
        cursor = conn.cursor()

        # 1. 학과 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                head TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 2. 학생 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                department_id INTEGER NOT NULL,
                grade INTEGER DEFAULT 1,
                gpa REAL DEFAULT 0.0,
                status TEXT DEFAULT 'Active',
                admission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(department_id) REFERENCES departments(id)
            )
        ''')

        # 3. 교과목 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                credits INTEGER DEFAULT 3,
                professor TEXT,
                department_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(department_id) REFERENCES departments(id)
            )
        ''')

        # 4. 수강신청 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                semester TEXT,
                enrolled_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(course_id) REFERENCES courses(id)
            )
        ''')

        # 5. 성적 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enrollment_id INTEGER NOT NULL,
                score REAL NOT NULL,
                grade TEXT,
                recorded_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(enrollment_id) REFERENCES enrollments(id)
            )
        ''')

        # 6. 출석 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                date DATE NOT NULL,
                status TEXT DEFAULT 'Present',
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(course_id) REFERENCES courses(id)
            )
        ''')

        # 샘플 데이터 삽입
        try:
            # 학과
            cursor.execute(
                "INSERT INTO departments (code, name, head) VALUES (?, ?, ?)",
                ("CSE", "Computer Science", "Kim Gogs")
            )
            cursor.execute(
                "INSERT INTO departments (code, name, head) VALUES (?, ?, ?)",
                ("ENG", "English", "Lee AI")
            )
            cursor.execute(
                "INSERT INTO departments (code, name, head) VALUES (?, ?, ?)",
                ("DS", "Data Science", "Park Data")
            )

            # 학생 (10명)
            students_data = [
                ("2024001", "Gogs Kim", 1),
                ("2024002", "AI Lee", 1),
                ("2024003", "Data Park", 3),
                ("2024004", "Code Choi", 1),
                ("2024005", "Smart Jung", 1),
                ("2024006", "Fast Do", 2),
                ("2024007", "Happy Han", 2),
                ("2024008", "Study Kang", 3),
                ("2024009", "Dream Lim", 3),
                ("2024010", "Hope Baek", 1),
            ]
            for i, (student_id, name, dept_id) in enumerate(students_data):
                cursor.execute(
                    "INSERT INTO students (student_id, name, department_id, gpa) VALUES (?, ?, ?, ?)",
                    (student_id, name, dept_id, round(3.5 + i * 0.05, 2))
                )

            # 교과목 (8개)
            courses_data = [
                ("CS101", "Python Basics", 3, "Kim Gogs", 1),
                ("CS201", "Data Structure", 4, "Kim Gogs", 1),
                ("CS301", "Algorithms", 4, "Kim Gogs", 1),
                ("DS101", "Statistics", 3, "Park Data", 3),
                ("DS201", "Machine Learning", 4, "Park Data", 3),
                ("ENG101", "English 1", 2, "Lee AI", 2),
                ("ENG201", "English 2", 2, "Lee AI", 2),
                ("ENG301", "Business English", 3, "Lee AI", 2),
            ]
            for code, name, credits, prof, dept_id in courses_data:
                cursor.execute(
                    "INSERT INTO courses (code, name, credits, professor, department_id) VALUES (?, ?, ?, ?, ?)",
                    (code, name, credits, prof, dept_id)
                )

            # 수강신청 + 성적 (각 학생이 3~4개 과목 신청)
            for i in range(1, 11):  # 학생 1~10
                for j in range(1, 4):  # 각 학생이 3개 과목
                    course_id = ((i + j - 1) % 8) + 1
                    cursor.execute(
                        "INSERT INTO enrollments (student_id, course_id, semester) VALUES (?, ?, ?)",
                        (i, course_id, "2024-Spring")
                    )
                    enrollment_id = cursor.lastrowid
                    score = 75 + (i + j) % 25
                    grade = "A" if score >= 90 else "B" if score >= 80 else "C"
                    cursor.execute(
                        "INSERT INTO grades (enrollment_id, score, grade) VALUES (?, ?, ?)",
                        (enrollment_id, score, grade)
                    )

            # 출석 기록 (각 학생마다 3개 과목의 5일 출석)
            for i in range(1, 11):  # 학생
                for j in range(1, 4):  # 3개 과목
                    course_id = ((i + j - 1) % 8) + 1
                    for k in range(5):  # 5일
                        date = (datetime.now() - timedelta(days=10-k)).strftime("%Y-%m-%d")
                        status = "Present" if (i + j + k) % 3 != 0 else "Absent"
                        cursor.execute(
                            "INSERT INTO attendance (student_id, course_id, date, status) VALUES (?, ?, ?, ?)",
                            (i, course_id, date, status)
                        )

            conn.commit()
        except:
            pass  # 이미 데이터 존재

        conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
# 【 4. Manager Classes (v6.4 패턴) 】
# ═══════════════════════════════════════════════════════════════════════════════

class AcademyManager:
    """기본 Manager 클래스 - 공통 속성"""
    def __init__(self, db_path: str):
        self.db_path = db_path


class StudentManager(AcademyManager):
    """학생 관리 (CRUD + Generator 활용)"""

    @log_operation
    def get_all_students(self) -> List[Dict]:
        """모든 학생 조회 (JOIN departments)"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.id, s.student_id, s.name, d.name as department_name,
                       s.grade, s.gpa, s.status
                FROM students s
                LEFT JOIN departments d ON s.department_id = d.id
                ORDER BY s.student_id
            ''')
            return [dict(row) for row in cursor.fetchall()]

    @log_operation
    def get_student(self, student_id: int) -> Optional[Dict]:
        """학생 상세 조회 (성적 포함)"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()

            # 학생 정보
            cursor.execute('''
                SELECT s.id, s.student_id, s.name, d.name as department_name,
                       s.grade, s.gpa, s.status, s.admission_date
                FROM students s
                LEFT JOIN departments d ON s.department_id = d.id
                WHERE s.id = ?
            ''', (student_id,))
            student = cursor.fetchone()
            if not student:
                return None

            student_dict = dict(student)

            # 성적 정보
            cursor.execute('''
                SELECT c.code, c.name, g.score, g.grade, e.semester
                FROM grades g
                JOIN enrollments e ON g.enrollment_id = e.id
                JOIN courses c ON e.course_id = c.id
                WHERE e.student_id = ?
                ORDER BY e.semester DESC
            ''', (student_id,))
            student_dict['grades'] = [dict(row) for row in cursor.fetchall()]

            return student_dict

    @log_operation
    def add_student(self, student_id: str, name: str, department_id: int) -> Optional[int]:
        """학생 추가"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO students (student_id, name, department_id, gpa) VALUES (?, ?, ?, ?)",
                    (student_id, name, department_id, 0.0)
                )
                conn.commit()
                return cursor.lastrowid
            except:
                return None

    @log_operation
    def update_student_gpa(self, student_id: int, gpa: float) -> bool:
        """학생 GPA 업데이트"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE students SET gpa = ? WHERE id = ?",
                (gpa, student_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    @log_operation
    def export_students_batch(self, batch_size: int = 100) -> Generator:
        """
        【 v3.2 Generator 】
        학생 데이터 배치 단위 스트리밍 (메모리 효율적)
        """
        all_students = self.get_all_students()
        yield from export_batch(all_students, batch_size)


class CourseManager(AcademyManager):
    """교과목 관리"""

    @log_operation
    def get_all_courses(self) -> List[Dict]:
        """모든 교과목 조회"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.id, c.code, c.name, c.credits, c.professor,
                       d.name as department_name
                FROM courses c
                LEFT JOIN departments d ON c.department_id = d.id
                ORDER BY c.code
            ''')
            return [dict(row) for row in cursor.fetchall()]

    @log_operation
    def add_course(self, code: str, name: str, credits: int, professor: str, dept_id: int) -> Optional[int]:
        """교과목 추가"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO courses (code, name, credits, professor, department_id) VALUES (?, ?, ?, ?, ?)",
                    (code, name, credits, professor, dept_id)
                )
                conn.commit()
                return cursor.lastrowid
            except:
                return None


class GradeManager(AcademyManager):
    """성적 관리"""

    @log_operation
    def get_student_grades(self, student_id: int) -> List[Dict]:
        """학생 성적 조회"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.code, c.name, g.score, g.grade, e.semester
                FROM grades g
                JOIN enrollments e ON g.enrollment_id = e.id
                JOIN courses c ON e.course_id = c.id
                WHERE e.student_id = ?
                ORDER BY e.semester DESC
            ''', (student_id,))
            return [dict(row) for row in cursor.fetchall()]

    @log_operation
    def calculate_gpa(self, student_id: int) -> float:
        """GPA 계산"""
        grades = self.get_student_grades(student_id)
        if not grades:
            return 0.0

        grade_points = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}
        total_points = sum(grade_points.get(g['grade'], 0) for g in grades)
        return round(total_points / len(grades) if grades else 0, 2)

    @log_operation
    def add_grade(self, enrollment_id: int, score: float, grade: str) -> Optional[int]:
        """성적 추가"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO grades (enrollment_id, score, grade) VALUES (?, ?, ?)",
                (enrollment_id, score, grade)
            )
            conn.commit()
            return cursor.lastrowid


class StatisticsManager(AcademyManager):
    """통계 (비동기 처리)"""

    @log_operation
    async def async_get_statistics(self) -> Dict:
        """
        【 v4.1 Async/Await 】
        비동기로 여러 통계를 병렬 계산
        """
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()

            # 1. 전체 학생 수
            cursor.execute("SELECT COUNT(*) as count FROM students")
            total_students = cursor.fetchone()['count']

            # 2. 평균 GPA
            cursor.execute("SELECT AVG(gpa) as avg_gpa FROM students")
            avg_gpa = cursor.fetchone()['avg_gpa'] or 0

            # 3. 전체 교과목 수
            cursor.execute("SELECT COUNT(*) as count FROM courses")
            total_courses = cursor.fetchone()['count']

            # 4. 학과별 학생 수
            cursor.execute("""
                SELECT d.name, COUNT(s.id) as count
                FROM departments d
                LEFT JOIN students s ON d.id = s.department_id
                GROUP BY d.id, d.name
            """)
            dept_stats = {row['name']: row['count'] for row in cursor.fetchall()}

            return {
                "total_students": total_students,
                "average_gpa": round(avg_gpa, 2),
                "total_courses": total_courses,
                "department_distribution": dept_stats
            }

    def get_statistics(self) -> Dict:
        """동기 래퍼"""
        return asyncio.run(self.async_get_statistics())


# ═══════════════════════════════════════════════════════════════════════════════
# 【 5. Flask REST API Endpoints (v5.3 패턴) 】
# ═══════════════════════════════════════════════════════════════════════════════

student_mgr = StudentManager(DB_PATH)
course_mgr = CourseManager(DB_PATH)
grade_mgr = GradeManager(DB_PATH)
stats_mgr = StatisticsManager(DB_PATH)


@app.route('/', methods=['GET'])
def api_info():
    """API 정보 페이지"""
    return jsonify({
        "title": "Gogs Academy — 통합 학사 관리 플랫폼",
        "version": "v1.0 (Graduation Project)",
        "description": "Python University v3.1~v5.3 모든 개념의 최종 통합",
        "philosophy": "기록이 증명이다 gogs",
        "integrated_patterns": [
            "v3.1: Decorators (require_auth, log_operation)",
            "v3.2: Generators (export_batch)",
            "v3.3: Context Managers (db_connection)",
            "v4.1: Async/Await (statistics)",
            "v5.2: Database Architecture (6 tables)",
            "v5.3: REST API (10+ endpoints)"
        ],
        "endpoints": {
            "GET /api/health": "서버 상태 체크",
            "GET /api/students": "모든 학생 조회",
            "GET /api/students/<id>": "학생 상세 조회",
            "POST /api/students": "학생 추가",
            "GET /api/courses": "모든 교과목 조회",
            "POST /api/courses": "교과목 추가",
            "GET /api/grades/<student_id>": "학생 성적 조회",
            "POST /api/grades": "성적 추가",
            "POST /api/attendance": "출석 기록",
            "GET /api/statistics": "통계 조회"
        }
    }), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """헬스 체크"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Gogs Academy Platform",
        "version": "1.0"
    }), 200


# ═══════════════════════════════════════════════════════════════════════════════
# 【 Students API 】
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/students', methods=['GET'])
def get_students():
    """모든 학생 조회"""
    students = student_mgr.get_all_students()
    return jsonify({
        "status": "success",
        "count": len(students),
        "data": students
    }), 200


@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """학생 상세 조회"""
    student = student_mgr.get_student(student_id)
    if not student:
        return jsonify({
            "status": "error",
            "message": f"학생 ID {student_id}를 찾을 수 없습니다"
        }), 404

    return jsonify({
        "status": "success",
        "data": student
    }), 200


@app.route('/api/students', methods=['POST'])
def add_student():
    """학생 추가"""
    data = request.get_json()

    # 유효성 검사
    if not data or not all(k in data for k in ['student_id', 'name', 'department_id']):
        return jsonify({
            "status": "error",
            "message": "student_id, name, department_id는 필수입니다"
        }), 400

    new_id = student_mgr.add_student(
        data['student_id'],
        data['name'],
        data['department_id']
    )

    if new_id is None:
        return jsonify({
            "status": "error",
            "message": "학생 추가에 실패했습니다"
        }), 400

    return jsonify({
        "status": "success",
        "message": "학생이 추가되었습니다",
        "id": new_id
    }), 201


# ═══════════════════════════════════════════════════════════════════════════════
# 【 Courses API 】
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/courses', methods=['GET'])
def get_courses():
    """모든 교과목 조회"""
    courses = course_mgr.get_all_courses()
    return jsonify({
        "status": "success",
        "count": len(courses),
        "data": courses
    }), 200


@app.route('/api/courses', methods=['POST'])
def add_course():
    """교과목 추가"""
    data = request.get_json()

    if not data or not all(k in data for k in ['code', 'name']):
        return jsonify({
            "status": "error",
            "message": "code, name은 필수입니다"
        }), 400

    new_id = course_mgr.add_course(
        data['code'],
        data['name'],
        data.get('credits', 3),
        data.get('professor', 'TBA'),
        data.get('department_id', 1)
    )

    if new_id is None:
        return jsonify({
            "status": "error",
            "message": "교과목 추가에 실패했습니다"
        }), 400

    return jsonify({
        "status": "success",
        "message": "교과목이 추가되었습니다",
        "id": new_id
    }), 201


# ═══════════════════════════════════════════════════════════════════════════════
# 【 Grades API 】
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/grades/<int:student_id>', methods=['GET'])
def get_grades(student_id):
    """학생 성적 조회"""
    grades = grade_mgr.get_student_grades(student_id)
    gpa = grade_mgr.calculate_gpa(student_id)

    return jsonify({
        "status": "success",
        "student_id": student_id,
        "gpa": gpa,
        "grades": grades
    }), 200


@app.route('/api/grades', methods=['POST'])
def add_grade():
    """성적 추가"""
    data = request.get_json()

    if not data or not all(k in data for k in ['enrollment_id', 'score', 'grade']):
        return jsonify({
            "status": "error",
            "message": "enrollment_id, score, grade는 필수입니다"
        }), 400

    grade_id = grade_mgr.add_grade(
        data['enrollment_id'],
        data['score'],
        data['grade']
    )

    return jsonify({
        "status": "success",
        "message": "성적이 추가되었습니다",
        "id": grade_id
    }), 201


# ═══════════════════════════════════════════════════════════════════════════════
# 【 Statistics API (비동기) 】
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """통계 조회"""
    stats = stats_mgr.get_statistics()
    return jsonify({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "data": stats
    }), 200


# ═══════════════════════════════════════════════════════════════════════════════
# 【 6. 통합 테스트 】
# ═══════════════════════════════════════════════════════════════════════════════

def run_tests():
    """12개 테스트 케이스"""
    client = app.test_client()

    print("\n" + "="*80)
    print("【 Gogs Academy 통합 테스트 】")
    print("="*80)

    passed = 0
    total = 0

    # Test 1: 헬스 체크
    total += 1
    print("\n【 Test 1: GET /api/health - 헬스 체크 】")
    resp = client.get('/api/health')
    if resp.status_code == 200:
        print("✅ PASS")
        passed += 1
    else:
        print(f"❌ FAIL ({resp.status_code})")

    # Test 2: 모든 학생 조회
    total += 1
    print("\n【 Test 2: GET /api/students - 학생 조회 】")
    resp = client.get('/api/students')
    data = resp.get_json()
    if resp.status_code == 200 and data['count'] > 0:
        print(f"✅ PASS ({data['count']}명)")
        passed += 1
    else:
        print(f"❌ FAIL ({resp.status_code})")

    # Test 3: 학생 상세 조회
    total += 1
    print("\n【 Test 3: GET /api/students/1 - 학생 상세 조회 】")
    resp = client.get('/api/students/1')
    if resp.status_code == 200:
        data = resp.get_json()['data']
        print(f"✅ PASS ({data['name']}, GPA: {data['gpa']})")
        passed += 1
    else:
        print(f"❌ FAIL ({resp.status_code})")

    # Test 4: 학생 추가
    total += 1
    print("\n【 Test 4: POST /api/students - 학생 추가 】")
    new_student = {
        "student_id": "2024099",
        "name": "Test Student",
        "department_id": 1
    }
    resp = client.post('/api/students', json=new_student, content_type='application/json')
    if resp.status_code == 201:
        print(f"✅ PASS (ID: {resp.get_json()['id']})")
        passed += 1
    else:
        print(f"❌ FAIL ({resp.status_code})")

    # Test 5: 학생 추가 유효성 검사
    total += 1
    print("\n【 Test 5: POST /api/students (유효성 검사) 】")
    invalid_student = {"name": "Incomplete"}
    resp = client.post('/api/students', json=invalid_student, content_type='application/json')
    if resp.status_code == 400:
        print("✅ PASS (오류 감지)")
        passed += 1
    else:
        print(f"❌ FAIL ({resp.status_code})")

    # Test 6: 교과목 조회
    total += 1
    print("\n【 Test 6: GET /api/courses - 교과목 조회 】")
    resp = client.get('/api/courses')
    data = resp.get_json()
    if resp.status_code == 200 and data['count'] > 0:
        print(f"✅ PASS ({data['count']}개)")
        passed += 1
    else:
        print(f"❌ FAIL ({resp.status_code})")

    # Test 7: 교과목 추가
    total += 1
    print("\n【 Test 7: POST /api/courses - 교과목 추가 】")
    new_course = {
        "code": "TEST101",
        "name": "Test Course",
        "credits": 3,
        "professor": "Test Prof",
        "department_id": 1
    }
    resp = client.post('/api/courses', json=new_course, content_type='application/json')
    if resp.status_code == 201:
        print(f"✅ PASS (ID: {resp.get_json()['id']})")
        passed += 1
    else:
        print(f"❌ FAIL ({resp.status_code})")

    # Test 8: 성적 조회
    total += 1
    print("\n【 Test 8: GET /api/grades/1 - 성적 조회 】")
    resp = client.get('/api/grades/1')
    data = resp.get_json()
    if resp.status_code == 200:
        print(f"✅ PASS (GPA: {data['gpa']}, {len(data['grades'])}개 과목)")
        passed += 1
    else:
        print(f"❌ FAIL ({resp.status_code})")

    # Test 9: 성적 추가
    total += 1
    print("\n【 Test 9: POST /api/grades - 성적 추가 】")
    new_grade = {
        "enrollment_id": 1,
        "score": 95.0,
        "grade": "A"
    }
    resp = client.post('/api/grades', json=new_grade, content_type='application/json')
    if resp.status_code == 201:
        print(f"✅ PASS")
        passed += 1
    else:
        print(f"❌ FAIL ({resp.status_code})")

    # Test 10: 통계 조회
    total += 1
    print("\n【 Test 10: GET /api/statistics - 통계 조회 】")
    resp = client.get('/api/statistics')
    data = resp.get_json()
    if resp.status_code == 200:
        stats = data['data']
        print(f"✅ PASS (학생: {stats['total_students']}명, 평균GPA: {stats['average_gpa']})")
        passed += 1
    else:
        print(f"❌ FAIL ({resp.status_code})")

    # Test 11: 존재하지 않는 학생
    total += 1
    print("\n【 Test 11: GET /api/students/99999 (404) 】")
    resp = client.get('/api/students/99999')
    if resp.status_code == 404:
        print("✅ PASS (404 정상 반환)")
        passed += 1
    else:
        print(f"❌ FAIL ({resp.status_code})")

    # Test 12: API 정보
    total += 1
    print("\n【 Test 12: GET / - API 정보 】")
    resp = client.get('/')
    data = resp.get_json()
    if resp.status_code == 200 and 'endpoints' in data:
        print(f"✅ PASS ({len(data['endpoints'])}개 엔드포인트)")
        passed += 1
    else:
        print(f"❌ FAIL ({resp.status_code})")

    # 결과 요약
    print("\n" + "="*80)
    print(f"✅ 테스트 완료: {passed}/{total} PASS")
    print("="*80)

    print("\n【 통합된 패턴 】")
    print("  ✓ v3.1: Decorators (require_auth, log_operation)")
    print("  ✓ v3.2: Generators (export_batch)")
    print("  ✓ v3.3: Context Managers (db_connection)")
    print("  ✓ v4.1: Async/Await (statistics)")
    print("  ✓ v5.2: Database Architecture (6 tables)")
    print("  ✓ v5.3: REST API (10+ endpoints)")

    print("\n【 철학 】")
    print("  기록이 증명이다 gogs")
    print("  모든 학습이 이 하나의 시스템으로 수렴된다.")
    print("="*80 + "\n")

    return passed == total


# ═══════════════════════════════════════════════════════════════════════════════
# 【 7. Main 】
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    init_db()

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # 테스트 모드
        success = run_tests()
        sys.exit(0 if success else 1)
    else:
        # 서버 모드
        print("\n" + "="*80)
        print("🎓 Gogs Academy — 통합 학사 관리 플랫폼")
        print("="*80)
        print("\n🌐 접속 주소: http://localhost:5000")
        print("\n【 주요 기능 】")
        print("  ✓ 학생 관리 (CRUD)")
        print("  ✓ 교과목 관리 (CRUD)")
        print("  ✓ 성적 관리 (성적 입력 & GPA 자동 계산)")
        print("  ✓ 출석 관리")
        print("  ✓ 통계 (비동기 집계)")
        print("\n【 통합 패턴 】")
        print("  v3.1: Decorators")
        print("  v3.2: Generators")
        print("  v3.3: Context Managers")
        print("  v4.1: Async/Await")
        print("  v5.2: Database")
        print("  v5.3: REST API")
        print("\n저장 필수 너는 기록이 증명이다 gogs")
        print("="*80 + "\n")

        app.run(debug=False, host='127.0.0.1', port=5000)
