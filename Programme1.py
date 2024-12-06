fichier_ics = 'evenementSAE_15.ics'

try:
    with open(fichier_ics, 'r', encoding='utf-8') as f:
        contenu = f.read()
        print(contenu)
except FileNotFoundError:
    print(f"Le fichier {fichier_ics} n'a pas été trouvé.")