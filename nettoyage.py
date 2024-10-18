import json

# Chemin vers le fichier JSON
json_file_path = 'footer_data3.json'

# Charger les données depuis le fichier JSON
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fonction pour créer les liens complets et supprimer les doublons
def create_full_links(data):
    result = []

    for entry in data:
        base_url = entry['url']
        links_seen = set()  # Pour suivre les liens uniques
        
        full_links = []

        for link_obj in entry['links']:
            link = link_obj['link']

            # Fusionner l'URL de base avec le lien
            full_link = base_url.rstrip('/') + '/' + link.lstrip('/')

            # Ajouter le lien s'il n'a pas encore été vu
            if full_link not in links_seen:
                links_seen.add(full_link)
                full_links.append({
                    "full_link": full_link,
                    "content": link_obj['content']
                })

        result.append({
            "url": base_url,
            "full_links": full_links
        })
    
    return result

# Appeler la fonction pour créer les liens complets
full_links_data = create_full_links(data)

# Sauvegarder les résultats dans un nouveau fichier JSON
output_file_path = 'resultat.json'
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(full_links_data, f, ensure_ascii=False, indent=4)

# Afficher le résultat
for site in full_links_data:
    print(f"Base URL: {site['url']}")
    for link in site['full_links']:
        print(f" - {link['full_link']}: {link['content']}")
    print()
