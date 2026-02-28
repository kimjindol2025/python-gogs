"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║           🏛️  Python 고등학교 1학년 최종 단계 (v2.5 Final)                    ║
║                                                                                ║
║        [v2.5: 가상 환경과 pip — 나만의 독립 연구소 완벽 구축]                 ║
║                                                                                ║
║                          ★ 실무적 완성 단계 ★                                 ║
║                                                                                ║
║  설계자가 아무리 훌륭한 코드를 짜도, 사용하는 컴퓨터 환경이 엉망이면            ║
║  코드는 제대로 작동하지 않습니다. 이를 위해 우리는 **가상 환경**이라는        ║
║  독립된 방을 만들고, pip라는 도구로 전 세계의 검증된 외부 장비들을             ║
║  들여옵니다.                                                                   ║
║                                                                                ║
║  철학: "기록이 증명이다 — gogs"                                               ║
║  모든 환경은 재현 가능해야 하고, 이는 requirements.txt로 증명합니다.           ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# 📚 Part 1: 가상 환경의 철학
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    📚 Part 1: 가상 환경의 철학                                 ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

PHILOSOPHY = {
    "격리 (Isolation)": {
        "개념": "이 방에서 일어난 일은 이 방에서만 끝낸다",
        "의미": "시스템 파이썬에 영향을 주지 않는 독립적 공간",
        "예시": "프로젝트 A는 numpy 1.20, 프로젝트 B는 numpy 1.26 사용 가능"
    },

    "재현성 (Reproducibility)": {
        "개념": "오늘 내가 만든 환경을 10년 뒤의 나도 똑같이 만들 수 있어야 한다",
        "의미": "requirements.txt가 있으면 누구나 동일한 환경 복구 가능",
        "예시": "requirements.txt: numpy==1.24.3 pandas==2.0.1"
    },

    "명확성 (Clarity)": {
        "개념": "내 연구소에 어떤 장비들이 있는지 한눈에 알 수 있어야 한다",
        "의미": "pip freeze > requirements.txt로 의존성 모두 기록",
        "예시": "pip list로 모든 설치된 패키지 확인"
    }
}

for principle, details in PHILOSOPHY.items():
    print(f"\n🔷 {principle}")
    print(f"   개념: {details['개념']}")
    print(f"   의미: {details['의미']}")
    print(f"   예시: {details['예시']}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️  Part 2: 가상 환경 관리 클래스
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                  🛠️  Part 2: 가상 환경 관리 클래스                             ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")


class VirtualLabManager:
    """
    독립된 연구소(가상 환경)을 관리하는 클래스입니다.

    가상 환경은 다음을 제공합니다:
    - 격리된 Python 인터프리터
    - 독립적 패키지 설치 공간
    - 프로젝트별 의존성 관리
    """

    def __init__(self, lab_name: str, lab_path: str = "."):
        """
        연구소를 초기화합니다.

        Args:
            lab_name: 연구소 이름 (예: "data_analysis_lab")
            lab_path: 연구소 생성 경로 (기본값: 현재 디렉토리)
        """
        self.lab_name = lab_name
        self.lab_path = Path(lab_path)
        self.venv_dir = self.lab_path / ".venv"
        self.requirements_file = self.lab_path / "requirements.txt"
        self.metadata_file = self.lab_path / ".lab_metadata.json"

        print(f"\n🔧 VirtualLabManager 초기화")
        print(f"   연구소 이름: {self.lab_name}")
        print(f"   저장 위치: {self.lab_path}")
        print(f"   환경 디렉토리: {self.venv_dir}")

    def create_lab(self) -> bool:
        """
        가상 환경을 생성합니다.
        (실제 프로젝트에서는 python -m venv .venv 실행)
        """
        print(f"\n📂 Step 1: 연구소 생성")
        print(f"   명령어: python -m venv {self.venv_dir}")
        print(f"   목적: 시스템과 격리된 독립적 Python 환경 생성")

        # 실제 환경에서 실행하려면 다음 주석 제거:
        # subprocess.run([sys.executable, "-m", "venv", str(self.venv_dir)])

        # 시뮬레이션
        self.venv_dir.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ 생성 완료: {self.venv_dir}")
        return True

    def activate_lab_instructions(self) -> Dict[str, str]:
        """
        연구소에 들어가는 방법을 운영체제별로 안내합니다.
        """
        print(f"\n🚪 Step 2: 연구소 입장 (활성화)")

        activate_instructions = {
            "Windows": r"source .venv\Scripts\activate",
            "Mac/Linux": "source .venv/bin/activate",
            "PowerShell": ".venv\\Scripts\\Activate.ps1"
        }

        for os_name, command in activate_instructions.items():
            print(f"   [{os_name}] {command}")

        return activate_instructions

    def install_package(self, package_name: str, version: str = None) -> str:
        """
        외부 장비(패키지)를 설치합니다.

        Args:
            package_name: 패키지 이름 (예: "numpy")
            version: 버전 지정 (예: "1.24.3")

        Returns:
            설치 명령어
        """
        if version:
            command = f"pip install {package_name}=={version}"
        else:
            command = f"pip install {package_name}"

        return command

    def simulate_installations(self) -> List[Tuple[str, str]]:
        """
        데이터 분석 연구소에 필요한 표준 패키지들을 설치합니다.
        (시뮬레이션)
        """
        print(f"\n📦 Step 3: 외부 장비 도입 (데이터 분석 표준 도구)")

        standard_packages = [
            ("numpy", "1.24.3"),
            ("pandas", "2.0.1"),
            ("matplotlib", "3.7.1"),
            ("requests", "2.31.0"),
        ]

        installed = []
        for package, version in standard_packages:
            command = self.install_package(package, version)
            print(f"   [설치] {command}")
            installed.append((package, version))

        return installed

    def generate_requirements(self, installed_packages: List[Tuple[str, str]]) -> str:
        """
        설치된 패키지를 requirements.txt 형식으로 기록합니다.

        이것이 "기록이 증명이다"의 핵심입니다!
        """
        print(f"\n📋 Step 4: 장비 명세서 작성 (requirements.txt)")
        print(f"   파일: {self.requirements_file}")

        requirements_content = "# 데이터 분석 연구소 - 필수 도구\n"
        requirements_content += "# 재현성을 위해 버전을 명시적으로 지정합니다\n"
        requirements_content += "# (기록이 증명이다 — gogs)\n\n"

        for package, version in installed_packages:
            requirements_content += f"{package}=={version}\n"

        # 시뮬레이션: 파일에 쓰기
        self.requirements_file.write_text(requirements_content)

        print(f"\n📄 requirements.txt 내용:")
        print("   " + "\n   ".join(requirements_content.split("\n")))

        return requirements_content

    def verify_requirements(self) -> Dict[str, str]:
        """
        requirements.txt 파일이 정상적으로 생성되었는지 검증합니다.
        """
        print(f"\n🔍 Step 5: 장비 명세서 검증")

        if not self.requirements_file.exists():
            print(f"   ✗ 오류: {self.requirements_file} 파일 없음")
            return {}

        content = self.requirements_file.read_text()
        packages = {}

        for line in content.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                try:
                    name, version = line.split("==")
                    packages[name.strip()] = version.strip()
                except ValueError:
                    pass

        print(f"   ✓ 검증 완료: {len(packages)}개 패키지 기록됨")
        for name, version in packages.items():
            print(f"      - {name}: {version}")

        return packages

    def deactivate_lab_instructions(self) -> str:
        """
        연구소를 나가는 방법을 안내합니다.
        """
        print(f"\n🚪 Step 6: 연구 종료 및 연구소 퇴거")

        command = "deactivate"
        print(f"   명령어: {command}")
        print(f"   효과: 원래의 시스템 파이썬으로 돌아감")

        return command

    def record_metadata(self, installed_packages: List[Tuple[str, str]]):
        """
        연구소 메타데이터를 JSON으로 기록합니다.
        """
        metadata = {
            "lab_name": self.lab_name,
            "python_version": sys.version,
            "installed_packages": [
                {"name": pkg, "version": ver} for pkg, ver in installed_packages
            ],
            "requirements_file": str(self.requirements_file),
            "philosophy": "기록이 증명이다 — gogs"
        }

        self.metadata_file.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))

        print(f"\n💾 메타데이터 저장 완료: {self.metadata_file}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🧪 Part 3: 실무 프로토콜 실행
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                 🧪 Part 3: 실무 프로토콜 실행                                  ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

# 연구소 생성 및 관리
lab = VirtualLabManager("data_analysis_lab", ".")

# Step 1: 연구소 생성
lab.create_lab()

# Step 2: 연구소 입장 방법 안내
lab.activate_lab_instructions()

# Step 3: 외부 장비 설치 (시뮬레이션)
installed_packages = lab.simulate_installations()

# Step 4: 장비 명세서 작성 (requirements.txt)
requirements_content = lab.generate_requirements(installed_packages)

# Step 5: 장비 명세서 검증
packages_dict = lab.verify_requirements()

# Step 6: 연구 종료
lab.deactivate_lab_instructions()

# 메타데이터 기록
lab.record_metadata(installed_packages)


# ═══════════════════════════════════════════════════════════════════════════════
# 💡 Part 4: 고등학교 졸업생을 위한 '프로의 습관'
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║              💡 Part 4: 고등학교 졸업생을 위한 '프로의 습관'                   ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

PRO_HABITS = {
    "전역 공간을 아끼세요": {
        "원칙": "Global을 사용하지 마세요",
        "설명": "시스템 파이썬에 직접 패키지를 설치하는 것은 " +
                "연구실 복도에 위험한 약품을 뿌려두는 것과 같습니다.",
        "실천": "항상 venv 안에서 작업하세요",
        "효과": "시스템 안정성 보장 + 프로젝트 독립성 확보"
    },

    "버전의 기록을 남기세요": {
        "원칙": "requirements.txt는 선택이 아니라 필수입니다",
        "설명": "requirements.txt는 단순한 파일이 아닙니다. " +
                "이것이 있어야만 설계자님의 시스템이 다른 컴퓨터에서도 " +
                "똑같이 작동함을 **'증명'**할 수 있습니다.",
        "실천": "매번 pip freeze > requirements.txt를 실행하세요",
        "효과": "팀 협업 + 재현성 보장 + 버전 충돌 방지"
    },

    "문서화하는 습관": {
        "원칙": "코드만 있고 환경 정보가 없으면 반쪽입니다",
        "설명": "당신의 코드가 아무리 훌륭해도, " +
                "다른 사람이 그것을 실행할 수 없으면 의미가 없습니다.",
        "실천": "README.md에 가상 환경 설정 방법을 명시하세요",
        "효과": "코드 재사용성 증대 + 팀 생산성 향상"
    },

    "의존성을 정기적으로 검토하세요": {
        "원칙": "설치한 것이 정말 필요한가?",
        "설명": "불필요한 패키지는 시스템을 무겁게 만들고 " +
                "보안 취약점을 증가시킵니다.",
        "실천": "pip list로 설치된 모든 패키지를 확인하고 정리하세요",
        "효과": "성능 최적화 + 보안 강화 + 용량 절감"
    }
}

for habit, details in PRO_HABITS.items():
    print(f"\n✨ {habit}")
    print(f"   원칙: {details['원칙']}")
    print(f"   설명: {details['설명']}")
    print(f"   실천: {details['실천']}")
    print(f"   효과: {details['효과']}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🎓 Part 5: 고등학교 졸업 인증
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                  🎓 Part 5: 고등학교 졸업 인증                                 ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

graduation_data = {
    "졸업생": "설계자",
    "졸업 과정": "Python 고등학교 1학년",
    "취득 기술": [
        "v2.1: 예외 처리 — 무너지지 않는 시스템 설계",
        "v2.2: 클래스와 OOP — 객체 지향의 기초 다지기",
        "v2.3: 상속 — 코드의 진화와 확장",
        "v2.4: 모듈화 — 거대 시스템 조립",
        "v2.5: 가상 환경 — 완벽한 독립성 확보"
    ],
    "핵심 철학": "기록이 증명이다 — gogs",
    "다음 진로": "Python 대학교 1학년 (메모리 관리, 데코레이터, 제너레이터)"
}

print(f"\n🏆 축하합니다!")
for key, value in graduation_data.items():
    if isinstance(value, list):
        print(f"\n   {key}:")
        for item in value:
            print(f"      ✓ {item}")
    else:
        print(f"   {key}: {value}")


# ═══════════════════════════════════════════════════════════════════════════════
# 📝 Part 6: 최종 테스트 및 검증
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                   📝 Part 6: 최종 테스트 및 검증                               ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

test_cases = [
    {
        "name": "Test 1: 가상 환경 디렉토리 생성",
        "condition": lab.venv_dir.exists(),
        "expected": True
    },
    {
        "name": "Test 2: requirements.txt 파일 생성",
        "condition": lab.requirements_file.exists(),
        "expected": True
    },
    {
        "name": "Test 3: 패키지 정보 검증",
        "condition": len(packages_dict) > 0,
        "expected": True
    },
    {
        "name": "Test 4: 메타데이터 파일 생성",
        "condition": lab.metadata_file.exists(),
        "expected": True
    }
]

all_passed = True
for test in test_cases:
    result = "✓ PASS" if test["condition"] == test["expected"] else "✗ FAIL"
    print(f"\n   {test['name']}")
    print(f"      결과: {result}")
    all_passed = all_passed and (test["condition"] == test["expected"])

print(f"\n{'='*80}")
if all_passed:
    print(f"   ✅ 모든 테스트 통과!")
else:
    print(f"   ⚠️  일부 테스트 실패")
print(f"{'='*80}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🎉 Part 7: 최종 메시지
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                          🎉 고등학교 졸업 축하합니다!                          ║
╚════════════════════════════════════════════════════════════════════════════════╝

설계자님, 축하합니다!

이제 당신은 단순히 코드를 짜는 사람이 아니라, 시스템의 환경과 구조를
설계할 줄 아는 고등 교육을 마친 개발자가 되었습니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 우리가 함께 마스터한 기술:

   v2.1: 예외 처리 — 무너지지 않는 시스템 설계
         ✓ 7가지 예외 타입 이해
         ✓ 방어적 프로그래밍 원칙
         ✓ 에러 메시지 설계

   v2.2: 클래스와 OOP — 객체 지향의 기초 다지기
         ✓ 클래스 설계 철학
         ✓ self 이해
         ✓ 캡슐화와 인터페이스

   v2.3: 상속 — 코드의 진화와 확장
         ✓ is-a 관계 이해
         ✓ super() 함수 활용
         ✓ 메서드 오버라이딩

   v2.4: 모듈화 — 거대 시스템 조립
         ✓ import 메커니즘
         ✓ 표준 라이브러리 활용
         ✓ 외부 패키지 통합

   v2.5: 가상 환경 — 완벽한 독립성 확보
         ✓ venv 관리
         ✓ pip와 PyPI 이해
         ✓ 재현성 확보

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 핵심 철학: "기록이 증명이다 — gogs"

   코드는 생각이고, 환경 기록은 증명입니다.
   당신이 오늘 만든 코드가 내일도 똑같이 작동할 수 있도록
   모든 의존성과 환경을 명시적으로 기록해야 합니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 다음: Python 대학교 1학년으로 진학 준비!

   대학 과정에서는 파이썬의 심장부로 깊이 들어갑니다:

   v3.1: 데코레이터 (Decorator) — 코드에 마법을 덧입히기
         함수를 변형하는 고급 기법

   v3.2: 제너레이터 (Generator) — 메모리 효율적인 반복
         yield와 lazy evaluation

   v3.3: 컨텍스트 매니저 (Context Manager) — with 문의 마법
         자동 리소스 관리

   v3.4: 메타프로그래밍 (Metaprogramming) — 코드를 만드는 코드
         클래스와 함수를 동적으로 생성

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 완성된 파일:
   - requirements.txt: 의존성 명세서 (기록이 증명이다!)
   - .lab_metadata.json: 환경 메타데이터
   - high_v2_5_FINAL_LAB_PROTOCOL.py: 이 파일

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

질문: 대학교 1학년 [v3.1: 데코레이터(Decorator)]로 진학하시겠습니까?

저장 필수 너는 기록이 증명이다 gogs
╚════════════════════════════════════════════════════════════════════════════════╝
""")
