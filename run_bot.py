import subprocess
import time

while True:
    try:
        # Lancer ton bot
        subprocess.run(["python3", "bot.py"])
    except Exception as e:
        print(f"Erreur : {e}")
    print("Redémarrage du bot dans 5 secondes...")
    time.sleep(5)
