#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import config

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o comando /start"""
    user_id = update.effective_user.id
    
    # Verifica se o usuário é autorizado
    if user_id != config.USER_ID:
        await update.message.reply_text("❌ *Acesso negado!*\nVocê não tem permissão para usar este bot.", parse_mode='Markdown')
        logger.warning(f"Tentativa de acesso não autorizado: User ID {user_id}")
        return
    
    # Envia mensagem de boas-vindas
    await update.message.reply_text(config.WELCOME_MESSAGE, parse_mode='Markdown')
    logger.info(f"Usuário autorizado {user_id} iniciou o bot")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o comando /help"""
    user_id = update.effective_user.id
    
    if user_id != config.USER_ID:
        await update.message.reply_text("❌ *Acesso negado!*", parse_mode='Markdown')
        return
    
    help_text = """
📚 *Comandos Disponíveis:*

/start - Inicia o bot e mostra mensagem de boas-vindas
/help - Mostra esta mensagem de ajuda
/info - Mostra informações técnicas sobre o bot

🔒 *Segurança:*
• Este bot só responde ao usuário com ID: `6037121105`
• Mensagens de outros usuários serão ignoradas
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o comando /info"""
    user_id = update.effective_user.id
    
    if user_id != config.USER_ID:
        await update.message.reply_text("❌ *Acesso negado!*", parse_mode='Markdown')
        return
    
    info_text = f"""
ℹ️ *Informações do Bot:*

🤖 *Bot ID:* `{config.BOT_TOKEN[:20]}...`
👤 *User ID autorizado:* `{config.USER_ID}`
📦 *Versão:* 1.0.0
🐍 *Python-telegram-bot:* 20.0+

⚙️ *Funcionalidades:*
• Sistema de segurança por ID de usuário
• Mensagem de boas-vindas personalizada
• Logs de atividades
"""
    
    await update.message.reply_text(info_text, parse_mode='Markdown')

async def unauthorized_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para mensagens não autorizadas"""
    user_id = update.effective_user.id
    
    if user_id != config.USER_ID:
        logger.warning(f"Mensagem não autorizada de User ID: {user_id}")
        # Não responde para manter privacidade
        return

def main():
    """Função principal para iniciar o bot"""
    print("🤖 Iniciando o bot...")
    print(f"👤 User ID autorizado: {config.USER_ID}")
    print(f"🔑 Token do bot: {config.BOT_TOKEN[:15]}...")
    
    # Cria a aplicação
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Adiciona handlers de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))
    
    # Handler para outras mensagens (apenas log)
    application.add_handler(telegram.ext.MessageHandler(
        telegram.ext.filters.TEXT & ~telegram.ext.filters.COMMAND,
        unauthorized_message
    ))
    
    # Inicia o bot
    print("✅ Bot iniciado! Pressione Ctrl+C para parar.")
    print("📱 Envie /start no Telegram para testar")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bot parado pelo usuário")
    except Exception as e:
        logger.error(f"Erro ao iniciar bot: {e}")
        print(f"❌ Erro: {e}")
