"""
bot.py
Bot principal do Telegram
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
import config

# Configuração do logging
logging.basicConfig(
    format=config.LOG_CONFIG["format"],
    level=getattr(logging, config.LOG_CONFIG["level"])
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.application = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /start"""
        try:
            user = update.effective_user
            user_id = user.id
            
            logger.info(f"Usuário {user_id} ({user.first_name}) iniciou o bot")
            
            # Verifica se é o dono
            if user_id == config.OWNER_ID:
                owner_status = "👑 *Dono do Bot* 👑"
            else:
                owner_status = "👤 *Usuário*"
            
            # Mensagem de boas-vindas
            welcome_msg = (
                f"{config.EMOJIS['start']} *Olá, {user.first_name}!* {config.EMOJIS['heart']}\n\n"
                f"{owner_status}\n\n"
                f"{config.MENU_CONFIG['welcome_message']}\n\n"
                f"_{config.MENU_CONFIG['developer']}_\n"
                f"Versão: {config.MENU_CONFIG['version']}"
            )
            
            # Teclado do menu
            keyboard = [
                [
                    InlineKeyboardButton(f"{config.EMOJIS['info']} Sobre", callback_data="menu_about"),
                    InlineKeyboardButton(f"{config.EMOJIS['settings']} Config", callback_data="menu_settings")
                ],
                [
                    InlineKeyboardButton(f"{config.EMOJIS['info']} Ajuda", callback_data="menu_help"),
                    InlineKeyboardButton(f"{config.EMOJIS['info']} Contato", callback_data="menu_contact")
                ],
                [
                    InlineKeyboardButton("🌐 GitHub", url=config.MENU_CONFIG['github'])
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                welcome_msg,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Erro no comando start: {e}")
            await update.message.reply_text(
                f"{config.EMOJIS['error']} Ocorreu um erro! Tente novamente."
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /help"""
        help_text = (
            f"{config.EMOJIS['info']} *COMANDOS DISPONÍVEIS*\n\n"
            "🚀 `/start` - Inicia o bot e mostra menu\n"
            "ℹ️ `/help` - Mostra esta mensagem\n"
            "👨‍💻 `/sobre` - Informações sobre o bot\n\n"
            f"{config.EMOJIS['warning']} *Use o menu interativo para mais opções!*"
        )
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def sobre_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /sobre"""
        sobre_text = (
            f"{config.EMOJIS['info']} *SOBRE O BOT*\n\n"
            f"🤖 *Nome:* Bot Top\n"
            f"📱 *Versão:* {config.MENU_CONFIG['version']}\n"
            f"👨‍💻 *Desenvolvedor:* {config.MENU_CONFIG['developer']}\n"
            f"🐍 *Linguagem:* Python\n"
            f"📚 *Biblioteca:* python-telegram-bot\n\n"
            f"🌐 *GitHub:* {config.MENU_CONFIG['github']}\n\n"
            f"{config.EMOJIS['heart']} _Desenvolvido com carinho para a comunidade_"
        )
        
        await update.message.reply_text(sobre_text, parse_mode='Markdown')
    
    async def menu_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para os botões do menu"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "menu_about":
            message = (
                f"{config.EMOJIS['info']} *SOBRE*\n\n"
                "Este é um bot desenvolvido em Python utilizando a biblioteca "
                "`python-telegram-bot`.\n\n"
                "🔧 *Funcionalidades:*\n"
                "• Menu interativo\n"
                "• Botões inline\n"
                "• Sistema de configuração\n"
                "• Identificação do dono\n\n"
                f"{config.EMOJIS['heart']} _Totalmente personalizável!_"
            )
            
        elif data == "menu_settings":
            message = (
                f"{config.EMOJIS['settings']} *CONFIGURAÇÕES*\n\n"
                "⚙️ *Opções disponíveis:*\n"
                "• Notificações\n"
                "• Idioma\n"
                "• Tema\n\n"
                f"{config.EMOJIS['warning']} *Em breve mais opções!*"
            )
            
        elif data == "menu_help":
            message = (
                f"{config.EMOJIS['info']} *AJUDA*\n\n"
                "📌 *Como usar:*\n"
                "• Use `/start` para abrir o menu\n"
                "• Clique nos botões para navegar\n"
                "• Use `/help` para ver comandos\n\n"
                f"{config.EMOJIS['warning']} *Dúvidas? Entre em contato!*"
            )
            
        elif data == "menu_contact":
            message = (
                f"{config.EMOJIS['info']} *CONTATO*\n\n"
                "📞 *Informações de contato:*\n\n"
                f"👑 *Dono:* ID {config.OWNER_ID}\n"
                f"🌐 *GitHub:* {config.MENU_CONFIG['github']}\n\n"
                f"{config.EMOJIS['warning']} _Reservado para assuntos importantes_"
            )
        
        else:
            message = f"{config.EMOJIS['error']} Opção não reconhecida!"
        
        # Botão para voltar
        keyboard = [[InlineKeyboardButton(f"{config.EMOJIS['back']} Voltar", callback_data="back_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def back_to_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Volta para o menu principal"""
        query = update.callback_query
        await query.answer()
        
        user = query.from_user
        
        welcome_msg = (
            f"{config.EMOJIS['home']} *Menu Principal*\n\n"
            f"Olá novamente, {user.first_name}!\n\n"
            f"{config.MENU_CONFIG['welcome_message']}"
        )
        
        keyboard = [
            [
                InlineKeyboardButton(f"{config.EMOJIS['info']} Sobre", callback_data="menu_about"),
                InlineKeyboardButton(f"{config.EMOJIS['settings']} Config", callback_data="menu_settings")
            ],
            [
                InlineKeyboardButton(f"{config.EMOJIS['info']} Ajuda", callback_data="menu_help"),
                InlineKeyboardButton(f"{config.EMOJIS['info']} Contato", callback_data="menu_contact")
            ],
            [
                InlineKeyboardButton("🌐 GitHub", url=config.MENU_CONFIG['github'])
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=welcome_msg,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para erros"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                f"{config.EMOJIS['error']} Ocorreu um erro inesperado!\n"
                f"Tente novamente mais tarde."
            )
    
    def setup_handlers(self):
        """Configura todos os handlers"""
        # Comandos
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("sobre", self.sobre_command))
        
        # Callbacks do menu
        self.application.add_handler(CallbackQueryHandler(self.menu_callback, pattern="^menu_"))
        self.application.add_handler(CallbackQueryHandler(self.back_to_menu, pattern="^back_menu$"))
        
        # Handler de erros
        self.application.add_error_handler(self.error_handler)
    
    def run(self):
        """Inicia o bot"""
        try:
            logger.info(f"Iniciando Bot Top v{config.MENU_CONFIG['version']}...")
            
            # Cria a aplicação
            self.application = Application.builder().token(config.BOT_TOKEN).build()
            
            # Configura handlers
            self.setup_handlers()
            
            logger.info("Bot iniciado com sucesso!")
            logger.info(f"Dono configurado: ID {config.OWNER_ID}")
            logger.info("Pressione Ctrl+C para parar")
            
            # Inicia polling
            self.application.run_polling(allowed_updates=Update.ALL_UPDATES)
            
        except Exception as e:
            logger.error(f"Erro ao iniciar bot: {e}")
            print(f"❌ Erro: {e}")
            print("🔧 Verifique se o token no config.py está correto!")

def main():
    """Função principal"""
    bot = TelegramBot()
    bot.run()

if __name__ == "__main__":
    main()
