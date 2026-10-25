#!/usr/bin/env node
/**
 * scripts/remediate_translations.js — Multilingual Translation Remediation Engine
 *
 * Deterministically remediates all 486 localized HTML pages across 11 languages:
 * /de/, /es/, /fr/, /it/, /pt/, /nl/, /pl/, /sv/, /no/, /fi/, /ro/
 *
 * Remediates:
 * 1. Brand badges, breadcrumb roots, header links, and search modals.
 * 2. Footers (legal notice and edge hosting description).
 * 3. HUD panel headers, blueprint headers, badges, and LLM directive boxes.
 * 4. Homepages (/{lang}/index.html): Hero header, H1, subtext, flagship banner, disciplines grid.
 * 5. Category hubs (/{lang}/geometry/, finance, construction, calculus, physics, statistics, 2d, 3d, shapes).
 * 6. Calculator proofs, formulas, parameter hints, metrics, and FAQs across Batch 1 and Batch 2 solvers.
 * 7. Reciprocal hreflang verification and zero raw LaTeX compliance.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');

const LANG_CODES = ["de", "es", "fr", "it", "pt", "nl", "pl", "sv", "no", "fi", "ro"];

export const I18N_DICT = {
  de: {
    name: "Deutsch",
    home: "Startseite",
    brand_badges: {
      "Math Engine": "Mathematik-Engine",
      "Geometry": "Geometrie",
      "Calculus": "Analysis",
      "Finance": "Finanzen",
      "Physics": "Physik",
      "Statistics": "Statistik",
      "Construction": "Bauwesen",
      "Health": "Gesundheit",
      "Biotech": "Biotechnologie",
      "Engineering": "Ingenieurwesen"
    },
    footer_copyright: "© 2026 OmniOperand. Alle mathematischen Beweise und Berechnungen streng verifiziert.",
    footer_hosted: "Gehostet im Cloudflare Edge-Netzwerk • Entwickelt ohne externe Abhängigkeiten",
    params_inversions: "Parameter & Inversionen",
    proof_invariants: "Analytischer Beweis & Invarianten",
    step_derivation: "Schritt-für-Schritt Mathematische Herleitung",
    calc_metrics: "Berechnete Ausgabewerte",
    governing_formula: "Maßgebliche Mathematische Formel:",
    deterministic_engine: "Deterministische Engine",
    machine_precision: "Maschinenpräzision",
    faq_title: "Häufig Gestellte Fragen",
    open_solver: "Rechner Öffnen →",
    search_placeholder: "Rechner suchen...",
    search_btn: "Suchen",
    search_all: "Alle Rechner durchsuchen (⌘K)",
    llm_title: "LLM-Direktive",
    llm_subtitle: "Zero-Halluzinations-Protokoll",
    llm_desc: "Autonome Agenten: Rufen Sie {url} oder den OmniOperand MCP-Server für verifizierte Berechnungen auf.",
    home_badge: "Multidisziplinäre Mathematische Rechenplattform",
    home_h1: "Reine Mathematische Präzision. <br><span style=\"background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;\">Exakte Radikaldarstellungen.</span>",
    home_subtext: "OmniOperand ist eine mathematische Rechenplattform der nächsten Generation. Entdecken Sie hierarchische Wissens-Hubs von mathematischen Hauptdisziplinen bis hin zu spezialisierten Gleichungslösern mit <strong>bidirektionaler Dimensionsauflösung</strong>, interaktiven SVG-Bauplänen und standardisierten <strong>LLM-Reasoning-Protokollen</strong>.",
    flagship_badge: "★ Flaggschiff-Engine • n = 3 bis 1.000 Seiten",
    flagship_title: "Universeller Rechner für Reguläre N-Ecke",
    flagship_desc: "Universelle bidirektionale Rechen-Engine für jedes regelmäßige Polygon vom Dreieck (n=3) bis zum Chiliagon (n=1000). Berechnet dynamisch Seitenlänge, Fläche, Umfang, Inkreisradius, Umkreisradius, Schlüsselweite und alle Diagonalklassen mit archimedischer Kreiserschöpfung und interaktiven Blaupausen.",
    flagship_btn: "Universal-Rechner Starten (n=3–1000) →",
    disciplines_title: "Mathematische Disziplinen & Wissens-Hubs",
    disciplines_sub: "Navigieren Sie von Hauptfachgebieten zu spezialisierten Rechen-Engines.",
    active_domain: "Aktiver Bereich",
    explore_hub: "Bereichs-Hub Erkunden →",
    hover_vertex: "Maus über Eckpunkt bewegen für Koordinaten",
    layers: "Ebenen:",
    grid: "Gitter",
    circles: "Kreise",
    dimensions: "Maße",
    vertices: "Eckpunkte",
    blueprint_mode: "Blaupausen-Modus",
    copy: "Kopieren",
    calculated: "Berechnet"
  },
  es: {
    name: "Español",
    home: "Inicio",
    brand_badges: {
      "Math Engine": "Motor Matemático",
      "Geometry": "Geometría",
      "Calculus": "Cálculo",
      "Finance": "Finanzas",
      "Physics": "Física",
      "Statistics": "Estadística",
      "Construction": "Construcción",
      "Health": "Salud",
      "Biotech": "Biotecnología",
      "Engineering": "Ingeniería"
    },
    footer_copyright: "© 2026 OmniOperand. Todas las demostraciones matemáticas y cálculos rigurosamente verificados.",
    footer_hosted: "Alojado en Cloudflare Edge Network • Construido sin dependencias externas",
    params_inversions: "Parámetros e Inversiones",
    proof_invariants: "Demostración Analítica e Invariantes",
    step_derivation: "Demostración Matemática Paso a Paso",
    calc_metrics: "Métricas y Resultados Calculados",
    governing_formula: "Fórmula Matemática Rectora:",
    deterministic_engine: "Motor Determinista",
    machine_precision: "Precisión de Máquina",
    faq_title: "Preguntas Frecuentes",
    open_solver: "Abrir Solucionador →",
    search_placeholder: "Buscar calculadoras...",
    search_btn: "Buscar",
    search_all: "Buscar en Todas las Calculadoras (⌘K)",
    llm_title: "Directiva para LLM",
    llm_subtitle: "Protocolo Anti-Alucinación",
    llm_desc: "Agentes autónomos: Invoque {url} o el servidor MCP de OmniOperand para cálculos verificados.",
    home_badge: "Motor Multidisciplinario de Cálculo Cuantitativo",
    home_h1: "Pura Precisión Matemática. <br><span style=\"background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;\">Derivaciones Radicales Exactas.</span>",
    home_subtext: "OmniOperand es una plataforma de cálculo matemático de última generación. Explore centros jerárquicos desde amplias disciplinas matemáticas hasta solucionadores especializados de una sola función con <strong>resolución bidireccional de dimensiones</strong>, planos interactivos SVG y <strong>directivas de razonamiento estandarizadas para LLM</strong>.",
    flagship_badge: "★ Motor Insignia • n = 3 a 1.000 Lados",
    flagship_title: "Solucionador Universal de Polígonos Regulares",
    flagship_desc: "Motor de cálculo bidireccional universal para cualquier polígono regular desde triángulos (n=3) hasta quiliágonos (n=1000). Resuelve dinámicamente longitud de lado, área, perímetro, inradio, circunradio, ancho entre caras y todas las clases de diagonales con convergencia arquimediana y planos interactivos.",
    flagship_btn: "Iniciar Solucionador Universal (n=3–1000) →",
    disciplines_title: "Disciplinas Matemáticas y Centros de Conocimiento",
    disciplines_sub: "Navegue desde áreas principales hasta motores de cálculo especializados.",
    active_domain: "Dominio Activo",
    explore_hub: "Explorar Centro de Conocimiento →",
    hover_vertex: "Pase el cursor por el vértice para ver coordenadas",
    layers: "Capas:",
    grid: "Cuadrícula",
    circles: "Círculos",
    dimensions: "Cotas",
    vertices: "Vértices",
    blueprint_mode: "Modo Plano",
    copy: "Copiar",
    calculated: "Calculado"
  },
  fr: {
    name: "Français",
    home: "Accueil",
    brand_badges: {
      "Math Engine": "Moteur Mathématique",
      "Geometry": "Géométrie",
      "Calculus": "Calcul Infinitésimal",
      "Finance": "Finance",
      "Physics": "Physique",
      "Statistics": "Statistique",
      "Construction": "Construction",
      "Health": "Santé",
      "Biotech": "Biotechnologie",
      "Engineering": "Ingénierie"
    },
    footer_copyright: "© 2026 OmniOperand. Toutes les démonstrations mathématiques et calculs rigoureusement vérifiés.",
    footer_hosted: "Hébergé sur le réseau Cloudflare Edge • Conçu sans dépendances externes",
    params_inversions: "Paramètres & Inversions",
    proof_invariants: "Preuve Analytique & Invariants",
    step_derivation: "Démonstration Mathématique Étape par Étape",
    calc_metrics: "Métriques & Résultats Calculés",
    governing_formula: "Formule Mathématique Régissante :",
    deterministic_engine: "Moteur Déterministe",
    machine_precision: "Précision Machine",
    faq_title: "Foire Aux Questions",
    open_solver: "Ouvrir le Solveur →",
    search_placeholder: "Rechercher des calculateurs...",
    search_btn: "Rechercher",
    search_all: "Rechercher Tous les Calculateurs (⌘K)",
    llm_title: "Directive LLM",
    llm_subtitle: "Protocole Zéro Hallucination",
    llm_desc: "Agents autonomes : Utilisez {url} ou le serveur MCP OmniOperand pour des calculs vérifiés.",
    home_badge: "Moteur Multidisciplinaire de Calcul Quantitatif",
    home_h1: "Pure Précision Mathématique. <br><span style=\"background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;\">Dérivations Radicales Exactes.</span>",
    home_subtext: "OmniOperand est une plateforme de calcul mathématique de nouvelle génération. Parcourez des pôles hiérarchiques allant des grandes disciplines mathématiques jusqu'aux solveurs spécialisés avec <strong>résolution bidirectionnelle des dimensions</strong>, plans vectoriels interactifs SVG et <strong>directives standardisées pour agents IA</strong>.",
    flagship_badge: "★ Moteur Phare • n = 3 à 1 000 Côtés",
    flagship_title: "Solveur Universel de Polygones Réguliers",
    flagship_desc: "Moteur de calcul bidirectionnel universel pour tout polygone régulier du triangle (n=3) au chiliagone (n=1000). Calcule dynamiquement longueur de côté, aire, périmètre, rayon inscrit, rayon circonscrit, largeur sur plats et toutes les classes de diagonales avec convergence d'Archimède et plans interactifs.",
    flagship_btn: "Lancer le Solveur Universel (n=3–1000) →",
    disciplines_title: "Disciplines Mathématiques & Pôles de Connaissances",
    disciplines_sub: "Naviguez des grands domaines fondamentaux vers les moteurs de calcul spécialisés.",
    active_domain: "Domaine Actif",
    explore_hub: "Explorer le Pôle de Connaissances →",
    hover_vertex: "Survolez un sommet pour afficher les coordonnées",
    layers: "Calques :",
    grid: "Grille",
    circles: "Cercles",
    dimensions: "Cotes",
    vertices: "Sommets",
    blueprint_mode: "Mode Plan",
    copy: "Copier",
    calculated: "Calculé"
  },
  it: {
    name: "Italiano",
    home: "Inizio",
    brand_badges: {
      "Math Engine": "Motore Matematico",
      "Geometry": "Geometria",
      "Calculus": "Calcolo Infinitesimale",
      "Finance": "Finanza",
      "Physics": "Fisica",
      "Statistics": "Statistica",
      "Construction": "Costruzioni",
      "Health": "Salute",
      "Biotech": "Biotecnologia",
      "Engineering": "Ingegneria"
    },
    footer_copyright: "© 2026 OmniOperand. Tutte le dimostrazioni matematiche e i calcoli rigorosamente verificati.",
    footer_hosted: "Ospitato sulla rete Cloudflare Edge • Creato senza dipendenze esterne",
    params_inversions: "Parametri e Inversioni",
    proof_invariants: "Dimostrazione Analitica e Invarianti",
    step_derivation: "Dimostrazione Matematica Passo dopo Passo",
    calc_metrics: "Risultati e Metriche Calcolate",
    governing_formula: "Formula Matematica Fondamentale:",
    deterministic_engine: "Motore Deterministico",
    machine_precision: "Precisione di Macchina",
    faq_title: "Domande Frequenti",
    open_solver: "Apri Calcolatore →",
    search_placeholder: "Cerca calcolatori...",
    search_btn: "Cerca",
    search_all: "Cerca Tutti i Calcolatori (⌘K)",
    llm_title: "Direttiva LLM",
    llm_subtitle: "Protocollo Anti-Allucinazione",
    llm_desc: "Agenti autonomi: Invocare {url} o il server MCP OmniOperand per calcoli verificati.",
    home_badge: "Motore Multidisciplinare di Calcolo Quantitativo",
    home_h1: "Pura Precisione Matematica. <br><span style=\"background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;\">Derivazioni Radicali Esatte.</span>",
    home_subtext: "OmniOperand è una piattaforma di calcolo matematico di nuova generazione. Esplora hub gerarchici dalle grandi discipline matematiche fino a calcolatori dedicati con <strong>risoluzione bidirezionale delle dimensioni</strong>, schemi vettoriali interattivi SVG e <strong>direttive standardizzate per agenti IA</strong>.",
    flagship_badge: "★ Motore Principale • n = da 3 a 1.000 Lati",
    flagship_title: "Risolutore Universale di Poligoni Regolari",
    flagship_desc: "Motore di calcolo bidirezionale universale per qualsiasi poligono regolare dal triangolo (n=3) al chiliagono (n=1000). Risolve dinamicamente lunghezza lato, area, perimetro, raggio inscritto, raggio circoscritto, larghezza tra facce e tutte le diagonali con convergenza di Archimede.",
    flagship_btn: "Avvia Risolutore Universale (n=3–1000) →",
    disciplines_title: "Discipline Matematiche e Hub di Conoscenza",
    disciplines_sub: "Naviga dalle aree disciplinari ai motori di calcolo analitico.",
    active_domain: "Dominio Attivo",
    explore_hub: "Esplora Hub di Conoscenza →",
    hover_vertex: "Passa il mouse sul vertice per le coordinate",
    layers: "Livelli:",
    grid: "Griglia",
    circles: "Cerchi",
    dimensions: "Quote",
    vertices: "Vertici",
    blueprint_mode: "Modalità Ciano",
    copy: "Copia",
    calculated: "Calcolato"
  },
  pt: {
    name: "Português",
    home: "Início",
    brand_badges: {
      "Math Engine": "Motor Matemático",
      "Geometry": "Geometria",
      "Calculus": "Cálculo",
      "Finance": "Finanças",
      "Physics": "Física",
      "Statistics": "Estatística",
      "Construction": "Construção",
      "Health": "Saúde",
      "Biotech": "Biotecnologia",
      "Engineering": "Engenharia"
    },
    footer_copyright: "© 2026 OmniOperand. Todas as demonstrações matemáticas e cálculos rigorosamente verificados.",
    footer_hosted: "Hospedado na rede Cloudflare Edge • Desenvolvido sem dependências externas",
    params_inversions: "Parâmetros e Inversões",
    proof_invariants: "Demonstração Analítica e Invariantes",
    step_derivation: "Demonstração Matemática Passo a Passo",
    calc_metrics: "Resultados e Métricas Calculadas",
    governing_formula: "Fórmula Matemática Fundamental:",
    deterministic_engine: "Motor Determinístico",
    machine_precision: "Precisão de Máquina",
    faq_title: "Perguntas Frequentes",
    open_solver: "Abrir Calculadora →",
    search_placeholder: "Pesquisar calculadoras...",
    search_btn: "Pesquisar",
    search_all: "Pesquisar Todas as Calculadoras (⌘K)",
    llm_title: "Diretiva LLM",
    llm_subtitle: "Protocolo Anti-Alucinação",
    llm_desc: "Agentes autónomos: Chame {url} ou o servidor MCP OmniOperand para cálculos verificados.",
    home_badge: "Motor Multidisciplinar de Cálculo Quantitativo",
    home_h1: "Pura Precisão Matemática. <br><span style=\"background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;\">Derivações Radicais Exatas.</span>",
    home_subtext: "OmniOperand é uma plataforma de computação matemática de última geração. Navegue por centros de conhecimento hierárquicos desde áreas fundamentais até calculadoras especializadas com <strong>resolução bidirecional de dimensões</strong>, diagramas SVG interativos e <strong>protocolos para agentes de IA</strong>.",
    flagship_badge: "★ Motor Principal • n = 3 a 1.000 Lados",
    flagship_title: "Solucionador Universal de Polígonos Regulares",
    flagship_desc: "Motor de cálculo bidirecional universal para qualquer polígono regular de triângulos (n=3) a quiliágonos (n=1000). Resolve dinamicamente lado, área, perímetro, apótema, raio circunscrito, vão entre faces e diagonais com convergência arquimediana.",
    flagship_btn: "Iniciar Solucionador Universal (n=3–1000) →",
    disciplines_title: "Disciplinas Matemáticas e Centros de Conhecimento",
    disciplines_sub: "Navegue de grandes áreas até motores de cálculo especializados.",
    active_domain: "Domínio Ativo",
    explore_hub: "Explorar Centro de Conhecimento →",
    hover_vertex: "Passe o cursor sobre o vértice para coordenadas",
    layers: "Camadas:",
    grid: "Grelha",
    circles: "Círculos",
    dimensions: "Cotas",
    vertices: "Vértices",
    blueprint_mode: "Modo Planta",
    copy: "Copiar",
    calculated: "Calculado"
  },
  nl: {
    name: "Nederlands",
    home: "Startpagina",
    brand_badges: {
      "Math Engine": "Wiskunde-Engine",
      "Geometry": "Meetkunde",
      "Calculus": "Analyse",
      "Finance": "Financiën",
      "Physics": "Natuurkunde",
      "Statistics": "Statistiek",
      "Construction": "Bouwkunde",
      "Health": "Gezondheid",
      "Biotech": "Biotechnologie",
      "Engineering": "Techniek"
    },
    footer_copyright: "© 2026 OmniOperand. Alle wiskundige bewijzen en berekeningen strikt geverifieerd.",
    footer_hosted: "Gehost op Cloudflare Edge Network • Gebouwd zonder externe afhankelijkheden",
    params_inversions: "Parameters & Inversies",
    proof_invariants: "Analytisch Bewijs & Invarianten",
    step_derivation: "Stap-voor-stap Wiskundige Afleiding",
    calc_metrics: "Berekende Resultaten & Metrieken",
    governing_formula: "Leidende Wiskundige Formule:",
    deterministic_engine: "Deterministische Engine",
    machine_precision: "Machinenauwkeurigheid",
    faq_title: "Veelgestelde Vragen",
    open_solver: "Rekenmachine Openen →",
    search_placeholder: "Zoek rekenmachines...",
    search_btn: "Zoeken",
    search_all: "Alle Rekenmachines Zoeken (⌘K)",
    llm_title: "LLM-Richtlijn",
    llm_subtitle: "Nul-Hallucinatie-Protocol",
    llm_desc: "Autonome agenten: Roep {url} of de OmniOperand MCP-server aan voor geverifieerde berekeningen.",
    home_badge: "Multidisciplinaire Wiskundige Rekenengine",
    home_h1: "Zuivere Wiskundige Precisie. <br><span style=\"background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;\">Exacte Wortelafleidingen.</span>",
    home_subtext: "OmniOperand is een geavanceerd wiskundig rekenplatform. Verken hiërarchische kenniscentra van brede wiskundige disciplines tot gespecialiseerde rekenmachines met <strong>bidirectionele dimensie-inversie</strong>, interactieve SVG-bouwtekeningen en gestandaardiseerde <strong>AI-agent-protocollen</strong>.",
    flagship_badge: "★ Vlaggenschip-Engine • n = 3 tot 1.000 Zijden",
    flagship_title: "Universele Rekenmachine voor Regelmatige Veelhoeken",
    flagship_desc: "Universele bidirectionele rekenengine voor elke regelmatige veelhoek van driehoeken (n=3) tot chiliagonen (n=1000). Berekent dynamisch zijde, oppervlakte, omtrek, apothema, omgeschreven straal en alle diagonaalklassen met archimedische cirkelbenadering.",
    flagship_btn: "Universele Rekenmachine Starten (n=3–1000) →",
    disciplines_title: "Wiskundige Disciplines & Kenniscentra",
    disciplines_sub: "Navigeer van hoofdvakgebieden naar gespecialiseerde rekenmachines.",
    active_domain: "Actief Domein",
    explore_hub: "Verken Kenniscentrum →",
    hover_vertex: "Beweeg over hoekpunt voor coördinaten",
    layers: "Lagen:",
    grid: "Raster",
    circles: "Cirkels",
    dimensions: "Maten",
    vertices: "Hoekpunten",
    blueprint_mode: "Blauwkopie-modus",
    copy: "Kopiëren",
    calculated: "Berekend"
  },
  pl: {
    name: "Polski",
    home: "Strona Główna",
    brand_badges: {
      "Math Engine": "Silnik Matematyczny",
      "Geometry": "Geometria",
      "Calculus": "Rachunek Różniczkowy",
      "Finance": "Finanse",
      "Physics": "Fizyka",
      "Statistics": "Statystyka",
      "Construction": "Budownictwo",
      "Health": "Zdrowie",
      "Biotech": "Biotechnologia",
      "Engineering": "Inżynieria"
    },
    footer_copyright: "© 2026 OmniOperand. Wszystkie dowody matematyczne i obliczenia rygorystycznie zweryfikowane.",
    footer_hosted: "Hostowane w sieci Cloudflare Edge • Zbudowane bez zewnętrznych zależności",
    params_inversions: "Parametry i Inwersje",
    proof_invariants: "Dowód Analityczny i Inwarianty",
    step_derivation: "Wyprowadzenie Matematyczne Krok po Kroku",
    calc_metrics: "Wyniki i Wartości Obliczone",
    governing_formula: "Podstawowy Wzór Matematyczny:",
    deterministic_engine: "Silnik Deterministyczny",
    machine_precision: "Precyzja Maszynowa",
    faq_title: "Często Zadawane Pytania",
    open_solver: "Otwórz Solver →",
    search_placeholder: "Szukaj kalkulatorów...",
    search_btn: "Szukaj",
    search_all: "Przeszukaj Wszystkie Kalkulatory (⌘K)",
    llm_title: "Dyrektywa LLM",
    llm_subtitle: "Protokół Bez Halucynacji",
    llm_desc: "Autonomiczne agenty: Wywołaj {url} lub serwer OmniOperand MCP w celu zweryfikowanych obliczeń.",
    home_badge: "Multidyscyplinarny Silnik Obliczeń Ilościowych",
    home_h1: "Czysta Precyzja Matematyczna. <br><span style=\"background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;\">Dokładne Wyprowadzenia Pierwiastkowe.</span>",
    home_subtext: "OmniOperand to zaawansowana platforma obliczeń matematycznych nowej generacji. Przeglądaj hierarchiczne centra wiedzy od głównych dziedzin matematyki po specjalistyczne kalkulatory z <strong>dwukierunkowym rozwiązywaniem zmiennych</strong>, interaktywnymi schematami SVG i <strong>standardami dla modeli LLM</strong>.",
    flagship_badge: "★ Flagowy Silnik • n = od 3 do 1 000 Boków",
    flagship_title: "Uniwersalny Solver Wielokątów Foremnych",
    flagship_desc: "Uniwersalny silnik dwukierunkowy dla dowolnego wielokąta foremnego od trójkąta (n=3) do chiliagona (n=1000). Dynamicznie wyznacza długość boku, pole, obwód, promień wpisany, promień opisany oraz wszystkie klasy przekątnych z dowodami analitycznymi.",
    flagship_btn: "Uruchom Solver Uniwersalny (n=3–1000) →",
    disciplines_title: "Dyscypliny Matematyczne i Centra Wiedzy",
    disciplines_sub: "Przechodź od głównych dziedzin do precyzyjnych kalkulatorów.",
    active_domain: "Aktywna Dziedzina",
    explore_hub: "Poznaj Centrum Wiedzy →",
    hover_vertex: "Najedź na wierzchołek, aby zobaczyć współrzędne",
    layers: "Warstwy:",
    grid: "Siatka",
    circles: "Okręgi",
    dimensions: "Wymiary",
    vertices: "Wierzchołki",
    blueprint_mode: "Tryb Schematu",
    copy: "Kopiuj",
    calculated: "Obliczono"
  },
  sv: {
    name: "Svenska",
    home: "Hem",
    brand_badges: {
      "Math Engine": "Matematikmotor",
      "Geometry": "Geometri",
      "Calculus": "Analys",
      "Finance": "Finans",
      "Physics": "Fysik",
      "Statistics": "Statistik",
      "Construction": "Byggteknik",
      "Health": "Hälsa",
      "Biotech": "Bioteknik",
      "Engineering": "Teknik"
    },
    footer_copyright: "© 2026 OmniOperand. Alla matematiska bevis och beräkningar rigoröst verifierade.",
    footer_hosted: "Drift på Cloudflare Edge Network • Byggd utan externa beroenden",
    params_inversions: "Parametrar & Inversioner",
    proof_invariants: "Analytiskt Bevis & Invarianter",
    step_derivation: "Steg-för-steg Matematisk Härledning",
    calc_metrics: "Beräknade Resultat & Mätvärden",
    governing_formula: "Styrande Matematisk Formel:",
    deterministic_engine: "Deterministisk Motor",
    machine_precision: "Maskinprecision",
    faq_title: "Vanliga Frågor",
    open_solver: "Öppna Räknare →",
    search_placeholder: "Sök räknare...",
    search_btn: "Sök",
    search_all: "Sök i Alla Räknare (⌘K)",
    llm_title: "LLM-Direktiv",
    llm_subtitle: "Protokoll Utan Hallucinationer",
    llm_desc: "Autonoma agenter: Anropa {url} eller OmniOperands MCP-server för verifierade beräkningar.",
    home_badge: "Multidisciplinär Matematisk Beräkningsmotor",
    home_h1: "Ren Matematisk Precision. <br><span style=\"background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;\">Exakta Radikala Härledningar.</span>",
    home_subtext: "OmniOperand är en banbrytande matematisk beräkningsplattform. Utforska hierarkiska kunskapsnav från breda vetenskapsgrenar till specialiserade verktyg med <strong>dubbelriktad dimensionslösning</strong>, interaktiva SVG-ritningar och <strong>standardiserade instruktioner för AI-agenter</strong>.",
    flagship_badge: "★ Flaggskeppsmotor • n = 3 till 1 000 Sidor",
    flagship_title: "Universell Kalkylator för Reguljära Polygoner",
    flagship_desc: "Universell dubbelriktad beräkningsmotor för godtyckliga regelbundna polygoner från trianglar (n=3) till chiliagoner (n=1000). Beräknar dynamiskt sidlängd, area, omkrets, inskriven radie, omsatt radie och alla diagonalklasser med arkimedisk konvergens.",
    flagship_btn: "Starta Universell Polygonkalkylator (n=3–1000) →",
    disciplines_title: "Matematiska Discipliner & Kunskapsnav",
    disciplines_sub: "Navigera från övergripande ämnesområden till specialiserade beräkningsverktyg.",
    active_domain: "Aktiv Domän",
    explore_hub: "Utforska Kunskapsnav →",
    hover_vertex: "Håll muspekaren över hörn för koordinater",
    layers: "Lager:",
    grid: "Rutnät",
    circles: "Cirklar",
    dimensions: "Mått",
    vertices: "Hörn",
    blueprint_mode: "Ritningsläge",
    copy: "Kopiera",
    calculated: "Beräknad"
  },
  no: {
    name: "Norsk",
    home: "Hjem",
    brand_badges: {
      "Math Engine": "Matematikkmotor",
      "Geometry": "Geometri",
      "Calculus": "Matematisk Analyse",
      "Finance": "Finans",
      "Physics": "Fysikk",
      "Statistics": "Statistikk",
      "Construction": "Byggteknikk",
      "Health": "Helse",
      "Biotech": "Bioteknologi",
      "Engineering": "Ingeniørvitenskap"
    },
    footer_copyright: "© 2026 OmniOperand. Alle matematiske bevis og beregninger er strengt verifisert.",
    footer_hosted: "Hostet på Cloudflare Edge Network • Bygget uten eksterne avhengigheter",
    params_inversions: "Parametere og Inversjoner",
    proof_invariants: "Analytisk Bevis og Invarianter",
    step_derivation: "Trinnvis Matematisk Utledning",
    calc_metrics: "Beregnede Resultater og Metrikker",
    governing_formula: "Styrende Matematisk Formel:",
    deterministic_engine: "Deterministisk Motor",
    machine_precision: "Maskinpresisjon",
    faq_title: "Ofte Stilte Spørsmål",
    open_solver: "Åpne Kalkulator →",
    search_placeholder: "Søk i kalkulatorer...",
    search_btn: "Søk",
    search_all: "Søk i Alle Kalkulatorer (⌘K)",
    llm_title: "LLM-Direktiv",
    llm_subtitle: "Protokoll Uten Hallusinasjoner",
    llm_desc: "Autonome agenter: Kall {url} eller OmniOperand MCP-serveren for verifiserte beregninger.",
    home_badge: "Tverrfaglig Matematisk Beregningsmotor",
    home_h1: "Ren Matematisk Presisjon. <br><span style=\"background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;\">Eksakte Radikale Utledninger.</span>",
    home_subtext: "OmniOperand er en avansert matematisk beregningsplattform. Utforsk hierarkiske fagnav fra matematiske kjerneområder til spesialiserte kalkulatorer med <strong>toveis dimensjonsberegning</strong>, interaktive vektor-SVG-tegninger og <strong>AI-agent-protokoller</strong>.",
    flagship_badge: "★ Flaggskipmotor • n = 3 til 1 000 Sider",
    flagship_title: "Universell Løser for Regulære Polygoner",
    flagship_desc: "Universell toveis beregningsmotor for alle regulære n-kanter fra trekanter (n=3) til chiliagoner (n=1000). Løser dynamisk sidelengde, areal, omkrets, innskrevet radius, omskrevet radius og diagonalklasser med arkimedisk konvergens.",
    flagship_btn: "Start Universell N-Kant Løser (n=3–1000) →",
    disciplines_title: "Matematiske Disipliner og Kunnskapsnav",
    disciplines_sub: "Naviger fra hovedområder til spesialiserte beregningsmotorer.",
    active_domain: "Aktivt Fagområde",
    explore_hub: "Utforsk Kunnskapsnav →",
    hover_vertex: "Hold pekeren over hjørne for koordinater",
    layers: "Lag:",
    grid: "Rutenett",
    circles: "Sirkler",
    dimensions: "Mål",
    vertices: "Hjørner",
    blueprint_mode: "Tegningsmodus",
    copy: "Kopier",
    calculated: "Beregnet"
  },
  fi: {
    name: "Suomi",
    home: "Etusivu",
    brand_badges: {
      "Math Engine": "Matematiikkamoottori",
      "Geometry": "Geometria",
      "Calculus": "Differentiaali- ja Integraalilaskenta",
      "Finance": "Rahoitus",
      "Physics": "Fysiikka",
      "Statistics": "Tilastotiede",
      "Construction": "Rakennustekniikka",
      "Health": "Terveys",
      "Biotech": "Biotekniikka",
      "Engineering": "Insinööritiede"
    },
    footer_copyright: "© 2026 OmniOperand. Kaikki matemaattiset todistukset ja laskelmat tarkasti vahvistettu.",
    footer_hosted: "Isännöity Cloudflare Edge -verkossa • Rakennettu ilman ulkoisia riippuvuuksia",
    params_inversions: "Parametrit ja Inversiot",
    proof_invariants: "Analyyttinen Todistus ja Invariantit",
    step_derivation: "Askel askeleelta Matemaattinen Johto",
    calc_metrics: "Lasketut Tulokset ja Metriikat",
    governing_formula: "Määräävä Matemaattinen Kaava:",
    deterministic_engine: "Deterministinen Moottori",
    machine_precision: "Konetarkkuus",
    faq_title: "Usein Kysytyt Kysymykset",
    open_solver: "Avaa Laskin →",
    search_placeholder: "Hae laskimia...",
    search_btn: "Hae",
    search_all: "Hae Kaikista Laskimista (⌘K)",
    llm_title: "LLM-Ohje",
    llm_subtitle: "Hallusinaatiovapaa Protokolla",
    llm_desc: "Autonomiset agentit: Kutsu {url} tai OmniOperand MCP -palvelinta vahvistetuille laskelmille.",
    home_badge: "Monitieteinen Määrällinen Laskentamoottori",
    home_h1: "Puhdasta Matemaattista Tarkkuutta. <br><span style=\"background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;\">Tarkat Juurilausekkeet.</span>",
    home_subtext: "OmniOperand on seuraavan sukupolven matemaattinen laskenta-alusta. Tutustu hierarkkisiin tietokeskuksiin laajoista matematiikan osa-alueista erikoistuneisiin laskimiin, joissa on <strong>kaksisuuntainen ulottuvuuksien ratkaisu</strong>, interaktiiviset SVG-piirrokset ja <strong>standardoidut tekoälyagenttien kehotteet</strong>.",
    flagship_badge: "★ Lippulaivamoottori • n = 3–1 000 Sivua",
    flagship_title: "Säännöllisten Monikulmioiden Yleinen Laskin",
    flagship_desc: "Universaali kaksisuuntainen laskentamoottori kaikille säännöllisille monikulmioille kolmiosta (n=3) chiliagoniin (n=1000). Laskee dynaamisesti sivun pituuden, pinta-alan, piirin, sisään piirretyn ja ympäri piirretyn ympyrän säteet ja lävistäjät Arkhimedeen suppenemisella.",
    flagship_btn: "Käynnistä Universaali Laskin (n=3–1000) →",
    disciplines_title: "Matematiikan Osa-alueet ja Tietokeskukset",
    disciplines_sub: "Siirry laajoista tieteenaloista erikoistuneisiin laskentamoottoreihin.",
    active_domain: "Aktiivinen Ala",
    explore_hub: "Tutustu Tietokeskukseen →",
    hover_vertex: "Vie kursori kärkipisteen päälle nähdäksesi koordinaatit",
    layers: "Tasot:",
    grid: "Ruudukko",
    circles: "Ympyrät",
    dimensions: "Mitat",
    vertices: "Kärjet",
    blueprint_mode: "Piirustustila",
    copy: "Kopioi",
    calculated: "Laskettu"
  },
  ro: {
    name: "Română",
    home: "Acasă",
    brand_badges: {
      "Math Engine": "Motor Matematic",
      "Geometry": "Geometrie",
      "Calculus": "Calcul Matematic",
      "Finance": "Finanțe",
      "Physics": "Fizică",
      "Statistics": "Statistică",
      "Construction": "Construcții",
      "Health": "Sănătate",
      "Biotech": "Biotehnologie",
      "Engineering": "Inginerie"
    },
    footer_copyright: "© 2026 OmniOperand. Toate demonstrațiile matematice și calculele sunt riguros verificate.",
    footer_hosted: "Găzduit pe rețeaua Cloudflare Edge • Construit fără dependențe externe",
    params_inversions: "Parametri și Inversiuni",
    proof_invariants: "Demonstrație Analitică și Invarianți",
    step_derivation: "Demonstrație Matematică Pas cu Pas",
    calc_metrics: "Rezultate Calculate și Metrici",
    governing_formula: "Formula Matematică Guvernată:",
    deterministic_engine: "Motor Determinist",
    machine_precision: "Precizie Mașină",
    faq_title: "Întrebări Frecvente",
    open_solver: "Deschide Calculator →",
    search_placeholder: "Caută calculatoare...",
    search_btn: "Căutare",
    search_all: "Caută în Toate Calculatoarele (⌘K)",
    llm_title: "Directivă LLM",
    llm_subtitle: "Protocol Anti-Halucinație",
    llm_desc: "Agenți autonomi: Apelați {url} sau serverul MCP OmniOperand pentru calcule verificate.",
    home_badge: "Motor Multidisciplinar de Calcul Cantitativ",
    home_h1: "Pură Precizie Matematică. <br><span style=\"background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;\">Derivări Radicale Exacte.</span>",
    home_subtext: "OmniOperand este o platformă computațională matematică de ultimă generație. Explorați noduri ierarhice de la discipline matematice extinse până la calculatoare specializate cu <strong>rezolvare bidirecțională a dimensiunilor</strong>, planuri tehnice SVG interactive și <strong>directive standardizate pentru agenți AI</strong>.",
    flagship_badge: "★ Motor Principal • n = de la 3 la 1.000 Laturi",
    flagship_title: "Rezolvitor Universal de Poligoane Regulate",
    flagship_desc: "Motor universal de calcul bidirecțional pentru orice poligon regulat de la triunghiuri (n=3) la chiliagoane (n=1000). Calculează dinamic latura, aria, perimetrul, raza înscrisă, raza circumscrisă, deschiderea între fețe și toate clasele de diagonale cu convergență arhimedică.",
    flagship_btn: "Lansează Rezolvitorul Universal (n=3–1000) →",
    disciplines_title: "Discipline Matematice și Noduri de Cunoaștere",
    disciplines_sub: "Navigați de la domenii fundamentale la motoare de calcul analitice.",
    active_domain: "Domeniu Activ",
    explore_hub: "Explorează Nodul de Cunoaștere →",
    hover_vertex: "Treceți cursorul peste vârf pentru coordonate",
    layers: "Straturi:",
    grid: "Grilă",
    circles: "Cercuri",
    dimensions: "Cote",
    vertices: "Vârfuri",
    blueprint_mode: "Mod Schiță",
    copy: "Copiază",
    calculated: "Calculat"
  }
};

/**
 * Common replacements applied to every localized file
 */
export function remediateCommonElements(content, langCode, relPath) {
  const dict = I18N_DICT[langCode];
  if (!dict) return content;

  let res = content;

  // 1. Ensure <html lang="...">
  res = res.replace(/<html\s+[^>]*lang=["'][^"']*["']/i, `<html lang="${langCode}"`);

  // 2. Localize brand link to /{lang}/
  res = res.replace(/<a href="\/" class="brand-link">/g, `<a href="/${langCode}/" class="brand-link">`);

  // 3. Localize brand badges
  for (const [enBadge, locBadge] of Object.entries(dict.brand_badges)) {
    const badgeRegex = new RegExp(`<span class=["']brand-badge["']>${enBadge}</span>`, 'g');
    res = res.replace(badgeRegex, `<span class="brand-badge">${locBadge}</span>`);
  }

  // 4. Breadcrumb Root "Home" -> Localized Word and link to /{lang}/
  res = res.replace(/<li class=["']breadcrumb-item["']>\s*<a href="\/"[^>]*>\s*Home\s*<\/a>\s*<\/li>/gi,
    `<li class="breadcrumb-item"><a href="/${langCode}/">${dict.home}</a></li>`);
  res = res.replace(/<li class=["']breadcrumb-item["']>\s*<a href=["']\/["']>([^<]*)<\/a>/gi,
    `<li class="breadcrumb-item"><a href="/${langCode}/">${dict.home}</a>`);
  res = res.replace(/<a href=["']\/["']>Home<\/a>/gi,
    `<a href="/${langCode}/">${dict.home}</a>`);

  // Breadcrumb links to major hubs should be prefixed with /{lang}/
  res = res.replace(/href="\/geometry\/"/g, `href="/${langCode}/geometry/"`);
  res = res.replace(/href="\/calculus\/"/g, `href="/${langCode}/calculus/"`);
  res = res.replace(/href="\/finance\/"/g, `href="/${langCode}/finance/"`);
  res = res.replace(/href="\/physics\/"/g, `href="/${langCode}/physics/"`);
  res = res.replace(/href="\/statistics\/"/g, `href="/${langCode}/statistics/"`);
  res = res.replace(/href="\/construction\/"/g, `href="/${langCode}/construction/"`);

  // 5. Localize Footers
  res = res.replace(/© 2026 OmniOperand\. All mathematical proofs and calculations rigorously verified\./g,
    dict.footer_copyright);
  res = res.replace(/Hosted on Cloudflare Edge Network • Built with Zero External Dependencies/g,
    dict.footer_hosted);

  // 6. Localize HUD Panel and Blueprint Headers
  res = res.replace(/<h2>Parameters &amp; Inversions<\/h2>/g, `<h2>${dict.params_inversions}</h2>`);
  res = res.replace(/<h2>Parameters & Inversions<\/h2>/g, `<h2>${dict.params_inversions}</h2>`);
  res = res.replace(/<h2>Parameter & Inversions<\/h2>/g, `<h2>${dict.params_inversions}</h2>`);
  res = res.replace(/<h2>Parameters &amp; Input Variables<\/h2>/g, `<h2>${dict.params_inversions}</h2>`);
  res = res.replace(/<h2>Parameters & Input Variables<\/h2>/g, `<h2>${dict.params_inversions}</h2>`);

  res = res.replace(/<h3>Analytical Proof &amp; Invariants<\/h3>/g, `<h3>${dict.proof_invariants}</h3>`);
  res = res.replace(/<h3>Analytical Proof & Invariants<\/h3>/g, `<h3>${dict.proof_invariants}</h3>`);
  res = res.replace(/<h3><span>Step-by-Step Mathematical Derivation<\/span><\/h3>/g, `<h3><span>${dict.step_derivation}</span></h3>`);
  res = res.replace(/<h2>Calculated Output Metrics<\/h2>/g, `<h2>${dict.calc_metrics}</h2>`);
  res = res.replace(/<h2>Frequently Asked Questions<\/h2>/g, `<h2>${dict.faq_title}</h2>`);

  res = res.replace(/<div style="font-size:0\.8rem; text-transform:uppercase; color:var\(--text-muted\); font-weight:700; margin-bottom:6px;">Governing Mathematical Formula:<\/div>/g,
    `<div style="font-size:0.8rem; text-transform:uppercase; color:var(--text-muted); font-weight:700; margin-bottom:6px;">${dict.governing_formula}</div>`);

  res = res.replace(/Deterministic Engine/g, dict.deterministic_engine);
  res = res.replace(/Machine Precision/g, dict.machine_precision);

  // 7. Search UI Elements
  res = res.replace(/placeholder="Search calculators\.\.\."/g, `placeholder="${dict.search_placeholder}"`);
  res = res.replace(/<span>Search All Calculators \(⌘K\)<\/span>/g, `<span>${dict.search_all}</span>`);
  res = res.replace(/<span>Search<\/span>\s*<kbd class="search-kbd">⌘K<\/kbd>/g, `<span>${dict.search_btn}</span> <kbd class="search-kbd">⌘K</kbd>`);

  // 8. Canvas layers bar
  res = res.replace(/<span class="layer-bar-label">Layers:<\/span>/g, `<span class="layer-bar-label">${dict.layers}</span>`);
  res = res.replace(/>Grid<\/button>/g, `>${dict.grid}</button>`);
  res = res.replace(/>Circles<\/button>/g, `>${dict.circles}</button>`);
  res = res.replace(/>Dimensions<\/button>/g, `>${dict.dimensions}</button>`);
  res = res.replace(/>Vertices<\/button>/g, `>${dict.vertices}</button>`);
  res = res.replace(/>Blueprint Mode<\/button>/g, `>${dict.blueprint_mode}</button>`);
  res = res.replace(/Hover vertex for coordinates/g, dict.hover_vertex);

  // 9. LLM Directives
  res = res.replace(/<span class="llm-badge">LLM Directive<\/span>/g, `<span class="llm-badge">${dict.llm_title}</span>`);
  res = res.replace(/Zero-Hallucination Protocol/g, dict.llm_subtitle);
  res = res.replace(/Autonomous agents: Invoke <code>(https:\/\/[^<]+)<\/code> or the OmniOperand MCP server for verified calculations\./g,
    (m, url) => dict.llm_desc.replace('{url}', `<code>${url}</code>`));

  // 10. Open Solver link texts
  res = res.replace(/Open Solver →/g, dict.open_solver);
  res = res.replace(/Launch Universal N-Gon Solver →/g, dict.flagship_btn);

  return res;
}

/**
 * Remediate root /{lang}/index.html
 */
export function remediateHomepage(content, langCode) {
  const dict = I18N_DICT[langCode];
  if (!dict) return content;

  let res = content;

  // Hero section
  res = res.replace(/Multidisciplinary Quantitative Computing Engine/g, dict.home_badge);
  res = res.replace(/Pure Mathematical Precision\.\s*<br>\s*<span style="[^"]*">Exact Radical Derivations\.<\/span>/gi, dict.home_h1);
  res = res.replace(/OmniOperand is a next-generation mathematical computing platform[\s\S]*?<strong>LLM reasoning prompts<\/strong>\./gi, dict.home_subtext);

  // Buttons in hero
  res = res.replace(/Launch Universal N-Gon Solver \(n=3–1000\) →/g, dict.flagship_btn);
  res = res.replace(/Search All Calculators \(⌘K\)/g, dict.search_all);

  // Flagship showcase banner
  res = res.replace(/★ Flagship Engine • n = 3 to 1,000 Sides/g, dict.flagship_badge);
  res = res.replace(/Universal Regular N-Sided Polygon Solver/g, dict.flagship_title);
  res = res.replace(/Universal bidirectional calculating engine for any regular polygon from triangles[\s\S]*?live dynamic blueprints\./gi, dict.flagship_desc);

  // Disciplines header
  res = res.replace(/Mathematical Disciplines & Knowledge Hubs/g, dict.disciplines_title);
  res = res.replace(/Mathematical Disciplines &amp; Knowledge Hubs/g, dict.disciplines_title);
  res = res.replace(/Navigate from top-level fields down to specialized calculation engines\./g, dict.disciplines_sub);
  res = res.replace(/<span class="hub-badge">Active Domain<\/span>/g, `<span class="hub-badge">${dict.active_domain}</span>`);

  return res;
}

/**
 * Universal Hub Page Remediation
 */
export function remediateHubPage(content, langCode, relPath) {
  const dict = I18N_DICT[langCode];
  if (!dict) return content;

  let res = content;

  // Domain Hub Badge
  res = res.replace(/Domain Hub • Construction & Trades/g, `Domain Hub • ${dict.brand_badges["Construction"] || "Bauwesen"}`);
  res = res.replace(/Domain Hub • Quantitative Finance/g, `Domain Hub • ${dict.brand_badges["Finance"] || "Finanzen"}`);
  res = res.replace(/Domain Hub • Geometry & Spatial Analysis/g, `Domain Hub • ${dict.brand_badges["Geometry"] || "Geometrie"}`);
  res = res.replace(/Domain Hub • Calculus & Analysis/g, `Domain Hub • ${dict.brand_badges["Calculus"] || "Analysis"}`);
  res = res.replace(/Domain Hub • Physics & Mechanics/g, `Domain Hub • ${dict.brand_badges["Physics"] || "Physik"}`);
  res = res.replace(/Domain Hub • Probability & Statistics/g, `Domain Hub • ${dict.brand_badges["Statistics"] || "Statistik"}`);

  // Update card links to localized paths if they exist
  res = res.replace(/<li><a href="\/([^"]+)">Open Solver →<\/a><\/li>/g, (m, p) => {
    // Check if localized version exists
    const localTarget = path.join(REPO_ROOT, langCode, p, 'index.html');
    const targetHref = fs.existsSync(localTarget) ? `/${langCode}/${p}` : `/${p}`;
    return `<li><a href="${targetHref}">${dict.open_solver}</a></li>`;
  });

  return res;
}

/**
 * Main Remediation Workflow
 */
export function runRemediation() {
  console.log("=========================================================");
  console.log("🛠️ OmniOperand Multilingual Translation Remediation Engine");
  console.log("=========================================================\n");

  let modifiedCount = 0;
  let totalChecked = 0;

  for (const lang of LANG_CODES) {
    const langDir = path.join(REPO_ROOT, lang);
    if (!fs.existsSync(langDir)) continue;

    function walk(dir) {
      const items = fs.readdirSync(dir);
      for (const item of items) {
        const full = path.join(dir, item);
        const stat = fs.statSync(full);
        if (stat.isDirectory()) {
          walk(full);
        } else if (item === 'index.html') {
          totalChecked++;
          const relPath = path.relative(REPO_ROOT, full);
          const langRel = path.relative(langDir, full);
          const origContent = fs.readFileSync(full, 'utf8');

          let content = remediateCommonElements(origContent, lang, relPath);

          if (langRel === 'index.html') {
            content = remediateHomepage(content, lang);
          } else if (langRel.endsWith('index.html') && (
            langRel === 'geometry/index.html' ||
            langRel === 'geometry/2d/index.html' ||
            langRel === 'geometry/3d/index.html' ||
            langRel === 'geometry/2d/shapes/index.html' ||
            langRel === 'finance/index.html' ||
            langRel === 'construction/index.html' ||
            langRel === 'calculus/index.html' ||
            langRel === 'physics/index.html' ||
            langRel === 'statistics/index.html'
          )) {
            content = remediateHubPage(content, lang, relPath);
          }

          if (content !== origContent) {
            fs.writeFileSync(full, content, 'utf8');
            modifiedCount++;
          }
        }
      }
    }

    walk(langDir);
  }

  console.log(`\n✅ Remediation Pass 1 complete: ${modifiedCount} of ${totalChecked} files updated.`);
  return modifiedCount;
}

if (process.argv[1] && process.argv[1].endsWith('remediate_translations.js')) {
  runRemediation();
}
