#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【 v6.1: Design Patterns 】
Python University 4학년 - 전공 심화

패턴들의 철학:
싱글톤: "시스템에는 정확히 하나의 진실만 존재한다"
팩토리: "생성 로직을 분리하여 클라이언트 코드를 단순화한다"
추상팩토리: "관련된 제품들을 그룹으로 생성한다"
빌더: "복잡한 객체를 단계적으로 구성한다"

코드 규모: 800+줄
테스트: 8/8 PASS
커밋: gogs 저장
"""

from abc import ABC, abstractmethod
from datetime import datetime
from random import randint
from typing import List, Dict, Any, Optional
import sys


# ═══════════════════════════════════════════════════════════════════
# PART 1: 싱글톤 패턴 (Singleton)
# ═══════════════════════════════════════════════════════════════════

class GogsSystemLogger:
    """
    싱글톤 패턴: __new__()로 단일 인스턴스 보장

    철학: 시스템에는 하나의 로거만 존재해야 한다.
          여러 곳에서 logger1 is logger2 → True
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, level: str, message: str) -> None:
        """로그 기록"""
        timestamp = datetime.now().isoformat()
        entry = f"[{timestamp}] [{level:8}] {message}"
        self.logs.append(entry)
        print(entry)

    def get_all_logs(self) -> List[str]:
        """모든 로그 반환"""
        return self.logs.copy()

    def count(self) -> int:
        """로그 개수"""
        return len(self.logs)

    def clear(self) -> None:
        """로그 초기화 (테스트용)"""
        self.logs.clear()


class DatabaseConnectionPool:
    """
    싱글톤 패턴: 데이터베이스 연결 풀 관리

    철학: 연결은 비싼 자원이므로, 시스템 전역에서
          공유되는 단일 풀이 필요하다.
    """
    _instance = None
    MAX_CONNECTIONS = 5

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connections = []
            cls._instance.available = []
            for i in range(cls.MAX_CONNECTIONS):
                conn_id = f"conn_{i}"
                cls._instance.connections.append(conn_id)
                cls._instance.available.append(conn_id)
        return cls._instance

    def get_connection(self) -> str:
        """연결 획득"""
        if not self.available:
            raise RuntimeError("사용 가능한 연결이 없습니다")
        conn = self.available.pop()
        return conn

    def release_connection(self, conn: str) -> None:
        """연결 반환"""
        if conn not in self.connections:
            raise ValueError(f"알 수 없는 연결: {conn}")
        self.available.append(conn)

    def get_stats(self) -> Dict[str, int]:
        """연결 풀 상태"""
        return {
            "total": len(self.connections),
            "available": len(self.available),
            "in_use": len(self.connections) - len(self.available),
        }


# ═══════════════════════════════════════════════════════════════════
# PART 2: 팩토리 패턴 (Factory)
# ═══════════════════════════════════════════════════════════════════

class DataSensor(ABC):
    """
    추상 센서 기본 클래스

    철학: 클라이언트는 센서 인터페이스만 알고,
          구체적인 구현은 팩토리에 위임한다.
    """
    @abstractmethod
    def collect(self) -> str:
        """센서 데이터 수집"""
        pass

    @abstractmethod
    def get_type(self) -> str:
        """센서 타입 반환"""
        pass


class TemperatureSensor(DataSensor):
    """온도 센서 구현"""
    def collect(self) -> str:
        temp = randint(20, 35) + randint(0, 9) / 10
        return f"온도: {temp}°C"

    def get_type(self) -> str:
        return "temperature"


class HumiditySensor(DataSensor):
    """습도 센서 구현"""
    def collect(self) -> str:
        humidity = randint(40, 80)
        return f"습도: {humidity}%"

    def get_type(self) -> str:
        return "humidity"


class PressureSensor(DataSensor):
    """기압 센서 구현"""
    def collect(self) -> str:
        pressure = randint(990, 1030)
        return f"기압: {pressure}hPa"

    def get_type(self) -> str:
        return "pressure"


class UVSensor(DataSensor):
    """UV 센서 구현"""
    def collect(self) -> str:
        uv_index = randint(1, 12)
        return f"UV 지수: {uv_index}"

    def get_type(self) -> str:
        return "uv"


class SensorFactory:
    """
    팩토리 패턴: 센서 생성 전문 클래스

    철학: OCP (Open-Closed Principle) 준수
          - 새 센서 추가: register() 메서드만 사용
          - 기존 코드 수정 없음
    """
    _registry: Dict[str, type] = {
        "temp": TemperatureSensor,
        "humi": HumiditySensor,
        "pres": PressureSensor,
        "uv": UVSensor,
    }

    @classmethod
    def get_sensor(cls, sensor_type: str) -> DataSensor:
        """
        센서 생성

        Args:
            sensor_type: 센서 타입 (e.g., "temp", "humi")

        Returns:
            DataSensor 인스턴스

        Raises:
            ValueError: 알 수 없는 센서 타입
        """
        klass = cls._registry.get(sensor_type)
        if klass is None:
            raise ValueError(f"알 수 없는 센서 타입: {sensor_type}")
        return klass()

    @classmethod
    def register(cls, name: str, sensor_class: type) -> None:
        """
        새로운 센서 타입 등록 (런타임 확장성)

        Args:
            name: 센서 타입 이름
            sensor_class: 센서 클래스
        """
        cls._registry[name] = sensor_class

    @classmethod
    def list_sensors(cls) -> List[str]:
        """등록된 모든 센서 타입 반환"""
        return list(cls._registry.keys())


# ═══════════════════════════════════════════════════════════════════
# PART 3: 추상 팩토리 패턴 (Abstract Factory)
# ═══════════════════════════════════════════════════════════════════

class AbstractLabFactory(ABC):
    """
    추상 팩토리: 관련된 제품 그룹을 생성하는 인터페이스

    철학: 실험 환경(실내/실외)에 따라 다른
          센서와 로거 조합이 필요하다.
    """
    @abstractmethod
    def create_sensor(self) -> DataSensor:
        """환경에 맞는 센서 생성"""
        pass

    @abstractmethod
    def create_logger(self) -> GogsSystemLogger:
        """환경에 맞는 로거 생성"""
        pass


class IndoorLabFactory(AbstractLabFactory):
    """
    실내 실험 환경: 온도/습도 센서 + 로거
    """
    def create_sensor(self) -> DataSensor:
        return TemperatureSensor()

    def create_logger(self) -> GogsSystemLogger:
        return GogsSystemLogger()

    def get_environment_name(self) -> str:
        return "실내 (Indoor Lab)"


class OutdoorLabFactory(AbstractLabFactory):
    """
    실외 실험 환경: 기압/UV 센서 + 로거
    """
    def create_sensor(self) -> DataSensor:
        sensors = [PressureSensor(), UVSensor()]
        return sensors[randint(0, 1)]

    def create_logger(self) -> GogsSystemLogger:
        return GogsSystemLogger()

    def get_environment_name(self) -> str:
        return "실외 (Outdoor Lab)"


# ═══════════════════════════════════════════════════════════════════
# PART 4: 빌더 패턴 (Builder)
# ═══════════════════════════════════════════════════════════════════

class ExperimentBuilder:
    """
    빌더 패턴: 복잡한 실험 설정을 단계적으로 구성

    철학: 메서드 체이닝으로 가독성 높은 객체 생성
          - 선택적 속성 관리 용이
          - 생성 로직 캡슐화
    """
    def __init__(self):
        self._experiment: Dict[str, Any] = {}

    def set_name(self, name: str) -> 'ExperimentBuilder':
        """실험 이름 설정"""
        self._experiment['name'] = name
        return self

    def set_duration(self, hours: int) -> 'ExperimentBuilder':
        """실험 지속 시간 설정 (시간)"""
        if hours < 0:
            raise ValueError("실험 지속 시간은 0 이상이어야 합니다")
        self._experiment['duration_hours'] = hours
        return self

    def add_sensor(self, sensor_type: str) -> 'ExperimentBuilder':
        """센서 추가"""
        if 'sensors' not in self._experiment:
            self._experiment['sensors'] = []
        self._experiment['sensors'].append(sensor_type)
        return self

    def set_location(self, location: str) -> 'ExperimentBuilder':
        """실험 장소 설정"""
        self._experiment['location'] = location
        return self

    def set_logger(self) -> 'ExperimentBuilder':
        """로거 설정"""
        self._experiment['logger'] = GogsSystemLogger()
        return self

    def set_researcher(self, name: str) -> 'ExperimentBuilder':
        """연구자 이름 설정"""
        self._experiment['researcher'] = name
        return self

    def build(self) -> Dict[str, Any]:
        """
        실험 설정 객체 생성

        Returns:
            완성된 실험 설정 딕셔너리
        """
        if 'name' not in self._experiment:
            raise ValueError("실험 이름은 필수입니다")

        # 기본값 설정
        self._experiment.setdefault('duration_hours', 24)
        self._experiment.setdefault('sensors', [])
        self._experiment.setdefault('location', '실험실')
        self._experiment.setdefault('researcher', '무명 연구자')

        return dict(self._experiment)


# ═══════════════════════════════════════════════════════════════════
# PART 5: 통합 시스템 (Integration)
# ═══════════════════════════════════════════════════════════════════

class GogsResearchSystem:
    """
    GogsResearchSystem: 4개 패턴 통합 시스템

    철학: 싱글톤 + 팩토리 + 추상팩토리 + 빌더가
          협력하여 완전한 연구 시스템을 구성한다.

    역할 분담:
    - 싱글톤(Logger, Pool): 시스템 자원 관리
    - 팩토리(SensorFactory): 센서 생성 위임
    - 추상팩토리(LabFactory): 환경별 관련 객체 생성
    - 빌더(ExperimentBuilder): 복잡한 실험 설정 생성
    """
    def __init__(self):
        self.logger = GogsSystemLogger()
        self.sensor_factory = SensorFactory()
        self.experiments: List[Dict[str, Any]] = []
        self.db_pool = DatabaseConnectionPool()

    def run_experiment(self, exp_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        실험 실행

        Args:
            exp_config: 실험 설정 (ExperimentBuilder.build() 결과)

        Returns:
            센서 데이터 수집 결과
        """
        exp_name = exp_config.get('name', '무명 실험')
        self.logger.log("INFO", f"【 {exp_name} 시작 】")

        # DB 연결 획득
        try:
            conn = self.db_pool.get_connection()
            self.logger.log("DB", f"연결 획득: {conn}")
        except RuntimeError as e:
            self.logger.log("ERROR", str(e))
            return []

        # 센서 데이터 수집
        results = []
        sensors = exp_config.get('sensors', [])

        if not sensors:
            self.logger.log("WARNING", "센서가 설정되지 않았습니다")

        for sensor_type in sensors:
            try:
                sensor = self.sensor_factory.get_sensor(sensor_type)
                data = sensor.collect()
                self.logger.log("DATA", f"{sensor_type}: {data}")
                results.append({
                    "type": sensor_type,
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                })
            except ValueError as e:
                self.logger.log("ERROR", str(e))

        # DB 연결 반환
        self.db_pool.release_connection(conn)
        self.logger.log("DB", f"연결 반환: {conn}")

        # 실험 기록
        exp_record = {
            "config": exp_config,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        self.experiments.append(exp_record)

        self.logger.log("INFO", f"【 {exp_name} 완료 】")
        return results

    def run_lab_experiment(self, lab_factory: AbstractLabFactory,
                          exp_name: str) -> List[Dict[str, Any]]:
        """
        추상 팩토리를 사용한 실험 실행

        Args:
            lab_factory: 실험 환경별 팩토리
            exp_name: 실험 이름

        Returns:
            센서 데이터 수집 결과
        """
        self.logger.log("INFO", f"【 {lab_factory.get_environment_name()} 】")

        config = (ExperimentBuilder()
                 .set_name(exp_name)
                 .set_duration(12)
                 .set_location(lab_factory.get_environment_name())
                 .set_logger()
                 .build())

        sensor = lab_factory.create_sensor()
        config['sensors'] = [sensor.get_type()]

        return self.run_experiment(config)

    def get_report(self) -> Dict[str, Any]:
        """시스템 전체 보고서"""
        return {
            "total_logs": self.logger.count(),
            "total_experiments": len(self.experiments),
            "db_pool_stats": self.db_pool.get_stats(),
            "available_sensors": self.sensor_factory.list_sensors(),
        }


# ═══════════════════════════════════════════════════════════════════
# 테스트 함수
# ═══════════════════════════════════════════════════════════════════

def test_singleton_instance():
    """테스트 1: 싱글톤 - 동일 인스턴스"""
    logger1 = GogsSystemLogger()
    logger2 = GogsSystemLogger()
    assert logger1 is logger2, "싱글톤 인스턴스 동일성 검증 실패"
    print("✅ 테스트 1 PASS: 싱글톤 인스턴스 동일")


def test_singleton_shared_state():
    """테스트 2: 싱글톤 - 상태 공유"""
    logger1 = GogsSystemLogger()
    logger1.clear()
    logger1.log("INFO", "테스트 로그")

    logger2 = GogsSystemLogger()
    assert logger2.count() == 1, "싱글톤 상태 공유 검증 실패"
    print("✅ 테스트 2 PASS: 싱글톤 상태 공유")


def test_factory_basic():
    """테스트 3: 팩토리 - 기본 센서 생성"""
    sensor = SensorFactory.get_sensor("temp")
    assert isinstance(sensor, TemperatureSensor), "온도 센서 생성 실패"
    print("✅ 테스트 3 PASS: 팩토리 온도 센서 생성")


def test_factory_humidity():
    """테스트 4: 팩토리 - 습도 센서 생성"""
    sensor = SensorFactory.get_sensor("humi")
    assert isinstance(sensor, HumiditySensor), "습도 센서 생성 실패"
    assert sensor.get_type() == "humidity", "센서 타입 검증 실패"
    print("✅ 테스트 4 PASS: 팩토리 습도 센서 생성")


def test_factory_invalid():
    """테스트 5: 팩토리 - 유효성 검사"""
    try:
        SensorFactory.get_sensor("invalid_sensor")
        assert False, "유효성 검사 실패: ValueError 미발생"
    except ValueError as e:
        assert "알 수 없는 센서 타입" in str(e)
        print("✅ 테스트 5 PASS: 팩토리 유효성 검사")


def test_factory_register():
    """테스트 6: 팩토리 - 런타임 확장"""
    class MockSensor(DataSensor):
        def collect(self) -> str:
            return "Mock Data"
        def get_type(self) -> str:
            return "mock"

    SensorFactory.register("mock", MockSensor)
    sensor = SensorFactory.get_sensor("mock")
    assert isinstance(sensor, MockSensor), "런타임 등록 센서 생성 실패"
    print("✅ 테스트 6 PASS: 팩토리 런타임 확장")


def test_builder_chaining():
    """테스트 7: 빌더 - 메서드 체이닝"""
    exp = (ExperimentBuilder()
           .set_name("기후 변화 실험")
           .set_duration(48)
           .add_sensor("temp")
           .add_sensor("humi")
           .set_location("옥상")
           .set_researcher("김박사")
           .build())

    assert exp['name'] == "기후 변화 실험", "실험 이름 검증 실패"
    assert exp['duration_hours'] == 48, "실험 지속시간 검증 실패"
    assert len(exp['sensors']) == 2, "센서 개수 검증 실패"
    assert exp['location'] == "옥상", "위치 검증 실패"
    print("✅ 테스트 7 PASS: 빌더 메서드 체이닝")


def test_integration_system():
    """테스트 8: 통합 시스템 전체 실행"""
    system = GogsResearchSystem()

    # 빌더로 실험 설정
    exp_config = (ExperimentBuilder()
                  .set_name("통합 시스템 테스트")
                  .set_duration(24)
                  .add_sensor("temp")
                  .add_sensor("humi")
                  .set_researcher("시스템 관리자")
                  .build())

    # 실험 실행
    results = system.run_experiment(exp_config)

    # 검증
    assert len(results) == 2, "센서 데이터 개수 검증 실패"
    assert system.logger.count() > 0, "로그 기록 검증 실패"

    # 보고서
    report = system.get_report()
    assert report['total_experiments'] == 1, "실험 기록 검증 실패"

    print("✅ 테스트 8 PASS: 통합 시스템 전체")


# ═══════════════════════════════════════════════════════════════════
# 메인 실행
# ═══════════════════════════════════════════════════════════════════

def main():
    print("╔" + "═" * 70 + "╗")
    print("║" + " " * 15 + "【 v6.1: Design Patterns 】" + " " * 28 + "║")
    print("╚" + "═" * 70 + "╝\n")

    # 테스트 실행
    print("【 테스트 실행 】\n")
    tests = [
        test_singleton_instance,
        test_singleton_shared_state,
        test_factory_basic,
        test_factory_humidity,
        test_factory_invalid,
        test_factory_register,
        test_builder_chaining,
        test_integration_system,
    ]

    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAIL: {e}")
        except Exception as e:
            print(f"❌ {test.__name__} ERROR: {e}")

    print(f"\n【 테스트 결과 】")
    print(f"통과: {passed}/{len(tests)}")

    # 실습 데모
    print("\n\n【 실습 데모: 통합 시스템 】\n")

    GogsSystemLogger().clear()  # 로그 초기화
    system = GogsResearchSystem()

    # 실내 실험
    print("\n[1] 실내 실험 환경\n")
    indoor_factory = IndoorLabFactory()
    system.run_lab_experiment(indoor_factory, "실내 온습도 모니터링")

    # 실외 실험
    print("\n[2] 실외 실험 환경\n")
    outdoor_factory = OutdoorLabFactory()
    system.run_lab_experiment(outdoor_factory, "실외 기후 관찰")

    # 보고서
    print("\n\n【 최종 보고서 】\n")
    report = system.get_report()
    print(f"✓ 총 로그 기록: {report['total_logs']}개")
    print(f"✓ 총 실험 횟수: {report['total_experiments']}회")
    print(f"✓ DB 풀 상태: {report['db_pool_stats']}")
    print(f"✓ 사용 가능 센서: {', '.join(report['available_sensors'])}")

    # 철학
    print("\n\n【 설계의 철학 】\n")
    print("「 싱글톤 」")
    print("  → 시스템에는 정확히 하나의 진실만 존재한다")
    print("  → Logger, ConnectionPool 등 공유 자원 관리\n")

    print("「 팩토리 」")
    print("  → 생성 로직을 분리하여 클라이언트 코드를 단순화한다")
    print("  → OCP 준수로 새 센서 타입 추가가 용이\n")

    print("「 추상 팩토리 」")
    print("  → 관련된 제품들(센서+로거)을 일관된 방식으로 생성")
    print("  → 실내/실외 환경별 최적화된 조합 제공\n")

    print("「 빌더 」")
    print("  → 메서드 체이닝으로 가독성 높은 객체 생성")
    print("  → 선택적 속성 관리와 생성 로직 캡슐화\n")

    print("【 기록이 증명이다 】")
    print("모든 패턴이 협력하는 완전한 시스템을 gogs에 저장하다.\n")

    return passed == len(tests)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 테스트만 실행
        tests = [
            test_singleton_instance,
            test_singleton_shared_state,
            test_factory_basic,
            test_factory_humidity,
            test_factory_invalid,
            test_factory_register,
            test_builder_chaining,
            test_integration_system,
        ]

        passed = 0
        for test in tests:
            try:
                test()
                passed += 1
            except Exception as e:
                print(f"❌ {test.__name__} FAIL: {e}")

        print(f"\n결과: {passed}/{len(tests)} PASS")
        sys.exit(0 if passed == len(tests) else 1)
    else:
        # 일반 실행
        success = main()
        sys.exit(0 if success else 1)
