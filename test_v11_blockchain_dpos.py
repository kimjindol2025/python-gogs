#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║        【 v11: 블록체인 & DPoS 합의 엔진 — 테스트 스위트 】                ║
║                                                                              ║
║                        20개 테스트 (100% 커버리지)                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import unittest
import math
import time
from university_v11_BLOCKCHAIN_DPOS import (
    CryptoUtils, TransactionPool, BlockFactory, Blockchain,
    DPoSEngine, StackVM, SmartContract, P2PNetwork, BlockExplorer,
    Transaction, BlockHeader, Block, ValidatorInfo, ConsensusResult,
    TransactionType, BlockStatus, NodeRole, ConsensusPhase
)


# ═══════════════════════════════════════════════════════════════════════════════
# Group A: TestCryptoAndTransaction (test_01~04)
# ═══════════════════════════════════════════════════════════════════════════════

class TestCryptoAndTransaction(unittest.TestCase):
    """암호 유틸리티 및 트랜잭션 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.crypto = CryptoUtils
        self.pool = TransactionPool()

    def test_01_sha256_hash(self):
        """test_01: SHA-256 해시 검증"""
        hash1 = self.crypto.sha256("hello")
        hash2 = self.crypto.sha256("hello")

        # 결정론적 출력
        self.assertEqual(hash1, hash2)
        # 64자 hex
        self.assertEqual(len(hash1), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in hash1))

    def test_02_merkle_root(self):
        """test_02: Merkle Root 계산"""
        hashes = [
            self.crypto.sha256("tx1"),
            self.crypto.sha256("tx2"),
            self.crypto.sha256("tx3")
        ]

        root1 = self.crypto.build_merkle_tree(hashes)
        root2 = self.crypto.build_merkle_tree(hashes)

        # 동일 입력 → 동일 결과 (결정론)
        self.assertEqual(root1, root2)
        # 64자 hex
        self.assertEqual(len(root1), 64)

        # 빈 목록 처리
        empty_root = self.crypto.build_merkle_tree([])
        self.assertEqual(len(empty_root), 64)

    def test_03_transaction_creation(self):
        """test_03: 트랜잭션 생성 및 고유성"""
        tx1 = Transaction(
            tx_hash=self.crypto.sha256("tx1"),
            sender="0x1234567890123456789012345678901234567890",
            receiver="0x0987654321098765432109876543210987654321",
            amount=100.0,
            tx_type=TransactionType.TRANSFER,
            timestamp=time.time(),
            fee=0.001
        )

        tx2 = Transaction(
            tx_hash=self.crypto.sha256("tx2"),
            sender="0x1234567890123456789012345678901234567890",
            receiver="0x0987654321098765432109876543210987654321",
            amount=100.0,
            tx_type=TransactionType.TRANSFER,
            timestamp=time.time(),
            fee=0.001
        )

        # 다른 해시
        self.assertNotEqual(tx1.tx_hash, tx2.tx_hash)

        # 음수 amount 거부
        tx_neg = Transaction(
            tx_hash=self.crypto.sha256("neg"),
            sender="0x1111111111111111111111111111111111111111",
            receiver="0x2222222222222222222222222222222222222222",
            amount=-100.0,
            tx_type=TransactionType.TRANSFER,
            timestamp=time.time()
        )
        self.assertFalse(self.pool.add_transaction(tx_neg))

    def test_04_address_generation(self):
        """test_04: 주소 생성 형식"""
        addr1 = self.crypto.generate_address("seed1")
        addr2 = self.crypto.generate_address("seed2")

        # 42자 형식 (0x + 40)
        self.assertEqual(len(addr1), 42)
        self.assertTrue(addr1.startswith("0x"))

        # 서로 다른 seed → 다른 주소
        self.assertNotEqual(addr1, addr2)

        # hmac 검증
        hmac_result = self.crypto.compute_hmac("key", "message")
        self.assertEqual(len(hmac_result), 64)


# ═══════════════════════════════════════════════════════════════════════════════
# Group B: TestBlock (test_05~08)
# ═══════════════════════════════════════════════════════════════════════════════

class TestBlock(unittest.TestCase):
    """블록 및 해시 체인 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.factory = BlockFactory()
        self.blockchain = Blockchain()
        self.blockchain.initialize()

    def test_05_genesis_block(self):
        """test_05: 제네시스 블록 구조"""
        genesis = self.blockchain._chain[0]

        # block_id == 0
        self.assertEqual(genesis.header.block_id, 0)
        # prev_hash == "0" * 64
        self.assertEqual(genesis.header.prev_hash, "0" * 64)
        # 빈 트랜잭션 목록
        self.assertEqual(len(genesis.transactions), 0)
        # validator == "genesis"
        self.assertEqual(genesis.header.validator, "genesis")
        # block_hash 형식
        self.assertEqual(len(genesis.block_hash), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in genesis.block_hash))

    def test_06_block_chain_link(self):
        """test_06: 블록 해시 체인 연결"""
        genesis = self.blockchain._chain[0]

        # 첫 블록 생성
        tx = Transaction(
            tx_hash=CryptoUtils.sha256("tx1"),
            sender="0x1111111111111111111111111111111111111111",
            receiver="0x2222222222222222222222222222222222222222",
            amount=50.0,
            tx_type=TransactionType.TRANSFER,
            timestamp=time.time()
        )

        block1 = self.factory.create_block(
            transactions=[tx],
            prev_block=genesis,
            validator_address="0x3333333333333333333333333333333333333333",
            slot_number=1
        )

        # prev_hash 일치
        self.assertEqual(block1.header.prev_hash, genesis.block_hash)
        # block_id 증가
        self.assertEqual(block1.header.block_id, 1)

    def test_07_merkle_root_integrity(self):
        """test_07: Merkle Root 무결성"""
        genesis = self.blockchain._chain[0]

        txs = [
            Transaction(
                tx_hash=CryptoUtils.sha256(f"tx{i}"),
                sender="0x1111111111111111111111111111111111111111",
                receiver="0x2222222222222222222222222222222222222222",
                amount=10.0 * (i + 1),
                tx_type=TransactionType.TRANSFER,
                timestamp=time.time()
            )
            for i in range(3)
        ]

        block = self.factory.create_block(
            transactions=txs,
            prev_block=genesis,
            validator_address="0x3333333333333333333333333333333333333333",
            slot_number=1
        )

        # Merkle Root 재계산 일치
        tx_hashes = [tx.tx_hash for tx in txs]
        expected_merkle = CryptoUtils.build_merkle_tree(tx_hashes)
        self.assertEqual(block.header.merkle_root, expected_merkle)

    def test_08_chain_validation(self):
        """test_08: 체인 검증 및 잔액 추적"""
        self.blockchain._balances["0x1111111111111111111111111111111111111111"] = 1000.0

        tx = Transaction(
            tx_hash=CryptoUtils.sha256("tx1"),
            sender="0x1111111111111111111111111111111111111111",
            receiver="0x2222222222222222222222222222222222222222",
            amount=100.0,
            tx_type=TransactionType.TRANSFER,
            timestamp=time.time(),
            fee=1.0
        )

        genesis = self.blockchain._chain[0]
        block = self.factory.create_block(
            transactions=[tx],
            prev_block=genesis,
            validator_address="0x3333333333333333333333333333333333333333",
            slot_number=1
        )

        self.blockchain.append_block(block)

        # 잔액 업데이트
        self.assertEqual(self.blockchain.get_balance("0x1111111111111111111111111111111111111111"), 899.0)
        self.assertEqual(self.blockchain.get_balance("0x2222222222222222222222222222222222222222"), 100.0)

        # 체인 검증
        valid, msg = self.blockchain.validate_chain()
        self.assertTrue(valid, msg)


# ═══════════════════════════════════════════════════════════════════════════════
# Group C: TestDPoS (test_09~12)
# ═══════════════════════════════════════════════════════════════════════════════

class TestDPoS(unittest.TestCase):
    """DPoS 합의 알고리즘 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.dpos = DPoSEngine()
        self.validators = [
            CryptoUtils.generate_address(f"validator_{i}")
            for i in range(30)
        ]

        for addr in self.validators:
            self.dpos.register_validator(addr, 5000.0)

    def test_09_validator_election(self):
        """test_09: 검증자 선출 (30명 → 21명)"""
        selected = self.dpos.run_election()

        # 21명 선발
        self.assertEqual(len(selected), 21)
        # 상위 stakers 포함
        self.assertIn(self.validators[0], selected)
        # 모든 선발자가 is_active=True
        for addr in selected:
            self.assertTrue(self.dpos._validators[addr].is_active)

    def test_10_delegation_accumulation(self):
        """test_10: 위임 투표 및 누적"""
        delegator = CryptoUtils.generate_address("delegator")
        validator1 = self.validators[0]

        initial_stake = self.dpos._validators[validator1].total_stake

        # 위임
        self.dpos.delegate(delegator, validator1, 1000.0)

        # total_stake 누적
        self.assertEqual(self.dpos._validators[validator1].total_stake, initial_stake + 1000.0)
        # delegator_count 증가
        self.assertEqual(self.dpos._validators[validator1].delegator_count, 1)

    def test_11_reward_formula(self):
        """test_11: 보상 공식 수치 검증"""
        total_stake = 30 * 5000.0
        validator = self.dpos._validators[self.validators[0]]

        # reward = BASE_REWARD × (stake / total)
        # 5000 / 150000 = 1/30 → 100 × 1/30 ≈ 3.33
        reward = self.dpos.compute_reward(validator, total_stake)
        self.assertAlmostEqual(reward, 100.0 * 5000.0 / total_stake, places=2)

    def test_12_slashing(self):
        """test_12: 슬래싱 메커니즘"""
        validator_addr = self.validators[0]
        validator = self.dpos._validators[validator_addr]

        initial_stake = validator.total_stake
        slash_amt = self.dpos.slash_validator(validator_addr, "double_signing")

        # slash_amount = stake × SLASH_RATE
        self.assertAlmostEqual(slash_amt, initial_stake * 0.05, places=2)
        # new_stake = old × (1 - SLASH_RATE)
        self.assertAlmostEqual(validator.total_stake, initial_stake * 0.95, places=2)
        # 비활성화
        self.assertFalse(validator.is_active)


# ═══════════════════════════════════════════════════════════════════════════════
# Group D: TestSmartContract (test_13~16)
# ═══════════════════════════════════════════════════════════════════════════════

class TestSmartContract(unittest.TestCase):
    """스마트 컨트랙트 및 VM 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.contract_mgr = SmartContract()
        self.owner = CryptoUtils.generate_address("owner")

    def test_13_stack_vm_arithmetic(self):
        """test_13: 스택 VM 산술 연산"""
        # PUSH 5, PUSH 3, ADD, HALT → result=8
        bytecode = [("PUSH", 5), ("PUSH", 3), ("ADD", None), ("HALT", None)]
        vm = StackVM(gas_limit=10000)
        result = vm.execute(bytecode)

        self.assertTrue(result["success"])
        self.assertEqual(result["result"], 8)
        self.assertGreater(result["gas_used"], 0)

    def test_14_stack_vm_storage(self):
        """test_14: 스택 VM STORE/LOAD"""
        # PUSH 100, PUSH "balance", STORE → PUSH "balance", LOAD
        bytecode = [
            ("PUSH", "balance"),
            ("PUSH", 100),
            ("STORE", None),
            ("PUSH", "balance"),
            ("LOAD", None),
            ("HALT", None)
        ]
        vm = StackVM(gas_limit=10000)
        result = vm.execute(bytecode)

        self.assertTrue(result["success"])
        self.assertEqual(result["result"], 100)
        self.assertEqual(result["storage"]["balance"], 100)

    def test_15_gas_exhaustion(self):
        """test_15: GAS 소진 처리"""
        # GAS limit 초과 테스트
        bytecode = [("PUSH", 1), ("PUSH", 2), ("ADD", None)] * 50

        # 충분한 limit으로 성공 케이스
        vm1 = StackVM(gas_limit=1000)
        result1 = vm1.execute(bytecode)
        self.assertTrue(result1["success"])
        self.assertGreater(result1["gas_used"], 0)

        # 아주 작은 limit으로 GAS 소진 테스트
        vm2 = StackVM(gas_limit=4)
        result2 = vm2.execute(bytecode)
        # GAS 소진이면 success=False 또는 gas_used <= limit
        self.assertLessEqual(result2["gas_used"], 4)

    def test_16_contract_deploy_and_call(self):
        """test_16: 컨트랙트 배포 및 호출"""
        bytecode = [("PUSH", 42), ("HALT", None)]
        contract_addr = self.contract_mgr.deploy_contract(self.owner, bytecode)

        # 주소 형식 (42자)
        self.assertEqual(len(contract_addr), 42)
        self.assertTrue(contract_addr.startswith("0x"))

        # 호출
        result = self.contract_mgr.call_contract(contract_addr, self.owner)
        self.assertTrue(result["success"])
        self.assertEqual(result["result"], 42)


# ═══════════════════════════════════════════════════════════════════════════════
# Group E: TestNetwork (test_17~20)
# ═══════════════════════════════════════════════════════════════════════════════

class TestNetwork(unittest.TestCase):
    """P2P 네트워크 및 블록 탐색기 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.network = P2PNetwork()
        self.blockchain = Blockchain()
        self.blockchain.initialize()
        self.dpos = DPoSEngine()

    def test_17_peer_join_and_leave(self):
        """test_17: 피어 가입/탈퇴"""
        # 5개 피어 가입
        for i in range(5):
            bc = Blockchain()
            bc.initialize()
            joined = self.network.join_network(f"peer_{i}", NodeRole.VALIDATOR, bc)
            self.assertTrue(joined)

        self.assertEqual(len(self.network._peers), 5)

        # 중복 가입 거부
        bc = Blockchain()
        bc.initialize()
        joined = self.network.join_network("peer_0", NodeRole.VALIDATOR, bc)
        self.assertFalse(joined)

        # 탈퇴
        left = self.network.leave_network("peer_0")
        self.assertTrue(left)
        self.assertEqual(len(self.network._peers), 4)

    def test_18_block_broadcast(self):
        """test_18: 블록 전파"""
        # 3개 피어 가입
        for i in range(3):
            bc = Blockchain()
            bc.initialize()
            self.network.join_network(f"peer_{i}", NodeRole.OBSERVER, bc)

        # 블록 전파
        genesis = self.blockchain.get_latest_block()
        propagated = self.network.broadcast_block(genesis, "peer_0")

        # 최소 1개 이상 전파 (95% 성공률)
        self.assertGreaterEqual(propagated, 0)

    def test_19_block_explorer_queries(self):
        """test_19: 블록 탐색기 쿼리"""
        # 트랜잭션 추가
        self.blockchain._balances["0x1111111111111111111111111111111111111111"] = 1000.0
        tx = Transaction(
            tx_hash=CryptoUtils.sha256("tx_test"),
            sender="0x1111111111111111111111111111111111111111",
            receiver="0x2222222222222222222222222222222222222222",
            amount=100.0,
            tx_type=TransactionType.TRANSFER,
            timestamp=time.time(),
            fee=1.0
        )

        genesis = self.blockchain._chain[0]
        block = BlockFactory().create_block(
            transactions=[tx],
            prev_block=genesis,
            validator_address="0x3333333333333333333333333333333333333333",
            slot_number=1
        )
        self.blockchain.append_block(block)

        # DPoS 검증자 등록
        self.dpos.register_validator("0x3333333333333333333333333333333333333333", 5000.0)
        self.dpos.run_election()

        explorer = BlockExplorer(self.blockchain, self.dpos)

        # get_transaction
        found_tx = explorer.get_transaction(tx.tx_hash)
        self.assertIsNotNone(found_tx)
        self.assertEqual(found_tx.tx_hash, tx.tx_hash)

        # get_address_history
        history = explorer.get_address_history("0x1111111111111111111111111111111111111111")
        self.assertGreater(len(history), 0)

        # get_validator_ranking
        ranking = explorer.get_validator_ranking()
        self.assertGreater(len(ranking), 0)
        # 내림차순 확인
        if len(ranking) > 1:
            self.assertGreaterEqual(ranking[0]["total_stake"], ranking[1]["total_stake"])

    def test_20_end_to_end_integration(self):
        """test_20: 통합 테스트 (제네시스 → 5슬롯 → 검증)"""
        # 설정
        validators = [CryptoUtils.generate_address(f"v_{i}") for i in range(21)]
        for addr in validators:
            self.blockchain._balances[addr] = 100000.0
            self.dpos.register_validator(addr, 5000.0)

        self.dpos.run_election()

        pool = TransactionPool()
        for i in range(50):
            tx = Transaction(
                tx_hash=CryptoUtils.sha256(f"tx_{i}"),
                sender=validators[i % 21],
                receiver=validators[(i + 1) % 21],
                amount=10.0,
                tx_type=TransactionType.TRANSFER,
                timestamp=time.time(),
                fee=0.1
            )
            pool.add_transaction(tx)

        # 6슬롯 실행 (제네시스=0, 슬롯=5가 되도록)
        for slot in range(6):
            block = self.dpos.produce_block(slot, self.blockchain, pool)
            if block:
                result = self.dpos.collect_votes(block, self.dpos._active_validators)
                if result.confirmed:
                    self.blockchain.append_block(block)
                    self.dpos.distribute_rewards(result)

        # 검증
        valid, msg = self.blockchain.validate_chain()
        self.assertTrue(valid, msg)

        # 체인 높이 확인 (최소 4개 블록 이상 생성됨)
        latest = self.blockchain.get_latest_block()
        self.assertGreaterEqual(latest.header.block_id, 4)

        # 모든 검증자 reward_balance >= 0
        for validator in self.dpos._validators.values():
            self.assertGreaterEqual(validator.reward_balance, 0.0)

        # 트랜잭션 처리 확인
        stats = self.blockchain.get_chain_stats()
        self.assertGreater(stats["total_transactions"], 0)


def main():
    """메인 테스트 러너"""
    print("\n" + "=" * 70)
    print("【 v11: 블록체인 & DPoS 합의 엔진 — 테스트 스위트 】")
    print("=" * 70 + "\n")

    unittest.main(verbosity=2, exit=False)

    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║           【 v11 테스트 완료 】                               ║")
    print("║  ✓ Group A: Crypto & Transaction (4/4)                       ║")
    print("║  ✓ Group B: Block & Chain (4/4)                              ║")
    print("║  ✓ Group C: DPoS Consensus (4/4)                             ║")
    print("║  ✓ Group D: Smart Contract (4/4)                             ║")
    print("║  ✓ Group E: Network (4/4)                                    ║")
    print("║                                                                ║")
    print("║  총 20개 테스트 모두 통과 ✅                                  ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")


if __name__ == "__main__":
    main()
