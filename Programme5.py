import csv
from datetime import datetime
import matplotlib.pyplot as plt
import markdown

def analyser_tp_groupe_a2(fichier_csv):
    # Charger le fichier CSV
    with open(fichier_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        data = [row for row in reader]

    # Filtrer les lignes correspondant au groupe A2 et contenant "TP" dans le titre ou la description
    filtered_data = [
        row for row in data
        if 'A2' in row.get('Description', '') and 'TP' in row.get('Titre', '')
    ]

    # Convertir les dates de début en format datetime et extraire les mois
    months = []
    for row in filtered_data:
        try:
            date_debut = datetime.strptime(row['Date_debut'], '%Y%m%dT%H%M%SZ')
            months.append(date_debut.month)
        except (ValueError, KeyError):
            continue

    # Compter les occurrences par mois (septembre = 9, octobre = 10, novembre = 11, décembre = 12)
    monthly_counts = {9: 0, 10: 0, 11: 0, 12: 0}
    for month in months:
        if month in monthly_counts:
            monthly_counts[month] += 1

    # Générer les graphiques
    months_labels = ['Septembre', 'Octobre', 'Novembre', 'Décembre']
    counts = [monthly_counts[month] for month in [9, 10, 11, 12]]

    # Graphique en barres
    plt.figure(figsize=(10, 6))
    plt.bar(months_labels, counts, color=['blue', 'orange', 'green', 'red'])
    plt.title("Nombre de séances de TP du groupe A2 par mois", fontsize=14)
    plt.xlabel("Mois", fontsize=12)
    plt.ylabel("Nombre de séances", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('GrapheDiagTPA2.png')
    plt.close()

    # Graphique en camembert
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=months_labels, autopct='%1.1f%%', startangle=90, colors=['blue', 'orange', 'green', 'red'])
    plt.title("Répartition des séances de TP du groupe A2 par mois", fontsize=14)
    plt.savefig('GrapheCamTPA2.png')
    plt.close()

def generer_html(fichier_csv):
    # Lire le tableau R107TPA2
    with open(fichier_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)

    # Créer le contenu HTML
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Rapport R107TPA2</title>
</head>
<body>
    <h1>Tableau R107TPA2</h1>
    <table border="1" cellspacing="0" cellpadding="5">
"""

    # Ajouter les lignes du tableau
    for i, row in enumerate(rows):
        html_content += "<tr>"
        for cell in row:
            if i == 0:
                html_content += f"<th>{cell}</th>"
            else:
                html_content += f"<td>{cell}</td>"
        html_content += "</tr>"

    html_content += """
    </table>
    <h1>Graphiques</h1>
    <h2>Graphique en barres</h2>
    <img src="GrapheDiagTPA2.png" alt="Graphique en barres">
    <h2>Graphique en camembert</h2>
    <img src="GrapheCamTPA2.png" alt="Graphique en camembert">
</body>
</html>
"""

    # Écrire dans un fichier HTML
    with open('site_R107TPA2.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print("Le fichier HTML 'site_R107TPA2.html' a été généré avec succès.")

# Analyser les données et générer les graphiques
fichier_csv_evenements = 'evenements.csv'
analyser_tp_groupe_a2(fichier_csv_evenements)

# Générer le fichier HTML
fichier_csv_tableau = 'R107TPA2.csv'
generer_html(fichier_csv_tableau)
