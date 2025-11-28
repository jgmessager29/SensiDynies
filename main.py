# ----------------------------------------
# IMPORTS STANDARD
# ----------------------------------------
import os
from datetime import datetime, timezone, timedelta
import random

# ----------------------------------------
# IMPORTS DISCORD
# ----------------------------------------
import discord
from discord.ui import View, Button
from discord.ext import commands

# ----------------------------------------
# HÉBERGEMENT
# ----------------------------------------
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# ----------------------------------------
# CONFIGURATION 
# ----------------------------------------
# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
# Token Discord depuis variable d'environnement Render
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

# ----------------------------------------
# CONFIGURATION DU BOT
# ----------------------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

# ----------------------------------------
# Mini serveur Flask pour Render
# ----------------------------------------
app = Flask('')

@app.route('/')
def home():
    return "SensiDynies en ligne !"

@app.route('/healthz')
def health():
    return "OK"

def run():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run).start()

# ----------------------------------------
# STATUT DU BOT AU LANCEMENT
# ----------------------------------------
@bot.event
async def on_ready():
    if bot.user is None:
        return
    print(f"Bot connecté en tant que {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print(f"Connecté à {len(bot.guilds)} serveur(s)")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="!aide pour les commandes."),
        status=discord.Status.online
    )
    print("Statut du bot défini avec succès !")

# ----------------------------------------
# CONFIGURATION DU SALON DE LOGS
# ----------------------------------------
LOG_CHANNEL_ID = 1443209968865116271

async def send_log_embed(title, description, color=discord.Color.pink()):
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        embed = discord.Embed(title=title, description=description, color=color)
        await channel.send(embed=embed)

recent_kicks = set()
recent_bans = set()

# SALON DE LOGS EVENEMENTS
@bot.event
async def on_member_join(member):
    await send_log_embed("**Arrivée**", f"🛬 **{member}** a rejoint le serveur !", color=discord.Color.pink())

@bot.event
async def on_member_remove(member):
    guild = member.guild
    async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.kick):
        if entry.target.id == member.id and member.id not in recent_kicks:
            recent_kicks.add(member.id)
            await send_log_embed("**Expulsion**", f"⚠️ **{member}** a été expulsé par {entry.user}.", color=discord.Color.pink())
            return
    await send_log_embed("**Départ**", f"🛫 **{member}** a quitté le serveur volontairement.", color=discord.Color.pink())

@bot.event
async def on_member_ban(guild, user):
    if user.id not in recent_bans:
        recent_bans.add(user.id)
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.ban):
            if entry.target.id == user.id:
                await send_log_embed("**Bannissement**", f"⛔ **{user}** a été banni par {entry.user}.", color=discord.Color.pink())
                return
        await send_log_embed("**Bannissement**", f"⛔ **{user}** a été banni du serveur.", color=discord.Color.pink())

@bot.event
async def on_member_update(before, after):
    if before.display_name != after.display_name and not before.bot:
        await send_log_embed("**Changement de pseudo**", f"✏️ **{before}** a changé de pseudo en **{after.display_name}**", color=discord.Color.pink())

@bot.event
async def on_presence_update(before, after):
    if after.bot:
        if before.status != after.status:
            if str(after.status) == "online":
                await send_log_embed(title="Bot connecté", description=f"{after} est maintenant en ligne", color=discord.Color.pink())
            elif str(after.status) == "offline":
                await send_log_embed(title="Bot déconnecté", description=f"{after} est maintenant hors ligne", color=discord.Color.pink())

# ----------------------------------------
# MESSAGE DE BIENVENUE
# ----------------------------------------
@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(1440448854347616290)
    if channel:
        member_number = len(member.guild.members)
        await channel.send(f"{member.mention}")
        embed = discord.Embed(
            title=f"🌿 Bienvenue {member.display_name} 🌿",
            description=(
                f"**Tu es le {member_number}ème membre à rejoindre le serveur !**\n\n"
                "Ici, tu trouveras un espace sûr pour échanger et partager.\n\n"
            ),
            color=discord.Color.pink()
        )
        embed.set_footer(text="Bot SensiDynies et Discord créés par Joguy, CEO Trisked : https://www.trisked.fr")
        await channel.send(embed=embed)

# ----------------------------------------
# RÉACTIONS AUTOMATIQUES AUX MESSAGES
# ----------------------------------------
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "sensidynies" in message.content.lower():
        await message.add_reaction("🛸")
    if "fibromyalgie" in message.content.lower():
        await message.add_reaction("🫂")
    await bot.process_commands(message)

# ----------------------------------------
# CHARGEMENT FICHIERS DES COMMANDES
# ----------------------------------------
def load_dico():
    dico = {}
    with open("dico.txt", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                key, value = line.strip().split(":", 1)
                dico[key.lower()] = value.strip()
    return dico

medical_dict = load_dico()

def load_blagues():
    with open("blagues.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

blagues = load_blagues()

# ----------------------------------------
# COMMANDE !aide
# ----------------------------------------
@bot.command(name="aide", help="Affiche la liste des commandes disponibles et leur description.")
async def aide(ctx, cmd_name=None):
    if cmd_name:
        cmd = bot.get_command(cmd_name)
        if cmd:
            embed = discord.Embed(
                title=f"Aide – {cmd.name}",
                description=cmd.help or "Aucune description disponible.",
                color=discord.Color.pink()
            )
            embed.add_field(name="Utilisation", value=f"`!{cmd.name} {cmd.signature}`", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Commande `{cmd_name}` introuvable.")
    else:
        embed = discord.Embed(
            title="Aide à l'utilisation de SensiDynies",
            description="Voici la liste des commandes disponibles par catégorie :",
            color=discord.Color.pink()
        )

        # --- Assistance ---
        cat1 = "**Assistance**\n"
        cat1 += "`!aide [commande]` : Affiche la commande et sa description.\n"
        cat1 += "`!dico` : Recherche les définitions médicales.\n"
        cat1 += "`!perdu` : Liste des salons pour se repérer.\n"
        embed.add_field(name="\u200b", value=cat1, inline=False)

        # --- Modération ---
        cat2 = "**Modération**\n"
        cat2 += "`!effacer [chiffre]` : Efface un nombre de messages (Admin).\n"
        cat2 += "`!reglement` : Affiche le règlement du serveur.\n"
        embed.add_field(name="\u200b", value=cat2, inline=False)

        # --- Utilitaire ---
        cat3 = "**Utilitaire**\n"
        cat3 += "`!info` : Affiche les informations du bot.\n"
        cat3 += "`!ping` : Vérifie la latence du bot.\n"
        cat3 += "`!astuce` : Guide des astuces Discord.\n"
        embed.add_field(name="\u200b", value=cat3, inline=False)

        # --- Amusement ---
        cat4 = "**Amusement**\n"
        cat4 += "`!choix` : Le bot choisit pour toi.\n"
        cat4 += "`!blague` : Raconte une blague aléatoire.\n"
        embed.add_field(name="\u200b", value=cat4, inline=False)

        embed.set_footer(text="Bot SensiDynies et Discord créés par Joguy, CEO Trisked : 'https://www.trisked.fr/'")
        await ctx.send(embed=embed)

# ----------------------------------------
# COMMANDE !astuce
# ----------------------------------------
@bot.command(name="astuce")
async def astuce_cmd(ctx):
    embed = discord.Embed(
        title="💡 Astuces Discord",
        description=(
            "\u200b\n"
            "🖊️ Changer pseudo ou avatar\n"
            "Adapte ton pseudo ou avatar selon le serveur.\n\n"

            "🔔 Notifications personnalisées\n"
            "Choisis quels salons te notifient pour rester informé sans spam.\n\n"

            "🙈 Masquer ou afficher des salons\n"
            "Affiche seulement les salons que tu souhaites voir pour plus de clarté.\n\n"

            "🏷️ Rôles et mentions\n"
            "Utilise les rôles pour filtrer les messages ou mentionner un groupe précis.\n\n"

            "🤪 Réagir aux messages\n"
            "Ajoute un emoji sous un message pour partager ton sentiment rapidement.\n\n"

            "📌 Épingler des messages\n"
            "Garde les messages importants visibles dans chaque salon.\n\n"

            "⛔ Sécurité des liens\n"
            "Ne clique jamais sur des liens suspects pour protéger ton compte et tes données.\n\n"

            "🛸 Guide officiel Discord (FR)\n"
            "Consulte le guide officiel en français pour tout savoir sur Discord : 'https://support.discord.com/hc/fr'"
        ),
        color=discord.Color.pink()
    )
    await ctx.send(embed=embed)
    
# ----------------------------------------
# COMMANDE !blague
# ----------------------------------------
@bot.command(name="blague", help="Envoie une blague aléatoire 😄")
async def blague(ctx):
    await ctx.send(random.choice(blagues))
    
# ----------------------------------------
# COMMANDE !choix
# ----------------------------------------
@bot.command(name="choix", help="Fais un choix entre plusieurs options. Sépare-les par une virgule.")
async def choix(ctx, *, options=None):
    if not options:
        await ctx.send("Veuillez me donner des options séparées par des virgules.")
        return
    option_list = [opt.strip() for opt in options.split(",") if opt.strip()]
    if len(option_list) < 2:
        await ctx.send("Il faut au moins deux options.")
        return
    await ctx.send(f"🎯 Je choisis : **{random.choice(option_list)}**")
    
# ----------------------------------------
# COMMANDE !dico
# ----------------------------------------
@bot.command(name="dico", help="Donne la définition d'un mot médical. Exemple: !dico fibromyalgie")
async def dico(ctx, *, word: str):
    definition = medical_dict.get(word.lower())
    if definition:
        await ctx.send(f"**{word}** : {definition}")
    else:
        await ctx.send(f"Désolé, je n'ai pas trouvé la définition pour le mot **{word}**.")

# ----------------------------------------
# COMMANDE !effacer
# ----------------------------------------
ADMIN_ROLE_ID = 1443251737803751484

@bot.command(name="effacer")
async def effacer(ctx, amount: int):
    if ADMIN_ROLE_ID not in [role.id for role in ctx.author.roles]:
        await ctx.send("🚫 Cette commande est réservée aux administrateurs.", delete_after=30)
        return
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"💊 Messages effacés x{amount} !", delete_after=30)
    await send_log_embed(title="**!effacer**", description=f"{ctx.author} a effacé {amount} messages dans <#{ctx.channel.id}>")

# ----------------------------------------
# COMMANDE !info
# ----------------------------------------
@bot.command(name="info")
async def info(ctx):
    human_count = len([member for member in ctx.guild.members if not member.bot])
    embed = discord.Embed(
        title="SensiDynies Bot",
        description="Bot SensiDynies et Discord créés par Joguy",
        color=discord.Color.pink()
    )
    embed.add_field(name="Préfixe", value="!", inline=True)
    embed.add_field(name="Latence", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="Membres", value=str(human_count), inline=True)
    embed.set_footer(text="Tapez !aide pour obtenir la liste des commandes.")
    await ctx.send(embed=embed)

# ----------------------------------------
# COMMANDE !perdu
# ----------------------------------------
@bot.command(name="perdu")
async def perdu_cmd(ctx):
    embed = discord.Embed(
        title="🆘 Perdu ? Voici les catégories principales",
        description=(
            "\u200b\n"
            "🔴➖ INFORMATIONS ➖🔴\n"
            "→ Toutes les infos essentielles : règles, annonces et conseils pour utiliser Discord.\n\n"

            "🟢➖ COMMUNICATION ➖🟢\n"
            "→ Échanges entre membres : discussions, partages et suggestions pour le serveur.\n\n"

            "🟠➖ SALONS VOCAUX ➖🟠\n"
            "→ Connecte-toi, parle ou écoute en direct avec les membres pour discuter ou se détendre.\n\n"

            "🟡➖ FORUM QUESTIONS ➖🟡\n"
            "→ Forum ou tu poses tes questions et partage tes expériences sur santé, vie quotidienne, conseils.\n\n"

            "🔵➖ VOTRE RÉGION ➖🔵\n"
            "→ Forum où se retrouvent les membres près de chez toi pour entraide et partages locaux.\n\n"

            "🟣➖ GUICHET ➖🟣\n"
            "→ Zone modération : suivi, gestion du serveur et configuration des bots.\n"
        ),
        color=discord.Color.pink()
    )
    await ctx.send(embed=embed)

# ----------------------------------------
# COMMANDE !ping
# ----------------------------------------
@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! Latence: {latency}ms")
    
# ----------------------------------------
# COMMANDE !reglement
# ----------------------------------------
@bot.command(name="reglement")
async def reglement_cmd(ctx):
    embed = discord.Embed(
        title="📝 Règlement du serveur",
        description=(
# Caractère invisible pour créer un espace
            "\u200b\n"
            "🌿 Bienvenue dans la communauté francophone dédiée aux maladies chroniques !\n\n"
            "👉 Ici, tu trouveras un espace sûr pour échanger ! S’entraider et partager nos expériences avec bienveillance.\n\n"
            "🙏 Serveur chaleureux, respectueux et solidaire ! Merci d’aider à le rendre ainsi.\n\n"
            "👀 Chacun doit se sentir au bon endroit. Merci de respecter les règles qui suivent.\n\n"
# Caractère invisible pour créer un espace
            "\u200b\n"
        
            "**1. Bienveillance avant tout**\n"
            "💛    Respect obligatoire : pas de moqueries ni jugements. Chacun est différent.\n\n"

            "**2. Un serveur pour avancer ensemble**\n"
                "📈 Participation douce, empathie et écoute. Chacun progresse à son rythme.\n\n"

            "**3. Espace sécurisé**\n"
            "🚫    Pas de propos discriminatoires ni contenus choquants, violents ou explicites.\n\n"

            "**4. Confidentialité**\n"
            "🔒    Ne partage jamais d’infos privées. Ce qui est ici reste confidentiel.\n\n"

            "**5. Santé : prudence**\n"
            "🩺    Partage d’expérience ok, mais pas de conseils médicaux dangereux. Consulte un professionnel.\n\n"

            "**6. Sécurité émotionnelle**\n"
            "🥺    Pas de propos alarmistes ou déclencheurs sans contexte. Partage avec respect.\n\n"

            "**7. Canaux et organisation**\n"
            "📌    Utilise les bons salons et lis les descriptions pour garder le serveur clair.\n\n"

            "**8. Publicités et liens**\n"
            "📢    Pas de promo ou liens commerciaux sans accord. Partage de ressources fiable ok.\n\n"

            "**9. Modération**\n"
            "🚸    Les modérateurs veillent au bien-être de tous. Respecte leurs décisions.\n\n"

            "**10. Partage du serveur**\n"
            "🔗    Merci de partager le lien : 'https://discord.gg/az9MUPYSEk'\n\n"

            "**11. Acceptation du règlement**\n"
            "✅    En rejoignant, tu acceptes ces règles. Non-respect = avertissements ou exclusion."
        ),
        color=discord.Color.pink()
    )
    await ctx.send(embed=embed)

# ----------------------------------------
# GESTION DES ERREURS
# ----------------------------------------
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Commande introuvable. Tapez !aide pour voir les commandes disponibles.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas l'autorisation d'utiliser cette commande.")
    else:
        await ctx.send(f"Une erreur s'est produite: {str(error)}")

# ----------------------------------------
# LANCEMENT DU BOT
# ----------------------------------------
if __name__ == "__main__":
    if not TOKEN:
        print("Erreur : DISCORD_BOT_TOKEN introuvable.")
    else:
        bot.run(TOKEN)
