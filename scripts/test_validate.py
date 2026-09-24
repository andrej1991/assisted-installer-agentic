import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from validate import Validator


REPO_ROOT = Path(__file__).resolve().parents[1]


class ValidatorTests(unittest.TestCase):
    def test_dependency_requires_matching_marketplace_registration(self):
        for qualified in (False, True):
            for registration in ("valid", "absent", "wrong-source", "duplicate"):
                with self.subTest(qualified=qualified, registration=registration):
                    with tempfile.TemporaryDirectory() as directory:
                        root = Path(directory)
                        dependency = "shared"
                        if qualified:
                            dependency = {"name": "shared", "marketplace": "sample"}
                        claude_entries = []
                        codex_entries = []
                        for name in ("workflow", "shared"):
                            plugin = root / "plugins" / name
                            (plugin / "skills").mkdir(parents=True)
                            for harness in (".claude-plugin", ".codex-plugin"):
                                manifest = {"name": name, "version": "0.1.0"}
                                if name == "workflow" and harness == ".claude-plugin":
                                    manifest["dependencies"] = [dependency]
                                (plugin / harness).mkdir()
                                (plugin / harness / "plugin.json").write_text(
                                    json.dumps(manifest), encoding="utf-8"
                                )
                            source = f"./plugins/{name}"
                            claude_entries.append({"name": name, "source": source})
                            codex_entries.append({
                                "name": name,
                                "source": {"source": "local", "path": source},
                                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                                "category": "Developer Tools",
                            })
                        if registration == "absent":
                            claude_entries.pop()
                        elif registration == "wrong-source":
                            claude_entries[-1]["source"] = "./plugins/workflow"
                        elif registration == "duplicate":
                            claude_entries.append(claude_entries[-1].copy())
                        (root / ".claude-plugin").mkdir()
                        (root / ".claude-plugin" / "marketplace.json").write_text(
                            json.dumps({"name": "sample", "plugins": claude_entries}),
                            encoding="utf-8",
                        )
                        (root / ".agents" / "plugins").mkdir(parents=True)
                        (root / ".agents" / "plugins" / "marketplace.json").write_text(
                            json.dumps({
                                "name": "sample",
                                "interface": {"displayName": "Sample"},
                                "plugins": codex_entries,
                            }), encoding="utf-8",
                        )
                        validator = Validator(root)
                        with contextlib.redirect_stdout(io.StringIO()):
                            result = validator.run("workflow")
                        if registration == "valid":
                            self.assertEqual(result, 0, validator.errors)
                        else:
                            self.assertEqual(result, 1, validator.errors)
                            expected = {
                                "absent": "dependency not registered in Claude marketplace: shared",
                                "wrong-source": "plugin source must resolve to plugins/shared",
                                "duplicate": "duplicate plugin name: shared",
                            }[registration]
                            self.assertTrue(any(expected in error for error in validator.errors), validator.errors)

    def test_repository_is_valid(self):
        validator = Validator(REPO_ROOT)
        self.assertEqual(validator.run(), 0, validator.errors)

    def test_single_skill_is_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin = root / "plugins" / "sample-plugin"
            skill = plugin / "skills" / "sample"
            (plugin / ".claude-plugin").mkdir(parents=True)
            (plugin / ".codex-plugin").mkdir()
            skill.mkdir(parents=True)
            (plugin / ".claude-plugin" / "plugin.json").write_text(
                '{"name": "sample-plugin", "version": "0.1.0"}\n',
                encoding="utf-8",
            )
            (plugin / ".codex-plugin" / "plugin.json").write_text(
                '{"name": "sample-plugin", "version": "0.1.0"}\n',
                encoding="utf-8",
            )
            (root / ".claude-plugin").mkdir()
            (root / ".claude-plugin" / "marketplace.json").write_text(
                '{"name": "sample", "plugins": [{"name": "sample-plugin", '
                '"source": "plugins/sample-plugin"}]}\n',
                encoding="utf-8",
            )
            (root / ".agents" / "plugins").mkdir(parents=True)
            (root / ".agents" / "plugins" / "marketplace.json").write_text(
                '{"name": "sample", "interface": {"displayName": "Sample"}, '
                '"plugins": [{"name": "sample-plugin", "source": {"source": "local", '
                '"path": "./plugins/sample-plugin"}, "policy": {"installation": "AVAILABLE", '
                '"authentication": "ON_INSTALL"}, "category": "Developer Tools"}]}\n',
                encoding="utf-8",
            )
            (skill / "SKILL.md").write_text(
                "---\nname: sample\ndescription: sample\n---\n",
                encoding="utf-8",
            )
            validator = Validator(root)
            with contextlib.redirect_stdout(io.StringIO()):
                result = validator.run("sample-plugin")
            self.assertEqual(result, 0, validator.errors)

    def test_invalid_skill_name_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin = root / "plugins" / "sample-plugin"
            skill = plugin / "skills" / "sample"
            skill.mkdir(parents=True)
            (plugin / ".claude-plugin").mkdir(parents=True)
            (plugin / ".codex-plugin").mkdir()
            (plugin / ".claude-plugin" / "plugin.json").write_text(
                '{"name": "sample-plugin", "version": "0.1.0"}\n',
                encoding="utf-8",
            )
            (plugin / ".codex-plugin" / "plugin.json").write_text(
                '{"name": "sample-plugin", "version": "0.1.0"}\n',
                encoding="utf-8",
            )
            (root / ".claude-plugin").mkdir()
            (root / ".claude-plugin" / "marketplace.json").write_text(
                '{"name": "sample", "owner": {"name": "test"}, '
                '"plugins": [{"name": "sample-plugin", "source": "plugins/sample-plugin"}]}\n',
                encoding="utf-8",
            )
            (root / ".agents" / "plugins").mkdir(parents=True)
            (root / ".agents" / "plugins" / "marketplace.json").write_text(
                '{"name": "sample", "interface": {"displayName": "Sample"}, '
                '"plugins": [{"name": "sample-plugin", "source": {"source": "local", '
                '"path": "./plugins/sample-plugin"}, "policy": {"installation": "AVAILABLE", '
                '"authentication": "ON_INSTALL"}, "category": "Developer Tools"}]}\n',
                encoding="utf-8",
            )
            (skill / "SKILL.md").write_text(
                "---\nname: wrong\ndescription: sample\n---\n",
                encoding="utf-8",
            )
            validator = Validator(root)
            with contextlib.redirect_stdout(io.StringIO()):
                result = validator.run("sample-plugin")
            self.assertEqual(result, 1)
            self.assertTrue(any("name must be sample" in error for error in validator.errors))


if __name__ == "__main__":
    unittest.main()
