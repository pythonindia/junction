from junction.proposals.services import markdown_to_html


def test_markdown_to_html():
    markdown = '#test'
    html = markdown_to_html(markdown)
    assert html == '<h1 id="test">test</h1>\n'
