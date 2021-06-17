+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2012-12-02T21:00:16"
draft = false
title = "Solaris 10: Budowanie pakietów"
+++
_UWAGA: Temat bardzo, bardzo niszowy. Jeżeli nie interesuje cię budowanie
pakietów pod Solarisem, nie czytaj dalej._

Oto 25-minutowa prezentacja, w której zaczynamy od świeżo zainstalowanego
systemu, do którego nawet nie można się zalogować przez SSH, a kończymy ze
zbudowanym pakietem.

Screencast jest skrócony; jest jedna operacja -- pobranie definicji pakietów
-- która zajmuje około pół godziny nawet przy szybkim komputerze i dobrym
łączu internetowym. Tego typu fragmenty wyciąłem. Oryginalnie całość zajęła mi
około godziny. Podejrzewam że ktoś kto nigdy nie robił pakietów, powinien
zarezerwować na podobne ćwiczenie około dwóch godzin.

Rzeczy potrzebne do zrobienia tego co pokazałem na screencaście:

  * Zainstalowany Solaris 10 (np. na VirtualBox)
  * Dostęp do konta root na tym systemie
  * Dostęp do internetu pozwalający na ściągnięcie kilkudziesięciu (kilkuset?) MB
  * Wolne 2h

Linkografia:

  * [OpenCSW](http://www.opencsw.org/)
  * [GAR](http://gar.opencsw.org/) -- [GAR setup](http://sourceforge.net/apps/trac/gar/wiki/GarSetup)
  * [OpenCSW wiki](http://wiki.opencsw.org/)
  * [OpenCSW i Puppet](http://www.opencsw.org/community/questions/38/how-to-install-opencsw-packages-with-puppet) (do zarządzania flotą Solarisów)

Jest sporo rzeczy, których na screencaście nie przedstawiłem, a mogły by być
interesujące:

  * przygotowywanie VirtualBox w formie headless (czyli na serwerze, bez
    monitora) -- chociaż ten temat już raz [zdążyłem
    opisać](http://automatthias.wordpress.com/2012/03/10/headless-virtualbox-setup/)
  * instalowanie Solarisa (może jednak wcale nie takie interesujące)
  * łatanie kodu, który nie chce się skompilować (tyleż interesujące, co
    bolesne)
  * budowa bardziej złożonego pakietu, z bibliotekami i plikami nagłówkowymi
  * dodawanie skryptów pre/postinstall i skryptów startowych
  * zakładanie lokalnej bazy danych umożliwiającej sprawdzanie poprawności
    pakietów
  * jak zrobiłem screencast pod Linuksem, temat obszerny sam w sobie, no i mocno
    meta

Bliżej zainteresowanych tematem zapraszam na kanał [#opencsw na
Freenode](http://www.opencsw.org/support/irc-channel/ "Kanał anglojęzyczny" ).

----
**Komentarze**

* Argon (2012-12-08 15:41:55): <p>Podziękował bardzo, za Usable Solaris.
  Przyszedł czas odkurzyć starą maszynę i trochę z nią porządków zrobić. A
  pakiety, cóż, jeśli czas pozwoli…</p>
