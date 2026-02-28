"""간단한 테스트 서버"""

from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Python University v7</title>
        <style>
            body { font-family: Arial; background: #667eea; color: white; }
            .container { max-width: 800px; margin: 50px auto; }
            h1 { text-align: center; }
            .box { background: white; color: black; padding: 20px; margin: 10px; border-radius: 5px; }
            button { padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Python University v7</h1>
            <h2>웹 기반 학생관리 시스템</h2>
            
            <div class="box">
                <h3>✅ 서버 연결 성공!</h3>
                <p>모든 API가 정상 작동 중입니다.</p>
                
                <h4>📊 API 테스트</h4>
                <button onclick="testAPI()">학생 목록 조회</button>
                <button onclick="testAPI2()">학과 정보 조회</button>
                <button onclick="testAPI3()">교과목 조회</button>
                
                <div id="result" style="margin-top: 20px; background: #f0f0f0; color: black; padding: 10px; border-radius: 5px; display: none;"></div>
            </div>
        </div>
        
        <script>
            function testAPI() {
                fetch('/api/students')
                    .then(r => r.json())
                    .then(data => {
                        let result = '<h4>학생 목록 (' + data.length + '명)</h4>';
                        data.forEach(s => {
                            result += `<p>- ${s.student_id}: ${s.name}</p>`;
                        });
                        document.getElementById('result').innerHTML = result;
                        document.getElementById('result').style.display = 'block';
                    });
            }
            
            function testAPI2() {
                fetch('/api/departments')
                    .then(r => r.json())
                    .then(data => {
                        let result = '<h4>학과 정보 (' + data.length + '개)</h4>';
                        data.forEach(d => {
                            result += `<p>- ${d.name}: ${d.student_count}명</p>`;
                        });
                        document.getElementById('result').innerHTML = result;
                        document.getElementById('result').style.display = 'block';
                    });
            }
            
            function testAPI3() {
                fetch('/api/courses')
                    .then(r => r.json())
                    .then(data => {
                        let result = '<h4>교과목 (' + data.length + '개)</h4>';
                        data.forEach(c => {
                            result += `<p>- ${c.code}: ${c.name}</p>`;
                        });
                        document.getElementById('result').innerHTML = result;
                        document.getElementById('result').style.display = 'block';
                    });
            }
        </script>
    </body>
    </html>
    '''

@app.route('/api/students')
def students():
    return json.dumps([
        {'student_id': '2024001', 'name': 'Kim Gogs', 'department_name': 'CSE'},
        {'student_id': '2024002', 'name': 'Lee AI', 'department_name': 'CSE'},
        {'student_id': '2024003', 'name': 'Park Data', 'department_name': 'DS'},
        {'student_id': '2024004', 'name': 'Choi Eng', 'department_name': 'ENG'},
        {'student_id': '2024005', 'name': 'Jung Smart', 'department_name': 'CSE'}
    ])

@app.route('/api/departments')
def departments():
    return json.dumps([
        {'name': 'Computer Science', 'student_count': 3},
        {'name': 'Data Science', 'student_count': 1},
        {'name': 'English', 'student_count': 1}
    ])

@app.route('/api/courses')
def courses():
    return json.dumps([
        {'code': 'CS101', 'name': 'Programming Basics'},
        {'code': 'CS201', 'name': 'Data Structure'},
        {'code': 'DS101', 'name': 'Data Analysis'},
        {'code': 'ENG101', 'name': 'English Conversation'},
        {'code': 'CS301', 'name': 'AI Basics'}
    ])

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 Python University v7 - 간단한 테스트 서버")
    print("="*80)
    print("\n🌐 접속 주소: http://localhost:5000")
    print("\n【 기능 】")
    print("  ✅ 학생 목록 조회")
    print("  ✅ 학과 정보 조회")
    print("  ✅ 교과목 조회")
    print("\n【 종료 】")
    print("  Ctrl+C")
    print("\n" + "="*80 + "\n")
    
    app.run(debug=False, host='127.0.0.1', port=5000)
