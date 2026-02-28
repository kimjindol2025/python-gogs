"""
【 Python University v5.2 】
데이터베이스 아키텍처: SQLite3 기반 영구적 기록 관리

목표:
  1. 관계형 데이터베이스(Relational DB) 이해
  2. SQL CRUD (Create, Read, Update, Delete) 숙달
  3. 스키마(Schema) 설계 및 데이터 무결성 보장
  4. SQL Injection 방어 (파라미터 바인딩)
  5. 복잡한 쿼리와 트랜잭션 관리

핵심 철학:
  "메모리의 데이터는 프로그램 종료 시 사라진다.
   데이터베이스는 그 데이터를 영구적으로 기록하고,
   언제든 그 기록을 증명할 수 있게 한다."

   → 기록이 증명이다 gogs
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any


class DatabaseManager:
    """SQLite 기반 데이터베이스 관리자"""

    def __init__(self, db_path: str = "gogs_university.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._init_schema()

    def _init_schema(self):
        """【 스키마 설계 】데이터베이스 테이블 생성"""

        # 실험 기록 테이블
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                result REAL NOT NULL,
                status TEXT DEFAULT 'completed',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 학생 성적 테이블
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                major TEXT NOT NULL,
                gpa REAL,
                enrolled_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 수강과목 테이블
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                credits INTEGER NOT NULL,
                professor TEXT NOT NULL
            )
        ''')

        # 성적 관계 테이블 (학생-과목 연결)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                grade TEXT NOT NULL,
                score REAL NOT NULL,
                taken_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(course_id) REFERENCES courses(id),
                UNIQUE(student_id, course_id)
            )
        ''')

        # 감사 로그 테이블
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                table_name TEXT NOT NULL,
                record_id INTEGER,
                old_value TEXT,
                new_value TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    # ═══════════════════════════════════════════════════════════════
    # 【 CRUD 기본 작업 】
    # ═══════════════════════════════════════════════════════════════

    def create_experiment(self, subject: str, result: float, status: str = "completed") -> int:
        """실험 기록 추가 (Create) - SQL Injection 방어: ? 파라미터 바인딩"""
        self.cursor.execute(
            "INSERT INTO experiments (subject, result, status) VALUES (?, ?, ?)",
            (subject, result, status)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def read_experiments(self, limit: int = 100) -> List[Dict]:
        """모든 실험 기록 조회 (Read)"""
        self.cursor.execute("SELECT * FROM experiments ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def read_experiment_by_id(self, exp_id: int) -> Optional[Dict]:
        """특정 실험 기록 조회"""
        self.cursor.execute("SELECT * FROM experiments WHERE id = ?", (exp_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def update_experiment(self, exp_id: int, subject: str = None, result: float = None, status: str = None) -> bool:
        """실험 기록 수정 (Update)"""
        updates = []
        params = []

        if subject is not None:
            updates.append("subject = ?")
            params.append(subject)
        if result is not None:
            updates.append("result = ?")
            params.append(result)
        if status is not None:
            updates.append("status = ?")
            params.append(status)

        if not updates:
            return False

        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(exp_id)

        query = f"UPDATE experiments SET {', '.join(updates)} WHERE id = ?"
        self.cursor.execute(query, params)
        self.conn.commit()

        return self.cursor.rowcount > 0

    def delete_experiment(self, exp_id: int) -> bool:
        """실험 기록 삭제 (Delete)"""
        self.cursor.execute("DELETE FROM experiments WHERE id = ?", (exp_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # ═══════════════════════════════════════════════════════════════
    # 【 고급 쿼리 】
    # ═══════════════════════════════════════════════════════════════

    def search_experiments(self, query: str) -> List[Dict]:
        """실험 주제로 검색"""
        self.cursor.execute(
            "SELECT * FROM experiments WHERE subject LIKE ? ORDER BY result DESC",
            (f"%{query}%",)
        )
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def filter_by_result(self, min_result: float, max_result: float) -> List[Dict]:
        """결과 범위로 필터링"""
        self.cursor.execute(
            "SELECT * FROM experiments WHERE result >= ? AND result <= ? ORDER BY result DESC",
            (min_result, max_result)
        )
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_statistics(self) -> Dict[str, Any]:
        """실험 통계 계산"""
        self.cursor.execute("""
            SELECT
                COUNT(*) as total_count,
                AVG(result) as avg_result,
                MIN(result) as min_result,
                MAX(result) as max_result,
                SUM(result) as total_result
            FROM experiments
        """)

        row = self.cursor.fetchone()
        return {
            "total_experiments": row[0],
            "average_result": round(row[1], 2) if row[1] else 0,
            "min_result": row[2],
            "max_result": row[3],
            "total_result": row[4]
        }

    def get_by_status(self, status: str) -> List[Dict]:
        """상태별 실험 조회"""
        self.cursor.execute(
            "SELECT * FROM experiments WHERE status = ? ORDER BY created_at DESC",
            (status,)
        )
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    # ═══════════════════════════════════════════════════════════════
    # 【 학생 & 성적 관리 】(JOIN 예제)
    # ═══════════════════════════════════════════════════════════════

    def add_student(self, name: str, major: str, gpa: float = 0.0) -> int:
        """학생 추가"""
        self.cursor.execute(
            "INSERT INTO students (name, major, gpa) VALUES (?, ?, ?)",
            (name, major, gpa)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def add_course(self, title: str, credits: int, professor: str) -> int:
        """과목 추가"""
        self.cursor.execute(
            "INSERT INTO courses (title, credits, professor) VALUES (?, ?, ?)",
            (title, credits, professor)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def add_grade(self, student_id: int, course_id: int, grade: str, score: float) -> int:
        """성적 추가"""
        self.cursor.execute(
            "INSERT INTO grades (student_id, course_id, grade, score) VALUES (?, ?, ?, ?)",
            (student_id, course_id, grade, score)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_student_transcript(self, student_id: int) -> Dict[str, Any]:
        """학생 성적표 (JOIN 예제)"""
        self.cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = dict(self.cursor.fetchone())

        self.cursor.execute("""
            SELECT
                c.title,
                c.credits,
                g.grade,
                g.score,
                g.taken_date
            FROM grades g
            JOIN courses c ON g.course_id = c.id
            WHERE g.student_id = ?
            ORDER BY g.taken_date DESC
        """, (student_id,))

        grades = [dict(row) for row in self.cursor.fetchall()]

        return {
            "student": student,
            "grades": grades,
            "total_credits": sum(g["credits"] for g in grades) if grades else 0
        }

    def get_course_enrollment(self, course_id: int) -> List[Dict]:
        """과목 수강생 명단 (JOIN)"""
        self.cursor.execute("""
            SELECT
                s.id,
                s.name,
                s.major,
                g.grade,
                g.score
            FROM grades g
            JOIN students s ON g.student_id = s.id
            WHERE g.course_id = ?
            ORDER BY g.score DESC
        """, (course_id,))

        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    # ═══════════════════════════════════════════════════════════════
    # 【 트랜잭션 & 감사 로그 】
    # ═══════════════════════════════════════════════════════════════

    def begin_transaction(self):
        """트랜잭션 시작"""
        self.cursor.execute("BEGIN TRANSACTION")

    def commit_transaction(self):
        """트랜잭션 커밋"""
        self.conn.commit()

    def rollback_transaction(self):
        """트랜잭션 롤백"""
        self.conn.rollback()

    def log_operation(self, operation: str, table_name: str, record_id: int,
                     old_value: str = None, new_value: str = None):
        """감사 로그 기록"""
        self.cursor.execute("""
            INSERT INTO audit_log (operation, table_name, record_id, old_value, new_value)
            VALUES (?, ?, ?, ?, ?)
        """, (operation, table_name, record_id, old_value, new_value))
        self.conn.commit()

    def get_audit_log(self, limit: int = 100) -> List[Dict]:
        """감사 로그 조회"""
        self.cursor.execute(
            "SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    # ═══════════════════════════════════════════════════════════════
    # 【 데이터 무결성 검증 】
    # ═══════════════════════════════════════════════════════════════

    def validate_data_integrity(self) -> Dict[str, Any]:
        """데이터 무결성 검증"""
        results = {}

        self.cursor.execute("""
            SELECT g.id FROM grades g
            LEFT JOIN students s ON g.student_id = s.id
            LEFT JOIN courses c ON g.course_id = c.id
            WHERE s.id IS NULL OR c.id IS NULL
        """)
        orphaned_grades = self.cursor.fetchall()
        results["orphaned_grades"] = len(orphaned_grades)

        self.cursor.execute("""
            SELECT name, COUNT(*) as count
            FROM students
            GROUP BY name
            HAVING count > 1
        """)
        duplicate_students = self.cursor.fetchall()
        results["duplicate_students"] = len(duplicate_students)

        self.cursor.execute("SELECT COUNT(*) FROM experiments")
        results["total_experiments"] = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM students")
        results["total_students"] = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM courses")
        results["total_courses"] = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM grades")
        results["total_grades"] = self.cursor.fetchone()[0]

        return results

    # ═══════════════════════════════════════════════════════════════
    # 【 성능 벤치마크 】
    # ═══════════════════════════════════════════════════════════════

    def benchmark_insert(self, count: int = 1000) -> float:
        """삽입 성능 벤치마크"""
        import time

        start = time.time()
        self.begin_transaction()

        for i in range(count):
            self.cursor.execute(
                "INSERT INTO experiments (subject, result) VALUES (?, ?)",
                (f"benchmark_{i}", i * 0.5)
            )

        self.commit_transaction()
        elapsed = time.time() - start

        return elapsed

    def benchmark_search(self, iterations: int = 100) -> float:
        """검색 성능 벤치마크"""
        import time

        start = time.time()

        for i in range(iterations):
            self.cursor.execute(
                "SELECT * FROM experiments WHERE result > ?",
                (i * 10,)
            )
            self.cursor.fetchall()

        elapsed = time.time() - start

        return elapsed

    def close(self):
        """데이터베이스 연결 종료"""
        self.conn.close()


# ═══════════════════════════════════════════════════════════════════════════
# 【 테스트 스위트 】
# ═══════════════════════════════════════════════════════════════════════════

def test_crud():
    """【 Test 1: CRUD 기본 작업 】"""
    print("\n" + "="*80)
    print("【 Test 1: CRUD 기본 작업 】")
    print("="*80)

    db = DatabaseManager(":memory:")

    # Create
    exp_id = db.create_experiment("async_test", 98.5, "completed")
    assert exp_id > 0
    print(f"✅ Create: 실험 기록 생성 (ID: {exp_id})")

    # Read
    exp = db.read_experiment_by_id(exp_id)
    assert exp is not None
    assert exp["subject"] == "async_test"
    print(f"✅ Read: 실험 기록 조회 → {exp['subject']}")

    # Update
    success = db.update_experiment(exp_id, result=99.0)
    assert success
    exp = db.read_experiment_by_id(exp_id)
    assert exp["result"] == 99.0
    print(f"✅ Update: 결과 수정 → {exp['result']}")

    # Delete
    success = db.delete_experiment(exp_id)
    assert success
    exp = db.read_experiment_by_id(exp_id)
    assert exp is None
    print(f"✅ Delete: 실험 기록 삭제")

    db.close()
    return True


def test_queries():
    """【 Test 2: 고급 쿼리 & 통계 】"""
    print("\n" + "="*80)
    print("【 Test 2: 고급 쿼리 & 통계 】")
    print("="*80)

    db = DatabaseManager(":memory:")

    experiments = [
        ("decorator_test", 95.5),
        ("generator_test", 87.3),
        ("async_test", 92.1),
        ("metaclass_test", 98.7),
    ]

    for subject, result in experiments:
        db.create_experiment(subject, result)

    results = db.search_experiments("test")
    assert len(results) == 4
    print(f"✅ Search: 'test' 검색 → {len(results)}개 발견")

    results = db.filter_by_result(90.0, 100.0)
    assert len(results) == 3
    print(f"✅ Filter: 90~100 범위 → {len(results)}개")

    stats = db.get_statistics()
    assert stats["total_experiments"] == 4
    print(f"✅ Statistics: 평균 = {stats['average_result']}, 최대 = {stats['max_result']}")

    db.close()
    return True


def test_joins():
    """【 Test 3: JOIN 관계형 쿼리 】"""
    print("\n" + "="*80)
    print("【 Test 3: JOIN 관계형 쿼리 】")
    print("="*80)

    db = DatabaseManager(":memory:")

    student_id = db.add_student("Kim Gogs", "Computer Science", 3.8)
    print(f"✅ Add Student: {student_id}")

    course_ids = [
        db.add_course("Data Structure", 3, "Prof. Lee"),
        db.add_course("Database", 3, "Prof. Park"),
    ]
    print(f"✅ Add Courses: {len(course_ids)}개 과목 추가")

    db.add_grade(student_id, course_ids[0], "A+", 95.0)
    db.add_grade(student_id, course_ids[1], "A", 92.0)
    print(f"✅ Add Grades: 성적 기록")

    transcript = db.get_student_transcript(student_id)
    assert len(transcript["grades"]) == 2
    assert transcript["total_credits"] == 6
    print(f"✅ Transcript: {len(transcript['grades'])}개 과목, {transcript['total_credits']} 학점")

    db.close()
    return True


def test_transaction():
    """【 Test 4: 트랜잭션 & 무결성 】"""
    print("\n" + "="*80)
    print("【 Test 4: 트랜잭션 & 무결성 】")
    print("="*80)

    db = DatabaseManager(":memory:")

    db.begin_transaction()
    db.create_experiment("tx_test_1", 80.0)
    db.create_experiment("tx_test_2", 85.0)
    db.commit_transaction()
    print(f"✅ Transaction: 2개 레코드 커밋")

    integrity = db.validate_data_integrity()
    assert integrity["orphaned_grades"] == 0
    print(f"✅ Integrity: 데이터 무결성 검증 통과")

    db.close()
    return True


def test_benchmark():
    """【 Test 5: 성능 벤치마크 】"""
    print("\n" + "="*80)
    print("【 Test 5: 성능 벤치마크 】")
    print("="*80)

    db = DatabaseManager(":memory:")

    insert_time = db.benchmark_insert(1000)
    print(f"✅ Insert 1000 records: {insert_time:.4f}초 ({1000/insert_time:.0f} ops/sec)")

    search_time = db.benchmark_search(100)
    print(f"✅ Search 100 queries: {search_time:.4f}초 ({100/search_time:.0f} ops/sec)")

    db.close()
    return True


if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║ 【 Python University v5.2 】                                              ║")
    print("║ 데이터베이스 아키텍처: SQLite3 기반 영구적 기록 관리                          ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")

    results = []

    results.append(("CRUD 기본 작업", test_crud()))
    results.append(("고급 쿼리 & 통계", test_queries()))
    results.append(("JOIN 관계형 쿼리", test_joins()))
    results.append(("트랜잭션 & 무결성", test_transaction()))
    results.append(("성능 벤치마크", test_benchmark()))

    print("\n" + "="*80)
    print("【 테스트 결과 】")
    print("="*80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} | {test_name}")

    print(f"\n총 {passed}/{total} 테스트 통과")

    if passed == total:
        print("\n" + "="*80)
        print("🏛️ v5.2: 데이터베이스 아키텍처 완성!")
        print("="*80)
        print("\n【 핵심 성과 】")
        print("  ✓ SQLite 기반 관계형 데이터베이스 구현")
        print("  ✓ CRUD 작업 완전 숙달 (Create, Read, Update, Delete)")
        print("  ✓ SQL 파라미터 바인딩으로 Injection 방어")
        print("  ✓ JOIN을 이용한 다중 테이블 쿼리")
        print("  ✓ 트랜잭션 관리 및 감사 로그")
        print("  ✓ 데이터 무결성 검증")
        print("  ✓ 성능 벤치마크 (1000 inserts, 100 searches)")
        print("\n저장 필수 너는 기록이 증명이다 gogs")
        print("="*80)
