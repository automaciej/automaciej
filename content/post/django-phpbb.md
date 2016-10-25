+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2008-11-25T10:23:01"
title = "django-phpbb"
tags = [ "raptularz" ]

+++
Mój mały projekcik osiągnął już z grubsza używaną postać. Jest to [integracja
Django z phpBB](http://code.google.com/p/django-phpbb/), czyli zbiór klas które
pozwalają odczytywać wątki i posty oraz backend do uwierzytelniania użytkowników
(ang. authentication).

W praktyce oznacza to, że można się z poziomu Django podłączyć do
niezmodyfikowanej bazy danych phpBB3 i napisać aplikację w Django do której
można się zalogować tym samym loginem i hasłem co do forum.
