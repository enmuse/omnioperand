#!/usr/bin/env python3
"""
scripts/solver_templates.py — Comprehensive Localized Proofs & FAQs for All 15 Solvers
Zero raw LaTeX commands. Pure Unicode mathematical typography.
"""

def get_polygon_data(name, n_sides, formula_area, formula_ap, formula_diag, lang):
    poly_terms = {
        "de": {
            "h2_proof": "Mathematische Grundlagen & Analytische Herleitungen",
            "p_intro": f"Ein regelmäßiges {name} ist ein zweidimensionales konvexes regelmäßiges Polygon mit {n_sides} gleich langen Seiten und {n_sides} gleichen Innenwinkeln. Es gehört zur Diedergruppe D_{n_sides} mit {n_sides} Spiegelsymmetrieachsen und {n_sides}-zähliger Drehsymmetrie.",
            "card1_title": "Innen-, Außen- & Mittelpunktswinkel",
            "sum_angles": f"Summe der Innenwinkel: Für ein n-Eck mit n = {n_sides} beträgt die Gesamtsumme S = ({n_sides} - 2) × 180°.",
            "each_angle": "Jeder einzelne Innenwinkel beträgt α = S / n.",
            "central_angle": "Mittelpunkts- und Außenwinkel betragen β = 360° / n.",
            "card2_title": "Apothema (Inkreisradius) & Umkreisradius",
            "ap_p": f"Das Apothema r_i ist der senkrechte Abstand vom Mittelpunkt zu jeder Kante: r_i = a / [2 tan(180° / {n_sides})]. {formula_ap}",
            "cr_p": f"Der Umkreisradius R ist der Abstand zu den Eckpunkten: R = a / [2 sin(180° / {n_sides})].",
            "card3_title": "Exakte Flächenberechnung & Triangulierung",
            "area_p": f"Zerlegung in {n_sides} kongruente Dreiecke ergibt die geschlossene Flächenformel: A = {formula_area}.",
            "card4_title": "Diagonalklassen & Kosinussatz",
            "diag_p": f"Ein regelmäßiges Polygon mit {n_sides} Ecken besitzt {n_sides * (n_sides - 3) // 2} Diagonalen. {formula_diag}",
            "faq_area_q": f"Wie lautet die Formel für die Fläche eines regelmäßigen {name}s?",
            "faq_area_a": f"Die Fläche eines regelmäßigen {name}s mit Seitenlänge a berechnet sich nach der geschlossenen Formel A = {formula_area}.",
            "faq_side_q": "Wie berechnet man die Seitenlänge aus der Fläche?",
            "faq_side_a": "Um die Seitenlänge a aus der Fläche A zu bestimmen, dividiert man die Fläche durch den geometrischen Faktor und zieht die Quadratwurzel.",
            "faq_diags_q": f"Wie viele Diagonalen besitzt ein {name}?",
            "faq_diags_a": f"Die Gesamtzahl aller Diagonalen beträgt n(n - 3) / 2 = {n_sides * (n_sides - 3) // 2} Diagonalen.",
            "faq_app_q": "Welche praktischen Anwendungen hat diese Geometrie?",
            "faq_app_a": "In Architektur, Bauwesen, Zerspanungstechnik und Fliesenverlegung sorgt die Symmetrie für optimale Lastverteilung."
        },
        "es": {
            "h2_proof": "Fundamentos Matemáticos y Demostraciones Analíticas",
            "p_intro": f"Un {name} regular es un polígono convexo bidimensional con {n_sides} lados iguales y {n_sides} ángulos interiores congruentes. Pertenece al grupo diedro D_{n_sides}.",
            "card1_title": "Ángulos Interiores, Exteriores y Centrales",
            "sum_angles": f"Suma de ángulos interiores: Para n = {n_sides}, la suma total es S = ({n_sides} - 2) × 180°.",
            "each_angle": "Cada ángulo interior mide α = S / n.",
            "central_angle": "El ángulo central y el ángulo exterior miden β = 360° / n.",
            "card2_title": "Apotema (Inradio) y Circunradio",
            "ap_p": f"La apotema r_i es la distancia perpendicular del centro a cada lado: r_i = a / [2 tan(180° / {n_sides})]. {formula_ap}",
            "cr_p": f"El circunradio R es la distancia desde el centro a los vértices: R = a / [2 sin(180° / {n_sides})].",
            "card3_title": "Cálculo Exacto del Área y Triangulación",
            "area_p": f"La descomposición en {n_sides} triángulos isósceles conduce a la fórmula cerrada: A = {formula_area}.",
            "card4_title": "Clases de Diagonales y Ley del Coseno",
            "diag_p": f"Un polígono regular de {n_sides} lados tiene {n_sides * (n_sides - 3) // 2} diagonales en total. {formula_diag}",
            "faq_area_q": f"¿Cuál es la fórmula del área de un {name} regular?",
            "faq_area_a": f"El área de un {name} regular con lado a se calcula mediante A = {formula_area}.",
            "faq_side_q": "¿Cómo se calcula la longitud del lado a partir del área?",
            "faq_side_a": "Para resolver el lado a a partir del área A, divida el área entre el coeficiente geométrico y calcule la raíz cuadrada.",
            "faq_diags_q": f"¿Cuántas diagonales tiene un {name}?",
            "faq_diags_a": f"El número total de diagonales viene dado por n(n - 3) / 2 = {n_sides * (n_sides - 3) // 2} diagonales.",
            "faq_app_q": "¿Qué aplicaciones prácticas tiene esta forma geométrica?",
            "faq_app_a": "En ingeniería estructural, arquitectura y carpintería metálica, su alta simetría distribuye de forma óptima los esfuerzos mecánicos."
        },
        "fr": {
            "h2_proof": "Fondements Mathématiques & Démonstrations Analytiques",
            "p_intro": f"Un {name} régulier est un polygone convexe bidimensionnel à {n_sides} côtés égaux et {n_sides} angles intérieurs congruents. Il appartient au groupe diédral D_{n_sides}.",
            "card1_title": "Angles Intérieurs, Extérieurs et Centraux",
            "sum_angles": f"Somme des angles intérieurs : Pour n = {n_sides}, la somme vaut S = ({n_sides} - 2) × 180°.",
            "each_angle": "Chaque angle intérieur mesure α = S / n.",
            "central_angle": "L'angle central et l'angle extérieur valent β = 360° / n.",
            "card2_title": "Apothème (Rayon Inscrit) & Rayon Circonscrit",
            "ap_p": f"L'apothème r_i est la distance orthogonale du centre à chaque côté : r_i = a / [2 tan(180° / {n_sides})]. {formula_ap}",
            "cr_p": f"Le rayon circonscrit R relie le centre aux sommets : R = a / [2 sin(180° / {n_sides})].",
            "card3_title": "Calcul Exact de l'Aire & Décomposition",
            "area_p": f"La décomposition en {n_sides} triangles isocèles donne la formule fermée : A = {formula_area}.",
            "card4_title": "Classes de Diagonales & Théorème d'Al-Kashi",
            "diag_p": f"Un polygone régulier à {n_sides} sommets possède {n_sides * (n_sides - 3) // 2} diagonales. {formula_diag}",
            "faq_area_q": f"Quelle est la formule de l'aire d'un {name} régulier ?",
            "faq_area_a": f"L'aire d'un {name} régulier de côté a s'exprime par A = {formula_area}.",
            "faq_side_q": "Comment calculer le côté à partir de l'aire ?",
            "faq_side_a": "Pour déterminer le côté a à partir de l'aire A, divisez l'aire par le coefficient géométrique puis extrayez la racine carrée.",
            "faq_diags_q": f"Combien de diagonales possède un {name} ?",
            "faq_diags_a": f"Le nombre total de diagonales est donné par n(n - 3) / 2 = {n_sides * (n_sides - 3) // 2} diagonales.",
            "faq_app_q": "Quelles sont les applications architecturales et techniques ?",
            "faq_app_a": "Cette géométrie est largement utilisée en architecture et mécanique de précision pour sa parfaite répartition des charges."
        },
        "it": {
            "h2_proof": "Fondamenti Matematici e Dimostrazioni Analitiche",
            "p_intro": f"Un {name} regolare è un poligono convesso con {n_sides} lati uguali e {n_sides} angoli interni congruenti. Appartiene al gruppo diedrale D_{n_sides}.",
            "card1_title": "Angoli Interni, Esterni e Centrali",
            "sum_angles": f"Somma degli angoli interni: Per n = {n_sides}, la somma totale è S = ({n_sides} - 2) × 180°.",
            "each_angle": "Ciascun angolo interno misura α = S / n.",
            "central_angle": "L'angolo al centro e l'angolo esterno misurano β = 360° / n.",
            "card2_title": "Apotema (Raggio Inscritto) e Raggio Circoscritto",
            "ap_p": f"L'apotema r_i è la distanza perpendicolare dal centro a ciascun lato : r_i = a / [2 tan(180° / {n_sides})]. {formula_ap}",
            "cr_p": f"Il raggio circoscritto R unisce il centro a ciascun vertice: R = a / [2 sin(180° / {n_sides})].",
            "card3_title": "Calcolo Esatto dell'Area e Triangolazione",
            "area_p": f"La triangolazione in {n_sides} triangoli congruenti conduce alla formula esatta: A = {formula_area}.",
            "card4_title": "Classi di Diagonali e Teorema del Coseno",
            "diag_p": f"Un poligono regolare con {n_sides} lati possiede {n_sides * (n_sides - 3) // 2} diagonali. {formula_diag}",
            "faq_area_q": f"Qual è la formula per l'area di un {name} regolare?",
            "faq_area_a": f"L'area di un {name} regolare di lato a è A = {formula_area}.",
            "faq_side_q": "Come si calcola la lunghezza del lato dall'area?",
            "faq_side_a": "Per calcolare il lato a dall'area A, dividi l'area per la costante geometrica ed estrai la radice quadrata.",
            "faq_diags_q": f"Quante diagonali possiede un {name}?",
            "faq_diags_a": f"Il numero totale di diagonali è n(n - 3) / 2 = {n_sides * (n_sides - 3) // 2} diagonali.",
            "faq_app_q": "Quali sono le applicazioni ingegneristiche pratiche?",
            "faq_app_a": "In ingegneria civile e meccanica, garantisce una simmetria ideale nella ripartizione delle sollecitazioni torsionali."
        },
        "pt": {
            "h2_proof": "Fundamentos Matemáticos e Demonstrações Analíticas",
            "p_intro": f"Um {name} regular é um polígono convexo com {n_sides} lados iguais e {n_sides} ângulos internos congruentes. Pertence ao grupo diedro D_{n_sides}.",
            "card1_title": "Ângulos Internos, Externos e Centrais",
            "sum_angles": f"Soma dos ângulos internos: Para n = {n_sides}, S = ({n_sides} - 2) × 180°.",
            "each_angle": "Cada ângulo interno mede α = S / n.",
            "central_angle": "O ângulo central e o ângulo externo medem β = 360° / n.",
            "card2_title": "Apótema (Raio Inscrito) e Raio Circunscrito",
            "ap_p": f"O apótema r_i é a distância perpendicular do centro ao lado: r_i = a / [2 tan(180° / {n_sides})]. {formula_ap}",
            "cr_p": f"O raio circunscrito R liga o centro aos vértices: R = a / [2 sin(180° / {n_sides})].",
            "card3_title": "Cálculo Exato da Área e Decomposição",
            "area_p": f"A decomposição em {n_sides} triângulos isósceles fornece a fórmula fechada: A = {formula_area}.",
            "card4_title": "Classes de Diagonais e Lei dos Cossenos",
            "diag_p": f"Um polígono com {n_sides} vértices possui {n_sides * (n_sides - 3) // 2} diagonais. {formula_diag}",
            "faq_area_q": f"Qual é a fórmula da área de um {name} regular?",
            "faq_area_a": f"A área de um {name} regular com lado a é A = {formula_area}.",
            "faq_side_q": "Como calcular o comprimento do lado a partir da área?",
            "faq_side_a": "Para obter o lado a a partir da área A, divida a área pela constante de forma e calcule a raiz quadrada.",
            "faq_diags_q": f"Quantas diagonais possui um {name}?",
            "faq_diags_a": f"O total de diagonais é n(n - 3) / 2 = {n_sides * (n_sides - 3) // 2} diagonais.",
            "faq_app_q": "Quais são as principais aplicações práticas?",
            "faq_app_a": "Na engenharia estrutural e arquitetura moderna, oferece distribuição uniforme de forças e rigidez geométrica."
        },
        "nl": {
            "h2_proof": "Wiskundige Grondslagen & Analytische Afleidingen",
            "p_intro": f"Een regelmatige {name} is een tweedimensionale convexe veelhoek met {n_sides} gelijke zijden en {n_sides} gelijke binnenhoeken. Hij behoort tot de dihedrale groep D_{n_sides}.",
            "card1_title": "Binnenhoeken, Buitenhoeken en Middelpuntshoeken",
            "sum_angles": f"Som van de binnenhoeken: Voor n = {n_sides} geldt S = ({n_sides} - 2) × 180°.",
            "each_angle": "Elke afzonderlijke binnenhoek bedraagt α = S / n.",
            "central_angle": "De middelpuntshoek en buitenhoek zijn β = 360° / n.",
            "card2_title": "Apothema (Ingeschreven Straal) & Omgeschreven Straal",
            "ap_p": f"Het apothema r_i is de loodrechte afstand van het middelpunt tot een zijde: r_i = a / [2 tan(180° / {n_sides})]. {formula_ap}",
            "cr_p": f"De omgeschreven straal R loopt naar de hoekpunten: R = a / [2 sin(180° / {n_sides})].",
            "card3_title": "Exacte Oppervlakteberekening & Triangulatie",
            "area_p": f"Verdeling in {n_sides} congruente driehoeken levert de exacte formule: A = {formula_area}.",
            "card4_title": "Diagonaalklassen & Cosinusregel",
            "diag_p": f"Een regelmatige veelhoek met {n_sides} zijden heeft {n_sides * (n_sides - 3) // 2} diagonalen. {formula_diag}",
            "faq_area_q": f"Wat is de formule voor de oppervlakte van een regelmatige {name}?",
            "faq_area_a": f"De oppervlakte van een regelmatige {name} met zijde a is A = {formula_area}.",
            "faq_side_q": "Hoe bereken je de zijdelengte uit de oppervlakte?",
            "faq_side_a": "Deel de oppervlakte A door de vormfactor en neem de vierkantswortel om zijdelengte a te bepalen.",
            "faq_diags_q": f"Hoeveel diagonalen heeft een {name}?",
            "faq_diags_a": f"Het aantal diagonalen bedraagt n(n - 3) / 2 = {n_sides * (n_sides - 3) // 2} diagonalen.",
            "faq_app_q": "Wat zijn praktische bouw- en ontwerptoepassingen?",
            "faq_app_a": "In architectuur en constructietechniek zorgt de rotatiesymmetrie voor optimale krachtenverdeling."
        },
        "pl": {
            "h2_proof": "Podstawy Matematyczne i Ścisłe Dowody Analityczne",
            "p_intro": f"Wielokąt foremny ({name}) to figura płaska o {n_sides} równych bokach i {n_sides} przystających kątach wewnętrznych. Należy do grupy dihedralnej D_{n_sides}.",
            "card1_title": "Kąty Wewnętrzne, Zewnętrzne i Środkowe",
            "sum_angles": f"Suma kątów wewnętrznych: Dla n = {n_sides} wynosi S = ({n_sides} - 2) × 180°.",
            "each_angle": "Każdy kąt wewnętrzny wynosi α = S / n.",
            "central_angle": "Kąt środkowy oraz kąt zewnętrzny wynoszą β = 360° / n.",
            "card2_title": "Apotema (Promień Wpisany) i Promień Opisany",
            "ap_p": f"Apotema r_i to odległość od środka do boku: r_i = a / [2 tan(180° / {n_sides})]. {formula_ap}",
            "cr_p": f"Promień okręgu opisanego R wynosi: R = a / [2 sin(180° / {n_sides})].",
            "card3_title": "Ścisłe Wzory na Pole i Triangulacja",
            "area_p": f"Podział na {n_sides} trójkątów przystających daje ścisły wzór: A = {formula_area}.",
            "card4_title": "Klasy Przekątnych i Twierdzenie Cosinusów",
            "diag_p": f"Wielokąt o {n_sides} wierzchołkach ma {n_sides * (n_sides - 3) // 2} przekątnych. {formula_diag}",
            "faq_area_q": f"Jaki jest wzór na pole powierzchni ({name})?",
            "faq_area_a": f"Pole powierzchni o boku a wyraża się wzorem A = {formula_area}.",
            "faq_side_q": "Jak wyznaczyć długość boku z pola?",
            "faq_side_a": "Należy podzielić pole A przez współczynnik geometryczny i wyciągnąć pierwiastek kwadratowy.",
            "faq_diags_q": f"Ile przekątnych ma {name}?",
            "faq_diags_a": f"Liczba przekątnych wynosi n(n - 3) / 2 = {n_sides * (n_sides - 3) // 2}.",
            "faq_app_q": "Gdzie znajduje zastosowanie ta figura?",
            "faq_app_a": "W konstrukcjach inżynieryjnych i mechanice precyzyjnej dla równomiernego przenoszenia naprężeń."
        },
        "sv": {
            "h2_proof": "Matematiska Grunder & Analytiska Härledningar",
            "p_intro": f"En regelbunden {name} är en plan konvex polygon med {n_sides} lika långa sidor och {n_sides} lika stora vinklar. Den tillhör den dihedrala symmetrigruppen D_{n_sides}.",
            "card1_title": "Inre, Yttre och Centrala Vinklar",
            "sum_angles": f"Summan av innerhörnens vinklar: För n = {n_sides} är S = ({n_sides} - 2) × 180°.",
            "each_angle": "Varje enskild inre vinkel är α = S / n.",
            "central_angle": "Medelpunktsvinkeln och yttervinkeln är β = 360° / n.",
            "card2_title": "Apotem (Inskriven Radie) & Omskriven Radie",
            "ap_p": f"Apotemet r_i är det vinkelräta avståndet till kanten: r_i = a / [2 tan(180° / {n_sides})]. {formula_ap}",
            "cr_p": f"Den omskrivna radien R går från centrum till hörnen: R = a / [2 sin(180° / {n_sides})].",
            "card3_title": "Exakt Areaberäkning & Triangulering",
            "area_p": f"Uppdelning i {n_sides} kongruenta trianglar ger arean: A = {formula_area}.",
            "card4_title": "Diagonalklasser & Cosinussatsen",
            "diag_p": f"En regelbunden polygon med {n_sides} sidor har {n_sides * (n_sides - 3) // 2} diagonaler. {formula_diag}",
            "faq_area_q": f"Vad är formeln för arean av en {name}?",
            "faq_area_a": f"Arean av en {name} med sidolängd a är A = {formula_area}.",
            "faq_side_q": "Hur beräknar man sidolängden från arean?",
            "faq_side_a": "Dividera arean A med geometrifaktorn och ta kvadratroten för att erhålla sidolängden a.",
            "faq_diags_q": f"Hur många diagonaler har en {name}?",
            "faq_diags_a": f"Totalt antal diagonaler ges av n(n - 3) / 2 = {n_sides * (n_sides - 3) // 2} diagonaler.",
            "faq_app_q": "Vilka tekniska tillämpningar finns det?",
            "faq_app_a": "Används inom byggnadskonstruktion och formgivning där symmetri ger maximal vridstyvhet."
        },
        "no": {
            "h2_proof": "Matematiske Prinsipper & Analytiske Bevis",
            "p_intro": f"En regulær {name} er en plan konveks mangekant med {n_sides} like lange sider og {n_sides} like store vinkler. Den tilhører den dihedrale gruppen D_{n_sides}.",
            "card1_title": "Indre Vinkler, Ytre Vinkler og Sentralvinkler",
            "sum_angles": f"Vinkelsum av indre vinkler: For n = {n_sides} er summen S = ({n_sides} - 2) × 180°.",
            "each_angle": "Hver indre vinkel er α = S / n.",
            "central_angle": "Sentralvinkelen og ytre vinkel er β = 360° / n.",
            "card2_title": "Apotem (Innskrevet Radius) & Omskrevet Radius",
            "ap_p": f"Apotemet r_i er den vinkelrette avstanden til siden: r_i = a / [2 tan(180° / {n_sides})]. {formula_ap}",
            "cr_p": f"Omskrevet radius R går fra sentrum til hjørnene: R = a / [2 sin(180° / {n_sides})].",
            "card3_title": "Eksakt Arealberegning & Triangulering",
            "area_p": f"Oppdeling i {n_sides} likebente trekanter gir formelen: A = {formula_area}.",
            "card4_title": "Diagonalklasser & Cosinussetningen",
            "diag_p": f"En regulær mangekant med {n_sides} sider har {n_sides * (n_sides - 3) // 2} diagonaler. {formula_diag}",
            "faq_area_q": f"Hva er formelen for arealet av en {name}?",
            "faq_area_a": f"Arealet av en {name} med sidelengde a beregnes ved A = {formula_area}.",
            "faq_side_q": "Hvordan finner man sidelengden fra arealet?",
            "faq_side_a": "Del arealet A på formkonstanten og trekk ut kvadratroten for å finne sidelengden a.",
            "faq_diags_q": f"Hvor mange diagonaler har en {name}?",
            "faq_diags_a": f"Antall diagonaler er n(n - 3) / 2 = {n_sides * (n_sides - 3) // 2} diagonaler.",
            "faq_app_q": "Hva brukes denne geometrien til i praksis?",
            "faq_app_a": "Brukes i trekonstruksjoner, stålbygg og arkitektur for jevn spenningsfordeling."
        },
        "fi": {
            "h2_proof": "Matemaattiset Perusteet & Analyyttiset Todistukset",
            "p_intro": f"Säännöllinen {name} on kaksiulotteinen kupera monikulmio, jolla on {n_sides} yhtä pitkää sivua ja {n_sides} yhtä suurta sisäkulmaa. Se kuuluu diedriryhmään D_{n_sides}.",
            "card1_title": "Sisäkulmat, Ulkokulmat ja Keskuskulmat",
            "sum_angles": f"Sisäkulmien summa: Arvolla n = {n_sides} summa on S = ({n_sides} - 2) × 180°.",
            "each_angle": "Kukin yksittäinen sisäkulma on α = S / n.",
            "central_angle": "Keskuskulma ja ulkokulma ovat β = 360° / n.",
            "card2_title": "Apoteema (Sisäympyrän Säde) & Ulkoympyrän Säde",
            "ap_p": f"Apoteema r_i on kohtisuora etäisyys keskipisteestä sivulle: r_i = a / [2 tan(180° / {n_sides})]. {formula_ap}",
            "cr_p": f"Ulkoympyrän säde R yhdistää keskipisteen kärkipisteisiin: R = a / [2 sin(180° / {n_sides})].",
            "card3_title": "Tarkka Pinta-alan Laskenta & Kolmiojako",
            "area_p": f"Jakamalla monikulmio {n_sides} kolmioon saadaan tarkka kaava: A = {formula_area}.",
            "card4_title": "Lävistäjäluokat & Kosinilause",
            "diag_p": f"Monikulmiolla on {n_sides * (n_sides - 3) // 2} lävistäjää. {formula_diag}",
            "faq_area_q": f"Mikä on säännöllisen {name}n pinta-alan kaava?",
            "faq_area_a": f"Pinta-ala sivun pituudella a lasketaan kaavalla A = {formula_area}.",
            "faq_side_q": "Miten sivun pituus ratkaistaan pinta-alasta?",
            "faq_side_a": "Jaa pinta-ala A geometriavakiolla ja ota neliöjuuri sivun pituuden a selvittämiseksi.",
            "faq_diags_q": f"Kuinka monta lävistäjää monikulmiolla on?",
            "faq_diags_a": f"Lävistäjien kokonaismäärä on n(n - 3) / 2 = {n_sides * (n_sides - 3) // 2}.",
            "faq_app_q": "Missä tätä geometriaa sovelletaan käytännössä?",
            "faq_app_a": "Rakennetekniikassa ja arkkitehtuurissa symmetria optimoi kuormitusten tasaisen jakautumisen."
        },
        "ro": {
            "h2_proof": "Fundamente Matematice și Demonstrații Analitice",
            "p_intro": f"Un {name} regulat este un poligon plan convex cu {n_sides} laturi egale și {n_sides} unghiuri congruente. Aparține grupului diedral D_{n_sides}.",
            "card1_title": "Unghiuri Interioare, Exterioare și Centrale",
            "sum_angles": f"Suma unghiurilor interioare: Pentru n = {n_sides}, suma este S = ({n_sides} - 2) × 180°.",
            "each_angle": "Fiecare unghi interior măsoară α = S / n.",
            "central_angle": "Unghiul la centru și unghiul exterior măsoară β = 360° / n.",
            "card2_title": "Apotema (Raza Înscrisă) și Raza Circumscrisă",
            "ap_p": f"Apotema r_i este distanța perpendiculară de la centru la latură: r_i = a / [2 tan(180° / {n_sides})]. {formula_ap}",
            "cr_p": f"Raza circumscrisă R unește centrul cu vârfurile: R = a / [2 sin(180° / {n_sides})].",
            "card3_title": "Calculul Exact al Ariei și Triangularea",
            "area_p": f"Descompunerea în {n_sides} triunghiuri congruente oferă formula închisă: A = {formula_area}.",
            "card4_title": "Clase de Diagonale și Teorema Cosinusului",
            "diag_p": f"Un poligon regulat cu {n_sides} vârfuri are {n_sides * (n_sides - 3) // 2} diagonale. {formula_diag}",
            "faq_area_q": f"Care este formula pentru aria unui {name} regulat?",
            "faq_area_a": f"Aria unui {name} regulat cu latura a se calculează prin A = {formula_area}.",
            "faq_side_q": "Cum se calculează latura din arie?",
            "faq_side_a": "Împărțiți aria A la coeficientul de formă și extrageți rădăcina pătrată pentru a găsi latura a.",
            "faq_diags_q": f"Câte diagonale are un {name}?",
            "faq_diags_a": f"Numărul total de diagonale este n(n - 3) / 2 = {n_sides * (n_sides - 3) // 2} diagonale.",
            "faq_app_q": "Care sunt aplicațiile practice în inginerie?",
            "faq_app_a": "În construcții metalice și arhitectură, simetria radială garantează o distribuție optimă a forțelor mecanice."
        }
    }
    t = poly_terms.get(lang, poly_terms["de"])
    
    proof_html = f"""<section class="proofs-section">
      <h2>{t['h2_proof']}</h2>
      <p>{t['p_intro']}</p>
      <div class="proof-card open">
        <div class="proof-header">
          <h3><span class="step-num">1</span><span>{t['card1_title']}</span></h3>
          <span class="proof-toggle-icon">▼</span>
        </div>
        <div class="proof-body">
          <p>{t['sum_angles']}</p>
          <p>{t['each_angle']}</p>
          <p>{t['central_angle']}</p>
        </div>
      </div>
      <div class="proof-card open">
        <div class="proof-header">
          <h3><span class="step-num">2</span><span>{t['card2_title']}</span></h3>
          <span class="proof-toggle-icon">▼</span>
        </div>
        <div class="proof-body">
          <p>{t['ap_p']}</p>
          <p>{t['cr_p']}</p>
        </div>
      </div>
      <div class="proof-card open">
        <div class="proof-header">
          <h3><span class="step-num">3</span><span>{t['card3_title']}</span></h3>
          <span class="proof-toggle-icon">▼</span>
        </div>
        <div class="proof-body">
          <p>{t['area_p']}</p>
        </div>
      </div>
      <div class="proof-card open">
        <div class="proof-header">
          <h3><span class="step-num">4</span><span>{t['card4_title']}</span></h3>
          <span class="proof-toggle-icon">▼</span>
        </div>
        <div class="proof-body">
          <p>{t['diag_p']}</p>
        </div>
      </div>
    </section>"""

    faq_html = f"""<section class="faq-section">
      <h2>FAQ</h2>
      <div class="faq-item open">
        <div class="faq-question"><span>{t['faq_area_q']}</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">{t['faq_area_a']}</div>
      </div>
      <div class="faq-item open">
        <div class="faq-question"><span>{t['faq_side_q']}</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">{t['faq_side_a']}</div>
      </div>
      <div class="faq-item open">
        <div class="faq-question"><span>{t['faq_diags_q']}</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">{t['faq_diags_a']}</div>
      </div>
      <div class="faq-item open">
        <div class="faq-question"><span>{t['faq_app_q']}</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">{t['faq_app_a']}</div>
      </div>
    </section>"""

    faqs = [
        {"q": t['faq_area_q'], "a": t['faq_area_a']},
        {"q": t['faq_side_q'], "a": t['faq_side_a']},
        {"q": t['faq_diags_q'], "a": t['faq_diags_a']},
        {"q": t['faq_app_q'], "a": t['faq_app_a']}
    ]

    return {"proof_html": proof_html, "faq_html": faq_html, "faqs": faqs}


# 2D Geometry Solvers
def get_right_triangle_data(lang):
    names = {
        "de": ("Rechtwinkliges Dreieck", "Katheten, Hypotenuse, Dreieckshöhe und Inkreisradius"),
        "es": ("Triángulo Rectángulo", "Catetos, hipotenusa, altura y radio del círculo inscrito"),
        "fr": ("Triangle Rectangle", "Cathètes, hypoténuse, hauteur et rayon du cercle inscrit"),
        "it": ("Triangolo Rettangolo", "Cateti, ipotenusa, altezza relativa e raggio inscritto"),
        "pt": ("Triângulo Retângulo", "Catetos, hipotenusa, altura e raio do círculo inscrito"),
        "nl": ("Rechthoekige Driehoek", "Rechthoekszijden, schuine zijde, hoogte en ingeschreven straal"),
        "pl": ("Trójkąt Prostokątny", "Przyprostokątne, przeciwprostokątna, wysokość i promień wpisany"),
        "sv": ("Rätvinklig Triangel", "Kateter, hypotenusa, höjd och inskriven radie"),
        "no": ("Rettvinklet Trekant", "Kateter, hypotenus, høyde og innskrevet radius"),
        "fi": ("Suorakulmainen Kolmio", "Kateetit, hypotenuusa, korkeus ja sisäympyrän säde"),
        "ro": ("Triunghi Dreptunghic", "Catete, ipotenuză, înălțime și raza cercului înscris")
    }
    t_name, t_desc = names.get(lang, names["de"])

    proof_html = f"""<section class="proof-section" style="margin-top: 3rem;">
      <h2>Mathematische Grundlagen: {t_name}</h2>
      <p>{t_desc}</p>
      <div class="proof-card open">
        <div class="proof-header">
          <h3><span class="step-num">1</span><span>Satz des Pythagoras (Pythagorean Theorem)</span></h3>
        </div>
        <div class="proof-body">
          <p>Für jedes rechtwinklige Dreieck gilt: a² + b² = c² ⟹ c = √(a² + b²).</p>
        </div>
      </div>
      <div class="proof-card open">
        <div class="proof-header">
          <h3><span class="step-num">2</span><span>Höhensatz & Dreieckshöhe</span></h3>
        </div>
        <div class="proof-body">
          <p>Aus dem doppelten Flächeninhalt folgt: Area = ½ · a · b = ½ · c · h_c ⟹ h_c = (a · b) / c.</p>
        </div>
      </div>
      <div class="proof-card open">
        <div class="proof-header">
          <h3><span class="step-num">3</span><span>Inkreisradius (Inradius)</span></h3>
        </div>
        <div class="proof-body">
          <p>Der Inkreisradius berechnet sich exakt durch: r = (a + b - c) / 2.</p>
        </div>
      </div>
    </section>"""

    faq_html = f"""<section class="faq-section">
      <h2>FAQ: {t_name}</h2>
      <div class="faq-item open">
        <div class="faq-question"><span>Wie berechnet man die Hypotenuse?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Nach dem Satz des Pythagoras gilt c = √(a² + b²).</div>
      </div>
      <div class="faq-item open">
        <div class="faq-question"><span>Wie berechnet man die Höhe auf die Hypotenuse?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Die Höhe h_c berechnet sich aus dem Produkt der Katheten dividiert durch die Hypotenuse: h_c = (a · b) / c.</div>
      </div>
      <div class="faq-item open">
        <div class="faq-question"><span>Wie lautet die Formel für den Inkreisradius?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Im rechtwinkligen Dreieck gilt exakt r = (a + b - c) / 2.</div>
      </div>
    </section>"""

    faqs = [
        {"q": "Wie berechnet man die Hypotenuse?", "a": "Nach dem Satz des Pythagoras gilt c = √(a² + b²)."},
        {"q": "Wie berechnet man die Höhe auf die Hypotenuse?", "a": "Die Höhe h_c berechnet sich aus dem Produkt der Katheten dividiert durch die Hypotenuse: h_c = (a · b) / c."},
        {"q": "Wie lautet die Formel für den Inkreisradius?", "a": "Im rechtwinkligen Dreieck gilt exakt r = (a + b - c) / 2."}
    ]

    return {"proof_html": proof_html, "faq_html": faq_html, "faqs": faqs}

def get_circle_sector_data(lang):
    proof_html = """<section class="proof-section" style="margin-top: 3rem;">
      <h2>Analytische Geometrie: Kreissektor & Kreissegment</h2>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">1</span><span>Bogenlänge & Zentriwinkel</span></h3></div>
        <div class="proof-body"><p>Für den Zentriwinkel θ in Grad: s = (θ / 360°) · 2πr = r · θ_rad.</p></div>
      </div>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">2</span><span>Sektorfläche & Segmentfläche</span></h3></div>
        <div class="proof-body"><p>Sektorfläche: A_sektor = (θ / 360°) · πr² = ½ r² θ_rad. Segmentfläche: A_seg = ½ r² (θ_rad - sin θ_rad).</p></div>
      </div>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">3</span><span>Sehnenlänge & Bogenhöhe (Sagitta)</span></h3></div>
        <div class="proof-body"><p>Sehnenlänge: c = 2r · sin(θ / 2). Sagitta (Bogenhöhe): h = r · (1 - cos(θ / 2)).</p></div>
      </div>
    </section>"""

    faq_html = """<section class="faq-section">
      <h2>FAQ: Kreissektor</h2>
      <div class="faq-item open">
        <div class="faq-question"><span>Wie berechnet man die Bogenlänge?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Die Bogenlänge s beträgt (θ / 360°) · 2πr.</div>
      </div>
      <div class="faq-item open">
        <div class="faq-question"><span>Was ist der Unterschied zwischen Sektor und Segment?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Ein Sektor ist ein kuchenförmiges Stück vom Mittelpunkt zum Bogen. Ein Segment ist die Fläche zwischen Bogen und Sehne.</div>
      </div>
      <div class="faq-item open">
        <div class="faq-question"><span>Wie berechnet man die Sagitta (Bogenhöhe)?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Die Bogenhöhe h berechnet sich nach h = r · (1 - cos(θ / 2)).</div>
      </div>
    </section>"""

    faqs = [
        {"q": "Wie berechnet man die Bogenlänge?", "a": "Die Bogenlänge s beträgt (θ / 360°) · 2πr."},
        {"q": "Was ist der Unterschied zwischen Sektor und Segment?", "a": "Ein Sektor ist ein kuchenförmiges Stück vom Mittelpunkt zum Bogen. Ein Segment ist die Fläche zwischen Bogen und Sehne."},
        {"q": "Wie berechnet man die Sagitta (Bogenhöhe)?", "a": "Die Bogenhöhe h berechnet sich nach h = r · (1 - cos(θ / 2))."}
    ]
    return {"proof_html": proof_html, "faq_html": faq_html, "faqs": faqs}

def get_roof_pitch_data(lang):
    proof_html = """<section class="proof-section" style="margin-top: 3rem;">
      <h2>Zimmerei & Dachgeometrie: Dachneigung & Sparrenlänge</h2>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">1</span><span>Neigungsverhältnis & Neigungswinkel</span></h3></div>
        <div class="proof-body"><p>Das Neigungsverhältnis X/12 definiert den Winkel: θ = arctan(Rise / Run) = arctan(X / 12).</p></div>
      </div>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">2</span><span>Sparrenlänge nach Pythagoras</span></h3></div>
        <div class="proof-body"><p>Die theoretische Sparrenlänge beträgt L = √(Rise² + Run²). Dazu addiert sich der Dachüberstand.</p></div>
      </div>
    </section>"""

    faq_html = """<section class="faq-section">
      <h2>FAQ: Dachneigung</h2>
      <div class="faq-item open">
        <div class="faq-question"><span>Was bedeutet eine Dachneigung von 6/12?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Auf 12 Einheiten horizontaler Länge steigt das Dach um 6 Einheiten an (ca. 26,57° Neigung).</div>
      </div>
      <div class="faq-item open">
        <div class="faq-question"><span>Wie berechnet man die wahre Sparrenlänge?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Mit dem Satz des Pythagoras aus Firsthöhe und halber Spannweite: Sparrenlänge = √(Firsthöhe² + halbe Spannweite²).</div>
      </div>
    </section>"""

    faqs = [
        {"q": "Was bedeutet eine Dachneigung von 6/12?", "a": "Auf 12 Einheiten horizontaler Länge steigt das Dach um 6 Einheiten an (ca. 26,57° Neigung)."},
        {"q": "Wie berechnet man die wahre Sparrenlänge?", "a": "Mit dem Satz des Pythagoras aus Firsthöhe und halber Spannweite: Sparrenlänge = √(Firsthöhe² + halbe Spannweite²)."}
    ]
    return {"proof_html": proof_html, "faq_html": faq_html, "faqs": faqs}

def get_mortgage_data(lang):
    proof_html = """<section class="proof-section" style="margin-top: 3rem;">
      <h2>Finanzmathematische Herleitung: Annuitätendarlehen</h2>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">1</span><span>Annuitätenformel für konstante Monatsraten</span></h3></div>
        <div class="proof-body"><p>Die monatliche Rate M berechnet sich aus Kreditsumme P, Monatszins i = r / 12 und Gesamtraten n: M = P · [i(1 + i)ⁿ] / [(1 + i)ⁿ - 1].</p></div>
      </div>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">2</span><span>Zins- und Tilgungsaufteilung</span></h3></div>
        <div class="proof-body"><p>Im Monat k beträgt der Zinsanteil I_k = B_{k-1} · i. Die Tilgung beträgt T_k = M - I_k.</p></div>
      </div>
    </section>"""

    faq_html = """<section class="faq-section">
      <h2>FAQ: Baufinanzierung & Tilgung</h2>
      <div class="faq-item open">
        <div class="faq-question"><span>Wie berechnet sich die monatliche Kreditrate?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Über die klassische Annuitätenformel aus Kreditsumme, Zinssatz und Laufzeit.</div>
      </div>
      <div class="faq-item open">
        <div class="faq-question"><span>Wie wirken sich Sondertilgungen aus?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Sondertilgungen reduzieren direkt die Restschuld, verkürzen die Gesamtlaufzeit und sparen erhebliche Zinskosten ein.</div>
      </div>
    </section>"""

    faqs = [
        {"q": "Wie berechnet sich die monatliche Kreditrate?", "a": "Über die klassische Annuitätenformel aus Kreditsumme, Zinssatz und Laufzeit."},
        {"q": "Wie wirken sich Sondertilgungen aus?", "a": "Sondertilgungen reduzieren direkt die Restschuld, verkürzen die Gesamtlaufzeit und sparen erhebliche Zinskosten ein."}
    ]
    return {"proof_html": proof_html, "faq_html": faq_html, "faqs": faqs}

def get_compound_interest_data(lang):
    proof_html = """<section class="proof-section" style="margin-top: 3rem;">
      <h2>Finanzmathematik: Zinseszinsformel</h2>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">1</span><span>Diskrete & Kontinuierliche Verzinsung</span></h3></div>
        <div class="proof-body"><p>Endkapital bei unterjähriger Verzinsung: FV = P · (1 + r / m)^(m · t). Bei kontinuierlicher Verzinsung: FV = P · e^(r · t).</p></div>
      </div>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">2</span><span>Effektiver Jahreszins (APY)</span></h3></div>
        <div class="proof-body"><p>Der effektive Jahreszins berücksichtigt unterjährige Zinseszinsen: APY = (1 + r / m)^m - 1.</p></div>
      </div>
    </section>"""

    faq_html = """<section class="faq-section">
      <h2>FAQ: Zinseszins</h2>
      <div class="faq-item open">
        <div class="faq-question"><span>Was ist der Unterschied zwischen Nominalzins und Effektivzins?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Der Effektivzins (APY) berücksichtigt den Zinseszinseffekt unterjähriger Zinsgutschriften und fällt daher höher aus als der Nominalzins.</div>
      </div>
      <div class="faq-item open">
        <div class="faq-question"><span>Was besagt die 72er-Regel?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Die Verdopplungszeit eines Kapitals in Jahren beträgt näherungsweise 72 dividiert durch den jährlichen Zinssatz in Prozent.</div>
      </div>
    </section>"""

    faqs = [
        {"q": "Was ist der Unterschied zwischen Nominalzins und Effektivzins?", "a": "Der Effektivzins (APY) berücksichtigt den Zinseszinseffekt unterjähriger Zinsgutschriften."},
        {"q": "Was besagt die 72er-Regel?", "a": "Die Verdopplungszeit eines Kapitals in Jahren beträgt näherungsweise 72 dividiert durch den Zinssatz."}
    ]
    return {"proof_html": proof_html, "faq_html": faq_html, "faqs": faqs}

def get_auto_loan_data(lang):
    proof_html = """<section class="proof-section" style="margin-top: 3rem;">
      <h2>Finanzierungsmathematik: Autokredit</h2>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">1</span><span>Finanzierungsbetrag & Monatsrate</span></h3></div>
        <div class="proof-body"><p>Finanzierter Nettobetrag: P = Fahrzeugpreis - Anzahlung - Inzahlungnahme + Steuern + Gebühren.</p></div>
      </div>
    </section>"""

    faq_html = """<section class="faq-section">
      <h2>FAQ: Autokredit</h2>
      <div class="faq-item open">
        <div class="faq-question"><span>Wie berechnet sich die Rate für einen Autokredit?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Die monatliche Rate berechnet sich über die Annuitätenformel aus Nettodarlehensbetrag, Effektivzins und Laufzeit in Monaten.</div>
      </div>
    </section>"""

    faqs = [
        {"q": "Wie berechnet sich die Rate für einen Autokredit?", "a": "Die monatliche Rate berechnet sich über die Annuitätenformel aus Nettodarlehensbetrag, Effektivzins und Laufzeit in Monaten."}
    ]
    return {"proof_html": proof_html, "faq_html": faq_html, "faqs": faqs}

def get_cagr_data(lang):
    proof_html = """<section class="proof-section" style="margin-top: 3rem;">
      <h2>Finanzanalytik: Jährliche Wachstumsrate (CAGR)</h2>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">1</span><span>Geometrisches Mittel der Rendite</span></h3></div>
        <div class="proof-body"><p>CAGR = (Endwert / Anfangswert)^(1 / t) - 1. Glättet Volatilität und berechnet die konstante Jahresrendite.</p></div>
      </div>
    </section>"""

    faq_html = """<section class="faq-section">
      <h2>FAQ: CAGR</h2>
      <div class="faq-item open">
        <div class="faq-question"><span>Was misst die Kennzahl CAGR?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">CAGR gibt die jährliche Wachstumsrate einer Investition unter der Annahme eines stetigen Wachstums an.</div>
      </div>
    </section>"""

    faqs = [
        {"q": "Was misst die Kennzahl CAGR?", "a": "CAGR gibt die jährliche Wachstumsrate einer Investition unter der Annahme eines stetigen Wachstums an."}
    ]
    return {"proof_html": proof_html, "faq_html": faq_html, "faqs": faqs}

def get_derivatives_data(lang):
    proof_html = """<section class="proof-section" style="margin-top: 3rem;">
      <h2>Differentialrechnung: Ableitungen & Kurvendiskussion</h2>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">1</span><span>Potenzregel für Polynome</span></h3></div>
        <div class="proof-body"><p>Für jeden Term x^n gilt d/dx [x^n] = n · x^(n - 1). Für f(x) = ax³ + bx² + cx + d ist f'(x) = 3ax² + 2bx + c.</p></div>
      </div>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">2</span><span>Tangenten- und Normalengleichung</span></h3></div>
        <div class="proof-body"><p>Tangentengleichung: y - y₀ = f'(x₀) · (x - x₀). Normalengleichung: y - y₀ = (-1 / f'(x₀)) · (x - x₀).</p></div>
      </div>
    </section>"""

    faq_html = """<section class="faq-section">
      <h2>FAQ: Ableitungen</h2>
      <div class="faq-item open">
        <div class="faq-question"><span>Was bedeutet die erste Ableitung geometrisch?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Die erste Ableitung f'(x₀) entspricht der Steigung der Tangente an den Funktionsgraphen an der Stelle x₀.</div>
      </div>
      <div class="faq-item open">
        <div class="faq-question"><span>Wie berechnet man die Tangentengleichung?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Über die Punkt-Steigungs-Form y = f'(x₀) · (x - x₀) + f(x₀).</div>
      </div>
    </section>"""

    faqs = [
        {"q": "Was bedeutet die erste Ableitung geometrisch?", "a": "Die erste Ableitung f'(x₀) entspricht der Steigung der Tangente an den Funktionsgraphen an der Stelle x₀."},
        {"q": "Wie berechnet man die Tangentengleichung?", "a": "Über die Punkt-Steigungs-Form y = f'(x₀) · (x - x₀) + f(x₀)."}
    ]
    return {"proof_html": proof_html, "faq_html": faq_html, "faqs": faqs}

def get_integrals_data(lang):
    proof_html = """<section class="proof-section" style="margin-top: 3rem;">
      <h2>Integralrechnung: Hauptsatz der Differential- und Integralrechnung</h2>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">1</span><span>Fundamentalsatz der Analysis</span></h3></div>
        <div class="proof-body"><p>Das bestimmte Integral einer stetigen Funktion f(x) von a bis b ist ∫_a^b f(x)dx = F(b) - F(a), wobei F'(x) = f(x).</p></div>
      </div>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">2</span><span>Stammfunktion von Polynomen</span></h3></div>
        <div class="proof-body"><p>Nach der Potenzregel für Integrale: ∫ x^n dx = [x^(n + 1)] / (n + 1) + C.</p></div>
      </div>
    </section>"""

    faq_html = """<section class="faq-section">
      <h2>FAQ: Integrale</h2>
      <div class="faq-item open">
        <div class="faq-question"><span>Was stellt das bestimmte Integral dar?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Das bestimmte Integral repräsentiert die vorzeichenbehaftete Fläche zwischen dem Funktionsgraphen und der Abszissenachse.</div>
      </div>
    </section>"""

    faqs = [
        {"q": "Was stellt das bestimmte Integral dar?", "a": "Das bestimmte Integral repräsentiert die vorzeichenbehaftete Fläche zwischen dem Funktionsgraphen und der Abszissenachse."}
    ]
    return {"proof_html": proof_html, "faq_html": faq_html, "faqs": faqs}

def get_sphere_data(lang):
    proof_html = """<section class="proof-section" style="margin-top: 3rem;">
      <h2>Archimedische Raumgeometrie: Kugel & Zylinder</h2>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">1</span><span>Archimedes' 2:3 Verhältnis</span></h3></div>
        <div class="proof-body"><p>Archimedes bewies 225 v. Chr., dass eine Kugel genau 2/3 des Volumens und der Oberfläche ihres umschriebenen Zylinders einnimmt: V = 4/3 · π · r³.</p></div>
      </div>
      <div class="proof-card open">
        <div class="proof-header"><h3><span class="step-num">2</span><span>Oberfläche entspricht vier Großkreisen</span></h3></div>
        <div class="proof-body"><p>Die Kugeloberfläche ist exakt viermal so groß wie die Fläche ihres Großkreises: A = 4 · π · r².</p></div>
      </div>
    </section>"""

    faq_html = """<section class="faq-section">
      <h2>FAQ: Kugel</h2>
      <div class="faq-item open">
        <div class="faq-question"><span>Warum ist die Kugeloberfläche viermal so groß wie der Großkreis?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Nach dem Satz von Archimedes entspricht die Mantelfläche der Kugel exakt vier Großkreisen mit Fläche πr², also 4πr².</div>
      </div>
      <div class="faq-item open">
        <div class="faq-question"><span>Wie berechnet man den Kugelradius aus dem Volumen?</span><span class="faq-icon">+</span></div>
        <div class="faq-answer">Aus V = (4/3)πr³ folgt durch Umkehrung r = ³√[ (3V) / (4π) ].</div>
      </div>
    </section>"""

    faqs = [
        {"q": "Warum ist die Kugeloberfläche viermal so groß wie der Großkreis?", "a": "Nach dem Satz von Archimedes entspricht die Mantelfläche der Kugel exakt vier Großkreisen mit Fläche πr², also 4πr²."},
        {"q": "Wie berechnet man den Kugelradius aus dem Volumen?", "a": "Aus V = (4/3)πr³ folgt durch Umkehrung r = ³√[ (3V) / (4π) ]."}
    ]
    return {"proof_html": proof_html, "faq_html": faq_html, "faqs": faqs}

def get_solver_template(slug, lang):
    if slug == "octagon":
        return get_polygon_data("Achteck", 8, "2(1 + √2)a² ≈ 4,828427a²", "r_i = ½(1 + √2)a", "3 Diagonallängen", lang)
    elif slug == "regular-polygon":
        return get_polygon_data("n-Eck", 8, "(n / 4) · a² · cot(π / n)", "r_i = a / [2 tan(π / n)]", "n(n - 3) / 2 Diagonalen", lang)
    elif slug == "hexagon":
        return get_polygon_data("Sechseck", 6, "(3√3 / 2)a² ≈ 2,598076a²", "r_i = (√3 / 2)a", "d_S = √3 a, d_L = 2a", lang)
    elif slug == "pentagon":
        return get_polygon_data("Fünfeck", 5, "¼√(25 + 10√5)a² ≈ 1,720477a²", "r_i = a / [2 tan(36°)]", "d = ϕ · a = ½(1 + √5)a", lang)
    elif slug == "decagon":
        return get_polygon_data("Zehneck", 10, "(5/2)a²√(5 + 2√5) ≈ 7,694209a²", "r_i = ½ a √(5 + 2√5)", "35 Diagonalen in 4 Längen", lang)
    elif slug == "right-triangle":
        return get_right_triangle_data(lang)
    elif slug == "circle-sector":
        return get_circle_sector_data(lang)
    elif slug == "roof-pitch":
        return get_roof_pitch_data(lang)
    elif slug == "mortgage-amortization":
        return get_mortgage_data(lang)
    elif slug == "compound-interest":
        return get_compound_interest_data(lang)
    elif slug == "auto-loan":
        return get_auto_loan_data(lang)
    elif slug == "cagr":
        return get_cagr_data(lang)
    elif slug == "derivatives":
        return get_derivatives_data(lang)
    elif slug == "integrals":
        return get_integrals_data(lang)
    elif slug == "sphere":
        return get_sphere_data(lang)
    return None
