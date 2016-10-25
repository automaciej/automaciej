+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2005-08-15T08:56:25"
title = "Wszyscy za firewallami"
tags = [ "informatyka", "opowieści" ]

+++
Wszyscy za firewallami - to jest coś co dzisiaj nazywa się "dostępem do
Internetu". Jestem pewien że niektórzy ludzie (a raczej korporacje) cieszą się
z tego, że nie ma połączeń peer-to-peer, nie ma wymiany plików, nie ma
bezpośrednich połączeń między komputerami. Używanie Internetu to czytanie
stron internetowych i sprawdzanie poczty, koniec kropka.

Uderzyło mnie to, kiedy przeprowadziłem się do nowego miejsca w czasie studiów
za granicą. Podłączyłem laptopa do gniazdka ethernetowego w ścianie,
sprawdziłem pocztę i poczytałem Slashdot.

Niespodzianka nastąpiła, kiedy chciałem zalogować się na serwer.
"ssh\_exchange\_identification: Connection closed by remote host", powiedział mi
kient SSH. Co? Mój serwer zamknął połączenie kiedy chciałem się zalogować? Po
krótkim dochodzeniu okazało się że jestem dosłownie odcięty od sieci, i działa
tylko przeglądanie WWW i sprawdzanie poczty. Nie ma oglądania strumieniowanych
multimediów, nie ma CVS, nie ma telefonii internetowej, nie ma bittorrenta
(ani żadnego innego p2p), nie ma gier online, nie ma komunikatorów, no i
wreszcie - nie ma SSH!

To miał być pokój z dostępem do Internetu! Być za firewallem, niedostępny z
zewnątrz i nie móc używać niczego poza www i pocztą - to nie jest coś co
nazwałbym _dostępem_ do Internetu.

Kro mi to zrobił i dlaczego? Kolejne dochodzenie wykazało że jestem za
serwerem Microsoft Internet Security and Acceleration (ISA). Więc duńscy
administratorzy postanowili zredukować używalność internetu, żeby co? podnieść
bezpieczeństwo?

Niespodzianka: Skype, obecnie "hip and cool" program do telefonii
internetowej, połączył się jakby nigdy nic. Okazało się, że Skype oszukuje
serwer ISA, udając że przegląda bezpieczne strony internetowe, w
rzeczywistości przesyłając wiadomości i głos. Najwyraźniej został
zaprojektowany do walki z tak nieprzyjaznymi warunkami jak u mnie.

Nie zajęło mi zbyt długo żeby użyć tej samej techniki i połączyć się przez SSH
do jednego z moich serwerów, z którego mogłem połączyć się do następnych.
Później nauczyłem się, jak tworzyć tunele do wybranych usług na wybranych
serwerach. Kolejnym krokiem było stworzenie lokalnego SOCKS proxy, które mogło
być używane przez różne aplikacje - to rozwiązało większość problemów.

Pewnego dnia postanowiłem kupić webcam, żeby dodać obraz do swoich rozmów ze
znajomymi i szefem. Webcam uruchomiłem bez większych problemów i zacząłem
szukać programu do rozmów. Skype okazało się, że jest tylko dla Windows.
Gnomemeeting posługuje się protokołem h.323 i nie może połączyć się przez
SOCKS, więc musiałem wymyślić inne rozwiązanie. Zamontowany na laptopie webcam
patrzył na mnie smutno...

Przełom nastąpił, kiedy przeczytałem [Firewall Piercing
HOWTO](http://www.tldp.org/HOWTO/Firewall-Piercing/). Od tego momentu mogłem
przypisać nowy i piękny adres publiczny do swojego laptopa, dzięki czemu na
powrót stałem się pełnoprawnym uczestnikiem globalnej Sieci. Wideokonferencje
działają świetnie i mój webcam jest nareszcie w użyciu!

Ta historia pokazuje, że ograniczanie dostępu do internetu przez odcinanie
usług nie przynosi większych efektów i można z nim sobie poradzić.
Bezpieczeństwa również szczególnie nie podnosi, bo użytkownicy wciąż są
atakowani przez programy z załączników email i złośliwych stron internetowych.

To smutne, że w dzisiejszych czasach Internet oznacza jedynie strony WWW i
email...

# Komentarze

* cenebris (2005-08-15 09:35:02): <p>Mam trochę podobny problem w akademiku -
  admin nie chce mi przekierować portu na moje ip. Sądzisz, że tą techniką
  udałoby się to ominąć?</p>
* riddle (2005-08-15 13:41:49): <p>Sprytnie to zrobiłeś. Ja też nie widzę w
  takim procederze przyszłości. Jeszcze brakuje tylko syt. znanej z Chin -
  Internet w Internecie. :&gt;</p>
* automaciej (2005-08-17 07:19:43): <p>cenebris: Udałoby się ominąć.
  Potrzebujesz &quot;przyjaciela&quot; na zewnątrz, czyli serwer na którym masz
  roota i który ma wystawione SSH na porcie 443.</p>
* automaciej (2007-08-16 09:53:57): <p>Przedmowa do Firewall Piercing mini-
  HOWTO<br /><br />W 2005 opisywałem jak znajdując się za restrykcyjnym
  firewallem ISA byłem odcięty od sieci i w jaki sposób udało mi się odzyskać
  wolność (czytaj: publiczny adres IP) przy pomocy techniki zaczerpniętej z
  Firewall Piercing mini-HOWTO. Osta[...]</p>
