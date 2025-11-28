# ----------------------------------------
# IMPORTS ET CONFIGURATION
# ----------------------------------------
# Pour accéder aux variables d'environnement
import os                           

# Bibliothèque Discord
import discord    
from discord.ui import View, Button
import random

# Pour gérer les commandes du bot
from discord.ext import commands     

# Pour charger les variables d'environnement depuis .env
from dotenv import load_dotenv       

# Flask pour garder le bot actif sur Render
from flask import Flask
from threading import Thread

# Charger les variables d'environnement depuis le fichier .env (local)
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
# HELP PERSONNALISE EN FRANCAIS (!aide)
# ----------------------------------------
# Commande !aide entièrement personnalisée 3 catégories avec backticks
@bot.command(name="aide", help="Affiche la liste des commandes disponibles et leur description.")
async def aide(ctx, cmd_name=None):
    if cmd_name:
        # Aide pour une commande spécifique
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
        # Aide générale
        embed = discord.Embed(
            title="Aide à l'utilisation de SensiDynies",
            description="Voici la liste des commandes disponibles par catégorie :",
            color=discord.Color.pink()
        )

        # Catégorie 1 : Commandes d'aide
        cat1 = "`!aide [commande]` : Affiche la commande et sa description.\n"
        cat1 += "`!dico` : Recheche les définitions en lien avec le médical.\n"
        cat1 += "`!perdu` : Perdu ? Voici la liste pour te repérer dans ce serveur.\n"
        embed.add_field(name="Assistance", value=cat1, inline=False)

        # Catégorie 2 : Utilitaires
        cat2 = "`!astuce` : Guide des astuces pour bien utiliser Discord.\n"
        cat2 += "`!info` : Afficher les informations relatives au bot.\n"
        cat2 += "`!ping` : Vérifie si le bot est réactif et affiche la latence en ms.\n"
        
        embed.add_field(name="Utilitaire", value=cat2, inline=False)

        # Catégorie 3 : Messages amicaux / fun
        cat3 = "`!choix` : Le bot choisit pour toi.\n"
        cat3 += "`!blague` : Raconte une blague aléatoire.\n"

        embed.add_field(name="Amusement", value=cat3, inline=False)

        # Catégorie 4 : Administration
        cat4 = "`!effacer [chiffre]` : Efface le nombre de messages indiqué (Admin).\n"
        cat4 += "`!reglement` : Affiche la charte du serveur.\n"

        embed.add_field(name="Modération", value=cat4, inline=False)

        # Footer
        embed.add_field(
            name="\u200b",  # champ sans titre
            value="Bot SensiDynies et Discord créés par Joguy, CEO Trisked : 'https://www.trisked.fr'",
            inline=False
        )
        await ctx.send(embed=embed)

# Commande !aide entièrement personnalisée 3 catégories avec backticks
# ----------------------------------------
# EVENEMENTS
# ----------------------------------------
# Quand le bot est connecté au serveur
@bot.event
async def on_ready():  
    if bot.user is None:
        return
    print(f"Bot connecté en tant que {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print(f"Connecté à {len(bot.guilds)} serveur(s)")

# Définir le statut du bot 
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="pour les commandes !ping"
        ),
        status=discord.Status.online
    )
    print("Statut du bot défini avec succès !")

# À chaque message reçu, le bot réagit automatiquement
@bot.event
async def on_message(message): 
    if message.author == bot.user:

# Ignorer ses propres messages
        return  

# Réactions automatiques selon mots-clés
    if "sensidynies" in message.content.lower():
        await message.add_reaction("🛸")
    if "fibromyalgie" in message.content.lower():
        await message.add_reaction("🫂")

# Traiter les commandes
    await bot.process_commands(message)  

# Quand un nouveau membre rejoint
@bot.event
async def on_member_join(member): 

# ID du channel de bienvenue 🏠┆sensidynies
    channel = member.guild.get_channel(1440448854347616290)  
    if channel:

        # Numéro du membre dans le serveur
        member_number = len(member.guild.members)
        
# Mention du membre
        await channel.send(f"{member.mention}")

        embed = discord.Embed(
            title=f"🌿 Bienvenue {member.display_name} 🌿",
            description=(
                f"**Tu es le {member_number}ème membre à rejoindre le serveur !**\n\n"
                "Ici, tu trouveras un espace sûr pour échanger et partager.\n\n"
            ),
            color=discord.Color.pink()
        )
# Caractère invisible pour créer un espace
        "\u200b\n"
        
# Ajouter un footer
        embed.set_footer(text="Bot SensiDynies et Discord créés par Joguy, CEO Trisked : "
                "https://www.trisked.fr")

        # Envoi dans le canal
        await channel.send(embed=embed)
# ----------------------------------------
# COMMANDES DU BOT
# ----------------------------------------
#COMMANDE : !perdu
@bot.command(name="perdu")
async def perdu_cmd(ctx):
    # Embed : Catégories du serveur
    embed = discord.Embed(
        title="🆘 Perdu ? Voici les catégories principales pour utiliser Discord facilement dès le début.",
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
    
#COMMANDE : !astuces
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
    
# COMMANDE : !reglement
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
        
            "**1. Bienveillance avant tout**"
            "💛    Respect obligatoire : pas de moqueries ni jugements. Chacun est différent.\n\n"

            "**2. Un serveur pour avancer ensemble**"
                "📈 Participation douce, empathie et écoute. Chacun progresse à son rythme.\n\n"

            "**3. Espace sécurisé**"
            "🚫    Pas de propos discriminatoires ni contenus choquants, violents ou explicites.\n\n"

            "**4. Confidentialité**"
            "🔒    Ne partage jamais d’infos privées. Ce qui est ici reste confidentiel.\n\n"

            "**5. Santé : prudence**"
            "🩺    Partage d’expérience ok, mais pas de conseils médicaux dangereux. Consulte un professionnel.\n\n"

            "**6. Sécurité émotionnelle**"
            "🥺    Pas de propos alarmistes ou déclencheurs sans contexte. Partage avec respect.\n\n"

            "**7. Canaux et organisation**"
            "📌    Utilise les bons salons et lis les descriptions pour garder le serveur clair.\n\n"

            "**8. Publicités et liens**"
            "📢    Pas de promo ou liens commerciaux sans accord. Partage de ressources fiable ok.\n\n"

            "**9. Modération**"
            "🚸    Les modérateurs veillent au bien-être de tous. Respecte leurs décisions.\n\n"

            "**10. Partage du serveur**"
            "🔗    Merci de partager le lien : 'https://discord.gg/az9MUPYSEk'\n\n"

            "**11. Acceptation du règlement**"
            "✅    En rejoignant, tu acceptes ces règles. Non-respect = avertissements ou exclusion."
        ),
        color=discord.Color.pink()
    )
    await ctx.send(embed=embed)
    
# Commande !choix” – le bot choisit pour toi
@bot.command(name="choix", help="Fais un choix entre plusieurs options. Sépare-les par une virgule.")
async def choix(ctx, *, options=None):

        # Si aucune option n'est fournie
        if options is None:
            await ctx.send("Veuillez me donner des options séparées par des virgules.\nExemple : `!choix rouge, bleu, vert`")
            return
        option_list = [opt.strip() for opt in options.split(',')]
        # Sécurité si l'utilisateur envoie juste des virgules
        if len(option_list) < 2:
            await ctx.send("Il faut au moins **deux options** pour faire un choix 😉")
            return
        await ctx.send(f"🎯 Je choisis : **{random.choice(option_list)}**")

# Debut - Commande “!blague” – renvoie une blague aléatoire
def load_blagues():
    with open("blagues.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# Charge les blagues au lancement du bot
blagues = load_blagues()

@bot.command(name="blague", help="Envoie une blague aléatoire 😄")
async def blague(ctx):
    await ctx.send(random.choice(blagues))
# Debut - Commande “!blague” – renvoie une blague aléatoire
    

# Début - Commande !dico
def load_dico():
    dico = {}
    with open("dico.txt", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                key, value = line.strip().split(":", 1)  # Sépare mot et définition par ':'
                dico[key.lower()] = value.strip()        # Supprime espaces inutiles
    return dico

# Charger dès le lancement du bot
medical_dict = load_dico()

@bot.command(name="dico", help="Donne la définition d'un mot médical. Exemple: !dico fibromyalgie")
async def dico(ctx, *, word: str):
    word_lower = word.lower()
    definition = medical_dict.get(word_lower)
    if definition:
        await ctx.send(f"**{word}** : {definition}")
    else:
        await ctx.send(f"Désolé, je n'ai pas trouvé la définition pour le mot **{word}**.")
# Fin - Commande !dico

# Commande !ping
@bot.command(name="ping")  
async def ping(ctx):
    """Vérifie si le bot est réactif et affiche la latence en ms."""
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! Latence: {latency}ms")

# Début : Commande !info
@bot.command(name="info")  
async def info(ctx):
    """Afficher les informations relatives au bot."""
# Nombre de membres humains dans le serveur
    human_count = len([member for member in ctx.guild.members if not member.bot])
# Création de l'embed
    embed = discord.Embed(
        title="SensiDynies Bot",
        description="-# Bot SensiDynies et Discord créés par Joguy, CEO Trisked : 'https://www.trisked.fr'",
# Couleur de l'embed
        color=discord.Color.pink()
    )
# Champ "Préfixe" indiquant le préfixe des commandes
    embed.add_field(name="**Préfixe :**", value="!", inline=True)  
# Champ "Latence" avec la latence du bot en ms
    embed.add_field(name="**Latence :**", value=f"{round(bot.latency * 1000)}ms", inline=True)
# Champ avec membres humains sur le serveur
    embed.add_field(name="**Membres**", value=str(human_count), inline=True)
# Pied de page avec un petit rappel pour l'utilisateur
    embed.set_footer(text="Tapez !aide pour obtenir la liste des commandes.")
# Envoie l'embed dans le canal où la commande a été utilisée
    await ctx.send(embed=embed)
# Fin commande !info

# DEBUT - Suppression des messages
ADMIN_ROLE_ID = 1443251737803751484

@bot.command(name="effacer")
async def effacer(ctx, amount: int):
        # Vérifie si l'utilisateur possède le rôle Admin
        if ADMIN_ROLE_ID not in [role.id for role in ctx.author.roles]:
            await ctx.send("🚫 Cette commande est réservée aux administrateurs.", delete_after=60)
            return

        # Suppression des messages
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"💊 **Posologie :** Messages effacés x{amount} ! Le canal est maintenant totalement indemne, aucun antidouleur requis!", delete_after=60)
# FIN - Suppression des messages

# ----------------------------------------
# GESTION DES ERREURS
# ----------------------------------------
# Quand une commande échoue
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "Commande introuvable. Tapez !aide pour voir les commandes disponibles."
        )
# Quand utilisateur essaie d’exécuter une commande mais qu’il n’a pas les permissions nécessaires.
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas l'autorisation d'utiliser cette commande.")

# Attrape toutes les autres erreurs
    else:
        await ctx.send(f"Une erreur s'est produite: {str(error)}")

# ----------------------------------------
# LANCEMENT DU BOT
# ----------------------------------------
if __name__ == "__main__": 

# Récupérer le token depuis Render
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

if not TOKEN:
    print("Erreur : DISCORD_BOT_TOKEN introuvable dans les variables d'environnement.")
    print("Veuillez définir votre jeton Discord bot comme variable d'environnement.")
else:
    bot.run(TOKEN)
