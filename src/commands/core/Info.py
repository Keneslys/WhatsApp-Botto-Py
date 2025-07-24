import time
from libs import BaseCommand, MessageClass
from models.User import User
from models.Group import Group


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "info",
                "category": "core",
                "aliases": ["in", "botinfo"],
                "description": {"content": "Show detailed bot information."},
                "exp": 1,
            },
        )
        self.start_time = time.time()

    def get_uptime(self):
        total_seconds = int(time.time() - self.start_time)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m {seconds}s"

    def exec(self, M: MessageClass, _):
        try:
            bot_name = "Muzn-Bot"
            version = "1.0.0"
            developer = "Jflex_OG"
            uptime = self.get_uptime()
            prefix = self.client.config.prefix
            framework = "Neonize + Custom Handler"

            command_count = len(self.handler.commands)
            total_users = User.objects.count()
            total_groups = Group.objects.count()
            total_mods = len(self.client.config.mods)

            text = f"""
🤖 *Bot Information* 🤖

📛 *Name:* {bot_name}
🛠️ *Version:* {version}
👨‍💻 *Developer:* {developer}
📅 *Uptime:* {uptime}
📦 *Total Commands:* {command_count}
👥 *Users:* {total_users}
👨‍👩‍👧‍👦 *Groups:* {total_groups}
🛡️ *Moderators:* {total_mods}
🔖 *Prefix:* {prefix}
🧠 *Framework:* {framework}
            """.strip()

            self.client.reply_message(text, M)
        except Exception as e:
            self.client.reply_message("❌ Failed to get bot info.", M)
            self.client.log.error(f"[info] {e}")
