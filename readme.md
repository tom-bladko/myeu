provincje

	defenses    0-5		obronnosc
	economy     1-12	bazowa wartosc prowincji		
	military	0-3		manpower dla armi
	shipyard	0-3		handel morski i flota
	science		0-3		co 50%
	culture		0-3		co 50%
	
jak dzialaja podatki ?
	bazą jest ECONOMY provincji, powiedzmy 1-12
	bonus za wladce 
	bonus za technologie ECONOMY 
	bonus za surowiec w prowincji
	bonus za brak kontaktu z capital 
	bonus za inna religie / culture 
	bonus za religie kraju 
	bonus za stabilonosc kraju 
	wychodzi z tego np 19$
	
	suwaki na poziomie kraju dziela to na 
		TECH 	10% TAX + 2 poziom budynku * 0.5 = 1.9B + 1B = 2B 
		CULTURE 5% TAX + 0 poziom budunku = 0.49C 
		[color_map.py](src%2Fcolor_map.py)
kupowanie technologi 
	techy maja 0-12 poziomów 
	kazdy poziom kosztuje 
		level * 100
		mod wielkosci kraju np x4 large country 
		ile sasiadow ma te technologie juz 
		poiozm TECH wladcy 
		poziom technolo
	techy maja swoj rok 
	jest kara za zbyt wczesne wynalazki
		0	600	[color_map.py](src%2Fcolor_map.py)
		1	800
		2	1000
		3	1200
		4	1300
		5	1400
		6	1500
		7	1575
		8	1650
		9	1700	
		10	1750
		11	1800
		12	1850

co mozna budowac w prowincji
    FORTS       0-5     zwieksza fortyfakcje prowincji                              
    SHIPYARD    0-3     zwieksza ilosc EXPLORE POINTS, TRADE POINTS, SHIP BUILDING  +100% na poziom     
    FARMS       0-3     zwieksza population growth                                  +3% na poziom
    BARRACKS    0-3     zwieksza manpower dla lądu, dla budowy armi, traditions tez +50% na poziom, +1   
    WORKSHOP    0-3     zwieksza dochody w prowincji z produkcji / podatkow         +25% na poziom
    MARKET      0-3     zwieksza wartosc prowincji z handlu dla center of trade     +50% na poziom
    LIBRARY     0-3     zwieksza generowane punkty nauki z prowincji                +10% na poziom
    TEMPLE      0-3     zwieksza ilosc missionarzy   +10% na poziom
    ROADS       0-3     zwieksza predkosc ruchu przez prowincje (dla wojska, handlu też)            poniżej
    COURTHOUSE          zmniejsza revolt risk

wonders ?
    w danej prowincji moze znajdowac sie SUPER WONDER
    to jest z dopiskiem GREAT jeden budynek i tylko jeden ktory daje 2 poziomy w danym obszarze
        GREAT TEMPLE    -> +2 poziomy do temple

fortyfikacje
    0       0
    1       5K
    2       10K
    3       15K
    4       20K
    5       30K

jak działaj drogi ?
    level       koszt ruchu
    0           200%
    1           100%
    2           50%
    3           25%    

co zbiera panstwo na poziomie grobalnym ?
    GOLD -> wiadoo
    SCIENCE -> kupowanie poziomów technologi
    LEGACY -> osiagniecia kulturowe, konwersja prowincji kultura, religia, zmiana religi
    EXPLORE -> zdobywanie pustych prowincji i explorowanie nowych prowincji
    DIPLOMACY -> akcje dyplomatyczne i szpiegowskie z innymi krajami
    TRADE -> wysyłanie kupców do centrum handlowych
    TRADITION -> limit ilosci armi ??, generowalowie
	
JAK DZIALA EXPLORE / COLONIZE
    za punkty EXPLORE mozna odkrywac istniejace prowincji
    morskie maja swoja cene zalezna od wielkosci i terenu
    ladowe puste maja swoja cene
    ladowe czyjesz maja o wiele wieksza cene
    nie potrzeba tam armi
    mozna odkrywac tylko prowincji obok tych ktore znasz
    dyplomacja moze wplywac na cele odkrycia prowincji
    odkryte prowincje (MAPA) mozna sprzedac lub kupic
    po wybraniu prowincji ze stolicy porusza sie jednostka EXPLORATOR ktora po najkrotszej sciezce leci do celu
    jak dotrze do celu to odkrywa teren

    pusta prowincje mozna explorowac, nie trzeba tam wysylać jednostki
    należy wysłać koloniste i on do tej prowincji sobie jedzie
    aby przejac prowincje na poziomie 1 trzeba miec 3 udane próby kolonizowania

jak działa DIPLOMACY POINTS
    gracz zbiera punkty diplomacy głownie przez
        polityke rządu
        religie
        władce 
    wybiera kraj i wybiera akcje
    w danym kraju mozna wybrac jedna akcje na ture czyli 1 miesiac 
    im wiekszy kraj tym drozsze akcje dyplomatyczne
    max ilosc punktow dyplimatyznych to 20

jak dziala LEGACY POINTS
    zbierane sa przez
        religie
        polityke rzadu
        wladce
        budynki kultorowe w prowincji
    na co mozna wydac ?
        konwersja prowincji CUTLURE na naszą (trwa 5 lat)
        konwersja prowincji RELIGION na naszą (trwa 5 lat)
    na zmiane religi kraju na jakas inna
    na zakup osiagniec kultorowych ktore daja jakies bonusy ??

jak działą SCIENCE POINTS
    w grze jest kilka sciezek technologi, kazda na poziomie 0-12
    gracz zbiera punkty i jak ma ich duzo to moze wybrac jakis poziom i zrobic BUY
    im wyzszy poziom technologi tym droższa technologia by 25%
    bazowa cena technologi zalezy od ilosci prowincji
    rodzaje technologi
        MILITARY            20% wiekszy power ARMI i FLOTY podczas bitwy
        TRADE               10% wiekszy dochód z handlu w COT
        PRODUCTION          10% wiekszy dochód z ekonomi prowincji        
        GOVERNANCE          mozliwosci zmiany polityki rzadu w kraju, 1 level = 1 poziom
        INFRASTRUCTURE      odblokowanie mozliwosci budowania różnych budynkow w prowincjach
    na co nie wplywa technologia ?
        na dyplomacje
        na kulture i religie 
        na populacje, chyba że FARMING przez infra
        na inne wynalazki, chyba że posrednio przez LIBRARY i infrastructure
        na exploracje, chyba ze posrednio przez SHIPYARD i infrastructure

jak dziala GOVERNANCE POINTS
    kazdy kraj ma punkty zaczyna od 3
    głównym zrodel zdobywania jest technologia GOVERNANCE (max 12)
    gracz kupuje różne FOCUS AREA, kazde ma 3 poziomy
        1   +25%    kosztuje 1
        2   +50%    kosztuje 2
        3   +100%   kosztuje 3
    czyli wejscie na poziom 3 kosztuje 6 punktów GOVERNANCE
    dodatkowo gracz dostaje co N lat za darmo punkt, np co 100 lat 

zakres czasowy gry 
    zakres 1250 - 1850 = 600 lat, 12 leveli
    Level 0 (1250-1350): This period saw significant technological advancements such as the introduction of the mechanical clock, which revolutionized timekeeping. Other notable inventions include the vertical windmill, spectacles, and improved water mills1.
    Level 1 (1350-1440): The invention of the printing press by Johannes Gutenberg around 1455 marked a major technological leap, enabling the mass production of books and the spread of knowledge2.
    Level 2 (1440-1510): This period witnessed the development of gunpowder weapons and advancements in navigation, such as the caravel, which facilitated exploration and military technology3.
    Level 3 (1510-1570): The Scientific Revolution began, with figures like Copernicus publishing his heliocentric theory in 1543, which forever changed astronomy. This period also saw the invention of the pocket watch by Peter Henlein in 151034.
    Level 4 (1570-1620): The invention of the telescope by Galileo Galilei in 1609 and the microscope by Zacharias Janssen around 1590 opened new frontiers in science, allowing for detailed observations of the cosmos and microscopic life3.
    Level 5 (1620-1660): The development of the steam engine by Thomas Newcomen in 1712 laid the groundwork for the Industrial Revolution. This period also saw the invention of the barometer by Evangelista Torricelli in 164356.
    Level 6 (1660-1690): The spread of the Scientific Revolution continued, with Isaac Newton's work on gravity and motion transforming our understanding of the natural world. Newton also invented the reflecting telescope in 16686.
    Level 7 (1690-1720): The early stages of the Industrial Revolution saw the rise of mechanized textile production and improvements in iron smelting. This period also saw the invention of the first practical steam engine by Thomas Savery in 16983.
    Level 8 (1720-1750): The invention of the spinning jenny by James Hargreaves in 1764 revolutionized the textile industry, leading to increased production and efficiency3.
    Level 9 (1750-1780): The development of the steam locomotive by George Stephenson in 1814 revolutionized transportation and trade3.
    Level 10 (1780-1810): The invention of the electric telegraph by Samuel Morse in the 1830s transformed communication, allowing for rapid transmission of information over long distances3.
    Level 11 (1810-1830): The culmination of the Industrial Revolution saw significant advancements in manufacturing, transportation, and communication, setting the stage for the modern era3.
    Level 12 (1830-1850): This period continued to build on the advancements of the Industrial Revolution, with further innovations in various fields3. 

COLORS  
    w tej chwili jest 11 x 3 = 33 kolory w grze bazowe

RESOURCES in province
    28 total surowców
    food                    6 types
        FISH        10      NEW
        GRAIN       5       NEW
        RICE        5       NEW
        CORN        5       NEW
        LIVESTOCK   10      NEW
        FRUITS      5       NEW    

    commodity               6 types       
        CLOTH       15      
        FURS        10      
        WINE        15      
        LUMBER      5       
        WOOL        5           
        SALT        15      
        SILK        ?       NEW
    
    mines                   6 types
        COPPER      15          
        GOLD        30      
        IRON        20      
        SLAVES      5       
        GEMS        40      NEW
        COAL        10      NEW
    exotic                  10 types
        COFFEE      10      
        TEA         10      
        COTTON      10      
        SUGAR       15      
        TOBACCO     10      
        SPICES      15      
        IVORY       20      
        CHINAWARE   15      
        DYES        10      NEW
        COCOA       15      NEW

    na co wpływa resource ?
        POPULATION GROWTH -> to samo co farming
        PRODUCTION -> to samo co workshop
        TRADE VALUE -> to samo co market 
        

populacja - province baseline
    LEVEL	POP in K
    1	4
    2	10
    3	19
    4	30
    5	44
    6	60
    7	79
    8	100
    9	124
    10	150
    11	179
    12	210
    13	244
    14	280
    15	319
    16	360
    17	404
    18	450
    19	499
    20	550
    21	604
    22	660
    23	719
    24	780
    25	844
    26	910
    27	979
    28	1050
    29	1124
    30	1200
    31	1279
    32	1360
    33	1444
    34	1530
    35	1619
    36	1710
    37	1804
    38	1900
    39	1999
    40	2100
    41	2204
    42	2310
    43	2419
    44	2530
    45	2644
    46	2760
    47	2879
    48	3000
    49	3124
    50	3250
    51	3379
    52	3510
    53	3644
    54	3780
    55	3919
    56	4060
    57	4204
    58	4350
    59	4499
    60	4650
    61	4804
    62	4960
    63	5119
    64	5280
    65	5444
    66	5610
    67	5779
    68	5950
    69	6124
    70	6300
    71	6479
    72	6660
    73	6844
    74	7030
    75	7219
    76	7410
    77	7604
    78	7800
    79	7999
    80	8200
    81	8404
    82	8610
    83	8819
    84	9030
    85	9244
    86	9460
    87	9679
    88	9900
    89	10124
    90	10350
    91	10579
    92	10810
    93	11044
    94	11280
    95	11519
    96	11760
    97	12004
    98	12250
    99	12499
    100	12750

	
władca
	administracja		handel 
	dyplomacja			diplo
	militaria			land, navy 	
	technology			tech level 	-10% per level
	
punkty focusu
	ileś obszarow które można specjalizowac 
	3 + level tech GOV, max 15
	wyższe poziomy kosztuja 1,2,3
	
podatki
	na co idzie kasa z TAX ?
	TECH		0% - 10% - 20%
	ARMY 		50% - 100% - 150%
	CULTURE		
	SPIES		0% - 5% - 10%
	
kultura
	różnica -25%
	
religia
	różnice -25%
	religia globalnie daje bonus 
	konwersja kosztuje punkty culture
	
surowce
	ryby	
	zboże		
	drewno 	
	złoto	
	żelazo	
	wełna		
	
armie i flota
	armia jest jedna LAND or NAVY 
	nie ma typow jednostek 

na jakosc wojska wpływa 
	technologia, 1 level to 25% wiecej, 50% base, max 650%
	focus kraju, 
		land focus 		25% - 50% - 100% wiecej
		navy focus 		25% - 50% - 100% wiecej
	religia 
		islam ma np +20%
	wladca
		1 punkt +10%, zakres 1-5
	general
		1 punkt to +20%, zakres 1-5
	stab kraju -3 do +3
		+-10% per punkt 
	morale wojska
		losowe wydarzenia
		utrzymanie państwa 
			low 	50%
			med 	100%
			high 	125%
	teren na którym jest bitwa 
		liczy sie teren obroncy i atakujacego
		+10% do -50%
	okrązenie
	ataku z 2 kierunkow 
	brak drogi ucieczki
		np -50%
	pogoda / klimat 
	rozkazy generala podczas bitwy
		szturm			POWER +25%, DMG 2
		ostroznie		POWER -25%, DMG 0.5
	okopanie armi 
		1 poziom = 10%, max 3 level 
	za duza armia np np mozliwosci bitwy / generala etc 
	zaopatrzenie w zapasy lub brak
		sa zapasy 		0%
		male zapasy 	-25%
		brak zapasow 	-75%
		
gra odbywa sie walka cos ala legion, nie moze byc 20 malych units 
	ilosc legionow 		3-6-9-12
		
na co wplywa wielkosc kraju 
	tiny	1		x1	2
	small	2-4		x2	4
	medium	5-9		x3	6
	large	10-16	x4	8
	huge	17+		x5	10
	
	bazowa wielkosc korupcji w prowincji ?
	bazowa cena technologi
	max ilosc armi / floty ?

rekrutacja armi ?
	cena 1 UNIT = 10$
		wiele rzeczy wplywa na koszt zakupu 
	ilosc max w turze w prow = man power
	dodatkowo jest manpower w kraju, zaklada pelny regeneracja 2 lata = 8 tur
	armia potem musi sie utrzymac
	
	manpower = province size * mod 
		no baracks = 50%
		baracks +50% za kazdy poziom 
		barack 3 poziom = 200% prov size 
	
	flota ma inny manpower 
		no shipyard = 25%
		shipyard za kazdy poziom +75%
		shipyard na 3 poziomie = 250% prov size 
		
	manpower lokalny regeneruje sie co ture, ale globalny jest ograniczeniem
		
	armia buduje sie 2 tury 
	flota buduje sie 4 tury 
		
surowce 
	zbieranie surowcow daje bonusy 
	
		
koszt budowy rozwoju prowincji 
	od 1 do 12 powiedzmy 
	koszt budowy 
		teren prowincji / klimat
			plains 100%
			mountains 250%
			desert 800%
		poziom na ktory wchodzisz
			bazowe 50$
			poziom 8 = 400$ i 8 tur
		province resouce 
			cos z zarciem -50%
		technologia agriculture 10%
			0 -> 120%
			12 -> 30%
		focus kraju 
			farming 	-25%, -50%, -75%
	czas budowy 
		poziom na ktory wychodzisz w turach 
		wejscie na 8 poziom = 8 tur = 2 lata 
		
fortyfikacje 
	level 0 do 5
	budowa kosztuje 200% za poziom 
	military level needed do budowy 
		level 1, 3, 5, 7, 9, 11
	budowa trwa tyle tur x2 co poziom max 10 tur
		
najemnicy 
	nie kosztuja manpower 
	kosztuja 25$ za UNIT 
	sa dostepni od reki 
	
koncepcja walki jest	
	strona A ma wojska SIZE 12 o POWER 21
	strona B ma wojska SIZE 16 o POWER 18
	stosunek POWER definiuje kto traci SIZE 
	na 1 ture jest np 5 takich rzutów 
	
atak na fort 
	fort ma wbudowana armie i mury 
	1 -> SIZE 2, WALL 0
	2 -> SIZE 5, WALL 1
	3 -> SIZE 10, WALL 2
	4 -> SIZE 20, WALL 3
	5 -> SIZE 40, WALL 4 = 1 rok
	
	WALL oznacza ile tur trzeba atakowac zeby pokonac mury 

jeszcze inne podejscie do ekonomi
    prowincja ma poziom od 1 do 24 tak jak cywizacja
    populacja jest luzno powiazana z poziomem
    populacja wolno rosnie przez pop growth

prowincja moze miec rozne budynki, ale tylko na 1 poziomie
    farmlands           province growth +3%
    barracks            province manpower x2, bravery +1
    shipyard            explorer +1, merchant +1, ships building x5
    manufacture         province production +50%
    marketplace         province trade value +100%, merchant +1
    library             province science output x2
    temple              province social output x2
    courthouse          revolt risk spada
    roads               poprawia predkosc prowincje
    forts               poziomy od 0 do 5


jak dziala suwaki budgetu na poziomie panstwa
    0-10-20% -> technologia
    0-10-20% -> social (czyli stabilizacja prowincji / kraju / zadowolenie)
    
jak dziala populacja i poziom 
    najwazniejszy w grze jest POZIOM PROVA
    jest on luzno powiazany z populacja
    przyrost naturalny jest na poziomie kilku % rocznie
    ale naliczany jest do POZIOMU a nie do POPULACJI
    liczony przyrost to
        2% niski
        5% sredni
        10% maxymalny
    co ture (miesiac) przyrasta dokładnie 1/12 przyrostu
    przy srednim przyroscie z LEVEL 10 przejdziesz na LEVEL 20 po 100 latach

co wplywa na przyrost ?
    stabilnosc          zakres -3% do +3%
    stolica             +1%
    farmalands          +3%
    dobry teren         +1%
    zły teren           -2%
    dobry klimat        +1%
    zły klimat          -2%
    COT                 +2%
    occupied            -3%
    looted              -10%        trwa 12 miesiecy
    enemy               -20%        jesli wrog jest w prowincji
    food resources      +2%

co wpływa na dochód z produkcji prowincji ?
    baze province level     12
    bonus za surowiec       0% do 100% 
    manufactura             x2
    technologia level       30% + 10% za level

co wpływa na wartosc handlowa prowincji ?
    baze province level
    wartosc handlowa surowca
        low         5-10%
        medium      15-20%    
        high        25-30%
    marketplace budynek         x2
    polityka rzadu ?            +25% za poziom
    przykład
        level           12 
        high value      30%
        + marketplace   x2
        politycs        +50%
        12 * 0.3 x2 + 50% = 12
    centrum handlowe zbiera wszystkie prowincje w zasiegu i ma jakas wartosc
    np 800 punktów handlu

COLORS jak robie
    kolory ladowane sa z colors
    kazdy ekran ma swoj color set
        
        screens
            diplomacy
            trade
            religions
            explore 
            terrain
            political
    
        REPORTS
            revolts
            wars    
            forts
            culture
            population
            wealth
            goods
            regions
            supply
            roads
prosty system
    prowincja ma poziom
    dochód z PRODUKCJI
    dochód z HANDLU
    
GROWTH 
    5-10% rocznie
    rośnie level o 1    
    jako pomoc konwertuje poziom do population
    bonus od surowca
        5-25$ price z EU
        5$  -> +0%      very low     
        10$ -> +1%      low
        15$ -> +2%      avg
        20$ -> +3%      high
        25$ -> +4%      very high

MANPOWER
    poziom prowincji i modsy
    nie core prowincja      -25%
    baraki                  +100%
    culture diff            -25%
    capital city            +25%
    overseas                -25%
    policies                up to +100%
    min value               1
    czas odnowy             2 lata

REKRUTACJA WOJSKA
    gracz na poziomie panstwa widzi tylko sume MP swoich provow
    budowa wojska jest na pozimie prova

BRAVERY
    kultura posiada bravery ktore wplywa na morale wojska
        low         2    
        medium      3    
        high        4         
    bravery modyfikuje morale wojska
    mercenaries maja zawsze bravery +1

PRODUCTION
    poziom prowincji
    bonus od surowca
        5-25$ price z EU
        5$  -> 50%      v low    
        10$ -> 75%      low
        15$ -> 100%     avg
        20$ -> 125%     high
        25$ -> 150%     v high
    poziom technologi
        30% bazowe + 10% per poziom aż do 30 + 120 % = 150%
    religia / cultura inna -30%
    stabilnosc kraju -5% za 1 poziom plus mius
    korupcja ? 
    
TRADE
    poziom prowincji
    bonus od surowca
        5-25 price z EU
        5$  -> 50%      v low
        10$ -> 75%      low
        15$ -> 100%     avg
        20$ -> 125%     high
        25$ -> 150%     v high
    wartosc sumowana w centrum handlowym
    ktora prowincja nalezy do ktorego COT zalezy od dyplomacji
           
bitwa
    dwie armie
    kazda ma swoje REGIMENTY np 5
    kazda ma swojego generala
    liczymy FIRE POWER
        duzo modyfikatorow na FIRE POWER
    testujemy FIRE POWER kto zadaje hita
    trafiony ma szanse na 
        20%   DODGE unik - nic sie nie dzieje
        40%   WIA regiment, czyli nie walczy ale przezywa
        40%   KIA zniszczony regiment
        0%    CIA zdobyty regiment przez wroga (za kase ?)
    jedna faza bitwy trwa 5 dni (ZMIENNE)
        podczas kazdej fazy za 1 dzien walki jest jeden rzut
        faza bitwy moze trwac od 1 do 9 dni max, srednio 5
    general armi
        OFFENSIVE 1-6 -> wplywa na FIRE POWER
        DEFENSIVE 1-6 -> wpływa na DEFENSE jesli trafiony
        SIEGE 1-6 -> wpływa na walke podczas oblegania
        TACTICS 1-6 -> mozliwosci rozkazów w trakcie bitwy ?
    walka z fortem to taka walka z armia tylko specyficzyny setup

fortyfikacje
    0   brak
    1   5 regimentów, 3 miesiace
    2   10 regimentów, 6 miesiecy
    3   15 regimentów, 9 miesiecy
    4   20 regimentów, 12 miesiecy
    5   25 regimentów, 15 miesiecy
    6   30 regimentów, 18 miesiecy

dwie metody zdobywania fortyfikacji
    szturm -> zwykła bitwa ale przeciwnik 
    siege -> fortyfikacje trwaja tyle tur / miesiecy ile level
            po tym czasie sie poddaja z braku zaopatrzenia
            ten czas moze sie wydlużyc


najnowszy model
    prowincja ma base value 
    to cos jak w master of orion
    to jest generalnie STAŁA LICZBA
        1    U POOR           50%    
        2    POOR             75%
        3    NORMAL           100%
        4    RICH             150%
        5    U RICH           200%

na co wpływa surowiec
    POPULACJE       powolny wzrost wartosci prowincji
    PRODUKCJE       lokalny dochów
    HANDEL          wartosc prowincji dla centrum handlowego
    każdy surowiec wpływa 
                    PROD    GROWTH  TRADE   GOLD    MANPOWER    
        V LOW       50%     0%      25%     +0      50%
        LOW         75%     1%      50%     +1      75%
        NORMAL      100%    2%      100%    +2      100%
        HIGH        125%    3%      150%    +4      150%
        V HIGH      150%    4%      200%    +8      200%
    

POPULACJA
    liczba na która ma wpływa gracz 
    zakres 1-24 z tym że 
    dla celów widowiskowych licze z tego populacje jak CIV2 powyżej
    co ture = miesiąc rośnie o 1/12 rocznego wzrostu który masz jest 15% (czyli 0.15 wzrost poziomu rocznie)

dochody z prowincji
    PROVINCE INCOME
        population level        np 7
        baseline mod            np 75%   POOR  
        goods mod               np 75%      
        manufactory             150% lub wiecej     
        capitol                 125%
        state religion mod      80%-120%    
        culture diff            75%
        religion diff           75%
        no connection to cap    75%
        infrastructure tech     30%-150%, krok co 10% na 12 leveli
        stability               -3 do 0 do +3  (100%, 100%, 100%, 100%, 100%, 110%, 120%)    
        state politics          100% - 150% (gracz wybiera)
        occupied by another     50%     (reszte przejmuje okupant)
        tax level               50% - 150% (gracz ustala)
    PROVINCE TRADE 
        population level        np 4
        baseline mod            np 150% HIGH
        good mod                np 200% HIGH
        marketplace             150% lub wiecej
        enemy army              50% (wojna i handel sie nie lubi)
        looted                  50% (wojna i handle sie nie lubi)
        technologia wplywa na dochód a nie na wartość w COT
        state politics          100% - 200%
    PROVINCE GROWTH
        wartosc bazowa          2%    
        state stability         wartosc STAB czyli -3% +3%
        COT                     +2%
        blisko COT              +1%
        capitol                 +1%
        farmlands               +3%
        goods mod               0 do +4%    
        looted                  -10%
        enemy army              -20%
        baseline mod nie wplywa
        technologia nie wpływa
        state politics nie wplywa

TECHNOLOGY
    kraj generuje punkty nauki za ktore mozna kupowac poziomy technologi w 5 obszarach
    gracz moze kupic kazde 20% poziomu jak ma punkty nauki
    co generuje punkty nauki
        WLADCA zaleznie od wielkosci ADMIN
        sasiedzi ktorzy maja wyzszy poziom

RODZAJE TECHNOLOGi  
    każda ma level 1-12
        MILITARY / MILITARY    wojna
        ADMIN / GOVERNANCE     decyzje w zarzadzaniu, polityka, konwersja religi kultury
        INFRA / ECONOMY        budowa w prowincjach, dochod z produkcji
        FINANCE / TRADE        zarzadzanie kasa i handel,

na góre na pasku mamy
    diplomat       max 12  akcje dyplomatyczne / akcje szpiegowskie / wywiadowcze / sabotaż
    merchant       max 12  handel w COT
    settlers       max 12  odkrywanie prowincji/ poprawianie poziomu POP LEVEL w prowincji (każdej w tym pustej)
    general        max 12  promowanie generałow w armi / flocie , trenowanie armi na wyższy exp
    missionary     max 12  konwersja kultury / religi w prowincji / albo obniza revolt risk w prowincjach
    inventor       max 12  kupowanie nowych technologi                     man-years
    advisors       max 12  aktywowanie nowych polityk                      e.g. +0.25 na rok, 3 poziom polityki kosztuje 1
    engineer       max 12  budowanie w prowincjach nowych budynków

kupowanie polityk
    max raz do roku
    1 level         4 advisors
    2 level         8 advisors
    3 level         12 advisors

kupowanie technologi 
    max raz do roku
    technologie maja swoje koszty np 20 man-years
    gracz moze wydac to co ma (max 12 moze zbierac) na postep w dowolnym obszarze


normal
    teren na prowincji + pogoda (snieg)
    granice krajow
    ikonka = flaga ownera prowincji 
    stolica kraju
    armie zawsze
    w prowincji buduje sie armia 
    
polityczna 
    kolor = owner prowincji
    granice krajow
    ikonka = flaga ownera prowincji 
    stolica kraju
  X  core prowinces dla aktualnego kraju 
    armie LUB nie zaleznie od politycznej
    
ekonomiczna
    kolor = wartosc produkcji w prowincji w odcieniu GREEN 
    granice krajów ??
    ikonka prowincji = surowiec
    stolica kraju ??
    
culturowa mapa
    kolor = kolor kultury prowincji 
    granice krajow 
    ikonka = tylko w stolicy kraju 
    
revolt risk map 
    kolor = aktualny revolt risk i inne sytuacje z happines 
    granice krajow 
    ikonka = flaga ownera prowincji 
    stolica kraju 
    
fortyfikacje 
    kolor = aktualny poziom fortyfikacji kraju 
    granice krajow 
    ikonka = flaga ownera prowincji 
    stolica kraju 
    
manpower
    kolor = aktualny poziom manpower w odcieniu RED
    granice krajow 
    ikonka = flaga ownera prowincji 
    stolica kraju     
    
zaopatrzenie 
    kolor = aktualny poziom zaopatrzenia w prowincji 
        green = jest
        yellow = czesciowy
        red = nie ma 
    granice krajow 
    ikonka = flaga ownera prowincji 
    stolica kraju     
    
mapa regionów
    kolor = aktualny region prowincji 
    granice krajow 
    ikonka = flaga ownera prowincji 
    stolica kraju     
    
mapa religii
    kolor = aktualna religia prowincji jako primary
    kolor = aktualna religia kraju jako secondary
    granice krajow 
    ikonka = tylko dla stolic krajów
    stolica kraju     
    
dyplomatyczna
    kolor = aktualny poziom relacji tego kraju z wybranym krajem 
    granice krajow 
    ikonka = tylko dla stolic krajów 
    dodatkowe ikonki ktore symbolizuja umowy krajów np SOJUSZ lub WOJNA
    stolica kraju  
 
handlowa COT 
    kolor = obszar do ktorego COT nalezy prowincja 
    granice krajow 
    ikonka = tylko dla miejsc COT to wlasciciel prowincji gdzie jest COT 
    NIE MA stolic kraju
    
explore & colony map 
    kolor = mozliwe akcje
        brak 
        light blue = mozliwosc odkywania terenu , tylko pobliskie prowincje ktore sa FOG 
        light green = mozliwosc kolonizacji pustej prowincji
        green = mozliwosc kolonizacji swojej prowincji 
        red = blokada kolonizacji / exploracji np sankcje / wojna 
        
infrastruktura 
    kolor = predkosc ruchu wszystkiego przez prowincje od DARK to WHITE 
    granice krajow 
    ikonka = flaga ownera prowincji 
    stolice krajow 


zrodla dochodów
    TAXES -> z produkcji wlasnych prowncji
    TRADE -> z handlu z kupców
    TARIFFS -> oplaty za to ze ktos przechodzi przez Twoj kraj + centra handlowe
    LOOTING -> z grabiezy podczas wojen
    GOLD -> ze sztucznego robienia kasy
    TRIBUTES -> od panst zaleznych, srednio 50% dochodu
    INTERESTS -> z odsetek pozyczek ktore komus dalismy    
    
zrodla wydatkow
    MILITARY -> utrzymanie wojska, floty, fortyfikacji
    TECHNOLOGY -> wydatki na innovatów
    STABIILITY -> wydatki na powrót do stabilnosci
    CORRUPTION -> wydatki ziwazane z utrata dochodu z różnych podowodw
    TRIBUTES -> wydatki dyplomatyczne
    INTERESTS -> wydatki na oplaty za kredyty

sliders wydatkow
    TAXES           poziom podatków ( wpływa na income TAXES )
    MILITARY        wysokosc wydatkow na wojsko, flote i obronnon (ilosc generals)
    TECHNOLOGY      wysokosc wydatkow na technologie (ilosc inwentorów)
    STABILITY       wysokosc wydatków na stabilnosc i revolt risk  (ilosc misjonarzy)  
    ADMINISTRATION  wysokosc wydatkow na administracje (korupcja / ilosc inzynierów / advisors )
    TARIFFS         wysokość ceł w swoim kraju 
    ESPIONAGE       ilosc szpiegów

jak zdobywam kazdego specjaliste
    diplomat
        bazowa ilosc        1
        skill krola         SKILL DIPLO - 1 czyli +1 do +5
        religia panstwa     od 0 do +2
        at war              +1
        polityka panstwa    ???? 
        z budgetu           ????
    merchant
        CoT                 +1 za kazde
        trade tech          tech / 4 round down
        policies            mercentalizm / free trade -2 +2
        religion            od 0 do +3
        coastal provinces   ilosc / 5 round up
        stabilnosc          -3 do +3
    settlers                -> exporacja i kolonizacja
        religia             0 +2
        shipyard            ilosc shipyards / 2 rounded up 
        polityka            mercentalizm do +1
        polityka            morska  do +2
        politya             ladowa do -2
        polityka            cos z tradycjami -2 do +2
    general                 -> budowanie armi, limit generałow, doswiadczenie wojska
        polityka            cos z land / cos z offensive / cos z quality        do +1 za kazde
        krol                MIL skill / 2
    missionary              -
        poziom polityki wiara / technologia w zakresie -2 do +2 rocznie
        religia stanowa od 0 do +2
        temple              +0.25 ??
    inventor                -> kupowanie wynalazkow
        wladca              akill ADMIN / 6
        inne panstwa        ??
        tech agreement      +0.5
        library w prow      +0.25
    advisors                -> zmiana polityk na poziomie kraju
        krol                skill ADMIN / 12  
        ??
    engineers               -> budowanie infrastruktury w prownincji
        base                1
        krol                skill ADMIN / 2 (max +3)
        budget              +1 +2 +3
        polityka ??         jakies do +2
        INFRA tech          level / 3

ostateczne technologie
    LAND
    NAVAL
    INFRA
    TRADE
    ADMIN
    cos jeszcze 


GENERAL BONUS
    range 1-6, which means 1 point is +10% with 1 = 0%
    OFFENSIVE   from 100% to 150%
    DEFENSIVE   from 100% to 150%
    SIEGE       from 100% to 150%

maintenance wojsk kosztuje 10% ich zakupu
najemnicy kosztuja x2 złota, nie kosztuja manpower, kosztuja utrzymanie x2 złota

general jakie ma skille
    offensive   - bonus do ataku w bitwie
    defensive   - bonus do obrony
    siege       - bonus do szturmu na twierdze
    tactics     - bonus do predkosci ruchu
    logistics   - koszt utrzymania armi

ruch wojska po mapie
    kazda jednostka ma 30 dni ruchu
    bazowy koszt wejscia na prowa to 10 dni
    general moze zwiekszac predkosc ruchu przez tactics
        1-2 0%
        3-4 +10%
        5-6 +20%
    bazowa predkosc armi, modyfikator do ilosci MOVE DAYS
        piechota        x1.0
        artyleria       x0.5
        kawaleria       x2.0
    bazowy koszt ruchu w prowincji
        plains          10
        forest          12
        swamp           14
        hills           16
        desert          12
    prowincje moge miec specjalny modufikator wielkosci
        small           1.0
        medium          1.2
        large           1.5
    drogi zbudowane w prowncji, koszt ruchu - 25%
    bad weather in province will increase cost +4
    technologia miedzy 0 a 12 poziomem daje 100% bonusu
        level   days
        0       28
        1       29
        2       30
        3       31
        4       32
        5       33
        6       34
        7       35
        8       36
        9       37
        10      38
        11      39
        12      40

ruch na morzu jest inaczej
    kazda jednostka ma 30 dni na ture 
    bazowy koszt wejscia 10 dni 
    general moze zwiekszac predkosc ruchu przez tactics
        1-2 0%
        3-4 +10%
        5-6 +20%
    predkosc jednostek 
        warship     x1
        galley      x1.5    (cannot enter ocean)
        transport   x0.5
    bazowy koszt ruchu w prowinicji
        coastal     10
        sea         15
        ocean       30
    nic nie mozna budowac w prowincji
    sztorm na morzu daje koszt ruchu +5
    technologia miedzy 0 a 12 poziomem daje 100% bonusu
        level   days
        0       28
        1       29
        2       30
        3       31
        4       32
        5       33
        6       34
        7       35
        8       36
        9       37
        10      38
        11      39
        12      40


koncepcja budunkow jest 
    specjalne filtry
        tylko dla religi
        tylko dla kraju
        tylko dla regionu
        tylko dla prowincji ID
        tylko dla technologi poziom min
        ile ma max poziomów, ktory poziom

jakie daje bonusy ?
    province growth
    military:
        province local army (army in fort)
        province local defenses (size of walls)
        province manpower 
        province army bravery (morale bonus)
        province ships build bonus
    economy:
        province production tax bonus
        province trade value bonus for local COT
        koszt ruchu wojsk / agenta przez prowincje
    agents:
        country explorer bonus
        country merchant bonus
        country inventor bonus 
        country missionary bonus
        country diplomats bonus
        country advisors bonus
        country generals bonus


# FAME

odpowiednik bad boy albo infamy
dostajesz negatywne za zle rzeczy
dostajesz pozotywne za dobre rzeczy
za duzo negatywow mozesz miec globalna wojne na siebie


ekonomia na nowo
    prowincja ma w sobie CITY
    CITY ma poziom ktory mniej wiecej odpowiada CIV 2
    LEVEL powoli rosnie razem w GROWTH np 5% rocznie czyli co 20 lat jeden poziom w górę
    
ilosc armi panstwa per ilosc prowincji
    1-2     1
    3-5     2
    6-9     3
    10-14   4
    itd

dochody z prowincji
    MANPOWER
        PROV LEVEL
        base modifier       50%     
        has barracks ?      200%    
        is core prov ?      100%    
        is not core prov    50%     albo wrong culture ??
        no connection       50%
        capitol             125%
        some policies       125% / 150% ??
    TAX 
        PROV LEVEL 
        * culture diff 
        * religion diff
        * tech level admin
        * country STAB
        * no connection to capitol
        * country religion bonus
        * province building town hall
    TRADE
        wartosc handlowa surowca 5-25
        bonus za prov level 
            1 - 50%
            5 - 100%
            10 - 150%
        * 