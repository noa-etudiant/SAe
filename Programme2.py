def extraire_evenements_ics(fichier_ics):
    evenements = []
    
    try:
        with open(fichier_ics, 'r', encoding='utf-8') as f:
            contenu = f.read()
            evenements_bruts = contenu.split('BEGIN:VEVENT')[1:]
            
            for evenement_brut in evenements_bruts:
                evenement = {}
                
                if 'SUMMARY:' in evenement_brut:
                    evenement['Titre'] = evenement_brut.split('SUMMARY:')[1].split('\n')[0].strip()
                else:
                    evenement['Titre'] = "vide"
                
                if 'DTSTART:' in evenement_brut:
                    evenement['Date_debut'] = evenement_brut.split('DTSTART:')[1].split('\n')[0].strip()
                else:
                    evenement['Date_debut'] = "vide"
                
                if 'DTEND:' in evenement_brut:
                    evenement['Date_fin'] = evenement_brut.split('DTEND:')[1].split('\n')[0].strip()
                else:
                    evenement['Date_fin'] = "vide"
                
                if 'LOCATION:' in evenement_brut:
                    lieux = evenement_brut.split('LOCATION:')[1].split('\n')[0].strip()
                    evenement['Lieu'] = lieux if lieux else "vide"
                else:
                    evenement['Lieu'] = "vide"
                
                if 'DESCRIPTION:' in evenement_brut:
                    description = evenement_brut.split('DESCRIPTION:')[1].split('\n')[0].strip()
                    evenement['Description'] = description if description else "vide"
                else:
                    evenement['Description'] = "vide"

                evenements.append(evenement)
    
    except FileNotFoundError:
        print(f"Le fichier {fichier_ics} n'a pas été trouvé.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier ICS : {e}")
    
    return evenements

def generer_csv(fichier_csv, evenements):
    entetes = [u'Titre', u'Date_debut', u'Date_fin', u'Lieu', u'Description']
    
    with open(fichier_csv, 'w', encoding='utf-8') as f:
        ligneEntete = ";".join(entetes) + "\n"
        f.write(ligneEntete)
        
        for evenement in evenements:
            ligne = f"{evenement.get('Titre', 'vide')};{evenement.get('Date_debut', 'vide')};{evenement.get('Date_fin', 'vide')};{evenement.get('Lieu', 'vide')};{evenement.get('Description', 'vide')}\n"
            f.write(ligne)

def main():
    fichier_ics = 'ADE_RT1_Septembre2023_Decembre2023.ics'
    fichier_csv = 'evenements.csv'
    
    evenements = extraire_evenements_ics(fichier_ics)
    generer_csv(fichier_csv, evenements)
    print(f"Le fichier CSV '{fichier_csv}' a été créé avec succès.")

if __name__ == "__main__":
    main()
