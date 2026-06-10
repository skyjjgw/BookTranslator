import hashlib
import json
import os
import sqlite3
from typing import Optional

try:
    from BookTranslator.book.content import ContentType
    from BookTranslator.utils.log_utils import log
except ModuleNotFoundError:
    from book.content import ContentType
    from utils.log_utils import log


class MemoryStore:
    """
    Lightweight agent memory for document translation.
    Stores:
    - exact translation memory
    - table header terminology memory
    - page/content-level checkpoints
    """

    def __init__(self, db_path: str, enabled: bool = True, domain: str = "general"):
        self.enabled = enabled
        self.db_path = db_path
        self.domain = domain or "general"
        if not self.enabled:
            return

        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS translation_memory (
                    source_hash TEXT NOT NULL,
                    source_text TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    source_language TEXT NOT NULL,
                    target_language TEXT NOT NULL,
                    hit_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (source_hash, content_type, source_language, target_language)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS terminology_memory (
                    source_term TEXT NOT NULL,
                    target_term TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    source_language TEXT NOT NULL,
                    target_language TEXT NOT NULL,
                    hit_count INTEGER DEFAULT 0,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (source_term, domain, source_language, target_language)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS checkpoints (
                    file_path TEXT NOT NULL,
                    page_index INTEGER NOT NULL,
                    content_index INTEGER NOT NULL,
                    source_language TEXT NOT NULL,
                    target_language TEXT NOT NULL,
                    status TEXT NOT NULL,
                    translation TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (file_path, page_index, content_index, source_language, target_language)
                )
                """
            )

    def get_cached_translation(self, content, source_language: str, target_language: str) -> Optional[str]:
        if not self.enabled:
            return None

        source_text = self._content_to_string(content)
        source_hash = self._hash_text(source_text)

        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT translated_text FROM translation_memory
                WHERE source_hash = ? AND content_type = ? AND source_language = ? AND target_language = ?
                """,
                (source_hash, content.content_type.name, source_language, target_language),
            ).fetchone()
            if not row:
                return None

            conn.execute(
                """
                UPDATE translation_memory
                SET hit_count = hit_count + 1, updated_at = CURRENT_TIMESTAMP
                WHERE source_hash = ? AND content_type = ? AND source_language = ? AND target_language = ?
                """,
                (source_hash, content.content_type.name, source_language, target_language),
            )
        return row[0]

    def save_translation_memory(self, content, translated_text: str, source_language: str, target_language: str):
        if not self.enabled or not translated_text:
            return

        source_text = self._content_to_string(content)
        source_hash = self._hash_text(source_text)
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO translation_memory (
                    source_hash, source_text, translated_text, content_type, source_language, target_language
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(source_hash, content_type, source_language, target_language)
                DO UPDATE SET
                    translated_text = excluded.translated_text,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    source_hash,
                    source_text,
                    translated_text,
                    content.content_type.name,
                    source_language,
                    target_language,
                ),
            )

        if content.content_type == ContentType.TABLE:
            self._save_table_header_memory(content, translated_text, source_language, target_language)

    def build_memory_context(self, content, source_language: str, target_language: str, limit: int = 8) -> str:
        if not self.enabled:
            return ""

        source_text = self._content_to_string(content)
        source_text_lower = source_text.lower()
        matches = []

        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT source_term, target_term FROM terminology_memory
                WHERE domain = ? AND source_language = ? AND target_language = ?
                ORDER BY LENGTH(source_term) DESC, hit_count DESC, updated_at DESC
                """,
                (self.domain, source_language, target_language),
            ).fetchall()

        for source_term, target_term in rows:
            if source_term.lower() in source_text_lower:
                matches.append((source_term, target_term))
            if len(matches) >= limit:
                break

        if not matches:
            return ""

        lines = [
            "请优先复用以下历史术语记忆，保持翻译风格和术语一致："
        ]
        lines.extend([f"- {src} -> {tgt}" for src, tgt in matches])
        return "\n".join(lines)

    def get_checkpoint(self, file_path: str, page_index: int, content_index: int, source_language: str, target_language: str):
        if not self.enabled:
            return None

        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT status, translation FROM checkpoints
                WHERE file_path = ? AND page_index = ? AND content_index = ? AND source_language = ? AND target_language = ?
                """,
                (file_path, page_index, content_index, source_language, target_language),
            ).fetchone()
        if not row:
            return None
        return {"status": row[0], "translation": row[1]}

    def save_checkpoint(
        self,
        file_path: str,
        page_index: int,
        content_index: int,
        source_language: str,
        target_language: str,
        status: str,
        translation: Optional[str] = None,
    ):
        if not self.enabled:
            return

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO checkpoints (
                    file_path, page_index, content_index, source_language, target_language, status, translation
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(file_path, page_index, content_index, source_language, target_language)
                DO UPDATE SET
                    status = excluded.status,
                    translation = excluded.translation,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    file_path,
                    page_index,
                    content_index,
                    source_language,
                    target_language,
                    status,
                    translation,
                ),
            )

    def _save_table_header_memory(self, content, translated_text: str, source_language: str, target_language: str):
        try:
            source_rows = content.original.values.tolist()
            target_rows = json.loads(translated_text)
        except Exception as exc:
            log.warning(f"写入表头术语记忆失败: {exc}")
            return

        if not source_rows or not target_rows:
            return

        source_header = source_rows[0]
        target_header = target_rows[0]
        if not isinstance(source_header, list) or not isinstance(target_header, list):
            return

        for source_term, target_term in zip(source_header, target_header):
            if not source_term or not target_term:
                continue
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO terminology_memory (
                        source_term, target_term, domain, source_language, target_language
                    ) VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(source_term, domain, source_language, target_language)
                    DO UPDATE SET
                        target_term = excluded.target_term,
                        hit_count = terminology_memory.hit_count + 1,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        str(source_term),
                        str(target_term),
                        self.domain,
                        source_language,
                        target_language,
                    ),
                )

    def _content_to_string(self, content) -> str:
        if content.content_type == ContentType.TABLE:
            return content.get_origianl_to_string()
        return str(content.original)

    def _hash_text(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
