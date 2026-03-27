"""Front-matter parsing and serialization for Wiki-SharePoint Sync."""

from __future__ import annotations

import frontmatter
import yaml

from models import FrontMatterError


class FrontMatterParser:
    """Parse YAML front-matter from article files."""

    def parse(self, file_path: str) -> tuple[dict, str]:
        """Parse an article file and return ``(metadata_dict, markdown_body)``.

        Raises :class:`FrontMatterError` with the file path and a
        description when front-matter is malformed or missing.
        """
        try:
            post = frontmatter.load(file_path)
        except FileNotFoundError:
            raise FrontMatterError(f"{file_path}: file not found")
        except Exception as exc:
            raise FrontMatterError(f"{file_path}: failed to parse front-matter — {exc}") from exc

        if not post.metadata:
            raise FrontMatterError(f"{file_path}: missing or empty front-matter")

        return dict(post.metadata), post.content


class FrontMatterPrinter:
    """Serialize metadata dicts back to YAML front-matter strings."""

    def print(self, metadata: dict) -> str:
        """Return a YAML front-matter string with ``---`` delimiters."""
        body = yaml.dump(metadata, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return f"---\n{body}---\n"
