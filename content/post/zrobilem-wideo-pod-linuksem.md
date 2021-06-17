+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2012-09-02T23:47:32"
draft = false
title = "Zrobiłem wideo pod Linuksem"
tags = [ "informatyka", "muzyka", ]
+++

Właściwie wszystko od początku do końca. Na występnie nagrałem obraz na
lustrzance cyfrowej, koledzy pomogli nagrywając dodatkowe zdjęcia przy na
telefonach komórkowych. Dźwięk nagrałem na żywo na miejscu. Montaż wideo
i mastering audio też zrobiłem sam, w sensie technicznym. W sensie koncepcyjnym
montażu pomagała mi swoimi wskazówkami [sama
artystka](http://www.youtube.com/user/wobblyfin).

<iframe width="560" height="315" src="https://www.youtube.com/embed/9xuCkNZqmS0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

Celem ćwiczenia było sprawdzenie uda się to w ogóle zrobić, czy też nie: jedna
lustrzanka, 3 telefony, ani centa wydanego na oprogramowanie, i wszystko
zrobione 100% legalnie i koszernie. No i udało się, przy pomocy Linuksa i
wolnego oprogramowania.

Największy problem był ze znalezieniem edytora wideo. Próbowałem programów
takich jak cinelerra i pitivi. Cinelerra się co chwilę wywalała, a pitivi nie
było w stanie zrenderować wynikowego wideo. W końcu stanęło na Blenderze,
który jest zasadniczo programem do grafiki 3D, któremu przez przypadek wyrosła
przyczłapka do edycji wideo. Traf chciał, że jest to najlepszy edytor jaki
jest dostępny pod Linuksem. O ile pitivi można zainstalować i od razu użyć,
Blender zdecydowanie wymagał wspięcia się na ostrą krzywą uczenia. Zajęło mi
to kilka wieczorów, ale stwierdzam że warto było, bo po nauczeniu się skrótów
klawiaturowych ‒ a w Blenderze inaczej się nie da ‒ edytowanie wideo przebiega
bardzo efektywnie.

Z paru sztuczek które zrobiłem, to np. trzymanie materiałów źródłowych na
macierzy dyskowej na osobnej maszynie, podpiętej przez gigabitowy ethernet. W
ten sposób maszyna na której chodził Blender, miała dużo mniej mielenia
dyskami.

Jakiego sprzętu użyłem, nie napiszę ponieważ za sprzęt zapłaciłem, więc
producenci dostali już moją porcję brzęczącej wdzięczności. Co innego z
oprogramowaniem! Oto, czego użyłem:

  * [Blender](http://www.blender.org/) ‒ montaż wideo
  * [Audacity](http://audacity.sourceforge.net/) ‒ wstępne przetwarzanie audio
  * [JAMin](http://jamin.sourceforge.net/) \+ [JACK](http://jackaudio.org/) \+ [ardour](http://ardour.org/) ‒ mastering audio
  * [ffmpeg](http://ffmpeg.org/) (avconv) ‒ kodowanie audio i wideo
  * [Ubuntu 12.04](http://www.ubuntu.com/)

Czego by o multimediach pod Linuksem nie mówić (trochę się w trakcie nakląłem,
nie zaprzeczam), wiem że mam już stopę w drzwiach i kolejne podejścia będą
tylko lepsze.

----
**Komentarze**

* torero (2012-09-03 07:56:22): <p>Niedobrze z tą cinelerrą, niedobrze...
  właśnie mam trochę materiału z występów dziecka i miałem zacząć się jej uczyć,
  bo czytałem, ze ponoć przezaawansowany :( OTOH ucząc się Blendera w jednej
  umiejętności będę teraz miał od razu dwie :)</p>
* Burro (2012-09-03 09:51:18): <p>Dzięki. Przyda się zwłaszcza, że pewnie sam
  bym się za Blendera nie zabrał w tym kontekście. :)</p>
* 3B| (2012-09-03 09:53:09): <p>Testowałeś może <a
  href="http://www.openshotvideo.com/" rel="nofollow">OpenShot</a>? Ja go kilka
  razy używałem i wydawał się stabilny. Nie wiem jak z zaawansowanymi funkcjami,
  ale do zastosowań amatorskich mi wystarcza.</p>
* occulkot (2012-09-03 10:00:52): <p>Ja filmiki ostatnio montuje w kdenlive.
  Duzo efektow przejsc, mozliwosc pracy z klipami "proxy" (gorsza jakosc,
  szybszy rendering). W dodatku bardzo stabilne nawet przy duzym
  projekcie.Openshot sprawdzalem, jest w porownaniu z kdenlive uproszczony,
  mniej opcji przelotow itd.</p>
* dobeer (2012-09-03 11:02:56): <p>Czepie się deprecjonowania Blendera, że to
  niby 3D z przyrostami ;) Generalnie to był i jest zestaw narzędzi do tworzenia
  animacji. Inna sprawa, że użytkownicy zazwyczaj ograniczają się do
  wykorzystania go tylko do "czyde". A i z klikaniem myszką da się go używać,
  tylko klawiszami zdecydowanie łatwiej.<br /> BTW. Generowałeś gotowy plik
  wideo czy obrazki i później to konwertowałeś jakimś kodekiem? Pytam, bo mnie
  ostatnim razem brzydko przycinał wideo, pomogło dopiero kodowanie przez jpeg-i
  ffmpeg-iem (tu nie jestem pewien przyczyny, może to wina sprzętu na którym
  działał blender, ale ffmpeg pomógł).</p>
* automaciej (2012-09-03 11:25:07): <p>dobeer, czy w Blenderze da się w miarę
  prosto zrobić animację 2D? Np. taką jakiej elementy widać w Storm
  (http://youtu.be/HhGuXCuDb1U)</p>  <p>Co do eksportowania, to eksportowałem od
  razu docelowe wideo, w kodeku H.264, a dźwięk w PCM. Z wideo nie było żadnych
  problemów, poza tylko momentem kiedy zauważyłem że rozdzielczość jest nie do
  końca taka jak chciałem, i znalazłem ustawienie gdzie się ustawia wielkość
  renderu w procentach docelowej rozdzielczości, domyślnie 50% (dlaczego?!).</p>
  <p>Dźwięk przygotowywałem osobno, a potem wszystko złożyłem w całość przy
  pomoc ffmpeg/avconv.</p>
* dobeer (2012-09-03 11:50:57): <p>I tak i nie :) Da się zrobić, raczej nie
  będzie to proste. Blender jest bardzo rozbudowanym narzędziem i nawet proste
  rzeczy potrafią być tam nieoczywiste. Dodam tylko, że w gałęzi 2.6 i tak jest
  łatwiej niż 2.4 (jak to przeczyta stary wyjadacz, to może się niezgodzić, ale
  dla nowych użytkowników jednak 2.6 jest łatwiejsza)</p>  <p>Co do domyślnych
  ustawień na 50%, tak już jest bo do modelowania najczęściej trzeba na szybko
  coś podejrzeć, wiec to takie pójście na rękę co by nie marnować zasobów na
  pełnowymiarowe podglądy. Do finalnych renderów i tak najczęściej się siedzi i
  dłubie własne optymalne ustawienia.</p>
* automaciej (2012-09-23 09:28:24): <p>Jeżeli chodzi o robienie animacji 2D, czy
  są jakieś inne programy które są prostsze niż Blender?</p>
