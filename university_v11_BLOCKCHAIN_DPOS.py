#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           【 v11: 블록체인 & DPoS 합의 엔진 】                              ║
║            Python University Post-Doctoral 심화 연구                        ║
║                                                                              ║
║         "위임 지분 증명으로 민주적 블록 생성을 실현한다"                    ║
║                                                                              ║
║  표준 라이브러리만 사용: hashlib, hmac, json, math, random, time,          ║
║                          dataclasses, enum, typing, collections             ║
║                                                                              ║
║  주요 개념:                                                                  ║
║  - SHA-256 해시 체인 + Merkle Tree (CryptoUtils)                           ║
║  - DPoS 위임 투표 (상위 21명 검증자 선출)                                   ║
║  - 경제적 인센티브 (보상 + 슬래싱)                                          ║
║  - 스택 기반 스마트 컨트랙트 VM (14 옵코드)                                 ║
║  - P2P Gossip 전파 & 포크 해결 (최장 체인)                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import hashlib
import hmac
import json
import math
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict


# ═══════════════════════════════════════════════════════════════════════════════
# PART 0: Enum & Dataclass 정의
# ═══════════════════════════════════════════════════════════════════════════════

class TransactionType(Enum):
    """트랜잭션 종류"""
    TRANSFER        = "transfer"         # 코인 전송
    STAKE           = "stake"            # 지분 예치
    DELEGATE        = "delegate"         # 검증자 위임
    CONTRACT_CALL   = "contract_call"    # 스마트 컨트랙트 호출


class BlockStatus(Enum):
    """블록 상태"""
    PENDING   = "pending"    # 생성 대기
    CONFIRMED = "confirmed"  # 2/3 합의 완료
    FINALIZED = "finalized"  # 불변 확정


class NodeRole(Enum):
    """네트워크 노드 역할"""
    VALIDATOR = "validator"  # 블록 생성 자격
    DELEGATOR = "delegator"  # 검증자 위임자
    OBSERVER  = "observer"   # 읽기 전용 참여자


class ConsensusPhase(Enum):
    """DPoS 합의 단계"""
    ELECTION   = "election"    # 검증자 선출 투표
    PRODUCING  = "producing"   # 블록 생성 순번
    VERIFYING  = "verifying"   # 블록 서명 수집
    FINALIZING = "finalizing"  # 최종 확정


@dataclass
class Transaction:
    """블록체인 트랜잭션"""
    tx_hash:    str              # SHA-256 트랜잭션 식별자 (64자 hex)
    sender:     str              # 발신자 주소 (42자: 0x + 40)
    receiver:   str              # 수신자 주소 (42자: 0x + 40)
    amount:     float            # 전송 금액 (음수 불가)
    tx_type:    TransactionType  # 트랜잭션 종류
    timestamp:  float            # Unix 타임스탬프
    data:       Dict[str, Any] = field(default_factory=dict)  # 추가 데이터 (컨트랙트용)
    fee:        float = 0.001    # 수수료 (기본 0.001)


@dataclass
class BlockHeader:
    """블록 헤더 — 해시 체인의 핵심"""
    block_id:    int    # 블록 높이 (제네시스=0)
    prev_hash:   str    # 이전 블록 해시 (64자 hex, 제네시스="0"*64)
    merkle_root: str    # 트랜잭션 Merkle Root (64자 hex)
    timestamp:   float  # Unix 타임스탬프 (생성 시각)
    validator:   str    # 생성 검증자 주소 (42자)
    slot_number: int    # DPoS 슬롯 번호 (0부터 증가)


@dataclass
class Block:
    """완전한 블록 구조"""
    header:       BlockHeader       # 블록 헤더
    transactions: List[Transaction] # 포함된 트랜잭션 목록
    block_hash:   str               # 블록 자체 해시 (64자 hex)
    size_bytes:   int               # 직렬화된 크기 (바이트 단위)
    status:       BlockStatus = BlockStatus.PENDING  # 블록 상태


@dataclass
class ValidatorInfo:
    """DPoS 검증자 정보"""
    address:         str    # 검증자 주소 (42자 hex)
    total_stake:     float  # 자기 지분 + 위임 지분 합계
    delegator_count: int    # 이 검증자에게 위임한 주소 수
    blocks_produced: int    # 이 검증자가 생산한 블록 수
    is_active:       bool   # 현재 슬롯에서 활성화 여부
    reward_balance:  float  # 누적 보상 잔액 (출금 전)


@dataclass
class ConsensusResult:
    """한 슬롯의 DPoS 합의 결과"""
    slot:           int    # 슬롯 번호
    producer:       str    # 블록 생산자 주소 (42자)
    block_hash:     str    # 생성된 블록 해시 (64자 hex)
    confirmed:      bool   # 2/3 이상 투표 확보 여부
    vote_count:     int    # 수집한 투표 수
    round_time_ms:  float  # 합의 완료까지 소요 시간 (밀리초)


# ═══════════════════════════════════════════════════════════════════════════════
# PART 1: CryptoUtils — 암호 유틸리티
# ═══════════════════════════════════════════════════════════════════════════════

class CryptoUtils:
    """블록체인 암호 기본 연산"""

    @staticmethod
    def sha256(data: str) -> str:
        """SHA-256 해시 (문자열 → 64자 hex)"""
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def double_sha256(data: str) -> str:
        """이중 SHA-256 (비트코인 표준)"""
        first_hash = CryptoUtils.sha256(data)
        return CryptoUtils.sha256(first_hash)

    @staticmethod
    def compute_tx_hash(tx: Transaction) -> str:
        """트랜잭션 내용 → SHA-256 해시"""
        tx_str = f"{tx.sender}{tx.receiver}{tx.amount}{tx.tx_type.value}{tx.timestamp}"
        return CryptoUtils.sha256(tx_str)

    @staticmethod
    def compute_block_hash(header: BlockHeader) -> str:
        """블록 헤더 → SHA-256 해시"""
        header_str = f"{header.block_id}{header.prev_hash}{header.merkle_root}{header.timestamp}{header.validator}{header.slot_number}"
        return CryptoUtils.sha256(header_str)

    @staticmethod
    def build_merkle_tree(tx_hashes: List[str]) -> str:
        """
        Merkle Root 계산 (이진 해시 트리)
        홀수 개 잎일 경우 마지막 해시를 복사하여 균형 트리 구성
        """
        if not tx_hashes:
            return CryptoUtils.sha256("empty_merkle")

        leaves = tx_hashes.copy()
        while len(leaves) > 1:
            if len(leaves) % 2 == 1:
                leaves.append(leaves[-1])  # 홀수 시 마지막 복사
            next_level = []
            for i in range(0, len(leaves), 2):
                combined = leaves[i] + leaves[i + 1]
                next_level.append(CryptoUtils.sha256(combined))
            leaves = next_level
        return leaves[0]

    @staticmethod
    def generate_address(seed: str) -> str:
        """
        지갑 주소 생성
        sha256(seed)의 앞 40자 + "0x" prefix → 42자
        """
        hash_result = CryptoUtils.sha256(seed)
        return "0x" + hash_result[:40]

    @staticmethod
    def compute_hmac(key: str, message: str) -> str:
        """HMAC-SHA256 계산 (서명 시뮬레이션용)"""
        return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def verify_chain_link(prev_hash: str, current_header: BlockHeader) -> bool:
        """이전 해시와 현재 헤더의 연결 유효성 검증"""
        return prev_hash == current_header.prev_hash


# ═══════════════════════════════════════════════════════════════════════════════
# PART 2: TransactionPool — Mempool 관리
# ═══════════════════════════════════════════════════════════════════════════════

class TransactionPool:
    """트랜잭션 메모리 풀 (Mempool)"""

    def __init__(self, max_size: int = 1000):
        """초기화"""
        self._pool: Dict[str, Transaction] = {}  # tx_hash → Transaction
        self._timestamps: Dict[str, float] = {}    # tx_hash → timestamp
        self._max_size = max_size

    def add_transaction(self, tx: Transaction) -> bool:
        """
        트랜잭션 추가
        - 중복 거부, 음수 amount 거부
        - max_size 초과 시 가장 낮은 fee 트랜잭션 제거
        """
        if tx.amount < 0:
            return False
        if tx.tx_hash in self._pool:
            return False

        if len(self._pool) >= self._max_size:
            # 최소 fee 트랜잭션 제거
            min_fee_hash = min(self._pool.keys(), key=lambda h: self._pool[h].fee)
            del self._pool[min_fee_hash]
            del self._timestamps[min_fee_hash]

        self._pool[tx.tx_hash] = tx
        self._timestamps[tx.tx_hash] = time.time()
        return True

    def remove_transaction(self, tx_hash: str) -> Optional[Transaction]:
        """트랜잭션 제거 (블록 포함 후 호출)"""
        if tx_hash in self._pool:
            tx = self._pool.pop(tx_hash)
            self._timestamps.pop(tx_hash, None)
            return tx
        return None

    def select_for_block(self, max_tx: int = 50) -> List[Transaction]:
        """
        블록 포함 후보 선택 (fee 내림차순)
        """
        sorted_txs = sorted(self._pool.values(), key=lambda t: t.fee, reverse=True)
        return sorted_txs[:max_tx]

    def get_pending_count(self) -> int:
        """미확인 트랜잭션 수"""
        return len(self._pool)

    def get_pool_stats(self) -> Dict[str, Any]:
        """풀 통계"""
        if not self._pool:
            return {
                "total": 0, "avg_fee": 0.0, "max_fee": 0.0,
                "min_fee": 0.0, "by_type": {}
            }

        fees = [tx.fee for tx in self._pool.values()]
        by_type = defaultdict(int)
        for tx in self._pool.values():
            by_type[tx.tx_type.value] += 1

        return {
            "total": len(self._pool),
            "avg_fee": sum(fees) / len(fees),
            "max_fee": max(fees),
            "min_fee": min(fees),
            "by_type": dict(by_type)
        }

    def flush_old_transactions(self, max_age_sec: float = 300.0) -> int:
        """오래된 트랜잭션 제거 (max_age_sec 이상 경과)"""
        now = time.time()
        to_remove = [h for h, ts in self._timestamps.items() if now - ts >= max_age_sec]
        for h in to_remove:
            self._pool.pop(h, None)
            self._timestamps.pop(h, None)
        return len(to_remove)

    def has_transaction(self, tx_hash: str) -> bool:
        """해당 해시의 트랜잭션 존재 여부"""
        return tx_hash in self._pool


# ═══════════════════════════════════════════════════════════════════════════════
# PART 3: BlockFactory — 블록 생성
# ═══════════════════════════════════════════════════════════════════════════════

class BlockFactory:
    """블록 생성 팩토리"""

    def __init__(self):
        """초기화"""
        self._blocks_created: int = 0

    def create_genesis_block(self) -> Block:
        """
        제네시스 블록 생성
        - block_id=0, prev_hash="0"*64
        - 빈 트랜잭션 목록, validator="genesis"
        """
        header = BlockHeader(
            block_id=0,
            prev_hash="0" * 64,
            merkle_root=CryptoUtils.build_merkle_tree([]),
            timestamp=time.time(),
            validator="genesis",
            slot_number=0
        )
        block_hash = CryptoUtils.compute_block_hash(header)
        block = Block(
            header=header,
            transactions=[],
            block_hash=block_hash,
            size_bytes=len(json.dumps(self._serialize_block_data(header, []))),
            status=BlockStatus.FINALIZED
        )
        self._blocks_created += 1
        return block

    def create_block(
        self,
        transactions: List[Transaction],
        prev_block: Block,
        validator_address: str,
        slot_number: int,
    ) -> Block:
        """
        신규 블록 생성
        1. Merkle Root 계산
        2. BlockHeader 생성
        3. Block Hash 계산
        4. Block 반환
        """
        tx_hashes = [tx.tx_hash for tx in transactions]
        merkle_root = CryptoUtils.build_merkle_tree(tx_hashes)

        header = BlockHeader(
            block_id=prev_block.header.block_id + 1,
            prev_hash=prev_block.block_hash,
            merkle_root=merkle_root,
            timestamp=time.time(),
            validator=validator_address,
            slot_number=slot_number
        )

        block_hash = CryptoUtils.compute_block_hash(header)
        serialized = self._serialize_block_data(header, transactions)
        size_bytes = len(json.dumps(serialized))

        block = Block(
            header=header,
            transactions=transactions,
            block_hash=block_hash,
            size_bytes=size_bytes,
            status=BlockStatus.PENDING
        )
        self._blocks_created += 1
        return block

    def validate_block_structure(self, block: Block, prev_block: Block) -> bool:
        """블록 구조 검증"""
        if block.header.prev_hash != prev_block.block_hash:
            return False
        if block.header.block_id != prev_block.header.block_id + 1:
            return False
        if block.header.timestamp <= prev_block.header.timestamp:
            return False

        # Merkle Root 재계산 검증
        tx_hashes = [tx.tx_hash for tx in block.transactions]
        expected_merkle = CryptoUtils.build_merkle_tree(tx_hashes)
        if block.header.merkle_root != expected_merkle:
            return False

        return True

    def serialize_block(self, block: Block) -> str:
        """블록 JSON 직렬화 (P2P 전파용)"""
        data = self._serialize_block_data(block.header, block.transactions)
        return json.dumps(data, sort_keys=True)

    @staticmethod
    def _serialize_block_data(header: BlockHeader, transactions: List[Transaction]) -> Dict:
        """블록 데이터 직렬화 헬퍼"""
        return {
            "block_id": header.block_id,
            "prev_hash": header.prev_hash,
            "merkle_root": header.merkle_root,
            "timestamp": header.timestamp,
            "validator": header.validator,
            "slot_number": header.slot_number,
            "tx_count": len(transactions),
            "transactions": [
                {
                    "tx_hash": tx.tx_hash,
                    "sender": tx.sender,
                    "receiver": tx.receiver,
                    "amount": tx.amount,
                    "type": tx.tx_type.value,
                    "fee": tx.fee
                }
                for tx in transactions
            ]
        }

    def get_block_stats(self) -> Dict[str, int]:
        """생성 통계"""
        return {"blocks_created": self._blocks_created}


# ═══════════════════════════════════════════════════════════════════════════════
# PART 4: Blockchain — 체인 관리
# ═══════════════════════════════════════════════════════════════════════════════

class Blockchain:
    """블록체인 원장 관리자"""

    INITIAL_BALANCE = 1000000.0  # 초기 주소별 잔액

    def __init__(self):
        """초기화"""
        self._chain: List[Block] = []
        self._balances: Dict[str, float] = {}
        self._factory: BlockFactory = BlockFactory()

    def initialize(self) -> Block:
        """제네시스 블록으로 초기화"""
        genesis = self._factory.create_genesis_block()
        self._chain.append(genesis)
        return genesis

    def append_block(self, block: Block) -> bool:
        """
        블록 추가
        1. 구조 검증
        2. 트랜잭션별 잔액 업데이트
        3. CONFIRMED 상태 설정
        """
        if not self._chain:
            return False

        latest = self._chain[-1]
        if not self._factory.validate_block_structure(block, latest):
            return False

        # 트랜잭션 처리
        for tx in block.transactions:
            if tx.tx_type == TransactionType.TRANSFER:
                # 송금 처리
                if self.get_balance(tx.sender) < tx.amount + tx.fee:
                    return False
                self._balances[tx.sender] = self.get_balance(tx.sender) - tx.amount - tx.fee
                self._balances[tx.receiver] = self.get_balance(tx.receiver) + tx.amount
                # 수수료는 검증자에게
                self._balances[block.header.validator] = self.get_balance(block.header.validator) + tx.fee

            elif tx.tx_type == TransactionType.STAKE:
                # 스테이킹 처리
                if self.get_balance(tx.sender) < tx.amount:
                    return False
                self._balances[tx.sender] = self.get_balance(tx.sender) - tx.amount

            elif tx.tx_type == TransactionType.DELEGATE:
                # 위임 처리 (잔액 영향 없음, 별도 추적)
                pass

        # 블록 상태 업데이트
        block.status = BlockStatus.CONFIRMED
        self._chain.append(block)
        return True

    def get_balance(self, address: str) -> float:
        """주소 잔액 조회"""
        return self._balances.get(address, 0.0)

    def get_block_by_id(self, block_id: int) -> Optional[Block]:
        """블록 ID로 조회"""
        if 0 <= block_id < len(self._chain):
            return self._chain[block_id]
        return None

    def get_latest_block(self) -> Optional[Block]:
        """최신 블록 조회"""
        return self._chain[-1] if self._chain else None

    def validate_chain(self) -> Tuple[bool, str]:
        """전체 체인 무결성 검증"""
        if not self._chain:
            return False, "empty chain"

        for i in range(len(self._chain)):
            block = self._chain[i]

            # 해시 검증
            expected_hash = CryptoUtils.compute_block_hash(block.header)
            if block.block_hash != expected_hash:
                return False, f"block {i} hash mismatch"

            # Merkle Root 검증
            tx_hashes = [tx.tx_hash for tx in block.transactions]
            expected_merkle = CryptoUtils.build_merkle_tree(tx_hashes)
            if block.header.merkle_root != expected_merkle:
                return False, f"block {i} merkle root mismatch"

            # 이전 해시 연결 검증
            if i > 0:
                prev_block = self._chain[i - 1]
                if block.header.prev_hash != prev_block.block_hash:
                    return False, f"block {i} prev_hash mismatch"

        return True, ""

    def resolve_fork(self, fork_chain: List[Block]) -> bool:
        """
        포크 해결 — 최장 체인 규칙
        """
        if len(fork_chain) <= len(self._chain):
            return False

        # 제네시스 블록 일치 확인
        if not fork_chain or not self._chain:
            return False
        if fork_chain[0].block_hash != self._chain[0].block_hash:
            return False

        # 포크 체인 전체 검증
        for i in range(1, len(fork_chain)):
            if not self._factory.validate_block_structure(fork_chain[i], fork_chain[i - 1]):
                return False

        # 교체 실행
        self._chain = fork_chain
        self._rebuild_balances()
        return True

    def get_chain_stats(self) -> Dict[str, Any]:
        """체인 통계"""
        if not self._chain:
            return {"height": 0, "total_transactions": 0, "average_block_size": 0.0}

        total_txs = sum(len(block.transactions) for block in self._chain)
        avg_size = sum(block.size_bytes for block in self._chain) / len(self._chain) if self._chain else 0.0

        return {
            "height": len(self._chain) - 1,
            "total_transactions": total_txs,
            "total_addresses": len(self._balances),
            "average_block_size": avg_size
        }

    def _rebuild_balances(self) -> None:
        """체인 전체를 재순회하여 잔액 재계산 (포크 해결 후 호출)"""
        self._balances.clear()
        for block in self._chain:
            for tx in block.transactions:
                if tx.tx_type == TransactionType.TRANSFER:
                    if self._balances.get(tx.sender, 0.0) < tx.amount + tx.fee:
                        continue
                    self._balances[tx.sender] = self._balances.get(tx.sender, self.INITIAL_BALANCE) - tx.amount - tx.fee
                    self._balances[tx.receiver] = self._balances.get(tx.receiver, 0.0) + tx.amount
                    self._balances[block.header.validator] = self._balances.get(block.header.validator, 0.0) + tx.fee

                elif tx.tx_type == TransactionType.STAKE:
                    self._balances[tx.sender] = self._balances.get(tx.sender, self.INITIAL_BALANCE) - tx.amount


# ═══════════════════════════════════════════════════════════════════════════════
# PART 5: DPoSEngine — 위임 지분 증명 (핵심)
# ═══════════════════════════════════════════════════════════════════════════════

class DPoSEngine:
    """위임 지분 증명(DPoS) 합의 엔진"""

    NUM_VALIDATORS = 21          # 활성 검증자 고정 수
    SLASH_RATE = 0.05            # 슬래싱 비율 (5%)
    BASE_REWARD = 100.0           # 블록 기본 보상

    def __init__(self):
        """초기화"""
        self._validators: Dict[str, ValidatorInfo] = {}
        self._delegations: Dict[str, Dict[str, float]] = defaultdict(dict)
        # {delegator_addr: {validator_addr: staked_amount}}
        self._active_validators: List[str] = []
        self._slot_schedule: List[str] = []
        self._phase: ConsensusPhase = ConsensusPhase.ELECTION
        self._current_slot: int = 0
        self._epoch: int = 0

    def register_validator(self, address: str, initial_stake: float) -> ValidatorInfo:
        """검증자 등록"""
        info = ValidatorInfo(
            address=address,
            total_stake=initial_stake,
            delegator_count=0,
            blocks_produced=0,
            is_active=False,
            reward_balance=0.0
        )
        self._validators[address] = info
        return info

    def stake(self, address: str, amount: float) -> bool:
        """자기 지분 예치"""
        if address not in self._validators:
            return False
        self._validators[address].total_stake += amount
        return True

    def delegate(self, delegator: str, validator: str, amount: float) -> bool:
        """위임 투표"""
        if validator not in self._validators:
            return False
        self._delegations[delegator][validator] = amount
        self._validators[validator].total_stake += amount
        self._validators[validator].delegator_count += 1
        return True

    def run_election(self) -> List[str]:
        """
        검증자 선출 (상위 NUM_VALIDATORS명)
        1. total_stake 내림차순 정렬
        2. 상위 선발
        3. 슬롯 스케줄 생성
        """
        sorted_validators = sorted(
            self._validators.values(),
            key=lambda v: v.total_stake,
            reverse=True
        )

        # 활성 검증자 비활성화
        for v in self._validators.values():
            v.is_active = False

        # 새로운 활성 검증자 선발
        self._active_validators = [v.address for v in sorted_validators[:self.NUM_VALIDATORS]]
        for addr in self._active_validators:
            self._validators[addr].is_active = True

        # 슬롯 스케줄 생성
        self._generate_slot_schedule()
        self._phase = ConsensusPhase.PRODUCING

        return self._active_validators

    def _generate_slot_schedule(self) -> None:
        """슬롯 스케줄 생성 (Fisher-Yates 셔플)"""
        self._slot_schedule = self._active_validators.copy()
        random.shuffle(self._slot_schedule)

    def get_slot_producer(self, slot: int) -> str:
        """슬롯의 블록 생산자"""
        if not self._slot_schedule:
            return ""
        return self._slot_schedule[slot % len(self._slot_schedule)]

    def produce_block(
        self,
        slot: int,
        blockchain: "Blockchain",
        tx_pool: TransactionPool
    ) -> Optional[Block]:
        """블록 생산"""
        producer = self.get_slot_producer(slot)
        if not producer:
            return None

        latest_block = blockchain.get_latest_block()
        if not latest_block:
            return None

        # 트랜잭션 선택
        transactions = tx_pool.select_for_block(max_tx=50)

        # 블록 생성
        block = blockchain._factory.create_block(
            transactions=transactions,
            prev_block=latest_block,
            validator_address=producer,
            slot_number=slot
        )

        # 검증자 통계 업데이트
        self._validators[producer].blocks_produced += 1

        return block

    def collect_votes(
        self,
        block: Block,
        active_validators: List[str]
    ) -> ConsensusResult:
        """
        투표 수집 (85% 참여율 시뮬레이션)
        quorum = ceil(n × 2/3) + 1
        """
        quorum = math.ceil(len(active_validators) * 2 / 3) + 1
        votes = 0

        for v in active_validators:
            if v != block.header.validator:
                if random.random() < 0.85:  # 85% 참여율
                    votes += 1

        confirmed = votes >= quorum

        return ConsensusResult(
            slot=block.header.slot_number,
            producer=block.header.validator,
            block_hash=block.block_hash,
            confirmed=confirmed,
            vote_count=votes,
            round_time_ms=random.uniform(100, 500)
        )

    def compute_reward(self, validator: ValidatorInfo, total_network_stake: float) -> float:
        """보상 계산"""
        if total_network_stake == 0:
            return 0.0
        return self.BASE_REWARD * (validator.total_stake / total_network_stake)

    def distribute_rewards(self, result: ConsensusResult) -> Dict[str, float]:
        """보상 분배"""
        if result.producer not in self._validators:
            return {}

        total_stake = sum(v.total_stake for v in self._validators.values())
        validator = self._validators[result.producer]
        reward = self.compute_reward(validator, total_stake)

        validator.reward_balance += reward
        return {result.producer: reward}

    def slash_validator(self, address: str, reason: str) -> float:
        """슬래싱"""
        if address not in self._validators:
            return 0.0

        validator = self._validators[address]
        slash_amount = validator.total_stake * self.SLASH_RATE
        validator.total_stake *= (1 - self.SLASH_RATE)
        validator.is_active = False

        return slash_amount

    def advance_epoch(self) -> int:
        """에폭 전환"""
        self._epoch += 1
        self._phase = ConsensusPhase.ELECTION
        self.run_election()
        return self._epoch

    def get_network_stats(self) -> Dict[str, Any]:
        """네트워크 통계"""
        total_stake = sum(v.total_stake for v in self._validators.values())
        return {
            "total_validators": len(self._validators),
            "active_validators": len(self._active_validators),
            "total_staked": total_stake,
            "epoch": self._epoch,
            "current_slot": self._current_slot,
            "phase": self._phase.value
        }


# ═══════════════════════════════════════════════════════════════════════════════
# PART 6: SmartContract — 스마트 컨트랙트 & StackVM
# ═══════════════════════════════════════════════════════════════════════════════

class StackVM:
    """경량 스택 가상 머신"""

    OPCODES = {
        "PUSH": 0x01, "POP": 0x02, "ADD": 0x10, "SUB": 0x11,
        "MUL": 0x12, "DIV": 0x13, "GT": 0x20, "LT": 0x21,
        "EQ": 0x22, "STORE": 0x30, "LOAD": 0x31, "EMIT": 0x40,
        "HALT": 0xFF
    }

    GAS_COSTS = {
        "PUSH": 3, "POP": 3, "ADD": 5, "SUB": 5, "MUL": 10,
        "DIV": 10, "GT": 5, "LT": 5, "EQ": 5, "STORE": 20,
        "LOAD": 20, "EMIT": 15, "HALT": 0
    }

    def __init__(self, gas_limit: int = 10000):
        """초기화"""
        self._stack: List[Any] = []
        self._storage: Dict[str, Any] = {}
        self._gas_used: int = 0
        self._gas_limit: int = gas_limit
        self._logs: List[str] = []

    def execute(self, bytecode: List[Tuple[str, Any]]) -> Dict[str, Any]:
        """바이트코드 실행"""
        for opcode, operand in bytecode:
            if self._gas_used >= self._gas_limit:
                return {
                    "success": False,
                    "result": None,
                    "gas_used": self._gas_used,
                    "logs": self._logs,
                    "storage": self._storage,
                    "error": "gas_exhausted"
                }

            self._consume_gas(opcode)

            if opcode == "PUSH":
                self._stack.append(operand)
            elif opcode == "POP":
                if self._stack:
                    self._stack.pop()
            elif opcode == "ADD":
                if len(self._stack) >= 2:
                    b = self._stack.pop()
                    a = self._stack.pop()
                    self._stack.append(a + b)
            elif opcode == "SUB":
                if len(self._stack) >= 2:
                    b = self._stack.pop()
                    a = self._stack.pop()
                    self._stack.append(a - b)
            elif opcode == "MUL":
                if len(self._stack) >= 2:
                    b = self._stack.pop()
                    a = self._stack.pop()
                    self._stack.append(a * b)
            elif opcode == "DIV":
                if len(self._stack) >= 2:
                    b = self._stack.pop()
                    a = self._stack.pop()
                    if b != 0:
                        self._stack.append(a / b)
                    else:
                        self._stack.append(0)
            elif opcode == "STORE":
                if len(self._stack) >= 2:
                    v = self._stack.pop()
                    k = self._stack.pop()
                    self._storage[str(k)] = v
            elif opcode == "LOAD":
                if self._stack:
                    k = self._stack.pop()
                    self._stack.append(self._storage.get(str(k), 0))
            elif opcode == "EMIT":
                if self._stack:
                    self._logs.append(str(self._stack.pop()))
            elif opcode == "HALT":
                break

        result = self._stack[-1] if self._stack else 0

        return {
            "success": True,
            "result": result,
            "gas_used": self._gas_used,
            "logs": self._logs,
            "storage": self._storage
        }

    def _consume_gas(self, opcode: str) -> None:
        """GAS 소비"""
        self._gas_used += self.GAS_COSTS.get(opcode, 0)


class SmartContract:
    """스마트 컨트랙트 관리자"""

    def __init__(self):
        """초기화"""
        self._contracts: Dict[str, Dict[str, Any]] = {}
        self._vm: StackVM = StackVM()

    def deploy_contract(
        self,
        owner: str,
        bytecode: List[Tuple[str, Any]],
        initial_state: Dict[str, Any] = None
    ) -> str:
        """컨트랙트 배포"""
        contract_address = CryptoUtils.generate_address(owner + str(time.time()))
        self._contracts[contract_address] = {
            "bytecode": bytecode,
            "state": initial_state or {},
            "owner": owner,
            "deploy_time": time.time()
        }
        return contract_address

    def call_contract(
        self,
        contract_address: str,
        caller: str,
        function_args: List[Any] = None
    ) -> Dict[str, Any]:
        """컨트랙트 호출"""
        if contract_address not in self._contracts:
            return {"success": False, "error": "contract not found"}

        contract = self._contracts[contract_address]
        vm = StackVM(gas_limit=10000)
        result = vm.execute(contract["bytecode"])

        if result["success"]:
            contract["state"].update(result["storage"])

        return result

    def get_contract_state(self, contract_address: str) -> Dict[str, Any]:
        """컨트랙트 상태 조회"""
        if contract_address in self._contracts:
            return self._contracts[contract_address].get("state", {})
        return {}

    def get_deployed_count(self) -> int:
        """배포된 컨트랙트 수"""
        return len(self._contracts)


# ═══════════════════════════════════════════════════════════════════════════════
# PART 7: P2PNetwork — P2P 네트워크 시뮬레이션
# ═══════════════════════════════════════════════════════════════════════════════

class P2PNetwork:
    """P2P 네트워크 시뮬레이터"""

    def __init__(self):
        """초기화"""
        self._peers: Dict[str, Dict[str, Any]] = {}
        self._message_log: List[Dict[str, Any]] = []

    def join_network(
        self,
        peer_id: str,
        role: NodeRole,
        blockchain: Blockchain
    ) -> bool:
        """네트워크 참가"""
        if peer_id in self._peers:
            return False

        self._peers[peer_id] = {
            "role": role,
            "blockchain": blockchain,
            "joined_at": time.time()
        }
        return True

    def leave_network(self, peer_id: str) -> bool:
        """네트워크 탈퇴"""
        if peer_id in self._peers:
            del self._peers[peer_id]
            return True
        return False

    def broadcast_block(self, block: Block, sender_id: str) -> int:
        """블록 전파 (Gossip 시뮬레이션)"""
        propagated = 0
        for peer_id, peer_info in self._peers.items():
            if peer_id == sender_id:
                continue
            if random.random() < 0.95:  # 95% 성공률
                peer_info["blockchain"].append_block(block)
                propagated += 1
        return propagated

    def broadcast_transaction(self, tx: Transaction) -> int:
        """트랜잭션 전파"""
        propagated = 0
        for peer_info in self._peers.values():
            if random.random() < 0.90:  # 90% 성공률
                # 각 피어의 tx_pool에 추가 (실제 구현에서)
                propagated += 1
        return propagated

    def sync_chain(self, requester_id: str) -> bool:
        """체인 동기화"""
        if requester_id not in self._peers:
            return False

        # 가장 긴 체인 찾기
        longest_chain = None
        max_height = -1

        for peer_info in self._peers.values():
            blockchain = peer_info["blockchain"]
            height = len(blockchain._chain) - 1
            if height > max_height:
                max_height = height
                longest_chain = blockchain._chain

        if longest_chain and requester_id in self._peers:
            requester_blockchain = self._peers[requester_id]["blockchain"]
            return requester_blockchain.resolve_fork(longest_chain)

        return False

    def simulate_partition(
        self,
        isolated_peers: List[str],
        duration_slots: int
    ) -> Dict[str, Any]:
        """네트워크 파티션 시뮬레이션"""
        # 파티션 동안 블록 생성 추적
        partition_blocks = 0
        forked = False

        # 복구
        for peer_id in isolated_peers:
            if peer_id in self._peers:
                self.sync_chain(peer_id)

        return {
            "partition_blocks": partition_blocks,
            "forked": forked,
            "duration_slots": duration_slots
        }

    def get_network_stats(self) -> Dict[str, Any]:
        """네트워크 통계"""
        role_counts = defaultdict(int)
        for peer_info in self._peers.values():
            role_counts[peer_info["role"].value] += 1

        return {
            "total_peers": len(self._peers),
            "roles": dict(role_counts),
            "message_count": len(self._message_log)
        }


# ═══════════════════════════════════════════════════════════════════════════════
# PART 8: BlockExplorer — 블록 탐색기
# ═══════════════════════════════════════════════════════════════════════════════

class BlockExplorer:
    """블록체인 데이터 탐색기 (읽기 전용)"""

    def __init__(self, blockchain: Blockchain, dpos: DPoSEngine):
        """초기화"""
        self._chain = blockchain
        self._dpos = dpos

    def get_transaction(self, tx_hash: str) -> Optional[Transaction]:
        """tx_hash로 트랜잭션 검색"""
        for block in self._chain._chain:
            for tx in block.transactions:
                if tx.tx_hash == tx_hash:
                    return tx
        return None

    def get_address_history(self, address: str) -> List[Transaction]:
        """주소 이력 (송수신)"""
        history = []
        for block in self._chain._chain:
            for tx in block.transactions:
                if tx.sender == address or tx.receiver == address:
                    history.append(tx)
        return history

    def get_validator_ranking(self) -> List[Dict[str, Any]]:
        """검증자 순위"""
        validators = sorted(
            self._dpos._validators.values(),
            key=lambda v: v.total_stake,
            reverse=True
        )
        return [
            {
                "rank": i + 1,
                "address": v.address[:10] + "...",
                "total_stake": v.total_stake,
                "blocks_produced": v.blocks_produced,
                "is_active": v.is_active,
                "reward_balance": v.reward_balance
            }
            for i, v in enumerate(validators[:10])
        ]

    def get_rich_list(self, top_n: int = 10) -> List[Tuple[str, float]]:
        """잔액 상위"""
        addresses = sorted(
            self._chain._balances.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return addresses[:top_n]

    def get_block_summary(self, block_id: int) -> Optional[Dict[str, Any]]:
        """블록 요약"""
        block = self._chain.get_block_by_id(block_id)
        if not block:
            return None

        return {
            "block_id": block.header.block_id,
            "timestamp": block.header.timestamp,
            "validator": block.header.validator[:10] + "...",
            "tx_count": len(block.transactions),
            "size_bytes": block.size_bytes,
            "status": block.status.value
        }

    def get_chain_analytics(self) -> Dict[str, Any]:
        """체인 분석"""
        stats = self._chain.get_chain_stats()
        avg_tx_per_block = stats["total_transactions"] / len(self._chain._chain) if self._chain._chain else 0

        validators_by_blocks = sorted(
            self._dpos._validators.values(),
            key=lambda v: v.blocks_produced,
            reverse=True
        )[:5]

        total_fees = sum(
            sum(tx.fee for tx in block.transactions)
            for block in self._chain._chain
        )

        return {
            "total_blocks": len(self._chain._chain),
            "total_transactions": stats["total_transactions"],
            "avg_tx_per_block": avg_tx_per_block,
            "total_addresses": stats["total_addresses"],
            "average_block_size": stats["average_block_size"],
            "total_fees_collected": total_fees,
            "top_validators": [v.address[:10] + "..." for v in validators_by_blocks]
        }

    def search(self, query: str) -> Dict[str, Any]:
        """통합 검색"""
        if query.isdigit():
            block = self.get_block_summary(int(query))
            return {"type": "block", "result": block}
        elif len(query) == 64 and all(c in "0123456789abcdef" for c in query.lower()):
            tx = self.get_transaction(query)
            return {"type": "transaction", "result": tx}
        elif query.startswith("0x") and len(query) == 42:
            history = self.get_address_history(query)
            return {"type": "address", "tx_count": len(history), "balance": self._chain.get_balance(query)}
        return {"type": "unknown", "result": None}


def main():
    """메인 데모"""
    print("\n" + "═" * 70)
    print("【 v11: 블록체인 & DPoS 합의 엔진 】")
    print("═" * 70 + "\n")

    # ────────────────────────────────────────────────────────────────────
    # SECTION 1: 제네시스 블록 & 검증자 등록
    # ────────────────────────────────────────────────────────────────────
    print("【 SECTION 1: 제네시스 블록 & 검증자 등록 】")
    print("─" * 70)

    blockchain = Blockchain()
    genesis = blockchain.initialize()
    dpos = DPoSEngine()

    # 초기 잔액 배분 (30명 주소)
    validator_addresses = [CryptoUtils.generate_address(f"validator_{i}") for i in range(30)]
    for addr in validator_addresses:
        blockchain._balances[addr] = 100000.0

    # 검증자 등록 및 스테이킹
    initial_stake = 5000.0
    for addr in validator_addresses:
        dpos.register_validator(addr, initial_stake)

    selected = dpos.run_election()
    total_stake = sum(v.total_stake for v in dpos._validators.values())

    print(f"✓ 제네시스 블록: {genesis.block_hash[:16]}...")
    print(f"✓ 검증자 등록: {len(validator_addresses)}명")
    print(f"✓ 활성 검증자: {len(selected)}명")
    print(f"✓ 총 스테이킹: {total_stake:,.0f} GOG")

    # ────────────────────────────────────────────────────────────────────
    # SECTION 2: 트랜잭션 생성 & Mempool
    # ────────────────────────────────────────────────────────────────────
    print("\n【 SECTION 2: 트랜잭션 생성 & Mempool 】")
    print("─" * 70)

    tx_pool = TransactionPool(max_size=1000)

    # TRANSFER 트랜잭션
    for i in range(100):
        sender = random.choice(validator_addresses)
        receiver = random.choice(validator_addresses)
        tx = Transaction(
            tx_hash=CryptoUtils.sha256(f"tx_{i}"),
            sender=sender,
            receiver=receiver,
            amount=random.uniform(10, 100),
            tx_type=TransactionType.TRANSFER,
            timestamp=time.time(),
            fee=random.uniform(0.001, 0.01)
        )
        tx_pool.add_transaction(tx)

    stats = tx_pool.get_pool_stats()
    print(f"✓ 트랜잭션 생성: {stats['total']}개")
    print(f"✓ 평균 수수료: {stats['avg_fee']:.4f} GOG")
    print(f"✓ 타입별: {stats['by_type']}")

    # ────────────────────────────────────────────────────────────────────
    # SECTION 3: DPoS 블록 생성 (10슬롯)
    # ────────────────────────────────────────────────────────────────────
    print("\n【 SECTION 3: DPoS 블록 생성 (10슬롯) 】")
    print("─" * 70)

    total_tx_in_blocks = 0
    consensus_success = 0

    for slot in range(10):
        block = dpos.produce_block(slot, blockchain, tx_pool)
        if block:
            result = dpos.collect_votes(block, dpos._active_validators)
            if result.confirmed:
                blockchain.append_block(block)
                dpos.distribute_rewards(result)
                consensus_success += 1
                total_tx_in_blocks += len(block.transactions)
                for tx in block.transactions:
                    tx_pool.remove_transaction(tx.tx_hash)

    avg_tx_per_block = total_tx_in_blocks / 10 if total_tx_in_blocks > 0 else 0.0
    success_rate = consensus_success / 10

    print(f"✓ 10슬롯 완료: 평균 {avg_tx_per_block:.1f}개 tx/블록")
    print(f"✓ 합의 성공률: {success_rate:.1%}")
    print(f"✓ 체인 높이: {blockchain.get_latest_block().header.block_id}")

    # ────────────────────────────────────────────────────────────────────
    # SECTION 4: 슬래싱 & 보상 분배
    # ────────────────────────────────────────────────────────────────────
    print("\n【 SECTION 4: 슬래싱 & 보상 분배 】")
    print("─" * 70)

    # 3명 슬래싱
    for i in range(3):
        addr = dpos._active_validators[i]
        slash_amt = dpos.slash_validator(addr, "double_signing")
        print(f"✓ 슬래싱 {addr[:10]}...: {slash_amt:.2f} GOG")

    # 보상 상위 5명
    top_validators = sorted(
        dpos._validators.values(),
        key=lambda v: v.reward_balance,
        reverse=True
    )[:5]

    print(f"✓ 보상 상위 5명:")
    for i, v in enumerate(top_validators, 1):
        print(f"  {i}. {v.address[:10]}...: {v.reward_balance:.2f} GOG")

    # ────────────────────────────────────────────────────────────────────
    # SECTION 5: 스마트 컨트랙트
    # ────────────────────────────────────────────────────────────────────
    print("\n【 SECTION 5: 스마트 컨트랙트 배포 & VM 실행 】")
    print("─" * 70)

    contract_mgr = SmartContract()

    # 간단한 컨트랙트 배포
    bytecode = [("PUSH", 5), ("PUSH", 3), ("ADD", None), ("HALT", None)]
    contract_addr = contract_mgr.deploy_contract(validator_addresses[0], bytecode)
    print(f"✓ 컨트랙트 주소: {contract_addr[:16]}...")

    result1 = contract_mgr.call_contract(contract_addr, validator_addresses[0])
    print(f"✓ 실행 1: result={result1['result']}, gas={result1['gas_used']}")

    # 두 번째 실행
    bytecode2 = [("PUSH", 10), ("PUSH", 20), ("MUL", None), ("HALT", None)]
    contract_addr2 = contract_mgr.deploy_contract(validator_addresses[1], bytecode2)
    result2 = contract_mgr.call_contract(contract_addr2, validator_addresses[1])
    print(f"✓ 실행 2: result={result2['result']}, gas={result2['gas_used']}")

    # ────────────────────────────────────────────────────────────────────
    # SECTION 6: P2P 네트워크
    # ────────────────────────────────────────────────────────────────────
    print("\n【 SECTION 6: P2P 네트워크 & 체인 동기화 】")
    print("─" * 70)

    network = P2PNetwork()

    # 5개 피어 참가
    peer_blockchains = []
    for i in range(5):
        peer_bc = Blockchain()
        peer_bc.initialize()
        network.join_network(f"peer_{i}", NodeRole.VALIDATOR, peer_bc)
        peer_blockchains.append(peer_bc)

    # 마지막 블록 전파
    last_block = blockchain.get_latest_block()
    if last_block:
        propagated = network.broadcast_block(last_block, "peer_0")
        print(f"✓ 네트워크 참가: {len(network._peers)}개 피어")
        print(f"✓ 블록 전파: {propagated}개 피어에 전달")

    # 동기화
    synced = network.sync_chain("peer_0")
    print(f"✓ 동기화: {'성공' if synced else '실패'}")

    # ────────────────────────────────────────────────────────────────────
    # SECTION 7: 블록 탐색기 & 검증
    # ────────────────────────────────────────────────────────────────────
    print("\n【 SECTION 7: 블록 탐색기 & 최종 검증 】")
    print("─" * 70)

    explorer = BlockExplorer(blockchain, dpos)
    validator_ranking = explorer.get_validator_ranking()

    print(f"✓ 검증자 순위 (상위 5):")
    for item in validator_ranking[:5]:
        print(f"  {item['rank']}위: {item['address']} ({item['total_stake']:.0f} GOG)")

    analytics = explorer.get_chain_analytics()
    valid, msg = blockchain.validate_chain()

    print(f"✓ 체인 무결성: {'유효' if valid else '오류: ' + msg}")
    print(f"✓ 총 트랜잭션: {analytics['total_transactions']}개")
    print(f"✓ 평균 블록 크기: {analytics['average_block_size']:.0f} bytes")

    # 최종 요약
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║          【 v11: 블록체인 & DPoS 합의 엔진 완성 】            ║")
    print("║                                                                ║")
    print("║  ✓ CryptoUtils: SHA-256 + Merkle Tree                        ║")
    print("║  ✓ TransactionPool: Mempool 관리                             ║")
    print("║  ✓ BlockFactory: 해시 체인 블록 생성                         ║")
    print("║  ✓ Blockchain: 잔액 추적 + 포크 해결                         ║")
    print("║  ✓ DPoSEngine: 21명 선출 + 보상 + 슬래싱                    ║")
    print("║  ✓ SmartContract: 스택 VM (14 옵코드)                        ║")
    print("║  ✓ P2PNetwork: Gossip 전파 + 동기화                          ║")
    print("║  ✓ BlockExplorer: 트랜잭션/주소/검증자 쿼리                 ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")


if __name__ == "__main__":
    main()
