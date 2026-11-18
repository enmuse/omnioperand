/**
 * scripts/translations/geometry_2d.js
 * 2D Geometry Solvers Localizations (FAQs & Proofs) across 11 languages.
 * Solvers: ellipse, trapezoid, rhombus, parallelogram, kite, arc-length
 */

export const GEOMETRY_2D = {
  "geometry/ellipse": {
    faqs: {
      de: [
        {
          q: "Warum gibt es keine einfache geschlossene Formel für den Umfang einer Ellipse?",
          a: "Im Gegensatz zu einem Kreis variiert die Krümmung einer Ellipse stetig. Die Integration des Bogenelements führt auf ein unvollständiges elliptisches Integral zweiter Art E(e), das sich nicht durch elementare algebraische Funktionen darstellen lässt."
        },
        {
          q: "Wie groß ist der Fehler der zweiten Näherungsformel von Ramanujan?",
          a: "Die zweite Näherungsformel von Ramanujan besitzt selbst für extrem langgestreckte Ellipsen einen maximalen relativen Fehler von unter 0,0015% und garantiert Sub-Millimeter-Präzision in ingenieurwissenschaftlichen Anwendungen."
        }
      ],
      es: [
        {
          q: "¿Por qué no existe una fórmula cerrada simple para el perímetro de una elipse?",
          a: "A diferencia de un círculo donde la curvatura es constante, en una elipse varía continuamente. La integración del elemento de arco conduce a una integral elíptica de segunda especie que no puede expresarse mediante funciones algebraicas elementales."
        },
        {
          q: "¿Cuál es el error de la segunda fórmula de perímetro de Ramanujan?",
          a: "La segunda aproximación de Ramanujan presenta un error relativo máximo extraordinariamente bajo, inferior al 0,0015% incluso para elipses extremadamente aplanadas con excentricidad cercana a 1."
        }
      ],
      fr: [
        {
          q: "Pourquoi n'y a-t-il pas de formule fermée simple pour le périmètre d'une ellipse ?",
          a: "Contrairement au cercle dont la courbure est constante, celle d'une ellipse varie continuellement. L'intégration de l'élément d'arc mène à une intégrale elliptique de deuxième espèce non réductible à des fonctions élémentaires."
        },
        {
          q: "Quelle est l'erreur de la seconde formule de périmètre de Ramanujan ?",
          a: "La seconde formule approchée de Ramanujan présente une erreur relative maximale inférieure à 0,0015 %, même pour des ellipses extrêmement aplaties dont l'excentricité approche 1."
        }
      ],
      it: [
        {
          q: "Perché non esiste una formula chiusa semplice per il perimetro di un'ellisse?",
          a: "A differenza del cerchio in cui la curvatura è costante, nell'ellisse varia continuamente. L'integrazione dell'elemento d'arco porta a un integrale ellittico di seconda specie non esprimibile con funzioni algebriche elementari."
        },
        {
          q: "Qual è l'errore della seconda formula del perimetro di Ramanujan?",
          a: "La seconda approssimazione di Ramanujan ha un errore relativo massimo straordinariamente ridotto, inferiore allo 0,0015% anche per ellissi molto schiacciate."
        }
      ],
      pt: [
        {
          q: "Por que não existe uma fórmula fechada simples para o perímetro de uma elipse?",
          a: "Ao contrário do círculo com curvatura constante, a curvatura de uma elipse varia continuamente. A integração do elemento de arco resulta em uma integral elíptica de segunda espécie sem representação algébrica elementar."
        },
        {
          q: "Qual é o erro da segunda fórmula de perímetro de Ramanujan?",
          a: "A segunda aproximação de Ramanujan apresenta um erro relativo máximo inferior a 0,0015%, mesmo para elipses extremamente achatadas com excentricidade próxima a 1."
        }
      ],
      nl: [
        {
          q: "Waarom is er geen eenvoudige gesloten formule voor de omtrek van een ellips?",
          a: "In tegenstelling tot een cirkel varieert de kromming van een ellips continu. Het integreren van het boogelement leidt tot een niet-elementaire elliptische integraal van de tweede soort."
        },
        {
          q: "Wat is de fout van Ramanujans tweede omtreksformule?",
          a: "De tweede benadering van Ramanujan heeft een uitzonderlijk kleine maximale relatieve fout van minder dan 0,0015%, zelfs voor zeer langgerekte ellipsen."
        }
      ],
      pl: [
        {
          q: "Dlaczego nie istnieje prosty zwarty wzór na obwód elipsy?",
          a: "W przeciwieństwie do koła o stałej krzywiźnie, krzywizna elipsy zmienia się w sposób ciągły. Całkowanie elementu łuku prowadzi do nieelementarnej całki eliptycznej drugiego rodzaju."
        },
        {
          q: "Jaki jest błąd drugiego wzoru Ramanujana na obwód elipsy?",
          a: "Drugie przybliżenie Ramanujana charakteryzuje się niezwykle małym błędem względnym poniżej 0,0015% nawet dla silnie spłaszczonych elips."
        }
      ],
      sv: [
        {
          q: "Varför finns det ingen enkel sluten formel för en ellips omkrets?",
          a: "Till skillnad från en cirkel med konstant krökning varierar en ellips krökning kontinuerligt. Integrering av bågelementet ger en icke-elementär elliptisk integral av andra slaget."
        },
        {
          q: "Vad är felet i Ramanujans andra omkretsformel?",
          a: "Ramanujans andra approximation har ett maximalt relativt fel på under 0,0015% även för extremt avlånga ellipser med excentricitet nära 1."
        }
      ],
      no: [
        {
          q: "Hvorfor finnes det ingen enkel lukket formel for omkretsen av en ellipse?",
          a: "I motsetning til en sirkel med konstant krumning, varierer krumningen til en ellipse kontinuerlig. Integrering av buelengdedifferensialet gir et ikke-elementært elliptisk integral som ikke kan uttrykkes med enkle funksjoner."
        },
        {
          q: "Hva er feilen i Ramanujans andre omkretsformel?",
          a: "Ramanujans andre tilnærming har en maksimal relativ feil på under 0,0015% selv for svært flate ellipser med eksentrisitet nær 1."
        }
      ],
      fi: [
        {
          q: "Miksi ellipsin kehän pituudelle ei ole yksinkertaista suljettua kaavaa?",
          a: "Toisin kuin ympyrässä, ellipsin kaarevuus vaihtelee jatkuvasti. Kaarenpituuden differentiaalin integrointi johtaa toisen lajin elliptiseen integraaliin, jota ei voida esittää alkeisfunktioilla."
        },
        {
          q: "Mikä on Ramanujanin toisen kehäkaavan virhe?",
          a: "Ramanujanin toisen approksimaation suurin suhteellinen virhe on poikkeuksellisen pieni, alle 0,0015% jopa erittäin litteille ellipseille."
        }
      ],
      ro: [
        {
          q: "De ce nu există o formulă închisă simplă pentru perimetrul unei elipse?",
          a: "Spre deosebire de cerc unde curbura este constantă, curbura unei elipse variază continuu. Integrarea diferențialei lungimii arcului duce la o integrală eliptică de speța a doua ce nu poate fi exprimată prin funcții algebrice elementare."
        },
        {
          q: "Care este eroarea celei de-a doua formule de perimetru a lui Ramanujan?",
          a: "A doua aproximare a lui Ramanujan are o eroare relativă maximă de sub 0,0015% chiar și pentru elipse foarte aplatizate cu excentricitatea apropiată de 1."
        }
      ]
    },
    proofs: {
      de: [
        { title: "Affine Streckung und Flächenintegral", body: "Eine Ellipse x²/a² + y²/b² = 1 entsteht durch lineare Streckung des Einheitskreises um a horizontal und b vertikal: Fläche = ∫∫ dx dy = π · a · b." },
        { title: "Zweite Umfangsformel nach Ramanujan", body: "Da der exakte Umfang ein elliptisches Integral erfordert, formulierte Srinivasa Ramanujan die hochpräzise geschlossene Näherung: P ≈ π(a + b)[1 + 3h / (10 + √(4 - 3h))], wobei h = (a - b)² / (a + b)²." },
        { title: "Brennpunkte und lineare Exzentrizität", body: "Linearer Brennpunktsabstand c = √(a² - b²). Numerische Exzentrizität e = c / a = √(1 - b²/a²). Bei e = 0 ist die Ellipse ein Kreis; für e ➔ 1 nähert sie sich einer Parabel." }
      ],
      es: [
        { title: "Integral de área por estiramiento afín", body: "Una elipse x²/a² + y²/b² = 1 es la transformación lineal del círculo unidad estirado horizontalmente por a y verticalmente por b: Área = ∫∫ dx dy = π · a · b." },
        { title: "Segunda fórmula de perímetro de Ramanujan", body: "Dado que el perímetro exacto requiere una integral elíptica, Srinivasa Ramanujan dedujo la aproximación cerrada: P ≈ π(a + b)[1 + 3h / (10 + √(4 - 3h))], con h = (a - b)² / (a + b)²." },
        { title: "Focos y excentricidad orbital", body: "Distancia focal lineal c = √(a² - b²). Primera excentricidad e = c / a = √(1 - b²/a²). Cuando e = 0 es un círculo perfecto; cuando e ➔ 1 se aplana hacia una parábola." }
      ],
      fr: [
        { title: "Intégrale d'aire par étirement affine", body: "Une ellipse x²/a² + y²/b² = 1 est la transformation affine du cercle unité étiré de a horizontalement et de b verticalement : Aire = ∫∫ dx dy = π · a · b." },
        { title: "Seconde formule de périmètre de Ramanujan", body: "Le périmètre exact exigeant une intégrale elliptique, Srinivasa Ramanujan a formulé l'approximation fermée : P ≈ π(a + b)[1 + 3h / (10 + √(4 - 3h))], où h = (a - b)² / (a + b)²." },
        { title: "Foyers et excentricité orbitale", body: "Distance focale linéaire c = √(a² - b²). Excentricité e = c / a = √(1 - b²/a²). Si e = 0 l'ellipse est un cercle parfait ; si e ➔ 1 elle tend vers une parabole." }
      ],
      it: [
        { title: "Integrale d'area per dilatazione affine", body: "Un'ellisse x²/a² + y²/b² = 1 è la trasformazione lineare del cerchio unitario dilatato di a in orizzontale e b in verticale: Area = ∫∫ dx dy = π · a · b." },
        { title: "Seconda formula del perimetro di Ramanujan", body: "Poiché il perimetro esatto richiede un integrale ellittico, Srinivasa Ramanujan formulò l'approssimazione chiusa: P ≈ π(a + b)[1 + 3h / (10 + √(4 - 3h))], con h = (a - b)² / (a + b)²." },
        { title: "Fuochi ed eccentricità orbitale", body: "Distanza focale c = √(a² - b²). Eccentricità e = c / a = √(1 - b²/a²). Quando e = 0 l'ellisse coincide con un cerchio; per e ➔ 1 degenera verso una parabola." }
      ],
      pt: [
        { title: "Integral de área por transformação afim", body: "Uma elipse x²/a² + y²/b² = 1 é a transformação afim do círculo unitário esticado por a horizontalmente e b verticalmente: Área = ∫∫ dx dy = π · a · b." },
        { title: "Segunda fórmula de perímetro de Ramanujan", body: "Como o perímetro exato requer uma integral elíptica, Srinivasa Ramanujan formulou a aproximação fechada: P ≈ π(a + b)[1 + 3h / (10 + √(4 - 3h))], onde h = (a - b)² / (a + b)²." },
        { title: "Focos e excentricidade orbital", body: "Distância focal linear c = √(a² - b²). Excentricidade e = c / a = √(1 - b²/a²). Quando e = 0 é um círculo perfeito; quando e ➔ 1 aproxima-se de uma parábola." }
      ],
      nl: [
        { title: "Oppervlakte-integraal via affiene rek", body: "Een ellips x²/a² + y²/b² = 1 is de lineaire transformatie van een eenheidscirkel gerekt met a horizontaal en b verticaal: Oppervlakte = ∫∫ dx dy = π · a · b." },
        { title: "Ramanujans tweede omtreksformule", body: "Omdat de exacte omtrek een elliptische integraal vereist, formuleerde Ramanujan de gesloten benadering: P ≈ π(a + b)[1 + 3h / (10 + √(4 - 3h))], waarin h = (a - b)² / (a + b)²." },
        { title: "Brandpunten en excentriciteit", body: "Lineaire brandpuntsafstand c = √(a² - b²). Excentriciteit e = c / a = √(1 - b²/a²). Bij e = 0 is het een cirkel; bij e ➔ 1 rekt hij uit naar een parabool." }
      ],
      pl: [
        { title: "Całka pola przez rozciąganie afiniczne", body: "Elipsa x²/a² + y²/b² = 1 jest liniowym przekształceniem koła jednostkowego rozciągniętego o a w poziomie i b w pionie: Pole = ∫∫ dx dy = π · a · b." },
        { title: "Drugi wzór Ramanujana na obwód", body: "Ponieważ dokładny obwód wymaga całki eliptycznej, Ramanujan sformułował zamknięte przybliżenie: P ≈ π(a + b)[1 + 3h / (10 + √(4 - 3h))], gdzie h = (a - b)² / (a + b)²." },
        { title: "Ogniska i mimośród orbitalny", body: "Liniowa odległość ogniskowa c = √(a² - b²). Mimośród e = c / a = √(1 - b²/a²). Gdy e = 0, elipsa staje się kołem; gdy e ➔ 1, spłaszcza się do paraboli." }
      ],
      sv: [
        { title: "Ytintegral genom affin sträckning", body: "En ellips x²/a² + y²/b² = 1 är den linjära transformationen av en enhetscirkel sträckt med a horisontellt och b vertikalt: Area = ∫∫ dx dy = π · a · b." },
        { title: "Ramanujans andra omkretsformel", body: "Eftersom den exakta omkretsen kräver en elliptisk integral formulerade Ramanujan approximationen: P ≈ π(a + b)[1 + 3h / (10 + √(4 - 3h))], där h = (a - b)² / (a + b)²." },
        { title: "Brännpunkter och excentricitet", body: "Linjärt brännpunktsavstånd c = √(a² - b²). Excentricitet e = c / a = √(1 - b²/a²). Vid e = 0 är det en cirkel; när e ➔ 1 närmar den sig en parabel." }
      ],
      no: [
        { title: "Arealintegral ved affin strekking", body: "En ellipse x²/a² + y²/b² = 1 er den lineære transformasjonen av en enhetssirkel strukket med a horisontalt og b vertikalt: Areal = ∫∫ dx dy = π · a · b." },
        { title: "Ramanujans andre omkretsformel", body: "Fordi den eksakte omkretsen krever et elliptisk integral, formulerte Ramanujan den lukkede tilnærmingen: P ≈ π(a + b)[1 + 3h / (10 + √(4 - 3h))], der h = (a - b)² / (a + b)²." },
        { title: "Brennpunkter og eksentrisitet", body: "Lineær brennpunktsavstand c = √(a² - b²). Eksentrisitet e = c / a = √(1 - b²/a²). Når e = 0 er ellipsen en sirkel; når e ➔ 1 strekkes den mot en parabel." }
      ],
      fi: [
        { title: "Pinta-alan integraali affiinilla venytyksellä", body: "Ellipsi x²/a² + y²/b² = 1 saadaan yksikköympyrästä venyttämällä vaakasuunnassa kertoimella a ja pystysuunnassa kertoimella b: Ala = ∫∫ dx dy = π · a · b." },
        { title: "Ramanujanin toinen kehäkaava", body: "Koska tarkka kehä vaatii elliptisen integraalin, Ramanujan johti tarkan suljetun approksimaation: P ≈ π(a + b)[1 + 3h / (10 + √(4 - 3h))], missä h = (a - b)² / (a + b)²." },
        { title: "Polttopisteet ja eksentrisyys", body: "Polttoväli c = √(a² - b²). Eksentrisyys e = c / a = √(1 - b²/a²). Kun e = 0, kyseessä on ympyrä; kun e ➔ 1, ellipsi litistyy kohti paraabelia." }
      ],
      ro: [
        { title: "Integrala ariei prin întindere afină", body: "O elipsă x²/a² + y²/b² = 1 este transformarea afină a cercului unitate întins cu a orizontal și b vertical: Arie = ∫∫ dx dy = π · a · b." },
        { title: "A doua formulă de perimetru a lui Ramanujan", body: "Deoarece perimetrul exact necesită o integrală eliptică, Srinivasa Ramanujan a formulat aproximarea închisă: P ≈ π(a + b)[1 + 3h / (10 + √(4 - 3h))], unde h = (a - b)² / (a + b)²." },
        { title: "Focare și excentricitate orbitală", body: "Distanța focală lineară c = √(a² - b²). Excentricitatea e = c / a = √(1 - b²/a²). Când e = 0 devine cerc; când e ➔ 1 se alungește spre o parabolă." }
      ]
    }
  },

  "geometry/trapezoid": {
    faqs: {
      de: [
        { q: "Was ist ein gleichschenkliges Trapez?", a: "Ein gleichschenkliges Trapez ist ein Trapez, bei dem die beiden nicht-parallelen Schenkel gleich lang sind (c = d), die Basiswinkel übereinstimmen und die Diagonalen identische Längen besitzen." },
        { q: "Was ist die Mittellinie eines Trapezes?", a: "Die Mittellinie verbindet die Mittelpunkte der beiden Schenkel. Ihre Länge entspricht dem arithmetischen Mittel der beiden parallelen Grundseiten: m = (a + b) / 2." }
      ],
      es: [
        { q: "¿Qué es un trapecio isósceles?", a: "Un trapecio isósceles es aquel cuyos lados no paralelos son congruentes (c = d), los ángulos adyacentes a cada base son iguales y las diagonales tienen idéntica longitud." },
        { q: "¿Qué es la mediana o base media de un trapecio?", a: "La base media conecta los puntos medios de los lados no paralelos. Su longitud es la media aritmética de las dos bases paralelas: m = (a + b) / 2." }
      ],
      fr: [
        { q: "Qu'est-ce qu'un trapèze isocèle ?", a: "Un trapèze isocèle est un trapèze dont les deux côtés non parallèles sont égaux (c = d), les angles à la base sont identiques et les diagonales ont la même longueur." },
        { q: "Qu'est-ce que la base moyenne d'un trapèze ?", a: "La base moyenne relie les milieux des côtés non parallèles. Sa longueur est la moyenne arithmétique des deux bases parallèles : m = (a + b) / 2." }
      ],
      it: [
        { q: "Cos'è un trapezio isoscele?", a: "Un trapezio isoscele è un trapezio in cui i due lati obliqui sono congruenti (c = d), gli angoli adiacenti alle basi sono uguali e le diagonali hanno la stessa lunghezza." },
        { q: "Cos'è la linea mediana di un trapezio?", a: "La linea mediana unisce i punti medi dei due lati obliqui. La sua lunghezza è la media aritmetica delle due basi parallele: m = (a + b) / 2." }
      ],
      pt: [
        { q: "O que é um trapézio isósceles?", a: "Um trapézio isósceles possui os dois lados oblíquos congruentes (c = d), ângulos da base iguais e diagonais de mesmo comprimento." },
        { q: "O que é a base média de um trapézio?", a: "A base média une os pontos médios dos lados oblíquos. Seu comprimento é a média aritmética das bases paralelas: m = (a + b) / 2." }
      ],
      nl: [
        { q: "Wat is een gelijkbenige trapezoïde?", a: "Een gelijkbenig trapezium heeft twee even lange schuine zijden (c = d), gelijke basishoeken en diagonalen van gelijke lengte." },
        { q: "Wat is de middenparallel van een trapezoïde?", a: "De middenparallel verbindt de middens van de niet-parallelle zijden. De lengte is het rekenkundig gemiddelde van de twee bases: m = (a + b) / 2." }
      ],
      pl: [
        { q: "Czym jest trapez równoramienny?", a: "Trapez równoramienny to trapez, w którym ramiona mają równą długość (c = d), kąty przy podstawie są równe, a przekątne mają jednakową długość." },
        { q: "Czym jest linia środkowa trapezu?", a: "Linia środkowa łączy środki ramion trapezu. Jej długość jest średnią arytmetyczną podstaw: m = (a + b) / 2 i jest do nich równoległa." }
      ],
      sv: [
        { q: "Vad är ett likbent trapets?", a: "Ett likbent trapets har två icke-parallella sidor med samma längd (c = d), lika basvinklar och diagonaler med samma längd." },
        { q: "Vad är medianen (mittlinjen) i ett trapets?", a: "Mittlinjen förenar mittpunkterna på de icke-parallella sidorna. Dess längd är det aritmetiska medelvärdet av baserna: m = (a + b) / 2." }
      ],
      no: [
        { q: "Hva er et likebeint trapes?", a: "Et likebeint trapes har to like lange ikke-parallelle sider (c = d), like grunnvinkler og diagonaler med lik lengde." },
        { q: "Hva er mellomlinjen i et trapes?", a: "Mellomlinjen forbinder midtpunktene på de to ikke-parallelle sidene. Lengden er det aritmetiske gjennomsnittet av basene: m = (a + b) / 2." }
      ],
      fi: [
        { q: "Mikä on tasakylkinen puolisuunnikas?", a: "Tasakylkinen puolisuunnikas on puolisuunnikas, jonka kaksi erisuuntaista kylkeä ovat yhtä pitkät (c = d), kantakulmat ovat yhtä suuret ja lävistäjät yhtä pitkät." },
        { q: "Mikä on puolisuunnikkaan keskijana?", a: "Keskijana yhdistää kylkien keskipisteet. Sen pituus on kantasivujen aritmeettinen keskiarvo: m = (a + b) / 2." }
      ],
      ro: [
        { q: "Ce este un trapez isoscel?", a: "Un trapez isoscel are laturile neparalele congruente (c = d), unghiurile alăturate bazelor egale și diagonalele de lungimi egale." },
        { q: "Ce este linia mijlocie a unui trapez?", a: "Linia mijlocie unește mijloacele laturilor neparalele. Lungimea sa este media aritmetică a celor două baze paralele: m = (a + b) / 2." }
      ]
    },
    proofs: {
      de: [
        { title: "Flächenbeweis durch Triangulierung", body: "Eine Diagonale teilt das Trapez in zwei Dreiecke mit identischer Höhe h: Fläche = ½ah + ½bh = ½h(a + b)." },
        { title: "Satz über die Mittellinie", body: "Die Verbindungsstrecke der Schenkelmitten ist parallel zu beiden Basen mit der Länge m = (a + b)/2. Folglich gilt: Fläche = m · h." },
        { title: "Umfangsberechnung", body: "Der Umfang ist die Summe aller vier begrenzenden Seitenkanten: P = a + b + c + d." }
      ],
      es: [
        { title: "Demostración de área por triangulación", body: "Una diagonal divide el trapecio en dos triángulos con la misma altura h: Área = ½ah + ½bh = ½h(a + b)." },
        { title: "Teorema de la base media", body: "El segmento que une los puntos medios de los lados es paralelo a las bases con longitud m = (a + b)/2, por lo que Área = m · h." },
        { title: "Perímetro perimetral", body: "El perímetro es la suma escalar de sus cuatro lados: P = a + b + c + d." }
      ],
      fr: [
        { title: "Démonstration d'aire par triangulation", body: "Une diagonale divise le trapèze en deux triangles de hauteur commune h : Aire = ½ah + ½bh = ½h(a + b)." },
        { title: "Théorème de la base moyenne", body: "Le segment joignant les milieux des côtés est parallèle aux bases avec m = (a + b)/2, d'où Aire = m · h." },
        { title: "Périmètre de contour", body: "Le périmètre est la somme des quatre côtés : P = a + b + c + d." }
      ],
      it: [
        { title: "Dimostrazione dell'area per triangolazione", body: "Una diagonale suddivide il trapezio in due triangoli di altezza comune h: Area = ½ah + ½bh = ½h(a + b)." },
        { title: "Teorema della mediana", body: "Il segmento congiungente i punti medi dei lati obliqui ha lunghezza m = (a + b)/2, quindi Area = m · h." },
        { title: "Perimetro", body: "Il perimetro è la somma dei quattro lati del trapezio: P = a + b + c + d." }
      ],
      pt: [
        { title: "Demonstração de área por triangulação", body: "Uma diagonal divide o trapézio em dois triângulos de altura comum h: Área = ½ah + ½bh = ½h(a + b)." },
        { title: "Teorema da base média", body: "O segmento que une os pontos médios dos lados oblíquos mede m = (a + b)/2, portanto Área = m · h." },
        { title: "Perímetro", body: "O perímetro é a soma dos quatro lados: P = a + b + c + d." }
      ],
      nl: [
        { title: "Oppervlaktebewijs door triangulatie", body: "Een diagonaal verdeelt het trapezium in twee driehoeken met gelijke hoogte h: Oppervlakte = ½ah + ½bh = ½h(a + b)." },
        { title: "Stelling van de middenparallel", body: "Het lijnstuk tussen de middens van de benen heeft lengte m = (a + b)/2, zodat Oppervlakte = m · h." },
        { title: "Omtrek", body: "De omtrek is de som van alle vier de zijden: P = a + b + c + d." }
      ],
      pl: [
        { title: "Dowód pola przez triangulację", body: "Przekątna dzieli trapez na dwa trójkąty o wspólnej wysokości h: Pole = ½ah + ½bh = ½h(a + b)." },
        { title: "Twierdzenie o linii środkowej", body: "Odcinek łączący środki ramion ma długość m = (a + b)/2, zatem Pole = m · h." },
        { title: "Obwód", body: "Obwód jest sumą wszystkich czterech boków: P = a + b + c + d." }
      ],
      sv: [
        { title: "Areabevis genom triangulering", body: "En diagonal delar trapetsen i två trianglar med samma höjd h: Area = ½ah + ½bh = ½h(a + b)." },
        { title: "Mittlinjesatsen", body: "Mittlinjen mellan benens mittpunkter har längden m = (a + b)/2, vilket ger Area = m · h." },
        { title: "Omkrets", body: "Omkretsen är summan av de fyra sidorna: P = a + b + c + d." }
      ],
      no: [
        { title: "Arealbevis ved triangulering", body: "En diagonal deler trapeset i to trekanter med samme høyde h: Areal = ½ah + ½bh = ½h(a + b)." },
        { title: "Mellomlinjesetningen", body: "Segmentet som forbinder midtpunktene på sidene har lengde m = (a + b)/2, slik at Areal = m · h." },
        { title: "Omkrets", body: "Omkretsen er summen av de fire sidene: P = a + b + c + d." }
      ],
      fi: [
        { title: "Pinta-alatodistus kolmioinnilla", body: "Lävistäjä jakaa puolisuunnikkaan kahdeksi kolmioksi, joiden korkeus on h: Ala = ½ah + ½bh = ½h(a + b)." },
        { title: "Keskijanalause", body: "Kylkien keskipisteet yhdistävän janan pituus on m = (a + b)/2, joten Ala = m · h." },
        { title: "Piiri", body: "Piiri on kaikkien neljän sivun summa: P = a + b + c + d." }
      ],
      ro: [
        { title: "Demonstrația ariei prin triangulație", body: "O diagonală împarte trapezul în două triunghiuri cu înălțimea comună h: Arie = ½ah + ½bh = ½h(a + b)." },
        { title: "Teorema liniei mijlocii", body: "Segmentul care unește mijloacele laturilor neparalele are lungimea m = (a + b)/2, deci Arie = m · h." },
        { title: "Perimetru", body: "Perimetrul este suma celor patru laturi: P = a + b + c + d." }
      ]
    }
  },

  "geometry/rhombus": {
    faqs: {
      de: [
        { q: "Was unterscheidet einen Rhombus von einem Quadrat?", a: "Ein Rhombus besitzt vier gleich lange Seiten, seine Innenwinkel müssen jedoch keine 90°-Winkel sein. Ein Quadrat ist ein spezieller Rhombus mit vier rechten Winkeln." },
        { q: "Können die Diagonalen eines Rhombus gleich lang sein?", a: "Ja, genau dann, wenn alle Innenwinkel 90° betragen; in diesem Fall ist der Rhombus per Definition ein Quadrat." }
      ],
      es: [
        { q: "¿En qué se diferencia un rombo de un cuadrado?", a: "Un rombo tiene cuatro lados congruentes, pero sus ángulos no son necesariamente de 90°. Un cuadrado es un rombo equiángulo con cuatro ángulos rectos." },
        { q: "¿Pueden las diagonales de un rombo tener la misma longitud?", a: "Sí, únicamente cuando todos sus ángulos interiores son de 90°, en cuyo caso el rombo es un cuadrado." }
      ],
      fr: [
        { q: "Quelle est la différence entre un losange et un carré ?", a: "Un losange a quatre côtés égaux, mais ses angles ne sont pas forcément droits. Un carré est un losange particulier possédant quatre angles droits." },
        { q: "Les diagonales d'un losange peuvent-elles être égales ?", a: "Oui, uniquement lorsque tous ses angles intérieurs valent 90°, auquel cas le losange est un carré." }
      ],
      it: [
        { q: "Qual è la differenza tra un rombo e un quadrato?", a: "Un rombo ha quattro lati congruenti, ma i suoi angoli non sono necessariamente retti. Un quadrato è un rombo speciale con angoli di 90°." },
        { q: "Le diagonali di un rombo possono essere congruenti?", a: "Sì, solo nel caso in cui tutti gli angoli interni misurino 90°, rendendo la figura un quadrato." }
      ],
      pt: [
        { q: "Qual a diferença entre um losango e um quadrado?", a: "Um losango tem quatro lados de mesmo comprimento, mas seus ângulos não são necessariamente retos. Um quadrado é um losango cujos quatro ângulos medem 90°." },
        { q: "As diagonais de um losango podem ser iguais?", a: "Sim, exatamente quando todos os ângulos internos medem 90°, caso em que o losango é um quadrado." }
      ],
      nl: [
        { q: "Wat is het verschil tussen een ruit en een vierkant?", a: "Een ruit heeft vier gelijke zijden, maar de hoeken hoeven geen 90° te zijn. Een vierkant is een ruit met vier rechte hoeken." },
        { q: "Kunnen de diagonalen van een ruit even lang zijn?", a: "Ja, alleen wanneer alle binnenhoeken 90° zijn; dan is de ruit tevens een vierkant." }
      ],
      pl: [
        { q: "Czym różni się romb od kwadratu?", a: "Romb ma cztery boki równej długości, ale jego kąty nie muszą wynosić 90°. Kwadrat jest szczególnym przypadkiem rombu o kątach prostych." },
        { q: "Czy przekątne rombu mogą mieć równą długość?", a: "Tak, wyłącznie wtedy, gdy wszystkie kąty wewnętrzne wynoszą 90°, co oznacza, że romb jest kwadratem." }
      ],
      sv: [
        { q: "Vad skiljer en romb från en kvadrat?", a: "En romb har fyra lika långa sidor, men vinklarna behöver inte vara räta. En kvadrat är en romb med fyra räta vinklar." },
        { q: "Kan diagonalerna i en romb vara lika långa?", a: "Ja, endast när alla innerhörn är 90°, vilket per definition gör romben till en kvadrat." }
      ],
      no: [
        { q: "Hva skiller en rombe fra et kvadrat?", a: "En rombe har fire like lange sider, men vinklene trenger ikke være rette. Et kvadrat er en rombe med fire 90°-vinkler." },
        { q: "Kan diagonalene i en rombe være like lange?", a: "Ja, bare dersom alle innvendige vinkler er 90°, slik at romben er et kvadrat." }
      ],
      fi: [
        { q: "Miten vinoneliö eroaa neliöstä?", a: "Vinoneliössä on neljä yhtä pitkää sivua, mutta sen kulmat eivät välttämättä ole 90°. Neliö on vinoneliön erikoistapaus, jossa kaikki kulmat ovat suoria." },
        { q: "Voivatko vinoneliön lävistäjät olla yhtä pitkät?", a: "Kyllä, vain silloin kun kaikki kulmat ovat 90°, jolloin kuvio on neliö." }
      ],
      ro: [
        { q: "Care este diferența dintre un romb și un pătrat?", a: "Un romb are toate cele patru laturi congruente, dar unghiurile nu sunt neapărat drepte. Un pătrat este un romb cu unghiuri de 90°." },
        { q: "Pot diagonalele unui romb să aibă lungimi egale?", a: "Da, doar atunci când toate unghiurile interioare sunt de 90°, caz în care rombul devine pătrat." }
      ]
    },
    proofs: {
      de: [
        { title: "Orthogonale Diagonalenteilung", body: "Die Diagonalen eines Rhombus halbieren sich gegenseitig unter einem rechten Winkel von 90°." },
        { title: "Pythagoreische Seitenberechnung", body: "Aus den vier rechtwinkligen Teildreiecken folgt nach Pythagoras: a² = (d₁/2)² + (d₂/2)² ⟹ a = ½√(d₁² + d₂²)." },
        { title: "Flächenbeweis aus Diagonalen", body: "Vier kongruente Dreiecke ergeben zusammen: Fläche = 4 × [½ · (d₁/2) · (d₂/2)] = ½ · d₁ · d₂." }
      ],
      es: [
        { title: "Bisección ortogonal de diagonales", body: "Las diagonales de un rombo se bisecan mutuamente formando un ángulo recto de 90°." },
        { title: "Derivación pitagórica del lado", body: "En cada triángulo rectángulo cuadrantal: a² = (d₁/2)² + (d₂/2)² ⟹ a = ½√(d₁² + d₂²)." },
        { title: "Área a partir de diagonales", body: "La suma de los cuatro triángulos rectángulos da: Área = 4 × [½ · (d₁/2) · (d₂/2)] = ½ · d₁ · d₂." }
      ],
      fr: [
        { title: "Bisection orthogonale des diagonales", body: "Les diagonales d'un losange se coupent en leur milieu perpendiculairement à 90°." },
        { title: "Dérivation pythagoricienne du côté", body: "Pour chaque triangle rectangle élémentaire : a² = (d₁/2)² + (d₂/2)² ⟹ a = ½√(d₁² + d₂²)." },
        { title: "Démonstration de l'aire par les diagonales", body: "La somme des quatre triangles rectangles donne : Aire = 4 × [½ · (d₁/2) · (d₂/2)] = ½ · d₁ · d₂." }
      ],
      it: [
        { title: "Bisezione ortogonale delle diagonali", body: "Le diagonali di un rombo si dimezzano reciprocamente formando un angolo retto di 90°." },
        { title: "Derivazione pitagorica del lato", body: "Applicando Pitagora a ciascun triangolo rettangolo: a² = (d₁/2)² + (d₂/2)² ⟹ a = ½√(d₁² + d₂²)." },
        { title: "Dimostrazione dell'area dalle diagonali", body: "Sommando i quattro triangoli rettangoli: Area = 4 × [½ · (d₁/2) · (d₂/2)] = ½ · d₁ · d₂." }
      ],
      pt: [
        { title: "Bissecção ortogonal das diagonais", body: "As diagonais de um losango cruzam-se nos seus pontos médios perpendicularmente a 90°." },
        { title: "Dedução pitagórica do lado", body: "Em cada triângulo retângulo resultante: a² = (d₁/2)² + (d₂/2)² ⟹ a = ½√(d₁² + d₂²)." },
        { title: "Área pelas diagonais", body: "A soma dos quatro triângulos retângulos resulta em: Área = 4 × [½ · (d₁/2) · (d₂/2)] = ½ · d₁ · d₂." }
      ],
      nl: [
        { title: "Loodrechte bissectie van diagonalen", body: "De diagonalen van een ruit delen elkaar middendoor onder een rechte hoek van 90°." },
        { title: "Pythagorese zijdeberekening", body: "In elk rechthoekig deel geldt: a² = (d₁/2)² + (d₂/2)² ⟹ a = ½√(d₁² + d₂²)." },
        { title: "Oppervlaktebewijs via diagonalen", body: "Vier rechthoekige driehoeken geven: Oppervlakte = 4 × [½ · (d₁/2) · (d₂/2)] = ½ · d₁ · d₂." }
      ],
      pl: [
        { title: "Prostopadłe przecinanie się przekątnych", body: "Przekątne rombu dzielą się na połowy pod kątem prostym 90°." },
        { title: "Pitagorejskie wyznaczenie boku", body: "W każdym z czterech trójkątów prostokątnych: a² = (d₁/2)² + (d₂/2)² ⟹ a = ½√(d₁² + d₂²)." },
        { title: "Pole z przekątnych", body: "Suma pól czterech trójkątów wynosi: Pole = 4 × [½ · (d₁/2) · (d₂/2)] = ½ · d₁ · d₂." }
      ],
      sv: [
        { title: "Ortogonal bisektion av diagonaler", body: "Diagonalerna i en romb skär varandra på mitten under en rät vinkel på 90°." },
        { title: "Pythagoreisk sidohärledning", body: "I varje deltriangel gäller: a² = (d₁/2)² + (d₂/2)² ⟹ a = ½√(d₁² + d₂²)." },
        { title: "Areabevis från diagonaler", body: "Fyra rätvinkliga trianglar ger: Area = 4 × [½ · (d₁/2) · (d₂/2)] = ½ · d₁ · d₂." }
      ],
      no: [
        { title: "Ortogonal halvering av diagonaler", body: "Diagonalene i en rombe halverer hverandre vinkelrett ved 90°." },
        { title: "Pytagoreisk sideberegning", body: "I hver av de fire rettvinklede trekantene: a² = (d₁/2)² + (d₂/2)² ⟹ a = ½√(d₁² + d₂²)." },
        { title: "Arealbevis fra diagonaler", body: "Fire rettvinklede trekanter gir: Areal = 4 × [½ · (d₁/2) · (d₂/2)] = ½ · d₁ · d₂." }
      ],
      fi: [
        { title: "Lävistäjien kohtisuora puolitus", body: "Vinoneliön lävistäjät puolittavat toisensa kohtisuorassa 90° kulmassa." },
        { title: "Pythagoraan sivukaava", body: "Kussakin neljässä suorakulmaisessa osakolmiossa: a² = (d₁/2)² + (d₂/2)² ⟹ a = ½√(d₁² + d₂²)." },
        { title: "Pinta-alatodistus lävistäjistä", body: "Neljän suorakulmaisen kolmion summa on: Ala = 4 × [½ · (d₁/2) · (d₂/2)] = ½ · d₁ · d₂." }
      ],
      ro: [
        { title: "Înjumătățirea ortogonală a diagonalelor", body: "Diagonalele unui romb se înjumătățesc reciproc sub un unghi drept de 90°." },
        { title: "Deducerea pitagoreică a laturii", body: "În fiecare din cele patru triunghiuri dreptunghice: a² = (d₁/2)² + (d₂/2)² ⟹ a = ½√(d₁² + d₂²)." },
        { title: "Demonstrația ariei din diagonale", body: "Suma celor patru triunghiuri dreptunghice dă: Arie = 4 × [½ · (d₁/2) · (d₂/2)] = ½ · d₁ · d₂." }
      ]
    }
  },

  "geometry/parallelogram": {
    faqs: {
      de: [
        { q: "Was unterscheidet ein Rechteck von einem allgemeinen Parallelogramm?", a: "Ein Rechteck ist ein Parallelogramm, bei dem alle vier Innenwinkel exakt 90° betragen und beide Diagonalen gleich lang sind." },
        { q: "Was besagt die Parallelogramm-Identität?", a: "Die Summe der quadrierten Diagonalen entspricht genau der Summe der quadrierten vier Seiten: p² + q² = 2(a² + b²)." }
      ],
      es: [
        { q: "¿En qué se diferencia un rectángulo de un paralelogramo general?", a: "Un rectángulo es un paralelogramo con cuatro ángulos rectos de 90° y diagonales de idéntica longitud." },
        { q: "¿Qué establece la ley del paralelogramo?", a: "Establece que la suma de los cuadrados de las dos diagonales es igual a la suma de los cuadrados de los cuatro lados: p² + q² = 2(a² + b²)." }
      ],
      fr: [
        { q: "Quelle est la différence entre un rectangle et un parallélogramme général ?", a: "Un rectangle est un parallélogramme dont les quatre angles valent 90° et dont les diagonales sont de même longueur." },
        { q: "Qu'énonce l'identité du parallélogramme ?", a: "La somme des carrés des diagonales est égale à la somme des carrés des quatre côtés : p² + q² = 2(a² + b²)." }
      ],
      it: [
        { q: "Qual è la differenza tra un rettangolo e un parallelogramma generale?", a: "Un rettangolo è un parallelogramma speciale in cui tutti e quattro gli angoli interni misurano 90° e le diagonali sono uguali." },
        { q: "Cosa afferma la legge del parallelogramma?", a: "Afferma che la somma dei quadrati delle due diagonali è uguale alla somma dei quadrati dei quattro lati: p² + q² = 2(a² + b²)." }
      ],
      pt: [
        { q: "Qual a diferença entre um retângulo e um paralelogramo geral?", a: "Um retângulo é um paralelogramo equiângulo com quatro ângulos de 90° e diagonais de mesmo comprimento." },
        { q: "O que enuncia a lei do paralelogramo?", a: "A soma dos quadrados das duas diagonais é igual à soma dos quadrados dos quatro lados: p² + q² = 2(a² + b²)." }
      ],
      nl: [
        { q: "Wat is het verschil tussen een rechthoek en een algemeen parallellogram?", a: "Een rechthoek is een parallellogram met vier rechte hoeken van 90° en gelijke diagonalen." },
        { q: "Wat houdt de parallellogramwet in?", a: "De som van de kwadraten van de twee diagonalen is gelijk aan de som van de kwadraten van de vier zijden: p² + q² = 2(a² + b²)." }
      ],
      pl: [
        { q: "Czym różni się prostokąt od ogólnego równoległoboku?", a: "Prostokąt to równoległobok, którego wszystkie cztery kąty mają 90°, a przekątne są równej długości." },
        { q: "Co mówi tożsamość równoległoboku?", a: "Suma kwadratów długości przekątnych równa się sumie kwadratów długości wszystkich czterech boków: p² + q² = 2(a² + b²)." }
      ],
      sv: [
        { q: "Vad skiljer en rektangel från ett allmänt parallellogram?", a: "En rektangel är ett parallellogram där alla fyra vinklar är 90° och diagonalerna har samma längd." },
        { q: "Vad innebär parallellogramlagen?", a: "Summan av kvadraterna på de två diagonalerna är lika med summan av kvadraterna på de fyra sidorna: p² + q² = 2(a² + b²)." }
      ],
      no: [
        { q: "Hva skiller et rektangel fra et generelt parallellogram?", a: "Et rektangel er et parallellogram der alle fire vinkler er 90° og diagonalene har samme lengde." },
        { q: "Hva sier parallellogramloven?", a: "Summen av kvadratene av de to diagonalene er lik summen av kvadratene av de fire sidene: p² + q² = 2(a² + b²)." }
      ],
      fi: [
        { q: "Miten suorakulmio eroaa yleisestä suunnikkaasta?", a: "Suorakulmio on suunnikas, jonka kaikki neljä kulmaa ovat 90° ja jonka lävistäjät ovat yhtä pitkät." },
        { q: "Mitä suunnikassääntö tarkoittaa?", a: "Lävistäjien neliöiden summa on yhtä suuri kuin kaikkien neljän sivun neliöiden summa: p² + q² = 2(a² + b²)." }
      ],
      ro: [
        { q: "Care este diferența dintre un dreptunghi și un paralelogram oarecare?", a: "Un dreptunghi este un paralelogram cu toate unghiurile de 90° și diagonale congruente." },
        { q: "Ce reprezintă legea paralelogramului?", a: "Suma pătratelor celor două diagonale este egală cu suma pătratelor celor patru laturi: p² + q² = 2(a² + b²)." }
      ]
    },
    proofs: {
      de: [
        { title: "Trigonometrische Höhe und Fläche", body: "Höhe h = b · sin(θ). Daher gilt: Fläche = a · h = a · b · sin(θ)." },
        { title: "Kosinussatz für die Diagonalen", body: "Für die Diagonalen p und q gilt: p = √[a² + b² + 2ab cos(θ)] und q = √[a² + b² - 2ab cos(θ)]." },
        { title: "Parallelogramm-Identität (Apollonios)", body: "Fundamentale Vektorinvariante: p² + q² = 2(a² + b²). Die Summe der Diagonalquadrate entspricht den vier Seitenquadraten." }
      ],
      es: [
        { title: "Altura trigonométrica y área", body: "Altura h = b · sin(θ). Por tanto: Área = a · h = a · b · sin(θ)." },
        { title: "Ley de cosenos para diagonales", body: "Para las diagonales p y q: p = √[a² + b² + 2ab cos(θ)] y q = √[a² + b² - 2ab cos(θ)]." },
        { title: "Ley del paralelogramo (Identidad de Apolonio)", body: "Invariante vectorial fundamental: p² + q² = 2(a² + b²)." }
      ],
      fr: [
        { title: "Hauteur trigonométrique et aire", body: "Hauteur h = b · sin(θ). Donc : Aire = a · h = a · b · sin(θ)." },
        { title: "Loi des cosinus pour les diagonales", body: "Pour les diagonales p et q : p = √[a² + b² + 2ab cos(θ)] et q = √[a² + b² - 2ab cos(θ)]." },
        { title: "Identité du parallélogramme (Apollonius)", body: "Invariant vectoriel fondamental : p² + q² = 2(a² + b²)." }
      ],
      it: [
        { title: "Altezza trigonometrica e area", body: "Altezza h = b · sin(θ). Quindi: Area = a · h = a · b · sin(θ)." },
        { title: "Teorema del coseno per le diagonali", body: "Per le diagonali p e q: p = √[a² + b² + 2ab cos(θ)] e q = √[a² + b² - 2ab cos(θ)]." },
        { title: "Legge del parallelogramma (Identità di Apollonio)", body: "Invariante vettoriale fondamentale: p² + q² = 2(a² + b²)." }
      ],
      pt: [
        { title: "Altura trigonométrica e área", body: "Altura h = b · sin(θ). Logo: Área = a · h = a · b · sin(θ)." },
        { title: "Lei dos cossenos para as diagonais", body: "Para as diagonais p e q: p = √[a² + b² + 2ab cos(θ)] e q = √[a² + b² - 2ab cos(θ)]." },
        { title: "Lei do paralelogramo (Identidade de Apolônio)", body: "Invariante vetorial: p² + q² = 2(a² + b²)." }
      ],
      nl: [
        { title: "Goniometrische hoogte en oppervlakte", body: "Hoogte h = b · sin(θ). Daarom: Oppervlakte = a · h = a · b · sin(θ)." },
        { title: "Cosinusregel voor diagonalen", body: "Voor diagonalen p en q: p = √[a² + b² + 2ab cos(θ)] en q = √[a² + b² - 2ab cos(θ)]." },
        { title: "Parallellogramwet (Apollonius-identiteit)", body: "Fundamentele vectorinvariante: p² + q² = 2(a² + b²)." }
      ],
      pl: [
        { title: "Wysokość trygonometryczna i pole", body: "Wysokość h = b · sin(θ). Zatem: Pole = a · h = a · b · sin(θ)." },
        { title: "Twierdzenie cosinusów dla przekątnych", body: "Dla przekątnych p i q: p = √[a² + b² + 2ab cos(θ)] oraz q = √[a² + b² - 2ab cos(θ)]." },
        { title: "Tożsamość równoległoboku (Apoloniusza)", body: "Podstawowy niezmiennik wektorowy: p² + q² = 2(a² + b²)." }
      ],
      sv: [
        { title: "Trigonometrisk höjd och area", body: "Höjd h = b · sin(θ). Alltså: Area = a · h = a · b · sin(θ)." },
        { title: "Cosinussatsen för diagonaler", body: "För diagonalerna p och q: p = √[a² + b² + 2ab cos(θ)] och q = √[a² + b² - 2ab cos(θ)]." },
        { title: "Parallellogramlagen (Apollonios identitet)", body: "Vektorinvariant: p² + q² = 2(a² + b²)." }
      ],
      no: [
        { title: "Trigonometrisk høyde og areal", body: "Høyde h = b · sin(θ). Derfor: Areal = a · h = a · b · sin(θ)." },
        { title: "Cosinussetningen for diagonaler", body: "For diagonalene p og q: p = √[a² + b² + 2ab cos(θ)] og q = √[a² + b² - 2ab cos(θ)]." },
        { title: "Parallellogramloven (Apollonios identitet)", body: "Vektorinvariant: p² + q² = 2(a² + b²)." }
      ],
      fi: [
        { title: "Trigonometrinen korkeus ja pinta-ala", body: "Korkeus h = b · sin(θ). Siten: Ala = a · h = a · b · sin(θ)." },
        { title: "Kosinilause lävistäjille", body: "Lävistäjille p ja q: p = √[a² + b² + 2ab cos(θ)] ja q = √[a² + b² - 2ab cos(θ)]." },
        { title: "Suunnikassääntö (Apolloniuksen identiteetti)", body: "Vektori-invariantti: p² + q² = 2(a² + b²)." }
      ],
      ro: [
        { title: "Înălțimea trigonometrică și aria", body: "Înălțimea h = b · sin(θ). Astfel: Arie = a · h = a · b · sin(θ)." },
        { title: "Teorema cosinusului pentru diagonale", body: "Pentru diagonalele p și q: p = √[a² + b² + 2ab cos(θ)] și q = √[a² + b² - 2ab cos(θ)]." },
        { title: "Legea paralelogramului (Identitatea lui Apollonius)", body: "Invariant vectorial fundamental: p² + q² = 2(a² + b²)." }
      ]
    }
  },

  "geometry/kite": {
    faqs: {
      de: [
        { q: "Was ist ein rechtwinkliger Drachen?", a: "Ein rechtwinkliger Drachen besitzt zwei gegenüberliegende rechte Winkel von 90° an den Seiten und ist immer ein Sehnenviereck." },
        { q: "Besitzt jeder Drachen einen Inkreis?", a: "Ja, jeder konvexe Drachen ist ein Tangentenviereck und besitzt einen eindeutigen Inkreis, dessen Mittelpunkt auf der Symmetrieachse liegt." }
      ],
      es: [
        { q: "¿Qué es un deltoide o cometa rectángulo?", a: "Es aquel que tiene dos ángulos rectos de 90° opuestos entre sí, siendo por tanto inscribible en una circunferencia." },
        { q: "¿Tiene todo deltoide una circunferencia inscrita?", a: "Sí, todo deltoide convexo es un cuadrilátero tangencial y admite una circunferencia inscrita cuyo centro se sitúa sobre el eje de simetría." }
      ],
      fr: [
        { q: "Qu'est-ce qu'un cerf-volant rectangle ?", a: "C'est un cerf-volant possédant deux angles droits de 90° opposés, ce qui en fait un quadrilatère inscriptible." },
        { q: "Tout cerf-volant admet-il un cercle inscrit ?", a: "Oui, tout cerf-volant convexe est un quadrilatère circonscriptible admettant un cercle inscrit dont le centre est sur l'axe de symétrie." }
      ],
      it: [
        { q: "Cos'è un deltoide retto?", a: "Un deltoide retto ha due angoli opposti di 90° ed è sempre inscrivibile in una circonferenza." },
        { q: "Ogni deltoide ammette una circonferenza inscritta?", a: "Sì, ogni deltoide convesso è circoscrivibile a una circonferenza il cui centro giace sull'asse di simmetria." }
      ],
      pt: [
        { q: "O que é um deltóide retângulo?", a: "É um deltóide que possui dois ângulos opostos de 90°, sendo portanto inscritível em uma circunferência." },
        { q: "Todo deltóide possui um círculo inscrito?", a: "Sim, todo deltóide convexo é tangencial e possui um círculo inscrito com centro no eixo de simetria." }
      ],
      nl: [
        { q: "Wat is een rechthoekige vlieger?", a: "Een rechthoekige vlieger heeft twee tegenover elkaar liggende rechte hoeken van 90° en is altijd een koordenvierhoek." },
        { q: "Heeft elke vlieger een ingeschreven cirkel?", a: "Ja, elke convexe vlieger is een raaklijnenvierhoek en bezit een ingeschreven cirkel met middelpunt op de symmetrieas." }
      ],
      pl: [
        { q: "Czym jest deltoid prostokątny?", a: "Deltoid prostokątny ma dwa przeciwległe kąty proste 90° i można na nim opisać okrąg." },
        { q: "Czy w każdy deltoid można wpisać okrąg?", a: "Tak, w każdy wypukły deltoid można wpisać okrąg, którego środek leży na osi symetrii." }
      ],
      sv: [
        { q: "Vad är en rätvinklig drake?", a: "En rätvinklig drake har två motstående räta vinklar på 90° och kan alltid inskrivas i en cirkel." },
        { q: "Har alla drakar en inskriven cirkel?", a: "Ja, varje konvex drake är en tangentfyrhörning och har en inskriven cirkel med medelpunkt på symmetriaxeln." }
      ],
      no: [
        { q: "Hva er en rettvinklet drake?", a: "En rettvinklet drake har to motstående rette vinkler på 90° og kan alltid innskrives i en sirkel." },
        { q: "Har enhver drake en innskrevet sirkel?", a: "Ja, enhver konveks drake er en tangentfirkant og har en innskrevet sirkel med sentrum på symmetriaksen." }
      ],
      fi: [
        { q: "Mikä on suorakulmainen leija?", a: "Suorakulmaisessa leijassa on kaksi vastakkaista 90° kulmaa, ja sen ympäri voidaan aina piirtää ympyrä." },
        { q: "Onko jokaisella leijalla sisään piirretty ympyrä?", a: "Kyllä, jokainen kupera leija on tangenttinelikulmio, johon voidaan piirtää ympyrä." }
      ],
      ro: [
        { q: "Ce este un deltoid dreptunghic?", a: "Un deltoid dreptunghic are două unghiuri opuse de 90° și este întotdeauna inscriptibil într-un cerc." },
        { q: "Are orice deltoid un cerc înscris?", a: "Da, orice deltoid convex este un patrulater tangențial și admite un cerc înscris cu centrul pe axa de simetrie." }
      ]
    },
    proofs: {
      de: [
        { title: "Flächensatz für orthodiagonale Vierecke", body: "Da die Diagonalen rechtwinklig aufeinander stehen (90°): Fläche = ½ · d₁ · d₂." },
        { title: "Pythagoreische Seitenberechnung", body: "Die Symmetriediagonale teilt die Querdiagonale mittig: a = √[h₁² + (d₂/2)²] und b = √[h₂² + (d₂/2)²]." },
        { title: "Umfangssumme", body: "Der Umfang ist die Summe der paarweise gleichen Seiten: P = 2(a + b)." }
      ],
      es: [
        { title: "Teorema de área para cuadriláteros ortodiagonales", body: "Dado que las diagonales son perpendiculares (90°): Área = ½ · d₁ · d₂." },
        { title: "Formulación pitagórica de pares de lados", body: "La diagonal de simetría biseca a la otra: a = √[h₁² + (d₂/2)²] y b = √[h₂² + (d₂/2)²]." },
        { title: "Suma perimetral", body: "El perímetro es la suma de sus lados congruentes por pares: P = 2(a + b)." }
      ],
      fr: [
        { title: "Théorème d'aire des quadrilatères orthodiagonaux", body: "Les diagonales étant perpendiculaires (90°) : Aire = ½ · d₁ · d₂." },
        { title: "Formulation pythagoricienne des côtés", body: "L'axe de symétrie coupe la seconde diagonale en son milieu : a = √[h₁² + (d₂/2)²] et b = √[h₂² + (d₂/2)²]." },
        { title: "Périmètre", body: "Le périmètre est la somme des côtés égaux deux à deux : P = 2(a + b)." }
      ],
      it: [
        { title: "Teorema dell'area per quadrilateri ortodiagonali", body: "Poiché le diagonali si intersecano ad angolo retto (90°): Area = ½ · d₁ · d₂." },
        { title: "Formulazione pitagorica dei lati", body: "L'asse di simmetria dimezza la seconda diagonale: a = √[h₁² + (d₂/2)²] e b = √[h₂² + (d₂/2)²]." },
        { title: "Perimetro", body: "Il perimetro è dato dalla somma delle due coppie di lati uguali: P = 2(a + b)." }
      ],
      pt: [
        { title: "Teorema de área para quadriláteros ortodiagonais", body: "Como as diagonais são perpendiculares (90°): Área = ½ · d₁ · d₂." },
        { title: "Dedução pitagórica dos lados", body: "O eixo de simetria divide a diagonal transversal ao meio: a = √[h₁² + (d₂/2)²] e b = √[h₂² + (d₂/2)²]." },
        { title: "Perímetro", body: "O perímetro é dado por P = 2(a + b)." }
      ],
      nl: [
        { title: "Oppervlaktestelling voor orthodiagonale vierhoeken", body: "Omdat de diagonalen loodrecht op elkaar staan (90°): Oppervlakte = ½ · d₁ · d₂." },
        { title: "Pythagorese zijdeberekening", body: "De symmetrie-as deelt de dwarsdiagonaal middendoor: a = √[h₁² + (d₂/2)²] en b = √[h₂² + (d₂/2)²]." },
        { title: "Omtrek", body: "De omtrek is de som van de twee paren zijden: P = 2(a + b)." }
      ],
      pl: [
        { title: "Twierdzenie o polu czworokąta ortodiagonalnego", body: "Ponieważ przekątne przecinają się pod kątem prostym (90°): Pole = ½ · d₁ · d₂." },
        { title: "Pitagorejskie wyznaczenie boków", body: "Główna przekątna dzieli drugą na połowy: a = √[h₁² + (d₂/2)²] i b = √[h₂² + (d₂/2)²]." },
        { title: "Obwód", body: "Obwód wynosi P = 2(a + b)." }
      ],
      sv: [
        { title: "Areasats för ortodiagonala fyrhörningar", body: "Eftersom diagonalerna skär varandra vinkelrätt (90°): Area = ½ · d₁ · d₂." },
        { title: "Pythagoreisk sidoberäkning", body: "Symmetriaxeln delar tvärdiagonalen i två delar: a = √[h₁² + (d₂/2)²] och b = √[h₂² + (d₂/2)²]." },
        { title: "Omkrets", body: "Omkretsen är P = 2(a + b)." }
      ],
      no: [
        { title: "Arealteorem for ortodiagonale firkanter", body: "Siden diagonalene skjærer hverandre vinkelrett (90°): Areal = ½ · d₁ · d₂." },
        { title: "Pytagoreisk sideberegning", body: "Symmetriaksen deler tverrdiagonalen på midten: a = √[h₁² + (d₂/2)²] og b = √[h₂² + (d₂/2)²]." },
        { title: "Omkrets", body: "Omkretsen er P = 2(a + b)." }
      ],
      fi: [
        { title: "Ortodiagonaalisen nelikulmion pinta-alateoreema", body: "Koska lävistäjät ovat toisiaan vastaan kohtisuorassa (90°): Ala = ½ · d₁ · d₂." },
        { title: "Pythagoraan sivukaava", body: "Symmetrialävistäjä puolittaa toisen lävistäjän: a = √[h₁² + (d₂/2)²] ja b = √[h₂² + (d₂/2)²]." },
        { title: "Piiri", body: "Piiri on P = 2(a + b)." }
      ],
      ro: [
        { title: "Teorema ariei pentru patrulatere ortodiagonale", body: "Deoarece diagonalele sunt perpendiculare (90°): Arie = ½ · d₁ · d₂." },
        { title: "Deducerea pitagoreică a laturilor", body: "Axa de simetrie împarte a doua diagonală în jumătate: a = √[h₁² + (d₂/2)²] și b = √[h₂² + (d₂/2)²]." },
        { title: "Perimetru", body: "Perimetrul este P = 2(a + b)." }
      ]
    }
  },

  "geometry/arc-length": {
    faqs: {
      de: [
        { q: "Was ist der Unterschied zwischen einem Kreissektor und einem Kreissegment?", a: "Ein Kreissektor ist ein kuchenstückförmiger Bereich, der von zwei Radien und einem Bogen begrenzt wird. Ein Kreissegment ist der Bereich zwischen einer Kreissehne und dem Bogen." },
        { q: "Warum werden Winkel in der Analysis im Bogenmaß gemessen?", a: "Im Bogenmaß gelten einfache Ableitungsregeln wie d/dx(sin x) = cos x ohne störende Umrechnungsfaktoren wie π/180." }
      ],
      es: [
        { q: "¿Cuál es la diferencia entre un sector circular y un segmento circular?", a: "Un sector circular es una porción en forma de porción de tarta delimitada por dos radios y un arco. Un segmento circular es el área comprendida entre una cuerda y el arco." },
        { q: "¿Por qué se miden los ángulos en radianes en cálculo?", a: "En cálculo, los radianes mantienen derivadas puras sin factores de conversión: d/dx(sin x) = cos x." }
      ],
      fr: [
        { q: "Quelle est la différence entre un secteur circulaire et un segment circulaire ?", a: "Un secteur circulaire est délimité par deux rayons et un arc. Un segment circulaire est la zone comprise entre une corde et son arc." },
        { q: "Pourquoi mesure-t-on les angles en radians en analyse ?", a: "Les radians préservent des dérivées simples sans facteurs résiduels : d/dx(sin x) = cos x." }
      ],
      it: [
        { q: "Qual è la differenza tra un settore circolare e un segmento circolare?", a: "Un settore circolare è delimitato da due raggi e un arco. Un segmento circolare è l'area compresa tra una corda e l'arco corrispondente." },
        { q: "Perché in analisi matematica gli angoli si misurano in radianti?", a: "I radianti garantiscono derivate pure prive di costanti di conversione: d/dx(sin x) = cos x." }
      ],
      pt: [
        { q: "Qual a diferença entre um setor circular e um segmento circular?", a: "Um setor circular é delimitado por dois raios e um arco. Um segmento circular é a região delimitada por uma corda e o arco." },
        { q: "Por que os ângulos são medidos em radianos no cálculo?", a: "Os radianos preservam derivadas imediatas sem fatores de conversão: d/dx(sin x) = cos x." }
      ],
      nl: [
        { q: "Wat is het verschil tussen een cirkelsector en een cirkelsegment?", a: "Een cirkelsector wordt begrensd door twee stralen en een boog. Een cirkelsegment is het gebied tussen een koorde en de boog." },
        { q: "Waarom worden hoeken in calculus in radialen gemeten?", a: "Radialen zorgen voor eenvoudige afgeleiden zonder omrekenfactoren: d/dx(sin x) = cos x." }
      ],
      pl: [
        { q: "Jaka jest różnica między wycinkiem a odcinkiem koła?", a: "Wycinek koła jest ograniczony dwoma promieniami i łukiem. Odcinek koła to obszar między cięciwą a łukiem okręgu." },
        { q: "Dlaczego w analizie matematycznej kąty mierzy się w radianach?", a: "Radiany upraszczają pochodne funkcji trygonometrycznych: d/dx(sin x) = cos x bez zbędnych współczynników." }
      ],
      sv: [
        { q: "Vad är skillnaden mellan en cirkelsektor och ett cirkelsegment?", a: "En cirkelsektor avgränsas av två radier och en cirkelbåge. Ett cirkelsegment är området mellan en korda och bågen." },
        { q: "Varför mäts vinklar i radianer i integralkalkyl?", a: "Radianer ger rena derivator utan omvandlingskonstanter: d/dx(sin x) = cos x." }
      ],
      no: [
        { q: "Hva er forskjellen mellom en sirkelsektor og et sirkelsegment?", a: "En sirkelsektor er avgrenset av to radier og en sirkelbue. Et sirkelsegment er arealet mellom en korde og buen." },
        { q: "Hvorfor måles vinkler i radianer i matematisk analyse?", a: "Radianer bevarer enkle deriverte uten omregningsfaktorer: d/dx(sin x) = cos x." }
      ],
      fi: [
        { q: "Mitä eroa on ympyräsektorilla ja ympyräsegmentillä?", a: "Ympyräsektori rajautuu kahteen säteeseen ja kaareen. Ympyräsegmentti on jänteen ja kaaren välinen alue." },
        { q: "Miksi kulmat mitataan differentiaalilaskennassa radiaaneina?", a: "Radiaanit säilyttävät puhtaat derivaatat ilman muuntokertoimia: d/dx(sin x) = cos x." }
      ],
      ro: [
        { q: "Care este diferența dintre un sector de cerc și un segment de cerc?", a: "Un sector de cerc este delimitat de două raze și un arc. Un segment de cerc este suprafața dintre o coardă și arcul corespunzător." },
        { q: "De ce unghiurile se măsoară în radiani în analiza matematică?", a: "Radianii asigură derivate simple fără constante de conversie: d/dx(sin x) = cos x." }
      ]
    },
    proofs: {
      de: [
        { title: "Radian-Definition und Bogenlänge", body: "Ein Radiant ist der Zentriwinkel, dessen Bogenlänge genau dem Radius r entspricht: s = r · θ." },
        { title: "Herleitung der Sektorfläche", body: "Die Fläche ist proportional zum Anteil am Vollkreis: Fläche_Sektor = (θ / 2π) · πr² = ½ · r² · θ." },
        { title: "Sehnenlänge und Segmentfläche", body: "Halbierung des gleichschenkligen Dreiecks ergibt: Sehne c = 2r sin(θ/2) und Segmentfläche = ½r²(θ - sin θ)." }
      ],
      es: [
        { title: "Definición de radián y longitud de arco", body: "Un radián es el ángulo central que subtiende un arco de longitud igual al radio r: s = r · θ." },
        { title: "Derivación del área del sector", body: "El área es proporcional a la fracción del círculo: Área_sector = (θ / 2π) · πr² = ½ · r² · θ." },
        { title: "Longitud de cuerda y área del segmento", body: "Bisecando el triángulo isósceles se obtiene: c = 2r sin(θ/2) y Área_segmento = ½r²(θ - sin θ)." }
      ],
      fr: [
        { title: "Définition du radian et longueur d'arc", body: "Un radian est l'angle au centre interceptant un arc de longueur r : s = r · θ." },
        { title: "Dérivation de l'aire du secteur", body: "L'aire est proportionnelle à la fraction du disque : Aire_secteur = (θ / 2π) · πr² = ½ · r² · θ." },
        { title: "Longueur de corde et aire du segment", body: "La bissectrice du triangle isocèle donne : corde c = 2r sin(θ/2) et Aire_segment = ½r²(θ - sin θ)." }
      ],
      it: [
        { title: "Definizione di radiante e lunghezza d'arco", body: "Un radiante è l'angolo al centro che sottende un arco pari al raggio r: s = r · θ." },
        { title: "Derivazione dell'area del settore", body: "L'area è proporzionale alla frazione del cerchio: Area_settore = (θ / 2π) · πr² = ½ · r² · θ." },
        { title: "Lunghezza della corda e area del segmento", body: "Dalla bisezione del triangolo isoscele: corda c = 2r sin(θ/2) e Area_segmento = ½r²(θ - sin θ)." }
      ],
      pt: [
        { title: "Definição de radiano e comprimento de arco", body: "Um radiano é o ângulo central que subtende um arco de comprimento igual ao raio r: s = r · θ." },
        { title: "Área do setor circular", body: "A área é proporcional à fração do círculo completo: Área_setor = (θ / 2π) · πr² = ½ · r² · θ." },
        { title: "Comprimento da corda e área do segmento", body: "Pela bissecção do triângulo isósceles: corda c = 2r sin(θ/2) e Área_segmento = ½r²(θ - sin θ)." }
      ],
      nl: [
        { title: "Definitie van radiaal en booglengte", body: "Een radiaal is de middelpuntshoek waarvan de booglengte gelijk is aan de straal r: s = r · θ." },
        { title: "Afleiding sectoroppervlakte", body: "De oppervlakte is evenredig met het deel van de cirkel: Oppervlakte_sector = (θ / 2π) · πr² = ½ · r² · θ." },
        { title: "Koordelengte en segmentoppervlakte", body: "Het halveren van de gelijkbenige driehoek geeft: koorde c = 2r sin(θ/2) en Oppervlakte_segment = ½r²(θ - sin θ)." }
      ],
      pl: [
        { title: "Definicja radiana i długość łuku", body: "Jeden radian to kąt środkowy oparty na łuku o długości równej promieniowi r: s = r · θ." },
        { title: "Wyprowadzenie pola wycinka koła", body: "Pole jest proporcjonalne do kąta pełnego: Pole_wycinka = (θ / 2π) · πr² = ½ · r² · θ." },
        { title: "Długość cięciwy i pole odcinka", body: "Podział trójkąta równoramiennego daje: cięciwa c = 2r sin(θ/2) oraz Pole_odcinka = ½r²(θ - sin θ)." }
      ],
      sv: [
        { title: "Radiandefinition och båglängd", body: "En radian är medelpunktsvinkeln som spänner över en båge med längden r: s = r · θ." },
        { title: "Härledning av sektorns area", body: "Arean är proportionell mot andelen av cirkeln: Area_sektor = (θ / 2π) · πr² = ½ · r² · θ." },
        { title: "Kordalängd och segmentarea", body: "Halvering av den likbenta triangeln ger: korda c = 2r sin(θ/2) och Area_segment = ½r²(θ - sin θ)." }
      ],
      no: [
        { title: "Radiandefinisjon og buelengde", body: "En radian er sentralvinkelen som spenner over en bue med lengde lik radien r: s = r · θ." },
        { title: "Utledning av sektorareal", body: "Arealet er proporsjonalt med brøkdelen av sirkelen: Areal_sektor = (θ / 2π) · πr² = ½ · r² · θ." },
        { title: "Kordelengde og segmentareal", body: "Halvering av den likebeinte trekanten gir: korde c = 2r sin(θ/2) og Areal_segment = ½r²(θ - sin θ)." }
      ],
      fi: [
        { title: "Radiaanin määritelmä ja kaarenpituus", body: "Yksi radiaani on keskuskulma, jota vastaavan kaaren pituus on säde r: s = r · θ." },
        { title: "Ympyräsektorin pinta-alan johto", body: "Pinta-ala on suhteessa koko ympyrän osuuteen: Ala_sektori = (θ / 2π) · πr² = ½ · r² · θ." },
        { title: "Jänteen pituus ja segmentin ala", body: "Tasakylkisen kolmion puolittaminen antaa: jänne c = 2r sin(θ/2) ja Ala_segmentti = ½r²(θ - sin θ)." }
      ],
      ro: [
        { title: "Definiția radianului și lungimea arcului", body: "Un radian este unghiul la centru ce subîntinde un arc egal cu raza r: s = r · θ." },
        { title: "Deducerea ariei sectorului", body: "Aria este proporțională cu fracțiunea din cerc: Arie_sector = (θ / 2π) · πr² = ½ · r² · θ." },
        { title: "Lungimea corzii și aria segmentului", body: "Bisectarea triunghiului isoscel dă: coarda c = 2r sin(θ/2) și Arie_segment = ½r²(θ - sin θ)." }
      ]
    }
  }
};

