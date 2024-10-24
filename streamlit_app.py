import streamlit as st
import os
from datetime import datetime

def search_files_without_phrase_by_date(directory, phrase, target_date):
    # Liste pour stocker les fichiers ne contenant pas la phrase
    files_without_phrase = []
    total_files_checked = 0  # Compteur de fichiers consultés

    for filename in os.listdir(directory):
        if filename.endswith('.log'):  # Vérifie les fichiers .log
            file_path = os.path.join(directory, filename)
            modification_time = os.path.getmtime(file_path)
            modification_date = datetime.fromtimestamp(modification_time).date()

            if modification_date == target_date:
                total_files_checked += 1
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()

                if phrase not in content:
                    files_without_phrase.append(filename)
    
    return files_without_phrase, total_files_checked

# Interface utilisateur avec Streamlit
st.title('Recherche de fichiers modifiés sans phrase spécifique')

# Sélection du répertoire
directory = st.text_input('Chemin du répertoire', value=r'C:\Chemin\Vers\Dossier')

# Phrase à chercher
phrase_to_search = st.text_input('Phrase à rechercher', 'Fermeture du journal')

# Date cible (AAA-MM-JJ)
target_date_str = st.text_input('Date cible (AAAA-MM-JJ)', '2024-10-22')

# Bouton pour lancer la recherche
if st.button('Lancer la recherche'):
    if directory and phrase_to_search and target_date_str:
        try:
            target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
            # Appel de la fonction de recherche
            files_without_phrase, total_files_checked = search_files_without_phrase_by_date(directory, phrase_to_search, target_date)

            # Affichage des résultats
            st.write(f'Nombre total de fichiers consultés : {total_files_checked}')
            if files_without_phrase:
                st.write('Fichiers ne contenant pas la phrase :')
                for file in files_without_phrase:
                    st.write(file)
            else:
                st.write(f'Tous les fichiers contiennent la phrase "{phrase_to_search}".')
        except ValueError:
            st.error("Le format de la date est invalide. Utilisez AAAA-MM-JJ.")
    else:
        st.warning('Veuillez remplir tous les champs.')
