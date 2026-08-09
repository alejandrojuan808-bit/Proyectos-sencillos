import unittest
from unittest.mock import patch

from main import download_youtube, normalize_format, validate_youtube_url


class TestFormatHandling(unittest.TestCase):
    def test_video_alias_maps_to_mp4(self):
        self.assertEqual(normalize_format("video"), "mp4")
        self.assertEqual(normalize_format("audio"), "mp3")

    def test_validate_youtube_url_accepts_standard_links(self):
        validate_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    @patch("main.shutil.which", side_effect=lambda name: None if name in {"ffmpeg", "ffprobe"} else "/usr/bin/true")
    def test_mp4_without_ffmpeg_raises_clear_error(self, _mock_which):
        with self.assertRaises(RuntimeError) as ctx:
            download_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "video")
        self.assertIn("ffmpeg", str(ctx.exception).lower())


if __name__ == "__main__":
    unittest.main()
