from __future__ import annotations

import contextlib
import datetime as dt
import hashlib
import json
import os
import platform
import tempfile
import time
from pathlib import Path
from typing import Any, Iterator

STATE_VERSION = 2
PACK_VERSION = "2.0.1"

def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()

def today() -> str:
    return dt.date.today().isoformat()

def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)

def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except Exception:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(tmp_name)
        raise

def atomic_write_json(path: Path, value: Any) -> None:
    atomic_write_text(path, json.dumps(value, indent=2, ensure_ascii=False, sort_keys=False) + "\n")

def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def safe_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())

def environment_summary() -> dict[str, str]:
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version(),
    }

class ProjectLock:
    def __init__(self, engineering_dir: Path, timeout_seconds: int = 20, stale_seconds: int = 1800):
        self.path = engineering_dir / ".sepack.lock"
        self.timeout_seconds = timeout_seconds
        self.stale_seconds = stale_seconds
        self.acquired = False

    def __enter__(self) -> "ProjectLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + self.timeout_seconds
        while True:
            try:
                fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                payload = {
                    "pid": os.getpid(),
                    "created_at": utc_now(),
                }
                os.write(fd, canonical_json_bytes(payload))
                os.close(fd)
                self.acquired = True
                return self
            except FileExistsError:
                try:
                    age = time.time() - self.path.stat().st_mtime
                    if age > self.stale_seconds:
                        self.path.unlink(missing_ok=True)
                        continue
                except FileNotFoundError:
                    continue
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"Could not acquire project-state lock: {self.path}")
                time.sleep(0.1)

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.acquired:
            self.path.unlink(missing_ok=True)
            self.acquired = False

def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())

def iter_files(root: Path, *, exclude_parts: set[str] | None = None) -> Iterator[Path]:
    exclude_parts = exclude_parts or set()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in exclude_parts for part in path.parts):
            continue
        yield path
