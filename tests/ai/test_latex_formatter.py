from app.ai.formatters import LatexFormatter


formatter = LatexFormatter()


def test_fraction():
    result = formatter.format_payload(
        {"question": "Solve x/y"}
    )
    assert "\\frac{x}{y}" in result["question"]


def test_square_root():
    result = formatter.format_payload(
        {"question": "Find sqrt(x)"}
    )
    assert "\\sqrt{x}" in result["question"]


def test_exponent():
    result = formatter.format_payload(
        {"question": "Evaluate x^2"}
    )
    assert "x^{2}" in result["question"]


def test_chemistry():
    result = formatter.format_payload(
        {"question": "H2SO4"}
    )
    assert "\\mathrm{H_2SO_4}" in result["question"]


def test_reaction():
    result = formatter.format_payload(
        {"question": "2H2 + O2 -> 2H2O"}
    )
    assert "\\rightarrow" in result["question"]


def test_existing_latex_is_preserved():
    result = formatter.format_payload(
        {"question": "$\\frac{x}{2}$"}
    )
    assert result["question"] == "$\\frac{x}{2}$"


def test_plain_text_not_modified():
    text = "Explain the importance of education."

    result = formatter.format_payload(
        {"question": text}
    )

    assert result["question"] == text
