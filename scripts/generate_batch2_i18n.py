#!/usr/bin/env python3
"""
scripts/generate_batch2_i18n.py — Generates Batch 2 Native Localized Solvers for OmniOperand
Batch 2 covers the remaining 19 Universal Geometry & Statistics Solvers:
- 15 Geometry: ellipse, trapezoid, rhombus, parallelogram, kite, cylinder, cone, sphere, torus,
  triangular-prism, pyramid, frustum-cone, frustum-pyramid, ellipsoid, arc-length
- 4 Statistics: standard-deviation, z-score, permutations-combinations, bayes-theorem

Total new localized pages = 19 solvers × 11 languages = 209 pages.
"""

import sys
import re
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

LANGUAGES = {
    "es": {
        "name": "Español", "flag": "🇪🇸", "locale": "es_ES",
        "home": "Inicio", "geometry": "Geometría", "statistics": "Estadística",
        "search_placeholder": "Buscar calculadoras...",
        "params_title": "Parámetros y Entradas",
        "derived_results": "Métricas y Resultados Calculados",
        "step_by_step": "Demostración Matemática Paso a Paso",
        "faq_title": "Preguntas Frecuentes",
    },
    "fr": {
        "name": "Français", "flag": "🇫🇷", "locale": "fr_FR",
        "home": "Accueil", "geometry": "Géométrie", "statistics": "Statistique",
        "search_placeholder": "Rechercher des calculateurs...",
        "params_title": "Paramètres & Variables",
        "derived_results": "Métriques & Résultats Calculés",
        "step_by_step": "Démonstration Mathématique Étape par Étape",
        "faq_title": "Foire Aux Questions",
    },
    "de": {
        "name": "Deutsch", "flag": "🇩🇪", "locale": "de_DE",
        "home": "Startseite", "geometry": "Geometrie", "statistics": "Statistik",
        "search_placeholder": "Rechner suchen...",
        "params_title": "Parameter & Eingabewerte",
        "derived_results": "Berechnete Ausgabewerte",
        "step_by_step": "Schritt-für-Schritt Herleitung",
        "faq_title": "Häufig Gestellte Fragen",
    },
    "it": {
        "name": "Italiano", "flag": "🇮🇹", "locale": "it_IT",
        "home": "Home", "geometry": "Geometria", "statistics": "Statistica",
        "search_placeholder": "Cerca calcolatori...",
        "params_title": "Parametri & Dati di Ingresso",
        "derived_results": "Risultati & Metriche Calcolate",
        "step_by_step": "Dimostrazione Matematica Passo dopo Passo",
        "faq_title": "Domande Frequenti",
    },
    "pt": {
        "name": "Português", "flag": "🇵🇹", "locale": "pt_PT",
        "home": "Início", "geometry": "Geometria", "statistics": "Estatística",
        "search_placeholder": "Pesquisar calculadoras...",
        "params_title": "Parâmetros e Variáveis de Entrada",
        "derived_results": "Resultados e Métricas Calculadas",
        "step_by_step": "Demonstração Matemática Passo a Passo",
        "faq_title": "Perguntas Frequentes",
    },
    "nl": {
        "name": "Nederlands", "flag": "🇳🇱", "locale": "nl_NL",
        "home": "Home", "geometry": "Meetkunde", "statistics": "Statistiek",
        "search_placeholder": "Zoek rekenmachines...",
        "params_title": "Parameters & Invoerwaarden",
        "derived_results": "Berekende Resultaten & Metrieken",
        "step_by_step": "Stap-voor-stap Wiskundige Afleiding",
        "faq_title": "Veelgestelde Vragen",
    },
    "pl": {
        "name": "Polski", "flag": "🇵🇱", "locale": "pl_PL",
        "home": "Strona Główna", "geometry": "Geometria", "statistics": "Statystyka",
        "search_placeholder": "Szukaj kalkulatorów...",
        "params_title": "Parametry & Wartości Wejściowe",
        "derived_results": "Wyniki & Wartości Obliczone",
        "step_by_step": "Wyprowadzenie Matematyczne Krok po Kroku",
        "faq_title": "Często Zadawane Pytania",
    },
    "sv": {
        "name": "Svenska", "flag": "🇸🇪", "locale": "sv_SE",
        "home": "Hem", "geometry": "Geometri", "statistics": "Statistik",
        "search_placeholder": "Sök kalkylatorer...",
        "params_title": "Parametrar & Indata",
        "derived_results": "Beräknade Resultat",
        "step_by_step": "Steg-för-steg Matematiskt Bevis",
        "faq_title": "Vanliga Frågor",
    },
    "no": {
        "name": "Norsk", "flag": "🇳🇴", "locale": "nb_NO",
        "home": "Hjem", "geometry": "Geometri", "statistics": "Statistikk",
        "search_placeholder": "Søk kalkulatorer...",
        "params_title": "Parametere & Inndata",
        "derived_results": "Beregnede Resultater",
        "step_by_step": "Trinnvis Matematisk Utledning",
        "faq_title": "Ofte Stilte Spørsmål",
    },
    "fi": {
        "name": "Suomi", "flag": "🇫🇮", "locale": "fi_FI",
        "home": "Etusivu", "geometry": "Geometria", "statistics": "Tilastotiede",
        "search_placeholder": "Hae laskimia...",
        "params_title": "Parametrit ja Syötteet",
        "derived_results": "Lasketut Tulokset ja Metriikat",
        "step_by_step": "Askel askeleelta Matemaattinen Johto",
        "faq_title": "Usein Kysytyt Kysymykset",
    },
    "ro": {
        "name": "Română", "flag": "🇷🇴", "locale": "ro_RO",
        "home": "Acasă", "geometry": "Geometrie", "statistics": "Statistică",
        "search_placeholder": "Caută calculatoare...",
        "params_title": "Parametri & Date de Intrare",
        "derived_results": "Rezultate Calculate & Metrici",
        "step_by_step": "Demonstrație Matematică Pas cu Pas",
        "faq_title": "Întrebări Frecvente",
    }
}

BATCH2_SOLVERS = [
    # 15 Geometry Solvers
    {
        "subpath": "geometry/ellipse/",
        "key": "ellipse",
        "category": "geometry",
        "titles": {
            "en": "Ellipse Area, Perimeter & Eccentricity Calculator | OmniOperand",
            "es": "Calculadora de Elipse — Área, Perímetro y Excentricidad | OmniOperand",
            "fr": "Calculateur d'Ellipse — Aire, Périmètre et Excentricité | OmniOperand",
            "de": "Ellipse Rechner — Fläche, Umfang und Exzentrizität | OmniOperand",
            "it": "Calcolatore Ellisse — Area, Perimetro ed Eccentricità | OmniOperand",
            "pt": "Calculadora de Elipse — Área, Perímetro e Excentricidade | OmniOperand",
            "nl": "Ellips Rekenmachine — Oppervlakte, Omtrek en Excentriciteit | OmniOperand",
            "pl": "Kalkulator Elipsy — Pole, Obwód i Mimośród | OmniOperand",
            "sv": "Ellipskalkylator — Area, Omkrets och Excentricitet | OmniOperand",
            "no": "Ellipsekalkulator — Areal, Omkrets og Eksentrisitet | OmniOperand",
            "fi": "Ellipsilaskuri — Pinta-ala, Piiri ja Eksentrisyys | OmniOperand",
            "ro": "Calculator Elipsă — Arie, Perimetru și Excentricitate | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate exact ellipse area, Ramanujan high-precision perimeter approximation, semi-axes, focal distance, and orbital eccentricity.",
            "es": "Calcula el área exacta de la elipse, aproximación del perímetro de Ramanujan, semiejes, distancia focal y excentricidad orbital.",
            "fr": "Calculez l'aire exacte de l'ellipse, le périmètre haute précision de Ramanujan, les demi-axes et l'excentricité orbitale.",
            "de": "Berechnet exakte Ellipsenfläche, Ramanujan-Umfangsnäherung, Halbachsen, Brennweite und lineare Exzentrizität.",
            "it": "Calcola l'area esatta dell'ellisse, l'approssimazione del perimetro di Ramanujan, i semiassi e l'eccentricità orbitale.",
            "pt": "Calcule a área exata da elipse, aproximação do perímetro de Ramanujan, semieixos, distância focal e excentricidade.",
            "nl": "Bereken exacte oppervlakte van de ellips, Ramanujan omtreksbenadering, halve assen en excentriciteit.",
            "pl": "Oblicz dokładne pole elipsy, przybliżenie obwodu Ramanujana, półosie, odległość ogniskową i mimośród.",
            "sv": "Beräkna exakt ellipsarea, Ramanujans omkretsapproximation, halvaxlar, brännvidd och excentricitet.",
            "no": "Beregn nøyaktig ellipseareal, Ramanujans omkretsapproksimasjon, halvser og eksentrisitet.",
            "fi": "Laske ellipsin tarkka pinta-ala, Ramanujanin piirin approksimaatio, puoliakselit ja eksentrisyys.",
            "ro": "Calculează aria exactă a elipsei, aproximarea perimetrului Ramanujan, semiaxele și excentricitatea.",
        }
    },
    {
        "subpath": "geometry/trapezoid/",
        "key": "trapezoid",
        "category": "geometry",
        "titles": {
            "en": "Trapezoid Area, Perimeter & Midsegment Calculator | OmniOperand",
            "es": "Calculadora de Trapecio — Área, Altura y Mediana | OmniOperand",
            "fr": "Calculateur de Trapèze — Aire, Hauteur et Base Moyenne | OmniOperand",
            "de": "Trapez Rechner — Fläche, Höhe und Mittellinie | OmniOperand",
            "it": "Calcolatore Trapezio — Area, Altezza e Mediana | OmniOperand",
            "pt": "Calculadora de Trapézio — Área, Altura e Base Média | OmniOperand",
            "nl": "Trapezoïde Rekenmachine — Oppervlakte, Hoogte en Middenparallel | OmniOperand",
            "pl": "Kalkulator Trapezu — Pole, Wysokość i Linia Środkowa | OmniOperand",
            "sv": "Trapetskalkylator — Area, Höjd och Median | OmniOperand",
            "no": "Trapes-kalkulator — Areal, Høyde og Mellomlinje | OmniOperand",
            "fi": "Puolisuunnikaslaskuri — Pinta-ala, Korkeus ja Keski-jana | OmniOperand",
            "ro": "Calculator Trapez — Arie, Înălțime și Linie Mijlocie | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate trapezoid area, perimeter, height, leg lengths, and midsegment with bidirectional step-by-step proofs.",
            "es": "Calcula área del trapecio, perímetro, altura, lados no paralelos y mediana con demostración matemática paso a paso.",
            "fr": "Calculez l'aire, le périmètre, la hauteur et la base moyenne du trapèze avec résolutions bidirectionnelles.",
            "de": "Berechnet Trapezfläche, Umfang, Höhe, Schenkellängen und Mittellinie mit Schritt-für-Schritt-Herleitung.",
            "it": "Calcola area del trapezio, perimetro, altezza, lati obliqui e mediana con dimostrazione matematica passo a passo.",
            "pt": "Calcule a área do trapézio, perímetro, altura, lados oblíquos e base média com deduções passo a passo.",
            "nl": "Bereken oppervlakte, omtrek, hoogte en middenparallel van een trapezoïde met bidirectionele afleidingen.",
            "pl": "Oblicz pole trapezu, obwód, wysokość, długość ramion i linię środkową z dowodem krok po kroku.",
            "sv": "Beräkna trapetsarea, omkrets, höjd, benlängder och median med steg-för-steg matematiskt bevis.",
            "no": "Beregn trapesareal, omkrets, høyde og mellomlinje med toveis matematisk utledning.",
            "fi": "Laske puolisuunnikkaan pinta-ala, piiri, korkeus ja keski-jana vaiheittaisella matemaattisella johdolla.",
            "ro": "Calculează aria trapezului, perimetrul, înălțimea, laturile neparalele și linia mijlocie pas cu pas.",
        }
    },
    {
        "subpath": "geometry/rhombus/",
        "key": "rhombus",
        "category": "geometry",
        "titles": {
            "en": "Rhombus Area, Diagonals & Perimeter Calculator | OmniOperand",
            "es": "Calculadora de Rombo — Área, Diagonales y Perímetro | OmniOperand",
            "fr": "Calculateur de Losange — Aire, Diagonales et Périmètre | OmniOperand",
            "de": "Raute Rechner — Fläche, Diagonalen und Umfang | OmniOperand",
            "it": "Calcolatore Rombo — Area, Diagonali e Perimetro | OmniOperand",
            "pt": "Calculadora de Losango — Área, Diagonais e Perímetro | OmniOperand",
            "nl": "Ruit Rekenmachine — Oppervlakte, Diagonalen en Omtrek | OmniOperand",
            "pl": "Kalkulator Rombu — Pole, Przekątne i Obwód | OmniOperand",
            "sv": "Rombkalkylator — Area, Diagonaler och Omkrets | OmniOperand",
            "no": "Rombekalkulator — Areal, Diagonaler og Omkrets | OmniOperand",
            "fi": "Neljäkkään Laskuri — Pinta-ala, Lävistäjät ja Piiri | OmniOperand",
            "ro": "Calculator Romb — Arie, Diagonale și Perimetru | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate rhombus area from diagonals, side length, interior angles, and inradius with exact algebraic solutions.",
            "es": "Calcula el área del rombo a partir de sus diagonales, lado, ángulos interiores y radio inscrito con fórmulas exactas.",
            "fr": "Calculez l'aire du losange à partir des diagonales, de la longueur du côté, des angles et du rayon inscrit.",
            "de": "Berechnet Rautenfläche aus Diagonalen, Seitenlänge, Innenwinkeln und Inkreisradius mit exakter Algebra.",
            "it": "Calcola l'area del rombo dalle diagonali, lato, angoli interni e raggio inscritto con formule esatte.",
            "pt": "Calcule a área do losango a partir das diagonais, comprimento do lado, ângulos internos e raio inscrito.",
            "nl": "Bereken ruitoppervlakte uit diagonalen, zijdelengte, binnenhoeken en ingeschreven cirkelstraal.",
            "pl": "Oblicz pole rombu z przekątnych, długość boku, kąty wewnętrzne i promień koła wpisanego.",
            "sv": "Beräkna rombens area från diagonaler, sidolängd, vinklar och inskriven radie med exakta formler.",
            "no": "Beregn rombeareal fra diagonaler, sidelengde, vinkler og innskrevet sirkelradius.",
            "fi": "Laske neljäkkään pinta-ala lävistäjistä, sivun pituus, sisäkulmat ja sisään piirretyn ympyrän säde.",
            "ro": "Calculează aria rombului din diagonale, lungimea laturii, unghiurile interioare și raza înscrisă.",
        }
    },
    {
        "subpath": "geometry/parallelogram/",
        "key": "parallelogram",
        "category": "geometry",
        "titles": {
            "en": "Parallelogram Area, Perimeter & Angles Calculator | OmniOperand",
            "es": "Calculadora de Paralelogramo — Área, Base y Altura | OmniOperand",
            "fr": "Calculateur de Parallélogramme — Aire, Base et Hauteur | OmniOperand",
            "de": "Parallelogramm Rechner — Fläche, Basis und Höhe | OmniOperand",
            "it": "Calcolatore Parallelogramma — Area, Base e Altezza | OmniOperand",
            "pt": "Calculadora de Paralelogramo — Área, Base e Altura | OmniOperand",
            "nl": "Parallellogram Rekenmachine — Oppervlakte, Basis en Hoogte | OmniOperand",
            "pl": "Kalkulator Równoległoboku — Pole, Podstawa i Wysokość | OmniOperand",
            "sv": "Parallellogramkalkylator — Area, Bas och Höjd | OmniOperand",
            "no": "Parallellogramkalkulator — Areal, Grunnlinje og Høyde | OmniOperand",
            "fi": "Suunnikaslaskuri — Pinta-ala, Kanta ja Korkeus | OmniOperand",
            "ro": "Calculator Paralelogram — Arie, Bază și Înălțime | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate parallelogram area, diagonals via Law of Cosines, altitude, and perimeter with full bidirectional derivations.",
            "es": "Calcula el área del paralelogramo, diagonales mediante el Teorema del Coseno, altura y perímetro paso a paso.",
            "fr": "Calculez l'aire du parallélogramme, les diagonales par la loi des cosinus, la hauteur et le périmètre.",
            "de": "Berechnet Parallelogrammfläche, Diagonalen über den Kosinussatz, Höhe und Umfang bidirektional.",
            "it": "Calcola area del parallelogramma, diagonali con il Teorema del Coseno, altezza e perimetro.",
            "pt": "Calcule a área do paralelogramo, diagonais pela Lei dos Cossenos, altura e perímetro com fórmulas exatas.",
            "nl": "Bereken oppervlakte, diagonalen via cosinusregel, hoogte en omtrek van een parallellogram.",
            "pl": "Oblicz pole równoległoboku, przekątne z twierdzenia cosinusów, wysokość i obwód.",
            "sv": "Beräkna parallellogrammets area, diagonaler via cosinussatsen, höjd och omkrets.",
            "no": "Beregn parallellogramareal, diagonaler via cosinussetningen, høyde og omkrets.",
            "fi": "Laske suunnikkaan pinta-ala, lävistäjät kosinilauseella, korkeus ja piiri.",
            "ro": "Calculează aria paralelogramului, diagonalele prin Teorema Cosinusului, înălțimea și perimetrul.",
        }
    },
    {
        "subpath": "geometry/kite/",
        "key": "kite",
        "category": "geometry",
        "titles": {
            "en": "Kite Area, Diagonals & Perimeter Calculator | OmniOperand",
            "es": "Calculadora de Deltoide (Cometa) — Área y Diagonales | OmniOperand",
            "fr": "Calculateur de Cerf-Volant (Deltoïde) — Aire et Diagonales | OmniOperand",
            "de": "Drachenviereck Rechner — Fläche und Diagonalen | OmniOperand",
            "it": "Calcolatore Deltoide — Area e Diagonali | OmniOperand",
            "pt": "Calculadora de Deltoide (Pipa) — Área e Diagonais | OmniOperand",
            "nl": "Vlieger Vorm Rekenmachine — Oppervlakte en Diagonalen | OmniOperand",
            "pl": "Kalkulator Deltoidu — Pole i Przekątne | OmniOperand",
            "sv": "Drakkalkylator — Area och Diagonaler | OmniOperand",
            "no": "Dravekalkulator — Areal og Diagonaler | OmniOperand",
            "fi": "Leijalaskuri — Pinta-ala ja Lävistäjät | OmniOperand",
            "ro": "Calculator Deltoid — Arie și Diagonale | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate kite geometry: orthogonal diagonals, unequal side pairs, inradius, and interior angles with geometric proofs.",
            "es": "Calcula la geometría del deltoide: diagonales ortogonales, pares de lados, radio inscrito y ángulos interiores.",
            "fr": "Calculez la géométrie du cerf-volant : diagonales orthogonales, paires de côtés, rayon inscrit et angles.",
            "de": "Berechnet Drachenviereck-Geometrie: orthogonale Diagonalen, Seitenpaare, Inkreisradius und Innenwinkel.",
            "it": "Calcola la geometria del deltoide: diagonali ortogonali, lati, raggio inscritto e angoli interni.",
            "pt": "Calcule a geometria do deltoide: diagonais ortogonais, pares de lados desiguais, raio inscrito e ângulos.",
            "nl": "Bereken vlieger geometrie: loodrechte diagonalen, zijdeparen, ingeschreven cirkel en binnenhoeken.",
            "pl": "Oblicz geometrię deltoidu: prostopadłe przekątne, pary boków, promień koła wpisanego i kąty.",
            "sv": "Beräkna drakens geometri: vinkelräta diagonaler, sidopar, inskriven radie och vinklar.",
            "no": "Beregn drakens geometri: vinkelrette diagonaler, sidepar, innskrevet radius og vinkler.",
            "fi": "Laske leijan geometria: kohtisuorat lävistäjät, sivuparit, sisään piirretty säde ja kulmat.",
            "ro": "Calculează geometria deltoidului: diagonale perpendiculare, perechi de laturi, raza înscrisă și unghiuri.",
        }
    },
    {
        "subpath": "geometry/cylinder/",
        "key": "cylinder",
        "category": "geometry",
        "titles": {
            "en": "Cylinder Volume, Surface Area & Radius Calculator | OmniOperand",
            "es": "Calculadora de Cilindro — Volumen y Área Superficial | OmniOperand",
            "fr": "Calculateur de Cylindre — Volume et Surface Totale | OmniOperand",
            "de": "Zylinder Rechner — Volumen und Oberfläche | OmniOperand",
            "it": "Calcolatore Cilindro — Volume e Superficie Totale | OmniOperand",
            "pt": "Calculadora de Cilindro — Volume e Área de Superfície | OmniOperand",
            "nl": "Cilinder Rekenmachine — Inhoud en Oppervlakte | OmniOperand",
            "pl": "Kalkulator Walca — Objętość i Pole Powierzchni | OmniOperand",
            "sv": "Cylinderkalkylator — Volym och Mantelyta | OmniOperand",
            "no": "Sylinderkalkulator — Volum og Overflateareal | OmniOperand",
            "fi": "Sylinterilaskuri — Tilavuus ja Pinta-ala | OmniOperand",
            "ro": "Calculator Cilindru — Volum și Arie Totală | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate right circular cylinder volume, lateral surface area, total surface area, radius, and height inversions.",
            "es": "Calcula el volumen del cilindro circular recto, área lateral, área total, radio y altura con resolución inversa.",
            "fr": "Calculez le volume, l'aire latérale, la surface totale, le rayon et la hauteur du cylindre circulaire droit.",
            "de": "Berechnet Zylindervolumen, Mantelfläche, Gesamtoberfläche, Radius und Höhe mit Umkehrformeln.",
            "it": "Calcola il volume del cilindro retto, superficie laterale, superficie totale, raggio e altezza.",
            "pt": "Calcule o volume do cilindro circular reto, área lateral, área total, raio e inversões de altura.",
            "nl": "Bereken volume, manteloppervlakte, totale oppervlakte, straal en hoogte van een rechte cilinder.",
            "pl": "Oblicz objętość walca, pole powierzchni bocznej, pole całkowite, promień i wysokość.",
            "sv": "Beräkna cylindervolym, mantelyta, total yta, radie och höjdinversioner.",
            "no": "Beregn sylindervolum, mantelareal, totalt overflateareal, radius og høyde.",
            "fi": "Laske suoran ympyrälieriön tilavuus, vaipan ala, kokonaispinta-ala, säde ja korkeus.",
            "ro": "Calculează volumul cilindrului circular drept, aria laterală, aria totală, raza și înălțimea.",
        }
    },
    {
        "subpath": "geometry/cone/",
        "key": "cone",
        "category": "geometry",
        "titles": {
            "en": "Cone Volume, Slant Height & Surface Area Calculator | OmniOperand",
            "es": "Calculadora de Cono — Volumen, Generatriz y Área | OmniOperand",
            "fr": "Calculateur de Cône — Volume, Apothème et Surface | OmniOperand",
            "de": "Kegel Rechner — Volumen, Mantellinie und Oberfläche | OmniOperand",
            "it": "Calcolatore Cono — Volume, Apotema e Superficie | OmniOperand",
            "pt": "Calculadora de Cone — Volume, Geratriz e Área | OmniOperand",
            "nl": "Kegel Rekenmachine — Inhoud, Schuine Hoogte en Oppervlakte | OmniOperand",
            "pl": "Kalkulator Stożka — Objętość, Tworząca i Pole | OmniOperand",
            "sv": "Konkalkylator — Volym, Sidohöjd och Area | OmniOperand",
            "no": "Kjeglekalkulator — Volum, Sidekant og Overflate | OmniOperand",
            "fi": "Kartiolaskuri — Tilavuus, Sivujana ja Pinta-ala | OmniOperand",
            "ro": "Calculator Con — Volum, Generatoare și Arie | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate right cone volume, slant height (generatrix), lateral surface area, base area, and apex angle.",
            "es": "Calcula el volumen del cono recto, generatriz, área lateral, área de la base y ángulo en el vértice.",
            "fr": "Calculez le volume du cône droit, la hauteur oblique (génératrice), la surface latérale et l'angle au sommet.",
            "de": "Berechnet Kegelvolumen, Mantellinie, Mantelfläche, Grundfläche und Öffnungswinkel mit exakter Algebra.",
            "it": "Calcola il volume del cono retto, apotema (generatrice), superficie laterale e angolo al vertice.",
            "pt": "Calcule o volume do cone reto, geratriz, área lateral, área da base e ângulo no ápice.",
            "nl": "Bereken kegelinhoud, schuine zijde (mantellijn), manteloppervlakte en tophoek.",
            "pl": "Oblicz objętość stożka, tworzącą, pole powierzchni bocznej, pole podstawy i kąt rozwarcia.",
            "sv": "Beräkna konens volym, sidohöjd, mantelyta, basarea och toppvinkel med exakta formler.",
            "no": "Beregn kjeglevolum, sidekant, mantelareal, grunnflate og toppvinkel.",
            "fi": "Laske suoran kartion tilavuus, sivujana, vaipan ala, pohjan ala ja huippukulma.",
            "ro": "Calculează volumul conului drept, generatoarea, aria laterală, aria bazei și unghiul la vârf.",
        }
    },
    {
        "subpath": "geometry/sphere/",
        "key": "sphere",
        "category": "geometry",
        "titles": {
            "en": "Sphere Volume, Surface Area & Radius Calculator | OmniOperand",
            "es": "Calculadora de Esfera — Volumen y Área Superficial | OmniOperand",
            "fr": "Calculateur de Sphère — Volume et Surface Sphérique | OmniOperand",
            "de": "Kugel Rechner — Volumen und Kugeloberfläche | OmniOperand",
            "it": "Calcolatore Sfera — Volume e Superficie Sferica | OmniOperand",
            "pt": "Calculadora de Esfera — Volume e Área Esférica | OmniOperand",
            "nl": "Bol Rekenmachine — Volume en Buitenoppervlakte | OmniOperand",
            "pl": "Kalkulator Kuli — Objętość i Pole Powierzchni | OmniOperand",
            "sv": "Sfärkalkylator — Volym och Mantelyta | OmniOperand",
            "no": "Kulekalkulator — Volum og Overflate | OmniOperand",
            "fi": "Pallolaskuri — Tilavuus ja Pallopinnan Ala | OmniOperand",
            "ro": "Calculator Sferă — Volum și Arie Sferică | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate sphere volume, surface area, radius, diameter, and great circle circumference with exact pi formulas.",
            "es": "Calcula el volumen de la esfera, área superficial, radio, diámetro y circunferencia del círculo máximo con π exacto.",
            "fr": "Calculez le volume de la sphère, l'aire de surface, le rayon, le diamètre et la circonférence avec π exact.",
            "de": "Berechnet Kugelvolumen, Oberfläche, Radius, Durchmesser und Großkreisumfang mit exakten Pi-Formeln.",
            "it": "Calcola il volume della sfera, superficie, raggio, diametro e circonferenza massima con formule esatte con π.",
            "pt": "Calcule o volume da esfera, área superficial, raio, diâmetro e circunferência com fórmulas exatas com π.",
            "nl": "Bereken bolvolume, buitenoppervlakte, straal, diameter en grootcirkelomtrek met exacte pi-formules.",
            "pl": "Oblicz objętość kuli, pole powierzchni, promień, średnicę i obwód koła wielkiego z użyciem π.",
            "sv": "Beräkna sfärens volym, mantelarea, radie, diameter och storcirkelomkrets med exakta pi-formler.",
            "no": "Beregn kulevolum, overflateareal, radius, diameter og storsirkelomkrets med eksakte pi-formler.",
            "fi": "Laske pallon tilavuus, pinta-ala, säde, halkaisija ja isoympyrän piiri tarkoilla piin kaavoilla.",
            "ro": "Calculează volumul sferei, aria suprafeței, raza, diametrul și circumferința cercului mare cu π exact.",
        }
    },
    {
        "subpath": "geometry/torus/",
        "key": "torus",
        "category": "geometry",
        "titles": {
            "en": "Torus Volume & Surface Area Calculator | OmniOperand",
            "es": "Calculadora de Toroide — Volumen y Área Superficial | OmniOperand",
            "fr": "Calculateur de Tore — Volume et Surface Torique | OmniOperand",
            "de": "Torus Rechner — Volumen und Ringoberfläche | OmniOperand",
            "it": "Calcolatore Toro — Volume e Superficie Toroidale | OmniOperand",
            "pt": "Calculadora de Toroide — Volume e Área de Superfície | OmniOperand",
            "nl": "Torus Rekenmachine — Inhoud en Buitenoppervlakte | OmniOperand",
            "pl": "Kalkulator Torusa — Objętość i Powierzchnia Torusa | OmniOperand",
            "sv": "Toruskalkylator — Volym och Mantelyta | OmniOperand",
            "no": "Toruskalkulator — Volum og Overflateareal | OmniOperand",
            "fi": "Toruslaskuri — Tilavuus ja Pinta-ala | OmniOperand",
            "ro": "Calculator Tor — Volum și Arie Toroidală | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate ring torus volume and surface area using Pappus-Guldinus centroid theorems and major/minor radii.",
            "es": "Calcula el volumen y área del toroide aplicando los teoremas del centroide de Pappus-Guldin y radios mayor/menor.",
            "fr": "Calculez le volume et la surface du tore circulaire via les théorèmes de Guldin et les rayons majeur et mineur.",
            "de": "Berechnet Torusvolumen und Ringoberfläche nach den Guldinschen Regeln mit Haupt- und Nebenradius.",
            "it": "Calcola il volume e la superficie del toro usando i teoremi di Pappo-Guldino e i raggi maggiore e minore.",
            "pt": "Calcule o volume e área do toroide aplicando os teoremas de Pappus-Guldin com raio maior e menor.",
            "nl": "Bereken volume en oppervlakte van een ringtorus met de stellingen van Pappus-Guldinus.",
            "pl": "Oblicz objętość i pole powierzchni torusa z twierdzenia Pappusa-Guldina przy znanych promieniach R i r.",
            "sv": "Beräkna torusvolym och mantelyta med Pappus-Guldinus satser och stor/liten radie.",
            "no": "Beregn torusvolum og overflate med Pappus-Guldins teoremer og stor/liten radius.",
            "fi": "Laske renkaan muotoisen toruksen tilavuus ja pinta-ala Pappuksen-Guldinin lauseilla.",
            "ro": "Calculează volumul și aria torului circular aplicând teoremele lui Pappus-Guldin și razele mare/mică.",
        }
    },
    {
        "subpath": "geometry/triangular-prism/",
        "key": "triangular-prism",
        "category": "geometry",
        "titles": {
            "en": "Triangular Prism Volume & Surface Area Calculator | OmniOperand",
            "es": "Calculadora de Prisma Triangular — Volumen y Área | OmniOperand",
            "fr": "Calculateur de Prisme Triangulaire — Volume et Aire | OmniOperand",
            "de": "Dreiecksprisma Rechner — Volumen und Oberfläche | OmniOperand",
            "it": "Calcolatore Prisma Triangolare — Volume e Superficie | OmniOperand",
            "pt": "Calculadora de Prisma Triangular — Volume e Área | OmniOperand",
            "nl": "Driezijdige Prisma Rekenmachine — Inhoud en Oppervlakte | OmniOperand",
            "pl": "Kalkulator Graniastosłupa Trójkątnego — Objętość i Pole | OmniOperand",
            "sv": "Triangulärt Prisma Kalkylator — Volym och Yta | OmniOperand",
            "no": "Trekantet Prisme Kalkulator — Volum og Areal | OmniOperand",
            "fi": "Kolmiosärmiölaskuri — Tilavuus ja Pinta-ala | OmniOperand",
            "ro": "Calculator Prismă Triunghiulară — Volum și Arie | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate right triangular prism volume, lateral surface area, total surface area, and base triangle geometry.",
            "es": "Calcula el volumen del prisma triangular recto, área lateral, área total y geometría del triángulo base.",
            "fr": "Calculez le volume du prisme triangulaire droit, la surface latérale, la surface totale et l'aire de la base.",
            "de": "Berechnet Volumen, Mantelfläche, Gesamtoberfläche und Dreiecksbasis eines geraden Dreiecksprismas.",
            "it": "Calcola volume del prisma triangolare retto, superficie laterale, superficie totale e geometria della base.",
            "pt": "Calcule o volume do prisma triangular reto, área lateral, área total e geometria da base triangular.",
            "nl": "Bereken volume, manteloppervlakte en totale oppervlakte van een recht driezijdig prisma.",
            "pl": "Oblicz objętość prostego graniastosłupa trójkątnego, pole powierzchni bocznej i całkowitej.",
            "sv": "Beräkna rätvinkligt triangulärt prismas volym, mantelyta, total yta och bastriangel.",
            "no": "Beregn volum, mantelareal og totalt overflateareal for et rett trekantet prisme.",
            "fi": "Laske suoran kolmiosärmiön tilavuus, vaipan ala, kokonaispinta-ala ja pohjakolmion geometria.",
            "ro": "Calculează volumul prismei triunghiulare drepte, aria laterală, aria totală și geometria bazei.",
        }
    },
    {
        "subpath": "geometry/pyramid/",
        "key": "pyramid",
        "category": "geometry",
        "titles": {
            "en": "Pyramid Volume, Slant Height & Surface Area Calculator | OmniOperand",
            "es": "Calculadora de Pirámide — Volumen, Apotema y Área | OmniOperand",
            "fr": "Calculateur de Pyramide — Volume, Apothème et Surface | OmniOperand",
            "de": "Pyramide Rechner — Volumen, Höhe und Oberfläche | OmniOperand",
            "it": "Calcolatore Piramide — Volume, Apotema e Superficie | OmniOperand",
            "pt": "Calculadora de Pirâmide — Volume, Apótema e Área | OmniOperand",
            "nl": "Piramide Rekenmachine — Inhoud en Buitenoppervlakte | OmniOperand",
            "pl": "Kalkulator Ostrosłupa — Objętość i Pole Powierzchni | OmniOperand",
            "sv": "Pyramidkalkylator — Volym och Mantelyta | OmniOperand",
            "no": "Pyramidekalkulator — Volum og Overflate | OmniOperand",
            "fi": "Pyramidilaskuri — Tilavuus ja Pinta-ala | OmniOperand",
            "ro": "Calculator Piramidă — Volum, Apotemă și Arie | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate regular right pyramid volume, slant height (apothem), lateral face area, base area, and total surface area.",
            "es": "Calcula el volumen de la pirámide regular recta, apotema, área de las caras laterales y área superficial total.",
            "fr": "Calculez le volume de la pyramide régulière droite, l'apothème, l'aire latérale et la surface totale.",
            "de": "Berechnet Pyramidenvolumen, Seitenhöhe (Apothema), Mantelfläche und Gesamtoberfläche für quadratische Pyramiden.",
            "it": "Calcola volume della piramide retta, apotema, area delle facce laterali, area di base e superficie totale.",
            "pt": "Calcule o volume da pirâmide regular reta, apótema, área lateral, área da base e área de superfície total.",
            "nl": "Bereken volume, schuine hoogte (apothema), manteloppervlakte en totale oppervlakte van een piramide.",
            "pl": "Oblicz objętość ostrosłupa prawidłowego, wysokość ściany bocznej, pole powierzchni bocznej i całkowitej.",
            "sv": "Beräkna regelbunden pyramids volym, sidohöjd (apotem), mantelyta och total yta.",
            "no": "Beregn regulær pyramides volum, sidehøyde (apotem), mantelareal og total overflate.",
            "fi": "Laske säännöllisen pyramidin tilavuus, sivukorkeus (apoteema), vaipan ala ja kokonaispinta-ala.",
            "ro": "Calculează volumul piramidei regulate drepte, apotema, aria fețelor laterale și aria totală.",
        }
    },
    {
        "subpath": "geometry/frustum-cone/",
        "key": "frustum-cone",
        "category": "geometry",
        "titles": {
            "en": "Truncated Cone (Frustum) Volume & Surface Area Calculator | OmniOperand",
            "es": "Calculadora de Tronco de Cono — Volumen y Área | OmniOperand",
            "fr": "Calculateur de Tronc de Cône — Volume et Aire Latérale | OmniOperand",
            "de": "Kegelstumpf Rechner — Volumen und Mantelfläche | OmniOperand",
            "it": "Calcolatore Tronco di Cono — Volume e Superficie | OmniOperand",
            "pt": "Calculadora de Tronco de Cone — Volume e Área | OmniOperand",
            "nl": "Afgeknotte Kegel Rekenmachine — Inhoud en Oppervlakte | OmniOperand",
            "pl": "Kalkulator Stożka Ściętego — Objętość i Pole | OmniOperand",
            "sv": "Stympad Kon Kalkylator — Volym och Mantelyta | OmniOperand",
            "no": "Avkortet Kjegle Kalkulator — Volum og Overflate | OmniOperand",
            "fi": "Katkaistun Kartion Laskuri — Tilavuus ja Pinta-ala | OmniOperand",
            "ro": "Calculator Trunchi de Con — Volum și Arie Laterală | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate frustum of a right circular cone: volume, slant height, lateral area, and total surface area.",
            "es": "Calcula el tronco de cono circular recto: volumen, generatriz, área lateral y área superficial total.",
            "fr": "Calculez le tronc de cône circulaire droit : volume, apothème, aire latérale et surface totale.",
            "de": "Berechnet Kegelstumpf: Volumen, Mantellinie, Mantelfläche und Gesamtoberfläche mit geschlossenen Formeln.",
            "it": "Calcola il tronco di cono retto: volume, apotema, superficie laterale e superficie totale.",
            "pt": "Calcule o tronco de cone circular reto: volume, geratriz, área lateral e área de superfície total.",
            "nl": "Bereken afgeknotte kegel: inhoud, schuine hoogte, manteloppervlakte en totale oppervlakte.",
            "pl": "Oblicz stożek ścięty: objętość, tworzącą, pole powierzchni bocznej i pole całkowite.",
            "sv": "Beräkna stympad kon: volym, sidohöjd, mantelyta och total yta med exakta formler.",
            "no": "Beregn avkortet kjegle: volum, sidekant, mantelareal og total overflate.",
            "fi": "Laske katkaistu kartio: tilavuus, sivujana, vaipan ala ja kokonaispinta-ala.",
            "ro": "Calculează trunchiul de con circular drept: volum, generatoare, arie laterală și arie totală.",
        }
    },
    {
        "subpath": "geometry/frustum-pyramid/",
        "key": "frustum-pyramid",
        "category": "geometry",
        "titles": {
            "en": "Truncated Pyramid (Frustum) Volume & Surface Area Calculator | OmniOperand",
            "es": "Calculadora de Tronco de Pirámide — Volumen y Área | OmniOperand",
            "fr": "Calculateur de Tronc de Pyramide — Volume et Surface | OmniOperand",
            "de": "Pyramidenstumpf Rechner — Volumen und Oberfläche | OmniOperand",
            "it": "Calcolatore Tronco di Piramide — Volume e Superficie | OmniOperand",
            "pt": "Calculadora de Tronco de Pirâmide — Volume e Área | OmniOperand",
            "nl": "Afgeknotte Piramide Rekenmachine — Inhoud en Oppervlakte | OmniOperand",
            "pl": "Kalkulator Ostrosłupa Ściętego — Objętość i Pole | OmniOperand",
            "sv": "Stympad Pyramid Kalkylator — Volym och Yta | OmniOperand",
            "no": "Avkortet Pyramide Kalkulator — Volum og Overflate | OmniOperand",
            "fi": "Katkaistun Pyramidin Laskuri — Tilavuus ja Pinta-ala | OmniOperand",
            "ro": "Calculator Trunchi de Piramidă — Volum și Arie | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate square truncated pyramid volume, slant height, trapezoidal lateral face areas, and total surface area.",
            "es": "Calcula el tronco de pirámide cuadrangular: volumen, apotema, áreas trapezoidales laterales y superficie total.",
            "fr": "Calculez le tronc de pyramide à base carrée : volume, apothème, surfaces latérales trapézoïdales et aire totale.",
            "de": "Berechnet Pyramidenstumpf mit quadratischer Grundfläche: Volumen, Seitenhöhe, Mantelfläche und Oberfläche.",
            "it": "Calcola il tronco di piramide quadrata: volume, apotema, superfici trapezoidali laterali e area totale.",
            "pt": "Calcule o tronco de pirâmide de base quadrada: volume, apótema, áreas laterais trapezoidais e superfície total.",
            "nl": "Bereken afgeknotte piramide: volume, schuine hoogte, trapeziumvormige zijvlakken en totale oppervlakte.",
            "pl": "Oblicz ostrosłup ścięty o podstawie kwadratowej: objętość, wysokość ściany bocznej i pole całkowite.",
            "sv": "Beräkna stympad kvadratisk pyramid: volym, sidohöjd, trapetssidor och total mantelyta.",
            "no": "Beregn avkortet kvadratisk pyramide: volum, sidehøyde, trapesformede sideflater og totalt areal.",
            "fi": "Laske katkaistu neliöpohjainen pyramidi: tilavuus, sivukorkeus, puolisuunnikassivut ja pinta-ala.",
            "ro": "Calculează trunchiul de piramidă pătrată: volum, apotemă, fețe laterale trapezoidale și arie totală.",
        }
    },
    {
        "subpath": "geometry/ellipsoid/",
        "key": "ellipsoid",
        "category": "geometry",
        "titles": {
            "en": "Ellipsoid Volume & Surface Area Calculator | OmniOperand",
            "es": "Calculadora de Elipsoide — Volumen y Superficie Tridimensional | OmniOperand",
            "fr": "Calculateur d'Ellipsoïde — Volume et Surface Tridimensionnelle | OmniOperand",
            "de": "Ellipsoid Rechner — Volumen und Näherungsoberfläche | OmniOperand",
            "it": "Calcolatore Ellissoide — Volume e Superficie Tridimensionale | OmniOperand",
            "pt": "Calculadora de Elipsoide — Volume e Área Tridimensional | OmniOperand",
            "nl": "Ellipsoïde Rekenmachine — Inhoud en Oppervlakte | OmniOperand",
            "pl": "Kalkulator Elipsoidy — Objętość i Pole Powierzchni | OmniOperand",
            "sv": "Ellipsoidkalkylator — Volym och Area | OmniOperand",
            "no": "Ellipsoidekalkulator — Volum og Overflate | OmniOperand",
            "fi": "Ellipsoidilaskuri — Tilavuus ja Pinta-ala | OmniOperand",
            "ro": "Calculator Elipsoid — Volum și Arie Tridimensională | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate tri-axial ellipsoid volume and Knud Thomsen high-precision surface area approximation with semi-axes a, b, c.",
            "es": "Calcula el volumen del elipsoide triaxial y la fórmula de aproximación de superficie de Knud Thomsen.",
            "fr": "Calculez le volume de l'ellipsoïde triaxial et l'approximation de surface de Knud Thomsen avec demi-axes a, b, c.",
            "de": "Berechnet Ellipsoidvolumen und Knud-Thomsen-Oberflächennäherung mit den Halbachsen a, b und c.",
            "it": "Calcola il volume dell'ellissoide triassiale e la formula di superficie di Knud Thomsen con i semiassi a, b, c.",
            "pt": "Calcule o volume do elipsoide triaxial e aproximação de superfície de Knud Thomsen com semieixos a, b, c.",
            "nl": "Bereken volume en Knud Thomsen oppervlaktebenadering van een drie-assige ellipsoïde.",
            "pl": "Oblicz objętość elipsoidy trójosiowej oraz pole powierzchni ze wzoru Knuda Thomsena dla półosi a, b, c.",
            "sv": "Beräkna triaxiell ellipsoids volym och Knud Thomsens ytapproximation med halvaxlarna a, b, c.",
            "no": "Beregn triaksial ellipsoides volum og Knud Thomsens overflateapproksimasjon med halvaksene a, b, c.",
            "fi": "Laske kolmiakselisen ellipsoidin tilavuus ja Knud Thomsenin pinta-alan approksimaatio puoliakseleilla.",
            "ro": "Calculează volumul elipsoidului triaxial și aproximarea ariei Knud Thomsen cu semiaxele a, b, c.",
        }
    },
    {
        "subpath": "geometry/arc-length/",
        "key": "arc-length",
        "category": "geometry",
        "titles": {
            "en": "Arc Length, Chord & Circle Sector Calculator | OmniOperand",
            "es": "Calculadora de Longitud de Arco y Ángulo Central | OmniOperand",
            "fr": "Calculateur de Longueur d'Arc et Angle au Centre | OmniOperand",
            "de": "Kreisbogenlänge & Zentriwinkel Rechner | OmniOperand",
            "it": "Calcolatore Lunghezza dell'Arco e Angolo al Centro | OmniOperand",
            "pt": "Calculadora de Comprimento de Arco e Ângulo Central | OmniOperand",
            "nl": "Booglengte en Middelpuntshoek Rekenmachine | OmniOperand",
            "pl": "Kalkulator Długości Łuku i Kąta Środkowego | OmniOperand",
            "sv": "Båglängd & Medelpunktsvinkel Kalkylator | OmniOperand",
            "no": "Buelengde & Sentralvinkel Kalkulator | OmniOperand",
            "fi": "Kaaren Pituus ja Keskuskulma Laskuri | OmniOperand",
            "ro": "Calculator Lungimea Arcului și Unghi la Centru | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate circular arc length, central angle in degrees and radians, chord length, sagitta, and sector area.",
            "es": "Calcula la longitud del arco circular, ángulo central en grados y radianes, cuerda, flecha y área del sector.",
            "fr": "Calculez la longueur d'arc circulaire, l'angle au centre en degrés et radians, la corde, la flèche et l'aire.",
            "de": "Berechnet Kreisbogenlänge, Zentriwinkel in Grad und Radiant, Sehnenlänge, Bogenhöhe und Sektorfläche.",
            "it": "Calcola lunghezza dell'arco, angolo al centro in gradi e radianti, corda, freccia (sagitta) e area del settore.",
            "pt": "Calcule comprimento do arco circular, ângulo central em graus e radianos, corda, flecha e área do setor.",
            "nl": "Bereken booglengte, middelpuntshoek in graden en radialen, koordelengte, pijlhoogte en sectoroppervlakte.",
            "pl": "Oblicz długość łuku kołowego, kąt środkowy w stopniach i radianach, cięciwę, strzałkę i pole wycinka.",
            "sv": "Beräkna cirkelbågens längd, medelpunktsvinkel i grader och radianer, korda, pilhöjd och sektorarea.",
            "no": "Beregn sirkelbuelengde, sentralvinkel i grader og radianer, korde, pilhøyde og sektorareal.",
            "fi": "Laske ympyrän kaaren pituus, keskuskulma asteina ja radiaaneina, jänne, sagitta ja sektorin pinta-ala.",
            "ro": "Calculează lungimea arcului de cerc, unghiul la centru în grade și radiani, coarda, săgeata și aria sectorului.",
        }
    },
    # 4 Statistics Solvers
    {
        "subpath": "statistics/standard-deviation/",
        "key": "standard-deviation",
        "category": "statistics",
        "titles": {
            "en": "Standard Deviation & Variance Calculator (Sample & Population) | OmniOperand",
            "es": "Calculadora de Desviación Estándar y Varianza | OmniOperand",
            "fr": "Calculateur d'Écart-Type et Variance Statistique | OmniOperand",
            "de": "Standardabweichung & Varianz Rechner | OmniOperand",
            "it": "Calcolatore Deviazione Standard e Varianza | OmniOperand",
            "pt": "Calculadora de Desvio Padrão e Variância | OmniOperand",
            "nl": "Standaarddeviatie & Variantie Rekenmachine | OmniOperand",
            "pl": "Kalkulator Odchylenia Standardowego i Wariancji | OmniOperand",
            "sv": "Standardavvikelse & Varians Kalkylator | OmniOperand",
            "no": "Standardavvik & Varians Kalkulator | OmniOperand",
            "fi": "Keskihajonta ja Varianssi Laskuri | OmniOperand",
            "ro": "Calculator Abatere Standard și Varianță | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate sample (s) and population (σ) standard deviation, variance, mean, and sum of squares with step-by-step proofs.",
            "es": "Calcula la desviación estándar muestral (s) y poblacional (σ), varianza, media y suma de cuadrados con pasos detallados.",
            "fr": "Calculez l'écart-type d'échantillon (s) et de population (σ), la variance, la moyenne et la somme des carrés.",
            "de": "Berechnet Stichproben- (s) und Populations-Standardabweichung (σ), Varianz, Mittelwert und Quadratsummen.",
            "it": "Calcola la deviazione standard campionaria (s) e della popolazione (σ), varianza, media e somma dei quadrati.",
            "pt": "Calcule o desvio padrão amostral (s) e populacional (σ), variância, média e soma dos quadrados com passos.",
            "nl": "Bereken steekproef (s) en populatie (σ) standaarddeviatie, variantie, gemiddelde en kwadratensom.",
            "pl": "Oblicz odchylenie standardowe próby (s) i populacji (σ), wariancję, średnią i sumę kwadratów odchyleń.",
            "sv": "Beräkna stickprovs- (s) och populationsstandardavvikelse (σ), varians, medelvärde och kvadratsummor.",
            "no": "Beregn utvalgs- (s) og populasjonsstandardavvik (σ), varians, gjennomsnitt og kvadratsum.",
            "fi": "Laske otos- (s) ja perusjoukon (σ) keskihajonta, varianssi, keskiarvo ja neliösumma vaiheittain.",
            "ro": "Calculează abaterea standard de selecție (s) și de populație (σ), varianța, media și suma pătratelor.",
        }
    },
    {
        "subpath": "statistics/z-score/",
        "key": "z-score",
        "category": "statistics",
        "titles": {
            "en": "Z-Score & Normal Distribution Probability Calculator | OmniOperand",
            "es": "Calculadora de Puntuación Z (Z-Score) y Probabilidad Normal | OmniOperand",
            "fr": "Calculateur de Score Z et Probabilité Normale | OmniOperand",
            "de": "Z-Score & Normalverteilung Rechner | OmniOperand",
            "it": "Calcolatore Punteggio Z (Z-Score) e Probabilità Normale | OmniOperand",
            "pt": "Calculadora de Escore Z (Z-Score) e Distribuição Normal | OmniOperand",
            "nl": "Z-Score & Normale Verdeling Rekenmachine | OmniOperand",
            "pl": "Kalkulator Z-Score i Rozkładu Normalnego | OmniOperand",
            "sv": "Z-Värde & Normalfördelning Kalkylator | OmniOperand",
            "no": "Z-Skår & Normalfordeling Kalkulator | OmniOperand",
            "fi": "Z-Pistemäärä ja Normaalijakauma Laskuri | OmniOperand",
            "ro": "Calculator Scor Z și Probabilitate Normală | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate z-score, standard normal cumulative probability P(Z < z), two-tailed p-values, and percentile ranks.",
            "es": "Calcula la puntuación Z, probabilidad acumulada de la normal estándar P(Z < z), valores p y percentiles.",
            "fr": "Calculez le score Z, la probabilité cumulée normale standard P(Z < z), les p-valeurs bilatérales et les rangs centiles.",
            "de": "Berechnet Z-Score, kumulierte Standardnormalverteilung P(Z < z), zweiseitige p-Werte und Perzentilränge.",
            "it": "Calcola il punteggio Z, la probabilità cumulativa normale standard P(Z < z), i p-value a due code e i percentili.",
            "pt": "Calcule o escore Z, probabilidade cumulativa normal padrão P(Z < z), valores-p bilaterais e percentis.",
            "nl": "Bereken z-score, cumulatieve standaardnormale verdeling P(Z < z), tweezijdige p-waarden en percentielen.",
            "pl": "Oblicz standaryzowaną wartość z-score, dystrybuantę rozkładu normalnego P(Z < z), p-wartości i percentyle.",
            "sv": "Beräkna z-värde, standardnormalfördelningens kumulativa sannolikhet P(Z < z), tvåsidiga p-värden och percentiler.",
            "no": "Beregn z-skår, standard normalfordelings kumulative sannsynlighet P(Z < z), tosidige p-verdier og persentiler.",
            "fi": "Laske z-pistemäärä, standardinormaalijakauman kertymäfunktio P(Z < z), kaksisuuntaiset p-arvot ja persentiilit.",
            "ro": "Calculează scorul Z, probabilitatea cumulată normală standard P(Z < z), valorile p bilaterale și percentilele.",
        }
    },
    {
        "subpath": "statistics/permutations-combinations/",
        "key": "permutations-combinations",
        "category": "statistics",
        "titles": {
            "en": "Permutations and Combinations Calculator (nPr and nCr) | OmniOperand",
            "es": "Calculadora de Permutaciones y Combinaciones (nPr y nCr) | OmniOperand",
            "fr": "Calculateur de Permutations et Combinaisons (nPr et nCr) | OmniOperand",
            "de": "Permutationen & Kombinationen Rechner (nPr und nCr) | OmniOperand",
            "it": "Calcolatore Permutazioni e Combinazioni (nPr e nCr) | OmniOperand",
            "pt": "Calculadora de Permutações e Combinações (nPr e nCr) | OmniOperand",
            "nl": "Permutaties en Combinaties Rekenmachine (nPr en nCr) | OmniOperand",
            "pl": "Kalkulator Permutacji i Kombinacji (nPr i nCr) | OmniOperand",
            "sv": "Permutationer och Kombinationer Kalkylator (nPr och nCr) | OmniOperand",
            "no": "Permutasjoner og Kombinasjoner Kalkulator (nPr og nCr) | OmniOperand",
            "fi": "Permutaatiot ja Kombinaatiot Laskuri (nPr ja nCr) | OmniOperand",
            "ro": "Calculator Permutări și Combinări (nPr și nCr) | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate permutations nPr and combinations nCr with and without repetition using exact arbitrary-precision factorials.",
            "es": "Calcula permutaciones nPr y combinaciones nCr con y sin repetición mediante factoriales de precisión exacta.",
            "fr": "Calculez les permutations nPr et combinaisons nCr avec et sans répétition grâce aux factorielles exactes.",
            "de": "Berechnet Permutationen nPr und Kombinationen nCr mit und ohne Wiederholung mittels exakter Fakultäten.",
            "it": "Calcola permutazioni nPr e combinazioni nCr con e senza ripetizione usando fattoriali a precisione esatta.",
            "pt": "Calcule permutações nPr e combinações nCr com e sem repetição usando fatoriais de precisão arbitrária.",
            "nl": "Bereken permutaties nPr en combinaties nCr met en zonder herhaling via exacte faculteiten.",
            "pl": "Oblicz permutacje nPr oraz kombinacje nCr z powtórzeniami i bez powtórzeń za pomocą dokładnych silni.",
            "sv": "Beräkna permutationer nPr och kombinationer nCr med och utan upprepning med exakta fakulteter.",
            "no": "Beregn permutasjoner nPr og kombinasjoner nCr med og uten repetisjon med eksakte fakulteter.",
            "fi": "Laske permutaatiot nPr ja kombinaatiot nCr toistolla ja ilman toistoa tarkoilla kertomilla.",
            "ro": "Calculează permutările nPr și combinările nCr cu și fără repetiție folosind factoriale exacte.",
        }
    },
    {
        "subpath": "statistics/bayes-theorem/",
        "key": "bayes-theorem",
        "category": "statistics",
        "titles": {
            "en": "Bayes' Theorem & Conditional Probability Calculator | OmniOperand",
            "es": "Calculadora del Teorema de Bayes y Probabilidad Condicional | OmniOperand",
            "fr": "Calculateur du Théorème de Bayes et Probabilité Conditionnelle | OmniOperand",
            "de": "Satz von Bayes & Bedingte Wahrscheinlichkeit Rechner | OmniOperand",
            "it": "Calcolatore Teorema di Bayes e Probabilità Condizionata | OmniOperand",
            "pt": "Calculadora do Teorema de Bayes e Probabilidade Condicional | OmniOperand",
            "nl": "Theorema van Bayes & Voorwaardelijke Kans Rekenmachine | OmniOperand",
            "pl": "Kalkulator Twierdzenia Bayesa i Prawdopodobieństwa Warunkowego | OmniOperand",
            "sv": "Bayes Sats & Betingad Sannolikhet Kalkylator | OmniOperand",
            "no": "Bayes' Teorem & Betinget Sannsynlighet Kalkulator | OmniOperand",
            "fi": "Bayesin Lause ja Ehdollinen Todennäköisyys Laskuri | OmniOperand",
            "ro": "Calculator Teorema lui Bayes și Probabilitate Condiționată | OmniOperand",
        },
        "descriptions": {
            "en": "Calculate posterior probability P(A|B) using Bayes' Rule, prior odds, likelihood ratios, and false positive rates.",
            "es": "Calcula la probabilidad a posteriori P(A|B) usando la Regla de Bayes, razones de verosimilitud y tasas de falsos positivos.",
            "fr": "Calculez la probabilité a posteriori P(A|B) selon le théorème de Bayes, les rapports de vraisemblance et faux positifs.",
            "de": "Berechnet A-posteriori-Wahrscheinlichkeit P(A|B) nach der Bayes-Formel, Likelihood-Quotienten und Falsch-Positiv-Raten.",
            "it": "Calcola la probabilità a posteriori P(A|B) usando il Teorema di Bayes, rapporti di verosimiglianza e falsi positivi.",
            "pt": "Calcule a probabilidade a posteriori P(A|B) usando a Regra de Bayes, razões de verossimilhança e taxas de falso positivo.",
            "nl": "Bereken posterior kans P(A|B) met de regel van Bayes, a priori kansen en likelihood ratio's.",
            "pl": "Oblicz prawdopodobieństwo a posteriori P(A|B) z reguły Bayesa, ilorazów wiarygodności i wskaźników fałszywie dodatnich.",
            "sv": "Beräkna posterior sannolikhet P(A|B) med Bayes regel, a priori-odds och falskt positiva frekvenser.",
            "no": "Beregn posterior sannsynlighet P(A|B) med Bayes regel, a priori sannsynligheter og falske positive rater.",
            "fi": "Laske posterioritodennäköisyys P(A|B) Bayesin kaavalla, aprioritodennäköisyyksillä ja väärien positiivisten osuudella.",
            "ro": "Calculează probabilitatea a posteriori P(A|B) folosind Teorema lui Bayes, ratele de verosimilitate și fals pozitiv.",
        }
    }
]

ALL_LANG_CODES = ["en", "es", "fr", "de", "it", "pt", "nl", "pl", "sv", "no", "fi", "ro"]

def build_hreflang_tags(subpath: str) -> str:
    norm_path = subpath.strip("/")
    path_suffix = f"/{norm_path}/" if norm_path else "/"
    tags = []
    for code in ALL_LANG_CODES:
        if code == "en":
            url = f"https://omnioperand.com{path_suffix}"
        else:
            url = f"https://omnioperand.com/{code}{path_suffix}"
        tags.append(f'  <link rel="alternate" hreflang="{code}" href="{url}">')
    tags.append(f'  <link rel="alternate" hreflang="x-default" href="https://omnioperand.com{path_suffix}">')
    return "\n".join(tags)

def update_english_hreflangs():
    print("Updating English canonical pages with reciprocal hreflang links...")
    hreflang_regex = re.compile(r'(\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*">)+', re.MULTILINE)
    canonical_pattern = re.compile(r'(<link rel="canonical" href="[^"]*">)')

    for solver in BATCH2_SOLVERS:
        subpath = solver["subpath"]
        en_file = REPO_ROOT / subpath / "index.html"
        if not en_file.exists():
            print(f"  ⚠️ Warning: {en_file} does not exist!")
            continue

        content = en_file.read_text(encoding="utf-8")
        clean_content = hreflang_regex.sub("", content)
        hreflangs_str = build_hreflang_tags(subpath)

        if canonical_pattern.search(clean_content):
            new_content = canonical_pattern.sub(r'\1\n' + hreflangs_str, clean_content, count=1)
            en_file.write_text(new_content, encoding="utf-8")
        else:
            print(f"  ⚠️ Canonical link missing in {en_file}")

    print(f"  ✅ {len(BATCH2_SOLVERS)} English canonical pages updated with reciprocal hreflangs.")

def localize_page(content: str, lang_code: str, solver: dict) -> str:
    dict_data = LANGUAGES[lang_code]
    subpath = solver["subpath"]
    norm_path = subpath.strip("/")
    path_suffix = f"/{norm_path}/" if norm_path else "/"
    localized_url = f"https://omnioperand.com/{lang_code}{path_suffix}"

    res = re.sub(r'<html lang="en"', f'<html lang="{lang_code}"', content)
    res = re.sub(
        r'<link rel="canonical" href="https://omnioperand.com/[^"]*">',
        f'<link rel="canonical" href="{localized_url}">',
        res
    )

    # Reciprocal hreflangs
    hreflangs_str = build_hreflang_tags(subpath)
    res = re.sub(r'(\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*">)+', "", res)
    res = re.sub(r'(<link rel="canonical" href="[^"]*">)', r'\1\n' + hreflangs_str, res, count=1)

    # Localized Title and Description
    new_title = solver["titles"].get(lang_code, solver["titles"]["en"])
    new_desc = solver["descriptions"].get(lang_code, solver["descriptions"]["en"])

    res = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', res, flags=re.DOTALL)
    res = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{new_desc}">', res, flags=re.DOTALL)
    res = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{new_title}">', res, flags=re.DOTALL)
    res = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{new_desc}">', res, flags=re.DOTALL)
    res = re.sub(r'<meta property="og:url" content=".*?">', f'<meta property="og:url" content="{localized_url}">', res, flags=re.DOTALL)

    # Update JSON-LD Schema
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
                        if item.get("itemListElement") and len(item["itemListElement"]) > 0:
                            item["itemListElement"][0]["name"] = dict_data["home"]
                            item["itemListElement"][0]["item"] = f"https://omnioperand.com/{lang_code}/"
                            if len(item["itemListElement"]) > 1:
                                cat = solver["category"]
                                cat_name = dict_data.get(cat, cat.capitalize())
                                item["itemListElement"][1]["name"] = cat_name
                                item["itemListElement"][1]["item"] = f"https://omnioperand.com/{lang_code}/{cat}/"
                            if len(item["itemListElement"]) > 2:
                                item["itemListElement"][-1]["name"] = new_title.split(" — ")[0].split(" | ")[0]
                                item["itemListElement"][-1]["item"] = localized_url
            return f'<script type="application/ld+json">\n{json.dumps(ld_obj, indent=2, ensure_ascii=False)}\n</script>'
        except Exception:
            return match.group(0)

    res = re.sub(r'<script type="application/ld\+json">(.*?)</script>', update_json_ld, res, flags=re.DOTALL)

    # Localize Breadcrumb UI links
    res = re.sub(r'<a href="/">Home</a>', f'<a href="/{lang_code}/">{dict_data["home"]}</a>', res)
    res = re.sub(r'<a href="/geometry/">Geometry</a>', f'<a href="/{lang_code}/geometry/">{dict_data["geometry"]}</a>', res)
    res = re.sub(r'<a href="/statistics/">Statistics</a>', f'<a href="/{lang_code}/statistics/">{dict_data["statistics"]}</a>', res)

    page_short_name = new_title.split(" — ")[0].split(" | ")[0]
    res = re.sub(r'<li class="breadcrumb-item active" aria-current="page">.*?</li>', f'<li class="breadcrumb-item active" aria-current="page">{page_short_name}</li>', res)

    # Localize Hero H1
    res = re.sub(r'<h1>(?:Regular )?[A-Za-z0-9 &–—\(\),/]+(?:Calculator|Solver)?</h1>', f'<h1>{page_short_name}</h1>', res, count=1)
    res = re.sub(r'<p class="hero-subtext">.*?</p>', f'<p class="hero-subtext">{new_desc}</p>', res, count=1, flags=re.DOTALL)

    # Localize common headings
    res = re.sub(r'<h2>Parameters &amp; Inversions</h2>', f'<h2>{dict_data["params_title"]}</h2>', res)
    res = re.sub(r'<h2>Parameters &amp; Input Variables</h2>', f'<h2>{dict_data["params_title"]}</h2>', res)
    res = re.sub(r'<h2>Calculated Output Metrics</h2>', f'<h2>{dict_data["derived_results"]}</h2>', res)
    res = re.sub(r'<h3><span>Step-by-Step Mathematical Derivation</span></h3>', f'<h3><span>{dict_data["step_by_step"]}</span></h3>', res)
    res = re.sub(r'<h2>Frequently Asked Questions</h2>', f'<h2>{dict_data["faq_title"]}</h2>', res)
    res = re.sub(r'placeholder="Search calculators\.\.\."', f'placeholder="{dict_data["search_placeholder"]}"', res)

    return res

def generate_batch2_pages():
    print(f"\n🚀 Generating Batch 2 localized pages across {len(LANGUAGES)} languages...")
    total_created = 0

    for lang_code, dict_data in LANGUAGES.items():
        print(f"\n🌍 Generating for {dict_data['name']} ({lang_code})...")
        lang_count = 0

        for solver in BATCH2_SOLVERS:
            subpath = solver["subpath"]
            en_file = REPO_ROOT / subpath / "index.html"
            if not en_file.exists():
                print(f"  ⚠️ Skipping missing source: {en_file}")
                continue

            content = en_file.read_text(encoding="utf-8")
            localized_html = localize_page(content, lang_code, solver)

            target_dir = REPO_ROOT / lang_code / subpath
            target_dir.mkdir(parents=True, exist_ok=True)
            target_file = target_dir / "index.html"
            target_file.write_text(localized_html, encoding="utf-8")

            lang_count += 1
            total_created += 1

        print(f"  ✅ {lang_count} pages created for {lang_code}.")

    print(f"\n🎉 Successfully created {total_created} Batch 2 localized HTML pages!")

def update_sitemap():
    print("\nUpdating sitemap.xml with all canonical and localized URLs...")
    sitemap_path = REPO_ROOT / "sitemap.xml"

    # Scan entire repo for all index.html files (canonical & localized)
    all_urls = {}
    for p in REPO_ROOT.glob("**/index.html"):
        if ".git" in p.parts or "scratch" in p.parts:
            continue
        rel = p.parent.relative_to(REPO_ROOT)
        if str(rel) == ".":
            url = "https://omnioperand.com/"
            prio = "1.0"
            freq = "weekly"
        else:
            url = f"https://omnioperand.com/{rel}/"
            # Prioritize canonical English solvers higher
            parts = str(rel).split("/")
            if parts[0] in LANGUAGES:
                prio = "0.8"
                freq = "weekly"
            elif len(parts) <= 2:
                prio = "0.9"
                freq = "weekly"
            else:
                prio = "0.85"
                freq = "weekly"
        all_urls[url] = (prio, freq)

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for url in sorted(all_urls.keys()):
        prio, freq = all_urls[url]
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{url}</loc>")
        xml_lines.append("    <lastmod>2026-10-24</lastmod>")
        xml_lines.append(f"    <changefreq>{freq}</changefreq>")
        xml_lines.append(f"    <priority>{prio}</priority>")
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>\n")

    sitemap_path.write_text("\n".join(xml_lines), encoding="utf-8")
    print(f"  ✅ sitemap.xml updated with {len(all_urls)} total indexed URLs!")

def main():
    print("=========================================================")
    print("🚀 OmniOperand Batch 2 Multi-Language Generation")
    print("=========================================================")
    update_english_hreflangs()
    generate_batch2_pages()

    # Synchronize headers, language selector dropdowns across all pages
    print("\nSynchronizing headers and language switchers...")
    try:
        from unify_headers import unify_all_headers
        unify_all_headers()
    except Exception as e:
        print(f"  ⚠️ Warning during header unification: {e}")

    update_sitemap()
    print("\n✅ Batch 2 generation complete!")

if __name__ == "__main__":
    main()
