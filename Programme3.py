import csv
from datetime import datetime

def extraire_evenements_csv(fichier_csv):
    """Lire le fichier CSV et extraire les événements spécifiques à R1.07 TP et RT1-TP A2."""
    evenements = []
    
    try:
        # Ouvrir le fichier CSV en mode lecture avec encodage UTF-8
        with open(fichier_csv, mode='r', encoding='utf-8') as f:
            lecteur_csv = csv.reader(f, delimiter=';')
            entetes = next(lecteur_csv)  # Lire les en-têtes (on ignore ici)
            
            for ligne in lecteur_csv:
                if len(ligne) < 5:  # Si la ligne est mal formée, on l'ignore
                    continue
                
                nom_seance = ligne[0]
                description = ligne[4]
                
                # Filtrer pour ne garder que les événements "R1.07 TP" et "RT1-TP A2"
                if ('R1.07 TP' in nom_seance or 'R1.07 DS TP 2H' in nom_seance) and 'RT1-TP A2' in description:
                    evenement = {
                        'Nom': nom_seance,
                        'Date_debut': ligne[1],
                        'Date_fin': ligne[2],
                        'Lieu': ligne[3],
                        'Description': description
                    }
                    evenements.append(evenement)
    
    except FileNotFoundError:
        print(f"Le fichier {fichier_csv} n'a pas été trouvé.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV : {e}")
    
    return evenements

def calculer_duree(date_debut, date_fin):
    """Calculer la durée en heures entre la date de début et la date de fin."""
    date_debut = datetime.strptime(date_debut, "%Y%m%dT%H%M%SZ")
    date_fin = datetime.strptime(date_fin, "%Y%m%dT%H%M%SZ")
    duree = (date_fin - date_debut).total_seconds() / 3600  # Convertir en heures
    return duree

def generer_csv(fichier_sortie, evenements):
    """Générer le fichier CSV avec les informations triées et organisées."""
    # Correction des titres des colonnes
    entetes = ['Nom de la seance', 'Type de seance', 'Date de la seance', 'Heure de debut', 'Duree (heures)', 'Salle']
    
    try:
        # Ouvrir le fichier en mode écriture avec encodage UTF-8
        with open(fichier_sortie, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            
            # Écrire les en-têtes
            writer.writerow(entetes)
            
            # Trier les événements par date de début (et heure de début)
            evenements_triees = sorted(evenements, key=lambda e: datetime.strptime(e['Date_debut'], "%Y%m%dT%H%M%SZ"))
            
            # Traiter chaque événement et écrire dans le fichier CSV
            for evenement in evenements_triees:
                nom_seance = evenement['Nom']
                description = evenement['Description']
                
                # Extraire la date et heure
                date_debut = evenement['Date_debut']
                date_fin = evenement['Date_fin']
                heure_debut = datetime.strptime(date_debut, "%Y%m%dT%H%M%SZ").strftime('%H:%M')
                date_seance = datetime.strptime(date_debut, "%Y%m%dT%H%M%SZ").strftime('%Y-%m-%d')
                
                # Calculer la durée
                duree = calculer_duree(date_debut, date_fin)
                
                # Extraire le type de séance (TP ou DS TP)
                if 'DS' in nom_seance:
                    type_seance = 'DS TP'
                else:
                    type_seance = 'TP'
                
                # Extraire la salle
                salle = evenement['Lieu']
                
                # Écrire la ligne dans le fichier CSV
                writer.writerow([nom_seance, type_seance, date_seance, heure_debut, f"{duree:.2f}", salle])
        
        print(f"Le fichier CSV '{fichier_sortie}' a été généré avec succès.")
    
    except Exception as e:
        print(f"Erreur lors de la génération du fichier CSV : {e}")

def main():
    # Fichier d'entrée CSV (ce fichier devrait déjà être généré avec vos événements)
    fichier_csv = 'evenements.csv'
    
    # Fichier de sortie CSV
    fichier_sortie = 'R107TPA2.csv'
    
    # Extraire les événements depuis le fichier CSV d'entrée
    evenements = extraire_evenements_csv(fichier_csv)
    
    # Générer le fichier CSV de sortie
    generer_csv(fichier_sortie, evenements)

if __name__ == "__main__":
    main()
