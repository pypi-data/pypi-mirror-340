#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for pyccup focusing on element ordering issues.
"""

import unittest

import src.pyccup.elems as e
from src.pyccup.core import convert


class OrderingTest(unittest.TestCase):
    """Test cases specifically for element ordering issues."""

    def test_multiple_string_elements(self):
        """Test that multiple string elements are preserved in correct order."""
        # Test arrow followed by text
        result = convert(
            ["a", {"class": "prev-post", "href": "/prev"}, "<-", "Previous Post"]
        )
        self.assertEqual(
            result, '<a class="prev-post" href="/prev"><-Previous Post</a>'
        )

        # Test text followed by arrow
        result = convert(
            ["a", {"class": "next-post", "href": "/next"}, "Next Post", "->"]
        )
        self.assertEqual(result, '<a class="next-post" href="/next">Next Post-></a>')

        # Test multiple text segments
        result = convert(["span", "First", " ", "Second", " ", "Third"])
        self.assertEqual(result, "<span>First Second Third</span>")

    def test_mixed_string_and_element_ordering(self):
        """Test that strings and nested elements maintain correct ordering."""
        # String before element
        result = convert(["p", "Text before ", ["em", "emphasized"], " text."])
        self.assertEqual(result, "<p>Text before <em>emphasized</em> text.</p>")

        # String after element
        result = convert(["p", ["strong", "Strong"], " followed by text."])
        self.assertEqual(result, "<p><strong>Strong</strong> followed by text.</p>")

        # Multiple mixed strings and elements
        result = convert(
            ["p", "Start ", ["em", "middle"], " end ", ["strong", "strong end"]]
        )
        self.assertEqual(
            result, "<p>Start <em>middle</em> end <strong>strong end</strong></p>"
        )

    def test_complex_nesting_with_strings(self):
        """Test more complex nesting scenarios with strings interspersed."""
        result = convert(
            [
                "div",
                "Start of div ",
                ["p", "Paragraph with ", ["code", "code block"], " inside"],
                " text between elements ",
                [
                    "ul",
                    ["li", "Item 1"],
                    ["li", "Item ", ["strong", "2"], " continued"],
                ],
            ]
        )

        expected = (
            "<div>Start of div "
            "<p>Paragraph with <code>code block</code> inside</p>"
            " text between elements "
            "<ul><li>Item 1</li><li>Item <strong>2</strong> continued</li></ul></div>"
        )
        self.assertEqual(result, expected)

    def test_empty_elements(self):
        """Test that empty strings don't disrupt element order."""
        result = convert(["p", "", ["em", "emphasized"], "", ["strong", "strong"], ""])
        self.assertEqual(result, "<p><em>emphasized</em><strong>strong</strong></p>")

        # Mixing empty and non-empty strings
        result = convert(["p", "", "Text", "", ["em", "emphasized"], ""])
        self.assertEqual(result, "<p>Text<em>emphasized</em></p>")

    def test_script_tag_ordering(self):
        """Test script tag content ordering which was specifically mentioned as an issue."""
        # Script with src followed by initialization script
        script_block = [
            [
                "script",
                {"type": "text/javascript", "src": "/static/js/highlight.pack.js"},
            ],
            ["script", {"type": "text/javascript"}, "hljs.initHighlightingOnLoad();"],
        ]

        result = convert(script_block)
        expected = (
            '<script src="/static/js/highlight.pack.js" type="text/javascript"></script>'
            '<script type="text/javascript">hljs.initHighlightingOnLoad();</script>'
        )
        self.assertEqual(result, expected)

    def test_using_elems_module(self):
        """Test that the elems module works with ordering fixes."""
        result = convert(
            [
                e.div,
                [e.P, "Text with ", [e.strong, "strong"], " content"],
                [e.P, "Another ", [e.em, "paragraph"], " here"],
            ]
        )

        expected = (
            "<div>"
            "<p>Text with <strong>strong</strong> content</p>"
            "<p>Another <em>paragraph</em> here</p>"
            "</div>"
        )
        self.assertEqual(result, expected)

    def test_mixed_case_tags(self):
        """Test that mixed case tag variants work properly."""
        # Mix uppercase and lowercase tags
        result = convert(
            [
                e.DIV,
                [e.p, "Lowercase p"],
                [e.P, "Uppercase P"],
                [e.span, "Lowercase span"],
                [e.SPAN, "Uppercase SPAN"],
            ]
        )

        expected = (
            "<div>"
            "<p>Lowercase p</p>"
            "<p>Uppercase P</p>"
            "<span>Lowercase span</span>"
            "<span>Uppercase SPAN</span>"
            "</div>"
        )
        self.assertEqual(result, expected)

    def test_attributes_with_ordering(self):
        """Test that attributes don't disrupt content ordering."""
        result = convert(
            [
                "a",
                {"href": "/link", "class": "button"},
                "Click ",
                ["span", {"class": "icon"}, "→"],
                " here",
            ]
        )

        expected = (
            '<a class="button" href="/link">Click <span class="icon">→</span> here</a>'
        )
        self.assertEqual(result, expected)

    def test_self_closing_tags(self):
        """Test that self-closing tags are handled properly within content."""
        result = convert(["p", "Line one", ["br"], "Line two", ["br"], "Line three"])

        expected = "<p>Line one<br/>Line two<br/>Line three</p>"
        self.assertEqual(result, expected)

    def test_deeply_nested_structures(self):
        """Test deeply nested structures with interleaved text."""
        deep_structure = [
            "div",
            {"id": "root"},
            "Root text ",
            [
                "div",
                {"class": "level1"},
                "Level 1 text ",
                [
                    "div",
                    {"class": "level2"},
                    "Level 2 text ",
                    ["div", {"class": "level3"}, "Level 3 text"],
                ],
            ],
        ]

        result = convert(deep_structure)
        expected = (
            '<div id="root">Root text '
            '<div class="level1">Level 1 text '
            '<div class="level2">Level 2 text '
            '<div class="level3">Level 3 text</div>'
            "</div>"
            "</div>"
            "</div>"
        )
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
