+++
date = "2008-05-19T20:12:55"
draft = false
title = "JumpStart"
aliases = [ "/2008/05/jumpstart/",]

+++

_Nie, to nie jest odkurzacz. Odkurzacz ma rurę. Tak, dźwięk wydaje podobny._

Moja Netra T1 jest maszyną nieco autystyczną. Porozumiewa się ze światem przez
port szeregowy, USB, SCSI i dwie sieciówki. Nie ma karty graficznej, ani
klawiatury. O karcie dźwiękowej nie wspomnę. Nie ma również CD-ROMu, co nieco
utrudnia instalację systemu.

Okazuje się, że jednak się da.
[JumpStart](http://www.sun.com/bigadmin/content/jet/) umożliwia zbootowanie
maszyny przez sieć i zainstalowanie systemu. Przy odrobinie przygotowań może
się to odbyć zupełnie bezobsługowo, od zbootowania do gotowego systemu z
ustawionym hasłem roota i dostępem przez ssh.

    
    
    JumpStart is complete @ Mon May 19 11:29:19 IST 2008
    netra console login:█
    

Instalacja była serwowana z Solarisa na VMWare Server, na moim laptopie x86.
Później z rozpędu próbowałem instalować Solarisa x86 na drugiej maszynie
wirtualnej, co się zasadniczo udało, ale niestety nie bezobsługowo. Po
zbootowaniu z sieci dostałem menu, z którego musiałem wybrać rodzaj
instalacji, a potem jeszcze pytanie o datę i godzinę.

Druga rzecz której jeszcze nie opanowałem, to wybieranie pakietów do
instalacji. Solaris _zasadniczo_ ma system pakietów, ale ten system niestety
nie potrafi pomóc w rozwiązywaniu zależności. A z domyślnych profili
instalacji jest albo instalacja tak minimalna, że nie ma ssh ani nawet basha
(uch...), albo od razu instalacja pełna, czyli 3GB towaru, który jest w dużej
większości niepotrzebny.

    
    
    SUNWxorg-clientlibs..............done.  2222.59 Mbytes remaining.
    SUNWlexpt........................done.  2222.06 Mbytes remaining.
    SUNWfontconfig-root..............done.  2221.99 Mbytes remaining.
    SUNWfontconfig...................done.  2221.20 Mbytes remaining.
    SUNWgnome-base-libs..............done.  2206.11 Mbytes remaining.
    SUNWgnome-a11y-base-libs.........done.  2205.51 Mbytes remaining.
    SUNWgnome-audio..................done.  2205.16 Mbytes remaining.
    

A na maszynie z 400MHz-owym procesorem instaluje się to w nieskończoność. Bo
co tu się oszukiwać. Netra jest powolna!

Chciałoby się więc przygotować własny profil, np. instalacja typowego serwera,
z narzędziami takimi jak serwer ssh, bash, wget i vim. Ale żeby to zrobić,
trzeba mieć jakieś specjalne solarisowe pakiet-fu, którego jeszcze nie
opanowałem.

A na razie cieszę się że ożywiłem nową maszynę.

W następny weekend spróbuję pobawić się zone'ami.

----
**Komentarze**

* Bonjoure (2008-05-20 07:40:26): <p>No faktycznie! Gnome się przyda&#8230;
  ;)</p>
* el_pilar (2009-04-02 19:17:15): <p>Witam,<br /> jak u netry z poziomem
  głośności, mam zamiar kupić taką żeby<br /> potestować solarisa a później
  wrzucić debiana i niech pracuje<br /> jako router. Problem tylko w tym, że jak
  będzie za głośna to <br /> ludzie w jej pobliżu oszaleją...</p>
  <p>Pozdrawiam</p>
