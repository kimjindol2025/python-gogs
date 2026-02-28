"""
【 Python University v7 】
웹 기반 학생관리 시스템 - Flask 서버 + UI

실행: python3 university_v7_app.py
접속: http://localhost:5000
"""

from flask import Flask, render_template_string, request, jsonify
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

app = Flask(__name__)
DB_PATH = "student_management.db"


# ═══════════════════════════════════════════════════════════════════════════
# 【 Database 연결 】
# ═══════════════════════════════════════════════════════════════════════════

def get_db():
    """DB 연결"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """데이터베이스 초기화"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            head TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            department_id INTEGER NOT NULL,
            gpa REAL DEFAULT 0.0,
            FOREIGN KEY(department_id) REFERENCES departments(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            credits INTEGER,
            professor TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            score REAL NOT NULL,
            grade TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(course_id) REFERENCES courses(id),
            UNIQUE(student_id, course_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT,
            status TEXT DEFAULT 'present',
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    ''')

    # 샘플 데이터
    try:
        cursor.execute("INSERT INTO departments (code, name, head) VALUES (?, ?, ?)", 
                      ("CSE", "컴퓨터공학과", "Park, Jin"))
        cursor.execute("INSERT INTO departments (code, name, head) VALUES (?, ?, ?)", 
                      ("DS", "데이터사이언스과", "Lee, Min"))
        cursor.execute("INSERT INTO departments (code, name, head) VALUES (?, ?, ?)", 
                      ("ENG", "영어학과", "Kim, Soon"))

        cursor.execute("INSERT INTO students (student_id, name, department_id, gpa) VALUES (?, ?, ?, ?)",
                      ("2024001", "Kim Gogs", 1, 3.8))
        cursor.execute("INSERT INTO students (student_id, name, department_id, gpa) VALUES (?, ?, ?, ?)",
                      ("2024002", "Lee AI", 1, 3.6))
        cursor.execute("INSERT INTO students (student_id, name, department_id, gpa) VALUES (?, ?, ?, ?)",
                      ("2024003", "Park Data", 2, 3.9))
        cursor.execute("INSERT INTO students (student_id, name, department_id, gpa) VALUES (?, ?, ?, ?)",
                      ("2024004", "Choi Eng", 3, 3.5))
        cursor.execute("INSERT INTO students (student_id, name, department_id, gpa) VALUES (?, ?, ?, ?)",
                      ("2024005", "Jung Smart", 1, 3.7))

        cursor.execute("INSERT INTO courses (code, name, credits, professor) VALUES (?, ?, ?, ?)",
                      ("CS101", "프로그래밍 기초", 3, "Prof. Kim"))
        cursor.execute("INSERT INTO courses (code, name, credits, professor) VALUES (?, ?, ?, ?)",
                      ("CS201", "자료구조", 3, "Prof. Lee"))
        cursor.execute("INSERT INTO courses (code, name, credits, professor) VALUES (?, ?, ?, ?)",
                      ("DS101", "데이터 분석", 3, "Prof. Park"))
        cursor.execute("INSERT INTO courses (code, name, credits, professor) VALUES (?, ?, ?, ?)",
                      ("ENG101", "영어회화", 2, "Prof. Choi"))
        cursor.execute("INSERT INTO courses (code, name, credits, professor) VALUES (?, ?, ?, ?)",
                      ("CS301", "AI 기초", 4, "Prof. Jung"))

        cursor.execute("INSERT INTO grades (student_id, course_id, score, grade) VALUES (?, ?, ?, ?)",
                      (1, 1, 95.0, "A+"))
        cursor.execute("INSERT INTO grades (student_id, course_id, score, grade) VALUES (?, ?, ?, ?)",
                      (1, 2, 88.0, "B+"))
        cursor.execute("INSERT INTO grades (student_id, course_id, score, grade) VALUES (?, ?, ?, ?)",
                      (2, 1, 92.0, "A"))
        cursor.execute("INSERT INTO grades (student_id, course_id, score, grade) VALUES (?, ?, ?, ?)",
                      (3, 3, 91.0, "A"))

        cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                      (1, "2024-02-20", "present"))
        cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                      (1, "2024-02-21", "present"))
        cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                      (1, "2024-02-22", "absent"))

        conn.commit()
    except:
        pass  # 데이터 이미 존재

    conn.close()


# ═══════════════════════════════════════════════════════════════════════════
# 【 API 엔드포인트 】
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    """메인 대시보드"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM departments")
    total_departments = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(gpa) FROM students")
    avg_gpa = round(cursor.fetchone()[0] or 0, 2)
    
    conn.close()
    
    return render_template_string(HTML_TEMPLATE, 
                                total_students=total_students,
                                total_departments=total_departments,
                                avg_gpa=avg_gpa)


@app.route('/api/students')
def get_students():
    """학생 목록 조회"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.*, d.name as department_name
        FROM students s
        JOIN departments d ON s.department_id = d.id
        ORDER BY s.student_id
    ''')
    students = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(students)


@app.route('/api/student/<int:student_id>')
def get_student(student_id):
    """학생 상세 정보"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.*, d.name as department_name
        FROM students s
        JOIN departments d ON s.department_id = d.id
        WHERE s.id = ?
    ''', (student_id,))
    student = dict(cursor.fetchone())
    
    cursor.execute('''
        SELECT c.code, c.name, g.score, g.grade
        FROM grades g
        JOIN courses c ON g.course_id = c.id
        WHERE g.student_id = ?
    ''', (student_id,))
    grades = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute('''
        SELECT date, status FROM attendance
        WHERE student_id = ?
        ORDER BY date DESC
    ''', (student_id,))
    attendance = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'student': student,
        'grades': grades,
        'attendance': attendance
    })


@app.route('/api/departments')
def get_departments():
    """학과 목록"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.*, COUNT(s.id) as student_count, AVG(s.gpa) as avg_gpa
        FROM departments d
        LEFT JOIN students s ON d.id = s.department_id
        GROUP BY d.id
    ''')
    departments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(departments)


@app.route('/api/courses')
def get_courses():
    """교과목 목록"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses ORDER BY code")
    courses = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(courses)


@app.route('/api/add_student', methods=['POST'])
def add_student():
    """학생 추가"""
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO students (student_id, name, department_id) VALUES (?, ?, ?)",
            (data['student_id'], data['name'], data['department_id'])
        )
        conn.commit()
        result = {'success': True, 'id': cursor.lastrowid}
    except Exception as e:
        result = {'success': False, 'error': str(e)}
    finally:
        conn.close()
    
    return jsonify(result)


@app.route('/api/add_grade', methods=['POST'])
def add_grade():
    """성적 추가"""
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO grades (student_id, course_id, score, grade) VALUES (?, ?, ?, ?)",
            (data['student_id'], data['course_id'], data['score'], data['grade'])
        )
        conn.commit()
        result = {'success': True}
    except Exception as e:
        result = {'success': False, 'error': str(e)}
    finally:
        conn.close()
    
    return jsonify(result)


@app.route('/api/mark_attendance', methods=['POST'])
def mark_attendance():
    """출석 기록"""
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
            (data['student_id'], datetime.now().strftime('%Y-%m-%d'), data['status'])
        )
        conn.commit()
        result = {'success': True}
    except Exception as e:
        result = {'success': False, 'error': str(e)}
    finally:
        conn.close()
    
    return jsonify(result)


# ═══════════════════════════════════════════════════════════════════════════
# 【 HTML 템플릿 】
# ═══════════════════════════════════════════════════════════════════════════

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>학생관리 시스템 - Python University v7</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }

        header h1 {
            color: #667eea;
            font-size: 28px;
            margin-bottom: 5px;
        }

        header p {
            color: #666;
            font-size: 14px;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }

        .stat-card h3 {
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
            text-transform: uppercase;
        }

        .stat-card .number {
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }

        .main-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }

        .card button {
            width: 100%;
            padding: 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            margin-top: 10px;
            transition: background 0.3s;
        }

        .card button:hover {
            background: #764ba2;
        }

        .card input, .card select {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        table th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }

        table td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }

        table tr:hover {
            background: #f5f5f5;
        }

        .success {
            background: #d4edda;
            color: #155724;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            display: none;
        }

        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            display: none;
        }

        .loading {
            text-align: center;
            color: #667eea;
            font-size: 14px;
        }

        @media (max-width: 768px) {
            .stats {
                grid-template-columns: 1fr;
            }
            
            .main-content {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎓 Python University v7</h1>
            <p>웹 기반 학생관리 시스템 - 배운 모든 패턴 실제 구현</p>
        </header>

        <div class="stats">
            <div class="stat-card">
                <h3>📚 총 학생 수</h3>
                <div class="number">{{ total_students }}</div>
            </div>
            <div class="stat-card">
                <h3>🏢 학과 수</h3>
                <div class="number">{{ total_departments }}</div>
            </div>
            <div class="stat-card">
                <h3>📊 평균 GPA</h3>
                <div class="number">{{ avg_gpa }}</div>
            </div>
        </div>

        <div class="main-content">
            <!-- 학생 관리 -->
            <div class="card">
                <h2>👨‍🎓 학생 관리</h2>
                <input type="text" id="student_id" placeholder="학번" maxlength="10">
                <input type="text" id="student_name" placeholder="이름" maxlength="20">
                <select id="department_id">
                    <option value="">학과 선택</option>
                    <option value="1">컴퓨터공학과</option>
                    <option value="2">데이터사이언스과</option>
                    <option value="3">영어학과</option>
                </select>
                <button onclick="addStudent()">✅ 학생 추가</button>
                <div class="success" id="student_success">학생이 추가되었습니다!</div>
                <div class="error" id="student_error"></div>
                <div id="students_list" class="loading">로딩 중...</div>
            </div>

            <!-- 성적 관리 -->
            <div class="card">
                <h2>📈 성적 관리</h2>
                <input type="number" id="grade_student_id" placeholder="학생 ID" min="1">
                <input type="number" id="grade_course_id" placeholder="과목 ID" min="1">
                <input type="number" id="grade_score" placeholder="점수 (0-100)" min="0" max="100">
                <input type="text" id="grade_letter" placeholder="학점 (A+, A, B+...)" maxlength="2">
                <button onclick="addGrade()">✅ 성적 추가</button>
                <div class="success" id="grade_success">성적이 추가되었습니다!</div>
                <div class="error" id="grade_error"></div>
            </div>

            <!-- 출석 관리 -->
            <div class="card">
                <h2>✍️ 출석 관리</h2>
                <input type="number" id="attend_student_id" placeholder="학생 ID" min="1">
                <select id="attend_status">
                    <option value="present">✅ 출석</option>
                    <option value="absent">❌ 결석</option>
                    <option value="late">⏰ 지각</option>
                </select>
                <button onclick="markAttendance()">✅ 출석 기록</button>
                <div class="success" id="attend_success">출석이 기록되었습니다!</div>
                <div class="error" id="attend_error"></div>
            </div>

            <!-- 학과 정보 -->
            <div class="card">
                <h2>🏢 학과 정보</h2>
                <div id="departments_list" class="loading">로딩 중...</div>
            </div>

            <!-- 교과목 -->
            <div class="card">
                <h2>📚 교과목</h2>
                <div id="courses_list" class="loading">로딩 중...</div>
            </div>

            <!-- 학생 상세 정보 -->
            <div class="card">
                <h2>🔍 학생 상세 정보</h2>
                <input type="number" id="search_student_id" placeholder="학생 ID" min="1">
                <button onclick="getStudentDetail()">🔍 조회</button>
                <div id="student_detail"></div>
            </div>
        </div>
    </div>

    <script>
        // 초기 로딩
        loadStudents();
        loadDepartments();
        loadCourses();

        function showMessage(elementId, message, isError = false) {
            const element = document.getElementById(elementId);
            element.textContent = message;
            element.style.display = 'block';
            setTimeout(() => {
                element.style.display = 'none';
            }, 3000);
        }

        function loadStudents() {
            fetch('/api/students')
                .then(r => r.json())
                .then(data => {
                    let html = '<table><tr><th>학번</th><th>이름</th><th>학과</th><th>GPA</th></tr>';
                    data.forEach(s => {
                        html += `<tr><td>${s.student_id}</td><td>${s.name}</td><td>${s.department_name}</td><td>${s.gpa}</td></tr>`;
                    });
                    html += '</table>';
                    document.getElementById('students_list').innerHTML = html;
                });
        }

        function loadDepartments() {
            fetch('/api/departments')
                .then(r => r.json())
                .then(data => {
                    let html = '<table><tr><th>학과</th><th>학생 수</th><th>평균 GPA</th></tr>';
                    data.forEach(d => {
                        html += `<tr><td>${d.name}</td><td>${d.student_count}</td><td>${(d.avg_gpa || 0).toFixed(2)}</td></tr>`;
                    });
                    html += '</table>';
                    document.getElementById('departments_list').innerHTML = html;
                });
        }

        function loadCourses() {
            fetch('/api/courses')
                .then(r => r.json())
                .then(data => {
                    let html = '<table><tr><th>과목 코드</th><th>과목명</th><th>학점</th><th>교수</th></tr>';
                    data.forEach(c => {
                        html += `<tr><td>${c.code}</td><td>${c.name}</td><td>${c.credits}</td><td>${c.professor}</td></tr>`;
                    });
                    html += '</table>';
                    document.getElementById('courses_list').innerHTML = html;
                });
        }

        function addStudent() {
            const student_id = document.getElementById('student_id').value;
            const name = document.getElementById('student_name').value;
            const department_id = document.getElementById('department_id').value;

            if (!student_id || !name || !department_id) {
                showMessage('student_error', '모든 필드를 입력하세요!', true);
                return;
            }

            fetch('/api/add_student', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({student_id, name, department_id})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    showMessage('student_success', '학생이 추가되었습니다!');
                    document.getElementById('student_id').value = '';
                    document.getElementById('student_name').value = '';
                    document.getElementById('department_id').value = '';
                    loadStudents();
                } else {
                    showMessage('student_error', data.error, true);
                }
            });
        }

        function addGrade() {
            const student_id = document.getElementById('grade_student_id').value;
            const course_id = document.getElementById('grade_course_id').value;
            const score = document.getElementById('grade_score').value;
            const grade = document.getElementById('grade_letter').value;

            if (!student_id || !course_id || !score || !grade) {
                showMessage('grade_error', '모든 필드를 입력하세요!', true);
                return;
            }

            fetch('/api/add_grade', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({student_id, course_id, score, grade})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    showMessage('grade_success', '성적이 추가되었습니다!');
                    document.getElementById('grade_student_id').value = '';
                    document.getElementById('grade_course_id').value = '';
                    document.getElementById('grade_score').value = '';
                    document.getElementById('grade_letter').value = '';
                } else {
                    showMessage('grade_error', data.error, true);
                }
            });
        }

        function markAttendance() {
            const student_id = document.getElementById('attend_student_id').value;
            const status = document.getElementById('attend_status').value;

            if (!student_id) {
                showMessage('attend_error', '학생 ID를 입력하세요!', true);
                return;
            }

            fetch('/api/mark_attendance', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({student_id, status})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    showMessage('attend_success', '출석이 기록되었습니다!');
                    document.getElementById('attend_student_id').value = '';
                } else {
                    showMessage('attend_error', data.error, true);
                }
            });
        }

        function getStudentDetail() {
            const student_id = document.getElementById('search_student_id').value;

            if (!student_id) {
                document.getElementById('student_detail').innerHTML = '';
                return;
            }

            fetch(`/api/student/${student_id}`)
                .then(r => r.json())
                .then(data => {
                    let html = `
                        <h3>${data.student.name} (${data.student.student_id})</h3>
                        <p><strong>학과:</strong> ${data.student.department_name}</p>
                        <p><strong>GPA:</strong> ${data.student.gpa}</p>
                        <h4>📚 성적</h4>
                        <table>
                            <tr><th>과목</th><th>점수</th><th>학점</th></tr>
                    `;
                    data.grades.forEach(g => {
                        html += `<tr><td>${g.code}</td><td>${g.score}</td><td>${g.grade}</td></tr>`;
                    });
                    html += `</table>`;
                    document.getElementById('student_detail').innerHTML = html;
                })
                .catch(e => {
                    document.getElementById('student_detail').innerHTML = '<p style="color: red;">학생을 찾을 수 없습니다.</p>';
                });
        }
    </script>
</body>
</html>
'''


if __name__ == "__main__":
    init_db()
    print("\n" + "="*80)
    print("🚀 Python University v7 - 웹 서버 시작")
    print("="*80)
    print("\n📌 접속 주소: http://localhost:5000")
    print("\n【 기능 】")
    print("  ✅ 학생 관리 (등록, 조회)")
    print("  ✅ 성적 관리 (추가, 조회)")
    print("  ✅ 출석 관리 (기록, 조회)")
    print("  ✅ 학과 정보 (조회)")
    print("  ✅ 교과목 (조회)")
    print("  ✅ 학생 상세 정보")
    print("\n【 사용 기술 】")
    print("  ✓ Flask (웹 프레임워크)")
    print("  ✓ SQLite (데이터베이스)")
    print("  ✓ HTML/CSS (UI)")
    print("  ✓ JavaScript (상호작용)")
    print("\n저장 필수 너는 기록이 증명이다 gogs")
    print("="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
