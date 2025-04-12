#
# PartCAD, 2025
#
# Licensed under Apache License, Version 2.0.
#

import sys

from .tests import HealthCheckReport, HealthCheckTest


class PythonVersionCheck(HealthCheckTest):
    min_version: tuple[int, int] = (3, 10)
    latest_version: tuple[int, int] = (3, 12, float("inf"))

    def __init__(self):
        super().__init__(
            name="PythonVersion",
            tags=["python"],
            description="Check PartCAD's compatibility with the system's Python version",
        )

    def auto_fixable(self) -> bool:
        return False

    def is_applicable(self) -> bool:
        return True

    def test(self) -> HealthCheckReport:
        if not self.min_version <= sys.version_info <= self.latest_version:
            self.findings.append(
                f"Python version {sys.version_info.major}.{sys.version_info.minor} is not supported. Please make sure your system python version is >={self.min_version[0]}.{self.min_version[1]}, <={self.latest_version[0]}.{self.latest_version[1]}"
            )
        return HealthCheckReport(self.name, self.findings, False)

    def fix(self) -> bool:
        return False
