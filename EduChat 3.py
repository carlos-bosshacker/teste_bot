import discord
from discord.ext import commands
import sqlite3
import random
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('perguntas_respostas.db')
cursor = conn.cursor()

# Criar a tabela se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS faq (
        pergunta TEXT PRIMARY KEY,
        resposta TEXT
    )
''')
conn.commit()

# Dicionário para armazenar mensagens do bot
mensagens_bot = {}

# Dicionário para armazenar configurações dinâmicas do bot
configuracoes_dinamicas = {
    'nome_bot': 'EduBot STEAM vestibular',
    'funcionalidade_ativa': True,
    # Adicione mais configurações conforme necessário
}

# Perguntas predefinidas
perguntas_possiveis = [
    "Qual é a sua cor favorita?",
    "Qual é o seu animal favorito?",
    "O que você gosta de fazer nas horas vagas?",
    "Qual é o seu filme favorito?",
    "Qual o nome das organelas da célula vegetal?"
        
    # Adicione mais perguntas conforme desejado
]

@bot.event
async def on_ready():
    print(f'Bot está pronto! Conectado como {bot.user.name} ({bot.user.id})')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Declaração da variável nome_usuario fora do bloco "olá"
    nome_usuario = None

    # Verificar se a palavra-chave está presente na mensagem
    if 'olá' in message.content.lower():
        # Responder à mensagem com a saudação e perguntar pelo nome
        embed = discord.Embed(
            title=f'Olá, me chamo {configuracoes_dinamicas["nome_bot"]}',
            description=f'Qual o seu nome?',
            color=discord.Color.blue()
        )
        resposta = await message.channel.send(embed=embed)
        mensagens_bot[message.id] = resposta.id

        # Esperar pela resposta do usuário
        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            resposta = await bot.wait_for('message', timeout=30, check=check)
            nome_usuario = resposta.content

            # Responder com a saudação personalizada
            embed = discord.Embed(
                title=f'Prazer em te conhecer, {nome_usuario}!',
                description='Em que posso ajudar você?',
                color=discord.Color.green()
            )
            await message.channel.send(embed=embed)
        except asyncio.TimeoutError:
            await message.channel.send('Tempo esgotado. Se precisar de ajuda, estou aqui!')

    # Verificar se a mensagem é uma pergunta
    if '?' in message.content:
        pergunta = message.content.lower()

        # Verificar se a pergunta já está no banco de dados
        cursor.execute('SELECT resposta FROM faq WHERE pergunta = ?', (pergunta,))
        resultado = cursor.fetchone()

        if resultado:
            # Se a pergunta já foi feita antes, usar a resposta armazenada
            embed = discord.Embed(
                title='Resposta:',
                description=f'**{resultado[0]}**',
                color=discord.Color.purple()
            )
            resposta = await message.channel.send(embed=embed)
            mensagens_bot[message.id] = resposta.id
        else:
            # Se a pergunta é nova, pedir ao usuário uma resposta e armazenar
            embed = discord.Embed(
                title=f'Desculpe, não conheço a resposta.',
                description=f'Qual seria a resposta para a pergunta: "{message.content}"?',
                color=discord.Color.orange()
            )
            resposta = await message.channel.send(embed=embed)
            mensagens_bot[message.id] = resposta.id
            resposta = await bot.wait_for('message', check=lambda m: m.author == message.author)
            
            # Armazenar a pergunta e resposta no banco de dados
            cursor.execute('INSERT INTO faq (pergunta, resposta) VALUES (?, ?)', (pergunta, resposta.content))
            conn.commit()
            embed = discord.Embed(
                title='Pergunta e resposta armazenadas com sucesso!',
                color=discord.Color.green()
            )
            await message.channel.send(embed=embed)

    # Alterar a condição para "me pergunte"
    if 'me pergunte' in message.content.lower():
        # Selecionar uma pergunta aleatória da lista de perguntas predefinidas
        pergunta_aleatoria = random.choice(perguntas_possiveis)
        embed = discord.Embed(
            title='Pergunta Aleatória:',
            description=f'**{pergunta_aleatoria}**',
            color=discord.Color.gold()
        )
        resposta_pergunta_aleatoria = await message.channel.send(embed=embed)
        mensagens_bot[message.id] = resposta_pergunta_aleatoria.id

        # Aguardar a resposta do usuário
        try:
            resposta_usuario = await bot.wait_for('message', timeout=30, check=lambda m: m.author == message.author)
            
            # Verificar se a resposta contém o próprio nome do usuário
            if nome_usuario and nome_usuario.lower() in resposta_usuario.content.lower():
                # Saudação personalizada se o próprio nome do usuário for mencionado na resposta
                saudacao_personalizada = f'Olá, {nome_usuario}! Como posso ajudar você?'
                embed_saudacao = discord.Embed(
                    title='Saudação Personalizada:',
                    description=saudacao_personalizada,
                    color=discord.Color.green()
                )
                await message.channel.send(embed=embed_saudacao)
            else:
                # Responder logicamente à pergunta do usuário
                resposta_logica = obter_resposta_logica(resposta_usuario.content)
                embed_logica = discord.Embed(
                    title='Resposta Lógica:',
                    description=f'**{resposta_logica}**',
                    color=discord.Color.teal()
                )
                await message.channel.send(embed=embed_logica)
        except asyncio.TimeoutError:
            await message.channel.send('Tempo esgotado. Se precisar de ajuda, estou aqui!')

    # Verificar palavras-chave para alterar configurações dinâmicas
    if 'alterar nome' in message.content.lower():
        await alterar_nome_bot(message)
    elif 'desativar funcionalidade' in message.content.lower():
        await desativar_funcionalidade(message)
    elif 'adicionar comando' in message.content.lower():
        await adicionar_comando(message)
    # Adicione mais palavras-chave conforme necessário

    await bot.process_commands(message)

def obter_resposta_logica(resposta_usuario):
    # Implemente lógica personalizada para responder à resposta do usuário
    # Por enquanto, retorna uma resposta genérica
    return f"Que legal! Obrigado por compartilhar. Posso te ajudar em mais alguma coisa?"

async def alterar_nome_bot(message):
    # Verificar se o autor da mensagem é um administrador ou usuário autorizado
    if message.author.guild_permissions.administrator:
        novo_nome = message.content.split('alterar nome ')[-1]
        await bot.user.edit(username=novo_nome)
        configuracoes_dinamicas['nome_bot'] = novo_nome
        embed = discord.Embed(
            title=f'Nome do bot alterado para: {novo_nome}',
            color=discord.Color.blue()
        )
        await message.channel.send(embed=embed) 

async def desativar_funcionalidade(message):
    # Verificar se o autor da mensagem é um administrador ou usuário autorizado
    if message.author.guild_permissions.administrator:
        configuracoes_dinamicas['funcionalidade_ativa'] = False
        embed = discord.Embed(
            title='Funcionalidade Desativada.',
            color=discord.Color.red()
        )
        await message.channel.send(embed=embed)

async def adicionar_comando(message):
    # Verificar se o autor da mensagem é um administrador ou usuário autorizado
    if message.author.guild_permissions.administrator:
        # Obter o comando a ser adicionado
        novo_comando = message.content.split('adicionar comando ')[-1]
        embed = discord.Embed(
            title=f'Comando adicionado: !{novo_comando}',
            color=discord.Color.green()
        )
        await message.channel.send(embed=embed)
        # Adicionar o novo comando à lista de comandos
        bot.command(name=novo_comando)(lambda ctx: ctx.send(f'Este é o comando !{novo_comando}'))

@bot.command(name='hello', help='Responde com uma saudação')
async def hello(ctx):
    if configuracoes_dinamicas['funcionalidade_ativa']:
        embed = discord.Embed(
            title=f'Olá, {ctx.author.display_name}!',
            description=f'Eu sou {configuracoes_dinamicas["nome_bot"]}.',
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title='Funcionalidade Desativada.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command(name='hd', help='Mostra as perguntas e respostas armazenadas')
async def mostrar_armazenamento(ctx):
    cursor.execute('SELECT * FROM faq')
    perguntas_respostas = cursor.fetchall()

    if perguntas_respostas:
        embed = discord.Embed(
            title='Perguntas e Respostas Armazenadas:',
            color=discord.Color.blue()
        )
        for pergunta, resposta in perguntas_respostas:
            embed.add_field(name=f'Pergunta: "{pergunta}"', value=f'Resposta: **{resposta}**', inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title='Nenhuma pergunta e resposta armazenada no momento.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

# Substitua 'SEU_TOKEN_AQUI' pelo token real do seu bot
bot.run('MTIwMDU0NTMxMDYzMjU5MTQ1MQ.GPs2An.-W3vQ8C2Tsbmcn9uPpobsSjbogDsEp4AMXZaow')

# Fechar a conexão com o banco de dados ao encerrar o bot
conn.close()
