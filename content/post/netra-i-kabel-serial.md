+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2008-05-16T09:24:01"
draft = false
title = "Netra i kabel serial"
+++
Pochylony nad biurkiem, roztaczałem zapach spalenizny, próbując trafić
lutownicą (ale nie pistoletową, tylko taką kolbą) w jedną z nóżek złącza
RS-232.

„Jestem już w połowie!” - powiedziałem, kiedy czwarty kabelek zaczął sprawiać
wrażenie trzymania się nóżki.

„Mam nadzieję że nie jesteś z tych, co to myślą że zlutują i zadziała od
pierwszego razu, co?” - przyjaźnie zagaił kolega.

Pytanie uznałem retoryczne i
[lutowałem](http://automaciej.jogger.pl/2006/09/12/lutowanie/) dalej. Po
zakończeniu, dzieło wyglądało tak:

![](http://media.blizinski.pl/images/blog/netra-serial-cable.jpg)

Dlaczego musiałem lutować? Otóż, o ile _zasadniczo_, jak lubi mawiać mój były
szef, maszyny Suna mają port serial kompatybilny z Cisco, to Netry są inne.
Netry są szczególnym przypadkiem.

`[citation needed]?` Można porównać złącze
[Cisco](http://pinouts.ws/cisco-console-rj45-db9-cable-pinout.html) vs
[Netra](http://devin.com/debian/debian-on-netra.html).

Kiedy skończyłem lutować, nie mając lepszego pomysłu, po prostu podłączyłem
kabel, odpaliłem `minicom`, podałem urządzenie `/dev/ttyUSB0`, ustawiłem
parametry na 9600 8N1 i...

...zadziałało od pierwszego razu!

`lom>poweron  
lom>  
LOM event: +21h13m51s host power on  
.  
Netra T1 200 (UltraSPARC-IIe 500MHz), No Keyboard  
OpenBoot 4.0, 1024 MB memory installed, Serial #51117387.  
Ethernet address 0:3:ba:b:fd:4b, Host ID: 830bfd4b.  
  
  
  
  
ok probe-scsi  
Target 1  
Unit 0 Disk FUJITSU MAJ3182M SUN18G 0804  
ok █`

LOM to ciekawy patent. Mogę nie tylko zdalnie wyłączyć komputer, ale również
go _włączyć_. Oczywiście pod warunkiem, że kabel zasilający jest wetknięty do
gniazdka i mam dostęp do portu serial.

Koleżanka doradza zlutowanie jeszcze ze dwóch takich kabli. Tak na wszelki
wypadek.

# Komentarze

* GiM (2008-05-18 11:52:25): <p>Niech żyje nasz przodownik pracy! ;)</p>
* lordmac (2008-05-19 10:56:41): <p>A jeszcze fajnieszy jest patent z Net
  management &#8211; ustawiasz w <span class="caps">ALOM</span> numer IP portu
  NetMGMT i masz konsole po sieci :)</p>
* burbie (2008-05-20 00:02:46): <p>Najbardziej podoba mi się to, że na zdjęciu
  punkty lutownicze są tak&#8230;. hm, dyskretnie ukryte :)</p>
