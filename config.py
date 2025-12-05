"""
config.py
Configurações do Bot Telegram
"""

# Token do Bot (obtido com @BotFather no Telegram)
BOT_TOKEN = "8193776420:AAE0rHpcYxkicl57txUG6e1g1o23aGvMKq0"  # Substitua pelo seu token

# ID do Dono (obtido com @userinfobot no Telegram)
OWNER_ID = 6037121105  # Substitua pelo seu ID

# Configurações adicionais
BOT_USERNAME = "@seu_bot"  # Nome de usuário do bot
ADMIN_IDS = [OWNER_ID]  # Lista de administradores

# Configurações do Menu
MENU_CONFIG = {
    "welcome_message": "🌟 *Bem-vindo ao Bot Top!* 🌟\n\n"
                       "Este é um bot desenvolvido com Python e muito carinho!\n\n"
                       "Use os comandos abaixo para navegar:",
    "developer": "Desenvolvido por: Seu Nome",
    "version": "1.0.0",
    "github": "https://github.com/seu-usuario/telegram-bot-top"
}

# Emojis para usar no bot
EMOJIS = {
    "start": "🚀",
    "menu": "📱",
    "settings": "⚙️",
    "info": "ℹ️",
    "warning": "⚠️",
    "success": "✅",
    "error": "❌",
    "home": "🏠",
    "back": "↩️",
    "heart": "❤️"
}

# Configurações de Log
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "filename": "bot.log"  # Opcional: salvar logs em arquivo
}
