import requests
import time
import sys

# DeepL API key
DEEPL_API_KEY = "your key"
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

def translate_word(word, target_lang):
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": word,
        "target_lang": target_lang
    }
    try:
        response = requests.get(DEEPL_API_URL, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()["translations"][0]["text"]
    except requests.exceptions.RequestException as e:
        print(f"Error translating '{word}': {e}")
        return None

def create_word_dict():
    common_french_words = [
    "le", "de", "un", "à", "être", "et", "en", "avoir", "que", "pour",
    "dans", "ce", "il", "qui", "ne", "sur", "se", "pas", "plus", "pouvoir",
    "par", "je", "avec", "tout", "faire", "son", "mettre", "autre", "on", "mais",
    "nous", "comme", "ou", "si", "leur", "y", "dire", "elle", "devoir", "avant",
    "deux", "même", "prendre", "aussi", "celui", "donner", "bien", "où", "fois", "vous",
    "petit", "plus", "aller", "jour", "très", "faire", "rien", "grand", "encore", "voir",
    "celui", "sans", "homme", "temps", "nouveau", "après", "année", "là", "bon", "alors",
    "quelque", "venir", "dont", "ainsi", "car", "peu", "moins", "vie", "trois", "pays",
    "monde", "entre", "chose", "femme", "premier", "dernier", "jamais", "trouver", "mer", "état",
    "falloir", "chaque", "parler", "mettre", "jeune", "moment", "pendant", "sans", "autre", "vers",
    "toujours", "maison", "partie", "point", "aujourd'hui", "père", "regarder", "politique", "enfant", "histoire",
    "sortir", "main", "vrai", "côté", "place", "alors", "ensemble", "marcher", "début", "mois",
    "porter", "loin", "fin", "croire", "plutôt", "penser", "quatre", "permettre", "tenir", "chef",
    "politique", "pied", "ville", "mer", "gens", "cas", "entendre", "rendre", "connaître", "type",
    "corps", "dix", "reste", "long", "assez", "raison", "idée", "matin", "suite", "peine",
    "seulement", "beaucoup", "personne", "soit", "famille", "vivre", "comprendre", "cause", "perdu", "tête",
    "question", "essayer", "eau", "manger", "boire", "chien", "chat", "poisson", "oiseau", "arbre",
    "fleur", "soleil", "lune", "étoile", "ciel", "nuage", "pluie", "neige", "vent", "feu",
    "terre", "montagne", "rivière", "océan", "forêt", "désert", "île", "plage", "route", "rue",
    "maison", "appartement", "école", "université", "hôpital", "restaurant", "magasin", "cinéma", "théâtre", "musée",
    "bibliothèque", "parc", "jardin", "zoo", "ferme", "bureau", "usine", "banque", "église", "mosquée",
    "temple", "aéroport", "gare", "port", "pont", "tour", "château", "palais", "statue", "monument",
    "voiture", "vélo", "bus", "train", "avion", "bateau", "métro", "taxi", "moto", "camion",
    "ordinateur", "téléphone", "télévision", "radio", "internet", "livre", "journal", "magazine", "lettre", "stylo",
    "crayon", "papier", "cahier", "sac", "valise", "clé", "montre", "lunettes", "chapeau", "chaussure",
    "vêtement", "pantalon", "chemise", "robe", "jupe", "manteau", "gant", "écharpe", "cravate", "bijou",
    "pain", "fromage", "viande", "poisson", "légume", "fruit", "riz", "pâte", "œuf", "lait",
    "café", "thé", "jus", "vin", "bière", "eau", "sucre", "sel", "huile", "sauce",
    "soupe", "salade", "dessert", "gâteau", "chocolat", "bonbon", "glace", "miel", "confiture", "beurre",
    "médecin", "infirmier", "avocat", "juge", "policier", "pompier", "soldat", "professeur", "étudiant", "élève",
    "vendeur", "client", "patron", "employé", "ouvrier", "agriculteur", "pêcheur", "artiste", "musicien", "acteur",
    "chanteur", "danseur", "peintre", "écrivain", "journaliste", "photographe", "scientifique", "ingénieur", "architecte", "designer",
    "sport", "football", "tennis", "basketball", "volleyball", "natation", "ski", "golf", "boxe", "judo",
    "yoga", "danse", "gymnastique", "athlétisme", "course", "saut", "lancer", "équitation", "voile", "plongée",
    "musique", "chanson", "concert", "instrument", "guitare", "piano", "violon", "batterie", "flûte", "trompette",
    "peinture", "sculpture", "dessin", "photographie", "cinéma", "film", "acteur", "réalisateur", "scène", "caméra",
    "animal", "mammifère", "oiseau", "poisson", "reptile", "amphibien", "insecte", "araignée", "ver", "bactérie",
    "lion", "tigre", "éléphant", "girafe", "singe", "ours", "loup", "renard", "cerf", "lapin",
    "aigle", "hibou", "perroquet", "pingouin", "mouette", "corbeau", "canard", "poule", "coq", "pigeon",
    "requin", "baleine", "dauphin", "pieuvre", "crabe", "homard", "crevette", "moule", "huître", "escargot",
    "serpent", "lézard", "crocodile", "tortue", "grenouille", "crapaud", "salamandre", "triton", "axolotl", "caméléon",
    "abeille", "fourmi", "mouche", "moustique", "papillon", "coccinelle", "scarabée", "libellule", "mante", "phasme",
    "corps", "tête", "cou", "épaule", "bras", "coude", "poignet", "main", "doigt", "ongle",
    "jambe", "genou", "cheville", "pied", "orteil", "dos", "ventre", "poitrine", "cœur", "poumon",
    "cerveau", "estomac", "foie", "rein", "intestin", "muscle", "os", "peau", "cheveu", "barbe",
    "œil", "nez", "bouche", "oreille", "dent", "langue", "lèvre", "joue", "menton", "front",
    "couleur", "rouge", "bleu", "vert", "jaune", "orange", "violet", "rose", "marron", "gris",
    "blanc", "noir", "clair", "foncé", "brillant", "mat", "transparent", "opaque", "arc-en-ciel", "nuance",
    "forme", "carré", "rectangle", "triangle", "cercle", "ovale", "losange", "étoile", "cœur", "flèche",
    "ligne", "courbe", "angle", "point", "surface", "volume", "dimension", "taille", "poids", "masse",
    "longueur", "largeur", "hauteur", "profondeur", "distance", "vitesse", "accélération", "force", "énergie", "puissance",
    "chaleur", "froid", "température", "pression", "densité", "gravité", "friction", "équilibre", "mouvement", "repos",
    "espace", "temps", "durée", "instant", "période", "cycle", "rythme", "fréquence", "passé", "présent",
    "futur", "hier", "aujourd'hui", "demain", "matin", "midi", "soir", "nuit", "aube", "crépuscule",
    "heure", "minute", "seconde", "jour", "semaine", "mois", "année", "siècle", "millénaire", "ère",
    "saison", "printemps", "été", "automne", "hiver", "climat", "météo", "orage", "tempête", "ouragan",
    "typhon", "tornade", "tsunami", "séisme", "volcan", "éruption", "avalanche", "inondation", "sécheresse", "canicule",
    "nord", "sud", "est", "ouest", "direction", "orientation", "boussole", "carte", "globe", "atlas",
    "continent", "pays", "région", "département", "ville", "village", "quartier", "rue", "avenue", "boulevard",
    "place", "carrefour", "impasse", "ruelle", "chemin", "sentier", "piste", "autoroute", "péage", "aire",
    "frontière", "douane", "passeport", "visa", "nationalité", "citoyenneté", "identité", "origine", "culture", "tradition",
    "coutume", "fête", "célébration", "cérémonie", "rituel", "religion", "spiritualité", "croyance", "foi", "mythe",
    "légende", "conte", "fable", "histoire", "récit", "roman", "nouvelle", "poème", "vers", "rime",
    "littérature", "grammaire", "vocabulaire", "syntaxe", "phrase", "mot", "syllabe", "lettre", "accent", "ponctuation",
    "langue", "dialecte", "accent", "prononciation", "intonation", "conversation", "dialogue", "monologue", "discours", "débat",
    "argument", "opinion", "idée", "pensée", "réflexion", "imagination", "créativité", "innovation", "invention", "découverte",
    "science", "théorie", "hypothèse", "expérience", "observation", "analyse", "synthèse", "conclusion", "résultat", "preuve",
    "mathématiques", "calcul", "algèbre", "géométrie", "statistique", "probabilité", "logique", "raisonnement", "problème", "solution",
    "physique", "chimie", "biologie", "géologie", "astronomie", "écologie", "météorologie", "océanographie", "archéologie", "paléontologie",
    "médecine", "anatomie", "physiologie", "pathologie", "diagnostic", "traitement", "thérapie", "chirurgie", "pharmacie", "vaccination",
    "psychologie", "comportement", "émotion", "sentiment", "perception", "mémoire", "apprentissage", "intelligence", "personnalité", "conscience",
    "sociologie", "société", "groupe", "communauté", "organisation", "institution", "gouvernement", "loi", "justice", "droit",
    "économie", "marché", "entreprise", "commerce", "industrie", "agriculture", "finance", "monnaie", "budget", "investissement",
    "politique", "démocratie", "république", "monarchie", "dictature", "élection", "vote", "parti", "parlement", "constitution",
    "diplomatie", "alliance", "conflit", "guerre", "paix", "négociation", "accord", "traité", "convention", "protocole",
    "environnement", "nature", "écosystème", "biodiversité", "pollution", "recyclage", "développement durable", "énergie renouvelable", "conservation", "protection",
    "technologie", "innovation", "progrès", "évolution", "révolution", "intelligence artificielle", "robotique", "nanotechnologie", "biotechnologie", "génétique",
    "informatique", "logiciel", "matériel", "réseau", "internet", "web", "cloud", "cybersécurité", "cryptographie", "blockchain",
    "communication", "média", "presse", "radio", "télévision", "cinéma", "publicité", "marketing", "relations publiques", "propagande",
    "art", "beauté", "esthétique", "style", "mode", "design", "architecture", "urbanisme", "paysage", "décoration",
    "philosophie", "éthique", "morale", "valeur", "principe", "sagesse", "connaissance", "vérité", "réalité", "existence",
    "bonheur", "amour", "amitié", "famille", "mariage", "enfance", "adolescence", "adulte", "vieillesse", "mort",
    "santé", "maladie", "handicap", "bien-être", "confort", "repos", "sommeil", "rêve", "cauchemar", "stress",
    "travail", "carrière", "profession", "métier", "emploi", "chômage", "retraite", "salaire", "revenu", "richesse",
    "pauvreté", "égalité", "inégalité", "discrimination", "préjugé", "stéréotype", "racisme", "sexisme", "homophobie", "xénophobie",
    "liberté", "indépendance", "autonomie", "responsabilité", "devoir", "obligation", "droit", "privilège", "honneur", "dignité",
    "courage", "peur", "confiance", "méfiance", "espoir", "désespoir", "optimisme", "pessimisme", "joie", "tristesse",
    "colère", "calme", "excitation", "ennui", "surprise", "déception", "fierté", "honte", "culpabilité", "pardon",
    "humour", "rire", "sourire", "larme", "plaisir", "douleur", "sensation", "toucher", "goût", "odorat"
     ]
    word_list = []
    for i, french_word in enumerate(common_french_words, 1):
        english_translations = translate_word(french_word, "EN")
        if english_translations:
            turkish_translations = []
            for english_translation in english_translations:
                turkish_translations.extend(translate_word(english_translation, "TR"))
            word_dict = {
                "french": french_word,
                "english": ", ".join(english_translations),
                "turkish": ", ".join(turkish_translations)
            }
            word_list.append(word_dict)
        time.sleep(0)  # To avoid hitting API rate limits
    return word_list

def save_to_file(word_list):
    with open("french_words_translated.py", "w", encoding="utf-8") as f:
        f.write("words = [\n")
        for word in word_list:
            f.write(f"    {word},\n")
        f.write("]\n")

if __name__ == "__main__":
    # Redirect stdout to a file
    with open("translation_output.txt", "w", encoding="utf-8") as f:
        original_stdout = sys.stdout  # Save a reference to the original standard output
        sys.stdout = f  # Redirect standard output to the file
        try:
            print("Starting translation process...")
            word_list = create_word_dict()
            save_to_file(word_list)
            print("Translation process completed.")
        finally:
            sys.stdout = original_stdout  # Reset standard output to its original value
