import shutil
import tempfile
import unittest
from pathlib import Path

from test_support import create_repo
from validate import Validator


REPO_ROOT = Path(__file__).resolve().parents[1]


class PluginIsolationTests(unittest.TestCase):
  def test_each_plugin_validates_without_checkout_or_sibling_plugins(self):
    for source in sorted((REPO_ROOT / "plugins").iterdir()):
      if not source.is_dir():
        continue
      with self.subTest(plugin=source.name):
        with tempfile.TemporaryDirectory() as directory:
          root = Path(directory)
          plugin = root / source.name
          shutil.copytree(source, plugin, symlinks=True)
          validator = Validator(root)
          validator.validate_plugin_manifest(plugin)
          validator.validate_plugin_contents(plugin)
          self.assertEqual(validator.errors, [])

  def test_isolated_plugin_cannot_use_checkout_only_references(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      checkout = root / "checkout"
      create_repo(checkout)
      skill = checkout / "plugins/workflow/skills/workflow-skill/SKILL.md"
      with skill.open("a", encoding="utf-8") as output:
        output.write("\n[Repository](../../../../README.md)\n")
      isolated = root / "isolated"
      plugin = isolated / "workflow"
      shutil.copytree(checkout / "plugins/workflow", plugin, symlinks=True)
      checkout.rename(root / "unavailable-checkout")
      validator = Validator(isolated)
      validator.validate_plugin_contents(plugin)
      self.assertTrue(
        any("link escapes plugin package" in error for error in validator.errors),
        validator.errors,
      )

  def test_isolated_plugin_requires_its_supporting_files(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      create_repo(root / "checkout")
      isolated = root / "isolated"
      plugin = isolated / "workflow"
      shutil.copytree(root / "checkout/plugins/workflow", plugin, symlinks=True)
      (plugin / "skills/workflow-skill/references/guide.md").unlink()
      validator = Validator(isolated)
      validator.validate_plugin_contents(plugin)
      self.assertTrue(
        any("missing link target" in error for error in validator.errors),
        validator.errors,
      )


if __name__ == "__main__":
  unittest.main()
