import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from apply_preview import planned_change
import pytest


def test_patch_single_anchor_only():
    baseline='a=1\nrender_top_toolbar(visible_tabs)\nactive_tab = st.session_state.active_tab\n'
    out=planned_change(baseline,'# Optional read-only Angular navigation/schedule preview.\n')
    assert out.startswith('a=1\n# Optional')
    assert out.endswith(baseline.split('a=1\n',1)[1])


def test_patch_rejects_missing_anchor():
    with pytest.raises(ValueError):
        planned_change('other code','block')
