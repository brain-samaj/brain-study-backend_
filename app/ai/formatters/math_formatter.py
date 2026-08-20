from __future__ import annotations

import re

from .latex_utils import (
    protect_latex,
    restore_latex,
)


class MathFormatter:
    """
    Central mathematical notation formatter for Brain Study.

    Converts common plain-text mathematical notation into
    KaTeX-compatible LaTeX while protecting expressions that
    are already formatted.

    Supported examples:

        x^2                 -> $x^{2}$
        2/3                 -> $\\frac{2}{3}$
        sqrt(x+4)           -> $\\sqrt{x+4}$
        (x+1)/(x-2)         -> $\\frac{x+1}{x-2}$
        1011 base 2         -> $1011_{2}$
        1011_2              -> $1011_{2}$
        log base 2 of 8     -> $\\log_{2}(8)$
        90 degrees          -> $90^\\circ$
        x <= 5              -> $x \\le 5$
        x >= 2              -> $x \\ge 2$
        x != 3              -> $x \\ne 3$

    Existing LaTeX is never reformatted.
    """

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def format(self, text: str) -> str:
        if not text or not text.strip():
            return text

        protected, placeholders = protect_latex(text)

        # Order matters.
        protected = self._symbols(protected)
        protected = self._logarithms(protected)
        protected = self._number_bases(protected)
        protected = self._square_roots(protected)
        protected = self._fractions(protected)
        protected = self._powers(protected)
        protected = self._subscripts(protected)
        protected = self._degrees(protected)

        return restore_latex(protected, placeholders)

    # ---------------------------------------------------------
    # Mathematical symbols
    # ---------------------------------------------------------

    def _symbols(self, text: str) -> str:
        """
        Convert common comparison and mathematical symbols.

        Function replacements are deliberately used with re.sub()
        so LaTeX backslashes are never interpreted as regex
        replacement escapes.
        """

        patterns = [
            (
                r"(?<![<])<=(?![>])",
                r"\le",
            ),
            (
                r"(?<![>])>=(?![<])",
                r"\ge",
            ),
            (
                r"!=",
                r"\ne",
            ),
            (
                r"(?<![=])=(?!=)",
                "=",
            ),
        ]

        for pattern, replacement in patterns:
            text = re.sub(
                pattern,
                lambda _match, value=replacement: value,
                text,
            )

        # Unicode mathematical symbols.
        replacements = {
            "≤": r"\le",
            "≥": r"\ge",
            "≠": r"\ne",
            "≈": r"\approx",
            "±": r"\pm",
            "∓": r"\mp",
            "×": r"\times",
            "÷": r"\div",
            "∞": r"\infty",
            "→": r"\rightarrow",
            "←": r"\leftarrow",
            "↔": r"\leftrightarrow",
            "⇌": r"\rightleftharpoons",
            "π": r"\pi",
            "Δ": r"\Delta",
            "θ": r"\theta",
            "α": r"\alpha",
            "β": r"\beta",
            "γ": r"\gamma",
            "λ": r"\lambda",
            "μ": r"\mu",
            "σ": r"\sigma",
            "ω": r"\omega",
        }

        for source, target in replacements.items():
            text = text.replace(source, target)

        return text

    # ---------------------------------------------------------
    # Logarithms
    # ---------------------------------------------------------

    def _logarithms(self, text: str) -> str:
        """
        Convert:

            log base 2 of 8
            log base 10 of 100
            log base 3 of x

        into:

            $\\log_{2}(8)$
            $\\log_{10}(100)$
            $\\log_{3}(x)$
        """

        pattern = re.compile(
            r"\blog\s+base\s+"
            r"([A-Za-z0-9]+)"
            r"\s+of\s+"
            r"([A-Za-z0-9.+\-*/()]+)",
            re.IGNORECASE,
        )

        return pattern.sub(
            lambda match: (
                f"$\\log_{{{match.group(1)}}}"
                f"({match.group(2)})$"
            ),
            text,
        )

    # ---------------------------------------------------------
    # Number bases
    # ---------------------------------------------------------

    def _number_bases(self, text: str) -> str:
        """
        Convert:

            1011 base 2
            1011 base 10
            7F base 16

        into:

            $1011_{2}$
            $1011_{10}$
            $7F_{16}$

        Also supports:

            1011_2
            7F_16
        """

        # "1011 base 2"
        base_words = re.compile(
            r"(?<![\w$])"
            r"([A-Za-z0-9]+)"
            r"\s+base\s+"
            r"([0-9]+)"
            r"(?![\w])",
            re.IGNORECASE,
        )

        text = base_words.sub(
            lambda match: (
                f"${match.group(1)}_{{{match.group(2)}}}$"
            ),
            text,
        )

        # "1011_2"
        base_subscript = re.compile(
            r"(?<![\w$])"
            r"([A-Za-z0-9]+)"
            r"_([0-9]+)"
            r"(?![\w])",
        )

        text = base_subscript.sub(
            lambda match: (
                f"${match.group(1)}_{{{match.group(2)}}}$"
            ),
            text,
        )

        return text

    # ---------------------------------------------------------
    # Square roots
    # ---------------------------------------------------------

    def _square_roots(self, text: str) -> str:
        """
        Convert:

            sqrt(x)
            sqrt(x+4)
            sqrt(25)

        into:

            $\\sqrt{x}$
            $\\sqrt{x+4}$
            $\\sqrt{25}$
        """

        pattern = re.compile(
            r"(?<![\w\\$])"
            r"sqrt"
            r"\(\s*"
            r"([^()]+?)"
            r"\s*\)",
            re.IGNORECASE,
        )

        return pattern.sub(
            lambda match: (
                f"$\\sqrt{{{match.group(1).strip()}}}$"
            ),
            text,
        )

    # ---------------------------------------------------------
    # Fractions
    # ---------------------------------------------------------

    def _fractions(self, text: str) -> str:
        """
        Convert simple fractions:

            2/3
            a/b
            (x+1)/(x-2)

        into LaTeX fractions.

        Parenthesized numerator/denominator are supported.
        """

        # Parenthesized fraction:
        #
        # (x+1)/(x-2)
        #
        parenthesized = re.compile(
            r"(?<![\w$])"
            r"\(\s*([^()]+?)\s*\)"
            r"\s*/\s*"
            r"\(\s*([^()]+?)\s*\)"
            r"(?![\w])",
        )

        text = parenthesized.sub(
            lambda match: (
                f"$\\frac"
                f"{{{match.group(1).strip()}}}"
                f"{{{match.group(2).strip()}}}$"
            ),
            text,
        )

        # Simple fraction:
        #
        # 2/3
        # a/b
        # x/5
        simple = re.compile(
            r"(?<![\w$])"
            r"([A-Za-z0-9]+)"
            r"\s*/\s*"
            r"([A-Za-z0-9]+)"
            r"(?![\w])",
        )

        text = simple.sub(
            lambda match: (
                f"$\\frac"
                f"{{{match.group(1)}}}"
                f"{{{match.group(2)}}}$"
            ),
            text,
        )

        return text

    # ---------------------------------------------------------
    # Powers
    # ---------------------------------------------------------

    def _powers(self, text: str) -> str:
        """
        Convert:

            x^2
            x^10
            10^3
            a^n

        into:

            $x^{2}$
            $x^{10}$
            $10^{3}$
            $a^{n}$

        Avoids changing already formatted LaTeX.
        """

        pattern = re.compile(
            r"(?<![\w\\$])"
            r"([A-Za-z0-9]+)"
            r"\^"
            r"([A-Za-z0-9]+)"
            r"(?![\w])",
        )

        return pattern.sub(
            lambda match: (
                f"${match.group(1)}^{{{match.group(2)}}}$"
            ),
            text,
        )

    # ---------------------------------------------------------
    # Subscripts
    # ---------------------------------------------------------

    def _subscripts(self, text: str) -> str:
        """
        Convert:

            x_1
            y_2
            a_n

        into:

            $x_{1}$
            $y_{2}$
            $a_{n}$

        Existing LaTeX remains protected.
        """

        pattern = re.compile(
            r"(?<![\w\\$])"
            r"([A-Za-z]+)"
            r"_"
            r"([A-Za-z0-9]+)"
            r"(?![\w])",
        )

        return pattern.sub(
            lambda match: (
                f"${match.group(1)}_{{{match.group(2)}}}$"
            ),
            text,
        )

    # ---------------------------------------------------------
    # Degrees
    # ---------------------------------------------------------

    def _degrees(self, text: str) -> str:
        """
        Convert:

            90 degrees
            45 degree

        into:

            $90^\\circ$
            $45^\\circ$
        """

        pattern = re.compile(
            r"(?<![\w$])"
            r"(\d+(?:\.\d+)?)"
            r"\s+degrees?"
            r"(?![\w])",
            re.IGNORECASE,
        )

        return pattern.sub(
            lambda match: (
                f"${match.group(1)}^\\circ$"
            ),
            text,
        )


# =============================================================
# Manual verification
# =============================================================

if __name__ == "__main__":
    formatter = MathFormatter()

    tests = [
        ("x^2", r"$x^{2}$"),
        ("2/3", r"$\frac{2}{3}$"),
        ("sqrt(x+4)", r"$\sqrt{x+4}$"),
        ("(x+1)/(x-2)", r"$\frac{x+1}{x-2}$"),
        ("1011 base 2", r"$1011_{2}$"),
        ("1011 base 10", r"$1011_{10}$"),
        ("7F base 16", r"$7F_{16}$"),
        ("1011_2", r"$1011_{2}$"),
        ("log base 2 of 8", r"$\log_{2}(8)$"),
        ("The answer is x^2.", r"The answer is $x^{2}$."),
        ("The formula is $x^2$.", r"The formula is $x^2$."),
        (
            r"Already formatted: $\frac{a}{b}$",
            r"Already formatted: $\frac{a}{b}$",
        ),
        (
            r"Already formatted: $\sqrt{x+4}$",
            r"Already formatted: $\sqrt{x+4}$",
        ),
        ("x <= 5", r"x \le 5"),
        ("x >= 2", r"x \ge 2"),
        ("x != 3", r"x \ne 3"),
        ("90 degrees", r"$90^\circ$"),
    ]

    passed = 0

    for source, expected in tests:
        result = formatter.format(source)

        print(f"INPUT : {source}")
        print(f"OUTPUT: {result}")
        print("-" * 60)

        if result == expected:
            passed += 1
        else:
            print(f"EXPECTED: {expected}")
            print()

    print(f"PASSED: {passed}/{len(tests)}")
