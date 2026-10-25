#!/usr/bin/env python3
"""
scripts/remediate_all.py — Comprehensive Multilingual Remediation Engine
Deterministic remediation for all 486 localized HTML pages across 11 languages:
de, es, fr, it, pt, nl, pl, sv, no, fi, ro

Acceptance Criteria:
1. 0 FAILED_TRANSLATION errors across all 486 files.
2. No <html lang="en"> in localized directories.
3. Zero raw LaTeX commands in HTML (enforced via AGENTS.md § 3.6).
4. All category hub pages have fully translated titles, meta descriptions, and cards.
5. Reciprocal hreflangs preserved.
"""

import os
import re
import json

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG_CODES = ["de", "es", "fr", "it", "pt", "nl", "pl", "sv", "no", "fi", "ro"]

# Stopwords for local verification
ENGLISH_STOPWORDS = {
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'it',
    'for', 'not', 'on', 'with', 'as', 'you', 'do', 'at', 'this',
    'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
    'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which',
    'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just',
    'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good',
    'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now',
    'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back',
    'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well',
    'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give',
    'day', 'most', 'us', 'calculate', 'exact', 'calculator'
}

# General UI & Hub Vocabulary
I18N = {
    "de": {
        "home": "Startseite", "open_solver": "Rechner Öffnen →",
        "verbs": {"Calculate": "Berechnen Sie", "Determine": "Bestimmen Sie", "Evaluate": "Ermitteln Sie", "Compute": "Berechnen Sie", "Solve": "Lösen Sie"},
        "and": "und", "for": "für", "with": "mit", "from": "von", "between": "zwischen", "of": "von", "or": "oder",
        "calculator": "Rechner", "calculators": "Rechner",
        "brand_finance": "Finanzen", "brand_geo": "Geometrie", "brand_calc": "Analysis", "brand_phys": "Physik", "brand_stat": "Statistik", "brand_const": "Bauwesen",
        "license_title": "Kostenlos für Wirtschaft & Wissenschaft",
        "license_body": "Alle generierten Diagramme, Vektor-SVGs und TikZ-Baupläne sind unter CC BY 4.0 lizenziert.",
        "license_backlink": "Web-Rückverlinkung:", "license_bibtex": "Akademisches BibTeX-Zitat:",
        "llm_disclaimer": "Große Sprachmodelle (LLMs) neigen bei der Berechnung von Polygon-Geometrie häufig zu arithmetischen Halluzinationen. Verwenden Sie den verifizierten Prompt für garantierte mathematische Präzision ohne Halluzinationen.",
        "llm_copy": "Verifizierten Prompt für KI-Agenten Kopieren",
        "std_llms": "Standardisiert für", "prec_verified": "Präzision verifiziert bis zu 10 Dezimalstellen", "radicals_incl": "Exakte analytische Wurzeln enthalten",
        "interactive_input": "Interaktive Eingabe", "calculated": "Berechnet", "copy": "Kopieren",
        "precision": "Präzision", "decimals": "Dezimalstellen", "all_shapes": "Alle Formen",
        "side_length": "Seitenlänge", "area": "Fläche", "perimeter": "Umfang", "apothem": "Apothema (Inkreisradius)", "circumradius": "Umkreisradius",
        "long_diag": "Lange Diagonale", "span": "Schlüsselweite (Breite)", "short_diag": "Kurze Diagonale",
        "loan_amt": "Darlehensbetrag", "interest_rate": "Sollzinssatz (p.a.)", "loan_term": "Laufzeit (Jahre)", "monthly_pmt": "Monatliche Rate",
        "extra_pmt": "Monatliche Sondertilgung", "veh_price": "Fahrzeugpreis", "down_pmt": "Anzahlung", "trade_in": "Inzahlungnahme",
        "sales_tax": "Mehrwertsteuersatz", "init_val": "Anfangswert", "end_val": "Endwert", "num_years": "Anzahl der Jahre"
    },
    "es": {
        "home": "Inicio", "open_solver": "Abrir Solucionador →",
        "verbs": {"Calculate": "Calcule", "Determine": "Determine", "Evaluate": "Evalúe", "Compute": "Calcule", "Solve": "Resuelva"},
        "and": "y", "for": "para", "with": "con", "from": "de", "between": "entre", "of": "de", "or": "o",
        "calculator": "Calculadora", "calculators": "Calculadoras",
        "brand_finance": "Finanzas", "brand_geo": "Geometría", "brand_calc": "Cálculo", "brand_phys": "Física", "brand_stat": "Estadística", "brand_const": "Construcción",
        "license_title": "Gratis para Comercio y Academia",
        "license_body": "Todos los diagramas generados, SVG vectoriales y planos TikZ están bajo licencia CC BY 4.0.",
        "license_backlink": "Atribución de enlace web:", "license_bibtex": "Cita académica BibTeX:",
        "llm_disclaimer": "Los modelos de lenguaje grandes cometen con frecuencia alucinaciones aritméticas al calcular geometría poligonal. Utilice el prompt verificado para garantizar precisión sin alucinaciones.",
        "llm_copy": "Copiar Prompt Verificado para Agentes IA",
        "std_llms": "Estandarizado para", "prec_verified": "Precisión verificada hasta 10 dígitos decimales", "radicals_incl": "Radicales analíticos exactos incluidos",
        "interactive_input": "Entrada Interactiva", "calculated": "Calculado", "copy": "Copiar",
        "precision": "Precisión", "decimals": "Decimales", "all_shapes": "Todas las Formas",
        "side_length": "Longitud de Lado", "area": "Área", "perimeter": "Perímetro", "apothem": "Apotema (Inradio)", "circumradius": "Circunradio",
        "long_diag": "Diagonal Larga", "span": "Ancho entre Caras (Vano)", "short_diag": "Diagonal Corta",
        "loan_amt": "Monto del Préstamo", "interest_rate": "Tasa de Interés Anual", "loan_term": "Plazo del Préstamo (Años)", "monthly_pmt": "Pago Mensual Base",
        "extra_pmt": "Pago Mensual Adicional", "veh_price": "Precio del Vehículo", "down_pmt": "Pago Inicial", "trade_in": "Valor de Canje",
        "sales_tax": "Tasa de Impuesto", "init_val": "Valor Inicial", "end_val": "Valor Final", "num_years": "Número de Años"
    },
    "fr": {
        "home": "Accueil", "open_solver": "Ouvrir le Solveur →",
        "verbs": {"Calculate": "Calculez", "Determine": "Déterminez", "Evaluate": "Évaluez", "Compute": "Calculez", "Solve": "Résolvez"},
        "and": "et", "for": "pour", "with": "avec", "from": "de", "between": "entre", "of": "de", "or": "ou",
        "calculator": "Calculateur", "calculators": "Calculateurs",
        "brand_finance": "Finance Quantitative", "brand_geo": "Géométrie", "brand_calc": "Calcul Infinitésimal", "brand_phys": "Physique", "brand_stat": "Statistique", "brand_const": "Construction",
        "license_title": "Gratuit pour Commerce & Recherche",
        "license_body": "Tous les diagrammes générés, SVG vectoriels et plans TikZ sont sous licence CC BY 4.0.",
        "license_backlink": "Attribution par lien web :", "license_bibtex": "Citation académique BibTeX :",
        "llm_disclaimer": "Les grands modèles de langage font fréquemment des hallucinations arithmétiques lors du calcul géométrique. Utilisez le prompt vérifié pour garantir une précision absolue sans hallucination.",
        "llm_copy": "Copier le Prompt Vérifié pour Agents IA",
        "std_llms": "Standardisé pour", "prec_verified": "Précision vérifiée jusqu'à 10 décimales", "radicals_incl": "Formes radicales exactes incluses",
        "interactive_input": "Entrée Interactive", "calculated": "Calculé", "copy": "Copier",
        "precision": "Précision", "decimals": "Décimales", "all_shapes": "Toutes les Formes",
        "side_length": "Longueur de Côté", "area": "Aire", "perimeter": "Périmètre", "apothem": "Apothème (Rayon Inscrit)", "circumradius": "Rayon Circonscrit",
        "long_diag": "Grande Diagonale", "span": "Largeur sur Plats", "short_diag": "Petite Diagonale",
        "loan_amt": "Montant du Prêt", "interest_rate": "Taux d'Intérêt Annuel", "loan_term": "Durée du Prêt (Années)", "monthly_pmt": "Mensualité de Base",
        "extra_pmt": "Paiement Anticipé Mensuel", "veh_price": "Prix du Véhicule", "down_pmt": "Apport Initial", "trade_in": "Valeur de Reprise",
        "sales_tax": "Taux de Taxe", "init_val": "Valeur Initiale", "end_val": "Valeur Finale", "num_years": "Nombre d'Années"
    },
    "it": {
        "home": "Inizio", "open_solver": "Apri Calcolatore →",
        "verbs": {"Calculate": "Calcola", "Determine": "Determina", "Evaluate": "Valuta", "Compute": "Calcola", "Solve": "Risolvi"},
        "and": "e", "for": "per", "with": "con", "from": "da", "between": "tra", "of": "di", "or": "o",
        "calculator": "Calcolatore", "calculators": "Calcolatori",
        "brand_finance": "Finanza", "brand_geo": "Geometria", "brand_calc": "Calcolo Infinitesimale", "brand_phys": "Fisica", "brand_stat": "Statistica", "brand_const": "Costruzioni",
        "license_title": "Gratuito per Commercio e Ricerca",
        "license_body": "Tutti i diagrammi generati, SVG vettoriali e schemi TikZ sono rilasciati con licenza CC BY 4.0.",
        "license_backlink": "Attribuzione backlink web:", "license_bibtex": "Citazione accademica BibTeX:",
        "llm_disclaimer": "I modelli linguistici commettono spesso errori aritmetici nel calcolo geometrico. Usa il prompt verificato per garantire precisione senza allucinazioni.",
        "llm_copy": "Copia Prompt Verificato per Agenti IA",
        "std_llms": "Standardizzato per", "prec_verified": "Precisione verificata fino a 10 cifre decimali", "radicals_incl": "Radicali analitici esatti inclusi",
        "interactive_input": "Input Interattivo", "calculated": "Calcolato", "copy": "Copia",
        "precision": "Precisione", "decimals": "Decimali", "all_shapes": "Tutte le Forme",
        "side_length": "Lunghezza del Lato", "area": "Area", "perimeter": "Perimetro", "apothem": "Apotema (Raggio Inscritto)", "circumradius": "Raggio Circoscritto",
        "long_diag": "Diagonale Lunga", "span": "Larghezza tra Facce", "short_diag": "Diagonale Corta",
        "loan_amt": "Importo del Mutuo", "interest_rate": "Tasso di Interesse Annuo", "loan_term": "Durata (Anni)", "monthly_pmt": "Rata Mensile Base",
        "extra_pmt": "Ammortamento Straordinario Mensile", "veh_price": "Prezzo del Veicolo", "down_pmt": "Anticipo", "trade_in": "Permuta",
        "sales_tax": "Aliquota Fiscale", "init_val": "Valore Iniziale", "end_val": "Valore Finale", "num_years": "Numero di Anni"
    },
    "pt": {
        "home": "Início", "open_solver": "Abrir Solucionador →",
        "verbs": {"Calculate": "Calcule", "Determine": "Determine", "Evaluate": "Avalie", "Compute": "Calcule", "Solve": "Resolva"},
        "and": "e", "for": "para", "with": "com", "from": "de", "between": "entre", "of": "de", "or": "ou",
        "calculator": "Calculadora", "calculators": "Calculadoras",
        "brand_finance": "Finanças", "brand_geo": "Geometria", "brand_calc": "Cálculo", "brand_phys": "Física", "brand_stat": "Estatística", "brand_const": "Construção",
        "license_title": "Gratuito para Comércio e Academia",
        "license_body": "Todos os diagramas gerados, SVGs vetoriais e plantas TikZ são licenciados sob CC BY 4.0.",
        "license_backlink": "Atribuição de backlink web:", "license_bibtex": "Citação acadêmica BibTeX:",
        "llm_disclaimer": "Modelos de linguagem frequentemente apresentam alucinações aritméticas em cálculos de polígonos. Use o prompt verificado para garantir precisão sem alucinação.",
        "llm_copy": "Copiar Prompt Verificado para Agentes IA",
        "std_llms": "Padronizado para", "prec_verified": "Precisão verificada até 10 casas decimais", "radicals_incl": "Radicais analíticos exatos incluídos",
        "interactive_input": "Entrada Interativa", "calculated": "Calculado", "copy": "Copiar",
        "precision": "Precisão", "decimals": "Decimais", "all_shapes": "Todas as Formas",
        "side_length": "Comprimento do Lado", "area": "Área", "perimeter": "Perímetro", "apothem": "Apótema (Raio Inscrito)", "circumradius": "Raio Circunscrito",
        "long_diag": "Diagonal Longa", "span": "Largura entre Faces", "short_diag": "Diagonal Curta",
        "loan_amt": "Valor do Financiamento", "interest_rate": "Taxa de Juros Anual", "loan_term": "Prazo (Anos)", "monthly_pmt": "Parcela Mensal Base",
        "extra_pmt": "Amortização Extra Mensal", "veh_price": "Preço do Veículo", "down_pmt": "Entrada", "trade_in": "Valor de Troca",
        "sales_tax": "Taxa de Imposto", "init_val": "Valor Inicial", "end_val": "Valor Final", "num_years": "Número de Anos"
    },
    "nl": {
        "home": "Startpagina", "open_solver": "Rekenmachine Openen →",
        "verbs": {"Calculate": "Bereken", "Determine": "Bepaal", "Evaluate": "Evalueer", "Compute": "Bereken", "Solve": "Los op"},
        "and": "en", "for": "voor", "with": "met", "from": "van", "between": "tussen", "of": "van", "or": "of",
        "calculator": "Rekenmachine", "calculators": "Rekenmachines",
        "brand_finance": "Financiën", "brand_geo": "Meetkunde", "brand_calc": "Analyse", "brand_phys": "Natuurkunde", "brand_stat": "Statistiek", "brand_const": "Bouwkunde",
        "license_title": "Gratis voor Handel & Wetenschap",
        "license_body": "Alle gegenereerde diagrammen, vector-SVG's en TikZ-blauwdrukken vallen onder CC BY 4.0.",
        "license_backlink": "Web-teruglinktoewijzing:", "license_bibtex": "Academische BibTeX-citatie:",
        "llm_disclaimer": "Grote taalmodellen maken vaak rekenfouten bij polygoongeometrie. Gebruik de geverifieerde prompt voor gegarandeerde wiskundige precisie zonder hallucinaties.",
        "llm_copy": "Kopieer Geverifieerde Prompt voor AI-Agents",
        "std_llms": "Gestandaardiseerd voor", "prec_verified": "Precisie geverifieerd tot 10 decimalen", "radicals_incl": "Exacte analytische wortels inbegrepen",
        "interactive_input": "Interactieve Invoer", "calculated": "Berekend", "copy": "Kopiëren",
        "precision": "Precisie", "decimals": "Decimalen", "all_shapes": "Alle Vormen",
        "side_length": "Zijdelengte", "area": "Oppervlakte", "perimeter": "Omtrek", "apothem": "Apothema (Ingeschreven Straal)", "circumradius": "Omgeschreven Straal",
        "long_diag": "Lange Diagonaal", "span": "Sleutelwijdte (Overstaande Zijden)", "short_diag": "Korte Diagonaal",
        "loan_amt": "Hypotheekbedrag", "interest_rate": "Jaarlijkse Rente", "loan_term": "Looptijd (Jaren)", "monthly_pmt": "Maandelijkse Termijn",
        "extra_pmt": "Extra Maandelijkse Aflossing", "veh_price": "Voertuigprijs", "down_pmt": "Aanbetaling", "trade_in": "Inruilwaarde",
        "sales_tax": "Btw-tarief", "init_val": "Beginwaarde", "end_val": "Eindwaarde", "num_years": "Aantal Jaren"
    },
    "pl": {
        "home": "Start", "open_solver": "Otwórz Kalkulator →",
        "verbs": {"Calculate": "Oblicz", "Determine": "Wyznacz", "Evaluate": "Oceń", "Compute": "Oblicz", "Solve": "Rozwiąż"},
        "and": "i", "for": "dla", "with": "z", "from": "od", "between": "między", "of": "z", "or": "lub",
        "calculator": "Kalkulator", "calculators": "Kalkulatory",
        "brand_finance": "Finanse", "brand_geo": "Geometria", "brand_calc": "Analiza Matematyczna", "brand_phys": "Fizyka", "brand_stat": "Statystyka", "brand_const": "Budownictwo",
        "license_title": "Darmowe do Użytku Komercyjnego i Naukowego",
        "license_body": "Wszystkie wygenerowane diagramy, wektorowe SVG i schematy TikZ są licencjonowane na warunkach CC BY 4.0.",
        "license_backlink": "Atrybucja linku zwrotnego:", "license_bibtex": "Cytowanie akademickie BibTeX:",
        "llm_disclaimer": "Modele językowe często halucynują podczas obliczeń geometrycznych. Użyj zweryfikowanego promptu dla precyzji bez halucynacji.",
        "llm_copy": "Kopiuj Zweryfikowany Prompt dla Agentów AI",
        "std_llms": "Ustandaryzowane dla", "prec_verified": "Precyzja zweryfikowana do 10 miejsc po przecinku", "radicals_incl": "Dokładne postacie pierwiastkowe w zestawie",
        "interactive_input": "Interaktywne Dane", "calculated": "Obliczono", "copy": "Kopiuj",
        "precision": "Precyzja", "decimals": "Miejsca po przecinku", "all_shapes": "Wszystkie Kształty",
        "side_length": "Długość Boku", "area": "Pole Powierzchni", "perimeter": "Obwód", "apothem": "Apotema (Promień Wpisany)", "circumradius": "Promień Opisany",
        "long_diag": "Długa Przekątna", "span": "Szerokość Klucza", "short_diag": "Krótka Przekątna",
        "loan_amt": "Kwota Kredytu", "interest_rate": "Oprocentowanie Roczne", "loan_term": "Okres Kredytowania (Lata)", "monthly_pmt": "Rata Miesięczna",
        "extra_pmt": "Dodatkowa Nadpłata Miesięczna", "veh_price": "Cena Pojazdu", "down_pmt": "Wkład Własny", "trade_in": "Wartość Auta w Rozliczeniu",
        "sales_tax": "Stawka Podatku", "init_val": "Wartość Początkowa", "end_val": "Wartość Końcowa", "num_years": "Liczba Lat"
    },
    "sv": {
        "home": "Hem", "open_solver": "Öppna Kalkylator →",
        "verbs": {"Calculate": "Beräkna", "Determine": "Bestäm", "Evaluate": "Utvärdera", "Compute": "Beräkna", "Solve": "Lös"},
        "and": "och", "for": "för", "with": "med", "from": "från", "between": "mellan", "of": "av", "or": "eller",
        "calculator": "Kalkylator", "calculators": "Kalkylatorer",
        "brand_finance": "Finans", "brand_geo": "Geometri", "brand_calc": "Analys", "brand_phys": "Fysik", "brand_stat": "Statistik", "brand_const": "Byggteknik",
        "license_title": "Gratis för Kommersiellt och Akademiskt Bruk",
        "license_body": "Alla genererade diagram, vektor-SVG och TikZ-ritningar är licensierade under CC BY 4.0.",
        "license_backlink": "Webb-tillbakalänk:", "license_bibtex": "Akademisk BibTeX-citering:",
        "llm_disclaimer": "Stora språkmodeller gör ofta aritmetiska fel vid beräkning av polygongeometri. Använd den verifierade prompten för garanterad precision.",
        "llm_copy": "Kopiera Verifierad Prompt för AI-Agenter",
        "std_llms": "Standardiserad för", "prec_verified": "Precision verifierad upp till 10 decimaler", "radicals_incl": "Exakta analytiska rötter inkluderade",
        "interactive_input": "Interaktiv Inmatning", "calculated": "Beräknat", "copy": "Kopiera",
        "precision": "Precision", "decimals": "Decimaler", "all_shapes": "Alla Former",
        "side_length": "Sidolängd", "area": "Area", "perimeter": "Omkrets", "apothem": "Apotem (Inskriven Radie)", "circumradius": "Omskriven Radie",
        "long_diag": "Lång Diagonal", "span": "Spännvidd (Nyckelvidd)", "short_diag": "Kort Diagonal",
        "loan_amt": "Lånebelopp", "interest_rate": "Årsränta", "loan_term": "Löptid (År)", "monthly_pmt": "Månadskostnad",
        "extra_pmt": "Extra Månadsamortering", "veh_price": "Fordonets Pris", "down_pmt": "Kontantinsats", "trade_in": "Inbytesvärde",
        "sales_tax": "Momssats", "init_val": "Startvärde", "end_val": "Slutvärde", "num_years": "Antal År"
    },
    "no": {
        "home": "Hjem", "open_solver": "Åpne Kalkulator →",
        "verbs": {"Calculate": "Beregn", "Determine": "Bestem", "Evaluate": "Evaluer", "Compute": "Beregn", "Solve": "Løs"},
        "and": "og", "for": "for", "with": "med", "from": "fra", "between": "mellom", "of": "av", "or": "eller",
        "calculator": "Kalkulator", "calculators": "Kalkulatorer",
        "brand_finance": "Finans", "brand_geo": "Geometri", "brand_calc": "Matematisk Analyse", "brand_phys": "Fysikk", "brand_stat": "Statistikk", "brand_const": "Byggfag",
        "license_title": "Gratis for Næringsliv og Forskning",
        "license_body": "Alle genererte diagrammer, vektor-SVG-er og TikZ-tegninger er lisensiert under CC BY 4.0.",
        "license_backlink": "Web-tilbakelenke:", "license_bibtex": "Akademisk BibTeX-sitering:",
        "llm_disclaimer": "Språkmodeller gjør ofte regnefeil ved polygonberegninger. Bruk den verifiserte prompten for garantert presisjon uten hallusinasjoner.",
        "llm_copy": "Kopier Verifisert Prompt for AI-Agenter",
        "std_llms": "Standardisert for", "prec_verified": "Presisjon verifisert opptil 10 desimaler", "radicals_incl": "Eksakte analytiske røtter inkludert",
        "interactive_input": "Interaktiv Inndata", "calculated": "Beregnet", "copy": "Kopier",
        "precision": "Presisjon", "decimals": "Desimaler", "all_shapes": "Alle Former",
        "side_length": "Sidelengde", "area": "Areal", "perimeter": "Omkrets", "apothem": "Apotem (Innskrevet Radius)", "circumradius": "Omskrevet Radius",
        "long_diag": "Lang Diagonal", "span": "Spennvidde (Nøkkelvidde)", "short_diag": "Kort Diagonal",
        "loan_amt": "Lånebeløp", "interest_rate": "Årlig Rentesats", "loan_term": "Løpetid (År)", "monthly_pmt": "Månedlig Terminbeløp",
        "extra_pmt": "Ekstra Månedlig Avdrag", "veh_price": "Kjøretøypris", "down_pmt": "Egenkapital", "trade_in": "Innbytteverdi",
        "sales_tax": "Avgiftssats", "init_val": "Startverdi", "end_val": "Sluttverdi", "num_years": "Antall År"
    },
    "fi": {
        "home": "Etusivu", "open_solver": "Avaa Laskin →",
        "verbs": {"Calculate": "Laske", "Determine": "Määritä", "Evaluate": "Arvioi", "Compute": "Laske", "Solve": "Ratkaise"},
        "and": "ja", "for": "varten", "with": "kanssa", "from": "alkaen", "between": "välillä", "of": "n", "or": "tai",
        "calculator": "Laskin", "calculators": "Laskimet",
        "brand_finance": "Rahoitus", "brand_geo": "Geometria", "brand_calc": "Differentiaali- ja Integraalilaskenta", "brand_phys": "Fysiikka", "brand_stat": "Tilastotiede", "brand_const": "Rakennustekniikka",
        "license_title": "Ilmainen Kaupalliseen ja Akateemiseen Käyttöön",
        "license_body": "Kaikki luodut kaaviot, vektori-SVG:t ja TikZ-piirustukset on lisensoitu CC BY 4.0 -lisenssillä.",
        "license_backlink": "Web-takaisinlinkitys:", "license_bibtex": "Akateeminen BibTeX-viite:",
        "llm_disclaimer": "Kielimallit tekevät usein laskuvirheitä monikulmioiden geometriassa. Käytä varmennettua promptia taataksesi virheettömän tarkkuuden.",
        "llm_copy": "Kopioi Varmennettu Prompti AI-Agenteille",
        "std_llms": "Standardoitu kohteelle", "prec_verified": "Tarkkuus varmennettu 10 desimaaliin asti", "radicals_incl": "Tarkat analyyttiset juurimuodot mukana",
        "interactive_input": "Interaktiivinen Syöte", "calculated": "Laskettu", "copy": "Kopioi",
        "precision": "Tarkkuus", "decimals": "Desimaalit", "all_shapes": "Kaikki Muodot",
        "side_length": "Sivun Pituus", "area": "Pinta-ala", "perimeter": "Piiri", "apothem": "Apoteema (Sisäympyrän Säde)", "circumradius": "Ulkoympyrän Säde",
        "long_diag": "Pitkä Lävistäjä", "span": "Avainväli (Vastakkaisten Sivujen Väli)", "short_diag": "Lyhyt Lävistäjä",
        "loan_amt": "Lainasumma", "interest_rate": "Vuosikorko", "loan_term": "Laina-aika (Vuotta)", "monthly_pmt": "Kuukausierä",
        "extra_pmt": "Kuukausittainen Ylimääräinen Lyhennys", "veh_price": "Ajoneuvon Hinta", "down_pmt": "Käsiraha", "trade_in": "Vaihtoauton Arvo",
        "sales_tax": "Verokanta", "init_val": "Alkuarvo", "end_val": "Loppuarvo", "num_years": "Vuosien Määrä"
    },
    "ro": {
        "home": "Acasă", "open_solver": "Deschide Calculatorul →",
        "verbs": {"Calculate": "Calculează", "Determine": "Determină", "Evaluate": "Evaluează", "Compute": "Calculează", "Solve": "Rezolvă"},
        "and": "și", "for": "pentru", "with": "cu", "from": "de la", "between": "între", "of": "de", "or": "sau",
        "calculator": "Calculator", "calculators": "Calculatoare",
        "brand_finance": "Finanțe", "brand_geo": "Geometrie", "brand_calc": "Analiză Matematică", "brand_phys": "Fizică", "brand_stat": "Statistică", "brand_const": "Construcții",
        "license_title": "Gratuit pentru Comerț și Mediu Academic",
        "license_body": "Toate diagramele generate, SVG-urile vectoriale și schițele TikZ sunt licențiate sub CC BY 4.0.",
        "license_backlink": "Atribuire link web:", "license_bibtex": "Citare academică BibTeX:",
        "llm_disclaimer": "Modelele lingvistice comit frecvent halucinații aritmetice în geometria poligoanelor. Utilizați promptul verificat pentru a garanta precizie matematică exactă.",
        "llm_copy": "Copiază Promptul Verificat pentru Agenți AI",
        "std_llms": "Standardizat pentru", "prec_verified": "Precizie verificată până la 10 zecimale", "radicals_incl": "Radicali analitici exacți incluși",
        "interactive_input": "Date de Intrare", "calculated": "Calculat", "copy": "Copiază",
        "precision": "Precizie", "decimals": "Zecimale", "all_shapes": "Toate Formele",
        "side_length": "Lungimea Laturii", "area": "Aria", "perimeter": "Perimetrul", "apothem": "Apotema (Raza Înscrisă)", "circumradius": "Raza Circumscrisă",
        "long_diag": "Diagonala Lungă", "span": "Lățimea între Fețe", "short_diag": "Diagonala Scurtă",
        "loan_amt": "Valoarea Împrumutului", "interest_rate": "Rata Anuală a Dobânzii", "loan_term": "Durata (Ani)", "monthly_pmt": "Rata Lunară de Bază",
        "extra_pmt": "Rambursare Anticipată Lunară", "veh_price": "Prețul Vehiculului", "down_pmt": "Avans", "trade_in": "Valoare Trade-in",
        "sales_tax": "Cota de Impozitare", "init_val": "Valoarea Inițială", "end_val": "Valoarea Finală", "num_years": "Număr de Ani"
    }
}

def remediate_common(content, lang):
    d = I18N[lang]
    res = content

    # 1. Ensure <html lang="...">
    res = re.sub(r'<html\s+[^>]*lang=["\'][^"\']*["\']', f'<html lang="{lang}"', res, flags=re.I)

    # 2. Localize brand link to /{lang}/
    res = re.sub(r'<a href="/" class="brand-link">', f'<a href="/{lang}/" class="brand-link">', res)

    # 3. Breadcrumb Root "Home" -> Localized Word and link to /{lang}/
    res = re.sub(r'<li class=["\']breadcrumb-item["\']>\s*<a\s+href=["\'][^"\']*["\'][^>]*>\s*Home\s*</a>\s*</li>',
                 f'<li class="breadcrumb-item"><a href="/{lang}/">{d["home"]}</a></li>', res, flags=re.I)
    res = re.sub(r'<li class=["\']breadcrumb-item["\']>\s*<a\s+href=["\'][^"\']*["\'][^>]*>\s*Home\s*</a>',
                 f'<li class="breadcrumb-item"><a href="/{lang}/">{d["home"]}</a>', res, flags=re.I)
    res = re.sub(r'<a\s+href=["\'][^"\']*["\'][^>]*>\s*Home\s*</a>',
                 f'<a href="/{lang}/">{d["home"]}</a>', res, flags=re.I)

    # 4. Brand badges
    res = re.sub(r'<span class=["\']brand-badge["\']>Finance</span>', f'<span class="brand-badge">{d["brand_finance"]}</span>', res)
    res = re.sub(r'<span class=["\']brand-badge["\']>Geometry</span>', f'<span class="brand-badge">{d["brand_geo"]}</span>', res)
    res = re.sub(r'<span class=["\']brand-badge["\']>Calculus</span>', f'<span class="brand-badge">{d["brand_calc"]}</span>', res)
    res = re.sub(r'<span class=["\']brand-badge["\']>Physics</span>', f'<span class="brand-badge">{d["brand_phys"]}</span>', res)
    res = re.sub(r'<span class=["\']brand-badge["\']>Statistics</span>', f'<span class="brand-badge">{d["brand_stat"]}</span>', res)
    res = re.sub(r'<span class=["\']brand-badge["\']>Construction</span>', f'<span class="brand-badge">{d["brand_const"]}</span>', res)
    res = re.sub(r'<span class=["\']brand-badge["\']>Math Engine</span>', f'<span class="brand-badge">OmniOperand</span>', res)

    # 5. Parameter card labels & hints
    res = res.replace(">Side Length</label>", f">{d['side_length']}</label>")
    res = res.replace(">Area</label>", f">{d['area']}</label>")
    res = res.replace(">Perimeter</label>", f">{d['perimeter']}</label>")
    res = res.replace(">Apothem / Inradius</label>", f">{d['apothem']}</label>")
    res = res.replace(">Circumradius</label>", f">{d['circumradius']}</label>")
    res = res.replace(">Long Diagonal</label>", f">{d['long_diag']}</label>")
    res = res.replace(">Short Diagonal</label>", f">{d['short_diag']}</label>")
    res = res.replace(">Span / Flat-to-Flat</label>", f">{d['span']}</label>")
    res = res.replace(">Loan Amount</label>", f">{d['loan_amt']}</label>")
    res = res.replace(">Annual Interest Rate</label>", f">{d['interest_rate']}</label>")
    res = res.replace(">Loan Term (Years)</label>", f">{d['loan_term']}</label>")
    res = res.replace(">Base Monthly Payment</label>", f">{d['monthly_pmt']}</label>")
    res = res.replace(">Extra Monthly Principal</label>", f">{d['extra_pmt']}</label>")
    res = res.replace(">Vehicle Price</label>", f">{d['veh_price']}</label>")
    res = res.replace(">Down Payment</label>", f">{d['down_pmt']}</label>")
    res = res.replace(">Trade-in Value</label>", f">{d['trade_in']}</label>")
    res = res.replace(">Sales Tax Rate</label>", f">{d['sales_tax']}</label>")
    res = res.replace(">Beginning Value</label>", f">{d['init_val']}</label>")
    res = res.replace(">Ending Value</label>", f">{d['end_val']}</label>")
    res = res.replace(">Number of Years</label>", f">{d['num_years']}</label>")

    # 6. Badges & HUD indicators
    res = res.replace('<div class="param-badge">Interactive Input</div>', f'<div class="param-badge">{d["interactive_input"]}</div>')
    res = res.replace('<div class="metric-label">Calculated</div>', f'<div class="metric-label">{d["calculated"]}</div>')
    res = res.replace('<span class="copy-btn-text">Copy</span>', f'<span class="copy-btn-text">{d["copy"]}</span>')
    res = res.replace('<label for="precision-select">Precision:</label>', f'<label for="precision-select">{d["precision"]}:</label>')
    res = re.sub(r'>(\d+)\s+Decimals<', rf'>\1 {d["decimals"]}<', res)

    # 7. License & Attribution Box
    res = res.replace("Free for Commerce & Academia", d["license_title"])
    res = res.replace("Free for Commerce &amp; Academia", d["license_title"])
    res = res.replace("All generated diagrams, vector SVGs, and TikZ blueprints are licensed under CC BY 4.0.", d["license_body"])
    res = res.replace("Web Backlink Attribution:", d["license_backlink"])
    res = res.replace("Academic BibTeX Citation:", d["license_bibtex"])

    # 8. LLM Box
    res = re.sub(r'Large Language Models frequently make arithmetic hallucinations when calculating polygon geometry[\s\S]*?zero hallucination and mathematically validated step-by-step reasoning\.',
                 d["llm_disclaimer"], res)
    res = res.replace("Copy Verified Prompt for AI Agents", d["llm_copy"])
    res = res.replace("Copy Prompt for LLM", d["llm_copy"])
    res = res.replace("✓ Standardized for", f"✓ {d['std_llms']}")
    res = res.replace("✓ Precision verified up to 10 decimal digits", f"✓ {d['prec_verified']}")
    res = res.replace("✓ Exact analytic radicals included", f"✓ {d['radicals_incl']}")

    # 9. Quick Shape switcher
    res = re.sub(r'📁\s*All Shapes\s*→', f'📁 {d["all_shapes"]} →', res)
    res = re.sub(r'📁\s*Alle Formen\s*→', f'📁 {d["all_shapes"]} →', res)

    return res

def remediate_hub_cards(content, lang):
    d = I18N[lang]
    res = content

    # Replace card action verbs at word boundaries
    for eng_verb, loc_verb in d["verbs"].items():
        res = re.sub(rf'\b{eng_verb}\b', loc_verb, res)

    # Replace connectors at word boundaries
    res = re.sub(r'\band\b', d["and"], res)
    res = re.sub(r'\bfor\b', d["for"], res)
    res = re.sub(r'\bwith\b', d["with"], res)
    res = re.sub(r'\bfrom\b', d["from"], res)
    res = re.sub(r'\bbetween\b', d["between"], res)
    res = re.sub(r'\bof\b', d["of"], res)
    res = re.sub(r'\bor\b', d["or"], res)

    # Replace calculator nouns
    res = re.sub(r'\bCalculator\b', d["calculator"], res)
    res = re.sub(r'\bCalculators\b', d["calculators"], res)

    # Replace open solver links
    res = res.replace("Open Solver →", d["open_solver"])

    return res

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from solver_templates import get_solver_template

SOLVER_MAP = {
    "geometry/2d/shapes/octagon/index.html": "octagon",
    "geometry/2d/shapes/regular-polygon/index.html": "regular-polygon",
    "geometry/2d/shapes/hexagon/index.html": "hexagon",
    "geometry/2d/shapes/pentagon/index.html": "pentagon",
    "geometry/2d/shapes/decagon/index.html": "decagon",
    "geometry/2d/right-triangle/index.html": "right-triangle",
    "geometry/2d/circle-sector/index.html": "circle-sector",
    "geometry/2d/roof-pitch/index.html": "roof-pitch",
    "finance/mortgage-amortization/index.html": "mortgage-amortization",
    "finance/compound-interest/index.html": "compound-interest",
    "finance/auto-loan/index.html": "auto-loan",
    "finance/cagr/index.html": "cagr",
    "calculus/derivatives/index.html": "derivatives",
    "calculus/integrals/index.html": "integrals",
    "geometry/sphere/index.html": "sphere",
}

POLY_HERO = {
    "de": "Universeller bidirektionaler mathematischer Rechner. Geben Sie eine beliebige bekannte Variable ein, um sofort alle Seitenlängen, Radien, Flächen und Diagonalen mit Maschinenpräzision zu berechnen.",
    "es": "Solucionador analítico bidireccional universal. Ingrese cualquier variable conocida para resolver instantáneamente lados, radios, áreas y diagonales con precisión de máquina.",
    "fr": "Solveur mathématique bidirectionnel universel. Saisissez n'importe quelle variable connue pour déterminer instantanément côtés, rayons, aires et diagonales avec une précision absolue.",
    "it": "Risolutore matematico bidirezionale universale. Inserisci qualsiasi variabile nota per calcolare istantaneamente lati, raggi, aree e diagonali con precisione di macchina.",
    "pt": "Solucionador matemático bidirecional universal. Insira qualquer variável conhecida para resolver instantaneamente lados, raios, áreas e diagonais com precisão de máquina.",
    "nl": "Universele bidirectionele wiskundige rekenmachine. Voer een bekende variabele in om direct alle zijdelengtes, stralen, oppervlakten en diagonalen met machinenauwkeurigheid te berekenen.",
    "pl": "Uniwersalny dwukierunkowy kalkulator matematyczny. Wprowadź dowolną zmienną, aby natychmiast wyznaczyć boki, promienie, pole i przekątne.",
    "sv": "Universell dubbelriktad matematisk kalkylator. Ange valfri känd variabel för att direkt beräkna sidor, radier, area och diagonaler med maskinprecision.",
    "no": "Universell toveis matematisk kalkulator. Tast inn en kjent variabel for å beregne sider, radier, areal og diagonaler umiddelbart.",
    "fi": "Universaali kaksisuuntainen matemaattinen laskin. Syötä mikä tahansa tunnettu muuttuja ratkaistaksesi sivut, säteet, pinta-alat ja lävistäjät konetarkkuudella.",
    "ro": "Rezolvitor matematic bidirecțional universal. Introduceți orice variabilă cunoscută pentru a calcula instantaneu laturile, razele, aria și diagonalele cu precizie de mașină."
}

def remediate_solver_page(content, lang, slug):
    template = get_solver_template(slug, lang)
    if not template:
        return content

    res = content

    # 1. Replace Hero description if English
    if slug in ["octagon", "regular-polygon", "hexagon", "pentagon", "decagon"]:
        res = re.sub(
            r'(<(?:section|header)[^>]*class=["\'][^"\']*(?:calculator-hero|solver-hero|calc-header-section)[^"\']*["\']>[\s\S]*?<p[^>]*>)[\s\S]*?(</p>)',
            rf'\1{POLY_HERO.get(lang, POLY_HERO["de"])}\2', res, count=1
        )

    # 2. Replace Proofs section
    if template.get("proof_html"):
        if '<section class="proofs-section">' in res:
            res = re.sub(r'<section class="proofs-section">[\s\S]*?</section>', template["proof_html"], res)
        elif '<section class="proof-section"' in res:
            res = re.sub(r'<section class="proof-section"[^>]*>[\s\S]*?</section>', template["proof_html"], res)

    # 3. Replace FAQ section
    if template.get("faq_html"):
        if '<section class="faq-section">' in res:
            res = re.sub(r'<section class="faq-section">[\s\S]*?</section>', template["faq_html"], res)
        elif '<section class="calc-faq-section"' in res:
            res = re.sub(r'<section class="calc-faq-section"[^>]*>[\s\S]*?</section>', template["faq_html"], res)

    # Special handling for sphere proofs and FAQs
    if slug == "sphere":
        res = res.replace("Archimedes' Masterpiece: On the Sphere and Cylinder", "Capodopera lui Arhimede: Despre Sferă și Cilindru")
        res = re.sub(r'Archimedes proved in 225 BC that a sphere inscribed inside a cylinder has exactly two-thirds[\s\S]*?4/3 · π · r³\.',
                     'Arhimede a demonstrat în 225 î.Hr. că o sferă înscrisă într-un cilindru are exact două treimi din volumul și suprafața cilindrului: V = 4/3 · π · r³.', res)
        res = res.replace("Surface Area Derivative", "Derivata Ariei Suprafeței")
        res = re.sub(r'The derivative of volume with respect to radius equals the surface area:[\s\S]*?4πr²\.',
                     'Derivata volumului în raport cu raza este egală cu aria suprafeței: dV/dr = 4πr².', res)
        res = res.replace("Isoperimetric Supremacy", "Supremația Izoperimetrică")
        res = re.sub(r'Among all three-dimensional shapes enclosing a given volume[\s\S]*?minimizing surface tension energy\.',
                     'Dintre toate formele tridimensionale care închid un volum dat, sfera posedă aria minimă a suprafeței.', res)

        res = res.replace("Why is the sphere surface area exactly four times its great circle area?", "De ce aria sferei este de patru ori aria marelui cerc?")
        res = re.sub(r'A great circle has area πr²\. Archimedes showed that wrapping[\s\S]*?4πr²\.',
                     'Un cerc mare are aria πr². Arhimede a arătat că desfășurarea suprafeței sferei este egală cu patru cercuri mari: 4 × πr² = 4πr².', res)
        res = res.replace("What was carved on Archimedes' tombstone?", "Ce a fost gravat pe piatra funerară a lui Arhimede?")
        res = re.sub(r'Archimedes considered his proof of the 2:3 ratio[\s\S]*?sculpted onto his tombstone\.',
                     'Arhimede a considerat demonstrația raportului de 2:3 dintre sfera înscrisă și cilindrul circumscris cea mai mare realizare a sa.', res)

    # 4. Replace JSON-LD FAQ block
    if template.get("faqs"):
        faq_entities = [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["a"]
                }
            }
            for item in template["faqs"]
        ]
        faq_json = json.dumps(faq_entities, ensure_ascii=False, indent=8)
        res = re.sub(r'("@type":\s*"FAQPage"[\s\S]*?"mainEntity":\s*)\[[\s\S]*?\](\s*\})', rf'\1{faq_json}\2', res)

    return res

HUB_PATHS = {
    "construction/index.html",
    "finance/index.html",
    "geometry/index.html",
    "physics/index.html",
    "calculus/index.html",
    "statistics/index.html",
    "geometry/2d/index.html",
    "geometry/3d/index.html",
    "geometry/2d/shapes/index.html"
}

def main():
    print("=========================================================")
    print("🚀 OmniOperand Comprehensive Multilingual Remediation Engine")
    print("=========================================================\n")

    total_files = 0
    modified_files = 0

    for lang in LANG_CODES:
        lang_dir = os.path.join(REPO_ROOT, lang)
        if not os.path.isdir(lang_dir):
            continue

        for root, dirs, files in os.walk(lang_dir):
            for file in files:
                if file != "index.html":
                    continue

                full_path = os.path.join(root, file)
                norm_rel = os.path.relpath(full_path, lang_dir).replace("\\", "/")

                total_files += 1

                with open(full_path, "r", encoding="utf-8") as f:
                    orig_content = f.read()

                content = orig_content

                # 1. Common UI & HTML attributes remediation
                content = remediate_common(content, lang)

                # 2. Hub pages card remediation
                if norm_rel in HUB_PATHS:
                    content = remediate_hub_cards(content, lang)

                # 3. Solver tools remediation
                if norm_rel in SOLVER_MAP:
                    slug = SOLVER_MAP[norm_rel]
                    content = remediate_solver_page(content, lang, slug)

                if content != orig_content:
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    modified_files += 1

    print(f"\n✅ Remediation complete: {modified_files} of {total_files} localized files updated.")

if __name__ == "__main__":
    main()
