# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = ["pyyaml>=6,<7", "jsonschema>=4,<5"]
# ///
"""Validate distributable skills and the Scuba configuration contract."""

import json
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        raise ValueError("No skills found")

    for skill in skills:
        match = re.match(r"\A---\n(.*?)\n---\n", skill.read_text(), re.DOTALL)
        if match is None:
            raise ValueError(f"Missing frontmatter: {skill}")
        metadata = yaml.safe_load(match.group(1))
        name = metadata["name"]
        if name != skill.parent.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"Invalid skill name: {name}")
        if len(name) > 64 or not 1 <= len(metadata["description"]) <= 1024:
            raise ValueError(f"Invalid metadata length: {skill}")

        interface = yaml.safe_load((skill.parent / "agents/openai.yaml").read_text())
        dependency = interface["dependencies"]["tools"][0]
        if dependency != {
            "type": "mcp",
            "value": "scuba",
            "description": "Scuba capture library and shared collections",
            "transport": "streamable_http",
            "url": "https://api.scuba.app/mcp/",
        }:
            raise ValueError(f"Unexpected MCP dependency: {skill}")
        if f"${name}" not in interface["interface"]["default_prompt"]:
            raise ValueError(f"Default prompt must name its skill: {skill}")

        for markdown in skill.parent.rglob("*.md"):
            check_links(markdown, skill.parent)

    for markdown in [root / "README.md", *(root / "docs").glob("*.md")]:
        check_links(markdown, root)

    assets = root / "skills/scuba-setup/assets"
    schema = json.loads((assets / "scuba-config.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    example = json.loads((assets / "scuba-config.example.json").read_text())
    if validator.is_valid(example):
        raise ValueError("Example must require the user to choose a real destination")
    example["engineering_memory"]["collection_id"] = "123e4567-e89b-42d3-a456-426614174000"
    validator.validate(example)
    for invalid in [
        {},
        {**example, "version": 2},
        {**example, "token": "not-a-real-token"},
        {**example, "engineering_memory": {"collection_id": "not-a-uuid"}},
        {**example, "engineering_memory": {"collection": "123e4567-e89b-42d3-a456-426614174000"}},
    ]:
        if validator.is_valid(invalid):
            raise ValueError(f"Invalid configuration accepted: {invalid}")
    print(f"Validated {len(skills)} skills, packaged links, MCP metadata, and configuration schema.")


def check_links(markdown: Path, boundary: Path) -> None:
    for target in re.findall(r"\]\(([^)]+)\)", markdown.read_text()):
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
            continue
        path = (markdown.parent / target.split("#", 1)[0]).resolve()
        if not path.is_relative_to(boundary.resolve()) or not path.exists():
            raise ValueError(f"Missing or unbundled reference in {markdown}: {target}")


if __name__ == "__main__":
    main()
