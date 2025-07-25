import os
import re
import random
import base64
import shutil
import string
import tempfile
import asyncio
import requests
from typing import Union
from bs4 import BeautifulSoup
from typing import List, Set, Any


class Utils:

    @staticmethod
    def sleep(ms: int):
        asyncio.sleep(ms / 1000)

    @staticmethod
    def fetch(url: str) -> Union[dict, None]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ERROR] fetch(): {e}")
            return None

    @staticmethod
    def fetch_buffer(url: str) -> bytes:
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"[ERROR] fetch_buffer(): {e}")
            return b""

    @staticmethod
    def is_truthy(value: Any) -> bool:
        return bool(value)

    @staticmethod
    def readdir_recursive(directory: str) -> List[str]:
        results = []
        for root, _, files in os.walk(directory):
            for file in files:
                results.append(os.path.join(root, file))
        return results

    @staticmethod
    def find_and_delete_all(filename, search_path="."):
        deleted_count = 0
        for root, _, files in os.walk(search_path):
            if filename in files:
                file_path = os.path.join(root, filename)
                try:
                    os.remove(file_path)
                    print(f"[Deleted] {file_path}")
                    deleted_count += 1
                except Exception as e:
                    print(f"[ERROR] Failed to delete {file_path}: {e}")
        if deleted_count == 0:
            print("[info] No matching files found.")
        return deleted_count

    @staticmethod
    def to_small_caps(text):
        map_small = {
            "a": "ᴀ",
            "b": "ʙ",
            "c": "ᴄ",
            "d": "ᴅ",
            "e": "ᴇ",
            "f": "ꜰ",
            "g": "ɢ",
            "h": "ʜ",
            "i": "ɪ",
            "j": "ᴊ",
            "k": "ᴋ",
            "l": "ʟ",
            "m": "ᴍ",
            "n": "ɴ",
            "o": "ᴏ",
            "p": "ᴘ",
            "q": "Q",
            "r": "ʀ",
            "s": "ꜱ",
            "t": "ᴛ",
            "u": "ᴜ",
            "v": "ᴠ",
            "w": "ᴡ",
            "x": "x",
            "y": "ʏ",
            "z": "ᴢ",
        }
        return "".join(map_small.get(c.lower(), c) for c in text)

    @staticmethod
    def buffer_to_base64(buffer: bytes) -> str:
        return base64.b64encode(buffer).decode("utf-8")

    @staticmethod
    def webp_to_mp4(webp: bytes) -> bytes:
        try:

            def request(form_data, file_id=None):
                url = (
                    f"https://ezgif.com/webp-to-mp4/{file_id}"
                    if file_id
                    else "https://ezgif.com/webp-to-mp4"
                )
                return BeautifulSoup(
                    requests.post(url, files=form_data).text, "html.parser"
                )

            files = {"new-image": ("upload.webp", webp, "image/webp")}
            soup1 = request(files)
            file_id = soup1.find("input", {"name": "file"})["value"]

            files = {
                "file": (file_id, "image/webp"),
                "convert": "Convert WebP to MP4!",
            }
            soup2 = request(files, file_id)
            video_url = (
                "https:"
                + soup2.find("div", id="output")
                .find("video")
                .find("source")["src"]
            )
            return requests.get(video_url).content

        except Exception as e:
            print(f"[ERROR] webp_to_mp4(): {e}")
            return b""

    @staticmethod
    def extract_numbers(content: str) -> List[int]:
        return [max(int(n), 0) for n in re.findall(r"-?\d+", content)]

    @staticmethod
    def get_random_int(min_val: int, max_val: int) -> int:
        return random.randint(min_val, max_val)

    @staticmethod
    def get_random_float(min_val: float, max_val: float) -> float:
        return random.uniform(min_val, max_val)

    @staticmethod
    def get_random_item(array: List[Any]) -> Any:
        return random.choice(array)

    @staticmethod
    def get_random_items(array: List[Any], count: int) -> List[Any]:
        return random.choices(array, k=count)

    @staticmethod
    def get_urls(text: str) -> Set[str]:
        return set(re.findall(r"https?://[^\s]+", text))

    @staticmethod
    def random_alpha_string(length=10):
        return "".join(random.choices(string.ascii_letters, k=length))

    @staticmethod
    def format_duration(seconds):
        if not seconds:
            return "N/A"
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if h:
            return f"{h:02}:{m:02}:{s:02}"
        return f"{m:02}:{s:02}"

    @staticmethod
    def format_filesize(size_bytes):
        if not size_bytes:
            return "Unknown"
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024

    @staticmethod
    def format_timedelta(delta):
        days = delta.days
        seconds = delta.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        parts = []
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        return " ".join(parts) if parts else "just now"
