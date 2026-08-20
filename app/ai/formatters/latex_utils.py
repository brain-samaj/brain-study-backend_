from __future__ import annotations

import re


# ============================================================
# Existing LaTeX detection
# ============================================================

INLINE_MATH_PATTERN = re.compile(
    r"\$(?!\$)(.+?)(?<!\$)\$",
    re.DOTALL,
)

DISPLAY_MATH_PATTERN = re.compile(
    r"\$\$(.+?)\$\$",
    re.DOTALL,
)

ESCAPED_INLINE_MATH_PATTERN = re.compile(
    r"\\\((.+?)\\\)",
    re.DOTALL,
)

ESCAPED_DISPLAY_MATH_PATTERN = re.compile(
    r"\\\[(.+?)\\\]",
    re.DOTALL,
)


# ============================================================
# Common plain-text mathematical notation
# ============================================================

SUPERSCRIPT_PATTERN = re.compile(
    r"(?<![\w\\])([A-Za-z0-9]+)\^([A-Za-z0-9]+)"
)

FRACTION_PATTERN = re.compile(
    r"(?<![\w\\])"
    r"([A-Za-z0-9]+)"
    r"\s*/\s*"
    r"([A-Za-z0-9]+)"
    r"(?![\w])"
)

SQRT_PATTERN = re.compile(
    r"(?<![\w\\])sqrt\(\s*([^()]+?)\s*\)"
)

SUBSCRIPT_PATTERN = re.compile(
    r"(?<![\w\\])"
    r"([A-Za-z]+)"
    r"(\d+)"
    r"(?![\w])"
)


# ============================================================
# Plain-text mathematical structures
# ============================================================

QUADRATIC_PATTERN = re.compile(
    r"\b([A-Za-z])x2\s*([+-])\s*"
    r"([A-Za-z0-9]+)x\s*([+-])\s*"
    r"([A-Za-z0-9]+)\s*=\s*0\b"
)

COORDINATE_PATTERN = re.compile(
    r"\(\s*"
    r"([A-Za-z0-9_]+)\s*,\s*"
    r"([A-Za-z0-9_]+)"
    r"\s*\)"
)

DEGREE_PATTERN = re.compile(
    r"(?<![\w\\])(\d+(?:\.\d+)?)\s*degrees?\b",
    re.IGNORECASE,
)

PLUS_MINUS_PATTERN = re.compile(
    r"\+/-"
)

MULTIPLICATION_PATTERN = re.compile(
    r"(?<=\d)\s*[x×]\s*(?=\d)"
)


# ============================================================
# Chemistry
# ============================================================

CHEMICAL_FORMULA_PATTERN = re.compile(
    r"\b"
    r"(?:"
    r"[A-Z][a-z]?"
    r"(?:\d+)?"
    r"){2,}"
    r"\b"
)

CHEMICAL_ARROW_PATTERN = re.compile(
    r"(?<!\\)->"
)

CHEMICAL_EQUATION_PATTERN = re.compile(
    r"\b"
    r"[A-Z][A-Za-z0-9()]*"
    r"(?:\s*\+\s*[A-Z][A-Za-z0-9()]*)+"
    r"\s*(?:->|→|⇌|<->)"
    r"\s*"
    r"[A-Z][A-Za-z0-9()]*"
)


# ============================================================
# Helpers
# ============================================================

def is_latex_wrapped(text: str) -> bool:
    """
    Return True when the entire string is already wrapped in
    a single LaTeX math delimiter.
    """

    value = text.strip()

    if len(value) < 2:
        return False

    if value.startswith("$$") and value.endswith("$$"):
        return True

    if value.startswith("$") and value.endswith("$"):
        return True

    if value.startswith(r"\(") and value.endswith(r"\)"):
        return True

    if value.startswith(r"\[") and value.endswith(r"\]"):
        return True

    return False


def contains_latex(text: str) -> bool:
    """
    Detect whether text already contains LaTeX math.
    """

    return bool(
        DISPLAY_MATH_PATTERN.search(text)
        or INLINE_MATH_PATTERN.search(text)
        or ESCAPED_DISPLAY_MATH_PATTERN.search(text)
        or ESCAPED_INLINE_MATH_PATTERN.search(text)
    )


def wrap_inline_math(text: str) -> str:
    """
    Wrap an entire expression in inline LaTeX.

    Existing math delimiters are preserved.
    """

    if not text or not text.strip():
        return text

    value = text.strip()

    if is_latex_wrapped(value):
        return value

    return f"${value}$"


def wrap_display_math(text: str) -> str:
    """
    Wrap an entire expression in display LaTeX.
    """

    if not text or not text.strip():
        return text

    value = text.strip()

    if value.startswith("$$") and value.endswith("$$"):
        return value

    return f"$$\n{value}\n$$"


# ============================================================
# LaTeX protection
# ============================================================

def protect_latex(text: str) -> tuple[str, dict[str, str]]:
    """
    Replace existing LaTeX expressions with placeholders.

    This prevents later plain-text transformations from corrupting
    expressions that the AI has already formatted correctly.
    """

    placeholders: dict[str, str] = {}

    pattern = re.compile(
        r"\$\$.*?\$\$"
        r"|\$.*?\$"
        r"|\\\[.*?\\\]"
        r"|\\\(.*?\\\)",
        re.DOTALL,
    )

    def replace(match: re.Match[str]) -> str:
        key = f"__LATEX_PLACEHOLDER_{len(placeholders)}__"
        placeholders[key] = match.group(0)
        return key

    protected = pattern.sub(replace, text)

    return protected, placeholders


def restore_latex(
    text: str,
    placeholders: dict[str, str],
) -> str:
    """
    Restore protected LaTeX expressions.
    """

    for key, value in placeholders.items():
        text = text.replace(key, value)

    return text


# ============================================================
# Cleanup
# ============================================================

def normalize_latex_spacing(text: str) -> str:
    """
    Normalize harmless spacing without changing mathematical meaning.
    """

    if not text:
        return text

    text = text.replace("$$ ", "$$")
    text = text.replace(" $$", "$$")

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    return text.strip()


def normalize_math_symbols(text: str) -> str:
    """
    Convert common Unicode/plain-text mathematical symbols into
    LaTeX-compatible forms.
    """

    replacements = {
        "×": r"\times ",
        "÷": r"\div ",
        "≤": r"\le ",
        "≥": r"\ge ",
        "≠": r"\ne ",
        "≈": r"\approx ",
        "∞": r"\infty ",
        "→": r"\rightarrow ",
        "←": r"\leftarrow ",
        "↔": r"\leftrightarrow ",
        "±": r"\pm ",
        "∓": r"\mp ",
        "∑": r"\sum ",
        "√": r"\sqrt{}",
        "π": r"\pi ",
        "Δ": r"\Delta ",
        "θ": r"\theta ",
        "α": r"\alpha ",
        "β": r"\beta ",
        "γ": r"\gamma ",
        "λ": r"\lambda ",
        "μ": r"\mu ",
        "σ": r"\sigma ",
        "ω": r"\omega ",
    }

    for source, target in replacements.items():
        text = text.replace(source, target)

    return text
