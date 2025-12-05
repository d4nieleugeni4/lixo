# bot.py
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== FUNÇÕES DO BOT ==========

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o comando /start"""
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name
    
    logger.info(f"Usuário {user_id} ({username}) iniciou o bot")
    
    # Verifica se é o dono
    if user_id == config.OWNER_ID:
        owner_status = "👑 *Dono do Bot* 👑"
    else:
        owner_status = "👤 *Usuário*"
    
    # Mensagem de boas-vindas personalizada
    welcome_msg = (
        f"{config.EMOJIS['start']} *Olá, {username}!* {config.EMOJIS['start']}\n\n"
        f"{owner_status}\n\n"
        f"{config.MENU_CONFIG['welcome_message']}\n\n"
        f"_{config.MENU_CONFIG['developer']}_\n"
        f"Versão: {config.MENU_CONFIG['version']}"
    )
    
    # Criação do teclado do menu
    keyboard = [
        [
            InlineKeyboardButton(f"{config.EMOJIS['info']} Sobre", callback_data="menu_about"),
            InlineKeyboardButton(f"{config.EMOJIS['settings']} Configurações", callback_data="menu_settings")
        ],
        [
            InlineKeyboardButton(f"{config.EMOJIS['info']} Ajuda", callback_data="menu_help"),
            InlineKeyboardButton("🌐 GitHub", url=config.MENU_CONFIG['github'])
        ],
        [
            InlineKeyboardButton(f"{config.EMOJIS['info']} Contato", callback_data="menu_contact")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Envia mensagem com foto (opcional)
    try:
        # Se quiser enviar com foto, descomente as linhas abaixo e adicione uma foto
        # photo_url = "URL_DA_SUA_FOTO_AQUI"
        # await update.message.reply_photo(
        #     photo=photo_url,
        #     caption=welcome_msg,
        #     reply_markup=reply_markup,
        #     parse_mode='Markdown'
        # )
        
        await update.message.reply_text(
            welcome_msg,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem de boas-vindas: {e}")
        await update.message.reply_text(
            welcome_msg,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para os botões do menu"""
    query = update.callback_query
    await query.answer()  # Responde à callback para remover o "loading" no botão
    
    data = query.data
    user = query.from_user
    
    # Define as respostas para cada botão
    if data == "menu_about":
        message = (
            f"{config.EMOJIS['info']} *SOBRE O BOT*\n\n"
            "🤖 *Nome:* Bot Top\n"
            f"📱 *Versão:* {config.MENU_CONFIG['version']}\n"
            "🐍 *Linguagem:* Python\n"
            "📚 *Biblioteca:* python-telegram-bot\n"
            f"👨‍💻 *Desenvolvedor:* {config.MENU_CONFIG['developer']}\n\n"
            "Um bot feito com carinho para demonstrar funcionalidades básicas!"
        )
        
    elif data == "menu_settings":
        message = (
            f"{config.EMOJIS['settings']} *CONFIGURAÇÕES*\n\n"
            "⚙️ *Configurações disponíveis:*\n"
            "• Idioma\n"
            "• Notificações\n"
            "• Tema\n\n"
            f"{config.EMOJIS['warning']} *Em desenvolvimento!*"
        )
        
    elif data == "menu_help":
        message = (
            f"{config.EMOJIS['info']} *AJUDA*\n\n"
            "📌 *Comandos disponíveis:*\n"
            "• /start - Inicia o bot e mostra menu\n"
            "• /help - Mostra esta mensagem\n\n"
            f"{config.EMOJIS['warning']} *Mais comandos em breve!*"
        )
        
    elif data == "menu_contact":
        message = (
            f"{config.EMOJIS['info']} *CONTATO*\n\n"
            "📧 *Para suporte ou dúvidas:*\n\n"
            f"👑 *Dono:* ID {config.OWNER_ID}\n"
            f"🌐 *GitHub:* {config.MENU_CONFIG['github']}\n\n"
            f"{config.EMOJIS['warning']} _Não respondo a spam!_"
        )
        
    else:
        message = "Opção não reconhecida!"
    
    # Botão para voltar ao menu principal
    keyboard = [[InlineKeyboardButton(f"{config.EMOJIS['back']} Voltar ao Menu", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Volta para o menu principal"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    username = user.username or user.first_name
    
    welcome_msg = (
        f"{config.EMOJIS['home']} *Menu Principal*\n\n"
        f"{config.MENU_CONFIG['welcome_message']}"
    )
    
    # Recria o teclado do menu
    keyboard = [
        [
            InlineKeyboardButton(f"{config.EMOJIS['info']} Sobre", callback_data="menu_about"),
            InlineKeyboardButton(f"{config.EMOJIS['settings']} Configurações", callback_data="menu_settings")
        ],
        [
            InlineKeyboardButton(f"{config.EMOJIS['info']} Ajuda", callback_data="menu_help"),
            InlineKeyboardButton("🌐 GitHub", url=config.MENU_CONFIG['github'])
        ],
        [
            InlineKeyboardButton(f"{config.EMOJIS['info']} Contato", callback_data="menu_contact")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=welcome_msg,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o comando /help"""
    help_text = (
        f"{config.EMOJIS['info']} *COMANDOS DISPONÍVEIS*\n\n"
        "🚀 /start - Inicia o bot e mostra o menu interativo\n"
        "ℹ️ /help - Mostra esta mensagem de ajuda\n"
        "👨‍💻 /sobre - Informações sobre o bot\n"
        "📞 /contato - Informações de contato\n\n"
        f"{config.EMOJIS['warning']} *Use o menu interativo para mais opções!*"
    )
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def sobre_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o comando /sobre"""
    sobre_text = (
        f"{config.EMOJIS['info']} *SOBRE ESTE BOT*\n\n"
        f"🤖 *Bot:* @{context.bot.username}\n"
        f"📅 *Versão:* {config.MENU_CONFIG['version']}\n"
        f"👨‍💻 *Desenvolvedor:* {config.MENU_CONFIG['developer']}\n"
        f"🐍 *Tecnologia:* Python + python-telegram-bot\n"
        f"📚 *Código Fonte:* {config.MENU_CONFIG['github']}\n\n"
        "_Desenvolvido com ❤️ para a comunidade Telegram_"
    )
    
    await update.message.reply_text(sobre_text, parse_mode='Markdown')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para erros"""
    logger.error(f"Erro: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            f"{config.EMOJIS['error']} Ocorreu um erro! Tente novamente mais tarde."
        )

# ========== FUNÇÃO PRINCIPAL ==========

def main():
    """Função principal para iniciar o bot"""
    logger.info("Iniciando o Bot Top...")
    
    # Cria a aplicação
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Adiciona os handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("sobre", sobre_command))
    
    # Handler para os callbacks do menu
    application.add_handler(CallbackQueryHandler(menu_callback, pattern="^menu_"))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$"))
    
    # Handler de erros
    application.add_error_handler(error_handler)
    
    # Inicia o bot
    logger.info("Bot iniciado! Pressione Ctrl+C para parar.")
    application.run_polling(allowed_updates=Update.ALL_UPDATES)

if __name__ == '__main__':
    main()
