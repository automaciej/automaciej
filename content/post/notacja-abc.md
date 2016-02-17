+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2014-09-14T23:51:15+01:00"
draft = false
title = "Notacja ABC"
description = "Tekstowy format reprezentacji zapisu nutowego"
tags = ["muzyka"]
menu = ["main"]
+++
[Notacja ABC][] istnieje od przynajmniej od 15 lat.  istnieje od przynajmniej od
15 lat.  Jest to zapis tekstowy, który komputer potrafi wyświetlić w postaci
nut, albo zamienić na plik MIDI i odegrać. Przykładowo, „Wlazł kotek na płotek”
wygląda tak:

    X:1
    T:Wlazł kotek na płotek
    C:Autor nieznany
    K:C
    L:1/4
    M:3/4
    GEE|FDD|C/E/G2|GEE|FDD|C/E/C2|]
    w:Wlazł ko tek na pło tek i mru ga Ład na to pio sen ka nie dłu ga.

Na tej podstawie możemy wyświetlić wersję graficzną:

<object data="/wlazl-kotek-na-plotek.svg" type="image/svg+xml"></object>

Do zamiany pliku `.abc` na grafikę używamy narzędzia
[abcm2ps][], albo robimy to online na stronie
[drawthedots.com](http://www.drawthedots.com). Jest wiele innych, ale te dwa
dawały najlepsze rezultaty.

Notacja ABC jest dobrze udokumentowanym standardem.  Obecna wersja to 2.1 z roku
2011.  Istniejące narzędzia niekoniecznie implementują najnowszą wersję
standardu i niekoniecznie implementują go w całości.

Niektóre narzędzia komercyjne takie jak aplikacja androidowa Fakebook potrafią
czytać ten format, ale bywa różnie z implementacją. Lepiej jest zamienić nasz
plik .abc na MusicXML i importować do komercyjnych narzędzi z MusicXML.

Wikipedia obsługuje ABC: żeby dodać nuty do artykułu wystarczy otoczyć tekst ABC
odpowiednim tagiem:

    <score lang="ABC">
    ...
    </score>

ABC jest najlepiej przystosowana do zapisu melodii z akordami i słowami.  Nuty
bardziej skomplikowane też można zapisać, ale szybko się to komplikuje.

Skoro ABC jest przejrzystym formatem, można się spodziewać istnienia
społeczności internetowych wymieniających muzykę w tym formacie. Faktycznie,
dużo materiału można znaleźć poprzez [wyszukiwarkę na
abcnotation.com](http://abcnotation.com/search). Jedną z głównych przeszkód
w dzieleniu się nutami (niezależnie od formatu) jest ochrona praw autorskich.
Dlatego też istniejące społeczności skupiają się na muzyce która nie jest
chroniona prawami autorskimi, czyli w większości na muzyce ludowej. Na przykład
[The Session](http://thesession.org) skupia się na ludowej muzyce irlandzkiej.
Szukałem polskiego odpowiednika, ale nie znalazłem.

Dotychczas używałem ABC tylko do eksperymentów: spisałem kilka utworów ze
słuchu. Niestety nie mogę tych nut opublikować z wiadomych względów.

Podczas wpisywania nut w formacie ABC brakuje mi sprzężenia zwrotnego. Kiedy
piszę nuty w [MuseScore](http://musescore.org/), program odgrywa każdą nowo
postawioną nutę. Jeżeli postawię zły dźwięk, od razu to słyszę. W ABC natomiast
piszę w ogólnym edytorze tekstowym, i w najlepszym przypadku mogę podglądać
automatycznie aktualizujący się obrazek, na przykład na drawthedots.com.

Przetestowałem z sukcesem taką ścieżkę:

1. Wklepanie do MuseScore
1. Zapisanie jako MusicXML
1. [Konwersja z MusicXML do ABC](http://wim.vree.org/svgParse/xml2abc.html)
1. Ręczne wyczyszczenie pliku ABC

Trochę naokoło, ale działa.

## Narzędzia

* [opis standardu](http://abcnotation.com/wiki/abc:standard:v2.1), instrukcja
* [konwersja z ABC](http://abc2xml.appspot.com/)
* [abcplus](http://abcplus.sourceforge.net/) -- lista narzędzi
* [abcm2ps][] -- z ABC do grafiki
* [drawthedots.com](http://www.drawthedots.com) -- pisanie ABC w przeglądarce

[Notacja ABC]: http://abcnotation.com/
[abcm2ps]: http://moinejf.free.fr/ "ABC → obrazek"
