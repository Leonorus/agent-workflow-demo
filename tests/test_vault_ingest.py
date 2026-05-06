from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from agent_workflow_demo.vault import build_index, write_index

ROOT = Path(__file__).parent / "fixtures" / "vault-clean"


class VaultIngestTests(unittest.TestCase):
    def test_build_index_is_deterministic(self) -> None:
        index = build_index(ROOT)
        self.assertEqual([doc.path for doc in index.docs], ["index.md", "notes/good-note.md"])
        self.assertEqual([doc.title for doc in index.docs], ["Clean Index", "Good Note"])

    def test_extracts_links_tags_and_word_count(self) -> None:
        index = build_index(ROOT)
        home = index.docs[0]
        self.assertEqual(home.links, ["Good Note"])
        self.assertEqual(home.tags, ["demo"])
        self.assertGreater(home.word_count, 3)

    def test_write_index_json(self) -> None:
        index = build_index(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "vault-index.json"
            write_index(index, out)
            payload = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(payload["docs"][0]["path"], "index.md")
        self.assertEqual(payload["docs"][1]["title"], "Good Note")


if __name__ == "__main__":
    unittest.main()
