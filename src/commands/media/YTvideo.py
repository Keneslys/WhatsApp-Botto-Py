from libs import BaseCommand, MessageClass
import yt_dlp
import os


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "ytvideo",
                "category": "media",
                "aliases": ["ytv"],
                "description": {
                    "content": "Download video from YouTube links (max 3).",
                    "usage": "<urls>",
                },
                "exp": 2,
            },
        )

    def exec(self, M: MessageClass, _):
        if not M.urls:
            return self.client.reply_message(
                "⚠️ Please provide *YouTube* links.", M
            )

        if len(M.urls) > 3:
            return self.client.reply_message(
                "⚠️ You can only provide up to *3 links*.", M
            )

        os.makedirs("downloads", exist_ok=True)

        for link in M.urls:
            try:
                random_filename = self.client.utils.random_alpha_string(10)
                output_path = os.path.join(
                    "downloads", f"{random_filename}.%(ext)s"
                )

                ydl_opts = {
                    "format": "best[ext=mp4]/best",
                    "quiet": True,
                    "outtmpl": output_path,
                    "noplaylist": True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=True)
                    title = info.get("title", "Unknown Title")
                    ext = info.get("ext", "mp4")
                    downloaded_file = os.path.join(
                        "downloads", f"{random_filename}.{ext}"
                    )

                if not os.path.exists(downloaded_file):
                    self.client.reply_message(
                        f"❌ Failed to find downloaded video for {title}", M
                    )
                    continue

                size = os.path.getsize(downloaded_file)
                if size > 100 * 1024 * 1024:
                    os.remove(downloaded_file)
                    self.client.reply_message(
                        f"❌ File size exceeds 100MB for: *{title}* ({self.client.utils.format_filesize(size)})",
                        M,
                    )
                    continue

                self.client.send_video(
                    M.gcjid,
                    file=downloaded_file,
                    caption=(
                        f"🎬 *Title:* {title}\n"
                        f"📦 *Size:* {self.client.utils.format_filesize(size)}\n"
                        f"📍 *Link:* {link}"
                    ),
                    quoted=M,
                )
                os.remove(downloaded_file)

            except Exception as e:
                self.client.reply_message(
                    f"❌ Error downloading video:\n{link}", M
                )
                self.client.log.error(f"[YouTubeVideoDownloadError] {e}")
