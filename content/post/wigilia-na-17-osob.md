+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2006-11-02T20:41:14"
title = "Wigilia na 17 osób"
tags = [ "życie" ]
+++
Do świąt zostało jeszcze sporo czasu, ale przed kim stoi wizja odbywania dwóch
Wigilii jednego dnia, temu czas zastanowić się nad rozwiązaniem.  Postanowiliśmy
z dziewczyną zrobić [podobnie jak na Wielkanoc](/2006/04/17/sped-rodzinny/),
tyle że w innym miejscu. Po ustaleniu składu i podliczeniu wszystkich osób
wyszło na to że będzie ich siedemnaście.

<!--more-->

Dotychczas na każde Święta każdy kupował prezent każdemu. Było to zupełnie w
porządku, kiedy przy wigilijnym stole zasiadało sześć do ośmiu osób. Przy
siedemnastu jednak liczba prezentów (czyli krawędzi w skierowanym grafie
pełnym) wynosi 17×16 czyli 272. To trochę za dużo; przy ograniczonych
funduszach byłyby to pewnie 272 baloniki.

Postanowiłem rozwiązać ten problem przy pomocy maszynki do losowania, która
generowałaby grafy o zadanych właściwościach. Posiedziałem i napisałem program
w Pythonie, który generuje opis grafu, wizualizowany potem przy pomocy
[Graphviz](http://www.graphviz.org/):

{{< figure src="/images/2006/prezenty-diagram.png" title="Przykładowy diagram" >}}

Na generowanie grafu można nakładać różnorakie warunki, na przykład maksymalną
liczbę prezentów jaką jest w stanie kupić dana osoba, lub to że prezenty
wymienia się pomiędzy domami (w obrębie domów można się wymienić następnego
dnia).

Czas pokaże czy pomysł się przyjmie. Jest niewątpliwie rozsądny. Sprawy
puszczone na żywioł sprawdzają się przy pięciu osobach, ale przy siedemnastu
już trzeba się organizować.

# Komentarze

* thot22003 (2006-11-02 21:05:08): <p>u mnie bylo zawsze 10 osob. jesli chodzi o
  rodzine. wtedy malzenstwa wspolnie skladaja sie na prezenty. :) nie musi to
  przeciez byc cos drogiego. wystarczy jakis drobiazg. liczy sie pamiec ;)</p>
* Hubert (2006-11-03 11:27:19): <p>Nie znoszę świąt Bożego Narodzenia a ten cały
  prezentowy idiotyzm jest jednym z głównych powodów. Nie potrafię kupować
  sensownych prezentów i sądząc po tym co zwykle dostaję - nie jestem wyjątkiem.
  <br /> <br />Próbowaliśmy (z małżonką) już nie raz &quot;ucywilizować&quot;
  kupowanie prezentów w rodzinie ale bez skutku... Kiedyś zaproponowaliśmy, żeby
  każdy powiedział co chciałby dostać, wtedy cała reszta się na to złoży i w ten
  sposób każdy dostanie coś z czego będzie zadowolony i coś na co być może
  normalnie nie mógłby sobie pozwolić. Ze mną sprawa jest prosta: od ręki mogę
  wysmarować całą listę płyt i książek które chciałbym mieć. Zażyczyłem więc
  sobie płyty, dość drogiej - żeby obdarowujący nie mieli wrażenia że zostałem
  obdarowany zbyt skromnie. I co? Dostałem tę płytę a oprócz niej taki sam
  zestaw niepotrzebnych mi przedmiotów jak zwykle...</p>
* thot22003 (2006-11-03 11:30:20): <p>no przynajmniej plyte dostales ;) a z
  resztu mozna zrobic tez pozytek. u mnie z gustem jest podobnie. pewna czesc
  rodziny zawsze kupi cos, co akurat mam albo wogole nie potrzebuje. wiec
  przynajmniej wystawiam to na aukcji :D</p>
* mama T (2006-11-03 18:38:19): <p>więc ,Maciek, wykonujesz pionierska pracę
  uczynienia z Gwiazdki i &quot;prezencji&quot; - przyjemności zamiast corocznej
  makabry.  Zawsze myślałam - gdybym tak mogła wydać 200 zeta na osobę. Ale
  szczerze mówiąc- nie tylko w finansach rzecz.  Kiedy kupujemy dla kogoś
  prezent - musimy o tej osobie przez chwilę pomyśleć, co lubi jaka jest co by
  się przydało. Niestety, w niektórych przypadkach nie da się wiele wymyslić.
  Daje się prezent, żeby zrobić przyjemnośc, a nie zaopatrywać. Prezenty nie-
  trafione zawsze można jakoś zutylizować. Mnie się pomysł maćka bardzo podoba,
  jak tez jego determinacja w pokonywaniu oporów co-bardziej-konserwatywnej
  części rodziny. Pewnie nie wszyscy sie zachwycą pomysłem, ale nie szkodzi.</p>
* Joanna Ludmiła (2006-11-04 17:12:53): <p>A dlaczego część osób rozdaje dwa
  prezenty, a część tylko po jednym?</p>
* Automaciej (2006-11-04 17:16:57): <p>Zasadą jest, że każda osoba otrzymuje dwa
  prezenty i tutaj nie ma wyjątków. Najprościej byłoby, gdyby każdy kupował i
  dostawał dwa prezenty. Sprawę jednak komplikuje fakt, że niektóre osoby, np.
  dzieci, nie kupują prezentów. Inne osoby mogą mieć założoną maksymalną liczbę
  prezentów jaką mogą kupić (np. jeden). Wtedy ktoś inny musi kupić trzy, żeby
  utrzymać dwa otrzymywane prezenty na osobę.</p>
* Joanna Ludmiła (2006-11-14 15:21:27): <p>Bardzo ciekawe. A opiszesz też ciąg
  dalszy po polsku? Bo to dopiero ciekawe. Nie spodziewałam się, że graf będzie
  miał zastosowanie w praktyce, myślałam, że tak się tylko bawisz.</p>  <p>No i
  jeszcze w ogóle by mnie interesowało, jak go zrobiłeś. Rozumiem podział na
  1-2-3 prezenty, czy były jeszcze jakieś warunki, czy tylko losowanie?</p>
* automaciej (2006-12-24 13:33:02): <p>11 dni do wylotu<br /><br />Dzisiaj
  Wigilia na 17 osób. Fajnie, że jedna! Nie będzie jeżdżenia po nocy od jednej
  babci do drugiej.<br />L. zrobiła na tę okazję cysternę sałatki warzywnej.
  Ciekawe, czy starczy.<br />Moja koncepcja prezentowa zostanie sprawdzona w
  praktyce. Z mo[...]</p>
* automaciej (2007-01-21 16:37:52): <p>11 dni do wylotu<br /><br />Dzisiaj
  Wigilia na 17 osób. Fajnie, że jedna! Nie będzie jeżdżenia po nocy od jednej
  babci do drugiej.<br />L. zrobiła na tę okazję cysternę sałatki warzywnej.
  Ciekawe, czy starczy.<br />Moja koncepcja prezentowa zostanie sprawdzona w
  praktyce. Z mo[...]</p>
* mamma (2007-06-13 18:57:42): <p>zapomniałeś opowiedzieć o fajnym pomyśle
  stworzenia forum na którym wszyscy &#8222;Wigilianie&#8221; mogli
  błyskawicznie sie porozumiec, nawet ci zza oceanu. Dla mnie to był
  majstersztyk. I nawet część artystyczna była!</p>
