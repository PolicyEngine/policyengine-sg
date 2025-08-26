#!/usr/bin/env python3
"""
PolicyEngine Vectorization Checker

Automatically detects if-elif-else statements in formula methods,
which violate PolicyEngine's mandatory vectorization requirements.

Usage:
    python check_vectorization.py [path_to_check]
    
Exit codes:
    0: All files pass vectorization check
    1: Vectorization violations found
"""

import ast
import sys
from pathlib import Path
from typing import List, Tuple


class VectorizationChecker(ast.NodeVisitor):
    """AST visitor that checks for if-elif-else statements in formula methods."""

    def __init__(self, filename: str):
        self.filename = filename
        self.violations: List[Tuple[int, str]] = []
        self.in_formula_method = False
        self.current_class = None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Track current class (likely a Variable subclass)."""
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Check if we're in a formula method."""
        old_in_formula = self.in_formula_method

        # Common PolicyEngine formula method names
        if node.name in ["formula", "compute", "calculate"]:
            self.in_formula_method = True

        self.generic_visit(node)
        self.in_formula_method = old_in_formula

    def visit_If(self, node: ast.If) -> None:
        """Flag if-elif-else statements in formula methods."""
        if self.in_formula_method:
            # Check if this is a simple if without elif/else (might be acceptable)
            has_elif = bool(node.orelse and isinstance(node.orelse[0], ast.If))
            has_else = bool(
                node.orelse and not isinstance(node.orelse[0], ast.If)
            )

            if has_elif:
                self.violations.append(
                    (
                        node.lineno,
                        f"CRITICAL: if-elif statement in formula method (line {node.lineno}). "
                        f"Use select() with default parameter instead.",
                    )
                )
            elif has_else:
                self.violations.append(
                    (
                        node.lineno,
                        f"CRITICAL: if-else statement in formula method (line {node.lineno}). "
                        f"Use where() or boolean multiplication instead.",
                    )
                )
            else:
                # Simple if without else - still discouraged but not auto-fail
                self.violations.append(
                    (
                        node.lineno,
                        f"WARNING: if statement in formula method (line {node.lineno}). "
                        f"Consider vectorization with where() or boolean operations.",
                    )
                )

        self.generic_visit(node)


def check_file(filepath: Path) -> List[Tuple[int, str]]:
    """Check a single Python file for vectorization violations."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=str(filepath))
        checker = VectorizationChecker(str(filepath))
        checker.visit(tree)
        return checker.violations

    except SyntaxError as e:
        return [(e.lineno or 0, f"Syntax error: {e.msg}")]
    except Exception as e:
        return [(0, f"Error parsing file: {e}")]


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        search_path = Path(sys.argv[1])
    else:
        search_path = Path("policyengine_au/variables")

    if not search_path.exists():
        print(f"Error: Path {search_path} does not exist")
        sys.exit(1)

    # Find all Python files
    if search_path.is_file() and search_path.suffix == ".py":
        python_files = [search_path]
    else:
        python_files = list(search_path.rglob("*.py"))

    total_violations = 0
    critical_violations = 0

    print("🚨 PolicyEngine Vectorization Check")
    print("=" * 50)

    for filepath in python_files:
        violations = check_file(filepath)

        if violations:
            print(f"\n📁 {filepath}")
            for line_no, message in violations:
                print(f"  Line {line_no}: {message}")
                total_violations += 1
                if "CRITICAL" in message:
                    critical_violations += 1

    print(f"\n{'='*50}")
    print(f"Total violations found: {total_violations}")
    print(f"Critical violations (auto-fail): {critical_violations}")

    if critical_violations > 0:
        print(
            "\n❌ REVIEW FAILURE: Critical vectorization violations detected!"
        )
        print("\nTo fix these violations:")
        print("- Replace if-elif-else with select() using default parameter")
        print("- Replace if-else with where() or boolean multiplication")
        print("- See REVIEWER_CHECKLIST.md for examples")
        sys.exit(1)
    elif total_violations > 0:
        print("\n⚠️  WARNING: Non-critical violations found")
        print("Consider improving vectorization for better performance")
        sys.exit(0)
    else:
        print("\n✅ All files pass vectorization requirements!")
        sys.exit(0)


if __name__ == "__main__":
    main()
