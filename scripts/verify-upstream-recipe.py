#!/usr/bin/env python3
"""Fail when the Spring AI integration build plan drifts from upstream CI."""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ["./mvnw", "--batch-mode", "-ntp", "--update-snapshots", "clean", "install", "-DskipTests"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    try:
        plan = tomllib.loads((ROOT / ".boringcache.toml").read_text())
        require(plan["adapters"]["maven"]["command"] == EXPECTED, "Maven plan changed")
        upstream = (ROOT / "upstream/.github/workflows/spring-ai-integration-tests.yml").read_text()
        for fragment in (
            "java-version: '17'",
            "distribution: 'liberica'",
            "./mvnw ${{ vars.COMMERCIAL && '-s commercial-settings.xml -Pcommercial' || '' }} --batch-mode -ntp --update-snapshots clean install -DskipTests",
            "${{ inputs.springBootVersion != '' && format('-Dspring-boot.version={0}', inputs.springBootVersion) || '' }}",
        ):
            require(fragment in upstream, f"upstream Maven job changed: {fragment}")
        action = (ROOT / ".github/actions/spring-maven-benchmark/action.yml").read_text()
        require("run-benchmark-plan.py maven --working-directory upstream" in action, "workflow bypasses the plan")
    except (KeyError, OSError, RuntimeError, tomllib.TOMLDecodeError) as error:
        print(f"Spring AI recipe mismatch: {error}", file=sys.stderr)
        return 1
    print("Verified Spring AI integration-build Maven plan against pinned upstream CI.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
