"""Tests for the commands.create module."""
import os

from cookie_composer.commands import create


def test_render_template(fixtures_path, tmp_path):
    """Test rendering a single template."""
    template_path = fixtures_path / "template1"
    project_path = create.create_cmd(str(template_path), tmp_path, no_input=True)
    rendered_items = {item.name for item in os.scandir(project_path)}

    assert rendered_items == {"README.md", "requirements.txt", ".composition.yaml"}


def test_render_composition(fixtures_path, tmp_path):
    """Test rendering a composition file."""
    template_path = fixtures_path / "multi-template.yaml"
    project_path = create.create_cmd(str(template_path), tmp_path, no_input=True)
    rendered_items = {item.name for item in os.scandir(project_path)}

    assert rendered_items == {"ABOUT.md", "README.md", "requirements.txt", ".composition.yaml"}
