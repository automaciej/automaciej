+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2007-05-17T00:33:10"
draft = false
title = "Któraż to godzina w Silicon Valley?"
+++

Jak sprawdzić godzinę, wie każde dziecko. Wystarczy wpisać w terminalu...

    
    
    
    maciej@clover ~ $ date
    Wed May 16 23:19:12 IST 2007
    
    

O, właśnie tak. Przy okazji dowiadujemy się z zaskoczeniem że został nam
podany czas IST, czyli Irish Summer Time. Ha! Lato idzie, Irlandia za oknem,
wszystko się zgadza.

A co jeżeli chcemy się dowiedzieć która godzina gdzieś w dalekim kraju
zamorskim? Albo wręcz zaoceanicznym? Wczoraj rozpracowaliśmy to z kolegą.
Wygląda to tak:

    
    
    
    maciej@clover ~ $ TZ=US/Pacific date
    Wed May 16 15:19:14 PDT 2007
    
    

Pięknie! PDT to Pacific Daylight Time, czas letni zachodniego wybrzeża USA.
PDT jest używany w Silicon Valley. Po krótkich poszukiwaniach znalazłem listę
miejsc i stref czasowych do których możemy się odwołać, wszystko jest w
katalogu /usr/share/zoneinfo.

    
    
    
    maciej@clover ~ $ TZ=Europe/Warsaw date
    Thu May 17 00:24:32 CEST 2007
    
    

Tak wygląda czas w pewnym mniej znanym kraju na obrzeżach Europy. Europa nas
nie ogranicza, możemy wybrać się dalej na wschód:

    
    
    
    maciej@clover ~ $ TZ=KGB date
    Wed May 16 22:25:14 KGB 2007
    
    

Jak widać, zawartość katalogu /usr/share/zoneinfo też nie stanowi bariery. Co
ciekawe, mechanizm ten potrafi poradzić sobie z napisami w UTF-8.

    
    
    
    maciej@clover ~ $ TZ="roku pańskiego" date
    Wed May 16 22:26:09 roku pańskiego 2007
    
    

# Komentarze

* Ja-Joanna (2007-05-17 01:04:31): <p>U mnie &#8222;roku pańskiego&#8221; nie
  działa. Podaje czas w <span class="caps">UTC</span>. Tzn. pisze: <span
  class="caps">UTC</span> 2007, a nie roku pańskiego<br /> zresztą roku
  pańskiego pojawia mi się jako &#8222;roku pa\305\204skiego&#8221; :(</p>
* mamaT (2007-05-17 09:13:03): <p>masz znakomity &#8222;pazur
  pedagogiczny&#8221; ;-) potrafisz zainteresować czlowieka. Moze nawet
  tępaka.</p>
* i0 (2007-05-17 11:56:09): <p>Ja-Joanna: locale ustawione na pl_PL.UTF-8? U
  mnie działa i się nie buntuje. ;&#62;</p>
* Cezary Okupski (2007-06-03 02:31:12): <p>Taka widać różnica w działaniu
  &#60;kbd&#62;date&#60;/kbd&#62; w <span class="caps">BSD</span> (także Mac OS
  X) od Linuksa. Potwierdzam efekt.</p>
