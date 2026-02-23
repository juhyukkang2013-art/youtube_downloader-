# 비디오 다운로더 테스트 가이드

## 수정 사항

**문제**: 다운로드를 시작하지 못했던 이유
- 형식 감지가 너무 엄격해서 일부 플랫폼(TikTok, Instagram 등)에서 포맷을 찾지 못함
- 형식 정보가 완전하지 않은 경우에 대한 처리가 부족

**해결 방법**:
1. ✓ 더 유연한 형식 필터링 추가 (비트레이트 기반 대체 옵션)
2. ✓ 형식을 찾지 못할 때 자동으로 최고 품질 옵션 사용
3. ✓ 더 강력한 에러 처리 추가
4. ✓ MP4 병합 옵션 추가 (비디오+오디오 통합)

---

## 빠른 테스트

### 1단계: 애플리케이션 실행

**방법 A - 가장 쉬운 방법 (추천)**:
```
C:\Users\강주혁\Desktop\03_APP\04_Downloader\VideoDownloader\run.bat
더블클릭
```

**방법 B - 커맨드 라인**:
```bash
cd "C:\Users\강주혁\Desktop\03_APP\04_Downloader\VideoDownloader"
python video_downloader.py
```

### 2단계: 테스트 URL 입력

다음 중 하나의 URL을 복사하여 앱에 붙여넣기:

**YouTube (권장 - 가장 안정적)**:
```
https://www.youtube.com/watch?v=jNQXAC9IVRw
```

**YouTube Shorts**:
```
https://www.youtube.com/shorts/videoid
(또는 https://youtu.be/videoid 형식)
```

**TikTok** (시간이 걸릴 수 있음):
```
https://www.tiktok.com/@user/video/123456789
```

**Instagram**:
```
https://www.instagram.com/p/videoid/
```

### 3단계: 다운로드 시작

1. **URL 붙여넣기** → 입력 필드에 URL 입력
2. **Download 버튼 클릭**
3. **형식 선택**:
   - "Video (with audio)" - 비디오 다운로드
   - "MP3 (audio only)" - 오디오만 추출
4. **화질 선택** (비디오 선택 시):
   - 목록에서 원하는 품질 선택
   - "Download" 버튼 클릭
5. **진행 상황 모니터링**:
   - 진행률 바 확인
   - 상태 로그 확인
6. **완료 확인**:
   - 알림 메시지 확인
   - `C:\Users\강주혁\Downloads\` 폴더에서 파일 확인

---

## 예상되는 동작

### 비디오 다운로드 흐름

```
URL 입력
    ↓
"Download" 버튼 클릭
    ↓
형식 선택 다이얼로그 표시
    ├─ "Video (with audio)" 선택
    │   ↓
    │ "Fetching available formats..." 로그
    │   ↓
    │ 2-5초 대기 (형식 감지 중)
    │   ↓
    │ 화질 선택 다이얼로그 표시 (1080p, 720p, 480p 등)
    │   ↓
    │ 원하는 화질 선택 후 "Download" 클릭
    │   ↓
    │ "Starting download: [화질]" 로그
    │   ↓
    │ "Downloading..." 로그
    │   ↓
    │ 진행률 바 업데이트 (0% → 100%)
    │   ↓
    │ 다운로드 완료 알림
    │   ↓
    │ Downloads 폴더에 파일 저장됨
```

### MP3 다운로드 흐름

```
URL 입력
    ↓
"Download" 버튼 클릭
    ↓
형식 선택 다이얼로그 표시
    ├─ "MP3 (audio only)" 선택
    │   ↓
    │ "Starting MP3 download..." 로그
    │   ↓
    │ "Downloading and converting to MP3..." 로그
    │   ↓
    │ 진행률 바 업데이트 (0% → 100%)
    │   ↓
    │ 다운로드 완료 알림
    │   ↓
    │ Downloads 폴더에 MP3 파일 저장됨
```

---

## 상태 로그 예시

### 정상 작동

```
Fetching available formats...
Starting download: 720p (MP4)
Downloading...
Download finished!
```

### 자동 형식 선택 (형식 감지 실패 시)

```
Fetching available formats...
Warning: No specific formats found, using best available
Starting download: Best Available (Automatic)
Downloading...
Download finished!
```

### MP3 변환

```
Starting MP3 download...
Downloading and converting to MP3...
Download finished!
```

---

## 문제 해결

### 문제 1: "Fetching available formats..." 후 응답 없음

**원인**: 형식 감지 중 (정상)
**해결**: 2-5초 기다리기 (네트워크 속도에 따라 다름)

### 문제 2: "No video formats available" 에러 (수정됨)

**원인**: 이제 자동으로 최고 품질 옵션 사용
**상태**: 수정됨 - 이제 대부분의 플랫폼 지원

### 문제 3: 다운로드가 시작되지 않음

**확인 사항**:
1. 인터넷 연결 확인
2. URL이 올바른지 확인
3. 콘솔 창에 에러 메시지 있는지 확인
4. 로그 창의 메시지 확인

### 문제 4: 느린 다운로드

**원인**: 정상 (서버 속도에 따라 다름)
**팁**:
- 낮은 화질 선택 (파일 크기 작음)
- 인터넷 속도 확인
- 다른 다운로드 일시 중지

### 문제 5: "FFmpeg 찾을 수 없음" (MP3 다운로드)

**해결**:
```bash
pip install yt-dlp[default]
```

---

## 테스트 체크리스트

- [ ] 애플리케이션이 오류 없이 시작됨
- [ ] URL을 입력할 수 있음
- [ ] Download 버튼을 클릭할 수 있음
- [ ] 형식 선택 다이얼로그가 표시됨
- [ ] "Video" 또는 "MP3" 선택 가능
- [ ] Video 선택 시 화질 목록이 표시됨
- [ ] 화질을 선택할 수 있음
- [ ] 다운로드가 시작됨 (로그 메시지 확인)
- [ ] 진행률 바가 업데이트됨
- [ ] 다운로드 완료 후 알림이 표시됨
- [ ] Downloads 폴더에 파일이 저장됨

---

## 성공 사례

### YouTube 테스트

1. URL: `https://www.youtube.com/watch?v=jNQXAC9IVRw`
2. Download 클릭
3. "Video (with audio)" 선택
4. 화질: "720p (MP4)" 선택
5. 기대 결과: 약 30초-2분 내에 MP4 파일 다운로드 완료

### MP3 테스트

1. 모든 URL에서 가능
2. Download 클릭
3. "MP3 (audio only)" 선택
4. 기대 결과: 음악 파일이 MP3로 변환되어 저장됨

---

## 수정 후 개선 사항

| 기능 | 이전 | 현재 |
|------|------|------|
| 형식 감지 | 엄격함 | 유연함 |
| 형식 없을 때 | 에러 | 자동 최고 품질 |
| 비트레이트 기반 | 미지원 | 지원 |
| MP4 병합 | 없음 | 자동 병합 |
| 에러 처리 | 기본적 | 강력함 |

---

## 다음 단계

1. **애플리케이션 실행**:
   ```bash
   cd "C:\Users\강주혁\Desktop\03_APP\04_Downloader\VideoDownloader"
   python video_downloader.py
   ```

2. **YouTube URL 테스트**:
   ```
   https://www.youtube.com/watch?v=jNQXAC9IVRw
   ```

3. **동작 확인**:
   - 형식 로딩 확인
   - 화질 목록 표시 확인
   - 다운로드 시작 확인

4. **다른 플랫폼 테스트**:
   - TikTok, Instagram, Facebook 등

---

## 문제 발생 시 정보 수집

문제가 발생하면 다음 정보를 제공하세요:

1. **사용한 URL**
2. **클릭한 단계** (어디서 멈췄는지)
3. **로그 메시지** (상태 로그에 표시된 내용)
4. **에러 메시지** (있으면)
5. **콘솔 창 내용** (있으면)

---

**업데이트**: 2026-02-15
**상태**: 다운로드 기능 수정 완료
