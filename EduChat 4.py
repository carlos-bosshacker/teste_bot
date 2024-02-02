import discord
from discord.ext import commands

# Configurar o bot
prefixo = "!"  # Você pode personalizar o prefixo do bot
token = 'MTIwMDU0NTMxMDYzMjU5MTQ1MQ.GWSPGm.zdpLYS6tXNe4oiJ4pCiuxjjJxNK7Ev6KUwkvUs'

# Definir os intents necessários
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.guilds = True  # Ativa a intenção de servidores (guilds)
intents.message_content = True  # Ativa a intenção de conteúdo de mensagem

# Criar uma instância do bot com os intents
bot = commands.Bot(command_prefix=prefixo, intents=intents)

# Dicionário para armazenar perguntas, respostas e links de imagem
perguntas_e_respostas = {}

# Evento de inicialização
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

# Evento de mensagem
@bot.event
async def on_message(message):
    # Verificar se a mensagem foi enviada por um bot (incluindo o próprio bot)
    if message.author.bot:
        return

    # Verificar a palavra-chave "olá"
    if 'olá' in message.content.lower():
        # Responder com a apresentação
        await message.channel.send(f'Olá, eu sou EduBot, em que posso ajudá-lo?')

    # Verificar se a mensagem contém uma pergunta registrada
    pergunta = message.content.lower()
    if pergunta in perguntas_e_respostas:
        # Responder com a resposta registrada e enviar a imagem
        resposta = perguntas_e_respostas[pergunta]['resposta']
        imagem_url = perguntas_e_respostas[pergunta]['imagem_url']

        await message.channel.send(resposta)
        
        # Verificar se há uma imagem associada
        if imagem_url:
            await message.channel.send(imagem_url)
    else:
        # Pedir uma resposta e registrar a pergunta com imagem
        await message.channel.send(f'Desculpe, não conheço a resposta para "{pergunta}". '
                                   f'Pode me dizer como devo responder? '
                                   f'(Digite !registrarpergunta Sua resposta e anexe uma imagem)')

    # Executar outros eventos de mensagem
    await bot.process_commands(message)

# Comando para registrar uma pergunta e resposta com imagem
@bot.command(name='registrarpergunta')
async def registrar_pergunta(ctx, pergunta: str, resposta: str):
    # Verificar se o usuário anexou uma imagem
    if ctx.message.attachments:
        imagem_url = ctx.message.attachments[0].url
    else:
        imagem_url = None

    # Registrar pergunta, resposta e imagem
    perguntas_e_respostas[pergunta.lower()] = {'resposta': resposta, 'imagem_url': imagem_url}
    await ctx.send(f'A pergunta "{pergunta}" foi registrada com a resposta "{resposta}" e a imagem associada.')

# Rodar o bot
bot.run(token)
