+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2005-08-20T10:52:58"
title = "Miksowanie w ALSA"
tags = [ "informatyka" ]

+++
Dopiero wczoraj wpadłem na opis wtyczki
[dmix](http://alsa.opensrc.org/index.php?page=DmixPlugin) do sterowników
dźwięku ALSA. Wtyczka potrafi miksować wyjście z wielu programów
korzystających z wyjścia dźwiękowego i odgrywać je na pojedynczym urządzeniu
dźwiękowym. W 1.0.9rc2 podobno dmix jest włączony na stałe dla wszystkich kart
które nie obsługują miksowania sprzętowego.  
Brzmi pięknie, ale u mnie nie jest różowo. Wpisałem co trzeba do ~/.asoundrc i
przy próbie odtwarzania programy zachowują się dość dziwnie. Na przykład:
"aoss mpg321 -o oss piosenka1.mp3" - słychać piosenkę1. Na drugim terminalu:
"aoss mpg321 -o oss piosenka2.mp3" \- nie słychać piosenki2. Zatrzymuję
piosenkę1 przy pomocy CTRL+C - piosenka2 staje się słyszalna. Uruchamiam
piosenkę1 jeszcze raz - cała odtwarza się jak na "fast forward", w ciągu 5
sekund.  

Czasami rzeczywiście można usłyszeć 2 piosenki naraz, ale nie umiem tego
zrobić na zawołanie; albo wychodzi albo nie.

# Komentarze

* Dexter (MG) (2005-08-20 12:43:31): <p>dmix działa, dopóki masz dwa głośniki,
  wszystko odtwarza w alsę a nie jakieś ossy i nie masz jakichś fanaberii w
  asoundrc. W znakomitej więkoszości pozostałych przypadków - ssie. ;)</p>
