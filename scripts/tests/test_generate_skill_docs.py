"""Tests for scripts/generate_skill_docs.py."""

from __future__ import annotations

# Import from parent scripts/ directory
import sys
import textwrap
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from generate_skill_docs import (
    _slugify,
    _split_sections,
    _title_case,
    api_badges,
    generate_en_page,
    generate_ja_page,
    main,
    parse_api_requirements,
    parse_cli_examples,
    parse_skill_md,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_skill(tmp_path):
    """Create a minimal skill directory with SKILL.md."""
    skill_dir = tmp_path / "skills" / "test-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        textwrap.dedent("""\
        ---
        name: test-skill
        description: A test skill for unit testing the doc generator.
        ---

        # Test Skill

        ## Overview

        This is a test skill that does testing things.

        ## When to Use

        Use when testing the documentation generator.

        ## Prerequisites

        - Python 3.9+
        - No API key required

        ## Workflow

        ### Step 1: Run the test

        ```bash
        python3 scripts/test_runner.py --output-dir reports/
        ```

        ### Step 2: Review results

        Check the output in reports/ directory.
        """)
    )
    refs_dir = skill_dir / "references"
    refs_dir.mkdir()
    (refs_dir / "methodology.md").write_text("# Methodology\n")

    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "test_runner.py").write_text("#!/usr/bin/env python3\n")

    return tmp_path


@pytest.fixture
def tmp_claude_md(tmp_path):
    """Create a minimal CLAUDE.md with API requirements table."""
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text(
        textwrap.dedent("""\
        # CLAUDE.md

        #### API Requirements by Skill

        | Skill | FMP API | FINVIZ Elite | Alpaca | Notes |
        |-------|---------|--------------|--------|-------|
        | **Test Skill** | ✅ Required | ❌ Not used | ❌ Not used | Test notes |
        | **Free Skill** | ❌ Not required | ❌ Not used | ❌ Not used | No API needed |
        | **Optional Skill** | 🟡 Optional | 🟡 Optional (Recommended) | ❌ Not used | Both optional |
        | **Alpaca Skill** | ❌ Not required | ❌ Not used | ✅ Required | Needs Alpaca |

        ### Running Helper Scripts

        **Test Skill:** ⚠️ Requires FMP API key
        ```bash
        python3 skills/test-skill/scripts/test_runner.py --output-dir reports/
        ```
        """)
    )
    return claude_md


# ---------------------------------------------------------------------------
# Tests: SKILL.md parser
# ---------------------------------------------------------------------------


class TestParseSkillMd:
    def test_parses_frontmatter(self, tmp_skill):
        data = parse_skill_md(tmp_skill / "skills" / "test-skill" / "SKILL.md")
        assert data["frontmatter"]["name"] == "test-skill"
        assert "unit testing" in data["frontmatter"]["description"]

    def test_parses_sections(self, tmp_skill):
        data = parse_skill_md(tmp_skill / "skills" / "test-skill" / "SKILL.md")
        assert "overview" in data["sections"]
        assert "when to use" in data["sections"]
        assert "workflow" in data["sections"]

    def test_no_frontmatter_returns_empty(self, tmp_path):
        md = tmp_path / "SKILL.md"
        md.write_text("# Just a title\n\nSome content.")
        data = parse_skill_md(md)
        assert data["frontmatter"] == {}


class TestSplitSections:
    def test_basic_split(self):
        body = "## Overview\n\nHello world.\n\n## Workflow\n\nDo stuff."
        sections = _split_sections(body)
        assert "overview" in sections
        assert "Hello world." in sections["overview"]
        assert "workflow" in sections
        assert "Do stuff." in sections["workflow"]

    def test_empty_body(self):
        assert _split_sections("") == {}


# ---------------------------------------------------------------------------
# Tests: CLAUDE.md parsers
# ---------------------------------------------------------------------------


class TestParseApiRequirements:
    def test_parses_table(self, tmp_claude_md):
        reqs = parse_api_requirements(tmp_claude_md)
        assert "test-skill" in reqs
        assert "Required" in reqs["test-skill"]["fmp"]

    def test_free_skill(self, tmp_claude_md):
        reqs = parse_api_requirements(tmp_claude_md)
        assert "free-skill" in reqs
        assert "Not required" in reqs["free-skill"]["fmp"]

    def test_optional_skill(self, tmp_claude_md):
        reqs = parse_api_requirements(tmp_claude_md)
        assert "optional-skill" in reqs
        assert "Optional" in reqs["optional-skill"]["fmp"]

    def test_alpaca_skill(self, tmp_claude_md):
        reqs = parse_api_requirements(tmp_claude_md)
        assert "alpaca-skill" in reqs
        assert "Required" in reqs["alpaca-skill"]["alpaca"]


class TestParseCLIExamples:
    def test_extracts_code_block(self, tmp_claude_md):
        examples = parse_cli_examples(tmp_claude_md)
        assert "test-skill" in examples
        assert "test_runner.py" in examples["test-skill"]


# ---------------------------------------------------------------------------
# Tests: Badge generation
# ---------------------------------------------------------------------------


class TestApiBadges:
    def test_no_api(self):
        assert "badge-free" in api_badges(None)

    def test_fmp_required(self):
        badges = api_badges({"fmp": "✅ Required", "finviz": "❌", "alpaca": "❌"})
        assert "badge-api" in badges
        assert "FMP Required" in badges

    def test_optional_shows_both(self):
        badges = api_badges({"fmp": "🟡 Optional", "finviz": "🟡 Optional", "alpaca": "❌"})
        assert "badge-free" in badges
        assert "badge-optional" in badges

    def test_alpaca_required(self):
        badges = api_badges({"fmp": "❌", "finviz": "❌", "alpaca": "✅ Required"})
        assert "Alpaca Required" in badges


# ---------------------------------------------------------------------------
# Tests: Title and slug helpers
# ---------------------------------------------------------------------------


class TestTitleCase:
    def test_basic(self):
        assert _title_case("earnings-trade-analyzer") == "Earnings Trade Analyzer"

    def test_acronyms(self):
        assert _title_case("us-stock-analysis") == "US Stock Analysis"
        assert _title_case("vcp-screener") == "VCP Screener"
        assert _title_case("pead-screener") == "PEAD Screener"

    def test_slugify(self):
        assert _slugify("Test Skill") == "test-skill"
        assert _slugify("**Bold Name**") == "bold-name"


# ---------------------------------------------------------------------------
# Tests: Page generation
# ---------------------------------------------------------------------------


class TestGenerateEnPage:
    def test_contains_frontmatter(self, tmp_skill):
        data = parse_skill_md(tmp_skill / "skills" / "test-skill" / "SKILL.md")
        page = generate_en_page(
            "test-skill", data, None, None, 11, {"references": [], "scripts": []}
        )
        assert "layout: default" in page
        assert 'title: "Test Skill"' in page
        assert "nav_order: 11" in page
        assert "grand_parent: English" in page

    def test_contains_overview(self, tmp_skill):
        data = parse_skill_md(tmp_skill / "skills" / "test-skill" / "SKILL.md")
        page = generate_en_page(
            "test-skill", data, None, None, 11, {"references": [], "scripts": []}
        )
        assert "testing things" in page

    def test_contains_workflow(self, tmp_skill):
        data = parse_skill_md(tmp_skill / "skills" / "test-skill" / "SKILL.md")
        page = generate_en_page(
            "test-skill", data, None, None, 11, {"references": [], "scripts": []}
        )
        assert "test_runner.py" in page

    def test_api_badges_included(self, tmp_skill):
        data = parse_skill_md(tmp_skill / "skills" / "test-skill" / "SKILL.md")
        api = {"fmp": "✅ Required", "finviz": "❌", "alpaca": "❌"}
        page = generate_en_page(
            "test-skill", data, api, None, 11, {"references": [], "scripts": []}
        )
        assert "badge-api" in page

    def test_resources_listed(self, tmp_skill):
        data = parse_skill_md(tmp_skill / "skills" / "test-skill" / "SKILL.md")
        resources = {"references": ["methodology.md"], "scripts": ["test_runner.py"]}
        page = generate_en_page("test-skill", data, None, None, 11, resources)
        assert "methodology.md" in page
        assert "test_runner.py" in page


class TestGenerateJaPage:
    def test_contains_ja_frontmatter(self, tmp_skill):
        data = parse_skill_md(tmp_skill / "skills" / "test-skill" / "SKILL.md")
        page = generate_ja_page("test-skill", data, None, 11)
        assert "grand_parent: 日本語" in page
        assert "parent: スキルガイド" in page

    def test_contains_translation_banner(self, tmp_skill):
        data = parse_skill_md(tmp_skill / "skills" / "test-skill" / "SKILL.md")
        page = generate_ja_page("test-skill", data, None, 11)
        assert "not yet been translated" in page

    def test_links_to_en_version(self, tmp_skill):
        data = parse_skill_md(tmp_skill / "skills" / "test-skill" / "SKILL.md")
        page = generate_ja_page("test-skill", data, None, 11)
        assert "/en/skills/test-skill/" in page


# ---------------------------------------------------------------------------
# Tests: End-to-end main()
# ---------------------------------------------------------------------------


class TestMain:
    def test_generates_pages(self, tmp_skill, tmp_claude_md):
        docs_dir = tmp_skill / "docs"
        (docs_dir / "en" / "skills").mkdir(parents=True)
        (docs_dir / "ja" / "skills").mkdir(parents=True)

        result = main(
            [
                "--skills-dir",
                str(tmp_skill / "skills"),
                "--docs-dir",
                str(docs_dir),
                "--claude-md",
                str(tmp_claude_md),
            ]
        )
        assert result == 0
        assert (docs_dir / "en" / "skills" / "test-skill.md").exists()
        assert (docs_dir / "ja" / "skills" / "test-skill.md").exists()

    def test_skips_hand_written(self, tmp_skill, tmp_claude_md):
        # Create a skill that matches HAND_WRITTEN
        hw_skill = tmp_skill / "skills" / "backtest-expert"
        hw_skill.mkdir()
        (hw_skill / "SKILL.md").write_text("---\nname: backtest-expert\ndescription: test\n---\n")

        docs_dir = tmp_skill / "docs"
        (docs_dir / "en" / "skills").mkdir(parents=True)
        (docs_dir / "ja" / "skills").mkdir(parents=True)

        main(
            [
                "--skills-dir",
                str(tmp_skill / "skills"),
                "--docs-dir",
                str(docs_dir),
                "--claude-md",
                str(tmp_claude_md),
            ]
        )
        # backtest-expert should not be generated (hand-written)
        assert not (docs_dir / "en" / "skills" / "backtest-expert.md").exists()

    def test_overwrite_regenerates(self, tmp_skill, tmp_claude_md):
        docs_dir = tmp_skill / "docs"
        en_path = docs_dir / "en" / "skills" / "test-skill.md"
        en_path.parent.mkdir(parents=True)
        (docs_dir / "ja" / "skills").mkdir(parents=True)
        en_path.write_text("old content")

        main(
            [
                "--skills-dir",
                str(tmp_skill / "skills"),
                "--docs-dir",
                str(docs_dir),
                "--claude-md",
                str(tmp_claude_md),
                "--overwrite",
            ]
        )
        assert "old content" not in en_path.read_text()
        assert "Test Skill" in en_path.read_text()

    def test_skips_dir_without_skill_md(self, tmp_skill, tmp_claude_md):
        # Create a directory without SKILL.md
        (tmp_skill / "skills" / "empty-skill").mkdir()

        docs_dir = tmp_skill / "docs"
        (docs_dir / "en" / "skills").mkdir(parents=True)
        (docs_dir / "ja" / "skills").mkdir(parents=True)

        main(
            [
                "--skills-dir",
                str(tmp_skill / "skills"),
                "--docs-dir",
                str(docs_dir),
                "--claude-md",
                str(tmp_claude_md),
            ]
        )
        assert not (docs_dir / "en" / "skills" / "empty-skill.md").exists()
