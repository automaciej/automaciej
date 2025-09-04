+++
date = "2007-03-29T11:40:54"
draft = false
title = "Playstation 3: centrum obliczeniowe"
aliases = [ "/2007/03/playstation-3-centrum-obliczeniowe/",]

+++
Ostatnio zaczynam mieć chrapkę na PS3. Ta konsola do gier jest napędzana
potężnym procesorem [Cell](http://en.wikipedia.org/wiki/Cell_microprocessor).
Sprzęt jest _dotowany_, Sony sprzedaje poniżej kosztów ― dopłaca około $200 do
każdego egzemplarza.

Ma on dość złożoną architekturę: jeden 64-bitowy procesor typu PowerPC i
siedem dodatkowych procesorów zmiennoprzecinkowych (SPE). IBM udostępnia [Cell
SDK](http://www.alphaworks.ibm.com/tech/cellsw?open&S_TACT=105AGX16&S_CMP=DWPA
) z własnym kompilatorem C i C++.

Wciąż mam kilka pytań na temat PS3, na które nie mogę znaleźć odpowiedzi: Na
czym polega podział pamięci RAM w PS3? Czy aby wykorzystać pełną moc procesora
Cell wystarczy skompilować kod ichnim kompilatorem, czy kod musi być
specjalnie napisany? Czy GCC potrafi wykorzystać możliwości procesora Cell?

Projekt nad którym pracuję to jednowątkowy, sekwencyjny program, który wymaga
dużo mocy obliczeniowej. Prace nad wersją współbieżną utknęły. Może
uruchomienie go na PS3 pozwoliłoby zrobić obliczenia kilkukrotnie szybciej niż
obecnie?

UPDATE 2018-06-23: Oczywiście żadnych obliczeń na PS3 nigdy nie wykonywałem, bo
w momencie kiedy kupiłem konsolę, już nie pracowałem przy projekcie który by
tego mógł potrzebować. Pomiałem ją sobie lat ileś (10?), po czym w tym miesiącu
ją sprzedałem, za €28. Plus dwa kontrolery, plus wszystkie gry, dostałem
z powrotem €65. Aż śmiesznie. Ale przynajmniej pozbyłem się zawalidrogi.

----
**Komentarze**

* Cthulhu (2007-03-29 13:32:48): PS3 ma z tego co pamiętam 256mb pamięci dla
  grafiki i drugie tyle dla reszty.  
 No i znów wychodzi to, że ta konsola
  jest dobra do wszystkiego tylko nie do grania ;].  
 A programy muszą być
  specjalnie napisane, specjalnie skompilowane (ale gcc sobie z tym radzi).
  Jednowątkowy program nie wykorzysta mocy drzemiącej w Cellu.
* Hubert (2007-03-29 23:46:48): Przyznam, że wyrafinowana
  wymówka&#8230;;)
