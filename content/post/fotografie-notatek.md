+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2007-07-16T03:18:43"
draft = false
title = "Fotografie notatek"
+++

O istotności tematu wrzucania notatek do komputera nie muszę przekonywać
żadnego studenta. Mógłbym spytać, jak im się czyta z ekranu fotografie
notatek, ale czy dobrze się je drukuje, pytać nie muszę.

Notatki są najczęściej nierówno oświetlone, jasne na środku, ciemne na
brzegach. Czasami są pogięte i różne fragmenty mają różną jasność. Kiedy
próbujemy poprawiać kontrast, to w jednym miejscu wychodzi dobrze, w innym
litery robią się bardzo blade, a w jeszcze innym tło robi się czarne.
Manipulacja samym kontrastem to za mało.

Dzisiaj miałem dokładnie ten problem i spędziłem chwilę nad tym żeby go
rozwiązać raz a dobrze. Rzecz nie jest bardzo skomplikowana i jest to filtr
górnoprzepustowy, po angielsku high-pass filter. Można taki znaleźć w postaci
pluginu do Gimpa, ale ja chciałem coś co zadziała jako skrypt. Udało mi się.
Potrzebne są:

  * Fotografia notatek
  * [ImageMagick](http://www.imagemagick.org/)

Krok 1: rozmazujemy obraz.

    convert photo.jpg -blur 0x120 blurry.jpg
    
Krok 2: robimy negatyw

    convert blurry.jpg -negate negative-blurry.jpg
    
Krok 3: nakładamy rozmazany negatyw na oryginał

    composite -dissolve 50% photo.jpg negative-blurry.jpg grayish.jpg
    
Krok 4: poprawiamy kontrast

    convert grayish.jpg -contrast-stretch 0x80% printable.jpg
    
Voila! Mój przykład jest trochę przesadzony, bo zawiera nierozprostowane
zagięcia; w przypadku typowych notatek efekt będzie jeszcze lepszy.

# Komentarze

* Barthalion (2007-07-16 07:04:32): <p>Świetny pomysł! W życiu bym na coś
  takiego nie wpadł.</p>
* D4rky (2007-07-16 15:04:02): <p>niezłe :)</p>
* Adex (2007-07-16 15:10:22): <p>Ciekawe, ciekawe&#8230; przyda się ;]</p>
* radmen (2007-07-16 16:16:09): <p>tru, dość ciekawe :)</p>
* G (2007-07-17 02:13:22): <p>++ <br /> :D</p>
* hcz (2007-07-17 18:50:39): <p>Naprawdę dobre. Przydałby się mały
  &#8222;podkład&#8221; teoretyczny lub przynajmniej link do takowego.</p>
* Automaciej (2007-07-21 19:59:00): <p>Nie znalazłem odpowiedniego linka. Ja
  wzorowałem się na tym przykładzie z Gimpa:<br />
  http://www.gimp.org/tutorials/Sketch_Effect/</p>    <p>Jeżeli chodzi o podkład
  teoretyczny, to wykorzystujemy tutaj taką właściwość tekstu, że interesujące
  nas elementy są wszystkie z grubsza jednego rozmiaru. Zakładamy, że obraz
  składa się z sumy dwóch obrazów: jeden z małymi elementami, a drugi z dużymi.
  Obraz z elementami dużymi możemy uzyskać przez rozmycie, a po odjęciu go od
  oryginału dostajemy obraz z samymi elementami małymi. Wielkość interesujących
  nas elementów wybieramy regulując promień rozmycia.</p>
* jachacy (2007-09-12 21:06:39): <p>Jakiej wersji ImageMagick używasz? U mnie
  rozmycie trwa min. minutę dla zdjęcia 3Mpx na procesorze 2Ghz. </p>  <p>Przy
  okazji zwraca: convert: unrecognized option `-contrast-stretch&#8217;.</p>
* Automaciej (2008-01-13 22:15:05): <p>ImageMagick 6.3.5.10.  Tak, rozmywanie
  jest potwornie powolne dla większych zdjęć.  Może warto poszukać innej,
  szybszej metody rozmywania.</p>
* vampire (2008-05-09 18:38:19): <p>moze byc szybciej jezeli uzyjesz filtra
  dolnoprzepustowego zamiast blura&#8230;</p>
* studentka (2009-01-16 17:47:01): <p>ciekawe. da się to zautomatyzować?</p>
* Automaciej (2009-01-17 13:00:10): <p>No ba!</p>
