import discord
from discord.ext import commands
import random
import asyncio

# Configuração do bot
token = 'MTIwMDU0NTMxMDYzMjU5MTQ1MQ.G70ybl.est3_atUmuZf9poNOJ0I0meCBNND5b9x28u3Ks'
prefixo = '!'  # Defina um prefixo padrão (pode ser qualquer string)

# Intents necessários para algumas operações
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.guilds = True  # Ativa a intenção de servidores (guilds)
intents.message_content = True  # Ativa a intenção de conteúdo de mensagem

# Criação do bot com os intents
bot = commands.Bot(command_prefix=prefixo, intents=intents)

# Dicionário para armazenar informações temporárias por usuário
info_usuarios = {}

# Lista de perguntas aleatórias
perguntas_aleatorias = [
    "Qual é a sua cor favorita?",
    "Você gosta de pizza?",
    "Qual é o seu filme favorito?",
    # Adicione mais perguntas aleatórias conforme desejado
]

# Evento de inicialização do bot
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

# Função para identificar nomes próprios
def identificar_nome_proprio(mensagem):
    palavras = mensagem.split()
    nomes_proprios = [palavra for palavra in palavras if palavra.istitle()]
    return nomes_proprios

# Função para processar a pergunta do usuário e formular uma resposta
def processar_pergunta(pergunta):
    # Lógica simples para responder a perguntas específicas
    if 'cor favorita' in pergunta.lower():
        return 'Minha cor favorita é azul!'
    elif 'gosta de pizza' in pergunta.lower():
        return 'Sim, eu adoraria uma fatia agora mesmo!'
    # Adicione mais lógica conforme necessário
    else:
        return 'Desculpe, não entendi. Pode reformular a pergunta?'

# Evento de mensagem
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignora mensagens do próprio bot

    # Verifica a palavra-chave na mensagem
    if 'ola' in message.content.lower():
        apresentacao = f'Olá {message.author.mention}! Eu sou o EduBot, qual é o seu nome?'
        await message.channel.send(apresentacao)

        # Aguarda a resposta do usuário por 60 segundos
        try:
            resposta = await bot.wait_for('message', check=lambda m: m.author == message.author, timeout=60)
            nomes_proprios = identificar_nome_proprio(resposta.content)

            if nomes_proprios:
                nome_usuario = nomes_proprios[0]
                await message.channel.send(f'Muito prazer, {nome_usuario}!')

                # Verifica se o nome do usuário está no "banco"
                if nome_usuario.lower() in info_usuarios:
                    await message.channel.send('Bem-vindo de volta!')

                else:
                    # Adiciona o nome do usuário ao "banco"
                    info_usuarios[nome_usuario.lower()] = {'perguntas': []}

                    # Envia outra mensagem perguntando em como pode ajudar
                    await message.channel.send(f'Em que posso ajudá-lo(a), {nome_usuario}?')

                    # Agora, vamos verificar algumas perguntas específicas e fornecer respostas
                    if 'cor favorita' in resposta.content.lower():
                        await message.channel.send('Minha cor favorita é azul!')

                    # Adicione mais verificações para perguntas específicas conforme necessário

                    # Agora, vamos fazer uma pergunta aleatória
                    pergunta_aleatoria = random.choice(perguntas_aleatorias)
                    await message.channel.send(pergunta_aleatoria)

            else:
                await message.channel.send('Não consegui identificar o seu nome. Vamos tentar de novo?')

        except asyncio.TimeoutError:
            await message.channel.send('Tempo esgotado. Se quiser conversar, estou por aqui!')

    elif message.author.name.lower() in info_usuarios:
        # Armazena a pergunta no "banco"
        info_usuarios[message.author.name.lower()]['perguntas'].append(message.content)

        # Processa a pergunta e formula uma resposta
        resposta = processar_pergunta(message.content)
        await message.channel.send(resposta)

    else:
        # Armazena perguntas não identificadas no "banco" e responde com lógica simples
        info_usuarios[message.author.name.lower()] = {'perguntas': [message.content]}
        resposta = processar_pergunta(message.content)
        await message.channel.send(resposta)

    await bot.process_commands(message)  # Isso é necessário para processar os comandos do bot

# Execução do bot
bot.run(token)
