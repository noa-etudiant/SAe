import csv
from datetime import datetime
import matplotlib.pyplot as plt

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

# Remplacez le chemin par le fichier CSV que vous voulez analyser
fichier_csv = 'evenements.csv'
analyser_tp_groupe_a2(fichier_csv)
