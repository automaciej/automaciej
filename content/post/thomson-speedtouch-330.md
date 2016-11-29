+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2005-10-17T07:11:31"
title = "Thomson Speedtouch 330"
tags = [ "zrzędzenie", "informatyka" ]

+++
Po przeprowadzce w nowe miejsce musiałem sobie zorganizować dostęp do
Macierzy, a jedyną możliwością jest Neostrada. Podobno idą obok linie Netii,
ale dzwoniłem do nich i twierdzili że nie mają tu warunków technicznych
(technologii miedzianej...?).

<!--more-->

Instalacja linii telefonicznej od &amp;TP odbyła się w tydzień po przyjęciu
zgłoszenia. Jeszcze tego samego dnia przyniosłem do domu pudełko z modemem i
musiałem tylko czekać na podłączenie w centrali.

&amp;TP dostarcza sterowniki do Linuksa. Próbowałem instalować - nie działają.
Miałem wrażenie, że były to sterowniki dla jądra 2.4 a ja mam 2.6. Wygooglałem
chyba z tuzin instrukcji, niektórych mocno różniących się od siebie i
próbowałem ich po kolei. Próbowałem skryptów speedtouchconf, speedtouchconfsh
i zawsze kończyłem z jakiimś komunikatem o błędzie który po wklejeniu do
Google nie dawał żadnych sensownych wyników. Najczęściej trafiałem na posty
usenetowe ludzi mających ten sam problem co ja, bez rozwiązania.

Po obejrzeniu wszystkich tutoriali przeczytałem nagle na usenecie pierwszą
użyteczną informację: są DWA sterowniki do Speedtoucha, jeden w postaci modułu
jądra a drugi w postaci programu przestrzeni użytkownika. Instalowanie ich naraz
nie ma sensu, oczywiście. [Najlepszy
tutorial](http://www.fedora.pl/index.php?option=content&task=view&id=98&Itemid=34)
dla Neostrady jaki znalazłem opisuje dokładnie, w jaki sposób przygotować pliki
z firmware. Musiałem tylko zauważyć (co mi zajęło z godzinę) że pliki z firmware
muszę skopiować do trochę innego katalogu niż pisali w tym tutorialu. Skrypty
hotplug w różnych dystrybucjach mają różnie zdefiniowaną zmienną FIRMWARE\_DIR.

Po tych wszystkich zmaganiach mam już chodzący modem, nawet napisałem sobie
specjalny skrypt dla hotpluga, który uruchamia modem po włożeniu wtyczki lub
przy uruchomieniu komputera. Teraz mam dylemat: Czy próbować opisać moje
doświadczenia i wystawić gdzieś w internecie? Na NIE widzę: będzie to kolejny
tutorial z tysiąca. Opiszę w nim rzeczy które zadziałały dla mnie, a które nie
wiadomo czy zadziałają i kogoś innego (inna wersja jądra, inna wersj modemu,
etc). Na TAK natomiast: pozbierałem różne użyteczne informacje z sieci, zebranie
ich w jednym miejscu jest dobrą rzeczą. Mogę też w tutorialu napisać dokładne
instrukcje sprawdzania różnych rzeczy, np. wersji jądra czy wersji modemu.

Pisać, czy nie pisać? Oto jest pytanie...

# Komentarze

* Zakrn (2005-10-17 07:59:53): <p>Od jądra 2.6.12.4 sterowniki są do
  wkompilowania w jądrze. A co do artu - przyda się, jeżeli nie będzie powtórką
  tego, co już jest na sieci. Swoją drogą, jak ja pierwszy raz instalowałem
  speedtocuha na 2.4 to musiałem nieźle się nakombinować, bo żaden z opisanych
  sposobów mi w pełni nie działał.</p>
