import discord
from discord.ext import commands
import random
import asyncio

prefixo = "!"
bot_token = 'MTIwMDU0NTMxMDYzMjU5MTQ1MQ.GXMmni.VZ1fsx6o2dorHCNjy99jB5AsHIhGik7qFZDDJk'

# Definindo as intenções necessárias
intents = discord.Intents.default()
intents.messages = True  # Ativa a intenção de mensagens
intents.guilds = True  # Ativa a intenção de servidores (guilds)
intents.message_content = True  # Ativa a intenção de conteúdo de mensagem

bot = commands.Bot(command_prefix=prefixo, intents=intents)

# Lista de perguntas e respostas
perguntas_respostas = [
    {"pergunta": "Qual é a cor do céu?", "resposta": "Azul"},
    {"pergunta": "Qual é a capital do Brasil?", "resposta": "Brasília"},
    {"pergunta": "Quanto é 2 + 2?", "resposta": "4"},
    
    # Adicione mais perguntas e respostas conforme necessário
]

@bot.event
async def on_ready():
    print(f'Bot está online como {bot.user.name}')

@bot.command(name='hello', help='Cumprimenta o usuário')
async def hello(ctx):
    await ctx.send(f'Olá {ctx.author.mention}!')

@bot.command(name='pergunta', help='Faz uma pergunta aleatória')
async def pergunta(ctx):
    # Seleciona uma pergunta aleatória
    pergunta_aleatoria = random.choice(perguntas_respostas)
    
    await ctx.send(pergunta_aleatoria["pergunta"])

    # Aguarda a resposta do usuário
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        resposta = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("Tempo esgotado. A resposta não foi recebida.")
        return

    # Verifica se a resposta está correta
    if resposta.content.lower() == pergunta_aleatoria["resposta"].lower():
        await ctx.send("Resposta correta! 🎉")
    else:
        await ctx.send(f"Resposta incorreta. A resposta correta é: {pergunta_aleatoria['resposta']}")

# Certifique-se de usar o evento on_message para processar comandos
@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run(bot_token)
