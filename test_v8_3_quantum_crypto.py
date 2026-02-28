#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【 v8.3: 양자 내성 암호 & PQC — 테스트 스위트 】

19개의 테스트 케이스로 양자 시대의 보안을 검증한다.
"""

import unittest
import time
from university_v8_3_QUANTUM_RESISTANT_CRYPTO import (
    QuantumThreat,
    CipherType,
    CryptoAgility,
    QuantumKey,
    EncapsulationResult,
    CryptoConfig,
    ThreatReport,
    QuantumThreatAnalyzer,
    LatticeKEM,
    HybridCryptoSystem,
    CryptoAgilityEngine,
    QuantumRandomNumberGenerator,
    GogsSecurityGate,
)


# ═══════════════════════════════════════════════════════════════════════════
# TestQuantumThreatAnalyzer (테스트 01~03)
# ═══════════════════════════════════════════════════════════════════════════


class TestQuantumThreatAnalyzer(unittest.TestCase):
    """양자 위협 분석 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.analyzer = QuantumThreatAnalyzer()

    def test_01_shor_threat_analysis(self):
        """test_01: 쇼어 알고리즘 위협 분석"""
        result = self.analyzer.analyze_shor_threat(2048)

        # RSA-2048 위협이 충분히 높아야 함
        self.assertIn("speedup_factor", result)
        self.assertGreater(result["speedup_factor"], 100000)  # 충분한 가속
        self.assertEqual(result["threat_level"], "CRITICAL")

    def test_02_grover_threat_analysis(self):
        """test_02: 그로버 알고리즘 위협 분석"""
        result = self.analyzer.analyze_grover_threat(256)

        # AES-256이 128비트로 축소되어야 함
        self.assertEqual(result["effective_bits_after_grover"], 128)
        self.assertIn("AES-512", result["recommendation"])

    def test_03_threat_report_generation(self):
        """test_03: 위협 보고서 생성"""
        report = self.analyzer.create_threat_report(QuantumThreat.SHOR)

        # 보고서가 정상적으로 생성되어야 함
        self.assertEqual(report.threat_type, QuantumThreat.SHOR)
        self.assertIn(CipherType.RSA, report.affected_ciphers)
        self.assertIn(CipherType.ECC, report.affected_ciphers)
        self.assertGreater(len(report.recommended_actions), 0)


# ═══════════════════════════════════════════════════════════════════════════
# TestLatticeKEM (테스트 04~07)
# ═══════════════════════════════════════════════════════════════════════════


class TestLatticeKEM(unittest.TestCase):
    """격자 기반 KEM 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.lattice = LatticeKEM(512)

    def test_04_keypair_generation(self):
        """test_04: 격자 기반 키 쌍 생성"""
        pub, priv = self.lattice.generate_keypair()

        # 키가 생성되어야 함
        self.assertIsInstance(pub, bytes)
        self.assertIsInstance(priv, bytes)
        self.assertEqual(len(pub), 32)  # SHA256 해시
        self.assertEqual(len(priv), 32)

    def test_05_encapsulation(self):
        """test_05: 키 캡슐화"""
        pub, _ = self.lattice.generate_keypair()
        result = self.lattice.encapsulate(pub)

        # 캡슐화 결과가 유효해야 함
        self.assertIsInstance(result, EncapsulationResult)
        self.assertEqual(result.algorithm, CipherType.LATTICE)
        self.assertIsInstance(result.ciphertext, bytes)
        self.assertIsInstance(result.shared_secret, bytes)
        self.assertGreater(result.encapsulation_time_ms, 0)

    def test_06_decapsulation(self):
        """test_06: 키 캡슐화 해제"""
        pub, priv = self.lattice.generate_keypair()
        encap_result = self.lattice.encapsulate(pub)

        # 캡슐화 해제가 작동해야 함
        recovered_secret = self.lattice.decapsulate(encap_result.ciphertext, priv)
        self.assertIsInstance(recovered_secret, bytes)
        self.assertEqual(len(recovered_secret), 32)

    def test_07_cipher_type(self):
        """test_07: 암호 타입 확인"""
        cipher_type = self.lattice.cipher_type()
        self.assertEqual(cipher_type, CipherType.LATTICE)


# ═══════════════════════════════════════════════════════════════════════════
# TestHybridCrypto (테스트 08~10)
# ═══════════════════════════════════════════════════════════════════════════


class TestHybridCryptoSystem(unittest.TestCase):
    """하이브리드 암호 시스템 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.hybrid = HybridCryptoSystem()
        self.lattice = LatticeKEM()

    def test_08_hybrid_encapsulation(self):
        """test_08: 하이브리드 캡슐화"""
        rsa_pub = b"dummy_rsa_pub"
        lattice_pub, _ = self.lattice.generate_keypair()

        result = self.hybrid.hybrid_encapsulate(rsa_pub, lattice_pub)

        # 결과가 RSA + Lattice 모두 포함
        self.assertIn("rsa_ciphertext", result)
        self.assertIn("lattice_ciphertext", result)
        self.assertIn("final_shared_secret", result)
        self.assertEqual(result["security_level"], "POST_QUANTUM")

    def test_09_hybrid_decapsulation(self):
        """test_09: 하이브리드 캡슐화 해제"""
        rsa_pub = b"dummy_rsa_pub"
        rsa_priv = b"dummy_rsa_priv"
        lattice_pub, lattice_priv = self.lattice.generate_keypair()

        encap = self.hybrid.hybrid_encapsulate(rsa_pub, lattice_pub)

        recovered = self.hybrid.hybrid_decapsulate(
            encap["rsa_ciphertext"],
            encap["lattice_ciphertext"],
            rsa_priv,
            lattice_priv,
        )

        self.assertIsInstance(recovered, bytes)
        self.assertEqual(len(recovered), 32)

    def test_10_hybrid_dual_layer_security(self):
        """test_10: 이중 레이어 보안 검증"""
        rsa_pub = b"dummy_rsa_pub"
        lattice_pub, _ = self.lattice.generate_keypair()

        result = self.hybrid.hybrid_encapsulate(rsa_pub, lattice_pub)

        # RSA와 Lattice 둘 다 실패해야 전체 시스템이 무너짐
        # (하나는 고전, 하나는 양자 내성)
        self.assertTrue(len(result["rsa_ciphertext"]) > 0)
        self.assertTrue(len(result["lattice_ciphertext"]) > 0)
        self.assertTrue(
            len(result["final_shared_secret"]) > 0, "Dual-layer failed"
        )


# ═══════════════════════════════════════════════════════════════════════════
# TestCryptoAgility (테스트 11~13)
# ═══════════════════════════════════════════════════════════════════════════


class TestCryptoAgilityEngine(unittest.TestCase):
    """암호 민첩성 엔진 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.agility = CryptoAgilityEngine()

    def test_11_cipher_registration(self):
        """test_11: 암호 알고리즘 등록"""
        new_cipher = LatticeKEM(256)
        self.agility.register_cipher(CipherType.LATTICE, new_cipher)

        # 암호가 등록되어야 함
        status = self.agility.get_cipher_status()
        self.assertIn(CipherType.LATTICE, status["available_ciphers"])

    def test_12_cipher_switching(self):
        """test_12: 실시간 암호 전환"""
        old_cipher = self.agility.active_cipher
        result = self.agility.switch_cipher(CipherType.LATTICE)

        # 전환이 성공해야 함
        self.assertEqual(result["status"], "SUCCESS")
        self.assertNotEqual(old_cipher, result["new_cipher"])
        self.assertGreater(result["switch_time_ms"], 0)

    def test_13_agility_status(self):
        """test_13: 민첩성 상태 확인"""
        status = self.agility.get_cipher_status()

        self.assertEqual(status["active_cipher"], CipherType.LATTICE.value)
        self.assertGreater(len(status["available_ciphers"]), 0)


# ═══════════════════════════════════════════════════════════════════════════
# TestQRNG (테스트 14~16)
# ═══════════════════════════════════════════════════════════════════════════


class TestQuantumRNG(unittest.TestCase):
    """양자 난수 생성기 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.qrng = QuantumRandomNumberGenerator()

    def test_14_random_generation(self):
        """test_14: 난수 생성"""
        data = self.qrng.generate(32)

        self.assertIsInstance(data, bytes)
        self.assertEqual(len(data), 32)
        self.assertGreater(self.qrng.generated_count, 0)

    def test_15_diehard_test(self):
        """test_15: NIST Diehard 난수 품질 테스트"""
        data = self.qrng.generate(1024)
        test_result = self.qrng.nist_diehard_test(data)

        # 테스트 결과가 유효해야 함
        self.assertIn("chi_square_statistic", test_result)
        self.assertIn("passes_test", test_result)
        self.assertGreater(test_result["entropy_quality"], 0)

    def test_16_entropy_info(self):
        """test_16: 난수 생성기 정보"""
        self.qrng.generate(256)
        info = self.qrng.get_entropy_info()

        self.assertEqual(info["entropy_source"], "quantum")
        self.assertGreater(info["generated_count"], 0)
        self.assertGreater(info["estimated_entropy_bits"], 0)


# ═══════════════════════════════════════════════════════════════════════════
# TestGogsSecurityGate (테스트 17~19)
# ═══════════════════════════════════════════════════════════════════════════


class TestGogsSecurityGate(unittest.TestCase):
    """통합 보안 게이트웨이 테스트"""

    def setUp(self):
        """테스트 설정"""
        config = CryptoConfig(
            primary_cipher=CipherType.LATTICE,
            backup_cipher=CipherType.RSA,
            use_hybrid=True,
        )
        self.gate = GogsSecurityGate(config)

    def test_17_secure_handshake(self):
        """test_17: 양자 내성 핸드셰이크"""
        handshake = self.gate.secure_handshake()

        # 핸드셰이크가 성공해야 함
        self.assertEqual(handshake["status"], "QUANTUM_SAFE")
        self.assertIn("SESSION_", handshake["session_id"])
        self.assertIn("LATTICE", handshake["algorithms"][1])
        self.assertGreater(handshake["entropy_bits"], 0)

    def test_18_threat_response(self):
        """test_18: 위협 자동 대응"""
        response = self.gate.threat_response(QuantumThreat.SHOR)

        # 대응이 작동해야 함
        self.assertEqual(response["threat_type"], QuantumThreat.SHOR.value)
        self.assertEqual(response["status"], "MITIGATED")
        self.assertGreater(len(response["affected_systems"]), 0)
        self.assertGreater(len(response["recommendations"]), 0)

    def test_19_security_status(self):
        """test_19: 보안 상태 확인"""
        # 여러 세션 생성
        self.gate.secure_handshake()
        self.gate.secure_handshake()

        status = self.gate.get_security_status()

        self.assertEqual(status["active_cipher"], CipherType.LATTICE.value)
        self.assertGreaterEqual(status["total_sessions"], 2)
        self.assertEqual(status["overall_status"], "SECURE")


# ═══════════════════════════════════════════════════════════════════════════
# 테스트 실행
# ═══════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    unittest.main(verbosity=2)
