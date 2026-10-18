import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from angular_preview import consume_nav_event, validate_nav_event, preview_rows


def test_authorized_navigation_and_replay():
    ids=[]
    event={'type':'navigate','id':'12345678-abcd','target':'시간표 조회'}
    assert consume_nav_event(event,['시간표 조회'],ids)=='시간표 조회'
    assert consume_nav_event(event,['시간표 조회'],ids) is None


def test_rejects_unapproved_or_write_events():
    assert validate_nav_event({'type':'navigate','id':'12345678-abcd','target':'🔑 아이디·권한 관리'},['시간표 조회']) is None
    assert validate_nav_event({'type':'commitSwap','id':'12345678-abcd','target':'시간표 조회'},['시간표 조회']) is None
    assert validate_nav_event({'type':'navigate','target':'시간표 조회'},['시간표 조회']) is None
    assert validate_nav_event({'type':'navigate','id':'short','target':'시간표 조회'},['시간표 조회']) is None


def test_preview_rows_includes_only_safe_schedule_columns():
    import pandas as pd
    source=pd.DataFrame([{'교사명':'교사A','요일':'월','교시':1,'과목':'수학','학급':'1-1','service_private_key':'abc'}])
    assert preview_rows(source)==[{'교사명':'교사A','요일':'월','교시':'1','과목':'수학','학급':'1-1'}]


def test_no_changes_to_original_except_preview_block():
    root=Path(__file__).resolve().parents[1]
    old=(root/'legacy'/'timetable_app2_snapshot.py').read_text()
    new=(root/'timetable_app2.py').read_text()
    assert old in new.replace(new[new.index('# Optional read-only Angular navigation/schedule preview.'):new.index('render_top_toolbar(visible_tabs)\nactive_tab')], '')
