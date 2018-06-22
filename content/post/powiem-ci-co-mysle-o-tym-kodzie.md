+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2008-10-19T13:34:32"
draft = false
title = "Powiem ci, co myślę o tym kodzie"
+++
_Opinie przedstawione w tym poście są moimi własnymi opiniami i nie
reprezentują opinii mojego pracodawcy, etcetera, etcetera. Khy, khy._

Czyż to nie jest czysta przyjemność, zakładać nowy projekt?

Taki czyściutki i świeżutki, z pustą stroną główną i dziewiczym repozytorium
kodu. Moment który spodziewamy się kiedyś wspominać: „A pamiętasz jak
zakładaliśmy ten projekt? To były czasy...”

Czy kilka klas pozwalających na integrację Django z phpBB jest wystarczającym
powodem do założenia nowego projektu... można by dyskutować. Jak się widzi
projekt [django-search](http://code.google.com/p/django-search/) obok projektu
[djangosearch](http://code.google.com/p/djangosearch/), to człowiek się
zastanawia, dlaczego koledzy się nie dogadali i nie połączyli wysiłków. Ale
może sama konkurencja jest dobra. W moim przypadku sam port phpBB-owej klasy
do sprawdzania haseł jest tego wart. Tak myślę. Ahem.

_Nawiasem mówiąc, sam napisałem kiedyś [django-
search](http://code.blizinski.pl/django-search/). Ale to było zanim jeszcze
tamte dwa ujrzały światło dzienne. Teraz pewnie skorzystałbym z gotowców._

Zakładając projekt, trzeba wybrać miejsce. Gdzie go założyć: na SourceForge,
BerliOS, a może jeszcze gdzieś indziej? Ale zacznijmy od innej opowieści.

Niedawno robiłem małą, 15-minutową [prezentację o testowaniu skryptów
shellowych](http://media.blizinski.pl/writing/shunit2.pdf) na spotkaniu ILUG.
Przychodzę, witam się, pomagam przenosić stoły i ustawiać krzesła, siadam i
patrzę jak gospodarz zaczyna mnie zapowiadać. I nagle słyszę coś takiego:

— Maciek będzie opowiadał o testowaniu skryptów shellowych w Google i innych
technikach programowania które są tam używane.

M... mmmomencik, ja wcale nie zapowiadałem że będę coś mówić o Google. To jest
zwykła prezentacja testowania zwykłych skryptów shellowych używając open-
source'owego projektu.

Widocznie, jak ktoś pracuje dla Google, to ludzie zaraz chcą żeby opowiadał o
jakichś cudach-niewidach. Być może dlatego, że myślą, że w Google się właśnie
na takich cudach-niewidach opiera. Google generalnie skąpi informacji o
detalach technicznych, a będąc firmą na której ludzie skupiają dużo uwagi,
staje się obiektem wszelkiego rodzaju domysłów i teorii spiskowych. Co jakiś
czas jednak zdarza się, że ktoś z Google opowiada o tym, że jakąś tam rzecz
robi się tam tak to a tak. Przykładem może być publikacja o
[Bigtable](http://labs.google.com/papers/bigtable.html). Ale apetyt na cuda-
niewidy nie słabnie. Wszyscy chcą wiedzieć, jak to jest że programy Google
dobrze działają. Odpowiedź: bo w Google pisze się dużo [unit-
testów](http://pl.wikipedia.org/wiki/Test_jednostkowy). Na to ludzie wzruszają
ramionami i mówią „testów śmestów”. I potem po cichu: „pewnie wcale nie o to
chodzi”.

Być może sekret polega na tym, że w Google testy te są pisane _naprawdę_.
Autentycznie, powstaje dużo dość grubaśnych plików kończących się na przykład
na `_test.py`. Jeżeli ktoś pisze kod do którego nie ma testów, jego koledzy po
prostu nie wpuszczają tego kodu do repozytorium. Proste.

Ciekawą rzeczą jest ten właśnie mechanizm wpuszczania kodu do repozytorium.
Oprócz testów, drugą interesującą rzeczą są _recenzje kodu_.

Ponad rok temu pisałem o swoim kontrakcie w UCD i problemach które tam miałem.
Problemy były typowe dla hermetycznego zespołu. Kod rozwijany przez 3 lata
niemal wyłącznie przez jednego człowieka. Być może samo w sobie nie musi to
być niczym złym, ale projekt prowadzony w ten sposób ma tyle okazji do zejścia
na manowce, że trudno mu jest przynajmniej jednej nie wykorzystać.

[Mistrz Foo](http://www.catb.org/~esr/writings/unix-koans/) mawiał, że nawet
jeżeli cały program składa się z trzech linijek, nadejdzie taki dzień, że
trzeba go będzie naprawiać.

Jeżeli nad jakimś kodem przez 3 lata pracuje tylko jedna osoba, każda nowa
osoba która usiądzie do kodu i będzie próbowała go zrozumieć, szybko przejdzie
do wyrywania sobie włosów z głowy. Nie oznacza to żadnej winy czy
niekompetencji po stronie autora kodu. Takie są po prostu prawa natury.

Repozytorium kodu jest cierpliwe, wszystko przyjmie. Kod nawet nie musi się
kompilować. Wciskamy „commit” i „gotowe”!

Nie mówię tutaj, że jedna osoba nie może napisać kodu który będzie dobrze
działać. Do pewnego rozmiaru projektów, jest to prawda (im projekt większy,
tym jest trudniej). Pojedyncza osoba może napisać bardzo dobrze działający
kod. Projekty pisane w ten sposób, o ile autor pracuje spójnie i
konsekwentnie, mają tę zaletę że są dobrze zaprojektowane. Ale dzień ma tylko
24 godziny, jedna osoba wielkiego projektu nie uciągnie.

Dorzucenie dodatkowych osób do projektu niekoniecznie rozwiązuje problem.
Powstaje spaghetti, w którym pojedyncze osoby robiły przypadkowe poprawki tu i
tam, nie przejmując się, jak to się ma do całości. Lub nawet nie tyle nie
przejmując się, ile po prostu fizycznie nie będąc w stanie w krótkim czasie
tej całości ogarnąć, na przykład z powodu braku dobrej dokumentacji. Czytanie
i analiza całego kodu rzadko wchodzi w rachubę. (Co? Przez cały miesiąc
będziesz siedzieć i czytać kod?)

Jeżeli do projektu nad którym pracowała jedna osoba dorzucimy drugą,
gwarantuję, że po pierwszym dniu będzie się drapać w brodę, marszczyć brwi i
nerwowo bębnić palcami po stole, a po drugim wyrywać sobie włosy z głowy.
Jeżeli wszystko pójdzie dobrze, po jakimś czasie ilość wyrywanych włosów
będzie malała, dokumentacja będzie się poprawiać. Jeżeli nie wszystko pójdzie
dobrze, wyrywania włosów będzie [coraz
więcej](http://automaciej.jogger.pl/2007/05/07/metoda-przezycia/).

Jeżeli kod ma być strawny dla nie jednej, ale grupy osób, nie ma innej rady,
jak rozmowa pomiędzy członkami tej grupy i osiągnięcie konsensusu. Oznacza to
między innymi ewentualną mocną krytykę kodu, i jeżeli ktoś nigdy wcześniej nie
widział jak się krytykuje jego kod, może to być dość przykre i może być
potrzeba czasu na wyrobienie sobie dystansu. (Co? _Mój_ kod jest
niedoskonały!?)

Krytyka powinna być konstruktywna, i mówić o konkretnych sprawach. Dlaczego ta
funkcja nazywa się tak to a tak, skoro robi to i to? Masz spacje na końcu
linii. Ten fragment nadaje się na osobną funkcję. Czy musisz używać tutaj
zmiennej globalnej? Tego tutaj kawałka nie musisz implementować, jest do tego
gotowy moduł. Co będzie jeżeli ktoś uruchomi dwie instancje tego skryptu
naraz? I tak dalej...

Żeby rozmowy o kodzie włączyć do codziennej pracy, sama chęć nie wystarczy.
Potrzebne są narzędzia. Guido van Rossum stwierdził, że fajnie będzie takie
coś napisać. Usiadł więc i napisał. Nazwał swoje dzieło Mondrian, na cześć
[malarza lubiącego prostokąty](http://pl.wikipedia.org/wiki/Piet_Mondrian). Na
YouTube jest godzinna prezentacja, podczas której Guido szczegółowo
[opowiada](http://www.youtube.com/watch?v=sMql3Di4Kgc "Ale to jest po
angielsku!" ) o Mondrianie i recenzjach kodu w Google. Tak, tym razem jest to
prezentacja o tym _jak to się w Google robi_. Jest też [dokumentacja on-
line](http://code.google.com/p/support/wiki/CodeReviews).

Zaraz, chwileczkę, jaka dokumentacja on-line, przecież to jest wewnętrzne
narzędzie Google! Otóż niekoniecznie. Narzędzie do recenzji kodu zostało
zintegrowane z `code.google.com`.

Są oczywiście różnice pomiędzy wersją wewnętrzną i zewnętrzną, ale wynikają
głównie z różnych środowisk. Wersja wewnętrzna jest mocno zintegrowana z
okolicznymi narzędziami i umożliwia recenzje pre-commit, czyli przed wysłaniem
kodu do repozytorium. W Internecie, środowisku bardziej rozproszonym,
implementacja tego jest trudna, a w praktyce niemożliwa. Narzędzia takie jak
`svn` musiałyby wysyłać aktualny diff na serwer, z możliwością łatwiej
aktualizacji.. Na `code.google.com` recenzje są więc robione post-commit.

Użycie jest proste: przeglądamy repozytorium, wykonujemy dwuklik na linijce
którą chcemy skomentować i wpisujemy tekst. W ten sposób każda linijka może
być początkiem wątku dyskusji. Kiedy już skomentujemy wszystkie miejsca które
nas interesują, wysyłamy całość - wszystkie komentarze naraz tworzą „paczkę”,
całość. Podobnie z odpowiedziami.

Pamiętam jak profesor z UCD opowiadał mi o swoich wysiłkach, żeby kod projektu
był przeglądany przez wiele osób, dobrze udokumentowany, i tak dalej. Był
trochę jak Charles Babbage: miał całą wiedzę i teorię. Brakowało tylko
technologii.
