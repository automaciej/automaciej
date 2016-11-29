+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2008-04-13T14:43:19"
title = "Własna podsieć IPv6"
tags = [ "informatyka" ]

+++
Po tygodniu używania tunelu IPv6 dostałem własną podsieć `/48`, co oznacza że
mam do dyspozycji 128 - 48 = 80 bitów, czyli 280 adresów. To z grubsza tyle,
ile 280 trylionów współczesnych Internetów. W najbliższym tygodniu adresy mi
się raczej nie skończą.

<!--more-->

Żeby z komputera zrobić router IPv6, wystarczy program `radvd`, do niego
[prosta konfiguracja](http://www.gentoo.org/doc/en/ipv6.xml#doc_chap5) i
router gotowy. Można wszystkim komputerom w LANie przypisywać adresy IPv6 i
wszystkie są od razu routowalne na świat.

I oto, co się teraz wyprawia:

  * dodatkowy gigabajt RAMu
  * Solaris 10 na vmware, z adresem IPv6
  * [linphone](http://www.linphone.org/index.php/eng) (VoIP obsługujący IPv6)
  * [wspólna sesja screen](http://linuxhacks.org/tutorials/jakes_gnu_screen_tutorial.php)

I można prowadzić rozkminki we dwójkę, nucąc sobie pod nosem:

# Komentarze

* grigorij (2008-04-13 15:26:58): <p>Chyba też sobie &#8222;założe&#8221; taki
  Internet w domu.. Myślę że tyle adresów w sam raz mi wystarczy;)</p>
* Zal (2008-05-13 00:33:26): <p>Woah! To 2^16 razy więcej adresów, niźli ja mam
  do dyspozycji ;D A jak przyjemnie wejść na serwer IRC-a z obsługą IPv6 i
  własnym wpisem revDNS :]</p>
* xnmrphr (2009-08-26 10:06:44): <p>Ja tylko dodam ":-)" </p>
