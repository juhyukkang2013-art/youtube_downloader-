import tkinter as tk
from tkinter import messagebox
import yt_dlp
import os
import re
import shutil
import threading
from urllib.parse import urlparse

class VideoDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("유튜브 다운로드")
        self.root.geometry("800x400")
        self.root.resizable(False, False)

        # Set the download path to Windows Downloads folder
        self.downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        # Initialize variables
        self.download_type = None
        self.selected_quality = None
        self.available_formats = None
        self.current_url = None

        self.create_ui()

    def create_ui(self):
        """Create the main UI components"""
        # Set white background
        self.root.configure(bg="white")

        # Main container frame - centered
        container = tk.Frame(self.root, bg="white")
        container.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Title - "유튜브 다운로드"
        title_label = tk.Label(
            container,
            text="유튜브 다운로드",
            font=("Malgun Gothic", 32, "bold"),
            fg="#333333",
            bg="white"
        )
        title_label.pack(pady=(0, 40))

        # Input frame (입력 필드 + 다운로드 버튼을 한 줄로)
        input_frame = tk.Frame(container, bg="white")
        input_frame.pack(fill=tk.X, pady=(0, 15))

        # URL Entry with green border
        entry_container = tk.Frame(input_frame, bg="#7CB342", bd=0)
        entry_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Inner frame for padding
        entry_inner = tk.Frame(entry_container, bg="white", bd=0)
        entry_inner.pack(padx=3, pady=3, fill=tk.BOTH, expand=True)

        self.url_entry = tk.Entry(
            entry_inner,
            font=("Malgun Gothic", 11),
            bg="white",
            fg="#666666",
            insertbackground="#333333",
            bd=0,
            relief=tk.FLAT
        )
        self.url_entry.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)
        self.url_entry.insert(0, "여기에 동영상 링크 붙여넣기")
        self.url_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.url_entry.bind("<FocusOut>", self._on_entry_focus_out)
        self.url_entry.config(fg="#999999")

        # Download button (green)
        self.download_button = tk.Button(
            input_frame,
            text="다운로드",
            command=self.on_download_click,
            bg="#7CB342",
            fg="white",
            font=("Malgun Gothic", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#689F38",
            width=12
        )
        self.download_button.pack(side=tk.LEFT, padx=(8, 0), ipady=13)

        # Terms text at bottom
        terms_frame = tk.Frame(container, bg="white")
        terms_frame.pack(pady=(0, 0))

        terms_text = tk.Label(
            terms_frame,
            text="당사의 서비스를 이용하면 당사의 ",
            font=("Malgun Gothic", 9),
            fg="#666666",
            bg="white"
        )
        terms_text.pack(side=tk.LEFT)

        terms_link1 = tk.Label(
            terms_frame,
            text="서비스 약관",
            font=("Malgun Gothic", 9, "underline"),
            fg="#1E88E5",
            bg="white",
            cursor="hand2"
        )
        terms_link1.pack(side=tk.LEFT)

        terms_text2 = tk.Label(
            terms_frame,
            text=" 및 ",
            font=("Malgun Gothic", 9),
            fg="#666666",
            bg="white"
        )
        terms_text2.pack(side=tk.LEFT)

        terms_link2 = tk.Label(
            terms_frame,
            text="개인정보보호정책",
            font=("Malgun Gothic", 9, "underline"),
            fg="#1E88E5",
            bg="white",
            cursor="hand2"
        )
        terms_link2.pack(side=tk.LEFT)

        terms_text3 = tk.Label(
            terms_frame,
            text=" 에 동의하는 것입니다.",
            font=("Malgun Gothic", 9),
            fg="#666666",
            bg="white"
        )
        terms_text3.pack(side=tk.LEFT)

        # Progress section (hidden by default)
        self.progress_frame = tk.Frame(self.root, bg="white")

        self.progress_label = tk.Label(
            self.progress_frame,
            text="다운로드 중...",
            font=("Malgun Gothic", 10),
            fg="#666666",
            bg="white"
        )
        self.progress_label.pack(pady=(10, 5))

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.Canvas(
            self.progress_frame,
            height=6,
            width=500,
            bg="#E0E0E0",
            highlightthickness=0
        )
        self.progress_bar.pack(pady=(0, 5))
        self.progress_bar_fill = self.progress_bar.create_rectangle(
            0, 0, 0, 6, fill="#7CB342", outline=""
        )

        self.progress_percent = tk.Label(
            self.progress_frame,
            text="0%",
            font=("Malgun Gothic", 9),
            fg="#7CB342",
            bg="white"
        )
        self.progress_percent.pack()

    def _on_entry_focus_in(self, event):
        """Remove placeholder text when entry gets focus"""
        if self.url_entry.get() == "여기에 동영상 링크 붙여넣기":
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(fg="#333333")

    def _on_entry_focus_out(self, event):
        """Add placeholder text back if entry is empty"""
        if not self.url_entry.get():
            self.url_entry.insert(0, "여기에 동영상 링크 붙여넣기")
            self.url_entry.config(fg="#999999")

    def log_message(self, message):
        """Log message (simplified for minimal UI)"""
        print(message)  # Print to console instead of UI log

    def _strip_ansi(self, text):
        """터미널 ANSI 이스케이프 코드 제거. GUI 메시지에 색상 코드가 그대로 보이는 것 방지."""
        if not text:
            return text
        ansi_escape = re.compile(r'\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def _is_ffmpeg_available(self):
        """시스템 PATH에 ffmpeg 실행 파일 존재 여부 확인. 비디오/오디오 병합 및 MP3 변환에 필요."""
        return self._get_ffmpeg_path() is not None

    def _get_ffmpeg_path(self):
        """
        ffmpeg 실행 파일의 전체 경로 반환. GUI 실행 시 PATH가 달라질 수 있어 경로를 명시해 yt-dlp에 전달하기 위함.
        반환: (ffmpeg가 있는 디렉터리 경로) 또는 None. yt-dlp는 이 디렉터리에서 ffmpeg, ffprobe를 찾음.
        """
        # 1) PATH에서 ffmpeg 찾기
        ffmpeg_exe = shutil.which('ffmpeg')
        if ffmpeg_exe:
            return os.path.dirname(os.path.abspath(ffmpeg_exe))
        # 2) Windows에서 winget/일반 설치 경로 후보 검사
        if os.name == 'nt':
            candidates = [
                os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), 'ffmpeg', 'bin'),
                os.path.join(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'), 'ffmpeg', 'bin'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'WinGet', 'Links'),  # winget 링크
            ]
            for dir_path in candidates:
                if not dir_path or not os.path.isdir(dir_path):
                    continue
                exe_path = os.path.join(dir_path, 'ffmpeg.exe')
                if os.path.isfile(exe_path):
                    return dir_path
        return None

    def _show_download_error(self, message, also_log=True):
        """다운로드 실패 시 사용자에게 보여줄 메시지. ANSI 제거 후 팝업 및 로그 기록."""
        clean_msg = self._strip_ansi(message)
        if also_log:
            self.log_message(clean_msg)
        messagebox.showerror("Download Error", clean_msg)

    def on_download_click(self):
        """Handle download button click"""
        url = self.url_entry.get().strip()

        # Check if placeholder text is still there
        if not url or url == "여기에 동영상 링크 붙여넣기":
            messagebox.showerror("오류", "동영상 링크를 입력해주세요")
            return

        # Validate URL format
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise ValueError("올바르지 않은 URL 형식입니다")
        except Exception as e:
            messagebox.showerror("오류", f"올바르지 않은 URL입니다: {str(e)}")
            return

        self.current_url = url
        self.show_download_type_dialog()

    def show_download_type_dialog(self):
        """다운로드 유형(비디오/MP3) 선택 모달 표시. 선택 후 '다운로드' 버튼으로 실제 다운로드 시작."""
        dialog = tk.Toplevel(self.root)
        dialog.title("다운로드 형식 선택")
        dialog.geometry("320x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="white")

        # 모달을 메인 창 중앙에 배치
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        label = tk.Label(
            dialog,
            text="다운로드할 형식을 선택하세요:",
            font=("Malgun Gothic", 10),
            bg="white"
        )
        label.pack(pady=(20, 15))

        download_type = tk.StringVar(value="video")

        video_radio = tk.Radiobutton(
            dialog,
            text="비디오 (동영상 + 오디오)",
            variable=download_type,
            value="video",
            font=("Malgun Gothic", 9),
            bg="white",
            activebackground="white"
        )
        video_radio.pack(anchor=tk.W, padx=50, pady=5)

        audio_radio = tk.Radiobutton(
            dialog,
            text="MP3 (오디오만)",
            variable=download_type,
            value="audio",
            font=("Malgun Gothic", 9),
            bg="white",
            activebackground="white"
        )
        audio_radio.pack(anchor=tk.W, padx=50, pady=5)

        # 라디오 옵션 아래: 다운로드 버튼(선택 확정 후 다운로드 시작), 취소 버튼
        button_frame = tk.Frame(dialog, bg="white")
        button_frame.pack(pady=(25, 20))

        def on_download_confirm():
            """모달에서 선택한 유형으로 다운로드 시작 후 모달 닫기"""
            self.download_type = download_type.get()
            dialog.destroy()

            if self.download_type == "video":
                self.start_download_video_auto()
            else:
                self.start_download_audio()

        download_confirm_btn = tk.Button(
            button_frame,
            text="다운로드",
            command=on_download_confirm,
            bg="#7CB342",
            fg="white",
            font=("Malgun Gothic", 9, "bold"),
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#689F38",
            padx=20,
            pady=5
        )
        download_confirm_btn.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(
            button_frame,
            text="취소",
            command=dialog.destroy,
            bg="#E0E0E0",
            fg="#333333",
            font=("Malgun Gothic", 9),
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#CCCCCC",
            padx=20,
            pady=5
        )
        cancel_button.pack(side=tk.LEFT, padx=5)

    def show_quality_dialog(self):
        """Show dialog to select video quality"""
        # Fetch available formats in a separate thread
        thread = threading.Thread(target=self._fetch_formats_and_show_dialog)
        thread.daemon = True
        thread.start()

    def start_download_video_auto(self):
        """Start video download automatically with best quality (no dialog)"""
        # Set the best available format and start download immediately
        self.selected_quality = {
            'label': 'Best Available (Auto)',
            'format_id': 'bestvideo+bestaudio',  # /best 폴백 없이 항상 비디오+오디오 병합만 사용
            'height': None
        }
        self.log_message("비디오 다운로드 시작 (최고 화질)...")
        self.start_download_video()

    def _fetch_formats_and_show_dialog(self):
        """Fetch formats from URL and show quality dialog"""
        self.log_message("Fetching available formats...")

        try:
            formats = self.get_available_formats(self.current_url)

            if not formats:
                self.log_message("Warning: No specific formats found, using best available")
                formats = [{
                    'label': 'Best Available (Automatic)',
                    'format_id': 'bestvideo+bestaudio/best',
                    'height': None
                }]

            self.available_formats = formats
            self.root.after(0, self._show_quality_selection_dialog)

        except Exception as e:
            error_msg = f"Error fetching formats: {str(e)}"
            self.log_message(error_msg)
            # Still try with best format
            self.available_formats = [{
                'label': 'Best Available (Automatic)',
                'format_id': 'bestvideo+bestaudio/best',
                'height': None
            }]
            self.root.after(0, self._show_quality_selection_dialog)

    def _show_quality_selection_dialog(self):
        """Show quality selection dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Video Quality")
        dialog.geometry("350x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        label = ttk.Label(dialog, text="Available Qualities:", font=("Arial", 10))
        label.pack(pady=(10, 10))

        # Listbox for quality selection
        listbox_frame = ttk.Frame(dialog)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, font=("Arial", 10))
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # Add quality options to listbox
        for i, format_info in enumerate(self.available_formats):
            listbox.insert(tk.END, format_info['label'])

        # Select first item by default
        if self.available_formats:
            listbox.select_set(0)
            listbox.see(0)

        # Button frame
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=(0, 20))

        def on_ok():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a quality")
                return

            self.selected_quality = self.available_formats[selection[0]]
            dialog.destroy()
            self.start_download_video()

        ok_button = ttk.Button(button_frame, text="Download", command=on_ok)
        ok_button.pack(side=tk.LEFT, padx=5)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def get_available_formats(self, url):
        """Get available video formats from URL using yt-dlp"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                # Extract and organize formats by resolution
                formats_dict = {}
                has_video_formats = False

                if 'formats' in info:
                    for fmt in info['formats']:
                        # Skip audio-only formats (vcodec is 'none')
                        if fmt.get('vcodec') == 'none':
                            continue

                        # Skip formats that have no video codec at all
                        if not fmt.get('vcodec'):
                            continue

                        # Get format info
                        format_id = fmt.get('format_id')
                        height = fmt.get('height')
                        ext = fmt.get('ext', 'mp4')
                        tbr = fmt.get('tbr')  # Total bitrate

                        # Use height if available, otherwise use bitrate or format_id
                        if height:
                            key = height
                            label_base = f"{height}p"
                        elif tbr:
                            key = int(tbr * 10)  # Use bitrate as key
                            label_base = f"{int(tbr)}k"
                        else:
                            continue

                        # Store best format for each quality level
                        if key not in formats_dict:
                            formats_dict[key] = {
                                'format_id': format_id,
                                'height': height,
                                'ext': ext,
                                'label_base': label_base
                            }
                            has_video_formats = True

                # Sort by resolution (descending)
                if formats_dict:
                    sorted_keys = sorted(formats_dict.keys(), reverse=True)
                    formats_list = []
                    for key in sorted_keys:
                        fmt = formats_dict[key]
                        label = f"{fmt['label_base']} ({fmt['ext'].upper()})"
                        formats_list.append({
                            'label': label,
                            'format_id': fmt['format_id'],
                            'height': fmt['height']
                        })
                    return formats_list if formats_list else None

                # Fallback: Use best video format if no specific resolutions found
                if not has_video_formats:
                    return [{
                        'label': 'Best Available',
                        'format_id': 'bestvideo+bestaudio/best',
                        'height': None
                    }]

                return None

        except Exception as e:
            # Fallback to best format on error
            return [{
                'label': 'Best Available (Automatic)',
                'format_id': 'bestvideo+bestaudio/best',
                'height': None
            }]

    def start_download_video(self):
        """Start video download in a separate thread"""
        thread = threading.Thread(target=self._download_video_thread)
        thread.daemon = True
        thread.start()

    def _ensure_audio_format(self, format_id):
        """
        비디오 전용 포맷 ID면 +bestaudio를 붙여 항상 오디오가 포함되도록 함.
        /best 폴백을 제거해 'best'가 비디오만 선택되는 경우를 막음.
        """
        if not format_id:
            return 'bestvideo+bestaudio'
        # 이미 + 가 있으면 비디오+오디오 조합. /best 폴백 제거(비디오만 나올 수 있음)
        if '+' in format_id:
            # bestvideo+bestaudio/best → bestvideo+bestaudio 로 변경해 항상 병합만 사용
            if '/best' in format_id:
                return format_id.split('/')[0].strip()
            return format_id
        # 단일 포맷(비디오만)이면 오디오 스트림 추가
        return f'{format_id}+bestaudio'

    def _get_ffmpeg_required_message(self):
        """ffmpeg 미설치 시 사용자에게 보여줄 안내 문구. 비디오/MP3 다운로드 공통."""
        return (
            "비디오·오디오 다운로드를 위해 'ffmpeg'가 필요합니다.\n\n"
            "설치 방법:\n"
            "• Windows: 명령 프롬프트에서 'winget install ffmpeg' 실행\n"
            "• 또는 https://ffmpeg.org 에서 다운로드 후 PATH에 추가\n\n"
            "설치 후 프로그램을 다시 실행해 주세요."
        )

    def _download_video_thread(self):
        """Download video in background thread"""
        try:
            self.root.after(0, lambda: self.download_button.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.progress_var.set(0))

            # 비디오+오디오 병합에 ffmpeg 필요. 미설치 시 안내 후 중단
            if not self._is_ffmpeg_available():
                msg = self._get_ffmpeg_required_message()
                self.root.after(0, lambda: self.log_message("ffmpeg가 설치되어 있지 않습니다. 비디오 다운로드를 건너뜁니다."))
                self.root.after(0, lambda: self._show_download_error(msg, also_log=False))
                return

            format_id = self.selected_quality['format_id']
            quality_label = self.selected_quality['label']

            self.root.after(0, lambda: self.log_message(f"Starting download: {quality_label}"))

            # 비디오만 있는 포맷 ID(예: 137, 248)면 반드시 +bestaudio 붙여 오디오 포함
            download_format = self._ensure_audio_format(format_id)

            # ffmpeg 경로 명시 (GUI 실행 시 PATH 미적용 방지, 병합 실패 방지)
            ffmpeg_dir = self._get_ffmpeg_path()
            ydl_opts = {
                'format': download_format,
                'outtmpl': os.path.join(self.downloads_path, '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [self._progress_hook],
                'merge_output_format': 'mp4',  # 비디오·오디오 병합 결과를 MP4로 저장
                'overwrites': True,  # 이미 있는 파일도 덮어써서, 소리 없는 이전 파일을 새로 받은 걸로 교체
                # 병합 시 오디오를 AAC로 인코딩 (Opus는 Windows 미디어 플레이어 등에서 재생 불가 → AAC로 변환)
                'postprocessor_args': {'ffmpeg': ['-c:a', 'aac', '-b:a', '192k']},
            }
            if ffmpeg_dir:
                ydl_opts['ffmpeg_location'] = ffmpeg_dir
                self.root.after(0, lambda: self.log_message(f"ffmpeg 사용 경로: {ffmpeg_dir}"))

            # yt-dlp 로그: 경고/오류와 병합·ffmpeg 관련 메시지만 앱 로그에 표시
            def _strip_ansi_log(text):
                if not text:
                    return ""
                return re.compile(r'\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', text)

            def _forward_log(msg, prefix=""):
                if not msg:
                    return
                clean = _strip_ansi_log(msg)
                if not clean:
                    return
                self.root.after(0, lambda m=prefix + clean: self.log_message(m))

            class LogLogger:
                def debug(self, msg):
                    if msg and ("merge" in msg.lower() or "ffmpeg" in msg.lower() or "muxing" in msg.lower()):
                        _forward_log(msg)
                def info(self, msg):
                    if msg and ("merge" in msg.lower() or "ffmpeg" in msg.lower() or "muxing" in msg.lower()):
                        _forward_log(msg)
                def warning(self, msg):
                    _forward_log(msg, "[경고] ")
                def error(self, msg):
                    _forward_log(msg, "[오류] ")

            ydl_opts['logger'] = LogLogger()

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.root.after(0, lambda: self.log_message("Downloading..."))
                info = ydl.extract_info(self.current_url, download=True)
                filename = ydl.prepare_filename(info)

                self.root.after(0, lambda: self._on_download_complete(filename))

        except Exception as e:
            raw_msg = f"Download failed: {str(e)}"
            self.root.after(0, lambda m=raw_msg: self._show_download_error(m))
        finally:
            self.root.after(0, lambda: self.download_button.config(state=tk.NORMAL))

    def start_download_audio(self):
        """Start audio download in a separate thread"""
        thread = threading.Thread(target=self._download_audio_thread)
        thread.daemon = True
        thread.start()

    def _download_audio_thread(self):
        """Download audio in background thread (MP3 변환에 ffmpeg 사용)"""
        try:
            self.root.after(0, lambda: self.download_button.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.progress_var.set(0))
            self.root.after(0, lambda: self.log_message("Starting MP3 download..."))

            # MP3 변환(FFmpegExtractAudio)에 ffmpeg 필요
            if not self._is_ffmpeg_available():
                msg = self._get_ffmpeg_required_message()
                self.root.after(0, lambda: self.log_message("ffmpeg가 설치되어 있지 않습니다. MP3 다운로드를 건너뜁니다."))
                self.root.after(0, lambda: self._show_download_error(msg, also_log=False))
                return

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(self.downloads_path, '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [self._progress_hook],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.root.after(0, lambda: self.log_message("Downloading and converting to MP3..."))
                info = ydl.extract_info(self.current_url, download=True)

                self.root.after(0, lambda: self._on_download_complete(f"{info.get('title', 'audio')}.mp3"))

        except Exception as e:
            raw_msg = f"Download failed: {str(e)}"
            self.root.after(0, lambda m=raw_msg: self._show_download_error(m))
        finally:
            self.root.after(0, lambda: self.download_button.config(state=tk.NORMAL))

    def _progress_hook(self, d):
        """Progress hook callback for yt-dlp"""
        if d['status'] == 'downloading':
            total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)

            if total > 0:
                progress = (downloaded / total) * 100
                self.root.after(0, lambda p=progress: self._update_progress_bar(p))
        elif d['status'] == 'finished':
            self.root.after(0, lambda: self._update_progress_bar(100))
            self.root.after(0, lambda: self.log_message("Download finished!"))

    def _update_progress_bar(self, progress):
        """Update progress bar with custom canvas"""
        # Show progress frame if not visible
        if not self.progress_frame.winfo_viewable():
            self.progress_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.progress_percent.config(text=f"{progress:.1f}%")

        # Get canvas width for progress calculation
        canvas_width = self.progress_bar.winfo_width() or 500
        fill_width = int(canvas_width * (progress / 100))

        # Update the rectangle
        self.progress_bar.coords(self.progress_bar_fill, 0, 0, fill_width, 6)

    def _on_download_complete(self, filename):
        """Called when download is complete"""
        # Hide progress frame
        self.progress_frame.place_forget()

        full_path = os.path.join(self.downloads_path, os.path.basename(filename))

        if os.path.exists(full_path):
            message = f"다운로드 완료!\n\n저장 위치:\n{full_path}"
            self.log_message(message)
            messagebox.showinfo("다운로드 완료", message)
        else:
            message = "다운로드가 완료되었습니다.\n다운로드 폴더를 확인하세요."
            self.log_message(message)
            messagebox.showinfo("다운로드 완료", message)


def main():
    root = tk.Tk()
    app = VideoDownloader(root)
    root.mainloop()


if __name__ == "__main__":
    main()
