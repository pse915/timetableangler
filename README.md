# Streamlit 유지형 Angular 전환 — 안전한 첫 단계

> **중요:** 이 산출물은 12개 기능을 Angular로 완전 전환한 완성본이 **아닙니다**. Angular 업무 탐색 및 원본 시간표 샘플(읽기 전용) 시제품 소스와, 원본 기능을 유지하는 Streamlit 엔트리포인트를 제공합니다. 외부 서버는 필요 없습니다. 운영 앱을 무검증 상태로 교체하지 마세요.

## 현재 실제 구현 상태

- `timetable_app2.py`: Library에서 확보한 원본 업무 로직 전체를 보존하고, 인증 뒤에만 Angular 미리보기를 렌더링하는 약 25줄 추가. 기본은 기존 UI 100% 그대로입니다.
- `legacy/timetable_app2_snapshot.py`: 수정 전 원본. 즉시 비교·복구할 수 있습니다.
- `angular_preview.py`: Streamlit Custom Component v1 브리지. 서버에서 권한별 메뉴 이벤트를 검증·중복 제거, 최소 컬럼만 화면에 전달. Google Sheets 쓰기 기능 **없음**.
- `frontend/src`: 진짜 Angular 22 standalone/Signals 기반 코드. 12개 업무의 메뉴를 보여주고 기존 Streamlit 업무 탭을 선택할 수 있으며 원본 샘플 검색·상세 팝업을 로컬 처리하도록 작성.
- **미검증:** Angular 빌드, 브라우저 팝업 동작, 실제 Community Cloud 실행. 이 환경은 npm 네트워크에 연결되지 않아 컴파일을 수행하지 못했습니다.

## 운영상 필수 주의

1. 기존 Streamlit 앱의 `*.streamlit.app` URL, 배포 설정, Google Sheets, `gcp_service_account` Secret은 바꾸지 않습니다.
2. 배포 서버에서 Node / FastAPI를 띄우지 않습니다. Angular는 **개발 머신/GitHub Actions에서 사전 빌드**한 파일만 사용합니다.
3. **GitHub main을 변경하기 전**, 현재 원본과 이 스냅샷의 버전 차이를 비교하세요. 현재 GitHub 파일을 직접 내려받을 수 없는 환경에서 이전 업로드 스냅샷을 사용했습니다. 원본을 덮어쓰지 마세요.
4. 미리보기를 사용하지 않으면 추가 브리지 로직은 실행되지 않습니다 (`TIMETABLE_ANGULAR_PREVIEW=0`, 기본값).
5. 이 프로젝트에는 컴파일된 Angular dist가 아직 없습니다. CI에서 생성된 `browser/` 디렉터리 내용을 `frontend/dist/timetable-angular/browser/` 경로에 복사하여 패키징해야 미리보기가 작동합니다.

## 개발 테스트

```bash
python -m py_compile timetable_app2.py angular_preview.py
python -m pytest -q tests
cd frontend
npm install   # 인터넷 접속 가능한 개발 PC 또는 GitHub Actions에서
npm run build
```

## 로컬 실행 및 선택적 미리보기

```bash
# 1) 기존 secrets.toml을 로컬 .streamlit/에 안전하게 준비 (GitHub에 커밋 금지)
# 2) 기존 UI 검증
streamlit run timetable_app2.py
# 3) Angular 빌드 자산 준비 후 로컬 미리보기 활성화
TIMETABLE_ANGULAR_PREVIEW=1 streamlit run timetable_app2.py
```

Windows PowerShell: `$env:TIMETABLE_ANGULAR_PREVIEW="1"; streamlit run timetable_app2.py`

## 남은 작업

- 12개 영역 UI/행동/검증/보고서/권한/업무 저장 로직 Angular로 개별 전환
- 실제 v1 컴포넌트의 브라우저 이벤트/iframe 포커스·팝업 테스트, v2와의 비교
- 원본 대비 Golden Master 결과, 동시성, 캐시 무효화, Google Sheets 쓰기 테스트
- 실제 Community Cloud 스테이징 앱 검증과 운영 브랜치 반영

완성으로 주장하지 말고 단계별로 검증 후 별도로 배포하세요.

## 최신 GitHub main 파일에 안전 적용하기

이 ZIP의 `timetable_app2.py`는 과거 업로드 스냅샷에 삽입한 사본입니다. 실제 GitHub main을 그대로 가져와 새 브랜치에서 다음을 실행하세요.

```bash
python tools/apply_preview.py --check timetable_app2.py  # 삽입 전 diff 확인
python tools/apply_preview.py --apply timetable_app2.py  # .pre_angular_backup 생성
```

**GitHub main의 기존 업무 코드를 이 ZIP의 원본으로 덮어쓰지 마세요.** `angular_preview.py`, `frontend/` 및 생성된 빌드 결과와 함께 현재 main에 삽입해야 합니다.
