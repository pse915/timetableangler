"""Safely insert only the opt-in preview block into an existing timetable_app2.py.

This is for cases when live GitHub main differs from the bundled legacy snapshot.
Run from the project root:
  python tools/apply_preview.py --check /path/to/current/timetable_app2.py
  python tools/apply_preview.py --apply /path/to/current/timetable_app2.py
"""
import argparse
from pathlib import Path
import difflib

ANCHOR = "render_top_toolbar(visible_tabs)\nactive_tab = st.session_state.active_tab"
MARKER = "# Optional read-only Angular navigation/schedule preview."


def planned_change(source: str, block: str) -> str:
    if MARKER in source:
        raise ValueError("이미 미리보기 블록이 존재합니다. 중복 적용할 수 없습니다.")
    if source.count(ANCHOR) != 1:
        raise ValueError("안전 삽입 지점을 정확히 식별할 수 없습니다. 수동 코드 검토가 필요합니다.")
    return source.replace(ANCHOR, block + ANCHOR)


def main():
    parser=argparse.ArgumentParser(description="Safely integrate Angular preview into current Streamlit app")
    modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check",action="store_true")
    modes.add_argument("--apply",action="store_true")
    parser.add_argument("file",type=Path)
    args=parser.parse_args()
    src=args.file
    original=src.read_text(encoding="utf-8")
    block=(Path(__file__).resolve().parent/"angular_optional_block.txt").read_text(encoding="utf-8")
    patched=planned_change(original,block)
    if args.check:
        diff=difflib.unified_diff(original.splitlines(),patched.splitlines(),fromfile=str(src),tofile=str(src)+" (planned)",lineterm="")
        print("\n".join(diff))
    else:
        backup=src.with_name(src.name+".pre_angular_backup")
        if backup.exists():
            raise FileExistsError("백업 파일이 이미 존재합니다. 안전을 위해 중단합니다: "+str(backup))
        backup.write_text(original,encoding="utf-8")
        src.write_text(patched,encoding="utf-8")
        print("블록 삽입 완료. 백업:",backup)

if __name__ == "__main__":
    main()
