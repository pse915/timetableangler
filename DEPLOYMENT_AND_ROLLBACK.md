# 기존 Streamlit 배포 유지·안전 배포 절차

1. 운영 중인 GitHub main의 `timetable_app2.py` SHA256, 커밋과 기존 `requirements.txt`, `.streamlit/config.toml`을 보존하세요. 이 패키지에는 이전 업로드 스냅샷이 들어 있으므로 현재 main과 `git diff`를 꼭 수행하세요.
2. 새로운 브랜치에 `frontend/`, `angular_preview.py`, 테스트만 우선 추가하세요. `timetable_app2.py`는 아래 옵트인 블록만 현재 main에 적용하고 원본 업무 함수의 내용을 덮어쓰지 마세요.
3. 프런트는 워크플로 `Angular Preview Build (non-production)`을 수동 실행하고 성공 여부 확인, 산출물 파일을 브랜치의 `frontend/dist/timetable-angular/browser/`에 커밋하세요. `.gitignore`의 `frontend/dist/` 예외는 빌드 후 사용자 환경에 맞춰 수정하세요. 서버에서 Node를 띄우지 않습니다.
4. 새 브랜치/테스트용 Google Sheets 사본/별도 Streamlit 테스트 앱에서 인증·미리보기 팝업·브리지 응답을 먼저 검증하세요.
5. 기존 Streamlit 앱 URL을 유지한 채 운영 브랜치에 검증된 변경만 병합하세요. Streamlit Cloud 설정에서 엔트리포인트는 기존 `timetable_app2.py`를 유지하세요. Google Secrets 값을 복사해 GitHub에 커밋하지 마세요.
6. 롤백: 문제 발생 시 GitHub 운영 브랜치의 마지막 정상 커밋으로 revert/restore하고 Streamlit Cloud 재배포를 확인하세요. 이미 실제 시트에 기록된 내용은 코드 revert로 되돌릴 수 없으니 별도 변경 이력과 백업으로 점검하세요.

현재 배포·롤백 검증은 미수행입니다.
