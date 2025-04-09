from bs4 import BeautifulSoup


def assert_html_has_script_tag_with_src(html: str, expected_src: str) -> None:
    soup = BeautifulSoup(html, "html.parser")
    elements = [
        e for e in soup.find_all("script") if e.get("src") == expected_src
    ]
    assert len(elements) == 1


def assert_revealjs_script_tag_with_code(
    html: str, expected_code: str
) -> None:
    soup = BeautifulSoup(html, "html.parser")
    revealjs_script = soup.find_all("script")[-1]
    assert expected_code in str(revealjs_script)
