from datetime import datetime

def extraire_seances(fichier_ics):
    """Extraire les événements liés à la ressource R1.07."""
    seances = []
    
    try:
        with open(fichier_ics, 'r', encoding='utf-8') as f:
            contenu = f.read()
            evenements_bruts = contenu.split('BEGIN:VEVENT')[1:]
            
            for evenement_brut in evenements_bruts:
                evenement = {}
                
                # Extraire la date de début (DTSTART) et de fin (DTEND)
                if 'DTSTART:' in evenement_brut:
                    evenement['Date_debut'] = evenement_brut.split('DTSTART:')[1].split('\n')[0].strip()
                else:
                    continue
                
                if 'DTEND:' in evenement_brut:
                    evenement['Date_fin'] = evenement_brut.split('DTEND:')[1].split('\n')[0].strip()
                else:
                    continue

                # Extraire le lieu (LOCATION) pour filtrer par ressource
                if 'LOCATION:' in evenement_brut:
                    evenement['Lieu'] = evenement_brut.split('LOCATION:')[1].split('\n')[0].strip()
                else:
                    evenement['Lieu'] = ""
                
                # Extraire la description (DESCRIPTION)
                if 'DESCRIPTION:' in evenement_brut:
                    evenement['Description'] = evenement_brut.split('DESCRIPTION:')[1].split('\n')[0].strip()
                else:
                    evenement['Description'] = ""
                
                # Si la ressource R1.07 est mentionnée dans le lieu, nous ajoutons l'événement
                if 'R1.07' in evenement['Lieu']:
                    seances.append(evenement)
    
    except FileNotFoundError:
        print(f"Le fichier {fichier_ics} n'a pas été trouvé.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier ICS : {e}")
    
    return seances

def calculer_duree(date_debut, date_fin):
    """Calculer la durée entre deux dates (en heures)."""
    format_ics = "%Y%m%dT%H%M%S"
    try:
        debut = datetime.strptime(date_debut, format_ics)
        fin = datetime.strptime(date_fin, format_ics)
        duree = fin - debut
        return duree.total_seconds() / 3600  # Durée en heures
    except ValueError:
        return 0  # Si les dates ne sont pas au bon format, retourne 0

def determiner_type_seance(description):
    """Déterminer le type de la séance (CM, TD, TP)."""
    if 'CM' in description:
        return 'CM'
    elif 'TD' in description:
        return 'TD'
    elif 'TP' in description:
        return 'TP'
    return 'vide'

def generer_tableau_seances(seances):
    """Générer le tableau avec les informations des séances."""
    tableau_seances = []
    
    for seance in seances:
        date_debut = seance.get('Date_debut', 'vide')
        date_fin = seance.get('Date_fin', 'vide')
        description = seance.get('Description', 'vide')
        
        if date_debut != 'vide' and date_fin != 'vide':
            duree = calculer_duree(date_debut, date_fin)
            type_seance = determiner_type_seance(description)
            tableau_seances.append([date_debut, f"{duree:.2f} heures", type_seance])
    
    return tableau_seances

def afficher_tableau_seances(tableau_seances):
    """Afficher le tableau avec les résultats des séances."""
    print("Date de la séance | Durée | Type de séance")
    for ligne in tableau_seances:
        print(f"{ligne[0]} | {ligne[1]} | {ligne[2]}")

def main():
    fichier_ics = 'ADE_RT1_Septembre2023_Decembre2023.ics'  # Nom du fichier .ics à traiter
    
    seances = extraire_seances(fichier_ics)
    tableau_seances = generer_tableau_seances(seances)
    afficher_tableau_seances(tableau_seances)

if __name__ == "__main__":
    main()
