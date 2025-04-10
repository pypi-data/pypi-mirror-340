"""Wrapper code for pyterraform."""

import sys
from pathlib import Path


def get_tf_root() -> Path:
    """Get Terraform root folder."""
    curdir = Path().resolve()
    while curdir != curdir.root:
        if (curdir / ".terraform").is_dir():
            return curdir / ".terraform"
        tf_roots = list(curdir.rglob(".terraform"))
        if len(tf_roots) == 1:
            return tf_roots[0]
        if len(tf_roots) > 1:
            raise ValueError(
                "More than one '.terraform' folder found.",
            )
        curdir = curdir.parent
    raise ValueError("No '.terraform' folder found!")


def main():
    """Find pyterraform module and evoke it."""
    tf_root = get_tf_root()
    pytf_roots = list((tf_root / "modules").glob("*/pyterraform"))
    if not pytf_roots:
        raise ValueError("No `sm-pipeline` module detected.")
    sys.path.insert(0, str(pytf_roots[0].parent))

    from pyterraform import sm

    sm.main()
