import unittest
from types import SimpleNamespace
from unittest.mock import patch

from youtube_downloader.core import build_download_options, download_youtube, normalize_format, validate_youtube_url


class TestFormatHandling(unittest.TestCase):
    def test_video_alias_maps_to_mp4(self):
        self.assertEqual(normalize_format("video"), "mp4")
        self.assertEqual(normalize_format("audio"), "mp3")

    def test_validate_youtube_url_accepts_standard_links(self):
        validate_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    @patch("youtube_downloader.core.shutil.which", side_effect=lambda name: None if name in {"ffmpeg", "ffprobe"} else "/usr/bin/true")
    def test_mp3_without_ffmpeg_raises_runtime_error(self, _mock_which):
        with self.assertRaises(RuntimeError) as ctx:
            build_download_options("mp3", output_dir=__import__("pathlib").Path("downloads"), ffmpeg_available=False)
        self.assertIn("FFmpeg/FFprobe", str(ctx.exception))

    def test_download_youtube_uses_ytdlp_when_available(self):
        class DummyYDL:
            def __init__(self, opts):
                self.opts = opts

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def extract_info(self, url, download):
                return {"title": "demo"}

        fake_module = SimpleNamespace(YoutubeDL=DummyYDL)

        with patch("youtube_downloader.core.yt_dlp", fake_module), patch("youtube_downloader.core.shutil.which", return_value="/usr/bin/true"):
            title = download_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "video")

        self.assertEqual(title, "demo")


if __name__ == "__main__":
    unittest.main()
