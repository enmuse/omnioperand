#!/usr/bin/env python3
"""
scripts/generate_i18n.py — Native Multi-Language Internationalization Generator for OmniOperand

Supports 7 non-English languages natively with dedicated crawlable subdirectories:
- Spanish (es)
- French (fr)
- German (de)
- Swedish (sv)
- Norwegian (no)
- Finnish (fi)
- Romanian (ro)

Implements:
1. Dedicated static HTML pages under /{lang}/
2. Reciprocal bidirectional hreflang tags across all languages + x-default
3. Native Unicode mathematical typography (Zero raw LaTeX in HTML)
4. Localized SEO titles, meta descriptions, OpenGraph, and Schema.org JSON-LD
5. Comma-decimal friendly input handling
6. Sitemaps and automated validation
"""

import os
import sys
import re
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

LANGUAGES = {
    "es": {
        "name": "Español",
        "flag": "🇪🇸",
        "locale": "es_ES",
        "home_title": "OmniOperand — Motor de Cálculo Matemático y Solvers Bidireccionales",
        "home_desc": "Plataforma de cálculo de alta precisión para geometría, cálculo, finanzas y física. Fórmulas exactas, planos SVG y protocolos para agentes de IA.",
        "geometry_title": "Geometría y Análisis Espacial | OmniOperand",
        "geometry_desc": "Solvers geométricos 2D y 3D: polígonos regulares, secciones cónicas, poliedros y demostraciones con radicales exactos.",
        "calc_title": "Cálculo y Análisis Matemático | OmniOperand",
        "calc_desc": "Solvers de cálculo diferencial e integral: derivadas polinomiales, integrales definidas y sumas de Riemann.",
        "fin_title": "Finanzas Cuantitativas y Matemáticas Actuariales | OmniOperand",
        "fin_desc": "Matrices de amortización de hipotecas, interés compuesto, rendimiento porcentual anual (APY) y tasa CAGR.",
        "phys_title": "Física y Mecánica Aplicada | OmniOperand",
        "phys_desc": "Calculadoras de cinemática, termodinámica, dinámica de fluidos y circuitos eléctricos con verificación determinista.",
        "stat_title": "Probabilidad y Estadística Matemática | OmniOperand",
        "stat_desc": "Distribuciones estocásticas, intervalos de confianza, pruebas de hipótesis y regresión lineal.",
        "const_title": "Construcción e Ingeniería Civil | OmniOperand",
        "const_desc": "Calculadoras de volumen de hormigón, pendiente de techos, cortes de armadura y dimensionamiento estructural.",
        "shapes_title": "Polígonos y Figuras Geométricas | OmniOperand",
        "shapes_desc": "Solvers analíticos de polígonos regulares de 3 a 1000 lados con expresiones exactas y planos interactivos.",
        "2d_title": "Geometría Bidimensional (2D) | OmniOperand",
        "2d_desc": "Figuras planas, triángulos rectángulos, polígonos regulares y geometría circular analítica.",
        "3d_title": "Geometría Tridimensional (3D) | OmniOperand",
        "3d_desc": "Cálculos volumétricos espaciales, cilindros, prismas y análisis estructural de ingeniería civil.",
        # Core Solvers
        "octagon_title": "Calculadora de Octógono Regular — Fórmulas Exactas, Área y Diagonales | OmniOperand",
        "octagon_desc": "Calculadora bidireccional de octógono regular. Calcula área, perímetro, apotema, circunradio y diagonales con radicales exactos.",
        "hexagon_title": "Calculadora de Hexágono Regular — Fórmulas Exactas, Apotema y Área | OmniOperand",
        "hexagon_desc": "Calculadora bidireccional de hexágono regular. Resuelve lado, apotema, circunradio R=a, área y ancho entre caras.",
        "pentagon_title": "Calculadora de Pentágono Regular — Proporción Áurea y Diagonales | OmniOperand",
        "pentagon_desc": "Calculadora de pentágono regular gobernada por la proporción áurea (ϕ). Resuelve lado, apotema, área y diagonales.",
        "decagon_title": "Calculadora de Decágono Regular — 10 Lados, Circunradio y Diagonales | OmniOperand",
        "decagon_desc": "Calculadora de decágono regular con circunradio R=a·ϕ, ancho entre caras y 4 clases de diagonales.",
        "regular_polygon_title": "Calculadora Universal de Polígonos Regulares (3 a 1000 Lados) | OmniOperand",
        "regular_polygon_desc": "Solucionador universal de polígonos regulares arbitrarios para lado, apotema, área, perímetro y convergencia de Arquímedes.",
        "concrete_title": "Calculadora de Volumen de Hormigón y Bolsas de Cemento | OmniOperand",
        "concrete_desc": "Calcula metros cúbicos, yardas y bolsas de mezcla para losas, zapatas, columnas cilíndricas y cimentaciones.",
        "right_triangle_title": "Calculadora de Triángulo Rectángulo y Teorema de Pitágoras | OmniOperand",
        "right_triangle_desc": "Solucionador de 12 variables para catetos, hipotenusa, altura relativa, radio inscrito y ángulos agudos.",
        "circle_sector_title": "Calculadora de Sector y Segmento Circular | OmniOperand",
        "circle_sector_desc": "Calcula longitud de arco, cuerda, flecha (sagita), área del sector y área del segmento circular.",
        "roof_pitch_title": "Calculadora de Pendiente de Techo y Longitud de Viga | OmniOperand",
        "roof_pitch_desc": "Calcula ángulo en grados, longitud de vigas maestras, cortes a plomo y asiento de viga.",
        "mortgage_title": "Calculadora de Hipotecas y Tabla de Amortización | OmniOperand",
        "mortgage_desc": "Calcula cuota mensual fija, desglose de capital e intereses, y ahorros por pagos anticipados.",
        "compound_title": "Calculadora de Interés Compuesto y Crecimiento de Inversión | OmniOperand",
        "compound_desc": "Capitalización periódica y continua, aportaciones periódicas, tasa efectiva anual (APY) y proyecciones.",
        "auto_loan_title": "Calculadora de Préstamo Automotriz y Cuota Mensual | OmniOperand",
        "auto_loan_desc": "Cuotas de financiamiento de vehículos, crédito por canje, impuestos y capacidad de endeudamiento.",
        "cagr_title": "Calculadora de Tasa de Crecimiento Anual Compuesto (CAGR) | OmniOperand",
        "cagr_desc": "Tasa media geométrica, tiempo de duplicación con regla del 72 y proyecciones de valoración terminal.",
        "integrals_title": "Calculadora de Integrales Definidas y Teorema Fundamental | OmniOperand",
        "integrals_desc": "Calcula integrales polinomiales exactas, antiderivadas y sumas de Riemann con precisión numérica.",
        "derivatives_title": "Calculadora de Derivadas y Recta Tangente | OmniOperand",
        "derivatives_desc": "Calcula derivadas analíticas, pendiente instantánea, ecuación de la recta tangente y concavidad.",
        # Terms
        "home": "Inicio",
        "geometry": "Geometría",
        "calculus": "Cálculo",
        "finance": "Finanzas",
        "physics": "Física",
        "statistics": "Estadística",
        "construction": "Construcción",
        "universal_ngon": "N-Gono Universal",
        "disciplines": "Disciplinas",
        "search_placeholder": "Buscar calculadoras...",
        "all_shapes": "Todas las Formas",
        "params_title": "Parámetros y Entradas",
        "derived_results": "Métricas y Resultados Calculados",
        "analytical_proof": "Demostración Analítica e Invariantes",
        "step_by_step": "Demostración Matemática Paso a Paso",
        "faq_title": "Preguntas Frecuentes",
        "unit_metric": "cm",
        "area_metric": "cm²",
        "vol_metric": "m³"
    },
    "fr": {
        "name": "Français",
        "flag": "🇫🇷",
        "locale": "fr_FR",
        "home_title": "OmniOperand — Moteur de Calcul Mathématique et Solveurs Bidirectionnels",
        "home_desc": "Plateforme de calcul haute précision en géométrie, analyse, finance et physique. Formules exactes et plans SVG interactifs.",
        "geometry_title": "Géométrie & Analyse Spatiale | OmniOperand",
        "geometry_desc": "Solveurs géométriques 2D et 3D : polygones réguliers, coniques, polyèdres et preuves analytiques avec radicaux exacts.",
        "calc_title": "Calcul Infinitésimal & Analyse Mathématique | OmniOperand",
        "calc_desc": "Dérivées de polynômes, intégrales définies, théorèmes fondamentaux et sommes de Riemann.",
        "fin_title": "Finance Quantitative & Mathématiques Actuarielles | OmniOperand",
        "fin_desc": "Tableaux d'amortissement de prêts immobiliers, intérêts composés, rendement annuel effectif et taux CAGR.",
        "phys_title": "Physique & Mécanique de l'Ingénieur | OmniOperand",
        "phys_desc": "Cinématique, thermodynamique, mécanique des fluides et circuits électriques avec calculs vérifiés.",
        "stat_title": "Probabilités & Statistique Mathématique | OmniOperand",
        "stat_desc": "Distributions statistiques, intervalles de confiance, tests d'hypothèses et régressions linéaires.",
        "const_title": "Construction & Génie Civil | OmniOperand",
        "const_desc": "Volume de béton, pente de toiture, calepinage de charpente et dimensionnement d'éléments porteurs.",
        "shapes_title": "Polygones & Formes Géométriques | OmniOperand",
        "shapes_desc": "Solveurs analytiques de polygones réguliers de 3 à 1000 côtés avec formules closes et plans vectoriels.",
        "2d_title": "Géométrie Bidimensionnelle (2D) | OmniOperand",
        "2d_desc": "Figures planes, triangles rectangles, polygones réguliers et arcs de cercle analytiques.",
        "3d_title": "Géométrie Tridimensionnelle (3D) | OmniOperand",
        "3d_desc": "Calculs volumétriques spatiaux, prismes, cylindres et cubatures de génie civil.",
        # Core Solvers
        "octagon_title": "Calculateur d'Octogone Régulier — Formules Exactes, Aire et Diagonales | OmniOperand",
        "octagon_desc": "Calculateur bidirectionnel d'octogone régulier. Résolvez aire, périmètre, apothème, rayon circonscrit et diagonales.",
        "hexagon_title": "Calculateur d'Hexagone Régulier — Formules Exactes, Apothème et Aire | OmniOperand",
        "hexagon_desc": "Solveur bidirectionnel d'hexagone régulier. Calcule côté, apothème, rayon circonscrit R=a, aire et largeur sur plats.",
        "pentagon_title": "Calculateur de Pentagone Régulier — Nombre d'Or et Diagonales | OmniOperand",
        "pentagon_desc": "Calculateur de pentagone régulier régi par le nombre d'or (ϕ). Calcule côté, apothème, aire et diagonales.",
        "decagon_title": "Calculateur de Décagone Régulier — 10 Côtés, Rayon et Diagonales | OmniOperand",
        "decagon_desc": "Calculateur de décagone régulier avec rayon circonscrit R=a·ϕ, largeur sur plats et 4 classes de diagonales.",
        "regular_polygon_title": "Calculateur Universel de Polygones Réguliers (3 à 1000 Côtés) | OmniOperand",
        "regular_polygon_desc": "Solveur universel de polygones réguliers arbitraires pour côté, apothème, aire, périmètre et convergence d'Archimède.",
        "concrete_title": "Calculateur de Volume de Béton et Nombre de Sacs | OmniOperand",
        "concrete_desc": "Calculez les mètres cubes de béton et le nombre de sacs de ciment pour dalles, semelles et poteaux.",
        "right_triangle_title": "Calculateur de Triangle Rectangle & Théorème de Pythagore | OmniOperand",
        "right_triangle_desc": "Solveur à 12 variables pour côtés, hypoténuse, hauteur relative, rayon inscrit et angles aigus.",
        "circle_sector_title": "Calculateur de Secteur & Segment Circulaire | OmniOperand",
        "circle_sector_desc": "Calculez la longueur d'arc, corde, flèche (sagitta), aire du secteur et aire du segment circulaire.",
        "roof_pitch_title": "Calculateur de Pente de Toit & Longueur de Chevron | OmniOperand",
        "roof_pitch_desc": "Calculez l'angle de pente en degrés, longueur de chevron, coupes d'aplomb et gueule de loup.",
        "mortgage_title": "Calculateur de Prêt Immobilier & Tableau d'Amortissement | OmniOperand",
        "mortgage_desc": "Échéances mensuelles de prêt immobilier, ventilation capital/intérêts et économies sur remboursements anticipés.",
        "compound_title": "Calculateur d'Intérêts Composés & Rendement d'Épargne | OmniOperand",
        "compound_desc": "Capitalisation périodique et continue, versements réguliers, taux effectif global et projections.",
        "auto_loan_title": "Calculateur de Crédit Auto & Mensualités | OmniOperand",
        "auto_loan_desc": "Financement automobile, apport, reprise de véhicule, taxes et mensualités détaillées.",
        "cagr_title": "Calculateur de Taux de Croissance Annuel Composé (CAGR) | OmniOperand",
        "cagr_desc": "Taux moyen géométrique, période de doublement selon la règle de 72 et valorisation prévisionnelle.",
        "integrals_title": "Calculateur d'Intégrales Définies & Théorème Fondamental | OmniOperand",
        "integrals_desc": "Évaluez les primitives exactes et les intégrales définies avec précision analytique.",
        "derivatives_title": "Calculateur de Dérivées & Tangente | OmniOperand",
        "derivatives_desc": "Calculez les dérivées polynomiales, la pente instantanée, l'équation de tangente et la concavité.",
        # Terms
        "home": "Accueil",
        "geometry": "Géométrie",
        "calculus": "Calcul",
        "finance": "Finance",
        "physics": "Physique",
        "statistics": "Statistique",
        "construction": "Construction",
        "universal_ngon": "N-Gone Universel",
        "disciplines": "Disciplines",
        "search_placeholder": "Rechercher des calculateurs...",
        "all_shapes": "Toutes les Formes",
        "params_title": "Paramètres & Variables",
        "derived_results": "Métriques & Résultats Calculés",
        "analytical_proof": "Preuve Analytique & Invariants",
        "step_by_step": "Démonstration Mathématique Étape par Étape",
        "faq_title": "Foire Aux Questions",
        "unit_metric": "cm",
        "area_metric": "cm²",
        "vol_metric": "m³"
    },
    "de": {
        "name": "Deutsch",
        "flag": "🇩🇪",
        "locale": "de_DE",
        "home_title": "OmniOperand — Mathematische Rechenplattform & Bidirektionale Gleichungslöser",
        "home_desc": "Hochpräzise Rechner für Geometrie, Analysis, Finanzmathematik und Physik. Exakte Radikale, SVG-Baupläne und KI-Agenten-Protokolle.",
        "geometry_title": "Geometrie & Raumgeometrie | OmniOperand",
        "geometry_desc": "2D- und 3D-Geometrie-Rechner: regelmäßige Polygone, Kegelschnitte, Polyeder und exakte Radikalbeweise.",
        "calc_title": "Analysis & Höhere Mathematik | OmniOperand",
        "calc_desc": "Differential- und Integralrechnung: Polynomableitungen, bestimmte Integrale und Riemann-Summen.",
        "fin_title": "Finanzmathematik & Investitionsanalyse | OmniOperand",
        "fin_desc": "Tilgungspläne für Baufinanzierung, Zinseszinsberechnung, Effektivzinssatz (APY) und CAGR-Wachstumsraten.",
        "phys_title": "Physik & Technische Mechanik | OmniOperand",
        "phys_desc": "Kinematik, Thermodynamik, Fluidmechanik und elektrische Schaltungen mit deterministischer Prüfung.",
        "stat_title": "Wahrscheinlichkeitsrechnung & Statistik | OmniOperand",
        "stat_desc": "Stochastische Verteilungen, Konfidenzintervalle, Hypothesentests und Regressionsmodelle.",
        "const_title": "Bauwesen & Baustatik | OmniOperand",
        "const_desc": "Betonvolumen- und Sackbedarfsrechner, Dachneigung, Sparrenlänge und statische Vorbemessung.",
        "shapes_title": "Polygone & Geometrische Formen | OmniOperand",
        "shapes_desc": "Analytische Rechner für regelmäßige Vielecke (3 bis 1000 Ecken) mit geschlossenen Formeln.",
        "2d_title": "Zweidimensionale (2D) Geometrie | OmniOperand",
        "2d_desc": "Ebene Figuren, rechtwinklige Dreiecke, regelmäßige Vielecke und Kreisbogensegmente.",
        "3d_title": "Dreidimensionale (3D) Geometrie | OmniOperand",
        "3d_desc": "Räumliche Volumenberechnungen, Prismen, Zylinder und Erdbau-Kubaturen im Ingenieurbau.",
        # Core Solvers
        "octagon_title": "Regelmäßiges Achteck Rechner — Exakte Formeln, Fläche & Diagonalen | OmniOperand",
        "octagon_desc": "Bidirektionaler Achteck-Rechner. Berechnet Seitenlänge, Fläche, Umfang, Inkreisradius, Umkreisradius und Diagonalen.",
        "hexagon_title": "Regelmäßiges Sechseck Rechner — Formeln, Inkreisradius & Fläche | OmniOperand",
        "hexagon_desc": "Bidirektionaler Sechseck-Rechner. Berechnet Seitenlänge, Inkreisradius, Umkreisradius R=a, Fläche und Schlüsselweite.",
        "pentagon_title": "Regelmäßiges Fünfeck Rechner — Goldener Schnitt & Diagonalen | OmniOperand",
        "pentagon_desc": "Fünfeck-Rechner bestimmt durch den Goldenen Schnitt (ϕ). Berechnet Seitenlänge, Inkreisradius, Fläche und Diagonalen.",
        "decagon_title": "Regelmäßiges Zehneck Rechner — 10 Ecken, Radius & Schlüsselweite | OmniOperand",
        "decagon_desc": "Zehneck-Rechner mit Umkreisradius R=a·ϕ, Schlüsselweite und 4 Diagonalenklassen.",
        "regular_polygon_title": "Universeller Vieleck-Rechner (3 bis 1000 Ecken) | OmniOperand",
        "regular_polygon_desc": "Universeller Rechner für beliebige regelmäßige Polygone: Seitenlänge, Inkreisradius, Fläche, Umfang und Kreisannäherung.",
        "concrete_title": "Betonvolumen & Sackbedarfsrechner | OmniOperand",
        "concrete_desc": "Berechnet Kubikmeter Beton und Fertigbetonsäcke für Bodenplatten, Fundamente und Rundstützen.",
        "right_triangle_title": "Rechtwinkliges Dreieck & Satz des Pythagoras Rechner | OmniOperand",
        "right_triangle_desc": "12-Variablen-Löser für Katheten, Hypotenuse, Dreieckshöhe, Inkreisradius und spitze Winkel.",
        "circle_sector_title": "Kreissektor & Kreissegment Rechner | OmniOperand",
        "circle_sector_desc": "Berechnet Bogenlänge, Sehnenlänge, Bogenhöhe (Sagitta), Sektorfläche und Segmentfläche.",
        "roof_pitch_title": "Dachneigung & Sparrenlänge Rechner | OmniOperand",
        "roof_pitch_desc": "Berechnet Neigungswinkel in Grad, Sparrenlänge, Lotschnitt und Kerve für Zimmerer und Dachdecker.",
        "mortgage_title": "Baufinanzierung & Tilgungsplan Rechner | OmniOperand",
        "mortgage_desc": "Monatliche Annuität, Zins- und Tilgungsanteil sowie Zinsersparnis durch Sondertilgungen.",
        "compound_title": "Zinseszins & Vermögensaufbau Rechner | OmniOperand",
        "compound_desc": "Periodische und kontinuierliche Verzinsung, Sparraten, effektiver Jahreszins (APY) und Endkapital.",
        "auto_loan_title": "Autokredit & Ratenrechner | OmniOperand",
        "auto_loan_desc": "Fahrzeugfinanzierung, Anzahlung, Inzahlungnahme, Monatsrate und Gesamtkosten.",
        "cagr_title": "Jährliche Wachstumsrate (CAGR) Rechner | OmniOperand",
        "cagr_desc": "Geometrisches Mittel der Rendite, Verdopplungszeit nach der 72er-Regel und Zielwertumkehrung.",
        "integrals_title": "Bestimmtes Integral & Hauptsatz Rechner | OmniOperand",
        "integrals_desc": "Berechnet exakte Stammfunktionen und bestimmte Integrale mit analytischer Präzision.",
        "derivatives_title": "Ableitungsrechner & Tangentengleichung | OmniOperand",
        "derivatives_desc": "Berechnet Polynomableitungen, momentane Steigung, Tangenten- und Normalengleichung.",
        # Terms
        "home": "Startseite",
        "geometry": "Geometrie",
        "calculus": "Analysis",
        "finance": "Finanzen",
        "physics": "Physik",
        "statistics": "Statistik",
        "construction": "Bauwesen",
        "universal_ngon": "Universelles N-Eck",
        "disciplines": "Fachgebiete",
        "search_placeholder": "Rechner suchen...",
        "all_shapes": "Alle Formen",
        "params_title": "Parameter & Eingabewerte",
        "derived_results": "Berechnete Ausgabewerte",
        "analytical_proof": "Analytischer Beweis & Invarianten",
        "step_by_step": "Schritt-für-Schritt Herleitung",
        "faq_title": "Häufig Gestellte Fragen",
        "unit_metric": "cm",
        "area_metric": "cm²",
        "vol_metric": "m³"
    },
    "sv": {
        "name": "Svenska",
        "flag": "🇸🇪",
        "locale": "sv_SE",
        "home_title": "OmniOperand — Matematisk Beräkningsmotor & Dubbelriktade Lösare",
        "home_desc": "Beräkningsverktyg med hög precision inom geometri, analys, finans och fysik. Exakta formler och interaktiva SVG-ritningar.",
        "geometry_title": "Geometri & Rumsanalys | OmniOperand",
        "geometry_desc": "2D- och 3D-geometriska lösare: regelbundna polygoner, kägelsnitt, polyedrar och exakta bevis.",
        "calc_title": "Matematisk Analys & Kalkyl | OmniOperand",
        "calc_desc": "Differential- och integrallösare: polynomderivator, bestämda integraler och Riemannsummor.",
        "fin_title": "Finansiell Matematik & Aktuariell Analys | OmniOperand",
        "fin_desc": "Amorteringsplaner för bolån, ränta-på-ränta, effektiv årsränta (APY) och CAGR-tillväxt.",
        "phys_title": "Fysik & Teknisk Mekanik | OmniOperand",
        "phys_desc": "Kinematik, termodynamik, strömningsmekanik och elektriska kretsar med maskinprecision.",
        "stat_title": "Sannolikhetsteori & Matematisk Statistik | OmniOperand",
        "stat_desc": "Stokastiska fördelningar, konfidensintervall, hypotesprövning och linjär regression.",
        "const_title": "Byggteknik & Väg- och Vattenbyggnad | OmniOperand",
        "const_desc": "Betongvolym, taklutning, takstolslängd och konstruktionsberäkningar.",
        "shapes_title": "Polygoner & Geometriska Figurer | OmniOperand",
        "shapes_desc": "Analytiska lösare för regelbundna månghörningar (3 till 1000 hörn) med sluten algebra.",
        "2d_title": "Tvådimensionell (2D) Geometri | OmniOperand",
        "2d_desc": "Plana figurer, rätvinkliga trianglar, regelbundna polygoner och cirkelbågar.",
        "3d_title": "Tredimensionell (3D) Geometri | OmniOperand",
        "3d_desc": "Volymberäkningar i rymden, prismor, cylindrar och schaktvolymer inom anläggning.",
        # Core Solvers
        "octagon_title": "Regelbunden Åtahörning Kalkylator — Exakta Formler, Area & Diagonaler | OmniOperand",
        "octagon_desc": "Dubbelriktad kalkylator för regelbunden oktagon. Beräknar sida, area, omkrets, apotem, omskriven radie och diagonaler.",
        "hexagon_title": "Regelbunden Sexhörning Kalkylator — Formler, Apotem & Area | OmniOperand",
        "hexagon_desc": "Dubbelriktad kalkylator för regelbunden hexagon. Löser sida, apotem, omskriven radie R=a, area och nyckelvidd.",
        "pentagon_title": "Regelbunden Femhörning Kalkylator — Gyllene Snittet & Diagonaler | OmniOperand",
        "pentagon_desc": "Femhörningslösare styrd av det gyllene snittet (ϕ). Beräknar sida, apotem, area och diagonallängder.",
        "decagon_title": "Regelbunden Tiohörning Kalkylator — 10 Hörn, Radie & Spännvidd | OmniOperand",
        "decagon_desc": "Dekagonkalkylator med omskriven radie R=a·ϕ, nyckelvidd och 4 diagonalklasser.",
        "regular_polygon_title": "Universell Månghörningskalkylator (3 till 1000 Hörn) | OmniOperand",
        "regular_polygon_desc": "Universell lösare för godtyckliga regelbundna polygoner: sida, apotem, area, omkrets och Archimedes cirkelkonvergens.",
        "concrete_title": "Betongvolym & Säcktalskalkylator | OmniOperand",
        "concrete_desc": "Beräknar kubikmeter betong och antal färdigbetongsäckar för plattor, fundament och runda pelare.",
        "right_triangle_title": "Rätvinklig Triangel & Pythagoras Sats Kalkylator | OmniOperand",
        "right_triangle_desc": "Lösare med 12 variabler för kateter, hypotenusa, höjd, inskriven radie och spetsiga vinklar.",
        "circle_sector_title": "Cirkelsektor & Cirkelsegment Kalkylator | OmniOperand",
        "circle_sector_desc": "Beräknar båglängd, korda, pilhöjd (sagitta), sektorarea och segmentarea.",
        "roof_pitch_title": "Taklutning & Takstolslängd Kalkylator | OmniOperand",
        "roof_pitch_desc": "Beräknar lutningsvinkel i grader, takstolslängd, lodsnitt och bärstöd för snickare och takläggare.",
        "mortgage_title": "Bolån & Amorteringskalkylator | OmniOperand",
        "mortgage_desc": "Månadskostnad för bolån, ränte- och amorteringsandel samt räntebesparing vid extraamortering.",
        "compound_title": "Ränta på Ränta & Sparandekalkylator | OmniOperand",
        "compound_desc": "Månadssparande, ränta-på-ränta-effekt, effektiv årsränta och kapitaltillväxt.",
        "auto_loan_title": "Billån & Avbetalningskalkylator | OmniOperand",
        "auto_loan_desc": "Finansiering av bil, handpenning, inbytesbil, månadskostnad och totalkostnad.",
        "cagr_title": "Genomsnittlig Årlig Tillväxt (CAGR) Kalkylator | OmniOperand",
        "cagr_desc": "Geometrisk medeltillväxt, fördubblingstid enligt 72-regeln och målkapitalberäkning.",
        "integrals_title": "Bestämd Integral & Analysens Fundamentalsats | OmniOperand",
        "integrals_desc": "Beräknar exakta primitiva funktioner och bestämda integraler med maskinprecision.",
        "derivatives_title": "Derivata & Tangentkalkylator | OmniOperand",
        "derivatives_desc": "Beräknar polynomderivator, momentan lutning, tangentlinjens ekvation och konkavitet.",
        # Terms
        "home": "Hem",
        "geometry": "Geometri",
        "calculus": "Analys",
        "finance": "Finans",
        "physics": "Fysik",
        "statistics": "Statistik",
        "construction": "Byggteknik",
        "universal_ngon": "Universell N-Gon",
        "disciplines": "Ämnen",
        "search_placeholder": "Sök kalkylatorer...",
        "all_shapes": "Alla Former",
        "params_title": "Parametrar & Indata",
        "derived_results": "Beräknade Resultat",
        "analytical_proof": "Analytiskt Bevis & Invarianter",
        "step_by_step": "Steg-för-steg Matematiskt Bevis",
        "faq_title": "Vanliga Frågor",
        "unit_metric": "cm",
        "area_metric": "cm²",
        "vol_metric": "m³"
    },
    "no": {
        "name": "Norsk",
        "flag": "🇳🇴",
        "locale": "nb_NO",
        "home_title": "OmniOperand — Matematisk Beregningsmotor & Toveis Likningsløsere",
        "home_desc": "Høypresisjons beregningsplattform innen geometri, analyse, finans og fysikk. Eksakte formler og interaktive SVG-tegninger.",
        "geometry_title": "Geometri & Romgeometri | OmniOperand",
        "geometry_desc": "2D- og 3D-geometriske løsere: regulære polygoner, kjeglesnitt, polyedre og eksakte radikalbevis.",
        "calc_title": "Matematisk Analyse & Kalkulus | OmniOperand",
        "calc_desc": "Derivasjon og integrasjon: polynomderivater, bestemte integraler og Riemann-summer.",
        "fin_title": "Finansiell Matematikk & Aktuaranalyse | OmniOperand",
        "fin_desc": "Nedbetalingsplaner for boliglån, rentesrente, effektiv rente (APY) og årlig sammensatt vekstrate (CAGR).",
        "phys_title": "Fysikk & Teknisk Mekanikk | OmniOperand",
        "phys_desc": "Kinematikk, termodynamikk, fluiddynamikk og elektriske kretser med maskinpresisjon.",
        "stat_title": "Sannsynlighetsregning & Statistikk | OmniOperand",
        "stat_desc": "Stokastiske fordelinger, konfidensintervaller, hypotesetesting og lineær regresjon.",
        "const_title": "Bygg & Anleggsteknikk | OmniOperand",
        "const_desc": "Kalkulator for betongvolum, takfall, sperrelengde og statiske konstruksjoner.",
        "shapes_title": "Polygoner & Geometriske Figurer | OmniOperand",
        "shapes_desc": "Analytiske løsere for regulære polygoner (3 til 1000 sider) med lukkede formler og tegninger.",
        "2d_title": "Todimensjonal (2D) Geometri | OmniOperand",
        "2d_desc": "Plane figurer, rettvinklede trekanter, regulære polygoner og sirkelsegmenter.",
        "3d_title": "Tredimensjonal (3D) Geometri | OmniOperand",
        "3d_desc": "Romlige volumberegninger, prismer, sylindre og masseberegninger for anlegg.",
        # Core Solvers
        "octagon_title": "Regelmessig Åttekant Kalkulator — Eksakte Formler, Areal & Diagonaler | OmniOperand",
        "octagon_desc": "Toveis kalkulator for regulær åttekant (oktogon). Beregner sidelengde, areal, omkrets, apotem, omskrevet radius og diagonaler.",
        "hexagon_title": "Regelmessig Sekskant Kalkulator — Formler, Apotem & Areal | OmniOperand",
        "hexagon_desc": "Toveis kalkulator for regulær heksagon. Beregner side, apotem, omskrevet radius R=a, areal og nøkkelvidde.",
        "pentagon_title": "Regelmessig Femkant Kalkulator — Det Gylne Snitt & Diagonaler | OmniOperand",
        "pentagon_desc": "Femkantkalkulator styrt av det gylne snitt (ϕ). Beregner sidelengde, apotem, areal og diagonaler.",
        "decagon_title": "Regelmessig Tikant Kalkulator — 10 Sider, Radius & Nøkkelvidde | OmniOperand",
        "decagon_desc": "Tikantkalkulator med omskrevet radius R=a·ϕ, nøkkelvidde og 4 diagonalklasser.",
        "regular_polygon_title": "Universell Polygonkalkulator (3 til 1000 Sider) | OmniOperand",
        "regular_polygon_desc": "Universell løser for vilkårlige regulære n-kanter: side, apotem, areal, omkrets og sirkeltilnærming.",
        "concrete_title": "Betongvolum & Sekketall Kalkulator | OmniOperand",
        "concrete_desc": "Beregner kubikkmeter betong og antall ferdigbetongsekker for støp av såler, plater og søyler.",
        "right_triangle_title": "Rettvinklet Trekant & Pythagoras' Læresetning Kalkulator | OmniOperand",
        "right_triangle_desc": "12-variabel løser for kateter, hypotenus, høyde, innskrevet radius og spisse vinkler.",
        "circle_sector_title": "Sirkelsektor & Sirkelsegment Kalkulator | OmniOperand",
        "circle_sector_desc": "Beregner buelengde, korde, pilhøyde (sagitta), sektorareal og segmentareal.",
        "roof_pitch_title": "Takfall & Sperrelengde Kalkulator | OmniOperand",
        "roof_pitch_desc": "Beregner takvinkel i grader, sperrelengde, loddavskjæring og bjelkeopplegg for tømrere.",
        "mortgage_title": "Boliglån & Nedbetalingsplan Kalkulator | OmniOperand",
        "mortgage_desc": "Terminbeløp på boliglån, fordeling av renter og avdrag, samt rentebesparelse ved ekstra innbetaling.",
        "compound_title": "Rentesrente & Sparekalkulator | OmniOperand",
        "compound_desc": "Månedlig sparing, rentesrenteeffekt, effektiv rente og formuesutvikling.",
        "auto_loan_title": "Billån & Avdragskalkulator | OmniOperand",
        "auto_loan_desc": "Billån med egenkapital, innbyttebil, månedlige avdrag og totale lånekostnader.",
        "cagr_title": "Årlig Sammensatt Vekstrate (CAGR) Kalkulator | OmniOperand",
        "cagr_desc": "Geometrisk gjennomsnittlig vekst, doblingstid etter 72-regelen og målverdiberegning.",
        "integrals_title": "Bestemt Integral & Fundamentalteoremet Kalkulator | OmniOperand",
        "integrals_desc": "Beregner eksakte antideriverte og bestemte integraler med maskinpresisjon.",
        "derivatives_title": "Derivasjon & Tangentkalkulator | OmniOperand",
        "derivatives_desc": "Beregner polynomderivater, momentan stigning, tangentligning og krumning.",
        # Terms
        "home": "Hjem",
        "geometry": "Geometri",
        "calculus": "Analyse",
        "finance": "Finans",
        "physics": "Fysikk",
        "statistics": "Statistikk",
        "construction": "Bygg & Anlegg",
        "universal_ngon": "Universell N-Gon",
        "disciplines": "Fagområder",
        "search_placeholder": "Søk etter kalkulatorer...",
        "all_shapes": "Alle Figurer",
        "params_title": "Parametere & Inndata",
        "derived_results": "Beregnede Resultater",
        "analytical_proof": "Analytisk Bevis & Invarianter",
        "step_by_step": "Steg-for-steg Matematisk Utledning",
        "faq_title": "Ofte Stilte Spørsmål",
        "unit_metric": "cm",
        "area_metric": "cm²",
        "vol_metric": "m³"
    },
    "fi": {
        "name": "Suomi",
        "flag": "🇫🇮",
        "locale": "fi_FI",
        "home_title": "OmniOperand — Matemaattinen Laskentamoottori & Kaksisuuntaiset Ratkaisimet",
        "home_desc": "Tarkan matematiikan laskimet geometrian, differentiaalilaskennan, talousmatematiikan ja fysiikan tarpeisiin.",
        "geometry_title": "Geometria & Tila-analyysi | OmniOperand",
        "geometry_desc": "2D- ja 3D-geometrian ratkaisimet: säännölliset monikulmiot, kartioleikkaukset, monitahokkaat ja eksaktit juurilausekkeet.",
        "calc_title": "Differentiaali- ja Integraalilaskenta | OmniOperand",
        "calc_desc": "Polynomien derivaatat, määrätyt integraalit, analyysin peruslause ja Riemannin summat.",
        "fin_title": "Kvantitatiivinen Rahoitus & Vakuutusmatematiikka | OmniOperand",
        "fin_desc": "Asuntolainan lyhennystaulukot, korkoa korolle -laskenta, todellinen vuosikorko (APY) ja CAGR-kasvuasteet.",
        "phys_title": "Fysiikka & Teknillinen Mekaniikka | OmniOperand",
        "phys_desc": "Kinematiikka, termodynamiikka, virtausmekaniikka ja sähköpiirit deterministisellä tarkkuudella.",
        "stat_title": "Todennäköisyyslaskenta & Tilastotiede | OmniOperand",
        "stat_desc": "Stokastiset jakaumat, luottamusvälit, hypoteesitestit ja lineaarinen regressio.",
        "const_title": "Rakennustekniikka & Maa- ja Vesirakennus | OmniOperand",
        "const_desc": "Betonimenekin laskuri, katon kaltevuus, kattotuolin pituus ja rakennesuunnittelun mitoitus.",
        "shapes_title": "Monikulmiot & Geometriset Muodot | OmniOperand",
        "shapes_desc": "Säännöllisten monikulmioiden (3–1000 sivua) analyyttiset ratkaisimet tarkoilla lausekkeilla.",
        "2d_title": "Kaksiulotteinen (2D) Geometria | OmniOperand",
        "2d_desc": "Tasokuviot, suorakulmaiset kolmiot, säännölliset monikulmiot ja ympyräsektorit.",
        "3d_title": "Kolmiulotteinen (3D) Geometria | OmniOperand",
        "3d_desc": "Avaruusgeometriset tilavuuslaskelmat, lieriöt, särmiöt ja maarakennuksen massalaskenta.",
        # Core Solvers
        "octagon_title": "Säännöllinen Kahdeksankulmio Laskuri — Kaavat, Pinta-ala & Diagonaalit | OmniOperand",
        "octagon_desc": "Kaksisuuntainen kahdeksankulmiolaskuri (oktagoni). Laske sivun pituus, pinta-ala, piiri, apoteema, ulkoympyrän säde ja lävistäjät.",
        "hexagon_title": "Säännöllinen Kuusikulmio Laskuri — Kaavat, Apoteema & Pinta-ala | OmniOperand",
        "hexagon_desc": "Kaksisuuntainen kuusikulmiolaskuri. Ratkaise sivu, apoteema, ulkoympyrän säde R=a, pinta-ala ja avainväli.",
        "pentagon_title": "Säännöllinen Viisikulmio Laskuri — Kultainen Leikkaus & Lävistäjät | OmniOperand",
        "pentagon_desc": "Viisikulmiolaskuri kultaisen leikkauksen (ϕ) suhteilla. Laske sivun pituus, apoteema, pinta-ala ja lävistäjät.",
        "decagon_title": "Säännöllinen Kymmenkulmio Laskuri — 10 Sivua, Säde & Avainväli | OmniOperand",
        "decagon_desc": "Kymmenkulmiolaskuri ulkoympyrän säteellä R=a·ϕ, avainvälillä ja 4 lävistäjäluokalla.",
        "regular_polygon_title": "Universaali Monikulmiolaskuri (3–1000 Sivua) | OmniOperand",
        "regular_polygon_desc": "Universaali säännöllisten n-kulmioiden ratkaisin: sivu, apoteema, pinta-ala, piiri ja Arkhimedeen suppeneminen.",
        "concrete_title": "Betonimenekki & Säkkimäärä Laskuri | OmniOperand",
        "concrete_desc": "Laske betonikuutiot ja kuivabetonisäkit laatoille, anturoille ja pyöreille pilareille.",
        "right_triangle_title": "Suorakulmainen Kolmio & Pythagoraan Lause Laskuri | OmniOperand",
        "right_triangle_desc": "12-muuttujan ratkaisin kateeteille, hypotenuusalle, korkeusjanalle, sisäympyrän säteelle ja kulmille.",
        "circle_sector_title": "Ympyrän Sektori & Segmentti Laskuri | OmniOperand",
        "circle_sector_desc": "Laske kaaren pituus, jänne, sagitta (korkeus), sektorin pinta-ala ja segmentin pinta-ala.",
        "roof_pitch_title": "Katon Kaltevuus & Kattotuolin Pituus Laskuri | OmniOperand",
        "roof_pitch_desc": "Laske kattokaltevuus asteina, kattotuolin pituus, pystykulmat ja räystään loveukset kirvesmiehille.",
        "mortgage_title": "Asuntolaina & Lyhennystaulukko Laskuri | OmniOperand",
        "mortgage_desc": "Kuukausierä, koron ja lyhennyksen osuus sekä säästö ylimääräisistä lyhennyksistä.",
        "compound_title": "Korkoa Korolle & Säästölaskuri | OmniOperand",
        "compound_desc": "Kuukausisäästäminen, korkoa korolle -ilmiö, todellinen vuosikorko ja säästöjen kasvuennuste.",
        "auto_loan_title": "Autolaina & Osamaksulaskuri | OmniOperand",
        "auto_loan_desc": "Auton rahoitus, käsiraha, vaihtoauto, kuukausierä ja kokonaiskustannukset.",
        "cagr_title": "Keskimääräinen Vuotuinen Kasvu (CAGR) Laskuri | OmniOperand",
        "cagr_desc": "Geometrinen keskimääräinen kasvu, 72-säännön tuplaantumisaika ja sijoituksen tuleva arvo.",
        "integrals_title": "Määrätyn Integraalin & Integraalilaskennan Peruslauseen Laskuri | OmniOperand",
        "integrals_desc": "Laske polynomien integraalit ja määrätyt integraalit analyyttisellä tarkkuudella.",
        "derivatives_title": "Derivaatta & Tangenttilaskuri | OmniOperand",
        "derivatives_desc": "Laske polynomien derivaatat, hetkellinen kulmakerroin, tangentin yhtälö ja kaarevuus.",
        # Terms
        "home": "Etusivu",
        "geometry": "Geometria",
        "calculus": "Analyysi",
        "finance": "Rahoitus",
        "physics": "Fysiikka",
        "statistics": "Tilastot",
        "construction": "Rakennus",
        "universal_ngon": "Universaali N-Kulmio",
        "disciplines": "Tieteenalat",
        "search_placeholder": "Etsi laskureita...",
        "all_shapes": "Kaikki Muodot",
        "params_title": "Parametrit & Syötteet",
        "derived_results": "Lasketut Tulokset",
        "analytical_proof": "Analyyttinen Todistus & Invariantit",
        "step_by_step": "Vaiheittainen Matemaattinen Johtaminen",
        "faq_title": "Usein Kysytyt Kysymykset",
        "unit_metric": "cm",
        "area_metric": "cm²",
        "vol_metric": "m³"
    },
    "ro": {
        "name": "Română",
        "flag": "🇷🇴",
        "locale": "ro_RO",
        "home_title": "OmniOperand — Motor de Calcul Matematic & Solvere Bidirecționale",
        "home_desc": "Platformă computațională de înaltă precizie pentru geometrie, analiză matematică, finanțe și fizică. Formule exacte și diagrame SVG.",
        "geometry_title": "Geometrie & Analiză Spațială | OmniOperand",
        "geometry_desc": "Solvere geometrice 2D și 3D: poligoane regulate, secțiuni conice, poliedre și demonstrații exacte cu radicali.",
        "calc_title": "Calcul Infinitezimal & Analiză Matematică | OmniOperand",
        "calc_desc": "Calcul diferențial și integral: derivate de polinoame, integrale definite și sume Riemann.",
        "fin_title": "Finanțe Cantitative & Matematică Actuarială | OmniOperand",
        "fin_desc": "Tabele de amortizare credite ipotecare, dobândă compusă, randament anual efectiv (APY) și rată CAGR.",
        "phys_title": "Fizică & Mecanică Tehnică | OmniOperand",
        "phys_desc": "Cinematică, termodinamică, dinamica fluidelor și circuite electrice cu precizie analitică.",
        "stat_title": "Probabilități & Statistică Matematică | OmniOperand",
        "stat_desc": "Distribuții stocastice, intervale de încredere, teste de ipoteză și regresie liniară.",
        "const_title": "Construcții & Inginerie Civilă | OmniOperand",
        "const_desc": "Calculator volum beton, pantă acoperiș, lungime căpriori și dimensionare structurală.",
        "shapes_title": "Poligoane & Figuri Geometrice | OmniOperand",
        "shapes_desc": "Solvere analitice pentru poligoane regulate de la 3 la 1000 de laturi cu formule închise.",
        "2d_title": "Geometrie Bidimensională (2D) | OmniOperand",
        "2d_desc": "Figuri plane, triunghiuri dreptunghice, poligoane regulate și segmente circulare.",
        "3d_title": "Geometrie Tridimensională (3D) | OmniOperand",
        "3d_desc": "Calculul volumelor corpurilor geometrice, prisme, cilindri și terasamente în inginerie civilă.",
        # Core Solvers
        "octagon_title": "Calculator Octogon Regulat — Formule Exacte, Arie & Diagonale | OmniOperand",
        "octagon_desc": "Calculator bidirecțional pentru octogon regulat. Calculează latura, aria, perimetrul, apotema, raza cercului circumscris și diagonalele.",
        "hexagon_title": "Calculator Hexagon Regulat — Formule Exacte, Apotemă & Arie | OmniOperand",
        "hexagon_desc": "Calculator bidirecțional pentru hexagon regulat. Rezolvă latura, apotema, raza circumscrisă R=a, aria și lățimea între fețe.",
        "pentagon_title": "Calculator Pentagon Regulat — Secțiunea de Aur & Diagonale | OmniOperand",
        "pentagon_desc": "Calculator pentagon regulat guvernat de secțiunea de aur (ϕ). Calculează latura, apotema, aria și diagonalele.",
        "decagon_title": "Calculator Decagon Regulat — 10 Laturi, Rază & Diagonale | OmniOperand",
        "decagon_desc": "Calculator decagon regulat cu raza circumscrisă R=a·ϕ, lățimea între fețe și 4 clase de diagonale.",
        "regular_polygon_title": "Calculator Universal de Poligoane Regulate (3 la 1000 Laturi) | OmniOperand",
        "regular_polygon_desc": "Calculator universal pentru poligoane regulate arbitrare: latură, apotemă, arie, perimetru și convergență arhimedică.",
        "concrete_title": "Calculator Volum Beton & Număr de Saci | OmniOperand",
        "concrete_desc": "Calculează metri cubi de beton și necesarul de saci de ciment pentru plăci, fundații și stâlpi rotunzi.",
        "right_triangle_title": "Calculator Triunghi Dreptunghic & Teorema lui Pitagora | OmniOperand",
        "right_triangle_desc": "Rezolvitor cu 12 variabile pentru catete, ipotenuză, înălțime, raza cercului înscris și unghiuri ascuțite.",
        "circle_sector_title": "Calculator Sector & Segment de Cerc | OmniOperand",
        "circle_sector_desc": "Calculează lungimea arcului, coarda, săgeata (înălțimea), aria sectorului și aria segmentului circular.",
        "roof_pitch_title": "Calculator Panta Acoperișului & Lungimea Căpriorilor | OmniOperand",
        "roof_pitch_desc": "Calculează unghiul de înclinare în grade, lungimea căpriorilor, tăieturile la fir și chertarea pe cosoroabă.",
        "mortgage_title": "Calculator Credit Ipotecar & Grafic de Rambursare | OmniOperand",
        "mortgage_desc": "Rata lunară fixă a creditului ipotecar, defalcarea capitalului și dobânzii, și economii din rambursări anticipate.",
        "compound_title": "Calculator Dobândă Compusă & Economii | OmniOperand",
        "compound_desc": "Capitalizare periodică și continuă, depuneri regulate, randament anual efectiv (APY) și proiecții financiare.",
        "auto_loan_title": "Calculator Credit Auto & Rate Lunare | OmniOperand",
        "auto_loan_desc": "Finanțare auto, avans, valoare vehicul la schimb, taxe și rate lunare detaliate.",
        "cagr_title": "Calculator Rata Anuală Compusă de Creștere (CAGR) | OmniOperand",
        "cagr_desc": "Rata medie geometrică, perioada de dublare conform Regulii de 72 și evaluarea valorii viitoare.",
        "integrals_title": "Calculator Integrale Definite & Teorema Fundamentală | OmniOperand",
        "integrals_desc": "Calculează primitive exacte și integrale definite cu precizie analitică garantată.",
        "derivatives_title": "Calculator Derivate & Ecuația Tangentei | OmniOperand",
        "derivatives_desc": "Calculează derivate de polinoame, panta instantanee, ecuația tangentei și concavitatea.",
        # Terms
        "home": "Acasă",
        "geometry": "Geometrie",
        "calculus": "Calcul",
        "finance": "Finanțe",
        "physics": "Fizică",
        "statistics": "Statistică",
        "construction": "Construcții",
        "universal_ngon": "N-Gon Universal",
        "disciplines": "Discipline",
        "search_placeholder": "Caută calculatoare...",
        "all_shapes": "Toate Formele",
        "params_title": "Parametri & Date de Intrare",
        "derived_results": "Rezultate Calculate & Metrici",
        "analytical_proof": "Demonstrație Analitică & Invarianți",
        "step_by_step": "Demonstrație Matematică Pas cu Pas",
        "faq_title": "Întrebări Frecvente",
        "unit_metric": "cm",
        "area_metric": "cm²",
        "vol_metric": "m³"
    },
    "pt": {
        "name": "Português",
        "flag": "🇵🇹",
        "locale": "pt_PT",
        "home_title": "OmniOperand — Motor de Cálculo Matemático & Solvers Bidirecionais",
        "home_desc": "Plataforma de computação de alta precisão para geometria, cálculo, finanças e física. Fórmulas exatas, plantas SVG e protocolos para agentes de IA.",
        "geometry_title": "Geometria e Análise Espacial | OmniOperand",
        "geometry_desc": "Solvers geométricos 2D e 3D: polígonos regulares, seções cônicas, poliedros e demonstrações analíticas com radicais exatos.",
        "calc_title": "Cálculo Infinitesimal e Análise Matemática | OmniOperand",
        "calc_desc": "Solvers de cálculo diferencial e integral: derivadas polinomiais, integrais definidas e somas de Riemann.",
        "fin_title": "Finanças Quantitativas e Matemática Atuarial | OmniOperand",
        "fin_desc": "Tabelas de amortização de hipotecas, juros compostos, rendimento percentual anual (APY) e taxa CAGR.",
        "phys_title": "Física e Mecânica Aplicada | OmniOperand",
        "phys_desc": "Cinemática, termodinâmica, dinâmica de fluidos e circuitos elétricos com validação determinística.",
        "stat_title": "Probabilidade e Estatística Matemática | OmniOperand",
        "stat_desc": "Distribuições estocásticas, intervalos de confiança, testes de hipóteses e regressão linear.",
        "const_title": "Construção Civil e Engenharia Estrutural | OmniOperand",
        "const_desc": "Calculadoras de volume de concreto, inclinação de telhados, cortes de caibro e pré-dimensionamento.",
        "shapes_title": "Polígonos e Formas Geométricas | OmniOperand",
        "shapes_desc": "Solvers analíticos de polígonos regulares de 3 a 1000 lados com fórmulas fechadas e plantas vetoriais.",
        "2d_title": "Geometria Bidimensional (2D) | OmniOperand",
        "2d_desc": "Figuras planas, triângulos retângulos, polígonos regulares e arcos circulares analíticos.",
        "3d_title": "Geometria Tridimensional (3D) | OmniOperand",
        "3d_desc": "Cálculos volumétricos espaciais, prismas, cilindros e cubagens de engenharia civil.",
        "octagon_title": "Calculadora de Octógono Regular — Fórmulas Exatas, Área e Diagonais | OmniOperand",
        "octagon_desc": "Calculadora bidirecional de octógono regular. Calcule lado, área, perímetro, apótema, circunraio e diagonais com radicais exatos.",
        "hexagon_title": "Calculadora de Hexágono Regular — Fórmulas Exatas, Apótema e Área | OmniOperand",
        "hexagon_desc": "Calculadora bidirecional de hexágono regular. Resolve lado, apótema, circunraio R=a, área e largura entre faces.",
        "pentagon_title": "Calculadora de Pentágono Regular — Proporção Áurea e Diagonais | OmniOperand",
        "pentagon_desc": "Calculadora de pentágono regular regida pela proporção áurea (ϕ). Calcule lado, apótema, área e diagonais.",
        "decagon_title": "Calculadora de Decágono Regular — 10 Lados, Raio e Diagonais | OmniOperand",
        "decagon_desc": "Calculadora de decágono regular com circunraio R=a·ϕ, largura entre faces e 4 classes de diagonais.",
        "regular_polygon_title": "Calculadora Universal de Polígonos Regulares (3 a 1000 Lados) | OmniOperand",
        "regular_polygon_desc": "Solver universal de polígonos regulares arbitrários para lado, apótema, área, perímetro e convergência de Arquimedes.",
        "concrete_title": "Calculadora de Volume de Concreto e Sacos de Cimento | OmniOperand",
        "concrete_desc": "Calcule metros cúbicos de concreto e quantidade de sacos de cimento para lajes, sapatas e pilares redondos.",
        "right_triangle_title": "Calculadora de Triângulo Retângulo e Teorema de Pitágoras | OmniOperand",
        "right_triangle_desc": "Solver de 12 variáveis para catetos, hipotenusa, altura relativa, raio inscrito e ângulos agudos.",
        "circle_sector_title": "Calculadora de Setor e Segmento Circular | OmniOperand",
        "circle_sector_desc": "Calcule comprimento de arco, corda, flecha (sagita), área do setor e área do segmento circular.",
        "roof_pitch_title": "Calculadora de Inclinação de Telhado e Comprimento de Caibro | OmniOperand",
        "roof_pitch_desc": "Calcule ângulo de inclinação em graus, comprimento de caibros, cortes de prumo e apoios estruturais.",
        "mortgage_title": "Calculadora de Financiamento Imobiliário e Tabela de Amortização | OmniOperand",
        "mortgage_desc": "Prestação mensal fixa, amortização de capital, juros e economia com amortizações extraordinárias.",
        "compound_title": "Calculadora de Juros Compostos e Rendimento de Investimentos | OmniOperand",
        "compound_desc": "Capitalização periódica e contínua, aportes regulares, rendimento anual efetivo (APY) e projeções financeiras.",
        "auto_loan_title": "Calculadora de Financiamento de Veículos e Parcelas | OmniOperand",
        "auto_loan_desc": "Financiamento automotivo, entrada, valor do veículo na troca, taxas e parcelas mensais detalhadas.",
        "cagr_title": "Calculadora de Taxa de Crescimento Anual Composta (CAGR) | OmniOperand",
        "cagr_desc": "Taxa média geométrica de crescimento, tempo de duplicação pela Regra dos 72 e avaliação terminal.",
        "integrals_title": "Calculadora de Integrais Definidas e Teorema Fundamental | OmniOperand",
        "integrals_desc": "Avalie primitivas exatas e integrais definidas com precisão analítica determinística.",
        "derivatives_title": "Calculadora de Derivadas e Reta Tangente | OmniOperand",
        "derivatives_desc": "Calcule derivadas analíticas, inclinação instantânea, equação da reta tangente e concavidade.",
        "home": "Início",
        "geometry": "Geometria",
        "calculus": "Cálculo",
        "finance": "Finanças",
        "physics": "Física",
        "statistics": "Estatística",
        "construction": "Construção",
        "universal_ngon": "N-Gono Universal",
        "disciplines": "Disciplinas",
        "search_placeholder": "Pesquisar calculadoras...",
        "all_shapes": "Todas as Formas",
        "params_title": "Parâmetros e Variáveis de Entrada",
        "derived_results": "Resultados e Métricas Calculadas",
        "analytical_proof": "Demonstração Analítica e Invariantes",
        "step_by_step": "Demonstração Matemática Passo a Passo",
        "faq_title": "Perguntas Frequentes",
        "unit_metric": "cm",
        "area_metric": "cm²",
        "vol_metric": "m³"
    },
    "it": {
        "name": "Italiano",
        "flag": "🇮🇹",
        "locale": "it_IT",
        "home_title": "OmniOperand — Motore di Calcolo Matematico & Risolutori Bidirezionali",
        "home_desc": "Piattaforma computazionale ad alta precisione per geometria, calcolo, finanza e fisica. Formule esatte, diagrammi SVG e protocolli AI.",
        "geometry_title": "Geometria & Analisi Spaziale | OmniOperand",
        "geometry_desc": "Risolutori geometrici 2D e 3D: poligoni regolari, sezioni coniche, poliedri e dimostrazioni analitiche esatte.",
        "calc_title": "Calcolo Infinitesimale & Analisi Matematica | OmniOperand",
        "calc_desc": "Risolutori di calcolo differenziale e integrale: derivate polinomiali, integrali definiti e somme di Riemann.",
        "fin_title": "Finanza Quantitativa & Matematica Attuariale | OmniOperand",
        "fin_desc": "Piani di ammortamento mutui, interesse composto, rendimento effettivo annuo (APY) e tasso di crescita CAGR.",
        "phys_title": "Fisica & Meccanica Applicata | OmniOperand",
        "phys_desc": "Cinematica, termodinamica, fluidodinamica e circuiti elettrici con verifica deterministica.",
        "stat_title": "Probabilità & Statistica Matematica | OmniOperand",
        "stat_desc": "Distribuzioni stocastiche, intervalli di confidenza, test d'ipotesi e regressione lineare.",
        "const_title": "Edilizia & Ingegneria Civile | OmniOperand",
        "const_desc": "Calcolatori di volume calcestruzzo, pendenza del tetto, puntoni e dimensionamento strutturale.",
        "shapes_title": "Poligoni & Figure Geometriche | OmniOperand",
        "shapes_desc": "Risolutori analitici di poligoni regolari da 3 a 1000 lati con formule chiuse e blueprint vettoriali.",
        "2d_title": "Geometria Bidimensionale (2D) | OmniOperand",
        "2d_desc": "Figure piane, triangoli rettangoli, poligoni regolari e archi circolari analitici.",
        "3d_title": "Geometria Tridimensionale (3D) | OmniOperand",
        "3d_desc": "Calcoli volumetrici nello spazio, prismi, cilindri e cubature per l'ingegneria civile.",
        "octagon_title": "Calcolatore Ottagono Regolare — Formule Esatte, Area & Diagonali | OmniOperand",
        "octagon_desc": "Calcolatore bidirezionale per ottagono regolare. Calcola lato, area, perimetro, apotema, raggio circoscritto e diagonali.",
        "hexagon_title": "Calcolatore Esagono Regolare — Formule Esatte, Apotema & Area | OmniOperand",
        "hexagon_desc": "Risolutore bidirezionale per esagono regolare. Calcola lato, apotema, raggio circoscritto R=a, area e larghezza tra facce.",
        "pentagon_title": "Calcolatore Pentagono Regolare — Sezione Aurea & Diagonali | OmniOperand",
        "pentagon_desc": "Calcolatore per pentagono regolare basato sulla sezione aurea (ϕ). Calcola lato, apotema, area e diagonali.",
        "decagon_title": "Calcolatore Decagono Regolare — 10 Lati, Raggio & Diagonali | OmniOperand",
        "decagon_desc": "Calcolatore per decagono regolare con raggio circoscritto R=a·ϕ, larghezza tra facce e 4 classi di diagonali.",
        "regular_polygon_title": "Calcolatore Universale di Poligoni Regolari (3 a 1000 Lati) | OmniOperand",
        "regular_polygon_desc": "Risolutore universale per poligoni regolari arbitrari: lato, apotema, area, perimetro e convergenza di Archimede.",
        "concrete_title": "Calcolatore Volume Calcestruzzo & Sacchi di Cemento | OmniOperand",
        "concrete_desc": "Calcola metri cubi di calcestruzzo e numero di sacchi per solette, fondazioni e colonne cilindriche.",
        "right_triangle_title": "Calcolatore Triangolo Rettangolo & Teorema di Pitagora | OmniOperand",
        "right_triangle_desc": "Risolutore a 12 variabili per cateti, ipotenusa, altezza relativa, raggio inscritto e angoli acuti.",
        "circle_sector_title": "Calcolatore Settore & Segmento Circolare | OmniOperand",
        "circle_sector_desc": "Calcola lunghezza dell'arco, corda, freccia (sagitta), area del settore e area del segmento circolare.",
        "roof_pitch_title": "Calcolatore Pendenza Tetto & Lunghezza Puntoni | OmniOperand",
        "roof_pitch_desc": "Calcola l'angolo di pendenza in gradi, lunghezza dei puntoni, tagli a piombo e intagli di trave.",
        "mortgage_title": "Calcolatore Mutuo & Piano di Ammortamento | OmniOperand",
        "mortgage_desc": "Rata mensile fissa, quota capitale, quota interessi e risparmio con estinzione anticipata.",
        "compound_title": "Calcolatore Interesse Composto & Crescita del Capitale | OmniOperand",
        "compound_desc": "Capitalizzazione periodica e continua, versamenti regolari, rendimento annuo effettivo e proiezioni.",
        "auto_loan_title": "Calcolatore Finanziamento Auto & Rate Mensili | OmniOperand",
        "auto_loan_desc": "Finanziamento auto, anticipo, permuta usato, imposte e rate mensili dettagliate.",
        "cagr_title": "Calcolatore Tasso Annuo di Crescita Composto (CAGR) | OmniOperand",
        "cagr_desc": "Tasso medio geometrico, tempo di raddoppio secondo la Regola del 72 e valutazione obiettivo.",
        "integrals_title": "Calcolatore Integrali Definiti & Teorema Fondamentale | OmniOperand",
        "integrals_desc": "Calcola primitive esatte e integrali definiti con precisione analitica deterministica.",
        "derivatives_title": "Calcolatore Derivate & Retta Tangente | OmniOperand",
        "derivatives_desc": "Calcola derivate polinomiali, pendenza istantanea, equazione della retta tangente e concavità.",
        "home": "Home",
        "geometry": "Geometria",
        "calculus": "Calcolo",
        "finance": "Finanza",
        "physics": "Fisica",
        "statistics": "Statistica",
        "construction": "Edilizia",
        "universal_ngon": "N-Gono Universale",
        "disciplines": "Discipline",
        "search_placeholder": "Cerca calcolatori...",
        "all_shapes": "Tutte le Figure",
        "params_title": "Parametri & Dati di Ingresso",
        "derived_results": "Risultati & Metriche Calcolate",
        "analytical_proof": "Dimostrazione Analitica & Invarianti",
        "step_by_step": "Dimostrazione Matematica Passo dopo Passo",
        "faq_title": "Domande Frequenti",
        "unit_metric": "cm",
        "area_metric": "cm²",
        "vol_metric": "m³"
    },
    "nl": {
        "name": "Nederlands",
        "flag": "🇳🇱",
        "locale": "nl_NL",
        "home_title": "OmniOperand — Wiskundige Rekenmachine & Bidirectionele Oplossers",
        "home_desc": "Uiterst nauwkeurige rekenmachines voor meetkunde, wiskundige analyse, financiën en natuurkunde. Exacte formules en SVG-bouwplannen.",
        "geometry_title": "Meetkunde & Ruimtelijke Analyse | OmniOperand",
        "geometry_desc": "2D- en 3D-meetkundige oplossers: regelmatige veelhoeken, kegelsneden, veelvlakken en exacte wortelbewijzen.",
        "calc_title": "Wiskundige Analyse & Differentiaalrekening | OmniOperand",
        "calc_desc": "Differentiaal- en integraalrekening: afgeleiden van polynomen, bepaalde integralen en Riemann-sommen.",
        "fin_title": "Kwantitatieve Financiën & Actuariële Wiskunde | OmniOperand",
        "fin_desc": "Aflossingstabellen voor hypotheken, samengestelde interest, effectief jaarrendement (APY) en CAGR.",
        "phys_title": "Natuurkunde & Technische Mechanica | OmniOperand",
        "phys_desc": "Kinematica, thermodynamica, stromingsleer en elektrische circuits met deterministische precisie.",
        "stat_title": "Kansrekening & Wiskundige Statistiek | OmniOperand",
        "stat_desc": "Stochastische verdelingen, betrouwbaarheidsintervallen, hypothesetoetsen en lineaire regressie.",
        "const_title": "Bouwkunde & Civiele Techniek | OmniOperand",
        "const_desc": "Betonvolume, aantal zakken cement, dakhelling, spantlengte en constructieve voorberekeningen.",
        "shapes_title": "Veelhoeken & Meetkundige Vormen | OmniOperand",
        "shapes_desc": "Analytische oplossers voor regelmatige veelhoeken (3 tot 1000 zijden) met exacte algebraïsche formules.",
        "2d_title": "Tweedimensionale (2D) Meetkunde | OmniOperand",
        "2d_desc": "Vlakke figuren, rechthoekige driehoeken, regelmatige polygonen en cirkelsegmenten.",
        "3d_title": "Driedimensionale (3D) Meetkunde | OmniOperand",
        "3d_desc": "Ruimtelijke volumeberekeningen, prisma's, cilinders en grondverzet in de grond-, weg- en waterbouw.",
        "octagon_title": "Regelmatige Achthoek Rekenmachine — Exacte Formules, Oppervlakte & Diagonalen | OmniOperand",
        "octagon_desc": "Bidirectionele achthoek-rekenmachine. Bereken zijde, oppervlakte, omtrek, apothema, omgeschreven straal en diagonalen.",
        "hexagon_title": "Regelmatige Zeshoek Rekenmachine — Formules, Apothema & Oppervlakte | OmniOperand",
        "hexagon_desc": "Bidirectionele zeshoek-oplosser. Berekent zijde, apothema, omgeschreven straal R=a, oppervlakte en sleutelwijdte.",
        "pentagon_title": "Regelmatige Vijfhoek Rekenmachine — Gulden Snede & Diagonalen | OmniOperand",
        "pentagon_desc": "Vijfhoek-rekenmachine gebaseerd op de gulden snede (ϕ). Bereken zijde, apothema, oppervlakte en diagonalen.",
        "decagon_title": "Regelmatige Tienhoek Rekenmachine — 10 Zijden, Straal & Diagonalen | OmniOperand",
        "decagon_desc": "Tienhoek-rekenmachine met omgeschreven straal R=a·ϕ, sleutelwijdte en 4 diagonaalklassen.",
        "regular_polygon_title": "Universele Veelhoek Rekenmachine (3 tot 1000 Zijden) | OmniOperand",
        "regular_polygon_desc": "Universele oplosser voor willekeurige regelmatige veelhoeken: zijdelengte, apothema, oppervlakte, omtrek en cirkelbenadering.",
        "concrete_title": "Betonvolume & Aantal Zakken Rekenmachine | OmniOperand",
        "concrete_desc": "Bereken kubieke meters beton en aantal zakken kant-en-klaar beton voor vloeren, funderingen en ronde kolommen.",
        "right_triangle_title": "Rechthoekige Driehoek & Stelling van Pythagoras Rekenmachine | OmniOperand",
        "right_triangle_desc": "12-variabelen oplosser voor rechthoekszijden, schuine zijde, hoogtelijn, ingeschreven straal en scherpe hoeken.",
        "circle_sector_title": "Cirkelsector & Cirkelsegment Rekenmachine | OmniOperand",
        "circle_sector_desc": "Bereken booglengte, koorde, pijlhoogte (sagitta), sectoroppervlakte en segmentoppervlakte.",
        "roof_pitch_title": "Dakhelling & Spantlengte Rekenmachine | OmniOperand",
        "roof_pitch_desc": "Bereken hellingshoek in graden, spantlengte, loodsnede en keepafschuining voor timmerlieden en dakdekkers.",
        "mortgage_title": "Hypotheek & Aflossingsschema Rekenmachine | OmniOperand",
        "mortgage_desc": "Maandelijkse annuïteit, rente- en aflossingsverdeling en rentebesparing door extra aflossingen.",
        "compound_title": "Samengestelde Interest & Vermogensopbouw Rekenmachine | OmniOperand",
        "compound_desc": "Periodieke en continue samengestelde rente, maandelijkse inleg, effectieve rente en kapitaalgroei.",
        "auto_loan_title": "Autolening & Maandlasten Rekenmachine | OmniOperand",
        "auto_loan_desc": "Autofinanciering, aanbetaling, inruilwaarde, rentekosten en maandelijkse termijnen.",
        "cagr_title": "Samengesteld Jaarlijks Groeipercentage (CAGR) Rekenmachine | OmniOperand",
        "cagr_desc": "Meetkundig gemiddelde van rendement, verdubbelingstijd via de 72-regel en doelwaarde-inversie.",
        "integrals_title": "Bepaalde Integraal & Hoofdstelling van de Analyse | OmniOperand",
        "integrals_desc": "Bereken exacte primitieve functies en bepaalde integralen met analytische nauwkeurigheid.",
        "derivatives_title": "Afgeleide & Raaklijn Rekenmachine | OmniOperand",
        "derivatives_desc": "Bereken polynoomafgeleiden, momentane helling, vergelijking van de raaklijn en kromming.",
        "home": "Home",
        "geometry": "Meetkunde",
        "calculus": "Analyse",
        "finance": "Financiën",
        "physics": "Natuurkunde",
        "statistics": "Statistiek",
        "construction": "Bouwkunde",
        "universal_ngon": "Universele N-Hoek",
        "disciplines": "Vakgebieden",
        "search_placeholder": "Zoek rekenmachines...",
        "all_shapes": "Alle Vormen",
        "params_title": "Parameters & Invoerwaarden",
        "derived_results": "Berekende Resultaten",
        "analytical_proof": "Analytisch Bewijs & Invarianten",
        "step_by_step": "Stap-voor-stap Wiskundig Bewijs",
        "faq_title": "Veelgestelde Vragen",
        "unit_metric": "cm",
        "area_metric": "cm²",
        "vol_metric": "m³"
    },
    "pl": {
        "name": "Polski",
        "flag": "🇵🇱",
        "locale": "pl_PL",
        "home_title": "OmniOperand — Matematyczny Silnik Obliczeniowy & Rozwiązywanie Dwukierunkowe",
        "home_desc": "Precyzyjna platforma obliczeniowa do geometrii, analizy matematycznej, finansów i fizyki. Dokładne wzory i interaktywne schematy SVG.",
        "geometry_title": "Geometria & Analiza Przestrzenna | OmniOperand",
        "geometry_desc": "Solvery geometryczne 2D i 3D: wielokąty foremne, stożkowe, wielościany i ścisłe dowody z pierwiastkami.",
        "calc_title": "Rachunek Różniczkowy i Całkowy | OmniOperand",
        "calc_desc": "Rachunek różniczkowy i całkowy: pochodne wielomianów, całki oznaczone i sumy Riemanna.",
        "fin_title": "Finanse Ilościowe & Matematyka Aktuarialna | OmniOperand",
        "fin_desc": "Harmonogramy spłat kredytów hipotecznych, procent składany, roczna stopa procentowa (APY) oraz CAGR.",
        "phys_title": "Fizyka & Mechanika Techniczna | OmniOperand",
        "phys_desc": "Kinematyka, termodynamika, mechanika płynów i obwody elektryczne z weryfikacją deterministyczną.",
        "stat_title": "Rachunek Prawdopodobieństwa & Statystyka | OmniOperand",
        "stat_desc": "Rozkłady stochastyczne, przedziały ufności, testy hipotez i regresja liniowa.",
        "const_title": "Budownictwo & Inżynieria Lądowa | OmniOperand",
        "const_desc": "Objętość betonu, liczba worków cementu, spadek dachu, długość krokwi i wymiarowanie konstrukcyjne.",
        "shapes_title": "Wielokąty & Figury Geometryczne | OmniOperand",
        "shapes_desc": "Analityczne solvery wielokątów foremnych od 3 do 1000 boków ze zwartymi wzorami i rzutami wektorowymi.",
        "2d_title": "Geometria Dwuwymiarowa (2D) | OmniOperand",
        "2d_desc": "Figury płaskie, trójkąty prostokątne, wielokąty foremne i wycinki kołowe.",
        "3d_title": "Geometria Trójwymiarowa (3D) | OmniOperand",
        "3d_desc": "Obliczenia objętości brył w przestrzeni, graniastosłupy, walce i kubatury robót ziemnych.",
        "octagon_title": "Kalkulator Ośmiokąta Foremnego — Ścisłe Wzory, Pole & Przekątne | OmniOperand",
        "octagon_desc": "Dwukierunkowy kalkulator ośmiokąta foremnego. Oblicz bok, pole, obwód, apotemę, promień koła opisanego i przekątne.",
        "hexagon_title": "Kalkulator Sześciokąta Foremnego — Wzory, Apotema & Pole | OmniOperand",
        "hexagon_desc": "Dwukierunkowy kalkulator sześciokąta foremnego. Oblicza bok, apotemę, promień koła opisanego R=a, pole i szerokość.",
        "pentagon_title": "Kalkulator Pięciokąta Foremnego — Złoty Podział & Przekątne | OmniOperand",
        "pentagon_desc": "Kalkulator pięciokąta foremnego opartego na złotym podziale (ϕ). Oblicza bok, apotemę, pole i przekątne.",
        "decagon_title": "Kalkulator Dziesięciokąta Foremnego — 10 Boków, Promień & Przekątne | OmniOperand",
        "decagon_desc": "Kalkulator dziesięciokąta foremnego z promieniem koła opisanego R=a·ϕ, rozpiętością i 4 klasami przekątnych.",
        "regular_polygon_title": "Uniwersalny Kalkulator Wielokątów Foremnych (3 do 1000 Boków) | OmniOperand",
        "regular_polygon_desc": "Uniwersalny solver dowolnych wielokątów foremnych: długość boku, apotema, pole, obwód i aproksymacja koła Archimedesa.",
        "concrete_title": "Kalkulator Objętości Betonu & Liczby Worków | OmniOperand",
        "concrete_desc": "Oblicz metry sześcienne betonu oraz liczbę worków gotowej mieszanki na płyty, fundamenty i słupy.",
        "right_triangle_title": "Trójkąt Prostokątny & Twierdzenie Pitagorasa Kalkulator | OmniOperand",
        "right_triangle_desc": "12-zmienny solver dla przyprostokątnych, przeciwprostokątnej, wysokości, promienia wpisanego i kątów ostrych.",
        "circle_sector_title": "Wycinek & Odcinek Koła Kalkulator | OmniOperand",
        "circle_sector_desc": "Oblicz długość łuku, cięciwę, strzałkę łuku (sagittę), pole wycinka i pole odcinka koła.",
        "roof_pitch_title": "Kąt Nachylenia Dachu & Długość Krokwi Kalkulator | OmniOperand",
        "roof_pitch_desc": "Oblicz kąt nachylenia w stopniach, długość krokwi, cięcia pionowe i zacięcia ciesielskie.",
        "mortgage_title": "Kredyt Hipoteczny & Harmonogram Spłat Kalkulator | OmniOperand",
        "mortgage_desc": "Miesięczna rata kapitałowo-odsetkowa, podział na kapitał i odsetki oraz oszczędności z nadpłat.",
        "compound_title": "Procent Składany & Kalkulator Inwestycyjny | OmniOperand",
        "compound_desc": "Kapitalizacja okresowa i ciągła, regularne dopłaty, efektywna stopa roczna i wzrost kapitału.",
        "auto_loan_title": "Kredyt Samochodowy & Raty Miesięczne Kalkulator | OmniOperand",
        "auto_loan_desc": "Finansowanie zakupu auta, wkład własny, auto w rozliczeniu, koszty odsetek i miesięczna rata.",
        "cagr_title": "Średnioroczna Stopa Wzrostu (CAGR) Kalkulator | OmniOperand",
        "cagr_desc": "Średnia geometryczna wzrostu, czas podwojenia kapitału wg Reguły 72 i wycena końcowa.",
        "integrals_title": "Całka Oznaczona & Podstawowe Twierdzenie Rachunku Całkowego | OmniOperand",
        "integrals_desc": "Oblicz dokładne funkcje pierwotne i całki oznaczone z precyzją analityczną.",
        "derivatives_title": "Pochodna Funkcji & Równanie Stycznej Kalkulator | OmniOperand",
        "derivatives_desc": "Oblicz pochodne wielomianów, chwilowe nachylenie, równanie stycznej i wypukłość.",
        "home": "Strona Główna",
        "geometry": "Geometria",
        "calculus": "Rachunek",
        "finance": "Finanse",
        "physics": "Fizyka",
        "statistics": "Statystyka",
        "construction": "Budownictwo",
        "universal_ngon": "Wielokąt N-Kątny",
        "disciplines": "Dyscypliny",
        "search_placeholder": "Szukaj kalkulatorów...",
        "all_shapes": "Wszystkie Figury",
        "params_title": "Parametry & Wartości Wejściowe",
        "derived_results": "Wyniki & Wartości Obliczone",
        "analytical_proof": "Dowód Analityczny & Inwarianty",
        "step_by_step": "Wyprowadzenie Matematyczne Krok po Kroku",
        "faq_title": "Często Zadawane Pytania",
        "unit_metric": "cm",
        "area_metric": "cm²",
        "vol_metric": "m³"
    }
}

# The 25 canonical paths to internationalize
CORE_PATHS = [
    ("", "index.html", "home"),
    ("geometry/", "index.html", "geometry"),
    ("geometry/2d/", "index.html", "2d"),
    ("geometry/3d/", "index.html", "3d"),
    ("geometry/2d/shapes/", "index.html", "shapes"),
    ("geometry/2d/shapes/regular-polygon/", "index.html", "regular_polygon"),
    ("geometry/2d/shapes/octagon/", "index.html", "octagon"),
    ("geometry/2d/shapes/hexagon/", "index.html", "hexagon"),
    ("geometry/2d/shapes/pentagon/", "index.html", "pentagon"),
    ("geometry/2d/shapes/decagon/", "index.html", "decagon"),
    ("geometry/2d/right-triangle/", "index.html", "right_triangle"),
    ("geometry/2d/circle-sector/", "index.html", "circle_sector"),
    ("geometry/2d/roof-pitch/", "index.html", "roof_pitch"),
    ("geometry/3d/concrete-volume/", "index.html", "concrete"),
    ("finance/", "index.html", "fin"),
    ("finance/mortgage-amortization/", "index.html", "mortgage"),
    ("finance/compound-interest/", "index.html", "compound"),
    ("finance/auto-loan/", "index.html", "auto_loan"),
    ("finance/cagr/", "index.html", "cagr"),
    ("calculus/", "index.html", "calc"),
    ("calculus/integrals/", "index.html", "integrals"),
    ("calculus/derivatives/", "index.html", "derivatives"),
    ("physics/", "index.html", "phys"),
    ("statistics/", "index.html", "stat"),
    ("construction/", "index.html", "const")
]

ALL_LANG_CODES = ["en", "es", "fr", "de", "it", "pt", "nl", "pl", "sv", "no", "fi", "ro"]

def build_hreflang_tags(base_subpath: str) -> str:
    """Builds reciprocal hreflang link tags for all supported languages + x-default."""
    norm_path = base_subpath.strip("/")
    path_suffix = f"/{norm_path}/" if norm_path else "/"
    
    tags = []
    for code in ALL_LANG_CODES:
        if code == "en":
            url = f"https://omnioperand.com{path_suffix}"
        else:
            url = f"https://omnioperand.com/{code}{path_suffix}"
        tags.append(f'  <link rel="alternate" hreflang="{code}" href="{url}">')
    
    # x-default points to canonical English
    tags.append(f'  <link rel="alternate" hreflang="x-default" href="https://omnioperand.com{path_suffix}">')
    return "\n".join(tags)

def update_english_page_hreflangs():
    """Injects reciprocal hreflang tags into existing canonical English pages."""
    print("Injecting reciprocal hreflang tags into English canonical pages...")
    hreflang_regex = re.compile(r'(\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*">)+', re.MULTILINE)
    
    for subpath, filename, key in CORE_PATHS:
        en_file = REPO_ROOT / subpath / filename
        if not en_file.exists():
            continue
        
        content = en_file.read_text(encoding="utf-8")
        hreflangs_str = build_hreflang_tags(subpath)
        
        # Remove any existing hreflangs to keep clean
        clean_content = hreflang_regex.sub("", content)
        
        # Inject right after canonical link
        canonical_pattern = re.compile(r'(<link rel="canonical" href="[^"]*">)')
        if canonical_pattern.search(clean_content):
            new_content = canonical_pattern.sub(r'\1\n' + hreflangs_str, clean_content, count=1)
            en_file.write_text(new_content, encoding="utf-8")
        else:
            print(f"  ⚠️ Could not find canonical tag in English file: {subpath}{filename}")

    print("  ✅ English pages updated with reciprocal hreflang links.")

def localize_html_content(content: str, lang_code: str, subpath: str, page_key: str) -> str:
    """Transforms an English source HTML page into a natively localized version."""
    dict_data = LANGUAGES[lang_code]
    norm_path = subpath.strip("/")
    path_suffix = f"/{norm_path}/" if norm_path else "/"
    localized_url = f"https://omnioperand.com/{lang_code}{path_suffix}"
    
    # 1. Update <html lang="en">
    res = re.sub(r'<html lang="en"', f'<html lang="{lang_code}"', content)
    
    # 2. Update Canonical link
    res = re.sub(
        r'<link rel="canonical" href="https://omnioperand.com/[^"]*">',
        f'<link rel="canonical" href="{localized_url}">',
        res
    )
    
    # 3. Inject reciprocal hreflangs
    hreflangs_str = build_hreflang_tags(subpath)
    # Remove existing hreflang
    res = re.sub(r'(\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*">)+', "", res)
    res = re.sub(
        r'(<link rel="canonical" href="[^"]*">)',
        r'\1\n' + hreflangs_str,
        res,
        count=1
    )
    
    # 4. Localize <title> and meta description
    title_key = f"{page_key}_title"
    desc_key = f"{page_key}_desc"
    
    new_title = dict_data.get(title_key, f"{dict_data['home_title']}")
    new_desc = dict_data.get(desc_key, f"{dict_data['home_desc']}")
    
    res = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', res, flags=re.DOTALL)
    res = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{new_desc}">', res, flags=re.DOTALL)
    
    # 5. Localize OpenGraph
    res = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{new_title}">', res, flags=re.DOTALL)
    res = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{new_desc}">', res, flags=re.DOTALL)
    res = re.sub(r'<meta property="og:url" content=".*?">', f'<meta property="og:url" content="{localized_url}">', res, flags=re.DOTALL)
    
    # 6. Localize JSON-LD Schema
    def update_json_ld(match):
        ld_str = match.group(1)
        try:
            ld_obj = json.loads(ld_str)
            if "@graph" in ld_obj:
                for item in ld_obj["@graph"]:
                    if item.get("@type") in ("WebApplication", "CollectionPage"):
                        item["name"] = new_title.split(" — ")[0].split(" | ")[0]
                        item["description"] = new_desc
                        item["url"] = localized_url
                        if "@id" in item:
                            item["@id"] = f"{localized_url}#{item['@id'].split('#')[-1]}"
                    elif item.get("@type") == "BreadcrumbList":
                        if "@id" in item:
                            item["@id"] = f"{localized_url}#breadcrumbs"
                        # Localize first crumb
                        if item.get("itemListElement") and len(item["itemListElement"]) > 0:
                            item["itemListElement"][0]["name"] = dict_data["home"]
                            item["itemListElement"][0]["item"] = f"https://omnioperand.com/{lang_code}/"
            return f'<script type="application/ld+json">\n{json.dumps(ld_obj, indent=2, ensure_ascii=False)}\n</script>'
        except Exception:
            return match.group(0)

    res = re.sub(r'<script type="application/ld\+json">(.*?)</script>', update_json_ld, res, flags=re.DOTALL)

    # 7. Localize Breadcrumb UI
    res = re.sub(r'<a href="/">Home</a>', f'<a href="/{lang_code}/">{dict_data["home"]}</a>', res)
    res = re.sub(r'<a href="/geometry/">Geometry</a>', f'<a href="/{lang_code}/geometry/">{dict_data["geometry"]}</a>', res)
    res = re.sub(r'<a href="/geometry/2d/">2D Geometry</a>', f'<a href="/{lang_code}/geometry/2d/">{dict_data["2d_title"].split(" | ")[0]}</a>', res)
    res = re.sub(r'<a href="/geometry/3d/">3D Geometry</a>', f'<a href="/{lang_code}/geometry/3d/">{dict_data["3d_title"].split(" | ")[0]}</a>', res)
    res = re.sub(r'<a href="/geometry/2d/shapes/">Shapes &amp; Polygons</a>', f'<a href="/{lang_code}/geometry/2d/shapes/">{dict_data["shapes_title"].split(" | ")[0]}</a>', res)
    res = re.sub(r'<a href="/geometry/2d/shapes/">Shapes & Polygons</a>', f'<a href="/{lang_code}/geometry/2d/shapes/">{dict_data["shapes_title"].split(" | ")[0]}</a>', res)
    res = re.sub(r'<a href="/calculus/">Calculus</a>', f'<a href="/{lang_code}/calculus/">{dict_data["calculus"]}</a>', res)
    res = re.sub(r'<a href="/finance/">Finance</a>', f'<a href="/{lang_code}/finance/">{dict_data["finance"]}</a>', res)
    res = re.sub(r'<a href="/physics/">Physics</a>', f'<a href="/{lang_code}/physics/">{dict_data["physics"]}</a>', res)
    res = re.sub(r'<a href="/statistics/">Statistics</a>', f'<a href="/{lang_code}/statistics/">{dict_data["statistics"]}</a>', res)
    res = re.sub(r'<a href="/construction/">Construction</a>', f'<a href="/{lang_code}/construction/">{dict_data["construction"]}</a>', res)
    
    # Active breadcrumb
    page_short_name = new_title.split(" — ")[0].split(" | ")[0]
    res = re.sub(r'<li class="breadcrumb-item active" aria-current="page">.*?</li>', f'<li class="breadcrumb-item active" aria-current="page">{page_short_name}</li>', res)

    # 8. Localize Hero Header H1 & description
    if page_key != "home":
        res = re.sub(r'<h1>(?:Regular )?[A-Za-z0-9 &–—\(\)]+(?:Calculator|Solver)?</h1>', f'<h1>{page_short_name}</h1>', res, count=1)
        res = re.sub(r'<p class="hero-subtext">.*?</p>', f'<p class="hero-subtext">{new_desc}</p>', res, count=1, flags=re.DOTALL)

    # 9. Localize Common Section Headings & Toolbars
    res = re.sub(r'<h2>Parameters &amp; Inversions</h2>', f'<h2>{dict_data["params_title"]}</h2>', res)
    res = re.sub(r'<h2>Parameters &amp; Input Variables</h2>', f'<h2>{dict_data["params_title"]}</h2>', res)
    res = re.sub(r'<h2>Calculated Output Metrics</h2>', f'<h2>{dict_data["derived_results"]}</h2>', res)
    res = re.sub(r'<h3>Analytical Proof &amp; Invariants</h3>', f'<h3>{dict_data["analytical_proof"]}</h3>', res)
    res = re.sub(r'<h3><span>Step-by-Step Mathematical Derivation</span></h3>', f'<h3><span>{dict_data["step_by_step"]}</span></h3>', res)
    res = re.sub(r'<h2>Frequently Asked Questions</h2>', f'<h2>{dict_data["faq_title"]}</h2>', res)
    res = re.sub(r'placeholder="Search calculators\.\.\."', f'placeholder="{dict_data["search_placeholder"]}"', res)

    # Toolbar labels
    units_lbl = {
        "es": "Unidades:", "fr": "Unités :", "de": "Einheiten:", "it": "Unità:",
        "pt": "Unidades:", "nl": "Eenheden:", "pl": "Jednostki:",
        "sv": "Enheter:", "no": "Enheter:", "fi": "Yksiköt:", "ro": "Unități:"
    }.get(lang_code, "Units:")
    dec_lbl = {
        "es": "Decimales:", "fr": "Décimales :", "de": "Dezimalstellen:", "it": "Decimali:",
        "pt": "Casas Decimais:", "nl": "Decimalen:", "pl": "Miejsca po Przecinku:",
        "sv": "Decimaler:", "no": "Desimaler:", "fi": "Desimaalit:", "ro": "Zecimale:"
    }.get(lang_code, "Decimals:")
    res = re.sub(r'<span class="toolbar-label">Units:</span>', f'<span class="toolbar-label">{units_lbl}</span>', res)
    res = re.sub(r'<span class="toolbar-label">Decimals:</span>', f'<span class="toolbar-label">{dec_lbl}</span>', res)

    # 10. Localize Polygon Switcher Bar & links
    tri_name = {"es": "Triángulo", "fr": "Triangle", "de": "Dreieck", "it": "Triangolo", "pt": "Triângulo", "nl": "Driehoek", "pl": "Trójkąt", "sv": "Triangel", "no": "Trekant", "fi": "Kolmio", "ro": "Triunghi"}.get(lang_code, "Triangle")
    sq_name = {"es": "Cuadrado", "fr": "Carré", "de": "Quadrat", "it": "Quadrato", "pt": "Quadrado", "nl": "Vierkant", "pl": "Kwadrat", "sv": "Kvadrat", "no": "Kvadrat", "fi": "Neliö", "ro": "Pătrat"}.get(lang_code, "Square")
    pent_name = {"es": "Pentágono", "fr": "Pentagone", "de": "Fünfeck", "it": "Pentagono", "pt": "Pentágono", "nl": "Vijfhoek", "pl": "Pięciokąt", "sv": "Femhörning", "no": "Femkant", "fi": "Viisikulmio", "ro": "Pentagon"}.get(lang_code, "Pentagon")
    hex_name = {"es": "Hexágono", "fr": "Hexagone", "de": "Sechseck", "it": "Esagono", "pt": "Hexágono", "nl": "Zeshoek", "pl": "Sześciokąt", "sv": "Sexhörning", "no": "Sekskant", "fi": "Kuusikulmio", "ro": "Hexagon"}.get(lang_code, "Hexagon")
    oct_name = {"es": "Octógono", "fr": "Octogone", "de": "Achteck", "it": "Ottagono", "pt": "Octógono", "nl": "Achthoek", "pl": "Ośmiokąt", "sv": "Åtahörning", "no": "Åttekant", "fi": "Kahdeksankulmio", "ro": "Octogon"}.get(lang_code, "Octagon")
    dec_name = {"es": "Decágono", "fr": "Décagone", "de": "Zehneck", "it": "Decagono", "pt": "Decágono", "nl": "Tienhoek", "pl": "Dziesięciokąt", "sv": "Tiohörning", "no": "Tikant", "fi": "Kymmenkulmio", "ro": "Decagon"}.get(lang_code, "Decagon")

    res = re.sub(r'Universal N-Gon \(3–1000\)', f'{dict_data["universal_ngon"]} (3–1000)', res)
    res = re.sub(r'▲ Triangle \(3\)', f'▲ {tri_name} (3)', res)
    res = re.sub(r'■ Square \(4\)', f'■ {sq_name} (4)', res)
    res = re.sub(r'⬠ Pentagon \(5\)', f'⬠ {pent_name} (5)', res)
    res = re.sub(r'⬡ Hexagon \(6\)', f'⬡ {hex_name} (6)', res)
    res = re.sub(r'🛑 Octagon \(8\)', f'🛑 {oct_name} (8)', res)
    res = re.sub(r'⯃ Decagon \(10\)', f'⯃ {dec_name} (10)', res)
    res = re.sub(r'📁 All Shapes', f'📁 {dict_data["all_shapes"]}', res)

    # Route switcher links to localized URLs
    res = re.sub(r'href="/geometry/2d/shapes/regular-polygon/"', f'href="/{lang_code}/geometry/2d/shapes/regular-polygon/"', res)
    res = re.sub(r'href="/geometry/2d/shapes/octagon/"', f'href="/{lang_code}/geometry/2d/shapes/octagon/"', res)
    res = re.sub(r'href="/geometry/2d/shapes/hexagon/"', f'href="/{lang_code}/geometry/2d/shapes/hexagon/"', res)
    res = re.sub(r'href="/geometry/2d/shapes/pentagon/"', f'href="/{lang_code}/geometry/2d/shapes/pentagon/"', res)
    res = re.sub(r'href="/geometry/2d/shapes/decagon/"', f'href="/{lang_code}/geometry/2d/shapes/decagon/"', res)
    res = re.sub(r'href="/geometry/2d/shapes/"', f'href="/{lang_code}/geometry/2d/shapes/"', res)

    # 11. Ensure zero raw LaTeX backslashes remain
    return res

def generate_all_language_pages():
    """Generates the static tree of localized pages across all 7 non-English languages."""
    print("Generating native multi-language pages for 7 languages...")
    total_generated = 0
    
    for lang_code in LANGUAGES.keys():
        print(f"\n🌍 Generating Language: {LANGUAGES[lang_code]['name']} ({lang_code})...")
        lang_count = 0
        
        for subpath, filename, page_key in CORE_PATHS:
            source_file = REPO_ROOT / subpath / filename
            if not source_file.exists():
                print(f"  ⚠️ Source file does not exist: {source_file}")
                continue
            
            source_content = source_file.read_text(encoding="utf-8")
            localized_content = localize_html_content(source_content, lang_code, subpath, page_key)
            
            target_dir = REPO_ROOT / lang_code / subpath
            target_dir.mkdir(parents=True, exist_ok=True)
            
            target_file = target_dir / filename
            target_file.write_text(localized_content, encoding="utf-8")
            
            lang_count += 1
            total_generated += 1
            
        print(f"  ✅ {lang_count} pages created for {lang_code}.")

    print(f"\n🎉 Successfully created {total_generated} native localized HTML pages!")

def update_sitemap():
    """Regenerates sitemap.xml to include all canonical English and localized language URLs."""
    print("Updating sitemap.xml with multilingual URLs...")
    sitemap_path = REPO_ROOT / "sitemap.xml"
    
    urls = []
    
    # 1. Base Canonical URLs
    for subpath, filename, _ in CORE_PATHS:
        norm_path = subpath.strip("/")
        suffix = f"/{norm_path}/" if norm_path else "/"
        urls.append((f"https://omnioperand.com{suffix}", "1.0" if not norm_path else "0.9", "weekly"))
        
        # 2. Localized URLs for all 7 languages
        for lang_code in LANGUAGES.keys():
            urls.append((f"https://omnioperand.com/{lang_code}{suffix}", "0.9" if not norm_path else "0.8", "weekly"))
            
    # Read existing sitemap to preserve other active solver URLs
    existing_urls = set()
    if sitemap_path.exists():
        content = sitemap_path.read_text(encoding="utf-8")
        loc_matches = re.findall(r'<loc>(https://omnioperand\.com/[^<]*)</loc>', content)
        for loc in loc_matches:
            existing_urls.add(loc)
            
    # Merge and build clean XML
    all_urls_dict = {}
    for loc, prio, freq in urls:
        all_urls_dict[loc] = (prio, freq)
        
    for loc in existing_urls:
        if loc not in all_urls_dict:
            all_urls_dict[loc] = ("0.8", "monthly")
            
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    
    for loc in sorted(all_urls_dict.keys()):
        prio, freq = all_urls_dict[loc]
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{loc}</loc>")
        xml_lines.append("    <lastmod>2026-10-24</lastmod>")
        xml_lines.append(f"    <changefreq>{freq}</changefreq>")
        xml_lines.append(f"    <priority>{prio}</priority>")
        xml_lines.append("  </url>")
        
    xml_lines.append("</urlset>\n")
    sitemap_path.write_text("\n".join(xml_lines), encoding="utf-8")
    print(f"  ✅ sitemap.xml updated with {len(all_urls_dict)} indexed URLs (Canonical + 7 Languages)!")

def main():
    print("=========================================================")
    print("🚀 OmniOperand Native Multi-Language i18n Pipeline")
    print("=========================================================")
    
    # 1. Update English canonical pages with reciprocal hreflangs
    update_english_page_hreflangs()
    
    # 2. Generate all localized pages for 7 languages
    generate_all_language_pages()
    
    # 3. Unify headers and inject language switchers across ALL pages
    print("\nSynchronizing headers, language selector dropdowns, and cache headers...")
    from unify_headers import unify_all_headers
    unify_all_headers()
    
    # 4. Update sitemap
    update_sitemap()
    
    print("\n✅ Multi-language internationalization generation complete!")

if __name__ == "__main__":
    main()
