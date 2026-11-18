/**
 * scripts/translations/statistics.js
 * Statistics Solvers Localizations (FAQs & Proofs) across 11 languages.
 * Solvers: bayes-theorem, permutations-combinations, standard-deviation, z-score
 */

export const STATISTICS = {
  "statistics/bayes-theorem": {
    faqs: {
      de: [
        { q: "Was ist der Prävalenzfehler (Base Rate Fallacy)?", a: "Der Prävalenzfehler ist die kognitive Verzerrung, die A-priori-Wahrscheinlichkeit einer Hypothese zu vernachlässigen. Selbst bei einem 99% genauen Test auf eine seltene Krankheit (1 zu 1000) ist ein positives Ergebnis wegen der geringen Grundrate nur zu etwa 9% zutreffend." },
        { q: "Wie wird der Satz von Bayes im maschinellen Lernen und der KI eingesetzt?", a: "Bayessche Inferenz treibt Spam-Filter (Naive Bayes), medizinische Diagnose-Systeme, Markov-Chain-Monte-Carlo-Algorithmen (MCMC) und Robotik-Sensorfusionen (Kalman-Filter) an." }
      ],
      es: [
        { q: "¿Qué es la falacia de la frecuencia base?", a: "Es el error cognitivo de ignorar la probabilidad a priori P(A). En enfermedades raras (1 de 1.000), un test con 99% de precisión solo implica un ~9% de probabilidad real tras un resultado positivo." },
        { q: "¿Cómo se utiliza el teorema de Bayes en aprendizaje automático e IA?", a: "La inferencia bayesiana alimenta clasificadores Naive Bayes para filtros de spam, sistemas de diagnóstico médico y filtros de Kalman para localización robótica." }
      ],
      fr: [
        { q: "Qu'est-ce que l'oubli de la fréquence de base ?", a: "C'est l'erreur cognitive consistant à négliger la probabilité a priori P(A). Pour une maladie rare (1 sur 1 000), un test fiable à 99 % ne donne qu'environ 9 % de probabilité d'être malade en cas de test positif." },
        { q: "Comment le théorème de Bayes est-il utilisé en machine learning et IA ?", a: "L'inférence bayésienne est au cœur des filtres anti-spam (Naive Bayes), des réseaux bayésiens de diagnostic médical et des filtres de Kalman en robotique." }
      ],
      it: [
        { q: "Cos'è l'errore del tasso di base (Base Rate Fallacy)?", a: "È l'errore cognitivo di ignorare la probabilità a priori P(A). Per una patologia rara (1 su 1.000), un test accurato al 99% comporta solo un ~9% di probabilità reale in caso di esito positivo." },
        { q: "Come viene usato il teorema di Bayes nel machine learning e nell'IA?", a: "L'inferenza bayesiana è alla base dei filtri anti-spam Naive Bayes, dei sistemi diagnostici e della fusione di sensori con filtri di Kalman." }
      ],
      pt: [
        { q: "O que é a falácia da taxa base?", a: "É o viés cognitivo de ignorar a probabilidade a priori P(A). Para uma condição rara (1 em 1.000), um teste com 99% de acerto resulta em apenas ~9% de chance real após resultado positivo." },
        { q: "Como o teorema de Bayes é usado em aprendizado de máquina e IA?", a: "A inferência bayesiana alimenta filtros de spam (Naive Bayes), diagnóstico médico automatizado e fusão de sensores com filtros de Kalman." }
      ],
      nl: [
        { q: "Wat is de base rate fallacy (basisfout)?", a: "Het is de denkfout waarbij de a priori kans P(A) wordt genegeerd. Bij een zeldzame aandoening (1 op 1.000) levert een 99% nauwkeurige test na een positieve uitslag slechts ~9% werkelijke trefkans op." },
        { q: "Hoe wordt de stelling van Bayes toegepast in machine learning en AI?", a: "Bayesiaanse inferentie vormt de basis van Naive Bayes spamfilters, medische expertsystemen en Kalman-filters in robotica." }
      ],
      pl: [
        { q: "Czym jest błąd koniunkcji z częstością bazową (Base Rate Fallacy)?", a: "To błąd poznawczy polegający na ignorowaniu prawdopodobieństwa a priori P(A). Przy rzadkiej chorobie (1 na 1000) test o czułości 99% oznacza jedynie ~9% szansy na rzeczywiste zachorowanie." },
        { q: "Jak twierdzenie Bayesa jest wykorzystywane w uczeniu maszynowym i AI?", a: "Wnioskowanie bayesowskie zasila filtry antyspamowe (Naive Bayes), systemy diagnostyki medycznej oraz filtry Kalmana w robotyce." }
      ],
      sv: [
        { q: "Vad är basfrekvensfelet (Base Rate Fallacy)?", a: "Det är det kognitiva misstaget att ignorera apriorisannolikheten P(A). Vid en ovanlig sjukdom (1 på 1 000) ger ett 99% säkert test endast ~9% sannolikhet för sjukdom vid positivt utfall." },
        { q: "Hur används Bayes sats inom maskininlärning och AI?", a: "Bayesiansk inferens driver Naive Bayes-skräppostfilter, medicinska diagnossystem och Kalman-filter för robotik." }
      ],
      no: [
        { q: "Hva er grunnfrekvensfeilen (Base Rate Fallacy)?", a: "Det er den kognitive feilslutningen å ignorere apriori-sannsynligheten P(A). Ved en sjelden tilstand (1 av 1 000) gir en 99% nøyaktig test bare ~9% reell sannsynlighet etter positiv prøve." },
        { q: "Hvordan brukes Bayes' teorem i maskinlæring og kunstig intelligens?", a: "Bayesiansk inferens driver søppelpostfiltre (Naive Bayes), medisinsk diagnostikk og Kalman-filtre i robotikk." }
      ],
      fi: [
        { q: "Mikä on perusfrekvenssiharha (Base Rate Fallacy)?", a: "Se on kognitiivinen vinouma, jossa jätetään huomiotta apriorinen todennäköisyys P(A). Harvinaisen taudin (1 / 1 000) kohdalla 99% tarkka testi antaa positiivisen tuloksen jälkeen vain noin 9% todellisen todennäköisyyden." },
        { q: "Miten Bayesin teoreemaa sovelletaan koneoppimisessa ja tekoälyssä?", a: "Bayesilainen päättely ohjaa roskapostisuodattimia (Naive Bayes), lääketieteellistä tekoälydiagnostiikkaa ja Kalman-suodattimia robotiikassa." }
      ],
      ro: [
        { q: "Ce este eroarea ratei de bază (Base Rate Fallacy)?", a: "Este eroarea cognitivă de a ignora probabilitatea a priori P(A). Pentru o afecțiune rară (1 la 1.000), un test precis în proporție de 99% oferă doar ~9% probabilitate reală la un rezultat pozitiv." },
        { q: "Cum este folosită teorema lui Bayes în învățarea automată și AI?", a: "Inferența bayesiană stă la baza filtrelor anti-spam Naive Bayes, sistemelor medicale de diagnoză și filtrelor Kalman în robotică." }
      ]
    },
    proofs: {
      de: [
        { title: "Definition der bedingten Wahrscheinlichkeit", body: "Verbundwahrscheinlichkeit P(A ∩ B) = P(A|B) · P(B) = P(B|A) · P(A). Gleichsetzen beider Seiten liefert die fundamentale Formel: P(A|B) = [P(B|A) · P(A)] / P(B)." },
        { title: "Satz von der totalen Wahrscheinlichkeit", body: "Die Evidenzwahrscheinlichkeit zerfällt über disjunkte Hypothesen: P(B) = P(B|A)P(A) + P(B|¬A)P(¬A)." },
        { title: "Auflösung des Prävalenzfehlers", body: "Wenn die A-priori-Wahrscheinlichkeit P(A) sehr klein ist, dominieren die Falsch-Positiven des dominierenden Komplements ¬A den Nenner." }
      ],
      es: [
        { title: "Definición de probabilidad condicional", body: "Probabilidad conjunta P(A ∩ B) = P(A|B) · P(B) = P(B|A) · P(A). Igualando ambos miembros: P(A|B) = [P(B|A) · P(A)] / P(B)." },
        { title: "Ley de probabilidad total", body: "La evidencia se particiona sobre hipótesis disjuntas: P(B) = P(B|A)P(A) + P(B|¬A)P(¬A)." },
        { title: "Resolución de la falacia de la frecuencia base", body: "Cuando la probabilidad a priori P(A) es muy reducida, los falsos positivos del complemento ¬A dominan el denominador." }
      ],
      fr: [
        { title: "Définition de la probabilité conditionnelle", body: "Probabilité conjointe P(A ∩ B) = P(A|B) · P(B) = P(B|A) · P(A). En égalisant les termes : P(A|B) = [P(B|A) · P(A)] / P(B)." },
        { title: "Loi des probabilités totales", body: "L'évidence se partitionne sur des hypothèses disjointes : P(B) = P(B|A)P(A) + P(B|¬A)P(¬A)." },
        { title: "Résolution de l'oubli de la fréquence de base", body: "Quand la probabilité a priori P(A) est minime, les faux positifs issus de ¬A dominent le dénominateur." }
      ],
      it: [
        { title: "Definizione di probabilità condizionata", body: "Probabilità congiunta P(A ∩ B) = P(A|B) · P(B) = P(B|A) · P(A). Uguagliando i membri: P(A|B) = [P(B|A) · P(A)] / P(B)." },
        { title: "Legge della probabilità totale", body: "L'evidenza complessiva si partiziona su ipotesi disgiunte: P(B) = P(B|A)P(A) + P(B|¬A)P(¬A)." },
        { title: "Risoluzione dell'errore del tasso di base", body: "Quando la probabilità a priori P(A) è molto bassa, i falsi positivi dominano il denominatore." }
      ],
      pt: [
        { title: "Definição de probabilidade condicional", body: "Probabilidade conjunta P(A ∩ B) = P(A|B) · P(B) = P(B|A) · P(A). Igualando os lados: P(A|B) = [P(B|A) · P(A)] / P(B)." },
        { title: "Lei da probabilidade total", body: "A evidência marginal particiona-se em hipóteses disjuntas: P(B) = P(B|A)P(A) + P(B|¬A)P(¬A)." },
        { title: "Resolução da falácia da taxa base", body: "Quando a probabilidade a priori P(A) é muito baixa, os falsos positivos de ¬A dominam o denominador." }
      ],
      nl: [
        { title: "Definitie van voorwaardelijke kans", body: "Gezamenlijke kans P(A ∩ B) = P(A|B) · P(B) = P(B|A) · P(A). Gelijkstellen geeft: P(A|B) = [P(B|A) · P(A)] / P(B)." },
        { title: "Wet van de totale kans", body: "De marginale evidentie splitst over disjuncte hypothesen: P(B) = P(B|A)P(A) + P(B|¬A)P(¬A)." },
        { title: "Verklaring van de basisfout", body: "Wanneer de a priori kans P(A) zeer klein is, domineren de vals-positieven van ¬A de noemer." }
      ],
      pl: [
        { title: "Definicja prawdopodobieństwa warunkowego", body: "Prawdopodobieństwo łączne P(A ∩ B) = P(A|B) · P(B) = P(B|A) · P(A). Po przyrównaniu: P(A|B) = [P(B|A) · P(A)] / P(B)." },
        { title: "Twierdzenie o prawdopodobieństwie całkowitym", body: "Prawdopodobieństwo całkowite rozkłada się na hipotezy rozłączne: P(B) = P(B|A)P(A) + P(B|¬A)P(¬A)." },
        { title: "Wyjaśnienie błędu częstości bazowej", body: "Gdy prawdopodobieństwo a priori P(A) jest bardzo małe, fałszywie dodatnie wyniki dominują mianownik." }
      ],
      sv: [
        { title: "Definition av betingad sannolikhet", body: "Betingad sannolikhet P(A ∩ B) = P(A|B) · P(B) = P(B|A) · P(A). Likheten ger: P(A|B) = [P(B|A) · P(A)] / P(B)." },
        { title: "Lagen om total sannolikhet", body: "Evidensen delas upp över disjunkta hypoteser: P(B) = P(B|A)P(A) + P(B|¬A)P(¬A)." },
        { title: "Förklaring av basfrekvensfelet", body: "När apriorisannolikheten P(A) är mycket låg dominerar falska positiva utfall nämnaren." }
      ],
      no: [
        { title: "Definisjon av betinget sannsynlighet", body: "Felles sannsynlighet P(A ∩ B) = P(A|B) · P(B) = P(B|A) · P(A). Likestilling gir: P(A|B) = [P(B|A) · P(A)] / P(B)." },
        { title: "Total sannsynlighetslov", body: "Evidensen partisjoneres over disjunkte hypoteser: P(B) = P(B|A)P(A) + P(B|¬A)P(¬A)." },
        { title: "Oppklaring av grunnfrekvensfeilen", body: "Når apriorisannsynligheten P(A) er svært lav, dominerer falske positive resultater nevneren." }
      ],
      fi: [
        { title: "Ehdollisen todennäköisyyden määritelmä", body: "Yhteistodennäköisyys P(A ∩ B) = P(A|B) · P(B) = P(B|A) · P(A). Yhtälöstä saadaan: P(A|B) = [P(B|A) · P(A)] / P(B)." },
        { title: "Kokonaistodennäköisyyden laki", body: "Todistusaineisto jakautuu erillisiin hypoteeseihin: P(B) = P(B|A)P(A) + P(B|¬A)P(¬A)." },
        { title: "Perusfrekvenssiharhan ratkaisu", body: "Kun apriorinen todennäköisyys P(A) on hyvin pieni, väärät positiiviset hallitsevat nimittäjää." }
      ],
      ro: [
        { title: "Definiția probabilității condiționate", body: "Probabilitatea reunită P(A ∩ B) = P(A|B) · P(B) = P(B|A) · P(A). Egalând termenii: P(A|B) = [P(B|A) · P(A)] / P(B)." },
        { title: "Legea probabilității totale", body: "Probabilitatea totală se partiționează pe ipoteze disjuncte: P(B) = P(B|A)P(A) + P(B|¬A)P(¬A)." },
        { title: "Rezolvarea erorii ratei de bază", body: "Când probabilitatea a priori P(A) este foarte redusă, rezultatele fals-pozitive domină numitorul." }
      ]
    }
  },

  "statistics/permutations-combinations": {
    faqs: {
      de: [
        { q: "Was ist der Hauptunterschied zwischen Permutationen und Kombinationen?", a: "Bei Permutationen spielt die Reihenfolge eine Rolle (z. B. PIN-Codes oder Platzierungen). Bei Kombinationen ist die Reihenfolge irrelevant (z. B. Lottozahlen oder Teamauswahlen)." },
        { q: "Warum ist 0! (0 Fakultät) gleich 1?", a: "Per Definition gibt es genau eine Möglichkeit, null Elemente anzuordnen (die leere Menge ∅). Zudem bewahrt 0! = 1 die Rekursion n! = n × (n - 1)! für n = 1." }
      ],
      es: [
        { q: "¿Cuál es la diferencia fundamental entre permutaciones y combinaciones?", a: "El orden importa en las permutaciones (códigos PIN, clasificaciones). El orden no importa en las combinaciones (loterías, selección de comités)." },
        { q: "¿Por qué 0! (cero factorial) es igual a 1?", a: "Por definición existe exactamente una forma de ordenar cero elementos (el conjunto vacío ∅). Además, satisface la relación n! = n × (n - 1)! cuando n = 1." }
      ],
      fr: [
        { q: "Quelle est la différence clé entre permutations et combinaisons ?", a: "L'ordre compte dans les permutations (codes de cadenas, podiums). L'ordre ne compte pas dans les combinaisons (mains de cartes, tirages du loto)." },
        { q: "Pourquoi 0! (factorielle zéro) vaut-il 1 ?", a: "Il existe exactement une façon d'ordonner zéro objet (l'ensemble vide ∅), et cela préserve la relation n! = n × (n - 1)! pour n = 1." }
      ],
      it: [
        { q: "Qual è la differenza fondamentale tra permutazioni e combinazioni?", a: "L'ordine conta nelle permutazioni (codici di sicurezza, classifiche). L'ordine non conta nelle combinazioni (mani di carte, lotterie)." },
        { q: "Perché 0! (fattoriale zero) è uguale a 1?", a: "Esiste esattamente un modo per ordinare zero oggetti (l'insieme vuoto ∅), preservando la proprietà ricorsiva n! = n × (n - 1)! per n = 1." }
      ],
      pt: [
        { q: "Qual a diferença entre permutações e combinações?", a: "A ordem importa nas permutações (senhas, pódios). A ordem não importa nas combinações (jogos de loteria, equipes)." },
        { q: "Por que 0! (zero fatorial) é igual a 1?", a: "Existe exatamente uma maneira de ordenar zero elementos (o conjunto vazio ∅), preservando a recursão n! = n × (n - 1)! para n = 1." }
      ],
      nl: [
        { q: "Wat is het belangrijkste verschil tussen permutaties en combinaties?", a: "Volgorde telt bij permutaties (pincodes, ranglijsten). Volgorde telt niet bij combinaties (loterijtrekkingen, commissies)." },
        { q: "Waarom is 0! (nul faculteit) gelijk aan 1?", a: "Er is exact één manier om nul objecten te rangschikken (de lege verzameling ∅), wat tevens de recursie n! = n × (n - 1)! bewaart voor n = 1." }
      ],
      pl: [
        { q: "Jaka jest różnica między permutacjami a kombinacjami?", a: "W permutacjach kolejność ma znaczenie (kody PIN, miejsca na podium). W kombinacjach kolejność nie ma znaczenia (losowania lotto, wybór delegacji)." },
        { q: "Dlaczego 0! (zero silnia) równa się 1?", a: "Z definicji istnieje dokładnie jeden sposób uporządkowania zera elementów (zbiór pusty ∅), co zachowuje tożsamość n! = n × (n - 1)! dla n = 1." }
      ],
      sv: [
        { q: "Vad är skillnaden mellan permutationer och kombinationer?", a: "Ordningen spelar roll i permutationer (pinkoder, placeringar). Ordningen saknar betydelse i kombinationer (lottorader, urval)." },
        { q: "Varför är 0! (noll fakultet) lika med 1?", a: "Det finns exakt ett sätt att ordna noll objekt (den tomma mängden ∅), vilket bevarar sambandet n! = n × (n - 1)! för n = 1." }
      ],
      no: [
        { q: "Hva er forskjellen mellom permutasjoner og kombinasjoner?", a: "Rekkefølgen betyr noe i permutasjoner (PIN-koder, plasseringer). Rekkefølgen betyr ingenting i kombinasjoner (lottotall, komitéutvalg)." },
        { q: "Hvorfor er 0! (null fakultet) lik 1?", a: "Det finnes nøyaktig én måte å ordne null objekter på (den tomme mengden ∅), noe som bevarer formelen n! = n × (n - 1)! for n = 1." }
      ],
      fi: [
        { q: "Mitä eroa on permutaatioilla ja kombinaatioilla?", a: "Järjestyksellä on väliä permutaatioissa (PIN-koodit, sijoitukset). Järjestyksellä ei ole väliä kombinaatioissa (lottorivit, ryhmävalinnat)." },
        { q: "Miksi 0! (nolla kertoma) on yhtä suuri kuin 1?", a: "Tyhjän joukon ∅ voi järjestää tasan yhdellä tavalla, mikä säilyttää relaation n! = n × (n - 1)! arvolla n = 1." }
      ],
      ro: [
        { q: "Care este diferența dintre permutări și combinări?", a: "Ordinea contează în permutări (coduri PIN, clasamente). Ordinea nu contează în combinări (bile de loterie, echipe)." },
        { q: "De ce 0! (zero factorial) este egal cu 1?", a: "Există exact un mod de a aranja zero elemente (mulțimea vidă ∅), ceea ce păstrează relația n! = n × (n - 1)! pentru n = 1." }
      ]
    },
    proofs: {
      de: [
        { title: "Fundamentales Zählprinzip (Permutationen)", body: "Die Auswahl von r geordneten Elementen aus n Objekten ergibt: n · (n - 1) · ... · (n - r + 1) = n! / (n - r)!." },
        { title: "Symmetrie und Quotientenbildung (Kombinationen)", body: "Da die r Elemente auf r! Arten permutiert werden können, dividiert man die Redundanz heraus: nCr = n! / [r! · (n - r)!]." },
        { title: "Pascalsche Rekursionsidentität", body: "Binomialkoeffizienten erfüllen Pascals Dreiecksregel: nCr = (n-1)C(r-1) + (n-1)Cr." }
      ],
      es: [
        { title: "Principio fundamental del conteo", body: "Seleccionar r elementos ordenados entre n objetos da: n · (n - 1) · ... · (n - r + 1) = n! / (n - r)!." },
        { title: "Simetría y división de redundancia", body: "Si el orden no importa, cada grupo puede ordenarse de r! formas: nCr = n! / [r! · (n - r)!]." },
        { title: "Identidad recurrente de Pascal", body: "Los coeficientes binomiales satisfacen la regla de Pascal: nCr = (n-1)C(r-1) + (n-1)Cr." }
      ],
      fr: [
        { title: "Principe fondamental de dénombrement", body: "Choisir r éléments ordonnés parmi n objets donne : n! / (n - r)!." },
        { title: "Symétrie et quotient de redondance", body: "L'ordre étant indifférent, chaque groupe de r éléments présente r! arrangements identiques : nCr = n! / [r! · (n - r)!]." },
        { title: "Identité de récurrence de Pascal", body: "Les coefficients binomiaux vérifient la règle du triangle de Pascal : nCr = (n-1)C(r-1) + (n-1)Cr." }
      ],
      it: [
        { title: "Principio fondamentale del calcolo combinatorio", body: "Selezionare r elementi ordinati tra n oggetti fornisce: n! / (n - r)!." },
        { title: "Simmetria e divisione delle ridondanze", body: "Se l'ordine non conta, ogni gruppo ammette r! permutazioni identiche: nCr = n! / [r! · (n - r)!]." },
        { title: "Identità di ricorrenza di Pascal", body: "I coefficienti binomiali soddisfano la regola di Pascal: nCr = (n-1)C(r-1) + (n-1)Cr." }
      ],
      pt: [
        { title: "Princípio fundamental da contagem", body: "Selecionar r itens ordenados entre n dá: n! / (n - r)!." },
        { title: "Simetria e eliminação da redundância", body: "Como a ordem é indiferente, divide-se por r!: nCr = n! / [r! · (n - r)!]." },
        { title: "Identidade de recorrência de Pascal", body: "Os coeficientes binomiais satisfazem a relação de Pascal: nCr = (n-1)C(r-1) + (n-1)Cr." }
      ],
      nl: [
        { title: "Fundamenteel telprincipe", body: "Het kiezen van r geordende elementen uit n geeft: n! / (n - r)!." },
        { title: "Symmetrie en deling van redundantie", body: "Als volgorde irrelevant is, deelt men door r!: nCr = n! / [r! · (n - r)!]." },
        { title: "Recursie-identiteit van Pascal", body: "Binomiaalcoëfficiënten voldoen aan Pascals regel: nCr = (n-1)C(r-1) + (n-1)Cr." }
      ],
      pl: [
        { title: "Podstawowa zasada kombinatoryki", body: "Wybór r uporządkowanych elementów z n obiektów daje: n! / (n - r)!." },
        { title: "Symetria i redukcja powtórzeń", body: "Gdy kolejność nie ma znaczenia, dzielimy przez r! permutacji: nCr = n! / [r! · (n - r)!]." },
        { title: "Tożsamość rekurencyjna Pascala", body: "Współczynniki dwumianowe spełniają regułę Pascala: nCr = (n-1)C(r-1) + (n-1)Cr." }
      ],
      sv: [
        { title: "Kombinatorikens grundprincip", body: "Val av r ordnade element bland n objekt ger: n! / (n - r)!." },
        { title: "Symmetri och redundansdivision", body: "Om ordningen är oviktig dividerar man med r!: nCr = n! / [r! · (n - r)!]." },
        { title: "Pascals identitet", body: "Binomialkoefficienter uppfyller Pascals triangelregel: nCr = (n-1)C(r-1) + (n-1)Cr." }
      ],
      no: [
        { title: "Kombinatorikkens grunnprinsipp", body: "Utvalg av r ordnede elementer blant n gir: n! / (n - r)!." },
        { title: "Symmetri og redundansdivisjon", body: "Dersom rekkefølgen er likegyldig, deles på r!: nCr = n! / [r! · (n - r)!]." },
        { title: "Pascals rekursjonsidentitet", body: "Binomialkoeffisienter oppfyller Pascals regel: nCr = (n-1)C(r-1) + (n-1)Cr." }
      ],
      fi: [
        { title: "Kombinatoriikan perusperiaate", body: "Valittaessa r järjestettyä alkiota n kohteesta: n! / (n - r)!." },
        { title: "Symmetria ja toistojen jako", body: "Jos järjestyksellä ei ole väliä, jaetaan luvulla r!: nCr = n! / [r! · (n - r)!]." },
        { title: "Pascalin rekursioidentiteetti", body: "Binomikertoimet toteuttavat Pascalin kolmiosäännön: nCr = (n-1)C(r-1) + (n-1)Cr." }
      ],
      ro: [
        { title: "Principiul fundamental al numărării", body: "Alegerea a r elemente ordonate din n obiecte dă: n! / (n - r)!." },
        { title: "Simetria și eliminarea redundanței", body: "Dacă ordinea este indiferentă, se împarte la r!: nCr = n! / [r! · (n - r)!]." },
        { title: "Identitatea de recurență a lui Pascal", body: "Coeficienții binomiali satisfac regula lui Pascal: nCr = (n-1)C(r-1) + (n-1)Cr." }
      ]
    }
  },

  "statistics/standard-deviation": {
    faqs: {
      de: [
        { q: "Wann sollte man die Stichproben-Standardabweichung (n - 1) verwenden?", a: "Verwenden Sie die Stichproben-Standardabweichung s (Bessel-Korrektur n - 1), wann immer Sie eine Teilmenge analysieren. Die Populationsformel (N) gilt nur, wenn der vollständige Datensatz vorliegt." },
        { q: "Was besagt die empirische 68-95-99,7-Regel?", a: "Bei einer Normalverteilung liegen ca. 68,27% aller Werte innerhalb von ±1σ um den Mittelwert, ca. 95,45% innerhalb von ±2σ und ca. 99,73% innerhalb von ±3σ." }
      ],
      es: [
        { q: "¿Cuándo usar la desviación típica muestral frente a la poblacional?", a: "Use la desviación muestral s (con corrección de Bessel n - 1) siempre que trabaje con una muestra. Use la poblacional (N) solo si mide la totalidad de la población." },
        { q: "¿Qué establece la regla empírica 68-95-99,7?", a: "Para una distribución normal, el 68,27% de las observaciones cae dentro de ±1σ de la media, el 95,45% dentro de ±2σ y el 99,73% dentro de ±3σ." }
      ],
      fr: [
        { q: "Quand utiliser l'écart-type échantillonnal plutôt que populationnel ?", a: "Utilisez l'écart-type échantillonnal s (correction de Bessel n - 1) dès que vos données sont un échantillon. Réservez la formule en N à la population entière." },
        { q: "Qu'énonce la règle empirique 68-95-99,7 ?", a: "Pour une loi normale, environ 68,27 % des valeurs se situent à ±1σ de la moyenne, 95,45 % à ±2σ et 99,73 % à ±3σ." }
      ],
      it: [
        { q: "Quando usare la deviazione standard campionaria rispetto a quella della popolazione?", a: "Utilizzare la deviazione campionaria s (con correzione di Bessel n - 1) per campioni parziali. Usare la formula con N solo per la popolazione completa." },
        { q: "Cosa stabilisce la regola empirica 68-95-99,7?", a: "In una distribuzione normale campanulare, il 68,27% delle osservazioni cade entro ±1σ dalla media, il 95,45% entro ±2σ e il 99,73% entro ±3σ." }
      ],
      pt: [
        { q: "Quando usar desvio padrão amostral versus populacional?", a: "Use o desvio amostral s (com correção de Bessel n - 1) sempre que seus dados forem uma amostra. Use N somente se tiver a população completa." },
        { q: "O que enuncia a regra empírica 68-95-99,7?", a: "Em uma curva normal, aproximadamente 68,27% dos dados estão a ±1σ da média, 95,45% a ±2σ e 99,73% a ±3σ." }
      ],
      nl: [
        { q: "Wanneer gebruik je steekproefstandaarddeviatie in plaats van populatiestandaarddeviatie?", a: "Gebruik steekproefstandaarddeviatie s (Bessel-correctie n - 1) bij een steekproef. Gebruik N alleen als de gehele populatie bekend is." },
        { q: "Wat houdt de 68-95-99,7 vuistregel in?", a: "Bij een normale verdeling ligt ca. 68,27% van de waarnemingen binnen ±1σ van het gemiddelde, 95,45% binnen ±2σ en 99,73% binnen ±3σ." }
      ],
      pl: [
        { q: "Kiedy stosować odchylenie standardowe z próby a kiedy z populacji?", a: "Stosuj odchylenie z próby s (poprawka Bessela n - 1), gdy analizujesz próbkę danych. Formułę z N stosuj tylko, gdy znasz całą populację." },
        { q: "Co mówi reguła empiryczna 68-95-99,7?", a: "W rozkładzie normalnym około 68,27% obserwacji mieści się w przedziale ±1σ od średniej, 95,45% w ±2σ, a 99,73% w ±3σ." }
      ],
      sv: [
        { q: "När ska man använda stickprovsstandardavvikelse kontra populationsstandardavvikelse?", a: "Använd stickprovsformeln s (Bessels korrektion n - 1) för urval. Använd N enbart om hela populationen mäts." },
        { q: "Vad innebär den empiriska 68-95-99,7-regeln?", a: "I en normalfördelning faller cirka 68,27% av observationerna inom ±1σ från medelvärdet, 95,45% inom ±2σ och 99,73% inom ±3σ." }
      ],
      no: [
        { q: "Når skal man bruke utvalgsstandardavvik mot populasjonsstandardavvik?", a: "Bruk utvalgsstandardavvik s (Bessels korreksjon n - 1) for stikkprøver. Bruk N kun når hele populasjonen er kjent." },
        { q: "Hva sier den empiriske 68-95-99,7-regelen?", a: "I en normalfordeling faller ca. 68,27% av dataene innenfor ±1σ fra gjennomsnittet, 95,45% innenfor ±2σ og 99,73% innenfor ±3σ." }
      ],
      fi: [
        { q: "Milloin käytetään otoksen keskihajontaa perusjoukon keskihajonnan sijasta?", a: "Käytä otoksen keskihajontaa s (Besselin korjaus n - 1) aina otokselle. Käytä jakajana N:ää vain jos koko perusjoukko on mitattu." },
        { q: "Mitä empiirinen 68-95-99,7-sääntö tarkoittaa?", a: "Normaalijakaumassa noin 68,27% havainnoista sijoittuu ±1σ etäisyydelle keskiarvosta, 95,45% välille ±2σ ja 99,73% välille ±3σ." }
      ],
      ro: [
        { q: "Când trebuie folosită deviația standard de eșantion față de cea de populație?", a: "Folosiți deviația de eșantion s (cu corecția lui Bessel n - 1) pentru eșantioane. Folosiți N doar dacă dispuneți de întreaga populație." },
        { q: "Ce reprezintă regula empirică 68-95-99,7?", a: "Într-o distribuție normală, 68,27% din valori se află în intervalul ±1σ față de medie, 95,45% în ±2σ și 99,73% în ±3σ." }
      ]
    },
    proofs: {
      de: [
        { title: "Transformation durch Zentrierung am Mittelwert", body: "Stichprobenmittelwert x̄ = (1/n) ∑ xᵢ. Abweichungen vom Mittelwert dᵢ = xᵢ - x̄ mit der Eigenschaft ∑ dᵢ ≡ 0." },
        { title: "Besselsche Korrektur für erwartungstreue Varianz", body: "Die Division durch n unterschätzt die Populationsvarianz, da der Stichprobenmittelwert bereits aus denselben Daten geschätzt wurde: s² = [1/(n - 1)] ∑ (xᵢ - x̄)²." },
        { title: "Metrik der Standardabweichung", body: "Die Standardabweichung s = √(s²) überführt die Streuung wieder in die ursprüngliche physikalische Maßeinheit der Daten." }
      ],
      es: [
        { title: "Centrado respecto a la media", body: "Media muestral x̄ = (1/n) ∑ xᵢ. Desviaciones dᵢ = xᵢ - x̄, cuya suma es idénticamente nula: ∑ dᵢ ≡ 0." },
        { title: "Corrección de Bessel para varianza insesgada", body: "Dividir por n subestima la varianza poblacional; la corrección insesgada divide por los grados de libertad: s² = [1/(n - 1)] ∑ (xᵢ - x̄)²." },
        { title: "Métrica de desviación estándar", body: "La desviación estándar s = √(s²) devuelve la medida de dispersión a las unidades originales de los datos." }
      ],
      fr: [
        { title: "Centrage par rapport à la moyenne", body: "Moyenne empirique x̄ = (1/n) ∑ xᵢ. Écarts à la moyenne dᵢ = xᵢ - x̄ vérifiant ∑ dᵢ ≡ 0." },
        { title: "Correction de Bessel pour variance sans biais", body: "Diviser par n sous-estime la variance de la population ; l'estimateur sans biais divise par (n - 1) : s² = [1/(n - 1)] ∑ (xᵢ - x̄)²." },
        { title: "Métrique de l'écart-type", body: "L'écart-type s = √(s²) ramène la mesure de dispersion dans l'unité physique des données d'origine." }
      ],
      it: [
        { title: "Centratura rispetto alla media", body: "Media campionaria x̄ = (1/n) ∑ xᵢ. Scarti dᵢ = xᵢ - x̄ con la proprietà fondamentale ∑ dᵢ ≡ 0." },
        { title: "Correzione di Bessel per varianza corretta", body: "Dividere per n sottostima la varianza; la stima corretta non distorta divide per i gradi di libertà: s² = [1/(n - 1)] ∑ (xᵢ - x̄)²." },
        { title: "Metrica della deviazione standard", body: "La deviazione standard s = √(s²) riporta la dispersione nella scala di misura originaria dei dati." }
      ],
      pt: [
        { title: "Centragem na média amostral", body: "Média amostral x̄ = (1/n) ∑ xᵢ. Desvios dᵢ = xᵢ - x̄ com soma identicamente nula: ∑ dᵢ ≡ 0." },
        { title: "Correção de Bessel para variância não viesada", body: "Dividir por n subestima a variância; o estimador não viesado divide por (n - 1): s² = [1/(n - 1)] ∑ (xᵢ - x̄)²." },
        { title: "Métrica do desvio padrão", body: "O desvio padrão s = √(s²) retorna a dispersão às unidades originais dos dados." }
      ],
      nl: [
        { title: "Centrering rond het steekproefgemiddelde", body: "Gemiddelde x̄ = (1/n) ∑ xᵢ. Afwijkingen dᵢ = xᵢ - x̄ met eigenschap ∑ dᵢ ≡ 0." },
        { title: "Bessel-correctie voor zuivere variantie", body: "Delen door n levert een onderschatting op; de zuivere schatter deelt door (n - 1): s² = [1/(n - 1)] ∑ (xᵢ - x̄)²." },
        { title: "Standaarddeviatie metriek", body: "De standaarddeviatie s = √(s²) herstelt de spreidingsmaat in de oorspronkelijke eenheid van de data." }
      ],
      pl: [
        { title: "Centrowanie wokół średniej próby", body: "Średnia z próby x̄ = (1/n) ∑ xᵢ. Odchylenia dᵢ = xᵢ - x̄ o sumie równej zeru: ∑ dᵢ ≡ 0." },
        { title: "Poprawka Bessela dla wariancji nieobciążonej", body: "Dzielenie przez n zaniża wariancję; estymator nieobciążony dzieli przez (n - 1): s² = [1/(n - 1)] ∑ (xᵢ - x̄)²." },
        { title: "Metryka odchylenia standardowego", body: "Odchylenie standardowe s = √(s²) sprowadza miarę rozproszenia do wyjściowych jednostek danych." }
      ],
      sv: [
        { title: "Centrering kring stickprovsmedelvärdet", body: "Medelvärde x̄ = (1/n) ∑ xᵢ. Avvikelser dᵢ = xᵢ - x̄ med egenskapen ∑ dᵢ ≡ 0." },
        { title: "Bessels korrektion för väntevärdesriktig varians", body: "Att dividera med n underskattar variansen; den väntevärdesriktiga skattningen dividerar med (n - 1): s² = [1/(n - 1)] ∑ (xᵢ - x̄)²." },
        { title: "Standardavvikelse som mått", body: "Standardavvikelsen s = √(s²) återför spridningsmåttet till dataunderlagets ursprungliga enhet." }
      ],
      no: [
        { title: "Sentrering rundt utvalgsgjennomsnittet", body: "Gjennomsnitt x̄ = (1/n) ∑ xᵢ. Avvik dᵢ = xᵢ - x̄ med egenskapen ∑ dᵢ ≡ 0." },
        { title: "Bessels korreksjon for forventningsrett varians", body: "Å dele på n underestimerer variansen; det forventningsrette estimatet deler på (n - 1): s² = [1/(n - 1)] ∑ (xᵢ - x̄)²." },
        { title: "Standardavvik som metrikk", body: "Standardavviket s = √(s²) fører spredningsmålet tilbake til den opprinnelige måleenheten." }
      ],
      fi: [
        { title: "Keskiarvokeskitys", body: "Otoksen keskiarvo x̄ = (1/n) ∑ xᵢ. Poikkeamat dᵢ = xᵢ - x̄, joiden summa on nolla: ∑ dᵢ ≡ 0." },
        { title: "Besselin korjaus harhattomalle varianssille", body: "Jakaminen n:llä aliarvioi varianssia; harhaton estimaattori jakaa luvulla (n - 1): s² = [1/(n - 1)] ∑ (xᵢ - x̄)²." },
        { title: "Keskihajonnan mitta", body: "Keskihajonta s = √(s²) palauttaa hajonnan mittauksen alkuperäiseen yksikköön." }
      ],
      ro: [
        { title: "Centrarea în jurul mediei de eșantion", body: "Media de eșantion x̄ = (1/n) ∑ xᵢ. Abaterile dᵢ = xᵢ - x̄ au proprietatea ∑ dᵢ ≡ 0." },
        { title: "Corecția lui Bessel pentru varianță nedeplasată", body: "Împărțirea la n subestimează varianța; estimatorul nedeplasat împarte la (n - 1): s² = [1/(n - 1)] ∑ (xᵢ - x̄)²." },
        { title: "Metrica deviației standard", body: "Deviația standard s = √(s²) readuce dispersia în unitățile de măsură inițiale ale datelor." }
      ]
    }
  },

  "statistics/z-score": {
    faqs: {
      de: [
        { q: "Was bedeutet ein negativer Z-Score?", a: "Ein negativer Z-Score (z < 0) zeigt an, dass der gemessene Rohwert unterhalb des Populationsmittelwerts liegt (z = -1,5 bedeutet 1,5 Standardabweichungen unter dem Mittelwert)." },
        { q: "Welcher Anteil der Daten liegt über z = 2,0?", a: "Da Φ(2,0) = 0,9772 (97,72% darunter) beträgt, liegen in einer Standardnormalverteilung genau 2,28% aller Beobachtungen oberhalb von z = 2,0." }
      ],
      es: [
        { q: "¿Qué indica una puntuación z negativa?", a: "Indica que la observación se sitúa por debajo de la media poblacional (un z = -1,5 está a 1,5 desviaciones estándar por debajo de la media)." },
        { q: "¿Qué porcentaje de datos se encuentra por encima de z = 2,0?", a: "Dado que Φ(2,0) = 0,9772 (97,72% por debajo), exactamente el 2,28% de las observaciones cae por encima de z = 2,0." }
      ],
      fr: [
        { q: "Que signifie un score z négatif ?", a: "Un score z négatif indique que la valeur observée est inférieure à la moyenne de la population (z = -1,5 signifie 1,5 écart-type sous la moyenne)." },
        { q: "Quel pourcentage des données se situe au-dessus de z = 2,0 ?", a: "Comme Φ(2,0) = 0,9772 (97,72 % en dessous), exactement 2,28 % des observations se situent au-dessus de z = 2,0." }
      ],
      it: [
        { q: "Cosa indica un punteggio z negativo?", a: "Un punteggio z negativo indica che l'osservazione si trova al di sotto della media della popolazione (z = -1,5 significa 1,5 deviazioni standard sotto la media)." },
        { q: "Quale percentuale di dati si trova sopra z = 2,0?", a: "Dato che Φ(2,0) = 0,9772 (97,72% al di sotto), esattamente il 2,28% dei dati cade al di sopra di z = 2,0." }
      ],
      pt: [
        { q: "O que indica um escore z negativo?", a: "Indica que a observação está abaixo da média populacional (z = -1,5 significa 1,5 desvio padrão abaixo da média)." },
        { q: "Qual porcentagem de dados fica acima de z = 2,0?", a: "Como Φ(2,0) = 0,9772 (97,72% abaixo), exatamente 2,28% das observações ficam acima de z = 2,0." }
      ],
      nl: [
        { q: "Wat betekent een negatieve z-score?", a: "Een negatieve z-score geeft aan dat de waarneming onder het populatiegemiddelde ligt (z = -1,5 is 1,5 standaarddeviatie onder het gemiddelde)." },
        { q: "Welk percentage van de gegevens ligt boven z = 2,0?", a: "Omdat Φ(2,0) = 0,9772 (97,72% eronder), ligt exact 2,28% van de data boven z = 2,0." }
      ],
      pl: [
        { q: "Co oznacza ujemny wskaźnik z-score?", a: "Ujemny z-score wskazuje, że wynik surowy leży poniżej średniej populacji (z = -1,5 oznacza 1,5 odchylenia standardowego poniżej średniej)." },
        { q: "Jaki odsetek danych leży powyżej z = 2,0?", a: "Ponieważ dystrybuanta Φ(2,0) = 0,9772 (97,72% poniżej), dokładnie 2,28% obserwacji leży powyżej z = 2,0." }
      ],
      sv: [
        { q: "Vad betyder ett negativt z-värde?", a: "Ett negativt z-värde anger att observationen ligger under populationens medelvärde (z = -1,5 innebär 1,5 standardavvikelser under medelvärdet)." },
        { q: "Hur stor andel av datamängden ligger över z = 2,0?", a: "Eftersom Φ(2,0) = 0,9772 (97,72% under), ligger exakt 2,28% av observationerna över z = 2,0." }
      ],
      no: [
        { q: "Hva betyr en negativ z-skår?", a: "En negativ z-skår angir at observasjonen ligger under populasjonsgjennomsnittet (z = -1,5 betyr 1,5 standardavvik under snittet)." },
        { q: "Hvor stor andel av dataene faller over z = 2,0?", a: "Fordi Φ(2,0) = 0,9772 (97,72% under), faller nøyaktig 2,28% av observasjonene over z = 2,0." }
      ],
      fi: [
        { q: "Mitä negatiivinen z-pistemäärä tarkoittaa?", a: "Negatiivinen z-arvo osoittaa, että havaintoarvo on perusjoukon keskiarvon alapuolella (z = -1,5 tarkoittaa 1,5 keskihajontaa keskiarvon alapuolella)." },
        { q: "Kuinka suuri osuus havainnoista sijoittuu arvon z = 2,0 yläpuolelle?", a: "Koska kertymäfunktio Φ(2,0) = 0,9772 (97,72% alapuolella), tasan 2,28% havainnoista on arvon z = 2,0 yläpuolella." }
      ],
      ro: [
        { q: "Ce indică un scor z negativ?", a: "Un scor z negativ indică faptul că observația se situează sub media populației (z = -1,5 înseamnă 1,5 deviații standard sub medie)." },
        { q: "Ce procent din date se situează peste z = 2,0?", a: "Deoarece Φ(2,0) = 0,9772 (97,72% dedesubt), exact 2,28% din observații cad peste z = 2,0." }
      ]
    },
    proofs: {
      de: [
        { title: "Standardisierungs-Normalisierung", body: "Der Z-Score misst die Distanz einer Beobachtung zum Mittelwert in Einheiten der Standardabweichung: z = (x - μ) / σ." },
        { title: "Gauss'sche kumulative Verteilungsfunktion", body: "Kumulative Wahrscheinlichkeit Φ(z) = (1 / √2π) ∫₋∞ᶻ e^(-t²/2) dt = ½[1 + erf(z / √2)]." },
        { title: "Signifikanzgrenze im Hypothesentest", body: "Im zweiseitigen Hypothesentest entspricht |z| ≥ 1,96 genau dem Signifikanzniveau p ≤ 0,05." }
      ],
      es: [
        { title: "Normalización de tipificación", body: "La puntuación z mide a cuántas desviaciones estándar se encuentra una observación respecto a la media: z = (x - μ) / σ." },
        { title: "Función de distribución acumulada gaussiana", body: "Probabilidad acumulada Φ(z) = (1 / √2π) ∫₋∞ᶻ e^(-t²/2) dt = ½[1 + erf(z / √2)]." },
        { title: "Umbral de contraste de hipótesis", body: "En un contraste bilateral, |z| ≥ 1,96 corresponde al nivel de significación estadística p ≤ 0,05." }
      ],
      fr: [
        { title: "Normalisation par centrage-réduction", body: "Le score z mesure l'écart à la moyenne en unités d'écart-type : z = (x - μ) / σ." },
        { title: "Fonction de répartition gaussienne", body: "Probabilité cumulée Φ(z) = (1 / √2π) ∫₋∞ᶻ e^(-t²/2) dt = ½[1 + erf(z / √2)]." },
        { title: "Seuil de test d'hypothèse", body: "Dans un test bilatéral, |z| ≥ 1,96 correspond au seuil de signification statistique p ≤ 0,05." }
      ],
      it: [
        { title: "Normalizzazione e standardizzazione", body: "Il punteggio z quantifica quante deviazioni standard un valore dista dalla media: z = (x - μ) / σ." },
        { title: "Funzione di ripartizione gaussiana", body: "Probabilità cumulata Φ(z) = (1 / √2π) ∫₋∞ᶻ e^(-t²/2) dt = ½[1 + erf(z / √2)]." },
        { title: "Soglia per la verifica di ipotesi", body: "In un test a due code, |z| ≥ 1,96 corrisponde alla significatività p ≤ 0,05." }
      ],
      pt: [
        { title: "Padronização e normalização", body: "O escore z afere quantos desvios padrão uma observação está da média: z = (x - μ) / σ." },
        { title: "Função de distribuição acumulada gaussiana", body: "Probabilidade acumulada Φ(z) = (1 / √2π) ∫₋∞ᶻ e^(-t²/2) dt = ½[1 + erf(z / √2)]." },
        { title: "Critério de teste de hipótese", body: "Em testes bicaudais, |z| ≥ 1,96 corresponde à significância estatística p ≤ 0,05." }
      ],
      nl: [
        { title: "Standaardisatie en normalisatie", body: "De z-score geeft aan hoeveel standaarddeviaties een waarneming van het gemiddelde afligt: z = (x - μ) / σ." },
        { title: "Gaussische cumulatieve verdelingsfunctie", body: "Cumulatieve kans Φ(z) = (1 / √2π) ∫₋∞ᶻ e^(-t²/2) dt = ½[1 + erf(z / √2)]." },
        { title: "Toetsingscriterium hypothesen", body: "Bij tweezijdig toetsen correspondeert |z| ≥ 1,96 met p ≤ 0,05." }
      ],
      pl: [
        { title: "Standaryzacja zmiennej losowej", body: "Wskaźnik z mierzy, o ile odchyleń standardowych wynik x różni się od średniej: z = (x - μ) / σ." },
        { title: "Dystrybuanta rozkładu normalnego Gaussa", body: "Prawdopodobieństwo skumulowane Φ(z) = (1 / √2π) ∫₋∞ᶻ e^(-t²/2) dt = ½[1 + erf(z / √2)]." },
        { title: "Wartość krytyczna testowania hipotez", body: "W teście dwustronnym |z| ≥ 1,96 odpowiada poziomowi istotności p ≤ 0,05." }
      ],
      sv: [
        { title: "Standardisering och normalisering", body: "Z-värdet mäter hur många standardavvikelser en observation avviker från medelvärdet: z = (x - μ) / σ." },
        { title: "Gauss kumulativa fördelningsfunktion", body: "Kumulativ sannolikhet Φ(z) = (1 / √2π) ∫₋∞ᶻ e^(-t²/2) dt = ½[1 + erf(z / √2)]." },
        { title: "Hypotestestningströskel", body: "Vid tvåsidigt hypotesprövning motsvarar |z| ≥ 1,96 signifikansnivån p ≤ 0,05." }
      ],
      no: [
        { title: "Standardisering og normalisering", body: "Z-skåren måler hvor mange standardavvik en observasjon avviker fra gjennomsnittet: z = (x - μ) / σ." },
        { title: "Gaussisk kumulativ fordelingsfunksjon", body: "Kumulativ sannsynlighet Φ(z) = (1 / √2π) ∫₋∞ᶻ e^(-t²/2) dt = ½[1 + erf(z / √2)]." },
        { title: "Kritisk verdi ved hypotesetesting", body: "I en tosidig hypotesetest svarer |z| ≥ 1,96 til signifikansnivået p ≤ 0,05." }
      ],
      fi: [
        { title: "Standardointi ja normalisointi", body: "Z-pistemäärä osoittaa, kuinka monen keskihajonnan päässä havainto on keskiarvosta: z = (x - μ) / σ." },
        { title: "Gaussin kertymäfunktio", body: "Kertymätodennäköisyys Φ(z) = (1 / √2π) ∫₋∞ᶻ e^(-t²/2) dt = ½[1 + erf(z / √2)]." },
        { title: "Hypoteesitestauksen raja-arvo", body: "Kaksisuuntaisessa testissä |z| ≥ 1,96 vastaa tilastollista merkitsevyystasoa p ≤ 0,05." }
      ],
      ro: [
        { title: "Standardizarea și normalizarea", body: "Scorul z măsoară distanța de la observație la medie în unități de deviație standard: z = (x - μ) / σ." },
        { title: "Funcția de repartiție gaussiană", body: "Probabilitatea cumulată Φ(z) = (1 / √2π) ∫₋∞ᶻ e^(-t²/2) dt = ½[1 + erf(z / √2)]." },
        { title: "Pragul de testare a ipotezelor", body: "Într-un test bilateral, |z| ≥ 1,96 corespunde pragului de semnificație statistică p ≤ 0,05." }
      ]
    }
  }
};

