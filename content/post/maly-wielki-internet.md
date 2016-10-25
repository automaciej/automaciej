+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2008-03-21T19:27:40"
title = "Mały wielki Internet"
tags = [ "opowieści", "informatyka" ]
+++
Kiedyś to były czasy. Prało się na tarce do prania, bo nie było jeszcze
pralek, i pocztę pisało się w pine, bo nie było jeszcze
[mutta](http://pl.wikipedia.org/wiki/Mutt), i robiło się wiele innych
niewygodnych rzeczy tylko dlatego, że się nie dało inaczej. Ale w nostalgii za
starymi czasami można zapomnieć, że teraz też są stare czasy! Pomyślcie tylko,
komputer z gigabajtem ramu. Ba, że kiedyś w ogóle się podawało ilość RAMu w
gigabajtach! I tak dalej.

Tak, teraz też są stare czasy, na przykład w Internecie są, aż śmieszne kiedy
się o tym pomyśli, tylko 4 miliardy adresów. Jest to tak żałośnie mało, że
podłączając swój dom do internetu dostaje się zaledwie _jeden_ adres, a
czasami nawet i tego nie. Do internetu jest podłączony tylko komputer, macie
pojęcie? A lodówka? A pralka? Przecież to śmieszne, żeby schodzić na dół i
sprawdzać czy pranie się skończyło... pralka której nie można nastawić ani
sprawdzić przez WWW? A żelazko? Nie można ze swojej komórki sprawdzić, czy nie
zostawiliśmy w domu włączonego żelazka? Naprawdę, ja nie wiem jak ludzie wtedy
żyli. To znaczy, teraz.

Pionierska żyłka odezwała się we mnie, kiedy znajomy opowiedział o tunelu
[IPv6](http://pl.wikipedia.org/wiki/IPv6), który sobie zestawił w domu.
Zamiast, jak każdy rozsądny człowiek, popukać się czoło i zapytać, kto tego
używa, poszedłem do [sixxs.net](http://www.sixxs.net/) i też [założyłem
sobie](http://www.sixxs.net/faq/account/?faq=10steps) taki tunel.

**Internet IPv6 jest wielki.** Na każdy milimetr powierzchni ziemi przypada 667
kwadrylionów adresów. Każdy włos na głowie każdego człowieka na kuli ziemskiej
może mieć własny adres IPv6. Nie tylko każdy włos na głowie, ale każda rzęsa,
każdy por w skórze, właściwie mogę bezpiecznie wymieniać wszystkie części ciała;
adresów nie zabraknie bo jest ich więcej niż atomów we Wszechświecie.
A konkretnie, tyle:

    python -c "print 2 ** 128"

Na czym dokładnie polega pionierska żyłka, trudno powiedzieć. Chyba na głębiej
nieuzasadnionej chęci robienia czegokolwiek nowego i mało popularnego, co
posiada potencjalną przewagę nad popularną alternatywą. Potencjalną przewagę
można oczywiście poznać po praktycznej ułomności.

**Internet IPv6 jest mały.** Kameralny. Prawie nikogo tam nie ma. I to jest
w nim fajne, bo jest trochę więcej przestrzeni i można odetchnąć. Czy na
powszechniejsze użycie się zanosi, trudno powiedzieć; jest to coś w rodzaju
problemu jajka i kury. Użytkownicy nie interesują się IPv6, bo nie ma tam nic,
czego oni by chcieli. Z kolei dostawcy tzw. _contentu_, czyli informacyjnej
karmy dla homo sapiens, nie umieszczają niczego w IPv6, bo nie ma użytkowników,
którzy z kolei... no, wiecie o chodzi.

Przejście na IPv6, jeżeli w ogóle, nastąpi prawdopodobnie nie w Europie, tylko
w Indiach albo Chinach, gdzie ludzie obecnie są popodłączani przez 7 warstw
NATu. Mogą się nagle wkurzyć, a że jest ich dużo... IPv4 może jeszcze przez parę
lat wytrzyma, ale [adresów ubywa, ubywa
i ubywa...](http://www.potaroo.net/tools/ipv4/index.html)

Tymczasem, co by nie mówić, jest kilka rzeczy które są już teraz dostępne po
IPv6, a niektóre _tylko_ po IPv6.

Na przykład, od niedawna można używać przez IPv6 wyszukiwarki Google, pod
adresem **ipv6.google.com** (można podejrzeć przez [bramę HTTP
IPv4](http://ipv6.google.com.ipv4.sixxs.org/)). Google w IPv6 można poznać po
animowanym logo.

Są też radia internetowe. Dlaczego akurat radia internetowe? Otóż w IPv6 jest
coś, co nazywa się _multicast_, i nie wdając się w szczegóły, powiem tylko że
jest to coś, dzięki czemu o wiele łatwiej jest serwować strumienie danych do
wielu odbiorców. Ja mógłbym na przykład ze swojego laptopa na DSLu nadawać dla
dziesięciu tysięcy użytkowników naraz. Czy zamierzam to zrobić? Nie
potwierdzę, ani nie zaprzeczę... Zresztą, nieistotne czy to zrobię czy nie.
Ważne, że _mogę_ (to jest właśnie przykład potencjalnej przewagi
technologicznej).

Z Polski [radio nadają
Poznaniacy](http://icecast.ipv6.man.poznan.pl.ipv4.sixxs.org/). Jedna ze
stacji, Radio BLUE FM, ma ciekawe przesłanie. Oczywiście po IPv6.

    maciej@clover ~ $ mplayer http://radio.**ipv6**.man.poznan.pl:8000/bluefm.ogg  

MPlayer dev-SVN-rUNKNOWN-4.1.2 (C) 2000-2008 MPlayer Team  
CPU: Genuine Intel(R) CPU T2050 @ 1.60GHz (Family: 6, Model: 14, Stepping: 8)  
CPUflags: MMX: 1 MMX2: 1 3DNow: 0 3DNow2: 0 SSE: 1 SSE2: 1  
Compiled for x86 CPU with extensions: MMX MMX2 SSE SSE2  
Playing http://radio.**ipv6**.man.poznan.pl:8000/bluefm.ogg.  
Resolving radio.**ipv6**.man.poznan.pl for **AF_INET6**...  
Connecting to server radio.ipv6.man.poznan.pl**[2001:808:0:6::198]**: 8000...  
Cache size set to 1280 KBytes  
Cache fill: 18.75% (245760 bytes)  
[Ogg] stream 0: audio (Vorbis), -aid 0  
Ogg file format detected.  
Clip info:  
Name: Radio 103,4 Blue FM : Pop non-stop prosto z Poznania  
**(Specjalne pozdrowienia dla sluchaczy zza malej wody :-))**

Bardzo sympatyczne. Dziękuję!

Ale radio nadają nie tylko Poznaniacy. Jest na przykład [Virgin
Radio](http://www.ipv6.ecs.soton.ac.uk.ipv4.sixxs.org/virginradio/), jedna ze
stacji nazywa się Groovy i nadaje to co lubię.

    mplayer http://virgin.6pack.org/dvb/vruk-gr-mp2

Oprócz multicastu jest jeszcze jedna rzecz, która mnie bardzo interesuje, a
mianowicie przesyłanie danych bezpośrednio z jednego komputera do drugiego (w
odróżnieniu od serwerów). Dlaczego? Na przykład, żebyśmy mogli porozmawiać
przez telefon internetowy. Tak, Skype to potrafi już teraz, ale to nie jest za
darmo. Nie w sensie pieniędzy, ale w sensie problemów z bezpieczeństwem i
odpowiedzialnością za ten ogromny botnet, który musieli stworzyć żeby to
wszystko _w ogóle_ działało.

Miałem nadzieję, że Ekiga będzie umiała IPv6, ale niestety. Co ciekawe,
GnomeMeeting jeszcze miał IPv6, a Ekiga już nie ma. Może w końcu [nauczyłbym
się w końcu programować i dorobił obsługę
IPv6](http://gsyc.es/~eva/IPv6-web/ipv6.html) do Ekigi...?

Na koniec ciekawostka. Na jednej stronie zatytułowanej „Dlaczego chcesz mieć
IPv6”, [możemy
przeczytać](http://en.linuxreviews.org/Why_you_want_IPv6#Totally_Unimportant):

> **Zupełnie nieważne**  
  
Krążą plotki że na publicznych serwerach FTP dostępnych tylko przez IPv6
znajduje się spora ilość materiałów, które są niedostępne lub trudno dostępne
w starym Internecie. Używanie tych serwerów, o ile one istnieją, może być lub
nie być nielegalne. Adresy tych serwerów nigdy nie powinny być publicznie
ujawniane, ale jedynie zdradzane zaufanym przyjaciołom. Serwisy te zazwyczaj
mają katalog w stylu /incoming albo /upload, gdzie każdy może zapisywać i
odczytywać jak mu się podoba.

Czy znalazłem te serwery? Nie potwierdzę, ani nie zaprzeczę...

_UPDATE: Atomów w (obserwowalnym) Wszechświecie jest jednak więcej, bo 1.7 ×
1077, a adresów IPv6 jest 2128 =~ 1038._

# Komentarze

* kkk (2008-03-21 21:09:24): <p>Ciekawy wpis.</p>
* Marek (2008-03-22 16:33:42): <p>Och, jak ja lubię czytać Twoje, Maćku, teksty.
  :-)</p>  <p>Przepastne serwery <span class="caps">FTP</span> w zaświatach
  IPv6&#8230; Można tam przeniknąć, naczerpać się i bezpiecznie powrócić...
  Fascynujące.</p>
