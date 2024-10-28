import streamlit as st
from pathlib import Path
from datetime import datetime

def search_files_without_phrase_by_date(directory, phrase, target_date):
    # Liste pour stocker les fichiers ne contenant pas la phrase
    files_without_phrase = []
    total_files_checked = 0  # Compteur de fichiers consultés

    for file_path in Path(directory).glob('*.log'):  # Vérifie uniquement les fichiers .log
        try:
            modification_date = datetime.fromtimestamp(file_path.stat().st_mtime).date()

            if modification_date == target_date:
                total_files_checked += 1
                with file_path.open('r', encoding='utf-8', errors='ignore') as file:
                    # Lecture ligne par ligne pour éviter de charger de gros fichiers en mémoire
                    contains_phrase = any(phrase in line for line in file)

                if not contains_phrase:
                    files_without_phrase.append(file_path.name)
        except (OSError, IOError) as e:
            st.warning(f"Impossible de lire le fichier {file_path}: {e}")
    
    return files_without_phrase, total_files_checked

def verify_directory_access(directory):
    # Vérifie si le répertoire est accessible
    return Path(directory).exists()

# Interface utilisateur avec Streamlit
st.title('Recherche de fichiers log')

# Sélection du répertoire (attention : chemin mappé à vérifier)
directory = r'L:\Admin\Logs\Interfaces\import_prepaie'

# Phrase à chercher
phrase_to_search = st.text_input('Phrase à rechercher', 'Fermeture du journal')

# Date cible (AAA-MM-JJ)
target_date_str = st.text_input('Date cible (AAAA-MM-JJ)', '2024-10-22')

# Bouton pour lancer la recherche
if st.button('Lancer la recherche'):
    if directory and phrase_to_search and target_date_str:
        if verify_directory_access(directory):
            st.success("Le chemin réseau est accessible.")
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
            st.error("Le chemin réseau n'est pas accessible. Vérifiez le chemin et les permissions.")
    else:
        st.warning('Veuillez remplir tous les champs.')
