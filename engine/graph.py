"""
graph.py — Precedence Relationship Graph (DAG)
Models task dependencies as a Directed Acyclic Graph.
"""

import pandas as pd
from collections import defaultdict, deque
from typing import Dict, List


class PrecedenceGraph:
    """
    DAG structure holding assembly line tasks and precedence relationships.

    Attributes:
        tasks       : {task_id: {"name": str, "duration": float}}
        successors  : {task_id: [task_id, ...]}   — who follows this task
        predecessors: {task_id: [task_id, ...]}   — who must come before this task
    """

    def __init__(self):
        self.tasks: Dict[str, dict] = {}
        self.successors: Dict[str, List[str]] = defaultdict(list)
        self.predecessors: Dict[str, List[str]] = defaultdict(list)

    # ------------------------------------------------------------------ #
    #  Data Loading
    # ------------------------------------------------------------------ #

    def load_from_dataframe(self, df: pd.DataFrame) -> None:
        """
        Load graph from a DataFrame.
        Expected columns: task_id, task_name, duration, predecessors
        predecessors column can be empty or a space-separated list of IDs.
        """
        self._reset()

        # Register tasks
        for _, row in df.iterrows():
            tid = str(row["task_id"]).strip()
            self.tasks[tid] = {
                "name": str(row["task_name"]).strip(),
                "duration": float(row["duration"]),
            }

        # Build precedence edges
        for _, row in df.iterrows():
            tid = str(row["task_id"]).strip()
            pred_raw = str(row.get("predecessors", "")).strip()

            if pred_raw and pred_raw.lower() not in ("nan", "none", ""):
                preds = pred_raw.split()
                for p in preds:
                    p = p.strip()
                    if p and p in self.tasks:
                        self.predecessors[tid].append(p)
                        self.successors[p].append(tid)

        self._validate()

    def load_from_csv(self, filepath: str) -> None:
        df = pd.read_csv(filepath)
        self.load_from_dataframe(df)

    def _reset(self):
        self.tasks.clear()
        self.successors.clear()
        self.predecessors.clear()
        self.successors = defaultdict(list)
        self.predecessors = defaultdict(list)

    # ------------------------------------------------------------------ #
    #  Validation
    # ------------------------------------------------------------------ #

    def _validate(self) -> None:
        """Check for cycles (must be a DAG)."""
        visited = set()
        rec_stack = set()

        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            for succ in self.successors[node]:
                if succ not in visited:
                    if has_cycle(succ):
                        return True
                elif succ in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for task in self.tasks:
            if task not in visited:
                if has_cycle(task):
                    raise ValueError(
                        "Cycle detected in precedence graph! "
                        "Please check your data."
                    )

    # ------------------------------------------------------------------ #
    #  Graph Metrics
    # ------------------------------------------------------------------ #

    def get_entry_tasks(self) -> List[str]:
        """Tasks with no predecessors (line entry points)."""
        return [t for t in self.tasks if not self.predecessors[t]]

    def get_exit_tasks(self) -> List[str]:
        """Tasks with no successors (line exit points)."""
        return [t for t in self.tasks if not self.successors[t]]

    def topological_sort(self) -> List[str]:
        """Topological sort using Kahn's algorithm."""
        in_degree = {t: len(self.predecessors[t]) for t in self.tasks}
        queue = deque([t for t, d in in_degree.items() if d == 0])
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for succ in self.successors[node]:
                in_degree[succ] -= 1
                if in_degree[succ] == 0:
                    queue.append(succ)

        if len(order) != len(self.tasks):
            raise ValueError("Topological sort failed — cycle exists in graph.")
        return order

    def positional_weight(self, task_id: str) -> float:
        """
        RPW (Ranked Positional Weight) calculation:
        Task's own duration + longest path sum through all successors.
        """
        memo = {}

        def _rpw(tid: str) -> float:
            if tid in memo:
                return memo[tid]
            w = self.tasks[tid]["duration"]
            if self.successors[tid]:
                w += max(_rpw(s) for s in self.successors[tid])
            memo[tid] = w
            return w

        return _rpw(task_id)

    def all_positional_weights(self) -> Dict[str, float]:
        """Return RPW values for all tasks."""
        return {tid: self.positional_weight(tid) for tid in self.tasks}

    def total_work_content(self) -> float:
        """Total work content (sum of all task durations)."""
        return sum(t["duration"] for t in self.tasks.values())

    def summary(self) -> dict:
        return {
            "task_count": len(self.tasks),
            "total_work_content": self.total_work_content(),
            "entry_tasks": self.get_entry_tasks(),
            "exit_tasks": self.get_exit_tasks(),
        }
