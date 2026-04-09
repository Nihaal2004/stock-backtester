"""
Simple mutation testing harness for DA3 evidence on Windows.
Creates controlled mutants in strategies.py and runs regression tests
to report killed vs survived mutants.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
TESTS_DIR = ROOT_DIR / "tests"
STRATEGIES_FILE = SRC_DIR / "strategies.py"


@dataclass(frozen=True)
class Mutant:
    mutant_id: str
    description: str
    replacements: tuple[tuple[str, str], ...]


MUTANTS = [
    Mutant(
        mutant_id="M001",
        description="SMA crossover direction reversed",
        replacements=(
            ("df['signal'] = (df['fast_sma'] > df['slow_sma']).astype(int)",
             "df['signal'] = (df['fast_sma'] < df['slow_sma']).astype(int)"),
        ),
    ),
    Mutant(
        mutant_id="M002",
        description="SMA uses max instead of mean",
        replacements=(
            ("return series.rolling(window, min_periods=window).mean()",
             "return series.rolling(window, min_periods=window).max()"),
        ),
    ),
    Mutant(
        mutant_id="M003",
        description="SMA validation weakens fast/slow check",
        replacements=(("if fast >= slow:", "if fast > slow:"),),
    ),
    Mutant(
        mutant_id="M004",
        description="RSI validation weakens threshold check",
        replacements=(("if buy_threshold >= sell_threshold:", "if buy_threshold > sell_threshold:"),),
    ),
    Mutant(
        mutant_id="M005",
        description="RSI buy condition becomes inclusive",
        replacements=(("if in_position == 0 and value < buy_threshold:",
                       "if in_position == 0 and value <= buy_threshold:"),),
    ),
]


def apply_mutation(original_source: str, mutant: Mutant) -> str:
    mutated_source = original_source
    for original_text, mutated_text in mutant.replacements:
        if original_text not in mutated_source:
            raise ValueError(f"Could not apply {mutant.mutant_id}: pattern not found: {original_text}")
        mutated_source = mutated_source.replace(original_text, mutated_text, 1)
    return mutated_source


def run_mutant(mutant: Mutant, original_source: str) -> tuple[str, int]:
    with tempfile.TemporaryDirectory(prefix="mutation_trial_") as temp_dir:
        temp_path = Path(temp_dir)
        shutil.copytree(SRC_DIR, temp_path / "src")
        shutil.copytree(TESTS_DIR, temp_path / "tests")
        (temp_path / "setup.cfg").write_text(
            "[tool:pytest]\n"
            "testpaths = tests\n"
            "python_files = test_*.py\n",
            encoding="utf-8",
        )

        mutated_source = apply_mutation(original_source, mutant)
        (temp_path / "src" / "strategies.py").write_text(mutated_source, encoding="utf-8")

        test_cmd = [sys.executable, "-m", "pytest", "-q", "tests/test_regression_backtest.py"]
        result = subprocess.run(test_cmd, cwd=temp_path, capture_output=True, text=True)
        output = (result.stdout + "\n" + result.stderr).strip()
        return output, result.returncode


def main() -> int:
    if not STRATEGIES_FILE.exists():
        print(f"Source file not found: {STRATEGIES_FILE}")
        return 2

    original_source = STRATEGIES_FILE.read_text(encoding="utf-8")
    print("=== Mutation Testing (Windows-compatible harness) ===")
    print(f"Target module: {STRATEGIES_FILE}")
    print(f"Total mutants: {len(MUTANTS)}\n")

    killed = 0
    survived = 0

    for mutant in MUTANTS:
        print(f"[{mutant.mutant_id}] {mutant.description}")
        try:
            output, return_code = run_mutant(mutant, original_source)
        except Exception as exc:  # Surface explicit mutation execution failures.
            print(f"  ERROR: {exc}\n")
            continue

        if return_code == 0:
            survived += 1
            print("  Status: SURVIVED (tests did not fail)")
        else:
            killed += 1
            print("  Status: KILLED (tests failed as expected)")

        first_output_line = output.splitlines()[0] if output else "No output"
        print(f"  Test output: {first_output_line}\n")

    print("=== Mutation Summary ===")
    print(f"Killed mutants:   {killed}")
    print(f"Survived mutants: {survived}")
    print(f"Total mutants:    {len(MUTANTS)}")
    score = (killed / len(MUTANTS)) * 100 if MUTANTS else 0.0
    print(f"Mutation score:   {score:.2f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
