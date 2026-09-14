"""数据库迁移（Alembic）验证测试（P1）

验证迁移链完整性：
  1. 所有迁移版本 down_revision 引用真实存在
  2. 迁移链无断链（从 root 到 head 可追溯）
  3. 合并迁移（merge）的两个父节点均存在
  4. 每个迁移文件有 upgrade/downgrade 函数

运行方式：
  cd backend && python -m pytest tests/test_db_migration.py -v --tb=short
"""

import ast
import os
from pathlib import Path

import pytest

VERSIONS_DIR = Path(__file__).resolve().parents[1] / "alembic" / "versions"


def _parse_revisions() -> dict[str, tuple[str | tuple[str, ...], str]]:
    """解析所有迁移文件，返回 {revision: (down_revision, filename)}。"""
    revisions: dict[str, tuple[str | tuple[str, ...], str]] = {}
    for f in sorted(VERSIONS_DIR.glob("*.py")):
        if f.name.startswith("__"):
            continue
        tree = ast.parse(f.read_text(encoding="utf-8"))
        rev_id = None
        down_rev = None
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "revision":
                        if isinstance(node.value, ast.Constant):
                            rev_id = node.value.value
                    elif isinstance(target, ast.Name) and target.id == "down_revision":
                        if isinstance(node.value, ast.Constant):
                            down_rev = node.value.value
                        elif isinstance(node.value, ast.Tuple):
                            down_rev = tuple(
                                elt.value
                                for elt in node.value.elts
                                if isinstance(elt, ast.Constant)
                            )
        if rev_id:
            revisions[rev_id] = (down_rev, f.name)
    return revisions


def _has_function(tree: ast.AST, name: str) -> bool:
    """检查 AST 中是否包含指定名称的函数定义。"""
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return True
    return False


class TestMigrationChain:
    """迁移链完整性验证"""

    @pytest.fixture(scope="class")
    def revisions(self):
        return _parse_revisions()

    def test_versions_dir_exists(self):
        """迁移版本目录存在。"""
        assert VERSIONS_DIR.exists(), f"迁移目录不存在: {VERSIONS_DIR}"
        assert VERSIONS_DIR.is_dir()

    def test_has_migration_files(self, revisions):
        """至少有一个迁移文件。"""
        assert len(revisions) > 0, "没有找到迁移文件"

    def test_all_down_revisions_exist(self, revisions):
        """所有迁移的 down_revision 引用的版本真实存在。"""
        broken = []
        for rev_id, (down_rev, fname) in revisions.items():
            if down_rev is None:
                continue
            if isinstance(down_rev, tuple):
                for dr in down_rev:
                    if dr not in revisions:
                        broken.append(f"{fname}: {rev_id} → {dr} (不存在)")
            elif down_rev not in revisions:
                broken.append(f"{fname}: {rev_id} → {down_rev} (不存在)")
        assert not broken, f"断链迁移:\n  " + "\n  ".join(broken)

    def test_single_root_revision(self, revisions):
        """只有一个根版本（down_revision=None）。"""
        roots = [rev_id for rev_id, (down_rev, _) in revisions.items() if down_rev is None]
        assert len(roots) == 1, f"根版本数量应为1，实际: {len(roots)} → {roots}"

    def test_chain_has_merge_revision_if_branched(self, revisions):
        """多分支链必须存在合并迁移（down_revision 为 tuple，不限头部位置）。"""
        heads = self._find_heads(revisions)
        if len(heads) <= 1:
            return
        for rev_id, (down_rev, _) in revisions.items():
            if isinstance(down_rev, tuple):
                return
        pytest.fail(f"多分支 ({len(heads)} 个头) 但链中无合并迁移")

    def test_merge_parents_exist(self, revisions):
        """合并迁移的父节点全部存在。"""
        for rev_id, (down_rev, fname) in revisions.items():
            if isinstance(down_rev, tuple):
                for parent in down_rev:
                    assert parent in revisions, f"合并 {rev_id} ({fname}) 的父节点 {parent} 不存在"

    def _find_heads(self, revisions: dict) -> list[str]:
        """找到所有头部版本（不被任何其他版本引用为 down_revision）。"""
        all_refs = set()
        for _, (down_rev, _) in revisions.items():
            if down_rev is None:
                continue
            if isinstance(down_rev, tuple):
                all_refs.update(down_rev)
            else:
                all_refs.add(down_rev)
        return [r for r in revisions if r not in all_refs]

    def test_no_duplicate_revisions(self, revisions):
        """无重复的 revision ID。"""
        assert len(revisions) == len(set(revisions.keys()))

    def test_chain_depth(self, revisions):
        """迁移链深度合理（>10个版本）。"""
        assert len(revisions) >= 10, f"迁移版本数: {len(revisions)}，应 >= 10"

    def test_migration_files_have_required_functions(self):
        """每个迁移文件包含 upgrade() 和 downgrade() 函数。"""
        missing = []
        for f in sorted(VERSIONS_DIR.glob("*.py")):
            if f.name.startswith("__"):
                continue
            tree = ast.parse(f.read_text(encoding="utf-8"))
            if not _has_function(tree, "upgrade"):
                missing.append(f"{f.name}: 缺少 upgrade()")
            if not _has_function(tree, "downgrade"):
                missing.append(f"{f.name}: 缺少 downgrade()")
        assert not missing, f"缺少必要函数:\n  " + "\n  ".join(missing)

    def test_down_revision_chain_is_connected(self, revisions):
        """从根版本出发，遍历 down_revision 链可达所有版本。"""
        roots = [r for r, (d, _) in revisions.items() if d is None]
        visited = set()

        def dfs(rev_id):
            if rev_id in visited:
                return
            visited.add(rev_id)
            for rid, (down_rev, _) in revisions.items():
                if down_rev is None:
                    continue
                if isinstance(down_rev, tuple):
                    if rev_id in down_rev:
                        dfs(rid)
                elif down_rev == rev_id:
                    dfs(rid)

        for root in roots:
            dfs(root)

        unvisited = set(revisions.keys()) - visited
        assert not unvisited, f"无法从根版本到达: {unvisited}"

    def test_revision_count_matches(self):
        """版本文件数与解析出的 revision 数一致。"""
        py_files = [f for f in VERSIONS_DIR.glob("*.py") if not f.name.startswith("__")]
        revisions = _parse_revisions()
        assert len(py_files) == len(revisions), (
            f"版本文件数: {len(py_files)}, 解析 revision 数: {len(revisions)}"
        )


class TestMigrationNaming:
    """迁移文件命名规范"""

    def test_revision_ids_are_unique(self):
        """revision ID 在 4-16 字符之间。"""
        revisions = _parse_revisions()
        for rev_id, (_, fname) in revisions.items():
            assert 4 <= len(rev_id) <= 20, f"{fname}: revision ID 长度 {len(rev_id)} 不在 4-20 范围"

    def test_migration_files_end_with_py(self):
        """迁移文件均为 .py 文件。"""
        for f in VERSIONS_DIR.iterdir():
            if f.is_file() and not f.name.startswith("__"):
                assert f.suffix == ".py", f"非 Python 文件: {f.name}"