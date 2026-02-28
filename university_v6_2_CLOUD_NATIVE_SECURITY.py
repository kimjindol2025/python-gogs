#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════════════════════╗
║    Python University v6.2: 클라우드 네이티브 보안 아키텍처 & 제로 트러스트     ║
║              Cloud-Native Security & Zero Trust Architecture              ║
║                                                                            ║
║  철학: 기록이 증명이다 gogs                                                  ║
║  원칙: 아무도 믿지 말고, 모든 것을 증명하고 기록하라                            ║
║                                                                            ║
║  【 핵심 개념 】                                                            ║
║  1. 암호화 & 해싱 (Encryption & Hashing)                                  ║
║  2. 사용자 인증 (Authentication)                                          ║
║  3. 역할 기반 접근 제어 (RBAC)                                            ║
║  4. JWT 토큰 (JSON Web Token)                                            ║
║  5. WAF (Web Application Firewall)                                       ║
║  6. 감사 로깅 (Audit Trail)                                              ║
║  7. TLS/SSL 보안 채널 (Secure Channel)                                   ║
║  8. 비밀 관리 (Secrets Management)                                       ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import hashlib
import hmac
import json
import secrets
import re
import base64
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import unittest

# ═══════════════════════════════════════════════════════════════════════════
# PART 1: 암호화 & 해싱 기본
# ═══════════════════════════════════════════════════════════════════════════

class EncryptionMethod(Enum):
    """암호화 알고리즘"""
    SHA256 = "sha256"
    PBKDF2 = "pbkdf2"
    HMAC = "hmac"

@dataclass
class CryptoConfig:
    """암호화 설정"""
    algorithm: EncryptionMethod = EncryptionMethod.PBKDF2
    hash_iterations: int = 100000
    salt_length: int = 32
    token_expiry_minutes: int = 60

class CryptoEngine:
    """암호화 엔진: 해싱, 대칭/비대칭 암호화"""

    def __init__(self, config: CryptoConfig = CryptoConfig()):
        self.config = config
        self.log: List[str] = []

    def generate_salt(self) -> bytes:
        """무작위 솔트 생성"""
        salt = secrets.token_bytes(self.config.salt_length)
        self._log("CRYPTO", f"솔트 생성 (길이: {len(salt)} bytes)")
        return salt

    def hash_password(self, password: str, salt: Optional[bytes] = None) -> Tuple[str, str]:
        """
        비밀번호 해싱 (PBKDF2)

        Returns:
            (hex_salt, hex_hash) 튜플
        """
        if salt is None:
            salt = self.generate_salt()

        # PBKDF2 해싱: 반복 횟수를 높여 Brute-force 공격 방지
        hash_bytes = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            self.config.hash_iterations
        )

        hex_salt = salt.hex()
        hex_hash = hash_bytes.hex()

        self._log("CRYPTO", f"비밀번호 해싱 완료 (반복: {self.config.hash_iterations})")
        return hex_salt, hex_hash

    def verify_password(self, password: str, stored_salt: str, stored_hash: str) -> bool:
        """저장된 해시값과 비교하여 검증"""
        salt = bytes.fromhex(stored_salt)
        _, computed_hash = self.hash_password(password, salt)

        # 타이밍 공격(Timing Attack) 방지: 상수 시간 비교
        is_valid = hmac.compare_digest(computed_hash, stored_hash)

        self._log("CRYPTO", f"비밀번호 검증: {'성공' if is_valid else '실패'}")
        return is_valid

    def hmac_sign(self, message: str, secret: str) -> str:
        """HMAC 서명"""
        signature = hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        self._log("CRYPTO", "HMAC 서명 생성")
        return signature

    def hmac_verify(self, message: str, signature: str, secret: str) -> bool:
        """HMAC 서명 검증"""
        expected = self.hmac_sign(message, secret)
        is_valid = hmac.compare_digest(signature, expected)

        self._log("CRYPTO", f"HMAC 검증: {'성공' if is_valid else '실패'}")
        return is_valid

    def _log(self, level: str, message: str):
        """로그 기록"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {level}: {message}"
        self.log.append(log_entry)

# ═══════════════════════════════════════════════════════════════════════════
# PART 2: 사용자 인증 시스템
# ═══════════════════════════════════════════════════════════════════════════

class UserRole(Enum):
    """사용자 역할"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

@dataclass
class User:
    """사용자 정보"""
    username: str
    email: str
    salt: str
    password_hash: str
    role: UserRole = UserRole.USER
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    mfa_enabled: bool = False
    is_active: bool = True

@dataclass
class AuthToken:
    """인증 토큰"""
    user_id: str
    username: str
    role: UserRole
    issued_at: datetime
    expires_at: datetime
    token_id: str = field(default_factory=lambda: secrets.token_hex(16))

    def is_expired(self) -> bool:
        """토큰 만료 확인"""
        return datetime.now() > self.expires_at

class AuthenticationEngine:
    """사용자 인증 엔진"""

    def __init__(self, crypto: CryptoEngine):
        self.crypto = crypto
        self.users: Dict[str, User] = {}
        self.auth_tokens: Dict[str, AuthToken] = {}
        self.failed_attempts: Dict[str, int] = {}
        self.lockout_threshold = 5
        self.lockout_duration_seconds = 300
        self.audit_log: List[str] = []

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        role: UserRole = UserRole.USER
    ) -> Tuple[bool, str]:
        """사용자 등록"""
        # 1. 유효성 검사
        if username in self.users:
            self._audit_log("REGISTER", f"실패: {username} 이미 존재", "FAIL")
            return False, "사용자 이미 존재"

        if not self._validate_email(email):
            self._audit_log("REGISTER", f"실패: {email} 유효하지 않음", "FAIL")
            return False, "이메일 형식 오류"

        if not self._validate_password(password):
            self._audit_log("REGISTER", f"실패: {username} 약한 비밀번호", "FAIL")
            return False, "비밀번호가 너무 약합니다 (8자 이상, 특수문자 포함)"

        # 2. 비밀번호 해싱
        salt, hash_value = self.crypto.hash_password(password)

        # 3. 사용자 저장
        user = User(
            username=username,
            email=email,
            salt=salt,
            password_hash=hash_value,
            role=role
        )
        self.users[username] = user

        self._audit_log("REGISTER", f"성공: {username} ({role.value})", "SUCCESS")
        return True, f"{username}님 등록 완료"

    def login(self, username: str, password: str) -> Tuple[bool, Optional[AuthToken], str]:
        """사용자 로그인"""
        # 1. 계정 잠금 확인
        if self._is_account_locked(username):
            self._audit_log("LOGIN", f"실패: {username} 계정 잠금 (5회 실패)", "FAIL")
            return False, None, "계정이 임시 잠금되었습니다"

        # 2. 사용자 존재 확인
        if username not in self.users:
            self._record_failed_attempt(username)
            self._audit_log("LOGIN", f"실패: {username} 사용자 없음", "FAIL")
            return False, None, "사용자 없음"

        user = self.users[username]

        # 3. 활성 확인
        if not user.is_active:
            self._audit_log("LOGIN", f"실패: {username} 비활성 계정", "FAIL")
            return False, None, "계정이 비활성화되었습니다"

        # 4. 비밀번호 검증
        if not self.crypto.verify_password(password, user.salt, user.password_hash):
            self._record_failed_attempt(username)
            self._audit_log("LOGIN", f"실패: {username} 잘못된 비밀번호", "FAIL")
            return False, None, "비밀번호 오류"

        # 5. 토큰 생성
        token = self._create_token(user)
        self.auth_tokens[token.token_id] = token
        user.last_login = datetime.now()

        # 6. 실패 횟수 초기화
        self.failed_attempts[username] = 0

        self._audit_log("LOGIN", f"성공: {username}", "SUCCESS")
        return True, token, f"{username}님 로그인 성공"

    def logout(self, token_id: str) -> bool:
        """로그아웃"""
        if token_id in self.auth_tokens:
            token = self.auth_tokens[token_id]
            del self.auth_tokens[token_id]
            self._audit_log("LOGOUT", f"성공: {token.username}", "SUCCESS")
            return True

        self._audit_log("LOGOUT", f"실패: 토큰 없음", "FAIL")
        return False

    def verify_token(self, token_id: str) -> Tuple[bool, Optional[AuthToken]]:
        """토큰 검증"""
        if token_id not in self.auth_tokens:
            self._audit_log("TOKEN_VERIFY", "실패: 토큰 없음", "FAIL")
            return False, None

        token = self.auth_tokens[token_id]

        if token.is_expired():
            del self.auth_tokens[token_id]
            self._audit_log("TOKEN_VERIFY", f"실패: {token.username} 토큰 만료", "FAIL")
            return False, None

        self._audit_log("TOKEN_VERIFY", f"성공: {token.username}", "SUCCESS")
        return True, token

    def _create_token(self, user: User) -> AuthToken:
        """토큰 생성"""
        now = datetime.now()
        expires_at = now + timedelta(minutes=60)

        token = AuthToken(
            user_id=user.username,
            username=user.username,
            role=user.role,
            issued_at=now,
            expires_at=expires_at
        )

        self._audit_log("TOKEN_CREATE", f"생성: {user.username}", "SUCCESS")
        return token

    def _is_account_locked(self, username: str) -> bool:
        """계정 잠금 확인"""
        return self.failed_attempts.get(username, 0) >= self.lockout_threshold

    def _record_failed_attempt(self, username: str):
        """실패 횟수 기록"""
        self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1

    def _validate_email(self, email: str) -> bool:
        """이메일 유효성 검사"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _validate_password(self, password: str) -> bool:
        """비밀번호 강도 검사"""
        # 최소 8자, 대문자, 소문자, 숫자, 특수문자 포함
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    def _audit_log(self, action: str, details: str, status: str):
        """감사 로그 기록"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {action} ({status}): {details}"
        self.audit_log.append(log_entry)

# ═══════════════════════════════════════════════════════════════════════════
# PART 3: 역할 기반 접근 제어 (RBAC)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class Permission:
    """권한"""
    resource: str
    action: str  # read, write, delete, admin

    def __hash__(self):
        return hash((self.resource, self.action))

    def __eq__(self, other):
        return self.resource == other.resource and self.action == other.action

class RBACEngine:
    """역할 기반 접근 제어"""

    def __init__(self):
        self.role_permissions: Dict[UserRole, set] = {
            UserRole.ADMIN: {
                Permission("users", "read"),
                Permission("users", "write"),
                Permission("users", "delete"),
                Permission("system", "admin"),
                Permission("logs", "read"),
                Permission("config", "write"),
            },
            UserRole.USER: {
                Permission("profile", "read"),
                Permission("profile", "write"),
                Permission("data", "read"),
                Permission("data", "write"),
            },
            UserRole.GUEST: {
                Permission("public", "read"),
            },
        }
        self.audit_log: List[str] = []

    def check_permission(
        self,
        role: UserRole,
        resource: str,
        action: str
    ) -> bool:
        """권한 확인"""
        required_perm = Permission(resource, action)
        has_perm = required_perm in self.role_permissions.get(role, set())

        status = "GRANT" if has_perm else "DENY"
        self._audit_log(f"{role.value}", f"{action} {resource}", status)

        return has_perm

    def _audit_log(self, role: str, resource: str, status: str):
        """감사 로그"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] RBAC ({status}): {role} → {resource}"
        self.audit_log.append(log_entry)

# ═══════════════════════════════════════════════════════════════════════════
# PART 4: JWT 토큰 (간단한 구현)
# ═══════════════════════════════════════════════════════════════════════════

class JWTEngine:
    """JSON Web Token 엔진"""

    def __init__(self, secret: str):
        self.secret = secret
        self.audit_log: List[str] = []

    def create_jwt(self, payload: Dict) -> str:
        """JWT 생성"""
        # Header (Base64URL)
        header = {
            "alg": "HS256",
            "typ": "JWT"
        }
        header_b64 = self._base64url_encode(json.dumps(header))

        # Payload (Base64URL)
        payload["iat"] = datetime.now().timestamp()
        payload["exp"] = (datetime.now() + timedelta(hours=1)).timestamp()
        payload_b64 = self._base64url_encode(json.dumps(payload))

        # Signature
        message = f"{header_b64}.{payload_b64}"
        signature = hmac.new(
            self.secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        signature_b64 = base64.urlsafe_b64encode(signature.encode()).decode().rstrip('=')

        jwt_token = f"{message}.{signature_b64}"
        self._audit_log("JWT_CREATE", "성공")
        return jwt_token

    def verify_jwt(self, token: str) -> Tuple[bool, Optional[Dict]]:
        """JWT 검증"""
        try:
            parts = token.split('.')
            if len(parts) != 3:
                self._audit_log("JWT_VERIFY", "실패: 형식 오류")
                return False, None

            header_b64, payload_b64, signature_b64 = parts

            # Signature 검증
            message = f"{header_b64}.{payload_b64}"
            expected_sig = hmac.new(
                self.secret.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()

            expected_sig_b64 = base64.urlsafe_b64encode(expected_sig.encode()).decode().rstrip('=')

            if not hmac.compare_digest(signature_b64, expected_sig_b64):
                self._audit_log("JWT_VERIFY", "실패: 서명 불일치")
                return False, None

            # Payload 디코딩
            payload_json = base64.urlsafe_b64decode(payload_b64 + '===')
            payload = json.loads(payload_json)

            # 만료 확인
            if payload.get("exp", 0) < datetime.now().timestamp():
                self._audit_log("JWT_VERIFY", "실패: 토큰 만료")
                return False, None

            self._audit_log("JWT_VERIFY", "성공")
            return True, payload

        except Exception as e:
            self._audit_log("JWT_VERIFY", f"실패: {str(e)}")
            return False, None

    def _base64url_encode(self, data: str) -> str:
        """Base64URL 인코딩"""
        return base64.urlsafe_b64encode(data.encode()).decode().rstrip('=')

    def _audit_log(self, action: str, status: str):
        """감사 로그"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {action}: {status}"
        self.audit_log.append(log_entry)

# ═══════════════════════════════════════════════════════════════════════════
# PART 5: WAF (Web Application Firewall)
# ═══════════════════════════════════════════════════════════════════════════

class WAFEngine:
    """웹 애플리케이션 방화벽"""

    def __init__(self):
        self.sql_injection_patterns = [
            r"(\bUNION\b.*\bSELECT\b)",
            r"(\bDROP\b.*\bTABLE\b)",
            r"(\bINSERT\b.*\bINTO\b)",
            r"(\bDELETE\b.*\bFROM\b)",
            r"(;\s*--)",
            r"(\bOR\b\s*['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?)",
        ]
        self.xss_patterns = [
            r"(<script[^>]*>.*?</script>)",
            r"(javascript:)",
            r"(onerror\s*=)",
            r"(onload\s*=)",
            r"(<iframe[^>]*>)",
        ]
        self.audit_log: List[str] = []

    def check_sql_injection(self, user_input: str) -> Tuple[bool, Optional[str]]:
        """SQL Injection 탐지"""
        for pattern in self.sql_injection_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                threat = re.search(pattern, user_input, re.IGNORECASE).group()
                self._audit_log("SQL_INJECTION_DETECTED", threat, "BLOCK")
                return False, f"의심스러운 패턴 감지: {threat}"

        self._audit_log("SQL_INJECTION_CHECK", "통과", "ALLOW")
        return True, None

    def check_xss(self, user_input: str) -> Tuple[bool, Optional[str]]:
        """XSS (Cross-Site Scripting) 탐지"""
        for pattern in self.xss_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                threat = re.search(pattern, user_input, re.IGNORECASE).group()
                self._audit_log("XSS_DETECTED", threat, "BLOCK")
                return False, f"의심스러운 스크립트 감지: {threat}"

        self._audit_log("XSS_CHECK", "통과", "ALLOW")
        return True, None

    def sanitize_input(self, user_input: str) -> str:
        """사용자 입력 정제"""
        # 위험한 문자 이스케이프
        sanitized = user_input.replace("<", "&lt;").replace(">", "&gt;").replace("'", "&#x27;").replace('"', "&quot;")
        self._audit_log("SANITIZE_INPUT", "완료", "SUCCESS")
        return sanitized

    def _audit_log(self, action: str, details: str, status: str):
        """감사 로그"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] WAF {action} ({status}): {details}"
        self.audit_log.append(log_entry)

# ═══════════════════════════════════════════════════════════════════════════
# PART 6: 통합 보안 엔진
# ═══════════════════════════════════════════════════════════════════════════

class SecurityArchitecture:
    """통합 보안 아키텍처"""

    def __init__(self):
        self.crypto = CryptoEngine()
        self.auth = AuthenticationEngine(self.crypto)
        self.rbac = RBACEngine()
        self.jwt = JWTEngine(secret="super_secret_key_gogs")
        self.waf = WAFEngine()
        self.access_log: List[str] = []

    def authenticate_and_authorize(
        self,
        username: str,
        password: str,
        required_resource: str,
        required_action: str
    ) -> Tuple[bool, str]:
        """인증 + 인가 통합"""
        # 1. WAF 검사
        is_safe, waf_error = self.waf.check_sql_injection(username)
        if not is_safe:
            return False, f"WAF 차단: {waf_error}"

        # 2. 로그인
        success, token, message = self.auth.login(username, password)
        if not success:
            return False, message

        # 3. 권한 확인
        if not self.rbac.check_permission(token.role, required_resource, required_action):
            self._access_log(username, required_resource, "DENY")
            return False, "권한 부족"

        # 4. JWT 토큰 생성
        jwt_token = self.jwt.create_jwt({
            "sub": username,
            "role": token.role.value,
            "resource": required_resource,
            "action": required_action
        })

        self._access_log(username, required_resource, "GRANT")
        return True, f"인증/인가 성공. JWT: {jwt_token[:50]}..."

    def secure_api_call(
        self,
        token_id: str,
        resource: str,
        action: str,
        data: str
    ) -> Tuple[bool, str]:
        """안전한 API 호출"""
        # 1. 토큰 검증
        valid, token = self.auth.verify_token(token_id)
        if not valid:
            return False, "토큰 검증 실패"

        # 2. 권한 확인
        if not self.rbac.check_permission(token.role, resource, action):
            return False, "권한 부족"

        # 3. WAF 검사
        is_safe, waf_error = self.waf.check_sql_injection(data)
        if not is_safe:
            return False, f"WAF 차단: {waf_error}"

        is_safe, waf_error = self.waf.check_xss(data)
        if not is_safe:
            return False, f"WAF 차단: {waf_error}"

        # 4. 데이터 정제
        sanitized_data = self.waf.sanitize_input(data)

        self._access_log(token.username, f"{action} {resource}", "SUCCESS")
        return True, f"API 호출 성공 (데이터: {sanitized_data})"

    def _access_log(self, user: str, resource: str, status: str):
        """접근 로그"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] ACCESS ({status}): {user} → {resource}"
        self.access_log.append(log_entry)

# ═══════════════════════════════════════════════════════════════════════════
# PART 7: 데모 함수
# ═══════════════════════════════════════════════════════════════════════════

def demo_1_user_authentication():
    """데모 1: 사용자 인증"""
    print("\n" + "="*80)
    print("데모 1: 사용자 인증 (Registration & Login)")
    print("="*80)

    security = SecurityArchitecture()

    # 등록
    print("\n[사용자 등록]")
    success, msg = security.auth.register_user(
        username="designer_gogs",
        email="gogs@example.com",
        password="SecurePass123!",
        role=UserRole.USER
    )
    print(f"  {msg}")

    # 로그인 성공
    print("\n[로그인 성공 시도]")
    success, token, msg = security.auth.login("designer_gogs", "SecurePass123!")
    print(f"  {msg}")
    if token:
        print(f"  토큰 ID: {token.token_id}")
        print(f"  만료: {token.expires_at}")

    # 로그인 실패
    print("\n[로그인 실패 시도]")
    success, token, msg = security.auth.login("designer_gogs", "WrongPassword")
    print(f"  {msg}")

def demo_2_rbac():
    """데모 2: 역할 기반 접근 제어"""
    print("\n" + "="*80)
    print("데모 2: 역할 기반 접근 제어 (RBAC)")
    print("="*80)

    rbac = RBACEngine()

    print("\n[ADMIN 권한]")
    print(f"  system admin: {rbac.check_permission(UserRole.ADMIN, 'system', 'admin')}")
    print(f"  users delete: {rbac.check_permission(UserRole.ADMIN, 'users', 'delete')}")

    print("\n[USER 권한]")
    print(f"  profile write: {rbac.check_permission(UserRole.USER, 'profile', 'write')}")
    print(f"  system admin: {rbac.check_permission(UserRole.USER, 'system', 'admin')}")

    print("\n[GUEST 권한]")
    print(f"  public read: {rbac.check_permission(UserRole.GUEST, 'public', 'read')}")
    print(f"  profile read: {rbac.check_permission(UserRole.GUEST, 'profile', 'read')}")

def demo_3_jwt():
    """데모 3: JWT 토큰"""
    print("\n" + "="*80)
    print("데모 3: JWT 토큰 (JSON Web Token)")
    print("="*80)

    jwt = JWTEngine(secret="secret_key")

    # JWT 생성
    payload = {
        "user_id": "user123",
        "username": "designer",
        "role": "admin"
    }
    token = jwt.create_jwt(payload)
    print(f"\n[JWT 생성]")
    print(f"  토큰 (처음 50글자): {token[:50]}...")

    # JWT 검증
    print(f"\n[JWT 검증]")
    valid, decoded = jwt.verify_jwt(token)
    print(f"  유효성: {valid}")
    if decoded:
        print(f"  사용자: {decoded.get('username')}")
        print(f"  역할: {decoded.get('role')}")

    # 잘못된 토큰
    print(f"\n[잘못된 토큰 검증]")
    valid, decoded = jwt.verify_jwt("invalid.token.here")
    print(f"  유효성: {valid}")

def demo_4_waf():
    """데모 4: WAF (Web Application Firewall)"""
    print("\n" + "="*80)
    print("데모 4: WAF 공격 탐지")
    print("="*80)

    waf = WAFEngine()

    # SQL Injection 테스트
    print("\n[SQL Injection 탐지]")
    test_cases = [
        ("SELECT * FROM users", "정상 쿼리"),
        ("'; DROP TABLE users; --", "SQL Injection"),
        ("1 OR 1=1", "조건 조작"),
    ]

    for payload, description in test_cases:
        is_safe, error = waf.check_sql_injection(payload)
        status = "✓ 통과" if is_safe else "✗ 차단"
        print(f"  {status}: {description}")

    # XSS 테스트
    print("\n[XSS (Cross-Site Scripting) 탐지]")
    xss_cases = [
        ("<script>alert('xss')</script>", "Script 태그"),
        ("javascript:void(0)", "Javascript URL"),
        ("<img onerror=alert('xss')>", "Event Handler"),
        ("Hello World", "정상 텍스트"),
    ]

    for payload, description in xss_cases:
        is_safe, error = waf.check_xss(payload)
        status = "✓ 통과" if is_safe else "✗ 차단"
        print(f"  {status}: {description}")

def demo_5_integrated_security():
    """데모 5: 통합 보안 아키텍처"""
    print("\n" + "="*80)
    print("데모 5: 통합 보안 시스템")
    print("="*80)

    security = SecurityArchitecture()

    # 사용자 등록
    security.auth.register_user(
        "admin_gogs",
        "admin@example.com",
        "AdminSecure123!",
        role=UserRole.ADMIN
    )

    # 인증 + 인가
    print("\n[인증/인가 통합]")
    success, msg = security.authenticate_and_authorize(
        username="admin_gogs",
        password="AdminSecure123!",
        required_resource="system",
        required_action="admin"
    )
    print(f"  결과: {msg[:80]}...")

    # 안전한 API 호출
    print("\n[안전한 API 호출]")
    _, token, _ = security.auth.login("admin_gogs", "AdminSecure123!")

    if token:
        success, msg = security.secure_api_call(
            token_id=token.token_id,
            resource="config",
            action="write",
            data="{'setting': 'value'}"
        )
        print(f"  결과: {msg}")

        # 악의적 데이터 차단
        print(f"\n[악의적 데이터 차단]")
        success, msg = security.secure_api_call(
            token_id=token.token_id,
            resource="config",
            action="write",
            data="'; DROP TABLE config; --"
        )
        print(f"  결과: {msg}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 8: 단위 테스트
# ═══════════════════════════════════════════════════════════════════════════

class TestCloudNativeSecurity(unittest.TestCase):
    """클라우드 네이티브 보안 테스트"""

    def setUp(self):
        self.security = SecurityArchitecture()

    def test_1_password_hashing(self):
        """테스트 1: 비밀번호 해싱"""
        password = "TestPassword123!"
        salt, hash_value = self.security.crypto.hash_password(password)

        self.assertTrue(len(salt) > 0)
        self.assertTrue(len(hash_value) > 0)
        self.assertNotEqual(password, hash_value)

        # 검증
        is_valid = self.security.crypto.verify_password(password, salt, hash_value)
        self.assertTrue(is_valid)

    def test_2_user_registration_and_login(self):
        """테스트 2: 사용자 등록 및 로그인"""
        success, msg = self.security.auth.register_user(
            "testuser",
            "test@example.com",
            "TestPass123!"
        )
        self.assertTrue(success)

        # 로그인 성공
        success, token, msg = self.security.auth.login("testuser", "TestPass123!")
        self.assertTrue(success)
        self.assertIsNotNone(token)

        # 로그인 실패
        success, token, msg = self.security.auth.login("testuser", "WrongPass")
        self.assertFalse(success)

    def test_3_rbac_permissions(self):
        """테스트 3: RBAC 권한 확인"""
        # ADMIN 권한
        has_perm = self.security.rbac.check_permission(
            UserRole.ADMIN, "system", "admin"
        )
        self.assertTrue(has_perm)

        # USER 비권한
        has_perm = self.security.rbac.check_permission(
            UserRole.USER, "system", "admin"
        )
        self.assertFalse(has_perm)

    def test_4_jwt_token_validation(self):
        """테스트 4: JWT 토큰 검증"""
        payload = {"user_id": "123", "role": "admin"}
        token = self.security.jwt.create_jwt(payload)

        valid, decoded = self.security.jwt.verify_jwt(token)
        self.assertTrue(valid)
        self.assertEqual(decoded["user_id"], "123")

    def test_5_waf_attack_detection(self):
        """테스트 5: WAF 공격 탐지"""
        # SQL Injection 탐지
        is_safe, _ = self.security.waf.check_sql_injection(
            "'; DROP TABLE users; --"
        )
        self.assertFalse(is_safe)

        # 정상 입력
        is_safe, _ = self.security.waf.check_sql_injection("normal_input")
        self.assertTrue(is_safe)

# ═══════════════════════════════════════════════════════════════════════════
# 메인 실행
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "Python University v6.2" + " "*36 + "║")
    print("║" + " "*10 + "클라우드 네이티브 보안 아키텍처 & 제로 트러스트" + " "*18 + "║")
    print("║" + " "*24 + "기록이 증명이다 gogs" + " "*33 + "║")
    print("╚" + "="*78 + "╝")

    # 데모 실행
    demo_1_user_authentication()
    demo_2_rbac()
    demo_3_jwt()
    demo_4_waf()
    demo_5_integrated_security()

    # 단위 테스트 실행
    print("\n" + "="*80)
    print("단위 테스트 실행")
    print("="*80 + "\n")

    unittest.main(argv=[''], exit=False, verbosity=2)

    print("\n" + "="*80)
    print("✓ v6.2 클라우드 네이티브 보안 완성!")
    print("  다음 단계: v6.3 졸업 논문 & 최종 아키텍처")
    print("="*80)
    print("\n저장 필수 너는 기록이 증명이다 gogs\n")
