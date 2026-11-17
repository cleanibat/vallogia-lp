# -*- coding: utf-8 -*-
"""Génère les landing pages Google Ads de Vallogia Fils (maçonnerie, Bogny-sur-Meuse, Ardennes).
Usage : python3 build.py
Sources des faits : ancien site https://vallogia.wixsite.com/website (accueil, service personnalisé, réalisations, contact).
"""
import datetime, html, json

# ---------------- Configuration ----------------
GTM_ID = ""                                   # "GTM-XXXXXXX" ; vide = snippet commenté
SITE = "https://www.vallogia.com/"            # domaine final (canonical, sitemap, Open Graph)
INDEX = False                                 # LP Ads : noindex tant que le domaine n'est pas en production
BRAND = "Vallogia Fils"
LEGAL = "Vallogia Fils SARL"
SINCE = 1984
PHONE_DISPLAY, PHONE_INTL = "03 24 32 31 98", "+33324323198"
MOBILE_DISPLAY, MOBILE_INTL = "06 16 38 05 73", "+33616380573"
EMAIL = "vallogia@orange.fr"                  # trouvé sur HelloWatt : à confirmer
ADDRESS_STREET, ADDRESS_CP, ADDRESS_CITY = "Rue des Cerisiers", "08120", "Bogny-sur-Meuse"
INSURER = "SMABTP"
# Qualibat / RGE affichés sur l'ancien site (2018) : à revérifier sur qualibat.com avant d'activer.
QUALIBAT_RGE = False
FORM_ACTION = "contact.php"
YEAR = datetime.date.today().year
TODAY = datetime.date.today().isoformat()
E = html.escape

# ---------------- Icônes ----------------
def ico(p, sw=2):
    return f'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

I = dict(
    PHONE=ico('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>'),
    ARROW=ico('<path d="M5 12h14M13 6l6 6-6 6"/>', 2.2),
    CHECK=ico('<path d="M20 6 9 17l-5-5"/>', 2.6),
    PIN=ico('<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'),
    DOC=ico('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8"/>'),
    SHIELD=ico('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>'),
    CAL=ico('<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>'),
    USERS=ico('<circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0"/><path d="M16 3.5a4 4 0 0 1 0 7.5M22 21a7 7 0 0 0-4-6.3"/>'),
    WALL=ico('<path d="M3 5h18v14H3z"/><path d="M3 10h18M3 15h18M8 5v5M13 10v5M8 15v4M16 5v5M16 15v4"/>'),
    HOME=ico('<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>'),
    HOUSEPLUS=ico('<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/><path d="M12 12v6M9 15h6"/>'),
    SLAB=ico('<path d="M2 17l10 4 10-4"/><path d="M2 12l10 4 10-4"/><path d="M2 7l10 4 10-4-10-4z"/>'),
    SCHOOL=ico('<path d="M3 21h18M5 21V10l7-5 7 5v11"/><path d="M9 21v-5h6v5M10 11h4"/>'),
    STAIRS=ico('<path d="M3 21h5v-5h5v-5h5V6h3"/>'),
    HAMMER=ico('<path d="m15 12-8.5 8.5a2.12 2.12 0 0 1-3-3L12 9"/><path d="M17.64 15 22 10.64M20.91 11.7l-1.25-1.25a2 2 0 0 1-.6-1.42v-.86L16.6 5.7a5.56 5.56 0 0 0-3.94-1.64H9l.92.82A6.18 6.18 0 0 1 12 9.5v1.42l2 2h2.47l2.26 1.91"/>'),
    TILE=ico('<rect x="3" y="3" width="8" height="8"/><rect x="13" y="3" width="8" height="8"/><rect x="3" y="13" width="8" height="8"/><rect x="13" y="13" width="8" height="8"/>'),
    LAYERS=ico('<path d="M4 4h4v16H4z"/><path d="M8 4h3v16H8"/><path d="M14 4h6v16h-6"/>'),
    THERMO=ico('<path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/>'),
    BOLT=ico('<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>'),
    SUN=ico('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
    BRUSH=ico('<path d="M9.06 11.9 17.14 3.8a2.12 2.12 0 0 1 3 3l-8.07 8.08"/><path d="M7.07 14.94c-1.66 0-3 1.35-3 3.02 0 1.33-2.5 1.52-2 2.02 1.08 1.1 2.49 2.02 4 2.02 2.2 0 4-1.8 4-4.04a3.01 3.01 0 0 0-3-3.02z"/>'),
    EURO=ico('<path d="M18 7a7 7 0 1 0 0 10"/><path d="M4 10h9M4 14h9"/>'),
)

LOGO_SVG = ('<svg class="logo-mark" viewBox="0 0 50 34" width="50" height="34" aria-hidden="true">'
            '<path fill="#b6d8e6" d="M1 19.5 15 11.5V33H1z"/><path fill="#b6d8e6" d="M34.5 2.5h8v12h-8z"/>'
            '<path fill="#0e527c" d="M14.5 4.5 21.5 0 49.5 17V30.5h-35z"/><path fill="#b6d8e6" d="M20 15.5h5v7h-5z"/></svg>')

# ---------------- Données communes ----------------
GALLERY = {
    "haulme": ("img/maison-haulme.jpg", "Construction d'une maison à Haulmé", 399, 297),
    "harcy": ("img/extension-ecole-harcy.jpg", "Extension d'une école à Harcy", 1400, 788),
    "carrelage": ("img/carrelage-bogny.jpg", "Pose de carrelage à Bogny-sur-Meuse", 787, 1400),
    "ite": ("img/ite-neufmanil.jpg", "Isolation thermique par l'extérieur à Neufmanil", 1280, 960),
    "danse": ("img/ecole-danse-vireux.jpg", "Construction d'une école de danse à Vireux-Wallerand", 1400, 788),
    "soussol": ("img/pavillon-sous-sol-bogny.jpg", "Pavillon sur sous-sol à Bogny-sur-Meuse", 1400, 814),
    "victorhugo": ("img/extension-ecole-victor-hugo.jpg", "Extension de l'école Victor Hugo à Bogny-sur-Meuse", 1400, 788),
    "plainpied": ("img/pavillon-plain-pied-bogny.jpg", "Pavillon plain-pied à Bogny-sur-Meuse", 787, 1400),
    "grosoeuvre": ("img/gros-oeuvre-maison.jpg", "Gros œuvre d'une maison en briques avec dalle béton", 1400, 853),
    "escalier": ("img/escalier-carrelage.jpg", "Escalier d'entrée rénové et carrelé", 1400, 1046),
    "terrasse": ("img/terrasse-carrelage.jpg", "Terrasse couverte carrelée devant une maison en pierre", 360, 480),
}

ZONE_COLS = [
    ("Vallée de la Meuse", ["Bogny-sur-Meuse", "Monthermé", "Deville", "Haulmé", "Thilay", "Les Hautes-Rivières", "Joigny-sur-Meuse", "Nouzonville"]),
    ("Charleville et alentours", ["Charleville-Mézières", "Neufmanil", "Harcy", "Renwez", "Rimogne", "Tournes"]),
    ("Pointe des Ardennes", ["Revin", "Fumay", "Haybes", "Vireux-Wallerand", "Givet"]),
]

STEPS_CONSTRUCTION = [
    ("Rendez-vous", "Nous vous recevons dans nos locaux pour étudier les plans de votre projet avec vous."),
    ("Étude de prix", "Vous recevez une étude de prix détaillée, poste par poste."),
    ("Planning", "Après acceptation de l'offre, nous fixons ensemble une date estimative de démarrage."),
    ("Réception", "Un procès-verbal de réception clôt le chantier et déclenche la garantie décennale."),
]
STEPS_RENO = [
    ("Visite sur place", "Nous venons voir les travaux à réaliser chez vous."),
    ("Devis détaillé", "Vous recevez une étude de prix détaillée, au plus près de votre projet."),
    ("Planning", "Après acceptation de l'offre, nous fixons ensemble une date estimative de démarrage."),
    ("Réception", "Un procès-verbal de réception clôt le chantier et déclenche la garantie décennale."),
]

FAQ_PRIX = ("Combien coûtent vos travaux ?", "Le prix dépend de la surface, des matériaux, de l'accès et de l'état de l'existant. Nous chiffrons après rendez-vous ou visite sur place : le devis est gratuit et sans engagement.")
FAQ_COLLECT = ("Travaillez-vous pour les entreprises et les collectivités ?", "Oui. Nous avons notamment réalisé l'extension de deux écoles et la construction d'une école de danse dans les Ardennes.")
FAQ_DECENNALE = ("Mes travaux sont-ils couverts par une garantie ?", f"Oui, nos travaux sont couverts par notre assurance décennale ({INSURER}) pendant 10 ans à compter de la réception du chantier.")
FAQ_ZONE = ("Jusqu'où intervenez-vous ?", "Depuis Bogny-sur-Meuse, nous intervenons dans la vallée de la Meuse, à Charleville-Mézières et ses alentours, et jusqu'à Givet.")

# ---------------- Pages ----------------
PAGES = [
  dict(
    file="index.html", lp="Accueil maçonnerie",
    title="Maçon dans les Ardennes, neuf et rénovation | Vallogia Fils",
    desc=f"Entreprise de maçonnerie à Bogny-sur-Meuse depuis {SINCE} : construction de maisons, extensions, rénovation, isolation par l'extérieur, carrelage. Devis gratuit.",
    hero="grosoeuvre", eyebrow="Bogny-sur-Meuse · Vallée de la Meuse · Charleville-Mézières",
    h1="Maçonnerie et gros œuvre <em>dans les Ardennes</em>",
    sub=f"Maisons neuves, extensions, rénovation, isolation par l'extérieur et carrelage. Entreprise de maçonnerie depuis {SINCE}, devis gratuit.",
    besoin=["Construction de maison", "Extension", "Rénovation", "Isolation thermique par l'extérieur", "Carrelage", "Autre"],
    services_h2="Nos travaux",
    services=[
        ("HOME", "Maisons neuves", "Pavillons plain-pied ou sur sous-sol, du terrassement au gros œuvre.", "Le plus demandé", "construction-extension.html"),
        ("HOUSEPLUS", "Extensions", "Agrandissement de maison ou de bâtiment, en continuité avec l'existant.", "", "construction-extension.html"),
        ("WALL", "Rénovation", "Escalier, maison ou bâtiment : reprise de maçonnerie et démolition.", "", "renovation-maconnerie.html"),
        ("LAYERS", "Isolation par l'extérieur", "Enveloppe isolante autour du bâti pour limiter les ponts thermiques.", "Économies d'énergie", "isolation-thermique-exterieur.html"),
        ("TILE", "Carrelage", "Pose de carrelage intérieur, terrasses et escaliers.", "", "renovation-maconnerie.html"),
        ("SCHOOL", "Bâtiments professionnels", "Écoles, salles et locaux pour les entreprises et les collectivités.", "Collectivités", "construction-extension.html"),
    ],
    gallery=["soussol", "danse", "ite", "victorhugo", "haulme", "carrelage"],
    steps=STEPS_RENO, steps_lead="Pour une construction neuve, le premier rendez-vous a lieu dans nos locaux.",
    faq=[FAQ_PRIX, ("Pouvez-vous prendre en charge tout mon projet ?", "Nous réalisons la maçonnerie et le gros œuvre, et nous vous mettons en relation avec des entreprises qualifiées pour les autres corps de métier."), FAQ_DECENNALE, FAQ_COLLECT, FAQ_ZONE],
  ),
  dict(
    file="construction-extension.html", lp="Construction et extension",
    title="Construction de maison et extension, Ardennes | Vallogia Fils",
    desc="Construction de maisons neuves et extensions à Bogny-sur-Meuse, Charleville-Mézières et vallée de la Meuse. Gros œuvre, étude de prix détaillée, devis gratuit.",
    hero="soussol", eyebrow="Maisons neuves · Extensions · Gros œuvre",
    h1="Construction de maison et extension <em>dans les Ardennes</em>",
    sub=f"Nous étudions les plans avec vous et réalisons le gros œuvre de votre maison ou de votre agrandissement. Maçons depuis {SINCE}, devis gratuit.",
    besoin=["Maison plain-pied", "Maison sur sous-sol", "Extension de maison", "Bâtiment professionnel ou public", "Autre"],
    services_h2="Ce que nous construisons",
    services=[
        ("HOME", "Pavillon plain-pied", "Fondations, dalle, élévation des murs et gros œuvre complet.", "Le plus demandé", ""),
        ("SLAB", "Maison sur sous-sol", "Sous-sol, plancher et élévation, adaptés aux terrains en pente de la vallée.", "", ""),
        ("HOUSEPLUS", "Extension", "Pièce en plus, garage ou agrandissement relié à l'existant.", "", ""),
        ("SCHOOL", "Bâtiments publics et pros", "Écoles, salles et locaux : nous en avons construit et agrandi plusieurs.", "Collectivités", ""),
        ("USERS", "Projet de A à Z", "Nous vous mettons en relation avec des entreprises qualifiées pour les autres lots.", "", ""),
        ("WALL", "Gros œuvre seul", "Vous avez déjà votre équipe ? Nous réalisons uniquement la maçonnerie.", "", ""),
    ],
    gallery=["soussol", "plainpied", "haulme", "grosoeuvre", "danse", "harcy"],
    steps=STEPS_CONSTRUCTION, steps_lead="",
    faq=[FAQ_PRIX, ("Faut-il un permis de construire ?", "Oui pour une maison neuve. Pour une extension, c'est une déclaration préalable ou un permis selon la surface et le PLU de la commune."),
         ("Pouvez-vous prendre en charge tout mon projet ?", "Nous réalisons le gros œuvre et vous mettons en relation avec des entreprises qualifiées pour les autres corps de métier."), FAQ_DECENNALE, FAQ_COLLECT],
  ),
  dict(
    file="renovation-maconnerie.html", lp="Rénovation",
    title="Rénovation de maison et maçonnerie, Ardennes | Vallogia Fils",
    desc="Rénovation de maisons et bâtiments, escaliers, démolition et carrelage à Bogny-sur-Meuse et dans les Ardennes. Visite sur place et devis gratuit.",
    hero="escalier", eyebrow="Rénovation · Démolition · Carrelage",
    h1="Rénovation de maison et de bâtiment <em>dans les Ardennes</em>",
    sub="Escalier, maison ou bâtiment : nous venons voir sur place puis vous remettons une étude de prix détaillée. Devis gratuit.",
    besoin=["Rénovation de maison", "Escalier", "Démolition", "Carrelage", "Rénovation de bâtiment", "Autre"],
    services_h2="Ce que nous rénovons",
    services=[
        ("HOME", "Maison", "Reprise de maçonnerie, ouvertures et réaménagement des volumes.", "Le plus demandé", ""),
        ("STAIRS", "Escalier", "Escalier d'entrée ou de jardin refait en maçonnerie et carrelé.", "", ""),
        ("HAMMER", "Démolition", "Démolition de murs, de cloisons ou d'annexes avant rénovation.", "", ""),
        ("TILE", "Carrelage", "Pose de carrelage au sol, sur terrasse et sur escalier.", "", ""),
        ("SCHOOL", "Bâtiment", "Rénovation de bâtiments pour les entreprises et les collectivités.", "Collectivités", ""),
        ("LAYERS", "Isolation par l'extérieur", "À coupler avec la rénovation de vos façades.", "", "isolation-thermique-exterieur.html"),
    ],
    gallery=["escalier", "terrasse", "carrelage", "victorhugo", "harcy", "ite"],
    steps=STEPS_RENO, steps_lead="",
    faq=[FAQ_PRIX, ("Faut-il une autorisation de la mairie ?", "Une modification de façade ou une ouverture demande en général une déclaration préalable. Les travaux intérieurs n'en demandent pas, sauf cas particuliers."),
         ("Posez-vous aussi le carrelage ?", "Oui, nous posons le carrelage intérieur, sur les terrasses et sur les escaliers."), FAQ_DECENNALE, FAQ_ZONE],
  ),
  dict(
    file="isolation-thermique-exterieur.html", lp="Isolation par l'extérieur",
    title="Isolation thermique par l'extérieur (ITE), Ardennes | Vallogia Fils",
    desc="Isolation thermique par l'extérieur à Bogny-sur-Meuse, Charleville-Mézières et vallée de la Meuse. Moins de ponts thermiques, façade rénovée. Devis gratuit.",
    hero="ite", eyebrow="Isolation thermique par l'extérieur · ITE",
    h1="Isolation thermique par l'extérieur <em>dans les Ardennes</em>",
    sub="Une enveloppe isolante continue autour de votre maison pour limiter les ponts thermiques et réduire vos dépenses de chauffage. Visite sur place, devis gratuit.",
    besoin=["Isolation d'une maison", "Isolation d'un bâtiment", "Isolation et rénovation de façade", "Autre"],
    services_h2="Ce que l'ITE change chez vous",
    services=[
        ("THERMO", "Moins de déperditions", "L'isolant couvre murs, tableaux et jonctions : les ponts thermiques sont limités.", "", ""),
        ("EURO", "Factures en baisse", "Une maison mieux isolée demande moins de chauffage l'hiver.", "", ""),
        ("SUN", "Confort été comme hiver", "Les murs restent du côté chaud en hiver et protégés en été.", "", ""),
        ("BRUSH", "Façade refaite", "L'ITE se termine par un enduit : votre façade est rénovée en même temps.", "", ""),
        ("HOME", "Aucune surface perdue", "L'isolation se fait dehors : vos pièces gardent leurs dimensions.", "", ""),
        ("USERS", "Vous restez chez vous", "Les travaux se font depuis l'extérieur, la maison reste habitable.", "", ""),
    ],
    gallery=["ite", "victorhugo", "harcy", "soussol"],
    steps=STEPS_RENO, steps_lead="",
    faq=[FAQ_PRIX, ("Faut-il une autorisation de la mairie ?", "Oui, l'ITE modifie l'aspect de la façade : une déclaration préalable de travaux est en général nécessaire."),
         ("Quelle est la meilleure période ?", "L'enduit de finition demande un temps sec et hors gel : les travaux se font surtout du printemps à l'automne."),
         FAQ_DECENNALE, FAQ_ZONE],
  ),
]

if QUALIBAT_RGE:
    for p in PAGES:
        if p["file"] == "isolation-thermique-exterieur.html":
            p["faq"].insert(1, ("Puis-je bénéficier d'aides ?", "Oui : nous sommes qualifiés Qualibat RGE et joignons à notre étude de prix le dossier de demande d'aides pour les travaux énergétiques."))

# ---------------- Rendu ----------------
def gtm_head():
    s = f"<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID or 'GTM-XXXXXXX'}');</script>"
    return s if GTM_ID else f"<!-- GTM (renseigner GTM_ID dans build.py) {s} -->"

def gtm_body():
    s = f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID or "GTM-XXXXXXX"}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>'
    return s if GTM_ID else f"<!-- {s} -->"

def head(p, img):
    url = SITE + ("" if p["file"] == "index.html" else p["file"])
    ld = {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": BRAND, "legalName": LEGAL,
          "telephone": PHONE_INTL, "email": EMAIL, "url": SITE, "image": SITE + img, "foundingDate": str(SINCE),
          "address": {"@type": "PostalAddress", "streetAddress": ADDRESS_STREET, "postalCode": ADDRESS_CP, "addressLocality": ADDRESS_CITY, "addressCountry": "FR"},
          "areaServed": [c for _, cs in ZONE_COLS for c in cs]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{gtm_head()}
<title>{E(p['title'])}</title>
<meta name="description" content="{E(p['desc'])}">
<meta name="robots" content="{'index, follow' if INDEX else 'noindex, follow'}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{E(p['title'])}"><meta property="og:description" content="{E(p['desc'])}">
<meta property="og:image" content="{SITE}{img}"><meta property="og:url" content="{url}">
<meta name="theme-color" content="#0e527c">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="{img}" fetchpriority="high">
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>
</head>
<body>
{gtm_body()}
"""

def header():
    return f"""<header class="top">
  <div class="wrap top-in">
    <a class="logo" href="index.html" aria-label="{BRAND}, accueil">{LOGO_SVG}<span><b>VALLOGIA FILS</b><small>Maçonnerie · Gros œuvre · Carrelage</small></span></a>
    <div class="top-cta">
      <a class="top-tel" href="tel:{PHONE_INTL}">{I['PHONE']}<span>{PHONE_DISPLAY}</span></a>
      <a class="btn btn-sm" href="#devis">Devis gratuit</a>
    </div>
  </div>
</header>
"""

def form(p):
    opts = "".join(f'<option>{E(b)}</option>' for b in p["besoin"])
    return f"""<form id="devisForm" class="card form" method="POST" action="{FORM_ACTION}">
  <h2 id="devis">Demandez votre devis gratuit</h2>
  <p class="form-lead">Réponse rapide par téléphone ou par e-mail.</p>
  <input type="hidden" name="Source" value="{E(p['lp'])}">
  <input type="text" name="_honey" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
  <label>Nom et prénom<input name="Nom" required autocomplete="name"></label>
  <div class="row2">
    <label>Téléphone<input name="Téléphone" type="tel" required autocomplete="tel"></label>
    <label>Commune<input name="Localité" required autocomplete="address-level2"></label>
  </div>
  <label>E-mail<input name="Email" type="email" required autocomplete="email"></label>
  <label>Votre projet<select name="Besoin" required><option value="">Choisir…</option>{opts}</select></label>
  <label><span>Message <span class="opt">(facultatif)</span></span><textarea name="Message" rows="3" placeholder="Type de travaux, surface, délai souhaité…"></textarea></label>
  <button class="btn btn-full" type="submit" data-sending="Envoi…">Recevoir mon devis gratuit {I['ARROW']}</button>
  <p class="privacy">Vos coordonnées servent uniquement à répondre à votre demande.</p>
</form>"""

def hero(p):
    src, alt, w, h = GALLERY[p["hero"]]
    reas = [("DOC", "Devis gratuit et sans engagement"), ("CAL", f"Entreprise de maçonnerie depuis {SINCE}"),
            ("SHIELD", f"Garantie décennale {INSURER}"), ("PIN", "Visite sur place avant chiffrage")]
    if QUALIBAT_RGE:
        reas[3] = ("CHECK", "Qualifiée Qualibat RGE")
    r = "".join(f'<li>{I[i]}<span>{E(t)}</span></li>' for i, t in reas)
    return f"""<section class="hero">
  <img class="hero-bg" src="{src}" alt="{E(alt)}" width="{w}" height="{h}" fetchpriority="high">
  <div class="wrap hero-in">
    <div class="hero-txt">
      <p class="eyebrow">{E(p['eyebrow'])}</p>
      <h1>{p['h1']}</h1>
      <p class="sub">{E(p['sub'])}</p>
      <div class="ctas">
        <a class="btn" href="#devis">Demander un devis {I['ARROW']}</a>
        <a class="btn btn-ghost" href="tel:{PHONE_INTL}">{I['PHONE']} {PHONE_DISPLAY}</a>
      </div>
      <ul class="reas">{r}</ul>
    </div>
    {form(p)}
  </div>
</section>
"""

def services(p):
    cards = ""
    for icon, t, d, tag, link in p["services"]:
        tagh = f'<span class="tag">{E(tag)}</span>' if tag else ""
        more = f'<a class="more" href="{link}">En savoir plus {I["ARROW"]}</a>' if link and link != p["file"] else ""
        cards += f'<div class="tile"><div class="tile-ico">{I[icon]}</div>{tagh}<h3>{E(t)}</h3><p>{E(d)}</p>{more}</div>'
    return f'<section class="sec"><div class="wrap"><p class="eyebrow">Vallogia Fils</p><h2>{E(p["services_h2"])}</h2><div class="tiles">{cards}</div></div></section>\n'

def gallery(p):
    items = ""
    for k in p["gallery"]:
        src, alt, w, h = GALLERY[k]
        items += f'<figure><img src="{src}" alt="{E(alt)}" width="{w}" height="{h}" loading="lazy"><figcaption>{E(alt)}</figcaption></figure>'
    return f'<section class="sec sec-alt"><div class="wrap"><p class="eyebrow">Réalisations</p><h2>Quelques chantiers dans les Ardennes</h2><div class="gal">{items}</div></div></section>\n'

def steps(p):
    s = "".join(f'<li><span class="num">{n}</span><h3>{E(t)}</h3><p>{E(d)}</p></li>' for n, (t, d) in enumerate(p["steps"], 1))
    lead = f'<p class="lead">{E(p["steps_lead"])}</p>' if p["steps_lead"] else ""
    return f'<section class="sec"><div class="wrap"><p class="eyebrow">Notre service personnalisé</p><h2>Votre chantier en quatre étapes</h2>{lead}<ol class="steps">{s}</ol></div></section>\n'

def trust():
    items = [("CAL", f"Depuis {SINCE}", "Une entreprise de maçonnerie installée à Bogny-sur-Meuse."),
             ("SHIELD", "Assurance décennale", f"Vos travaux sont couverts 10 ans par {INSURER} après la réception."),
             ("DOC", "Procès-verbal de réception", "La fin du chantier est actée par écrit avec vous.")]
    if QUALIBAT_RGE:
        items.append(("CHECK", "Qualibat RGE", "Qualification qui ouvre droit aux aides pour la rénovation énergétique."))
    t = "".join(f'<div class="trust-i">{I[i]}<div><h3>{E(a)}</h3><p>{E(b)}</p></div></div>' for i, a, b in items)
    return f'<section class="band"><div class="wrap trust">{t}</div></section>\n'

def zone():
    cols = "".join(f'<div><h3>{E(t)}</h3><ul>{"".join(f"<li>{E(c)}</li>" for c in cs)}</ul></div>' for t, cs in ZONE_COLS)
    return f'<section class="sec sec-alt"><div class="wrap"><p class="eyebrow">Zone d\'intervention</p><h2>Vallée de la Meuse et Charleville-Mézières</h2><p class="lead">Depuis Bogny-sur-Meuse, chez les particuliers, les entreprises et les collectivités.</p><div class="zone">{cols}</div></div></section>\n'

def faq(p):
    q = "".join(f'<details><summary>{E(a)}</summary><p>{E(b)}</p></details>' for a, b in p["faq"])
    return f'<section class="sec"><div class="wrap narrow"><p class="eyebrow">Questions fréquentes</p><h2>Vos questions</h2><div class="faq">{q}</div></div></section>\n'

def cta_band():
    return f"""<section class="cta-band"><div class="wrap cta-in">
  <div><h2>Un projet de construction ou de rénovation ?</h2><p>Appelez-nous ou demandez votre devis gratuit en ligne.</p></div>
  <div class="ctas"><a class="btn btn-light" href="tel:{PHONE_INTL}">{I['PHONE']} {PHONE_DISPLAY}</a><a class="btn btn-ghost-light" href="#devis">Devis en ligne</a></div>
</div></section>
"""

def footer(current):
    links = "".join(f'<li><a href="{q["file"]}">{E(q["lp"] if q["file"] != "index.html" else "Maçonnerie générale")}</a></li>' for q in PAGES if q["file"] != current)
    return f"""<footer class="foot"><div class="wrap foot-in">
  <div><a class="logo logo-light" href="index.html">{LOGO_SVG}<span><b>VALLOGIA FILS</b><small>Maçonnerie · Gros œuvre · Carrelage</small></span></a>
    <p>{E(ADDRESS_STREET)}, {ADDRESS_CP} {E(ADDRESS_CITY)}</p></div>
  <div><h3>Contact</h3><p><a href="tel:{PHONE_INTL}">Tél. {PHONE_DISPLAY}</a><br><a href="tel:{MOBILE_INTL}">Portable {MOBILE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
  <div><h3>Nos travaux</h3><ul>{links}</ul></div>
</div><p class="copy">© {YEAR} {E(LEGAL)} · <a href="mentions-legales.html">Mentions légales</a></p></footer>
<div class="mbar"><a href="tel:{PHONE_INTL}">{I['PHONE']} Appeler</a><a href="#devis" class="mbar-cta">Devis gratuit</a></div>
<script src="main.js" defer></script>
</body>
</html>
"""

def page(p):
    return head(p, GALLERY[p["hero"]][0]) + header() + "<main>\n" + hero(p) + services(p) + trust() + gallery(p) + steps(p) + zone() + faq(p) + cta_band() + "</main>\n" + footer(p["file"])

def simple(file, title, body, robots="noindex, follow"):
    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
{gtm_head()}
<title>{E(title)} | {BRAND}</title><meta name="robots" content="{robots}"><link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css"></head><body>
{gtm_body()}
{header().replace('href="#devis"', 'href="index.html#devis"')}<main class="sec"><div class="wrap narrow simple">{body}</div></main>
{footer(file).replace('href="#devis"', 'href="index.html#devis"')}"""

MERCI = f"""<h1>Merci, votre demande est bien envoyée</h1>
<p class="lead">Nous revenons vers vous rapidement pour parler de votre projet. Pour une question urgente, appelez-nous au <a href="tel:{PHONE_INTL}">{PHONE_DISPLAY}</a>.</p>
<p><a class="btn" href="index.html">Retour à l'accueil</a></p>"""

MENTIONS = f"""<h1>Mentions légales</h1>
<h2>Éditeur</h2><p>{E(LEGAL)}<br>{E(ADDRESS_STREET)}, {ADDRESS_CP} {E(ADDRESS_CITY)}<br>Téléphone : {PHONE_DISPLAY} · E-mail : {EMAIL}</p>
<h2>Assurance</h2><p>Assurance décennale : {INSURER}.</p>
<h2>Données personnelles</h2><p>Les informations envoyées par le formulaire servent uniquement à répondre à votre demande de devis. Elles ne sont ni cédées ni revendues. Vous pouvez demander leur suppression par e-mail à {EMAIL}.</p>"""

if __name__ == "__main__":
    for p in PAGES:
        open(p["file"], "w").write(page(p))
    open("merci.html", "w").write(simple("merci.html", "Merci", MERCI))
    open("mentions-legales.html", "w").write(simple("mentions-legales.html", "Mentions légales", MENTIONS))
    open("404.html", "w").write(simple("404.html", "Page introuvable", f'<h1>Page introuvable</h1><p><a class="btn" href="index.html">Retour à l\'accueil</a></p>'))
    open("favicon.svg", "w").write(LOGO_SVG.replace(' class="logo-mark"', ' xmlns="http://www.w3.org/2000/svg"'))
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}{'' if p['file']=='index.html' else p['file']}</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGES) if INDEX else ""
    open("sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print("Pages générées :", ", ".join(p["file"] for p in PAGES))
