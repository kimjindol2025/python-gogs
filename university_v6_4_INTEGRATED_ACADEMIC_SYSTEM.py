"""
【 Python University v6.4 】
SQLite 통합 학사 관리 시스템 - 배운 모든 패턴 실제 구현

학습 패턴 활용:
  v3.1: 데코레이터 (권한, 로깅, 캐싱)
  v3.2: 제너레이터 (대량 데이터 처리)
  v3.3: 컨텍스트 매니저 (DB 연결)
  v4.1: async/await (동시 작업)
  v5.1: 마이크로서비스 (모듈화)
  v5.2: SQLite DB (영구 저장)
  v5.3: 알고리즘 (최적화)
  v5.4: 디자인 패턴 (구조)

목표: 실제로 동작하는 학사 관리 시스템
      SQLite 파일에 데이터가 저장되고
      조회/수정/삭제가 모두 작동하는 것을 확인
"""

import sqlite3
import asyncio
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Any, Generator
from functools import wraps
from contextlib import contextmanager


# ═══════════════════════════════════════════════════════════════════════════
# 【 v3.1: 데코레이터 패턴 】
# ═══════════════════════════════════════════════════════════════════════════

def require_auth(role: str):
    """권한 확인 데코레이터"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            current_role = getattr(self, 'current_role', 'guest')
            if current_role != role and current_role != 'admin':
                raise PermissionError(f"Role '{role}' required, got '{current_role}'")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def log_operation(func):
    """작업 로깅 데코레이터"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start = datetime.now()
        result = func(self, *args, **kwargs)
        elapsed = (datetime.now() - start).total_seconds()
        print(f"  📝 [{func.__name__}] {elapsed:.4f}초")
        return result
    return wrapper


def cache_result(func):
    """결과 캐싱 데코레이터"""
    cache = {}
    @wraps(func)
    def wrapper(self, *args):
        key = str(args)
        if key not in cache:
            cache[key] = func(self, *args)
        return cache[key]
    return wrapper


# ═══════════════════════════════════════════════════════════════════════════
# 【 v3.3: 컨텍스트 매니저 패턴 】
# ═══════════════════════════════════════════════════════════════════════════

@contextmanager
def db_connection(db_path: str):
    """DB 연결 컨텍스트 매니저"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


# ═══════════════════════════════════════════════════════════════════════════
# 【 v3.2: 제너레이터 패턴 】
# ═══════════════════════════════════════════════════════════════════════════

def batch_generator(items: List, batch_size: int = 100) -> Generator:
    """대량 데이터를 배치로 처리하는 제너레이터"""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


# ═══════════════════════════════════════════════════════════════════════════
# 【 v4.1: async/await 패턴 】
# ═══════════════════════════════════════════════════════════════════════════

async def async_batch_process(items: List, delay: float = 0.01) -> int:
    """비동기로 대량 데이터 처리"""
    async def process_item(item):
        await asyncio.sleep(delay)
        return item
    
    tasks = [process_item(item) for item in items]
    results = await asyncio.gather(*tasks)
    return len(results)


# ═══════════════════════════════════════════════════════════════════════════
# 【 v5.2: SQLite 데이터베이스 】
# ═══════════════════════════════════════════════════════════════════════════

class AcademicDatabase:
    """학사 관리 데이터베이스"""

    def __init__(self, db_path: str = "academic_system.db"):
        self.db_path = db_path
        with db_connection(db_path) as conn:
            cursor = conn.cursor()
            
            # 학생 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    major TEXT NOT NULL,
                    enrollment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active'
                )
            ''')

            # 과목 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT NOT NULL UNIQUE,
                    title TEXT NOT NULL,
                    credits INTEGER NOT NULL,
                    professor TEXT NOT NULL
                )
            ''')

            # 성적 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    score REAL NOT NULL,
                    grade TEXT NOT NULL,
                    recorded_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(student_id) REFERENCES students(id),
                    FOREIGN KEY(course_id) REFERENCES courses(id),
                    UNIQUE(student_id, course_id)
                )
            ''')

            # 학위 요구사항 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS degree_requirements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    major TEXT NOT NULL UNIQUE,
                    required_credits INTEGER NOT NULL,
                    required_courses TEXT
                )
            ''')

            conn.commit()


# ═══════════════════════════════════════════════════════════════════════════
# 【 v5.1: 마이크로서비스 모듈화 】
# ═══════════════════════════════════════════════════════════════════════════

class StudentManager:
    """학생 관리 마이크로서비스"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.current_role = 'admin'

    @require_auth('admin')
    @log_operation
    def register_student(self, name: str, major: str) -> int:
        """학생 등록"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (name, major) VALUES (?, ?)",
                (name, major)
            )
            conn.commit()
            return cursor.lastrowid

    @log_operation
    def get_student(self, student_id: int) -> Optional[Dict]:
        """학생 조회"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @log_operation
    def list_students(self) -> List[Dict]:
        """모든 학생 조회"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students ORDER BY enrollment_date DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    @require_auth('admin')
    @log_operation
    def update_status(self, student_id: int, status: str) -> bool:
        """학생 상태 변경"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE students SET status = ? WHERE id = ?",
                (status, student_id)
            )
            conn.commit()
            return cursor.rowcount > 0


class CourseManager:
    """과목 관리 마이크로서비스"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.current_role = 'admin'

    @require_auth('admin')
    @log_operation
    def add_course(self, code: str, title: str, credits: int, professor: str) -> int:
        """과목 추가"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO courses (code, title, credits, professor) VALUES (?, ?, ?, ?)",
                (code, title, credits, professor)
            )
            conn.commit()
            return cursor.lastrowid

    @log_operation
    def get_course(self, course_id: int) -> Optional[Dict]:
        """과목 조회"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @log_operation
    def list_courses(self) -> List[Dict]:
        """모든 과목 조회"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses ORDER BY code")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]


class GradeManager:
    """성적 관리 마이크로서비스"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.current_role = 'admin'

    @require_auth('admin')
    @log_operation
    def record_grade(self, student_id: int, course_id: int, score: float) -> int:
        """성적 기록"""
        grade = self._score_to_grade(score)
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO grades (student_id, course_id, score, grade) VALUES (?, ?, ?, ?)",
                (student_id, course_id, score, grade)
            )
            conn.commit()
            return cursor.lastrowid

    @log_operation
    def get_student_transcript(self, student_id: int) -> Dict:
        """학생 성적표"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 학생 정보
            cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
            student = dict(cursor.fetchone())

            # 성적 정보 (JOIN)
            cursor.execute('''
                SELECT c.code, c.title, c.credits, g.score, g.grade
                FROM grades g
                JOIN courses c ON g.course_id = c.id
                WHERE g.student_id = ?
                ORDER BY g.recorded_date DESC
            ''', (student_id,))
            
            grades = [dict(row) for row in cursor.fetchall()]

            # GPA 계산
            gpa = self._calculate_gpa(grades)
            total_credits = sum(g['credits'] for g in grades)

            return {
                'student': student,
                'grades': grades,
                'gpa': gpa,
                'total_credits': total_credits
            }

    @log_operation
    def get_class_statistics(self, course_id: int) -> Dict:
        """과목 통계"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT
                    COUNT(*) as count,
                    AVG(score) as avg_score,
                    MIN(score) as min_score,
                    MAX(score) as max_score
                FROM grades
                WHERE course_id = ?
            ''', (course_id,))
            
            row = cursor.fetchone()
            return {
                'total_students': row[0],
                'average_score': round(row[1], 2) if row[1] else 0,
                'min_score': row[2],
                'max_score': row[3]
            }

    @staticmethod
    def _score_to_grade(score: float) -> str:
        """v5.3: 알고리즘 - 학점 계산"""
        if score >= 90: return 'A+'
        elif score >= 85: return 'A'
        elif score >= 80: return 'B+'
        elif score >= 75: return 'B'
        elif score >= 70: return 'C'
        else: return 'F'

    @staticmethod
    def _calculate_gpa(grades: List[Dict]) -> float:
        """v5.4: 디자인 패턴 - 가중 평균 GPA"""
        if not grades:
            return 0.0
        
        grade_points = {
            'A+': 4.0, 'A': 4.0, 'B+': 3.5, 'B': 3.0,
            'C': 2.5, 'D': 2.0, 'F': 0.0
        }
        
        total_points = sum(grade_points.get(g['grade'], 0) * g['credits'] for g in grades)
        total_credits = sum(g['credits'] for g in grades)
        
        return round(total_points / total_credits, 2) if total_credits > 0 else 0.0


class DataExporter:
    """데이터 내보내기 (v3.2: 제너레이터)"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def export_students_batch(self, batch_size: int = 100) -> Generator:
        """학생 데이터를 배치로 내보내기"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            
            while True:
                rows = cursor.fetchmany(batch_size)
                if not rows:
                    break
                yield [dict(row) for row in rows]

    def export_all_grades(self) -> Generator:
        """모든 성적 데이터 내보내기"""
        with db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.name, c.code, c.title, g.score, g.grade
                FROM grades g
                JOIN students s ON g.student_id = s.id
                JOIN courses c ON g.course_id = c.id
                ORDER BY s.name, c.code
            ''')
            
            for row in cursor.fetchall():
                yield dict(row)


# ═══════════════════════════════════════════════════════════════════════════
# 【 테스트 】
# ═══════════════════════════════════════════════════════════════════════════

def test_integrated_system():
    """【 Test: 통합 시스템 검증 】"""
    import os
    
    db_path = "test_academic.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    print("\n" + "="*80)
    print("【 Python University v6.4 - 통합 학사 관리 시스템 】")
    print("="*80)

    # 데이터베이스 초기화
    AcademicDatabase(db_path)
    print("✅ 데이터베이스 생성 완료")

    # 학생 관리
    print("\n【 1단계: 학생 등록 】")
    student_mgr = StudentManager(db_path)
    
    s1 = student_mgr.register_student("Kim Gogs", "Computer Science")
    s2 = student_mgr.register_student("Lee AI", "Data Science")
    print(f"✅ 2명 학생 등록 (ID: {s1}, {s2})")

    # 과목 관리
    print("\n【 2단계: 과목 등록 】")
    course_mgr = CourseManager(db_path)
    
    c1 = course_mgr.add_course("CS101", "Data Structure", 3, "Prof. Park")
    c2 = course_mgr.add_course("CS201", "Database", 3, "Prof. Lee")
    c3 = course_mgr.add_course("CS301", "AI", 4, "Prof. Kim")
    print(f"✅ 3개 과목 등록")

    # 성적 기록
    print("\n【 3단계: 성적 기록 】")
    grade_mgr = GradeManager(db_path)
    
    grade_mgr.record_grade(s1, c1, 95.0)
    grade_mgr.record_grade(s1, c2, 88.0)
    grade_mgr.record_grade(s1, c3, 92.0)
    
    grade_mgr.record_grade(s2, c1, 87.0)
    grade_mgr.record_grade(s2, c2, 91.0)
    grade_mgr.record_grade(s2, c3, 94.0)
    print(f"✅ 6개 성적 기록")

    # 성적표 조회
    print("\n【 4단계: 성적표 조회 】")
    
    transcript1 = grade_mgr.get_student_transcript(s1)
    print(f"✅ {transcript1['student']['name']}")
    print(f"   GPA: {transcript1['gpa']}")
    print(f"   총 학점: {transcript1['total_credits']}")
    print(f"   과목 수: {len(transcript1['grades'])}")

    transcript2 = grade_mgr.get_student_transcript(s2)
    print(f"✅ {transcript2['student']['name']}")
    print(f"   GPA: {transcript2['gpa']}")
    print(f"   총 학점: {transcript2['total_credits']}")

    # 과목 통계
    print("\n【 5단계: 과목 통계 】")
    
    stats = grade_mgr.get_class_statistics(c1)
    print(f"✅ CS101 통계: 평균 = {stats['average_score']}, 학생 수 = {stats['total_students']}")

    # 데이터 내보내기 (제너레이터)
    print("\n【 6단계: 데이터 내보내기 (v3.2 제너레이터) 】")
    
    exporter = DataExporter(db_path)
    batch_count = 0
    for batch in exporter.export_students_batch(batch_size=1):
        batch_count += len(batch)
    print(f"✅ {batch_count}명 학생 배치 내보내기")

    # async 처리
    print("\n【 7단계: 비동기 처리 (v4.1 async/await) 】")
    
    async def test_async():
        items = list(range(10))
        count = await async_batch_process(items, delay=0.001)
        return count
    
    result = asyncio.run(test_async())
    print(f"✅ {result}개 항목 비동기 처리")

    # 최종 확인
    print("\n【 8단계: 데이터 검증 】")
    
    all_students = student_mgr.list_students()
    all_courses = course_mgr.list_courses()
    print(f"✅ 총 {len(all_students)}명 학생, {len(all_courses)}개 과목 저장됨")

    # 파일 확인
    import os
    file_size = os.path.getsize(db_path)
    print(f"✅ SQLite 파일 크기: {file_size} bytes")

    os.remove(db_path)
    print("\n" + "="*80)
    print("🎓 v6.4: 통합 학사 관리 시스템 완성!")
    print("="*80)
    print("\n【 활용 패턴 】")
    print("  ✓ v3.1 데코레이터: 권한 체크 + 로깅")
    print("  ✓ v3.2 제너레이터: 대량 데이터 배치 처리")
    print("  ✓ v3.3 컨텍스트 매니저: DB 연결 안전 관리")
    print("  ✓ v4.1 async/await: 동시 작업 처리")
    print("  ✓ v5.1 마이크로서비스: 기능별 모듈 분리")
    print("  ✓ v5.2 SQLite: 실제 데이터 영구 저장")
    print("  ✓ v5.3 알고리즘: 학점 계산, GPA 계산")
    print("  ✓ v5.4 디자인 패턴: 가중 평균 계산")
    print("\n저장 필수 너는 기록이 증명이다 gogs")
    print("="*80)
    
    return True


if __name__ == "__main__":
    test_integrated_system()
