/**
 * scripts/translations/geometry_3d.js
 * 3D Geometry Solvers Localizations (FAQs & Proofs) across 11 languages.
 * Solvers: cone, cylinder, ellipsoid, torus, pyramid, triangular-prism, frustum-cone, frustum-pyramid, concrete-volume
 */

export const GEOMETRY_3D = {
  "geometry/cone": {
    faqs: {
      de: [
        { q: "Warum beträgt das Volumen eines Kegels genau ein Drittel eines Zylinders?", a: "Wie bereits von Eudoxos und Archimedes bewiesen, führt die lineare Verjüngung eines rotierenden Dreiecks über ein Integral auf: V = π ∫₀ʰ (r/h)² x² dx = ⅓ · π · r² · h, exakt ein Drittel des Zylinders." },
        { q: "Was ist der Schüttwinkel bei kegelförmigen Schüttguthaufen?", a: "Wenn trockenes Schüttgut (Sand, Kies) aufgeschüttet wird, begrenzt die innere Reibung den Böschungswinkel θ = arctan(h/r) zu einem stabilen Kegel (~34° bei Kies)." }
      ],
      es: [
        { q: "¿Por qué el volumen de un cono es exactamente un tercio del de un cilindro?", a: "Como demostraron Eudoxo, Arquímedes y el cálculo integral, la revolución de una recta genera secciones circulares cuya integración da: V = π ∫₀ʰ (r/h)² x² dx = ⅓ · π · r² · h." },
        { q: "¿Qué es el ángulo de reposo en montículos cónicos de material granular?", a: "Al verter materiales secos (arena, grava), la fricción interna limita el ángulo de inclinación θ = arctan(h/r), formando un cono estable característico (~34° para grava)." }
      ],
      fr: [
        { q: "Pourquoi le volume d'un cône vaut-il exactement un tiers de celui d'un cylindre ?", a: "Comme démontré par Eudoxe, Archimède et le calcul intégral, la rotation d'un triangle engendre des disques dont l'intégration donne : V = ⅓ · π · r² · h." },
        { q: "Qu'est-ce que l'angle de talus naturel dans les tas coniques de granulats ?", a: "Lors du déversement de granulats secs, le frottement interne limite la pente à l'angle de talus θ = arctan(h/r), formant un cône d'équilibre (~34° pour le gravier)." }
      ],
      it: [
        { q: "Perché il volume di un cono è esattamente un terzo di quello di un cilindro?", a: "Come dimostrato da Eudosso, Archimede e dal calcolo infinitesimale, l'integrazione delle sezioni circolari fornisce: V = ⅓ · π · r² · h, esattamente un terzo del cilindro." },
        { q: "Cos'è l'angolo di riposo naturale nei cumuli conici di materiale granulare?", a: "Quando materiali granulari asciutti si accumulano, l'attrito interno limita la pendenza all'angolo di riposo θ = arctan(h/r), generando un cono stabile (~34° per la ghiaia)." }
      ],
      pt: [
        { q: "Por que o volume de um cone é exatamente um terço do volume de um cilindro?", a: "Como demonstrado por Eudoxo, Arquimedes e pelo cálculo integral, a integração das fatias circulares fornece: V = ⅓ · π · r² · h, exatamente um terço do cilindro." },
        { q: "O que é o ângulo de repouso em pilhas cônicas de material granular?", a: "Ao despejar agregados secos (areia, cascalho), o atrito interno limita a inclinação ao ângulo θ = arctan(h/r), gerando um cone estável (~34° para brita)." }
      ],
      nl: [
        { q: "Waarom is het volume van een kegel precies een derde van een cilinder?", a: "Zoals bewezen door Eudoxus, Archimedes en integraalrekening, levert de integratie van cirkelvormige schijven: V = ⅓ · π · r² · h, exact een derde van de cilinderinhoud." },
        { q: "Wat is de natuurlijk taluudhoek bij kegelvormige korrelhopen?", a: "Bij het storten van zand of grind begrenst de interne wrijving de hellingshoek tot θ = arctan(h/r), waardoor een stabiele kegel ontstaat (~34° voor grind)." }
      ],
      pl: [
        { q: "Dlaczego objętość stożka wynosi dokładnie jedną trzecią objętości walca?", a: "Jak udowodnili Eudoksos, Archimedes i rachunek całkowy, całkowanie przekrojów poprzecznych daje: V = ⅓ · π · r² · h, dokładnie jedną trzecią opisanego walca." },
        { q: "Czym jest kąt nasypu w stożkowych hałdach materiałów sypkich?", a: "Gdy sypki materiał usypuje się w hałdę, tarcie wewnętrzne ogranicza kąt nachylenia stoku θ = arctan(h/r), tworząc stabilny stożek nasypowy (~34° dla żwiru)." }
      ],
      sv: [
        { q: "Varför är en kons volym exakt en tredjedel av en cylinders?", a: "Som bevisats av Eudoxos, Arkimedes och integralkalkyl ger rotation av en rät linje: V = ⅓ · π · r² · h, exakt en tredjedel av cylinderns volym." },
        { q: "Vad är rasvinkeln för koniska materialhögar?", a: "När torrt material hälls upp begränsar inre friktion släntvinkeln till θ = arctan(h/r), vilket bildar en stabil kon (~34° för grus)." }
      ],
      no: [
        { q: "Hvorfor er volumet av en kjegle nøyaktig en tredjedel av en sylinder?", a: "Som bevist av Eudoxos, Arkimedes og integralkalkylen, gir integrasjon av tverrsnittene: V = ⅓ · π · r² · h, nøyaktig en tredjedel av sylindervolumet." },
        { q: "Hva er rasvinkelen for kjegleformede masser?", a: "Når tørre masser fylles opp, begrenser indre friksjon skråningsvinkelen til θ = arctan(h/r), og danner en stabil kjegle (~34° for grus)." }
      ],
      fi: [
        { q: "Miksi kartion tilavuus on tasan kolmasosa lieriön tilavuudesta?", a: "Kuten Eudoksos, Arkhimedes ja integraalilaskenta osoittavat, poikkileikkausten integrointi antaa: V = ⅓ · π · r² · h, tasan yhden kolmasosan lieriön tilavuudesta." },
        { q: "Mikä on lepokulma kartiomaisissa maarakeisissa kasoissa?", a: "Kun soraa tai hiekkaa kasataan, sisäinen kitka rajoittaa kaltevuuskulman arvoon θ = arctan(h/r), jolloin syntyy vakaa kartio (~34° soralle)." }
      ],
      ro: [
        { q: "De ce volumul unui con este exact o treime din volumul unui cilindru?", a: "Așa cum au demonstrat Eudoxus, Arhimede și calculul integral, integrarea secțiunilor circulare oferă: V = ⅓ · π · r² · h, exact o treime din volumul cilindrului circumscris." },
        { q: "Ce este unghiul de taluz natural în grămezile conice de granule?", a: "Când materiale granulare uscate sunt vărsate, frecarea internă limitează panta la unghiul θ = arctan(h/r), formând un con stabil (~34° pentru pietriș)." }
      ]
    },
    proofs: {
      de: [
        { title: "Rotationskörper-Integral", body: "Rotation der Geraden y = (r/h)x von 0 bis h um die x-Achse: V = π ∫₀ʰ (r/h)² x² dx = π(r²/h²) · [h³/3] = ⅓ · π · r² · h." },
        { title: "Pythagoreische Mantellinie", body: "Spitze, Mittelpunkt und Umfang bilden ein rechtwinkliges Dreieck: Mantellinie s = √(r² + h²)." },
        { title: "Sektorabwicklung für die Mantelfläche", body: "Die abgewickelte Mantelfläche bildet einen Kreissektor mit Radius s und Bogen 2πr: A_Mantel = π · r · s. Gesamtoberfläche = πr(s + r)." }
      ],
      es: [
        { title: "Integral de sólido de revolución", body: "Rotando la recta y = (r/h)x de 0 a h sobre el eje x: V = π ∫₀ʰ (r/h)² x² dx = ⅓ · π · r² · h." },
        { title: "Generatriz pitagórica", body: "El vértice, el centro y el perímetro forman un triángulo rectángulo: s = √(r² + h²)." },
        { title: "Desarrollo del sector para el área lateral", body: "La superficie lateral extendida forma un sector circular de radio s y arco 2πr: A_lat = π · r · s. Área Total = πr(s + r)." }
      ],
      fr: [
        { title: "Intégrale de solide de révolution", body: "En faisant tourner la droite y = (r/h)x de 0 à h autour de l'axe Ox : V = π ∫₀ʰ (r/h)² x² dx = ⅓ · π · r² · h." },
        { title: "Génératrice pythagoricienne", body: "Le sommet, le centre et le contour forment un triangle rectangle : s = √(r² + h²)." },
        { title: "Développement du secteur pour l'aire latérale", body: "La surface latérale déroulée forme un secteur de rayon s et d'arc 2πr : A_lat = π · r · s. Aire Totale = πr(s + r)." }
      ],
      it: [
        { title: "Integrale di solido di rivoluzione", body: "Ruotando la retta y = (r/h)x attorno all'asse x da 0 a h: V = π ∫₀ʰ (r/h)² x² dx = ⅓ · π · r² · h." },
        { title: "Apotema pitagorico", body: "Il vertice, il centro e il perimetro formano un triangolo rettangolo: s = √(r² + h²)." },
        { title: "Sviluppo del settore per l'area laterale", body: "La superficie laterale sviluppata forma un settore circolare di raggio s e arco 2πr: A_lat = π · r · s. Area Totale = πr(s + r)." }
      ],
      pt: [
        { title: "Integral de sólido de revolução", body: "Rotacionando a reta y = (r/h)x em torno do eixo x de 0 a h: V = π ∫₀ʰ (r/h)² x² dx = ⅓ · π · r² · h." },
        { title: "Geratriz pitagórica", body: "O vértice, o centro e o perímetro formam um triângulo retângulo: s = √(r² + h²)." },
        { title: "Planificação do setor para área lateral", body: "A superfície lateral planificada forma um setor de raio s e arco 2πr: A_lat = π · r · s. Área Total = πr(s + r)." }
      ],
      nl: [
        { title: "Omwentelingsintegraal calculus", body: "Het wentelen van de lijn y = (r/h)x om de x-as van 0 tot h: V = π ∫₀ʰ (r/h)² x² dx = ⅓ · π · r² · h." },
        { title: "Pythagorese schuine hoogte", body: "De top, het middelpunt en de omtrek vormen een rechthoekige driehoek: s = √(r² + h²)." },
        { title: "Sectoraanwas voor manteloppervlakte", body: "Het uitgevouwen mantelvlak vormt een cirkelsector met straal s en boog 2πr: A_mantel = π · r · s. Totale oppervlakte = πr(s + r)." }
      ],
      pl: [
        { title: "Całka bryły obrotowej", body: "Obrót prostej y = (r/h)x wokół osi x od 0 do h daje: V = π ∫₀ʰ (r/h)² x² dx = ⅓ · π · r² · h." },
        { title: "Pitagorejska tworząca stożka", body: "Wierzchołek, środek i obwód podstawy tworzą trójkąt prostokątny: s = √(r² + h²)." },
        { title: "Rozwinięcie wycinka na pole boczne", body: "Powierzchnia boczna po rozwinięciu tworzy wycinek koła o promieniu s i łuku 2πr: A_boczne = π · r · s. Pole całkowite = πr(s + r)." }
      ],
      sv: [
        { title: "Rotationskroppsintegral", body: "Rotation av linjen y = (r/h)x runt x-axeln från 0 till h: V = π ∫₀ʰ (r/h)² x² dx = ⅓ · π · r² · h." },
        { title: "Pythagoreisk sidohöjd (generatris)", body: "Spetsen, mittpunkten och omkretsen bildar en rätvinklig triangel: s = √(r² + h²)." },
        { title: "Sektorutveckling för mantelyta", body: "Den utrullade mantelytan bildar en cirkelsektor med radie s och båglängd 2πr: A_mantel = π · r · s. Total area = πr(s + r)." }
      ],
      no: [
        { title: "Rotasjonskropp-integral", body: "Rotasjon av linjen y = (r/h)x rundt x-aksen fra 0 til h: V = π ∫₀ʰ (r/h)² x² dx = ⅓ · π · r² · h." },
        { title: "Pytagoreisk sidehøyde (generatrise)", body: "Toppunktet, sentrum og omkretsen danner en rettvinklet trekant: s = √(r² + h²)." },
        { title: "Sektorutvikling for mantelflate", body: "Den utrullede mantelflaten danner en sirkelsektor med radius s og buelengde 2πr: A_mantel = π · r · s. Totalt areal = πr(s + r)." }
      ],
      fi: [
        { title: "Pyörähdyskappaleen integraali", body: "Suoran y = (r/h)x pyörähtäessä x-akselin ympäri välillä 0...h: V = π ∫₀ʰ (r/h)² x² dx = ⅓ · π · r² · h." },
        { title: "Pythagoraan sivujana (generatrisi)", body: "Kärki, keskipiste ja kehä muodostavat suorakulmaisen kolmion: s = √(r² + h²)." },
        { title: "Sektorileikkaus vaipan alalle", body: "Auki rullattu vaippa muodostaa ympyräsektorin, jonka säde on s ja kaari 2πr: A_vaippa = π · r · s. Kokonaisala = πr(s + r)." }
      ],
      ro: [
        { title: "Integrala corpului de rotație", body: "Rotirea dreptei y = (r/h)x în jurul axei Ox de la 0 la h: V = π ∫₀ʰ (r/h)² x² dx = ⅓ · π · r² · h." },
        { title: "Apotema conului (Pitagora)", body: "Vârful, centrul bazei și cercul de bază formează un triunghi dreptunghic: s = √(r² + h²)." },
        { title: "Desfășurarea sectorului pentru aria laterală", body: "Suprafața laterală desfășurată formează un sector circular de rază s și arc 2πr: A_laterală = π · r · s. Arie totală = πr(s + r)." }
      ]
    }
  },

  "geometry/cylinder": {
    faqs: {
      de: [
        { q: "Welche Zylinderabmessungen maximieren das Volumen bei gegebener Oberfläche?", a: "Bei einem geschlossenen Zylinder mit vorgegebener Gesamtoberfläche wird das Volumen maximiert, wenn die Höhe genau dem Durchmesser entspricht (h = 2r)." },
        { q: "Wie berechnet man das Flüssigkeitsvolumen in einem liegenden Zylindertank?", a: "Das Flüssigkeitsvolumen entspricht der Kreisabschnittsfläche der Stirnseite multipliziert mit der Zylinderlänge L: V = L · [r² arccos((r-h)/r) - (r-h)√(2rh - h²)]." }
      ],
      es: [
        { q: "¿Qué dimensiones del cilindro maximizan el volumen para una superficie dada?", a: "Para un cilindro cerrado con área total fija, el volumen se maximiza cuando la altura es igual al diámetro (h = 2r)." },
        { q: "¿Cómo se calcula el volumen de líquido en un cilindro horizontal parcialmente lleno?", a: "El volumen equivale al área del segmento circular de la base multiplicada por la longitud L: V = L · [r² arccos((r-h)/r) - (r-h)√(2rh - h²)]." }
      ],
      fr: [
        { q: "Quelles dimensions de cylindre maximisent le volume pour une surface donnée ?", a: "Pour un cylindre fermé d'aire totale fixée, le volume est maximal lorsque la hauteur est égale au diamètre (h = 2r)." },
        { q: "Comment calcule-t-on le volume de liquide dans un cylindre horizontal partiellement rempli ?", a: "Le volume correspond à l'aire du segment circulaire rempli multipliée par la longueur L : V = L · [r² arccos((r-h)/r) - (r-h)√(2rh - h²)]." }
      ],
      it: [
        { q: "Quali dimensioni del cilindro massimizzano il volume per una data superficie?", a: "Per un cilindro chiuso di superficie totale assegnata, il volume è massimizzato quando l'altezza è pari al diametro (h = 2r)." },
        { q: "Come si calcola il volume di liquido in un cilindro orizzontale parzialmente pieno?", a: "Il volume corrisponde all'area del segmento circolare bagnato moltiplicata per la lunghezza L: V = L · [r² arccos((r-h)/r) - (r-h)√(2rh - h²)]." }
      ],
      pt: [
        { q: "Quais dimensões de cilindro maximizam o volume para uma dada área de superfície?", a: "Para um cilindro fechado com área superficial fixa, o volume é maximizado quando a altura é igual ao diâmetro (h = 2r)." },
        { q: "Como calcular o volume de líquido em um cilindro horizontal parcialmente cheio?", a: "O volume equivale à área do segmento circular multiplicada pelo comprimento L: V = L · [r² arccos((r-h)/r) - (r-h)√(2rh - h²)]." }
      ],
      nl: [
        { q: "Welke cilinderafmetingen maximaliseren het volume bij een gegeven oppervlakte?", a: "Voor een gesloten cilinder met een vast oppervlak is het volume maximaal wanneer de hoogte gelijk is aan de diameter (h = 2r)." },
        { q: "Hoe bereken je de vloeistofinhoud van een gedeeltelijk gevulde liggende cilinder?", a: "De inhoud is gelijk aan de oppervlakte van het cirkelsegment vermenigvuldigd met de lengte L: V = L · [r² arccos((r-h)/r) - (r-h)√(2rh - h²)]." }
      ],
      pl: [
        { q: "Jakie wymiary walca maksymalizują objętość przy danym polu powierzchni?", a: "Dla zamkniętego walca o stałym polu powierzchni objętość jest maksymalna, gdy wysokość równa się średnicy (h = 2r)." },
        { q: "Jak obliczyć objętość cieczy w częściowo napełnionym poziomym walcu?", a: "Objętość cieczy równa się polu zalanego odcinka koła pomnożonemu przez długość walca L: V = L · [r² arccos((r-h)/r) - (r-h)√(2rh - h²)]." }
      ],
      sv: [
        { q: "Vilka cylindermått maximerar volymen för en given mantelyta och totalarea?", a: "För en sluten cylinder med fast totalarea maximeras volymen när höjden är lika med diametern (h = 2r)." },
        { q: "Hur beräknas vätskevolymen i en delvis fylld horisontell cylinder?", a: "Vätskevolymen är lika med cirkelsegmentets area multiplicerat med cylinderns längd L: V = L · [r² arccos((r-h)/r) - (r-h)√(2rh - h²)]." }
      ],
      no: [
        { q: "Hvilke sylinderdimensjoner maksimerer volumet for et gitt overflateareal?", a: "For en lukket sylinder med fast overflateareal, maksimeres volumet når høyden er lik diameteren (h = 2r)." },
        { q: "Hvordan beregner man væskevolum i en delvis fylt liggende sylinder?", a: "Væskevolumet tilsvarer sirkelsegmentets areal multiplisert med sylinderens lengde L: V = L · [r² arccos((r-h)/r) - (r-h)√(2rh - h²)]." }
      ],
      fi: [
        { q: "Mitkä lieriön mitat maksimoivat tilavuuden annetulla kokonaispinta-alalla?", a: "Umpinaiselle lieriölle tilavuus maksimoituu annetulla pinta-alalla, kun korkeus on yhtä suuri kuin halkaisija (h = 2r)." },
        { q: "Miten lasketaan nesteen tilavuus osittain täytetyssä makaavassa lieriössä?", a: "Nesteen tilavuus on ympyräsegmentin pinta-ala kerrottuna lieriön pituudella L: V = L · [r² arccos((r-h)/r) - (r-h)√(2rh - h²)]." }
      ],
      ro: [
        { q: "Ce dimensiuni ale cilindrului maximizează volumul pentru o suprafață dată?", a: "Pentru un cilindru închis cu suprafață totală fixă, volumul este maximizat când înălțimea este egală cu diametrul (h = 2r)." },
        { q: "Cum se calculează volumul de lichid într-un cilindru orizontal parțial umplut?", a: "Volumul este egal cu aria segmentului de cerc umplut înmulțită cu lungimea cilindrului L: V = L · [r² arccos((r-h)/r) - (r-h)√(2rh - h²)]." }
      ]
    },
    proofs: {
      de: [
        { title: "Cavalierisches Prinzip für das Volumen", body: "Das Volumen eines geraden Zylinders ist das Produkt aus Grundfläche und Höhe: V = π · r² · h." },
        { title: "Abwicklung der Mantelfläche", body: "Die abgewickelte Mantelfläche bildet ein Rechteck mit der Breite des Kreisumfangs 2πr und der Höhe h: A_Mantel = 2πr · h." },
        { title: "Gesamte geschlossene Oberfläche", body: "Summe aus Mantelfläche sowie oberem und unterem Kreisdeckel: A_gesamt = 2πrh + 2πr² = 2πr(h + r)." }
      ],
      es: [
        { title: "Principio volumétrico de Cavalieri", body: "El volumen de un cilindro recto es el producto del área de su base circular por su altura: V = π · r² · h." },
        { title: "Desarrollo del área lateral", body: "Desenrollar la superficie curva produce un rectángulo de ancho 2πr y altura h: A_lat = 2πr · h." },
        { title: "Área total cerrada", body: "Sumando la superficie lateral más las dos bases circulares: A_total = 2πrh + 2πr² = 2πr(h + r)." }
      ],
      fr: [
        { title: "Principe volumétrique de Cavalieri", body: "Le volume d'un cylindre circulaire droit est le produit de sa base par sa hauteur : V = π · r² · h." },
        { title: "Patron et aire latérale", body: "Dérouler la surface courbe forme un rectangle de largeur 2πr et de hauteur h : A_lat = 2πr · h." },
        { title: "Aire totale fermée", body: "Somme de la surface latérale et des deux disques de base : A_totale = 2πrh + 2πr² = 2πr(h + r)." }
      ],
      it: [
        { title: "Principio volumetrico di Cavalieri", body: "Il volume di un cilindro circolare retto è il prodotto dell'area di base per l'altezza: V = π · r² · h." },
        { title: "Sviluppo dell'area laterale", body: "Lo sviluppo della superficie curva produce un rettangolo con base 2πr e altezza h: A_lat = 2πr · h." },
        { title: "Superficie totale chiusa", body: "Somma della parete laterale più le due basi circolari: A_totale = 2πrh + 2πr² = 2πr(h + r)." }
      ],
      pt: [
        { title: "Princípio volumétrico de Cavalieri", body: "O volume de um cilindro circular reto é o produto da área da base pela altura: V = π · r² · h." },
        { title: "Planificação da área lateral", body: "A planificação da parede curva forma um retângulo de largura 2πr e altura h: A_lat = 2πr · h." },
        { title: "Área total fechada", body: "Soma da área lateral com as duas tampas circulares: A_total = 2πrh + 2πr² = 2πr(h + r)." }
      ],
      nl: [
        { title: "Volumetrisch principe van Cavalieri", body: "Het volume van een rechte cilinder is het product van het grondvlak en de hoogte: V = π · r² · h." },
        { title: "Uitslag van de manteloppervlakte", body: "Het uitrollen van de mantel levert een rechthoek met breedte 2πr en hoogte h: A_mantel = 2πr · h." },
        { title: "Totale gesloten oppervlakte", body: "Som van de mantel plus boven- en ondercirkel: A_totaal = 2πrh + 2πr² = 2πr(h + r)." }
      ],
      pl: [
        { title: "Zasada Cavalieriego dla objętości", body: "Objętość walca prostego jest iloczynem pola podstawy kołowej i wysokości: V = π · r² · h." },
        { title: "Rozwinięcie powierzchni bocznej", body: "Rozwinięcie powierzchni bocznej tworzy prostokąt o szerokości 2πr i wysokości h: A_boczne = 2πr · h." },
        { title: "Pole powierzchni całkowitej", body: "Suma pola powierzchni bocznej i dwóch podstaw: A_całkowite = 2πrh + 2πr² = 2πr(h + r)." }
      ],
      sv: [
        { title: "Cavalieris volymprincip", body: "Volymen av en rät cirkulär cylinder är produkten av dess basarea och höjd: V = π · r² · h." },
        { title: "Mantelytans utbredning", body: "Utbredningen av den krökta mantelytan bildar en rektangel med bredden 2πr och höjden h: A_mantel = 2πr · h." },
        { title: "Total innesluten area", body: "Summan av mantelytan och de två cirkulära basytorna: A_total = 2πrh + 2πr² = 2πr(h + r)." }
      ],
      no: [
        { title: "Cavalieris volumprinsipp", body: "Volumet av en rett sirkulær sylinder er produktet av grunnflatearealet og høyden: V = π · r² · h." },
        { title: "Mantelflatens utbredelse", body: "Utrullingen av den krumme mantelflaten danner et rektangel med bredde 2πr og høyde h: A_mantel = 2πr · h." },
        { title: "Totalt overflateareal", body: "Summen av mantelflaten og de to sirkulære bunn- og toppflatene: A_total = 2πrh + 2πr² = 2πr(h + r)." }
      ],
      fi: [
        { title: "Cavalierin periaate tilavuudelle", body: "Suoran ympyrälieriön tilavuus on pohjan pinta-alan ja korkeuden tulo: V = π · r² · h." },
        { title: "Vaipan tasoitus", body: "Kaarevan vaipan avaaminen tasoon muodostaa suorakulmion, jonka kanta on 2πr ja korkeus h: A_vaippa = 2πr · h." },
        { title: "Kokonaispinta-ala", body: "Vaipan ja kahden ympyräpohjan pinta-alojen summa: A_kokonais = 2πrh + 2πr² = 2πr(h + r)." }
      ],
      ro: [
        { title: "Principiul volumetric al lui Cavalieri", body: "Volumul unui cilindru circular drept este produsul ariei bazei cu înălțimea: V = π · r² · h." },
        { title: "Desfășurarea ariei laterale", body: "Desfășurarea suprafeței curbe formează un dreptunghi cu lățimea 2πr și înălțimea h: A_laterală = 2πr · h." },
        { title: "Aria totală a cilindrului", body: "Suma ariei laterale și a celor două baze circulare: A_totală = 2πrh + 2πr² = 2πr(h + r)." }
      ]
    }
  },

  "geometry/ellipsoid": {
    faqs: {
      de: [
        { q: "Welche geometrische Form hat die Erde?", a: "Durch die Zentrifugalkraft der Erdrotation ist die Erde keine Kugel, sondern ein abgeplattetes Rotationsellipsoid mit einem Äquatorradius von ca. 6378 km und einem Polarradius von 6357 km." },
        { q: "Was unterscheidet ein gestrecktes von einem abgeplatteten Ellipsoid?", a: "Ein gestrecktes Ellipsoid (prolat, zigarrenförmig) hat a = b < c. Ein abgeplattetes Ellipsoid (oblat, linsenförmig) hat a = b > c." }
      ],
      es: [
        { q: "¿Qué forma geométrica tiene el planeta Tierra?", a: "Debido a las fuerzas centrífugas de su rotación, la Tierra es un esferoide oblato con un semieje ecuatorial de 6378 km y un semieje polar de 6357 km." },
        { q: "¿Cuál es la diferencia entre un elipsoide prolato y oblato?", a: "Un esferoide prolato (forma de balón) tiene a = b < c. Un esferoide oblato (forma de lenteja o disco) tiene a = b > c." }
      ],
      fr: [
        { q: "Quelle est la forme géométrique de la planète Terre ?", a: "En raison de la force centrifuge liée à sa rotation, la Terre est un ellipsoïde aplati aux pôles (sphéroïde oblate) avec un rayon équatorial de 6378 km et un rayon polaire de 6357 km." },
        { q: "Quelle est la différence entre un ellipsoïde prolate et oblate ?", a: "Un ellipsoïde prolate (forme de ballon) vérifie a = b < c. Un ellipsoïde oblate (aplati aux pôles) vérifie a = b > c." }
      ],
      it: [
        { q: "Qual è la forma geometrica del pianeta Terra?", a: "A causa della forza centrifuga dovuta alla rotazione, la Terra è uno sferoide oblato con raggio equatoriale di 6378 km e raggio polare di 6357 km." },
        { q: "Qual è la differenza tra un ellissoide prolato e oblato?", a: "Uno sferoide prolato (a forma di sigaro) ha a = b < c. Uno sferoide oblato (schiacciato ai poli) ha a = b > c." }
      ],
      pt: [
        { q: "Qual a forma geométrica do planeta Terra?", a: "Devido à rotação, a Terra é um esferoide oblato com raio equatorial de 6378 km e raio polar de 6357 km." },
        { q: "Qual a diferença entre um elipsoide prolato e oblato?", a: "Um esferoide prolato possui a = b < c. Um esferoide oblato (achatado nos polos) possui a = b > c." }
      ],
      nl: [
        { q: "Welke geometrische vorm heeft de aarde?", a: "Door de middelpuntvliedende kracht van de aardrotatie is de aarde een afgeplatte ellipsoïde met een equatorstraal van 6378 km en een poolstraal van 6357 km." },
        { q: "Wat is het verschil tussen een gerekte en afgeplatte ellipsoïde?", a: "Een gerekte ellipsoïde (prolaat) heeft a = b < c. Een afgeplatte ellipsoïde (oblaat) heeft a = b > c." }
      ],
      pl: [
        { q: "Jaki kształt geometryczny ma Ziemia?", a: "Z powodu siły odśrodkowej Ziemia jest elipsoidą obrotową spłaszczoną o promieniu równikowym 6378 km i biegunowym 6357 km." },
        { q: "Czym różni się elipsoida wydłużona od spłaszczonej?", a: "Elipsoida wydłużona (prolate) spełnia a = b < c. Elipsoida spłaszczona (oblate) spełnia a = b > c." }
      ],
      sv: [
        { q: "Vilken form har planeten jorden?", a: "Jordens rotation gör att den är en tillplattad rotationsellipsoid med en ekvatorsradie på 6378 km och polradie på 6357 km." },
        { q: "Vad skiljer en prolat från en oblat ellipsoid?", a: "En prolat ellipsoid (avflackad vid ekvatorn) har a = b < c. En oblat ellipsoid (tillplattad vid polerna) har a = b > c." }
      ],
      no: [
        { q: "Hvilken form har planeten jorden?", a: "Jordens rotasjon gjør at den er en flattrykt rotasjonsellipsoide med ekvatorradius på 6378 km og polradius på 6357 km." },
        { q: "Hva er forskjellen mellom en prolat og oblat ellipsoide?", a: "En prolat ellipsoide har a = b < c. En oblat ellipsoide (flattrykt ved polene) har a = b > c." }
      ],
      fi: [
        { q: "Mikä on maapallon geometrinen muoto?", a: "Maan pyörimisestä johtuen maapallo on navoiltaan litistynyt ellipsoidi, jonka päiväntasaajasäde on 6378 km ja napasäde 6357 km." },
        { q: "Mitä eroa on pitkänomaisella ja litistyneellä ellipsoidilla?", a: "Pitkänomaisessa ellipsoidissa a = b < c. Litistyneessä ellipsoidissa a = b > c." }
      ],
      ro: [
        { q: "Ce formă geometrică are planeta Pământ?", a: "Datorită forței centrifuge a rotației, Pământul este un elipsoid turtit la poli cu raza ecuatorială de 6378 km și polară de 6357 km." },
        { q: "Care este diferența dintre un elipsoid prolat și oblat?", a: "Un sferoid prolat are a = b < c. Un sferoid oblat (turtit la poli) are a = b > c." }
      ]
    },
    proofs: {
      de: [
        { title: "Ellipsoid-Volumenintegral", body: "Lineare Streckung der Einheitskugel um die Faktoren a, b und c: V = ∭ dx dy dz = ⁴⁄₃ · π · a · b · c." },
        { title: "Oberflächenformel nach Knud Thomsen", body: "Da die exakte Oberfläche elliptische Integrale erfordert, liefert Thomsens Formel eine geschlossene Näherung: S ≈ 4π · [((ab)ᵖ + (ac)ᵖ + (bc)ᵖ) / 3]^(1/p) mit p ≈ 1,6075." },
        { title: "Schranke für den relativen Fehler", body: "Thomsens Näherung begrenzt den maximalen relativen Fehler auf unter 1,061% über alle denkbaren Achsenverhältnisse." }
      ],
      es: [
        { title: "Integral de volumen del elipsoide", body: "Estirando linealmente la esfera unidad por los factores a, b y c: V = ∭ dx dy dz = ⁴⁄₃ · π · a · b · c." },
        { title: "Fórmula de superficie de Knud Thomsen", body: "La superficie exacta requiere integrales elípticas; la fórmula de Thomsen proporciona: S ≈ 4π · [((ab)ᵖ + (ac)ᵖ + (bc)ᵖ) / 3]^(1/p) con p ≈ 1,6075." },
        { title: "Límite del error relativo", body: "La fórmula de Thomsen acota el error relativo máximo por debajo del 1,061% en cualquier geometría elipsoidal." }
      ],
      fr: [
        { title: "Intégrale de volume de l'ellipsoïde", body: "Par étirement de la sphère unité selon les facteurs a, b et c : V = ∭ dx dy dz = ⁴⁄₃ · π · a · b · c." },
        { title: "Formule de surface de Knud Thomsen", body: "L'aire exacte nécessitant des intégrales elliptiques, la formule de Thomsen donne : S ≈ 4π · [((ab)ᵖ + (ac)ᵖ + (bc)ᵖ) / 3]^(1/p) avec p ≈ 1,6075." },
        { title: "Borne sur l'erreur relative", body: "La formule de Thomsen garantit une erreur relative maximale inférieure à 1,061 % pour toute configuration d'axes." }
      ],
      it: [
        { title: "Integrale di volume dell'ellissoide", body: "Per dilatazione lineare della sfera unitaria con fattori a, b e c: V = ∭ dx dy dz = ⁴⁄₃ · π · a · b · c." },
        { title: "Formula di superficie di Knud Thomsen", body: "L'area esatta richiede integrali ellittici; la formula di Thomsen approssima: S ≈ 4π · [((ab)ᵖ + (ac)ᵖ + (bc)ᵖ) / 3]^(1/p) con p ≈ 1,6075." },
        { title: "Limite dell'errore relativo", body: "La formula di Thomsen limita l'errore relativo massimo a meno dell'1,061% per qualsiasi rapporto tra i semiassi." }
      ],
      pt: [
        { title: "Integral de volume do elipsoide", body: "Por transformação afim da esfera unitária com fatores a, b e c: V = ∭ dx dy dz = ⁴⁄₃ · π · a · b · c." },
        { title: "Fórmula de superfície de Knud Thomsen", body: "Como a área exata exige integrais elípticas, Thomsen propôs: S ≈ 4π · [((ab)ᵖ + (ac)ᵖ + (bc)ᵖ) / 3]^(1/p) com p ≈ 1,6075." },
        { title: "Limite do erro relativo", body: "A fórmula de Thomsen limita o erro relativo máximo a menos de 1,061% para qualquer proporção de eixos." }
      ],
      nl: [
        { title: "Volume-integraal ellipsoïde", body: "Lineaire oprekking van de eenheidsbol met a, b en c: V = ∭ dx dy dz = ⁴⁄₃ · π · a · b · c." },
        { title: "Oppervlakteformule van Knud Thomsen", body: "Omdat de exacte oppervlakte elliptische integralen vereist, geldt: S ≈ 4π · [((ab)ᵖ + (ac)ᵖ + (bc)ᵖ) / 3]^(1/p) met p ≈ 1,6075." },
        { title: "Foutgrens", body: "Thomsens formule beperkt de maximale relatieve fout tot minder dan 1,061% voor alle mogelijke asverhoudingen." }
      ],
      pl: [
        { title: "Całka objętości elipsoidy", body: "Liniowe przekształcenie kuli jednostkowej ze współczynnikami a, b i c: V = ∭ dx dy dz = ⁴⁄₃ · π · a · b · c." },
        { title: "Wzór Knuda Thomsena na pole powierzchni", body: "Dokładne pole wymaga całek eliptycznych; wzór Thomsena podaje: S ≈ 4π · [((ab)ᵖ + (ac)ᵖ + (bc)ᵖ) / 3]^(1/p) z p ≈ 1,6075." },
        { title: "Ograniczenie błędu względnego", body: "Przybliżenie Thomsena ogranicza maksymalny błąd względny do poniżej 1,061% dla dowolnych osi." }
      ],
      sv: [
        { title: "Volymintegral för ellipsoid", body: "Linjär sträckning av enhetsklotet med faktorerna a, b och c: V = ∭ dx dy dz = ⁴⁄₃ · π · a · b · c." },
        { title: "Knud Thomsens ytformel", body: "Eftersom exakt area kräver elliptiska integraler ger Thomsens formel: S ≈ 4π · [((ab)ᵖ + (ac)ᵖ + (bc)ᵖ) / 3]^(1/p) med p ≈ 1,6075." },
        { title: "Övre gräns för relativt fel", body: "Thomsens approximation begränsar det maximala relativa felet till under 1,061% för alla axelförhållanden." }
      ],
      no: [
        { title: "Volumintegral for ellipsoide", body: "Lineær strekking av enhetskulen med faktorene a, b og c: V = ∭ dx dy dz = ⁴⁄₃ · π · a · b · c." },
        { title: "Knud Thomsens overflateformel", body: "Siden nøyaktig areal krever elliptiske integraler gir Thomsens formel: S ≈ 4π · [((ab)ᵖ + (ac)ᵖ + (bc)ᵖ) / 3]^(1/p) med p ≈ 1,6075." },
        { title: "Grense for relativ feil", body: "Thomsens formel begrenser den maksimale relative feilen til under 1,061% for alle akseforhold." }
      ],
      fi: [
        { title: "Ellipsoidin tilavuusintegraali", body: "Yksikköpallon venytys kertoimilla a, b ja c: V = ∭ dx dy dz = ⁴⁄₃ · π · a · b · c." },
        { title: "Knud Thomsenin pinta-alakaava", body: "Tarkka ala vaatii elliptisiä integraaleja; Thomsenin kaava antaa: S ≈ 4π · [((ab)ᵖ + (ac)ᵖ + (bc)ᵖ) / 3]^(1/p), missä p ≈ 1,6075." },
        { title: "Suhteellisen virheen yläraja", body: "Thomsenin kaavan suurin suhteellinen virhe on alle 1,061% kaikilla mahdollisilla akselisuhteilla." }
      ],
      ro: [
        { title: "Integrala volumului elipsoidului", body: "Întinderea liniară a sferei unitate cu factorii a, b și c: V = ∭ dx dy dz = ⁴⁄₃ · π · a · b · c." },
        { title: "Formula de arie a lui Knud Thomsen", body: "Aria exactă necesitând integrale eliptice, formula lui Thomsen oferă: S ≈ 4π · [((ab)ᵖ + (ac)ᵖ + (bc)ᵖ) / 3]^(1/p) cu p ≈ 1,6075." },
        { title: "Limita erorii relative", body: "Formula lui Thomsen plafonează eroarea relativă maximă sub 1,061% pentru orice elipsoid." }
      ]
    }
  },

  "geometry/torus": {
    faqs: {
      de: [
        { q: "Was ist der Unterschied zwischen einem Ring-Torus, Horn-Torus und Spindel-Torus?", a: "Bei R > r entsteht ein offener Ring-Torus (Donut). Bei R = r berührt sich das Mittelloch im Horn-Torus. Bei R < r schneidet sich die Oberfläche selbst im Spindel-Torus." },
        { q: "Welche Euler-Charakteristik besitzt ein Torus?", a: "Ein Torus besitzt das topologische Geschlecht g = 1 und die Euler-Charakteristik χ = V - E + F = 2 - 2g = 0." }
      ],
      es: [
        { q: "¿Cuál es la diferencia entre un toro anular, cornudo y fusiforme?", a: "Con R > r se tiene un toro anular con orificio central abierto. Con R = r se tocan en el eje formando un toro cornudo. Con R < r la superficie se autointerseca formando un toro huso o fusiforme." },
        { q: "¿Cuál es la característica de Euler de un toro?", a: "Un toro tiene género topológico g = 1 y característica de Euler χ = V - E + F = 2 - 2g = 0." }
      ],
      fr: [
        { q: "Quelle est la différence entre un tore anneau, un tore à cornes et un tore croisé ?", a: "Pour R > r, le tore est un anneau classique. Pour R = r, il s'agit d'un tore à cornes se touchant en un point. Pour R < r, le tore est croisé ou fusiforme." },
        { q: "Quelle est la caractéristique d'Euler d'un tore ?", a: "Un tore a pour genre topologique g = 1 et pour caractéristique d'Euler χ = V - E + F = 2 - 2g = 0." }
      ],
      it: [
        { q: "Qual è la differenza tra toro ad anello, a corno e a fuso?", a: "Con R > r si ottiene un toro ad anello aperto (ciambella). Con R = r le superfici si toccano sull'asse (toro a corno). Con R < r la superficie si autointerseca (toro a fuso)." },
        { q: "Qual è la caratteristica di Eulero di un toro?", a: "Un toro ha genere topologico g = 1 e caratteristica di Eulero χ = V - E + F = 2 - 2g = 0." }
      ],
      pt: [
        { q: "Qual a diferença entre um toro anular, chifrudo e fuso?", a: "Com R > r temos um toro anular aberto. Com R = r as faces tocam-se no eixo. Com R < r a superfície cruza-se a si mesma formando um toro fuso." },
        { q: "Qual é a característica de Euler de um toro?", a: "O toro possui gênero topológico g = 1 e característica de Euler χ = V - E + F = 2 - 2g = 0." }
      ],
      nl: [
        { q: "Wat is het verschil tussen een ringtorus, hoorntorus en spiltorus?", a: "Bij R > r is er een open ringtorus. Bij R = r raakt het middengat elkaar. Bij R < r snijdt het oppervlak zichzelf in een spiltorus." },
        { q: "Wat is de Euler-karakteristiek van een torus?", a: "Een torus heeft geslacht g = 1 en Euler-karakteristiek χ = V - E + F = 2 - 2g = 0." }
      ],
      pl: [
        { q: "Jaka jest różnica między torusem pierścieniowym, rogowym a wrzecionowatym?", a: "Gdy R > r, torus ma otwarty otwór (obwarzanek). Gdy R = r, otwór zbiega się w punkcie. Gdy R < r, powierzchnia przecina samą siebie." },
        { q: "Jaka jest charakterystyka Eulera torusa?", a: "Torus ma genus g = 1 i charakterystykę Eulera χ = V - E + F = 2 - 2g = 0." }
      ],
      sv: [
        { q: "Vad skiljer en ringtorus, horntorus och spindeltorus?", a: "När R > r har man en öppen ringtorus (donut). Vid R = r möts ytorna i centrum. Vid R < r skär ytan sig själv i en spindeltorus." },
        { q: "Vad är en torus Euler-karakteristik?", a: "En torus har topologiskt genus g = 1 och Euler-karakteristik χ = V - E + F = 2 - 2g = 0." }
      ],
      no: [
        { q: "Hva skiller en ringtorus, horntorus og spindeltorus?", a: "Når R > r har man en åpen ringtorus. Ved R = r møtes flatene i midtpunktet. Ved R < r skjærer flaten seg selv i en spindeltorus." },
        { q: "Hva er en torus' Euler-karakteristikk?", a: "En torus har topologisk genus g = 1 og Euler-karakteristikk χ = V - E + F = 2 - 2g = 0." }
      ],
      fi: [
        { q: "Mitä eroa on rengastoruksella, sarvitoruksella ja sukkulatoruksella?", a: "Kun R > r, kyseessä on avoin rengastorus (donitsi). Kun R = r, keskireikä sulkeutuu yhdessä pisteessä. Kun R < r, pinta leikkaa itsensä." },
        { q: "Mikä on toruksen Eulerin karakteristika?", a: "Toruksen suku on g = 1 ja Eulerin karakteristika on χ = V - E + F = 2 - 2g = 0." }
      ],
      ro: [
        { q: "Care este diferența dintre un tor inelar, un tor cornut și un tor fusiform?", a: "Pentru R > r avem un tor inelar cu deschidere centrală. Pentru R = r orificiul se atinge în centru. Pentru R < r suprafața se autointersectează într-un tor fusiform." },
        { q: "Care este caracteristica Euler a unui tor?", a: "Un tor are genul topologic g = 1 și caracteristica Euler χ = V - E + F = 2 - 2g = 0." }
      ]
    },
    proofs: {
      de: [
        { title: "Erster Satz von Pappus-Guldin (Volumen)", body: "Das Volumen entspricht der Querschnittsfläche multipliziert mit dem Weg des Schwerpunkts: V = (πr²) · (2πR) = 2π² · R · r²." },
        { title: "Zweiter Satz von Pappus-Guldin (Oberfläche)", body: "Die Oberfläche entspricht dem Kreisumfang multipliziert mit dem Umlaufweg: A = (2πr) · (2πR) = 4π² · R · r." },
        { title: "Geometrische Bedingung für den Ring-Torus", body: "Für R > r ist der Torus regulär ohne Selbstdurchdringung und besitzt eine lichte Öffnung von 2(R - r)." }
      ],
      es: [
        { title: "Primer teorema de Pappus-Guldin (Volumen)", body: "El volumen es el área transversal por la distancia recorrida por su centroide: V = (πr²) · (2πR) = 2π² · R · r²." },
        { title: "Segundo teorema de Pappus-Guldin (Área superficial)", body: "El área superficial es el perímetro transversal por la trayectoria recorrida: A = (2πr) · (2πR) = 4π² · R · r." },
        { title: "Condición geométrica del toro anular", body: "Cuando R > r, el toro es regular y posee una abertura central de 2(R - r)." }
      ],
      fr: [
        { title: "Premier théorème de Guldin (Volume)", body: "Le volume est égal à l'aire de la section multipliée par la trajectoire du centroïde : V = (πr²) · (2πR) = 2π² · R · r²." },
        { title: "Second théorème de Guldin (Aire de surface)", body: "L'aire vaut le périmètre de la section multiplié par la distance parcourue : A = (2πr) · (2πR) = 4π² · R · r." },
        { title: "Condition géométrique du tore anneau", body: "Pour R > r, le tore est régulier sans auto-intersection et possède un trou de 2(R - r)." }
      ],
      it: [
        { title: "Primo teorema di Pappo-Guldino (Volume)", body: "Il volume è dato dall'area della sezione per la distanza percorsa dal baricentro: V = (πr²) · (2πR) = 2π² · R · r²." },
        { title: "Secondo teorema di Pappo-Guldino (Superficie)", body: "La superficie è pari al perimetro della sezione per il percorso compiuto: A = (2πr) · (2πR) = 4π² · R · r." },
        { title: "Condizione geometrica del toro ad anello", body: "Per R > r il toro è privo di autointersezioni con un'apertura di 2(R - r)." }
      ],
      pt: [
        { title: "Primeiro teorema de Pappus-Guldin (Volume)", body: "O volume equivale à área transversal multiplicada pelo trajeto do centroide: V = (πr²) · (2πR) = 2π² · R · r²." },
        { title: "Segundo teorema de Pappus-Guldin (Área superficial)", body: "A área superficial é o perímetro transversal vezes a distância percorrida: A = (2πr) · (2πR) = 4π² · R · r." },
        { title: "Condição geométrica do toro anular", body: "Quando R > r, o toro é regular com abertura central de 2(R - r)." }
      ],
      nl: [
        { title: "Eerste stelling van Guldin (Volume)", body: "Het volume is gelijk aan de doorsnede-oppervlakte maal de afgelegde weg van het zwaartepunt: V = (πr²) · (2πR) = 2π² · R · r²." },
        { title: "Tweede stelling van Guldin (Oppervlakte)", body: "De oppervlakte is de omtrek van de doorsnede maal de omwentelingsbaan: A = (2πr) · (2πR) = 4π² · R · r." },
        { title: "Meetkundige voorwaarde ringtorus", body: "Voor R > r is de torus een open ring met centrale opening 2(R - r)." }
      ],
      pl: [
        { title: "Pierwsze twierdzenie Pappusa-Guldina (Objętość)", body: "Objętość równa się polu przekroju pomnożonemu przez drogę środka ciężkości: V = (πr²) · (2πR) = 2π² · R · r²." },
        { title: "Drugie twierdzenie Pappusa-Guldina (Pole powierzchni)", body: "Pole powierzchni równa się obwodowi przekroju pomnożonemu przez drogę obrotu: A = (2πr) · (2πR) = 4π² · R · r." },
        { title: "Warunek geometryczny torusa pierścieniowego", body: "Gdy R > r, torus jest regularny ze światłem otworu 2(R - r)." }
      ],
      sv: [
        { title: "Pappos-Guldins första sats (Volym)", body: "Volymen är lika med tvärsnittsarean multiplicerad med tyngdpunktens bana: V = (πr²) · (2πR) = 2π² · R · r²." },
        { title: "Pappos-Guldins andra sats (Area)", body: "Arean är lika med tvärsnittets omkrets gånger dess rotationsväg: A = (2πr) · (2πR) = 4π² · R · r." },
        { title: "Geometriskt villkor för ringtorus", body: "När R > r bildas en regelbunden ringtorus med fri öppning 2(R - r)." }
      ],
      no: [
        { title: "Pappus-Guldins første teorem (Volum)", body: "Volumet er lik tverrsnittsarealet multiplisert med tyngdepunktets bane: V = (πr²) · (2πR) = 2π² · R · r²." },
        { title: "Pappus-Guldins andre teorem (Overflateareal)", body: "Overflatearealet er tverrsnittets omkrets multiplisert med rotasjonsbanen: A = (2πr) · (2πR) = 4π² · R · r." },
        { title: "Geometrisk betingelse for ringtorus", body: "Når R > r er torusen en regulær ring med en åpning på 2(R - r)." }
      ],
      fi: [
        { title: "Pappuksen ensimmäinen lause (Tilavuus)", body: "Tilavuus on poikkileikkauksen pinta-ala kerrottuna painopisteen kulkureitillä: V = (πr²) · (2πR) = 2π² · R · r²." },
        { title: "Pappuksen toinen lause (Pinta-ala)", body: "Pinta-ala on poikkileikkauksen piiri kerrottuna pyörähdysradan pituudella: A = (2πr) · (2πR) = 4π² · R · r." },
        { title: "Rengastoruksen geometrinen ehto", body: "Kun R > r, torus on säännöllinen rengastorus, jonka keskiaukko on 2(R - r)." }
      ],
      ro: [
        { title: "Prima teoremă Pappus-Guldin (Volum)", body: "Volumul este aria secțiunii transversale înmulțită cu drumul parcurs de centrul de greutate: V = (πr²) · (2πR) = 2π² · R · r²." },
        { title: "A doua teoremă Pappus-Guldin (Arie)", body: "Aria suprafeței este perimetrul secțiunii înmulțit cu drumul parcurs: A = (2πr) · (2πR) = 4π² · R · r." },
        { title: "Condiția geometrică a torului inelar", body: "Când R > r, torul este regulat, fără autointersecții, cu o deschidere de 2(R - r)." }
      ]
    }
  },

  "geometry/pyramid": {
    faqs: {
      de: [
        { q: "Warum beträgt das Volumen einer quadratischen Pyramide ein Drittel des Prismas?", a: "Ein Würfel lässt sich exakt in drei identische, kongruente Pyramiden mit quadratischer Grundfläche zerlegen: V = ⅓ · a² · h." },
        { q: "Welchen Neigungswinkel besitzt die Cheops-Pyramide von Gizeh?", a: "Die Cheops-Pyramide besitzt einen Neigungswinkel von ca. 51,85° (51° 50′), was dem Verhältnis des Goldenen Schnitts φ entspricht." }
      ],
      es: [
        { q: "¿Por qué el volumen de una pirámide cuadrada es un tercio del prisma?", a: "Un prisma o cubo puede descomponerse en tres pirámides congruentes de base cuadrada: V = ⅓ · a² · h." },
        { q: "¿Qué inclinación tiene la Gran Pirámide de Guiza?", a: "Posee una pendiente de aproximadamente 51,85° (51° 50′), muy cercana a la proporción áurea φ." }
      ],
      fr: [
        { q: "Pourquoi le volume d'une pyramide vaut-il un tiers de celui du prisme ?", a: "Un cube se décompose exactement en trois pyramides congruentes de base carrée : V = ⅓ · a² · h." },
        { q: "Quelle est l'inclinaison de la Grande Pyramide de Gizeh ?", a: "La pyramide de Khéops a une pente d'environ 51,85° (51° 50′), liée au nombre d'or φ." }
      ],
      it: [
        { q: "Perché il volume di una piramide quadrata è un terzo del prisma?", a: "Un cubo può essere scomposto in tre piramidi congruenti a base quadrata: V = ⅓ · a² · h." },
        { q: "Qual è la pendenza della Grande Piramide di Giza?", a: "Presenta una pendenza di circa 51,85° (51° 50′), legata alla sezione aurea φ." }
      ],
      pt: [
        { q: "Por que o volume de uma pirâmide é um terço do prisma?", a: "Um cubo decompõe-se exatamente em três pirâmides congruentes: V = ⅓ · a² · h." },
        { q: "Qual a inclinação da Grande Pirâmide de Gizé?", a: "Apresenta uma inclinação de aproximadamente 51,85°, relacionada à proporção áurea φ." }
      ],
      nl: [
        { q: "Waarom is het volume van een piramide een derde van een prisma?", a: "Een kubus kan worden ontleed in drie congruente piramides met vierkant grondvlak: V = ⅓ · a² · h." },
        { q: "Wat is de hellingshoek van de Piramide van Cheops?", a: "De Grote Piramide heeft een helling van ongeveer 51,85°, gekoppeld aan de gulden snede φ." }
      ],
      pl: [
        { q: "Dlaczego objętość ostrosłupa prawidłowego wynosi jedną trzecią graniastosłupa?", a: "Sześcian można podzielić na trzy przystające ostrosłupy o kwadratowej podstawie: V = ⅓ · a² · h." },
        { q: "Jaki jest kąt nachylenia Piramidy Cheopsa?", a: "Wielka Piramida w Gizie ma kąt nachylenia około 51,85° (51° 50′), powiązany ze złotym podziałem φ." }
      ],
      sv: [
        { q: "Varför är volymen av en fyrsidig pyramid en tredjedel av ett prisma?", a: "En kub kan delas upp i tre kongruenta pyramider med kvadratisk bas: V = ⅓ · a² · h." },
        { q: "Vilken lutningsvinkel har Cheopspyramiden?", a: "Cheopspyramiden har en sidolutning på cirka 51,85°, vilket anknyter till det gyllene snittet φ." }
      ],
      no: [
        { q: "Hvorfor er volumet av en kvadratisk pyramide en tredjedel av et prisme?", a: "En terning kan deles inn i tre kongruente pyramider med kvadratisk grunnflate: V = ⅓ · a² · h." },
        { q: "Hva er helningsvinkelen til Kheopspyramiden?", a: "Kheopspyramiden har en helningsvinkel på omtrent 51,85°, nært knyttet til det gylne snitt φ." }
      ],
      fi: [
        { q: "Miksi neliöpohjaisen pyramidin tilavuus on kolmasosa särmiöstä?", a: "Kuutio voidaan jakaa kolmeksi yhteneväksi neliöpohjaiseksi pyramidiksi: V = ⅓ · a² · h." },
        { q: "Mikä on Gizan suuren pyramidin kaltevuuskulma?", a: "Kheopsin pyramidin kaltevuuskulma on noin 51,85°, mikä liittyy kultaiseen leikkaukseen φ." }
      ],
      ro: [
        { q: "De ce volumul unei piramide este o treime din cel al prismei?", a: "Un cub poate fi descompus în trei piramide congruente cu baza pătrată: V = ⅓ · a² · h." },
        { q: "Ce unghi de înclinare are Marea Piramidă din Giza?", a: "Marea Piramidă are o pantă de circa 51,85°, asociată cu secțiunea de aur φ." }
      ]
    },
    proofs: {
      de: [
        { title: "Volumenbeweis der Pyramide", body: "Drei kongruente Pyramiden bilden einen Quader mit gleicher Grundfläche und Höhe: V = ⅓ · a² · h." },
        { title: "Seitenhöhe über den Satz des Pythagoras", body: "Höhe h, Basisapothema a/2 und Seitenhöhe s bilden ein rechtwinkliges Dreieck: Seitenhöhe s = √[h² + (a/2)²]." },
        { title: "Mantelfläche aus vier Dreiecken", body: "Mantelfläche = 4 × [½ · a · s] = 2 · a · s. Gesamte Oberfläche = a² + 2 · a · s." }
      ],
      es: [
        { title: "Demostración de volumen piramidal", body: "Tres pirámides congruentes componen un prisma recto: V = ⅓ · a² · h." },
        { title: "Apotema lateral mediante teorema de Pitágoras", body: "La altura h, el apotema de base a/2 y el apotema lateral s forman un triángulo rectángulo: s = √[h² + (a/2)²]." },
        { title: "Desarrollo de cuatro caras triangulares", body: "Área lateral = 4 × [½ · a · s] = 2 · a · s. Área Total = a² + 2 · a · s." }
      ],
      fr: [
        { title: "Démonstration du volume pyramidal", body: "Trois pyramides congruentes assemblent un prisme droit : V = ⅓ · a² · h." },
        { title: "Apothème latéral par Pythagore", body: "La hauteur h, le demi-côté a/2 et l'apothème s forment un triangle rectangle : s = √[h² + (a/2)²]." },
        { title: "Patron à quatre faces latérales", body: "Aire latérale = 4 × [½ · a · s] = 2 · a · s. Aire Totale = a² + 2 · a · s." }
      ],
      it: [
        { title: "Dimostrazione del volume della piramide", body: "Tre piramidi congruenti formano un prisma retto: V = ⅓ · a² · h." },
        { title: "Apotema laterale con il teorema di Pitagora", body: "L'altezza h, l'apotema di base a/2 e l'apotema s formano un triangolo rettangolo: s = √[h² + (a/2)²]." },
        { title: "Sviluppo di quattro facce triangolari", body: "Area laterale = 4 × [½ · a · s] = 2 · a · s. Area Totale = a² + 2 · a · s." }
      ],
      pt: [
        { title: "Demonstração de volume da pirâmide", body: "Três pirâmides congruentes formam um prisma reto: V = ⅓ · a² · h." },
        { title: "Apótema lateral pelo teorema de Pitágoras", body: "A altura h, a metade do lado a/2 e o apótema lateral s formam um triângulo retângulo: s = √[h² + (a/2)²]." },
        { title: "Área das quatro faces triangulares", body: "Área lateral = 4 × [½ · a · s] = 2 · a · s. Área Total = a² + 2 · a · s." }
      ],
      nl: [
        { title: "Volumebewijs piramide", body: "Drie congruente piramides vormen een prisma: V = ⅓ · a² · h." },
        { title: "Schuine hoogte via Pythagoras", body: "De hoogte h, basis-apothema a/2 en schuine hoogte s vormen een rechthoekige driehoek: s = √[h² + (a/2)²]." },
        { title: "Manteloppervlakte van vier driehoeken", body: "Manteloppervlakte = 4 × [½ · a · s] = 2 · a · s. Totale oppervlakte = a² + 2 · a · s." }
      ],
      pl: [
        { title: "Dowód na objętość ostrosłupa", body: "Trzy przystające ostrosłupy składają się w graniastosłup: V = ⅓ · a² · h." },
        { title: "Wysokość ściany bocznej z twierdzenia Pitagorasa", body: "Wysokość h, apotema podstawy a/2 i wysokość ściany s tworzą trójkąt prostokątny: s = √[h² + (a/2)²]." },
        { title: "Siatka czterech ścian bocznych", body: "Pole boczne = 4 × [½ · a · s] = 2 · a · s. Pole całkowite = a² + 2 · a · s." }
      ],
      sv: [
        { title: "Volymbevis för pyramid", body: "Tre kongruenta pyramider bygger upp ett prisma: V = ⅓ · a² · h." },
        { title: "Sidohöjd via Pythagoras sats", body: "Höjden h, basens apotema a/2 och sidohöjden s bildar en rätvinklig triangel: s = √[h² + (a/2)²]." },
        { title: "Fyra triangulära sidoytor", body: "Mantelyta = 4 × [½ · a · s] = 2 · a · s. Total area = a² + 2 · a · s." }
      ],
      no: [
        { title: "Volumbevis for pyramide", body: "Tre kongruente pyramider danner et prisme: V = ⅓ · a² · h." },
        { title: "Sidehøyde via Pytagoras' læresetning", body: "Høyden h, grunnflate-apotema a/2 og sidehøyden s danner en rettvinklet trekant: s = √[h² + (a/2)²]." },
        { title: "Fire trekantede sideflater", body: "Mantelflate = 4 × [½ · a · s] = 2 · a · s. Totalt areal = a² + 2 · a · s." }
      ],
      fi: [
        { title: "Pyramidin tilavuustodistus", body: "Kolme yhtenevää pyramidia muodostaa särmiön: V = ⅓ · a² · h." },
        { title: "Sivutahkon korkeus Pythagoraan lauseella", body: "Korkeus h, pohjan apoteema a/2 ja sivukorkeus s muodostavat suorakulmaisen kolmion: s = √[h² + (a/2)²]." },
        { title: "Neljän kolmiotahkon vaippa", body: "Vaipan ala = 4 × [½ · a · s] = 2 · a · s. Kokonaisala = a² + 2 · a · s." }
      ],
      ro: [
        { title: "Demonstrația volumului piramidei", body: "Trei piramide congruente alcătuiesc o prismă: V = ⅓ · a² · h." },
        { title: "Apotema piramidei prin Pitagora", body: "Înălțimea h, apotema bazei a/2 și apotema piramidei s formează un triunghi dreptunghic: s = √[h² + (a/2)²]." },
        { title: "Desfășurarea celor patru fețe laterale", body: "Aria laterală = 4 × [½ · a · s] = 2 · a · s. Aria Totală = a² + 2 · a · s." }
      ]
    }
  },

  "geometry/triangular-prism": {
    faqs: {
      de: [
        { q: "Was ist die optische Dispersion eines Glasprismas?", a: "Isaac Newton bewies 1666, dass ein dreiseitiges Glasprisma weißes Sonnenlicht nach dem Snelliusschen Brechungsgesetz in sein kontinuierliches Farbspektrum zerlegt." },
        { q: "Wie viele Ecken, Kanten und Flächen hat ein Dreiecksprisma?", a: "Ein Dreiecksprisma besitzt 5 Flächen (2 Dreiecke + 3 Rechtecke), 9 Kanten und 6 Ecken, womit der Eulersche Polyedersatz F - E + V = 5 - 9 + 6 = 2 erfüllt ist." }
      ],
      es: [
        { q: "¿Qué es la dispersión óptica en un prisma triangular?", a: "Isaac Newton demostró en 1666 que un prisma de vidrio refracta la luz blanca dividiéndola en su espectro de colores debido a la variación del índice de refracción según la longitud de onda." },
        { q: "¿Cuántos vértices, aristas y caras tiene un prisma triangular?", a: "Tiene 5 caras (2 bases triangulares + 3 caras laterales), 9 aristas y 6 vértices, satisfaciendo la fórmula de Euler: 5 - 9 + 6 = 2." }
      ],
      fr: [
        { q: "Qu'est-ce que la dispersion optique d'un prisme triangulaire ?", a: "Isaac Newton démontra en 1666 qu'un prisme réfracte la lumière blanche en un spectre continu de couleurs selon la loi de Snell-Descartes." },
        { q: "Combien de sommets, arêtes et faces possède un prisme triangulaire ?", a: "Il possède 5 faces (2 bases + 3 faces latérales), 9 arêtes et 6 sommets, respectant la formule d'Euler : 5 - 9 + 6 = 2." }
      ],
      it: [
        { q: "Cos'è la dispersione ottica di un prisma triangolare?", a: "Isaac Newton dimostrò nel 1666 che un prisma di vetro rifrange la luce bianca separandola nelle sue lunghezze d'onda." },
        { q: "Quanti vertici, spigoli e facce possiede un prisma triangolare?", a: "Possiede 5 facce (2 triangoli + 3 rettangoli), 9 spigoli e 6 vertici, verificando la relazione di Eulero: 5 - 9 + 6 = 2." }
      ],
      pt: [
        { q: "O que é a dispersão óptica em um prisma triangular?", a: "Isaac Newton provou em 1666 que um prisma de vidro dispersa a luz branca em seu espectro contínuo de cores." },
        { q: "Quantos vértices, arestas e faces tem um prisma triangular?", a: "Tem 5 faces (2 bases + 3 faces laterais), 9 arestas e 6 vértices, satisfazendo Euler: 5 - 9 + 6 = 2." }
      ],
      nl: [
        { q: "Wat is de optische dispersie van een prisma?", a: "Isaac Newton toonde in 1666 aan dat een glazen prisma wit zonlicht splitst in een continu kleurenspectrum." },
        { q: "Hoeveel hoekpunten, ribben en vlakken heeft een driehoekig prisma?", a: "Het heeft 5 vlakken, 9 ribben en 6 hoekpunten, waarmee aan de Euler-formule wordt voldaan: 5 - 9 + 6 = 2." }
      ],
      pl: [
        { q: "Czym jest dyspersja optyczna w pryzmacie trójkątnym?", a: "Isaac Newton udowodnił w 1666 r., że szklany pryzmat rozszczepia światło białe na ciągłe spektrum barw." },
        { q: "Ile wierzchołków, krawędzi i ścian ma graniastosłup trójkątny?", a: "Ma 5 ścian (2 podstawy + 3 ściany boczne), 9 krawędzi i 6 wierzchołków: 5 - 9 + 6 = 2." }
      ],
      sv: [
        { q: "Vad är optisk dispersion i ett glasprisma?", a: "Isaac Newton bevisade 1666 att ett prisma bryter vitt solljus till ett spektrum av färger enligt Snells lag." },
        { q: "Hur många hörn, kanter och sidor har ett tresidigt prisma?", a: "Ett tresidigt prisma har 5 sidor, 9 kanter och 6 hörn: 5 - 9 + 6 = 2." }
      ],
      no: [
        { q: "Hva er optisk dispersjon i et trefløyet prisme?", a: "Isaac Newton beviste i 1666 at et glassprisme bryter hvitt lys inn i fargespekteret." },
        { q: "Hvor mange hjørner, kanter og flater har et trekantet prisme?", a: "Det har 5 flater, 9 kanter og 6 hjørner: 5 - 9 + 6 = 2." }
      ],
      fi: [
        { q: "Mitä on optinen dispersio lasiprismassa?", a: "Isaac Newton osoitti vuonna 1666, että lasiprisma hajottaa valkoisen auringonvalon värispektriksi." },
        { q: "Kuinka monta kärkeä, särmää ja tahkoa kolmisärmiössä on?", a: "Särmiössä on 5 tahkoa, 9 särmää ja 6 kärkeä: 5 - 9 + 6 = 2." }
      ],
      ro: [
        { q: "Ce este dispersia optică a unei prisme triunghiulare?", a: "Isaac Newton a demonstrat în 1666 că o prismă refractă lumina albă descompunând-o în spectrul său de culori." },
        { q: "Câte vârfuri, muchii și fețe are o prismă triunghiulară?", a: "Are 5 fețe (2 triunghiuri + 3 dreptunghiuri), 9 muchii și 6 vârfuri: 5 - 9 + 6 = 2." }
      ]
    },
    proofs: {
      de: [
        { title: "Volumenextrusion gleichförmiger Querschnitte", body: "Das Volumen jedes geraden Prismas entspricht Grundfläche mal Länge: V = Fläche_Dreieck · L." },
        { title: "Fläche der drei Mantelflächen", body: "Mantelfläche = Umfang der Dreiecksgrundfläche multipliziert mit der Prismalänge: A_Mantel = (a + b + c) · L." },
        { title: "Gesamtes Prismennetz", body: "Gesamte Oberfläche = (2 × Fläche_Dreieck) + Mantelfläche." }
      ],
      es: [
        { title: "Extrusión volumétrica de sección uniforme", body: "El volumen de cualquier prisma recto es el producto de su base triangular por su longitud: V = Área_base · L." },
        { title: "Área de paredes laterales", body: "Área lateral = perímetro de la base triangular por la longitud: A_lat = (a + b + c) · L." },
        { title: "Superficie total cerrada", body: "Área Total = (2 × Área_base) + Área_lateral." }
      ],
      fr: [
        { title: "Extrusion volumique de section uniforme", body: "Le volume de tout prisme droit est le produit de sa base par sa longueur : V = Aire_base · L." },
        { title: "Aire des faces latérales", body: "Aire latérale = périmètre du triangle de base multiplié par la longueur : A_lat = (a + b + c) · L." },
        { title: "Patron complet fermé", body: "Aire Totale = (2 × Aire_base) + Aire_latérale." }
      ],
      it: [
        { title: "Estrusione volumetrica a sezione uniforme", body: "Il volume di un prisma retto è dato dall'area del triangolo di base per la lunghezza: V = Area_base · L." },
        { title: "Area delle pareti laterali", body: "Area laterale = perimetro di base per la lunghezza: A_lat = (a + b + c) · L." },
        { title: "Superficie totale chiusa", body: "Area Totale = (2 × Area_base) + Area_laterale." }
      ],
      pt: [
        { title: "Extrusão volumétrica de seção uniforme", body: "O volume de qualquer prisma reto é a área da base multiplicada pelo comprimento: V = Área_base · L." },
        { title: "Área das faces laterais", body: "Área lateral = perímetro da base triangular multiplicado pelo comprimento: A_lat = (a + b + c) · L." },
        { title: "Área total", body: "Área Total = (2 × Área_base) + Área_lateral." }
      ],
      nl: [
        { title: "Uniforme doorsnede-extrusie", body: "Het volume van elk recht prisma is het product van het grondvlak en de lengte: V = Oppervlakte_basis · L." },
        { title: "Oppervlakte van zijwanden", body: "Manteloppervlakte = omtrek van de driehoek maal de lengte: A_mantel = (a + b + c) · L." },
        { title: "Totale uitslag", body: "Totale oppervlakte = (2 × Oppervlakte_basis) + Manteloppervlakte." }
      ],
      pl: [
        { title: "Ekstruzja objętościowa o stałym przekroju", body: "Objętość każdego graniastosłupa prostego równa się polu podstawy pomnożonemu przez długość: V = Pole_podstawy · L." },
        { title: "Pole ścian bocznych", body: "Pole boczne = obwód podstawy trójkątnej pomnożony przez długość: A_boczne = (a + b + c) · L." },
        { title: "Pole powierzchni całkowitej", body: "Pole całkowite = (2 × Pole_podstawy) + Pole_boczne." }
      ],
      sv: [
        { title: "Volymextrudering av likformigt tvärsnitt", body: "Volymen av ett rätvinkligt prisma är basytans area gånger längden: V = Basarea · L." },
        { title: "Mantelyta", body: "Mantelyta = basens omkrets multiplicerad med längden: A_mantel = (a + b + c) · L." },
        { title: "Total innesluten yta", body: "Total area = (2 × Basarea) + Mantelyta." }
      ],
      no: [
        { title: "Volumekstrudering av jevnt tverrsnitt", body: "Volumet av et rett prisme er grunnflatens areal multiplisert med lengden: V = Grunnflate · L." },
        { title: "Mantelflatens areal", body: "Mantelflate = grunnflatens omkrets multiplisert med lengden: A_mantel = (a + b + c) · L." },
        { title: "Totalt overflateareal", body: "Totalt areal = (2 × Grunnflate) + Mantelflate." }
      ],
      fi: [
        { title: "Tasaisen poikkileikkauksen tilavuus", body: "Suoran särmiön tilavuus on pohjakolmion pinta-ala kerrottuna pituudella: V = Pohjan_ala · L." },
        { title: "Vaipan seinämien pinta-ala", body: "Vaipan ala = pohjakolmion piiri kerrottuna pituudella: A_vaippa = (a + b + c) · L." },
        { title: "Kokonaispinta-ala", body: "Kokonaisala = (2 × Pohjan_ala) + Vaipan_ala." }
      ],
      ro: [
        { title: "Extrudarea volumetrică a secțiunii uniforme", body: "Volumul oricărei prisme drepte este produsul ariei bazei cu lungimea: V = Arie_bază · L." },
        { title: "Aria fețelor laterale", body: "Aria laterală = perimetrul bazei triunghiulare înmulțit cu lungimea: A_laterală = (a + b + c) · L." },
        { title: "Aria totală a prismei", body: "Aria Totală = (2 × Arie_bază) + Aria_laterală." }
      ]
    }
  },

  "geometry/frustum-cone": {
    faqs: {
      de: [
        { q: "Welche Alltagsgegenstände haben die Form eines Kegelstumpfes?", a: "Kaffeebecher, Eimer, Lampenschirme, Pflanztöpfe und industrielle Kühltürme von Kraftwerken nutzen die Form eines Kegelstumpfes." },
        { q: "Wie verhält sich das Volumen im Vergleich zu einem einfachen Zylinder?", a: "Ein Zylinder mit dem mittleren Radius r_mittel = (R + r)/2 unterschätzt das wahre Kegelstumpfvolumen, da der Term (R² + Rr + r²)/3 quadratisch gewichtet ist." }
      ],
      es: [
        { q: "¿Qué objetos cotidianos tienen forma de tronco de cono?", a: "Cubos, vasos de café de papel, pantallas de lámparas, macetas y torres de refrigeración de centrales eléctricas." },
        { q: "¿Cómo se compara el volumen de un tronco con un cilindro simple?", a: "Un cilindro con radio promedio r_med = (R + r)/2 subestima el volumen real del tronco de cono, cuya fórmula exacta es V = ⅓ · π · h · (R² + Rr + r²)." }
      ],
      fr: [
        { q: "Quels objets du quotidien ont la forme d'un tronc de cône ?", a: "Les seaux, gobelets en carton, abat-jour, pots de fleurs et tours de refroidissement industrielles." },
        { q: "Comment le volume d'un tronc se compare-t-il à un cylindre simple ?", a: "Un cylindre de rayon moyen r_moyen = (R + r)/2 sous-estime le volume réel du tronc de cône donné par V = ⅓ · π · h · (R² + Rr + r²)." }
      ],
      it: [
        { q: "Quali oggetti quotidiani hanno la forma di un tronco di cono?", a: "Secchi, bicchieri di carta, paralumi, vasi per piante e torri di raffreddamento industriali." },
        { q: "Come si confronta il volume di un tronco rispetto a un cilindro?", a: "Un cilindro con raggio medio r_medio = (R + r)/2 sottostima il volume reale del tronco di cono: V = ⅓ · π · h · (R² + Rr + r²)." }
      ],
      pt: [
        { q: "Quais objetos cotidianos têm a forma de um tronco de cone?", a: "Baldes, copos de café, cúpulas de abajur, vasos de plantas e torres de resfriamento industriais." },
        { q: "Como o volume de um tronco se compara a um cilindro simples?", a: "Um cilindro com raio médio subestima o volume real do tronco de cone dado por V = ⅓ · π · h · (R² + Rr + r²)." }
      ],
      nl: [
        { q: "Welke alledaagse voorwerpen hebben de vorm van een afgeknotte kegel?", a: "Emmers, papieren koffiebekers, lampenkappen, bloempotten en industriële koeltorens." },
        { q: "Hoe verhoudt het volume zich tot een eenvoudige cilinder?", a: "Een cilinder met gemiddelde straal onderschat het werkelijke volume: V = ⅓ · π · h · (R² + Rr + r²)." }
      ],
      pl: [
        { q: "Jakie przedmioty codziennego użytku mają kształt stożka ściętego?", a: "Wiadra, papierowe kubki do kawy, abażury, donice oraz chłodnie kominowe elektrowni." },
        { q: "Jak ma się objętość stożka ściętego do zwykłego walca?", a: "Walec o średnim promieniu zaniża rzeczywistą objętość stożka ściętego: V = ⅓ · π · h · (R² + Rr + r²)." }
      ],
      sv: [
        { q: "Vilka vardagsföremål har formen av en stympad kon?", a: "Hinkar, kaffekoppar, lampskärmar, blomkrukor och industriella kyltorn." },
        { q: "Hur förhåller sig volymen till en vanlig cylinder?", a: "En cylinder med medelradie underskattar den verkliga volymen: V = ⅓ · π · h · (R² + Rr + r²)." }
      ],
      no: [
        { q: "Hvilke hverdagsgjenstander har form som en avkortet kjegle?", a: "Bøtter, kaffekopper, lampeskjermer, blomsterpotter og kjøletårn." },
        { q: "Hvordan er volumet sammenlignet med en enkel sylinder?", a: "En sylinder med gjennomsnittsradius underestimerer det virkelige volumet: V = ⅓ · π · h · (R² + Rr + r²)." }
      ],
      fi: [
        { q: "Mitä arkipäivän esineitä on katkaistun kartion muotoisia?", a: "Ämpärit, paperikupit, lampunvarjostimet, kukkaruukut ja jäähdytystornit." },
        { q: "Miten katkaistun kartion tilavuus vertautuu lieriöön?", a: "Keskisäteellä laskettu lieriö aliarvioi tarkan tilavuuden: V = ⅓ · π · h · (R² + Rr + r²)." }
      ],
      ro: [
        { q: "Ce obiecte cotidiene au forma unui trunchi de con?", a: "Găleți, pahare de cafea din carton, abajururi, ghivece de flori și turnuri de răcire industriale." },
        { q: "Cum se compară volumul unui trunchi de con cu un cilindru simplu?", a: "Un cilindru cu raza medie subestimează volumul real al trunchiului: V = ⅓ · π · h · (R² + Rr + r²)." }
      ]
    },
    proofs: {
      de: [
        { title: "Subtraktive Kegel-Infinitesimalrechnung", body: "Ein Kegelstumpf entsteht durch Subtraktion eines kleinen Kegels der Höhe h₁ von einem großen Kegel der Höhe (h₁ + h): V = ⅓ · π · h · (R² + Rr + r²)." },
        { title: "Pythagoreische Beziehung der Mantellinie", body: "Die Differenz der Radien (R - r) bildet mit der Höhe h ein rechtwinkliges Dreieck: s = √[h² + (R - r)²]." },
        { title: "Mantelfläche als Sektordifferenz", body: "Mantelfläche A_Mantel = π(R + r)s. Gesamtoberfläche = A_Mantel + πR² + πr²." }
      ],
      es: [
        { title: "Cálculo sustractivo cónico", body: "Un tronco se forma restando un cono pequeño de uno completo: V = ⅓ · π · h · (R² + Rr + r²)." },
        { title: "Relación pitagórica de la generatriz", body: "La diferencia de radios (R - r) con la altura forma un triángulo rectángulo: s = √[h² + (R - r)²]." },
        { title: "Diferencia de sectores para el área lateral", body: "Área lateral A_lat = π(R + r)s. Área Total = A_lat + πR² + πr²." }
      ],
      fr: [
        { title: "Calcul soustractif conique", body: "Un tronc est obtenu en soustrayant un petit cône d'un grand cône : V = ⅓ · π · h · (R² + Rr + r²)." },
        { title: "Relation pythagoricienne de la génératrice", body: "La différence de rayons (R - r) avec la hauteur forme un triangle rectangle : s = √[h² + (R - r)²]." },
        { title: "Aire latérale", body: "Aire latérale A_lat = π(R + r)s. Aire Totale = A_lat + πR² + πr²." }
      ],
      it: [
        { title: "Calcolo sottrattivo conico", body: "Un tronco si ottiene sottraendo un cono piccolo da uno grande: V = ⅓ · π · h · (R² + Rr + r²)." },
        { title: "Relazione pitagorica dell'apotema", body: "La differenza dei raggi (R - r) con l'altezza forma un triangolo rettangolo: s = √[h² + (R - r)²]." },
        { title: "Area laterale", body: "Area laterale A_lat = π(R + r)s. Area Totale = A_lat + πR² + πr²." }
      ],
      pt: [
        { title: "Cálculo subtrativo cônico", body: "Um tronco é formado pela subtração de um cone menor de um cone maior: V = ⅓ · π · h · (R² + Rr + r²)." },
        { title: "Relação pitagórica da geratriz", body: "A diferença de raios (R - r) e a altura formam um triângulo retângulo: s = √[h² + (R - r)²]." },
        { title: "Área lateral", body: "Área lateral A_lat = π(R + r)s. Área Total = A_lat + πR² + πr²." }
      ],
      nl: [
        { title: "Subtractieve kegelberekening", body: "Een afgeknotte kegel ontstaat door een kleine kegel af te trekken van een grote: V = ⅓ · π · h · (R² + Rr + r²)." },
        { title: "Pythagorese schuine zijde", body: "Het verschil in stralen (R - r) vormt met de hoogte een rechthoekige driehoek: s = √[h² + (R - r)²]." },
        { title: "Manteloppervlakte", body: "Manteloppervlakte A_mantel = π(R + r)s. Totale oppervlakte = A_mantel + πR² + πr²." }
      ],
      pl: [
        { title: "Subtraktywne wyprowadzenie całkowe", body: "Stożek ścięty powstaje przez odcięcie małego stożka od stożka wyjściowego: V = ⅓ · π · h · (R² + Rr + r²)." },
        { title: "Pitagorejska relacja tworzącej", body: "Różnica promieni (R - r) wraz z wysokością tworzy trójkąt prostokątny: s = √[h² + (R - r)²]." },
        { title: "Pole powierzchni bocznej", body: "Pole boczne A_boczne = π(R + r)s. Pole całkowite = A_boczne + πR² + πr²." }
      ],
      sv: [
        { title: "Subtraktiv konisk kalkyl", body: "En stympad kon bildas genom att subtrahera en liten kon från en stor kon: V = ⅓ · π · h · (R² + Rr + r²)." },
        { title: "Pythagoreisk sidohöjdsrelation", body: "Radieskillnaden (R - r) och höjden bildar en rätvinklig triangel: s = √[h² + (R - r)²]." },
        { title: "Mantelyta", body: "Mantelyta A_mantel = π(R + r)s. Total area = A_mantel + πR² + πr²." }
      ],
      no: [
        { title: "Subtraktiv kjeglekalkyle", body: "En avkortet kjegle dannes ved å trekke en liten kjegle fra en stor kjegle: V = ⅓ · π · h · (R² + Rr + r²)." },
        { title: "Pytagoreisk sidehøyderelasjon", body: "Radieforskjellen (R - r) danner med høyden en rettvinklet trekant: s = √[h² + (R - r)²]." },
        { title: "Mantelflate", body: "Mantelflate A_mantel = π(R + r)s. Totalt areal = A_mantel + πR² + πr²." }
      ],
      fi: [
        { title: "Katkaistun kartion tilavuuden johto", body: "Katkaistu kartio saadaan vähentämällä pieni kartio suuresta kartiosta: V = ⅓ · π · h · (R² + Rr + r²)." },
        { title: "Sivujanan Pythagoraan yhteys", body: "Säteiden erotus (R - r) muodostaa korkeuden kanssa suorakulmaisen kolmion: s = √[h² + (R - r)²]." },
        { title: "Vaipan pinta-ala", body: "Vaipan ala A_vaippa = π(R + r)s. Kokonaisala = A_vaippa + πR² + πr²." }
      ],
      ro: [
        { title: "Calculul substractiv al trunchiului de con", body: "Un trunchi de con se obține scăzând un con mic dintr-un con mare: V = ⅓ · π · h · (R² + Rr + r²)." },
        { title: "Relația pitagoreică a generatoarei", body: "Diferența razelor (R - r) formează cu înălțimea un triunghi dreptunghic: s = √[h² + (R - r)²]." },
        { title: "Aria laterală", body: "Aria laterală A_lat = π(R + r)s. Aria Totală = A_lat + πR² + πr²." }
      ]
    }
  },

  "geometry/frustum-pyramid": {
    faqs: {
      de: [
        { q: "Warum ist Aufgabe 14 des Papyrus Moskau historisch so bedeutend?", a: "Aufgabe 14 des altägyptischen Papyrus Moskau (ca. 1850 v. Chr.) liefert den ältesten bekannten Beweis für die exakte Pyramidenstumpfformel: V = ⅓ · h · (a² + ab + b²)." },
        { q: "Welche Bauwerke nutzen die Form eines Pyramidenstumpfes?", a: "Mesoamerikanische Stufenpyramiden (wie in Chichén Itzá), Sockelbauwerke und Stützmauern im Erdbau." }
      ],
      es: [
        { q: "¿Por qué el Problema 14 del Papiro de Moscú es tan importante?", a: "Datan del 1850 a.C. y contiene la demostración más antigua de la fórmula exacta del tronco de pirámide: V = ⅓ · h · (a² + ab + b²)." },
        { q: "¿Qué estructuras utilizan pirámides truncadas?", a: "Pirámides escalonadas mesoamericanas (como El Castillo en Chichén Itzá), pedestales de monumentos y cimentaciones." }
      ],
      fr: [
        { q: "Pourquoi le problème 14 du papyrus de Moscou est-il si célèbre ?", a: "Datant de 1850 av. J.-C., il présente la formule exacte du tronc de pyramide : V = ⅓ · h · (a² + ab + b²)." },
        { q: "Quelles structures utilisent un tronc de pyramide ?", a: "Les pyramides à degrés précolombiennes, les socles architecturaux et les massifs de fondation." }
      ],
      it: [
        { q: "Perché il Problema 14 del Papiro di Mosca è così celebre?", a: "Risalente al 1850 a.C., attesta la prima formulazione esatta del tronco di piramide: V = ⅓ · h · (a² + ab + b²)." },
        { q: "Quali strutture adottano la forma di tronco di piramide?", a: "Le piramidi a gradoni mesoamericane, basamenti e plinti di fondazione nell'ingegneria civile." }
      ],
      pt: [
        { q: "Por que o Problema 14 do Papiro de Moscou é histórico?", a: "Datado de 1850 a.C., contém a mais antiga fórmula exata do tronco de pirâmide: V = ⅓ · h · (a² + ab + b²)." },
        { q: "Quais construções usam pirâmides truncadas?", a: "Pirâmides em degraus pré-colombianas, pedestais e fundações de engenharia civil." }
      ],
      nl: [
        { q: "Waarom is probleem 14 van de Moskou-papyrus zo beroemd?", a: "Het dateert uit 1850 v.Chr. en bevat de oudste exacte formule voor een afgeknotte piramide: V = ⅓ · h · (a² + ab + b²)." },
        { q: "Welke bouwwerken hebben de vorm van een afgeknotte piramide?", a: "Meso-Amerikaanse trappiramides, sokkels en civieltechnische funderingen." }
      ],
      pl: [
        { q: "Dlaczego Zadanie 14 z Papirusu Moskiewskiego jest historyczne?", a: "Zredagowane ok. 1850 r. p.n.e. zawiera najstarszy znany poprawny wzór na objętość ostrosłupa ściętego: V = ⅓ · h · (a² + ab + b²)." },
        { q: "Jakie budowle mają kształt ostrosłupa ściętego?", a: "Mezoamerykańskie piramidy schodkowe, cokoły pomników i fundamenty budowlane." }
      ],
      sv: [
        { q: "Varför är problem 14 i Moskvapapyrusen historiskt berömt?", a: "Det härstammar från 1850 f.Kr. och innehåller det äldsta beviset för den stympade pyramidens volymformel: V = ⅓ · h · (a² + ab + b²)." },
        { q: "Vilka byggnadsverk använder stympade pyramider?", a: "Mesoamerikanska trappstegspyramider, fundament och maskinsocklar." }
      ],
      no: [
        { q: "Hvorfor er problem 14 i Moskva-papyrusen historisk viktig?", a: "Det dateres til 1850 f.Kr. og inneholder verdens eldste nøyaktige formel for avkortet pyramide: V = ⅓ · h · (a² + ab + b²)." },
        { q: "Hvilke konstruksjoner bruker avkortede pyramider?", a: "Mesoamerikanske trappepyramider, sokler og fundamenter." }
      ],
      fi: [
        { q: "Miksi Moskovan papyruksen tehtävä 14 on historiallinen?", a: "Se on peräisin vuodelta 1850 eKr. ja sisältää vanhimman tunnetun tarkan kaavan katkaistulle pyramidille: V = ⅓ · h · (a² + ab + b²)." },
        { q: "Missä rakennelmissa käytetään katkaistua pyramidia?", a: "Mesoamerikan porraspyramideissa, jalustoissa ja maarakennuksen perustuksissa." }
      ],
      ro: [
        { q: "De ce este Problema 14 din Papirusul din Moscova istorică?", a: "Datând din 1850 î.Hr., conține cea mai veche formulă exactă a trunchiului de piramidă: V = ⅓ · h · (a² + ab + b²)." },
        { q: "Ce construcții au forma de trunchi de piramidă?", a: "Piramidele în trepte mezoamericane, soclurile de monumente și fundațiile de inginerie civilă." }
      ]
    },
    proofs: {
      de: [
        { title: "Der Papyrus Moskau (Aufgabe 14)", body: "Die altägyptische Herleitung beweist: V = ⅓ · h · (a² + a·b + b²)." },
        { title: "Geometrisches Mittel der Schnittflächen", body: "Für jeden Pyramidenstumpf mit Grundflächen A₁ und A₂ gilt: V = ⅓ · h · (A₁ + √(A₁A₂) + A₂)." },
        { title: "Trapezförmige Seitenflächen", body: "Jede der vier Seitenflächen ist ein gleichschenkliges Trapez: A_Mantel = 2(a + b) · s_seite. Gesamtoberfläche = A_Mantel + a² + b²." }
      ],
      es: [
        { title: "El Papiro Matemático de Moscú (Problema 14)", body: "La derivación egipcia demuestra: V = ⅓ · h · (a² + a·b + b²)." },
        { title: "Media geométrica de áreas de base", body: "Para cualquier tronco de pirámide con bases A₁ y A₂: V = ⅓ · h · (A₁ + √(A₁A₂) + A₂)." },
        { title: "Caras laterales trapezoidales", body: "Las 4 caras laterales son trapecios isósceles: Área lateral = 2(a + b) · s. Área Total = A_lat + a² + b²." }
      ],
      fr: [
        { title: "Le Papyrus de Moscou (Problème 14)", body: "La dérivation égyptienne antique prouve que : V = ⅓ · h · (a² + a·b + b²)." },
        { title: "Moyenne géométrique des bases", body: "Pour tout tronc de pyramide de bases A₁ et A₂ : V = ⅓ · h · (A₁ + √(A₁A₂) + A₂)." },
        { title: "Faces latérales trapézoïdales", body: "Chacune des quatre faces est un trapèze isocèle : Aire latérale = 2(a + b) · s. Aire Totale = A_lat + a² + b²." }
      ],
      it: [
        { title: "Il Papiro di Mosca (Problema 14)", body: "L'antica derivazione egizia dimostra: V = ⅓ · h · (a² + a·b + b²)." },
        { title: "Media geometrica delle sezioni di base", body: "Per qualsiasi tronco di piramide con basi A₁ e A₂: V = ⅓ · h · (A₁ + √(A₁A₂) + A₂)." },
        { title: "Facce laterali trapezoidali", body: "Ciascuna delle 4 facce è un trapezio isoscele: Area laterale = 2(a + b) · s. Area Totale = A_lat + a² + b²." }
      ],
      pt: [
        { title: "O Papiro de Moscou (Problema 14)", body: "A dedução egípcia comprova que: V = ⅓ · h · (a² + a·b + b²)." },
        { title: "Média geométrica das bases", body: "Para qualquer tronco de pirâmide: V = ⅓ · h · (A₁ + √(A₁A₂) + A₂)." },
        { title: "Faces laterais trapezoidais", body: "Cada face lateral é um trapézio isósceles: Área lateral = 2(a + b) · s. Área Total = A_lat + a² + b²." }
      ],
      nl: [
        { title: "De Moskou-papyrus (Probleem 14)", body: "Het oud-Egyptische bewijs toont aan: V = ⅓ · h · (a² + a·b + b²)." },
        { title: "Meetkundig gemiddelde van de grondvlakken", body: "Voor elke afgeknotte piramide: V = ⅓ · h · (A₁ + √(A₁A₂) + A₂)." },
        { title: "Trapeziumvormige zijvlakken", body: "Elk van de 4 zijvlakken is een gelijkbenig trapezium: A_mantel = 2(a + b) · s. Totale oppervlakte = A_mantel + a² + b²." }
      ],
      pl: [
        { title: "Papirus Moskiewski (Zadanie 14)", body: "Egipskie wyprowadzenie dowodzi: V = ⅓ · h · (a² + a·b + b²)." },
        { title: "Średnia geometryczna pól podstaw", body: "Dla dowolnego ostrosłupa ściętego: V = ⅓ · h · (A₁ + √(A₁A₂) + A₂)." },
        { title: "Trapezowe ściany boczne", body: "Każda z 4 ścian bocznych jest trapezem równoramiennym: A_boczne = 2(a + b) · s. Pole całkowite = A_boczne + a² + b²." }
      ],
      sv: [
        { title: "Moskvapapyrusen (Problem 14)", body: "Den fornegyptiska härledningen visar: V = ⅓ · h · (a² + a·b + b²)." },
        { title: "Geometriskt medelvärde av basytorna", body: "För varje stympad pyramid gäller: V = ⅓ · h · (A₁ + √(A₁A₂) + A₂)." },
        { title: "Trapetsformade sidoytor", body: "De fyra sidoytorna är likbenta trapets: A_mantel = 2(a + b) · s. Total area = A_mantel + a² + b²." }
      ],
      no: [
        { title: "Moskva-papyrusen (Problem 14)", body: "Den gammelengelske utledningen viser: V = ⅓ · h · (a² + a·b + b²)." },
        { title: "Geometrisk gjennomsnitt av grunnflatene", body: "For enhver avkortet pyramide: V = ⅓ · h · (A₁ + √(A₁A₂) + A₂)." },
        { title: "Trapesformede sideflater", body: "De fire sideflatene er likebeinte trapes: A_mantel = 2(a + b) · s. Totalt areal = A_mantel + a² + b²." }
      ],
      fi: [
        { title: "Moskovan papyrus (Tehtävä 14)", body: "Muinainen egyptiläinen johto osoittaa: V = ⅓ · h · (a² + a·b + b²)." },
        { title: "Pohjapintojen geometrinen keskiarvo", body: "Katkaistulle pyramidille: V = ⅓ · h · (A₁ + √(A₁A₂) + A₂)." },
        { title: "Puolisuunnikkaan muotoiset sivutahkot", body: "Sivutahkot ovat tasakylkisiä puolisuunnikkaita: A_vaippa = 2(a + b) · s. Kokonaisala = A_vaippa + a² + b²." }
      ],
      ro: [
        { title: "Papirusul din Moscova (Problema 14)", body: "Deducerea egipteană antică demonstrează: V = ⅓ · h · (a² + a·b + b²)." },
        { title: "Media geometrică a ariilor bazelor", body: "Pentru orice trunchi de piramidă: V = ⅓ · h · (A₁ + √(A₁A₂) + A₂)." },
        { title: "Fețe laterale trapezoidale", body: "Cele 4 fețe sunt trapeze isoscele: A_laterală = 2(a + b) · s. Aria Totală = A_lat + a² + b²." }
      ]
    }
  },

  "geometry/3d/concrete-volume": {
    faqs: {
      de: [
        { q: "Wie berechnet man das Betonvolumen für eine Bodenplatte?", a: "Alle Maße in Meter umrechnen und multiplizieren: Volumen (m³) = Länge (m) × Breite (m) × Dicke (m). Für den angloamerikanischen Raum gilt: Kubikyards = (Länge_ft × Breite_ft × Tiefe_in / 12) / 27." },
        { q: "Was ist die Standarddicke einer Betonplatte?", a: "Standard-Gehwege und Terrassen werden mit 10 cm (4 Zoll) Dicke gegossen. Einfahrten für Pkw betragen üblicherweise 10 bis 12,5 cm (4-5 Zoll) mit Bewehrung; Lkw-Stellflächen 15 cm oder mehr." },
        { q: "Wie viele Fertigbetonsäcke benötigt man pro Kubikmeter?", a: "Ein typischer 25-kg-Sack Trockenbeton ergibt ca. 12 Liter Frischbeton. Für einen Kubikmeter (1000 Liter) benötigt man ca. 80 bis 84 Säcke à 25 kg." },
        { q: "Wie viel wiegt ein Kubikmeter Beton?", a: "Normalbeton wiegt ca. 2.400 kg (2,4 Tonnen) pro Kubikmeter, weshalb größere Mengen stets im Transportbetonmischer geliefert werden." }
      ],
      es: [
        { q: "¿Cómo se calcula el volumen de hormigón para una losa?", a: "Multiplique Largo × Ancho × Espesor en metros para obtener metros cúbicos (m³): Volumen = L × W × H. Para yardas cúbicas: (L_pies × W_pies × Prof_pulg / 12) / 27." },
        { q: "¿Cuál es el espesor estándar de una losa de hormigón?", a: "Aceras y patios residenciales estándar se vierten a 10 cm (4 pulgadas). Accesos vehiculares suelen tener de 10 a 12,5 cm con mallazo, y áreas de tráfico pesado 15 cm o más." },
        { q: "¿Cuántos sacos de hormigón premoldeado equivalen a 1 metro cúbico?", a: "Un saco estándar de 25 kg rinde unos 12 litros de hormigón fresco; se necesitan aproximadamente 83 sacos para completar 1 m³." },
        { q: "¿Cuánto pesa un metro cúbico de hormigón?", a: "El hormigón de peso normal pesa aproximadamente 2.400 kg (2,4 toneladas) por metro cúbico." }
      ],
      fr: [
        { q: "Comment calcule-t-on le volume de béton pour une dalle ?", a: "Multipliez Longueur × Largeur × Épaisseur en mètres pour obtenir le volume en m³ : V = L × l × e." },
        { q: "Quelle est l'épaisseur standard d'une dalle en béton ?", a: "Les allées piétonnes et terrasses font généralement 10 cm (4 pouces). Les allées pour voitures font de 10 à 12,5 cm armées, et les aires de stationnement pour poids lourds 15 cm ou plus." },
        { q: "Combien de sacs de béton prêt à l'emploi font 1 mètre cube ?", a: "Un sac de 25 kg donne environ 12 litres de béton frais ; il faut environ 83 sacs de 25 kg pour 1 m³." },
        { q: "Combien pèse un mètre cube de béton ?", a: "Le béton standard pèse environ 2 400 kg (2,4 tonnes) par mètre cube." }
      ],
      it: [
        { q: "Come si calcola il volume di calcestruzzo per una soletta?", a: "Moltiplicare Lunghezza × Larghezza × Spessore in metri per ottenere i metri cubi (m³): Volume = L × L × S." },
        { q: "Qual è lo spessore standard di una soletta in calcestruzzo?", a: "Marciapiedi e patii residenziali sono colati a 10 cm (4 pollici). I passi carrai sono tipicamente spessi 10-12,5 cm armati, e le aree per carichi pesanti 15 cm o più." },
        { q: "Quanti sacchi di premiscelato servono per 1 metro cubo?", a: "Un sacco da 25 kg produce circa 12 litri di calcestruzzo; occorrono circa 83 sacchi da 25 kg per 1 m³." },
        { q: "Quanto pesa un metro cubo di calcestruzzo?", a: "Il calcestruzzo normale pesa circa 2.400 kg (2,4 tonnellate) per metro cubo." }
      ],
      pt: [
        { q: "Como calcular o volume de concreto para uma laje?", a: "Multiplique Comprimento × Largura × Espessura em metros para obter metros cúbicos (m³): Volume = C × L × E." },
        { q: "Qual a espessura padrão de uma laje ou calçada de concreto?", a: "Passeios e pátios são concretados com 10 cm (4 polegadas). Garagens exigem 10 a 12,5 cm com malha de aço, e áreas de caminhões 15 cm ou mais." },
        { q: "Quantos sacos de concreto pronto equivalem a 1 metro cúbico?", a: "Um saco de 25 kg rende aproximadamente 12 litros de concreto misturado; são necessários cerca de 83 sacos para 1 m³." },
        { q: "Quanto pesa um metro cúbico de concreto?", a: "O concreto convencional pesa cerca de 2.400 kg (2,4 toneladas) por metro cúbico." }
      ],
      nl: [
        { q: "Hoe bereken je de hoeveelheid beton voor een vloer?", a: "Vermenigvuldig Lengte × Breedte × Dikte in meters voor kubieke meters (m³): Volume = L × B × D." },
        { q: "Wat is de standaarddikte van een betonvloer?", a: "Tuinpaden en terrassen worden doorgaans 10 cm dik gestort. Opritten voor personenauto's zijn 10 tot 12,5 cm gewapend; voor zwaar verkeer 15 cm of meer." },
        { q: "Hoeveel zakken kant-en-klaar beton gaan er in 1 m³?", a: "Een zak van 25 kg levert circa 12 liter specie op; er zijn circa 83 zakken nodig voor 1 kubieke meter." },
        { q: "Wat weegt een kubieke meter beton?", a: "Normaal beton weegt circa 2.400 kg (2,4 ton) per kubieke meter." }
      ],
      pl: [
        { q: "Jak obliczyć objętość betonu na płytę fundamentową lub posadzkę?", a: "Pomnóż Długość × Szerokość × Grubość w metrach, aby otrzymać metry sześcienne (m³): V = Dł × Szer × Gr." },
        { q: "Jaka jest standardowa grubość płyty betonowej?", a: "Chodniki i tarasy wylewa się na grubość 10 cm. Podjazdy samochodowe mają zwykle 10-12,5 cm ze zbrojeniem, a parkingi dla pojazdów ciężarowych 15 cm lub więcej." },
        { q: "Ile worków gotowego betonu potrzeba na 1 m³?", a: "Worek 25 kg daje około 12 litrów zaprawy; na 1 m³ potrzeba około 83 worków 25 kg." },
        { q: "Ile waży metr sześcienny betonu?", a: "Beton zwykły waży około 2 400 kg (2,4 tony) na metr sześcienny." }
      ],
      sv: [
        { q: "Hur beräknar man betongvolym för en platta?", a: "Multiplicera Längd × Bredd × Tjocklek i meter för kubikmeter (m³): Volym = L × B × T." },
        { q: "Vilken är standardtjockleken för en betongplatta?", a: "Gångar och uteplatser gjuts vanligen med 10 cm tjocklek. Garageuppfarter är 10-12,5 cm armerade och ytor för tunga fordon 15 cm eller mer." },
        { q: "Hur många säckar grovbetong motsvarar 1 kubikmeter?", a: "En säck om 25 kg ger cirka 12 liter betong; det krävs cirka 83 säckar för 1 m³." },
        { q: "Vad väger en kubikmeter betong?", a: "Normalbetong väger cirka 2 400 kg (2,4 ton) per kubikmeter." }
      ],
      no: [
        { q: "Hvordan beregner man betongvolum for en støpt plate?", a: "Multipliser Lengde × Bredde × Tykkelse i meter for kubikkmeter (m³): Volum = L × B × T." },
        { q: "Hva er standardtykkelsen på et betongdekke?", a: "Gangveier og terrasser støpes normalt 10 cm tykke. Innkjørsler er 10-12,5 cm armert, og plasser for tunge kjøretøy 15 cm eller mer." },
        { q: "Hvor mange sekker tørrmørtel trengs per kubikkmeter?", a: "En 25 kg sekk gir omtrent 12 liter ferdig betong; det trengs ca. 83 sekker for 1 m³." },
        { q: "Hva veier en kubikkmeter betong?", a: "Normalbetong veier cirka 2 400 kg (2,4 tonn) per kubikkmeter." }
      ],
      fi: [
        { q: "Miten lasketaan betonilaatan tilavuus?", a: "Kerro Pituus × Leveys × Paksuus metreinä saadaksesi kuutiometrit (m³): Tilavuus = P × L × K." },
        { q: "Mikä on betonilaatan vakiopaksuus?", a: "Kävelytiet ja terassit valetaan 10 cm paksuisiksi. Autotallit ja pihatiet vaativat 10-12,5 cm raudoitettuna, raskaat ajoneuvot vähintään 15 cm." },
        { q: "Kuinka monta säkkiä kuivabetonia tarvitaan kuutiometriin?", a: "Yksi 25 kg säkki tuottaa noin 12 litraa valmista massaa; yhteen kuutiometriin tarvitaan noin 83 säkkiä." },
        { q: "Paljonko kuutiometri betonia painaa?", a: "Normaalipainoinen betoni painaa noin 2 400 kg (2,4 tonnia) kuutiometriltä." }
      ],
      ro: [
        { q: "Cum se calculează volumul de beton pentru o placă?", a: "Înmulțiți Lungimea × Lățimea × Grosimea în metri pentru a obține metri cubi (m³): Volum = L × l × g." },
        { q: "Care este grosimea standard a unei plăci de beton?", a: "Trotuarele și terasele rezidențiale au o grosime de 10 cm (4 țoli). Aleile carosabile au 10-12,5 cm armate, iar platformele pentru trafic greu 15 cm sau mai mult." },
        { q: "Câți saci de beton uscat intră într-un metru cub?", a: "Un sac de 25 kg produce aproximativ 12 litri de beton proaspăt; sunt necesari circa 83 de saci pentru 1 m³." },
        { q: "Cât cântărește un metru cub de beton?", a: "Betonul obișnuit cântărește aproximativ 2.400 kg (2,4 tone) pe metru cub." }
      ]
    },
    proofs: {}
  }
};

