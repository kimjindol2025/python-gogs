"""
【 Python University v5.3 】
REST API 설계와 웹 프레임워크 기초 — 시스템의 외부 개방

데이터베이스(v5.2)의 연구 기록을 외부에서 접근 가능하도록
HTTP 기반의 RESTful API 서버를 설계합니다.

핵심:
- Resource (자원): /api/experiments
- HTTP Method: GET (Read), POST (Create), PUT (Update), DELETE (Delete)
- JSON: 표준 데이터 교환 형식
- Stateless: 서버가 클라이언트 상태를 기억하지 않음
"""

from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json

app = Flask(__name__)

# ═══════════════════════════════════════════════════════════════════════════
# 【 Database 설정 】
# ═══════════════════════════════════════════════════════════════════════════

DB_PATH = "research_records.db"

def init_db():
    """데이터베이스 초기화"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'In Progress',
            result REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 샘플 데이터
    try:
        cursor.execute(
            "INSERT INTO experiments (subject, description, status, result) VALUES (?, ?, ?, ?)",
            ("Async Engine", "비동기 프로그래밍 엔진 설계", "Success", 98.5)
        )
        cursor.execute(
            "INSERT INTO experiments (subject, description, status, result) VALUES (?, ?, ?, ?)",
            ("Metaclass Audit", "메타클래스 감사", "In Progress", None)
        )
        cursor.execute(
            "INSERT INTO experiments (subject, description, status, result) VALUES (?, ?, ?, ?)",
            ("Database Design", "데이터베이스 구조 설계", "Success", 95.0)
        )
        conn.commit()
    except:
        pass  # 이미 존재
    
    conn.close()


# ═══════════════════════════════════════════════════════════════════════════
# 【 REST API Endpoints 】
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/api/experiments', methods=['GET'])
def get_all_experiments():
    """
    【 GET /api/experiments 】
    모든 실험 기록 조회
    
    HTTP Method: GET (Read)
    Status Code: 200 OK
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM experiments ORDER BY created_at DESC")
    experiments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        "status": "success",
        "count": len(experiments),
        "data": experiments
    }), 200


@app.route('/api/experiments/<int:exp_id>', methods=['GET'])
def get_experiment(exp_id):
    """
    【 GET /api/experiments/<id> 】
    특정 실험 기록 조회
    
    Stateless: 각 요청이 독립적으로 완벽한 정보를 포함
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM experiments WHERE id = ?", (exp_id,))
    experiment = cursor.fetchone()
    conn.close()
    
    if not experiment:
        return jsonify({
            "status": "error",
            "message": f"실험 ID {exp_id}를 찾을 수 없습니다"
        }), 404
    
    return jsonify({
        "status": "success",
        "data": dict(experiment)
    }), 200


@app.route('/api/experiments', methods=['POST'])
def create_experiment():
    """
    【 POST /api/experiments 】
    새로운 실험 기록 생성
    
    HTTP Method: POST (Create)
    Status Code: 201 Created
    
    요청 본문 (JSON):
    {
        "subject": "New Experiment",
        "description": "설명",
        "status": "In Progress"
    }
    """
    data = request.get_json()
    
    # 유효성 검사
    if not data or 'subject' not in data:
        return jsonify({
            "status": "error",
            "message": "subject 필드는 필수입니다"
        }), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO experiments (subject, description, status) VALUES (?, ?, ?)",
        (
            data.get('subject'),
            data.get('description', ''),
            data.get('status', 'In Progress')
        )
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        "status": "success",
        "message": "실험 기록이 생성되었습니다",
        "id": new_id
    }), 201


@app.route('/api/experiments/<int:exp_id>', methods=['PUT'])
def update_experiment(exp_id):
    """
    【 PUT /api/experiments/<id> 】
    실험 기록 수정
    
    HTTP Method: PUT (Update)
    Status Code: 200 OK
    
    요청 본문 (JSON):
    {
        "status": "Success",
        "result": 98.5
    }
    """
    data = request.get_json()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 먼저 기록이 존재하는지 확인
    cursor.execute("SELECT * FROM experiments WHERE id = ?", (exp_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({
            "status": "error",
            "message": f"실험 ID {exp_id}를 찾을 수 없습니다"
        }), 404
    
    # 업데이트
    updates = []
    params = []
    
    if 'subject' in data:
        updates.append("subject = ?")
        params.append(data['subject'])
    if 'status' in data:
        updates.append("status = ?")
        params.append(data['status'])
    if 'result' in data:
        updates.append("result = ?")
        params.append(data['result'])
    
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(exp_id)
        
        query = f"UPDATE experiments SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
    
    conn.close()
    
    return jsonify({
        "status": "success",
        "message": "실험 기록이 수정되었습니다",
        "id": exp_id
    }), 200


@app.route('/api/experiments/<int:exp_id>', methods=['DELETE'])
def delete_experiment(exp_id):
    """
    【 DELETE /api/experiments/<id> 】
    실험 기록 삭제
    
    HTTP Method: DELETE (Delete)
    Status Code: 200 OK 또는 204 No Content
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM experiments WHERE id = ?", (exp_id,))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({
            "status": "error",
            "message": f"실험 ID {exp_id}를 찾을 수 없습니다"
        }), 404
    
    conn.close()
    
    return jsonify({
        "status": "success",
        "message": "실험 기록이 삭제되었습니다",
        "id": exp_id
    }), 200


@app.route('/api/experiments/status/<status>', methods=['GET'])
def get_experiments_by_status(status):
    """
    【 GET /api/experiments/status/<status> 】
    상태별 실험 기록 조회
    
    예: /api/experiments/status/Success
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM experiments WHERE status = ? ORDER BY created_at DESC",
        (status,)
    )
    experiments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        "status": "success",
        "filter": status,
        "count": len(experiments),
        "data": experiments
    }), 200


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    【 GET /api/statistics 】
    실험 통계 조회
    
    Stateless 원칙: 서버가 클라이언트 상태를 기억하지 않음
    모든 통계를 매 요청마다 새로 계산
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM experiments")
    total_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM experiments WHERE status = 'Success'")
    success_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(result) FROM experiments WHERE result IS NOT NULL")
    avg_result = cursor.fetchone()[0]
    
    cursor.execute("SELECT MAX(result) FROM experiments WHERE result IS NOT NULL")
    max_result = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        "status": "success",
        "statistics": {
            "total_experiments": total_count,
            "success_count": success_count,
            "average_result": round(avg_result, 2) if avg_result else None,
            "max_result": max_result
        }
    }), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    【 GET /api/health 】
    서버 상태 체크 (헬스 체크)
    
    시스템이 정상 작동하는지 확인
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Gogs Research Record API"
    }), 200


@app.route('/', methods=['GET'])
def api_info():
    """메인 페이지"""
    return jsonify({
        "title": "Python University v5.3",
        "subject": "REST API 설계와 웹 프레임워크 기초",
        "description": "데이터베이스를 HTTP를 통해 외부에 개방",
        "endpoints": {
            "GET /api/experiments": "모든 실험 조회",
            "GET /api/experiments/<id>": "특정 실험 조회",
            "POST /api/experiments": "새로운 실험 생성",
            "PUT /api/experiments/<id>": "실험 수정",
            "DELETE /api/experiments/<id>": "실험 삭제",
            "GET /api/experiments/status/<status>": "상태별 조회",
            "GET /api/statistics": "통계 조회",
            "GET /api/health": "서버 상태 체크"
        },
        "philosophy": "기록이 증명이다 gogs"
    }), 200


# ═══════════════════════════════════════════════════════════════════════════
# 【 테스트 】
# ═══════════════════════════════════════════════════════════════════════════

def test_api():
    """REST API 테스트"""
    client = app.test_client()
    
    print("\n" + "="*80)
    print("【 Python University v5.3 】")
    print("REST API 설계와 웹 프레임워크 기초")
    print("="*80)
    
    # Test 1: 모든 실험 조회 (GET)
    print("\n【 Test 1: GET /api/experiments - 모든 실험 조회 】")
    response = client.get('/api/experiments')
    data = response.get_json()
    print(f"✅ Status: {response.status_code}")
    print(f"✅ 실험 수: {data['count']}")
    for exp in data['data'][:2]:
        print(f"   - {exp['subject']}: {exp['status']}")
    
    # Test 2: 특정 실험 조회 (GET)
    print("\n【 Test 2: GET /api/experiments/1 - 특정 실험 조회 】")
    response = client.get('/api/experiments/1')
    data = response.get_json()
    print(f"✅ Status: {response.status_code}")
    print(f"✅ 실험명: {data['data']['subject']}")
    print(f"✅ 상태: {data['data']['status']}")
    
    # Test 3: 새로운 실험 생성 (POST)
    print("\n【 Test 3: POST /api/experiments - 새로운 실험 생성 】")
    new_exp = {"subject": "API Testing", "description": "테스트", "status": "Testing"}
    response = client.post('/api/experiments', 
                          json=new_exp,
                          content_type='application/json')
    data = response.get_json()
    print(f"✅ Status: {response.status_code} (Created)")
    print(f"✅ 생성된 ID: {data['id']}")
    
    # Test 4: 실험 수정 (PUT)
    print("\n【 Test 4: PUT /api/experiments/1 - 실험 수정 】")
    update_data = {"status": "Success", "result": 99.5}
    response = client.put('/api/experiments/1',
                         json=update_data,
                         content_type='application/json')
    data = response.get_json()
    print(f"✅ Status: {response.status_code}")
    print(f"✅ 메시지: {data['message']}")
    
    # Test 5: 상태별 조회 (GET)
    print("\n【 Test 5: GET /api/experiments/status/Success - 상태별 조회 】")
    response = client.get('/api/experiments/status/Success')
    data = response.get_json()
    print(f"✅ Status: {response.status_code}")
    print(f"✅ Success 실험: {data['count']}개")
    
    # Test 6: 통계 조회 (GET)
    print("\n【 Test 6: GET /api/statistics - 통계 조회 】")
    response = client.get('/api/statistics')
    data = response.get_json()
    print(f"✅ Status: {response.status_code}")
    print(f"✅ 총 실험: {data['statistics']['total_experiments']}개")
    print(f"✅ 성공: {data['statistics']['success_count']}개")
    print(f"✅ 평균: {data['statistics']['average_result']}")
    
    # Test 7: 삭제 (DELETE)
    print("\n【 Test 7: DELETE /api/experiments/<id> - 실험 삭제 】")
    response = client.delete('/api/experiments/4')
    data = response.get_json()
    print(f"✅ Status: {response.status_code}")
    print(f"✅ 메시지: {data['message']}")
    
    # Test 8: 헬스 체크
    print("\n【 Test 8: GET /api/health - 서버 상태 체크 】")
    response = client.get('/api/health')
    data = response.get_json()
    print(f"✅ Status: {response.status_code}")
    print(f"✅ 상태: {data['status']}")
    print(f"✅ 서비스: {data['service']}")
    
    print("\n" + "="*80)
    print("✅ 모든 API 테스트 완료!")
    print("="*80)
    print("\n【 REST API 핵심 개념 】")
    print("  ✓ Resource: /api/experiments")
    print("  ✓ HTTP Method: GET, POST, PUT, DELETE")
    print("  ✓ JSON: 표준 데이터 형식")
    print("  ✓ Status Code: 200, 201, 400, 404")
    print("  ✓ Stateless: 각 요청이 독립적")
    print("\n【 웹 프레임워크의 역할 】")
    print("  ✓ HTTP 요청 처리")
    print("  ✓ 라우팅 (@app.route)")
    print("  ✓ JSON 직렬화")
    print("  ✓ 상태 코드 관리")
    print("\n저장 필수 너는 기록이 증명이다 gogs")
    print("="*80 + "\n")


if __name__ == "__main__":
    init_db()
    
    # 테스트 모드
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test_api()
    else:
        # 서버 실행
        print("\n" + "="*80)
        print("🚀 Python University v5.3 - REST API 서버")
        print("="*80)
        print("\n🌐 접속 주소: http://localhost:5000")
        print("\n【 주요 엔드포인트 】")
        print("  GET  /api/experiments          - 모든 실험 조회")
        print("  GET  /api/experiments/<id>     - 특정 실험 조회")
        print("  POST /api/experiments          - 새로운 실험 생성")
        print("  PUT  /api/experiments/<id>     - 실험 수정")
        print("  DELETE /api/experiments/<id>   - 실험 삭제")
        print("  GET  /api/statistics           - 통계 조회")
        print("\n저장 필수 너는 기록이 증명이다 gogs")
        print("="*80 + "\n")
        
        app.run(debug=True, host='127.0.0.1', port=5000)
