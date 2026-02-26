"""
parser.py — CSV File Parser and Validator
Parses user-uploaded CSV files and validates their contents.
"""

import pandas as pd
import io
from typing import List, Union
from collections import defaultdict


REQUIRED_COLUMNS = {"task_id", "task_name", "duration", "predecessors"}


def parse_csv(source: Union[str, io.BytesIO, io.StringIO]) -> pd.DataFrame:
    """
    Parse a CSV source and return a validated DataFrame.

    Args:
        source: File path (str) or file-like object (BytesIO/StringIO)

    Returns:
        Validated DataFrame

    Raises:
        ValueError: Missing columns, invalid data, etc.
    """
    # ---- Read ----
    if isinstance(source, str):
        df = pd.read_csv(source)
    else:
        df = pd.read_csv(source)

    # ---- Column check ----
    df.columns = df.columns.str.strip().str.lower()
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing columns in CSV: {', '.join(missing)}. "
            f"Expected columns: {', '.join(REQUIRED_COLUMNS)}"
        )

    # ---- Data cleanup ----
    df["task_id"] = df["task_id"].astype(str).str.strip()
    df["task_name"] = df["task_name"].astype(str).str.strip()
    df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
    df["predecessors"] = df["predecessors"].fillna("").astype(str).str.strip()

    # ---- Validation ----
    errors = validate_tasks(df)
    if errors:
        raise ValueError("CSV validation errors:\n" + "\n".join(f"  • {e}" for e in errors))

    return df


def validate_tasks(df: pd.DataFrame) -> List[str]:
    """
    Validate task data in a DataFrame.

    Returns:
        List of errors (empty if everything is valid)
    """
    errors = []

    # 1. Empty DataFrame
    if df.empty:
        errors.append("CSV file is empty — at least one task is required.")
        return errors

    # 2. Duplicate task_id
    duplicates = df[df["task_id"].duplicated()]["task_id"].tolist()
    if duplicates:
        errors.append(f"Duplicate task IDs: {', '.join(duplicates)}")

    # 3. Negative or invalid duration
    invalid_dur = df[df["duration"].isna() | (df["duration"] <= 0)]
    if not invalid_dur.empty:
        bad_ids = invalid_dur["task_id"].tolist()
        errors.append(f"Invalid duration (<=0 or NaN): {', '.join(bad_ids)}")

    # 4. Unknown predecessor references
    all_ids = set(df["task_id"].tolist())
    for _, row in df.iterrows():
        pred_raw = str(row["predecessors"]).strip()
        if pred_raw and pred_raw.lower() not in ("nan", "none", ""):
            for p in pred_raw.split():
                p = p.strip()
                if p and p not in all_ids:
                    errors.append(
                        f"Task '{row['task_id']}' references unknown predecessor: '{p}'"
                    )

    # 5. Cycle detection (simple DFS)
    if not errors:
        cycle_error = _check_cycles(df)
        if cycle_error:
            errors.append(cycle_error)

    return errors


def _check_cycles(df: pd.DataFrame) -> str:
    """Simple DFS cycle detection."""
    successors = defaultdict(list)
    all_ids = set()

    for _, row in df.iterrows():
        tid = str(row["task_id"]).strip()
        all_ids.add(tid)
        pred_raw = str(row["predecessors"]).strip()
        if pred_raw and pred_raw.lower() not in ("nan", "none", ""):
            for p in pred_raw.split():
                p = p.strip()
                if p:
                    successors[p].append(tid)

    visited = set()
    rec_stack = set()

    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        for s in successors.get(node, []):
            if s not in visited:
                result = dfs(s)
                if result:
                    return result
            elif s in rec_stack:
                return f"Cycle detected: ... -> {node} -> {s} -> ..."
        rec_stack.discard(node)
        return ""

    for tid in all_ids:
        if tid not in visited:
            result = dfs(tid)
            if result:
                return result

    return ""
