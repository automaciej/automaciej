+++
date = "2008-05-14T09:36:23"
draft = false
title = "Nowa zabawka: Netra T1"
aliases = [ "/2008/05/nowa-zabawka-netra-t1/",]

+++
Postanowiłem spróbować bliżej zapoznać się ze sprzętem Suna. Nigdy nie byłem
fanem Suna i Solarisa, i raczej już nie zostanę, ale mogę zrobić przynajmniej
tyle, żeby bliżej pomacać jakieś SPARC-owe pudło, zanim wyrzucę je przez okno.

Jedna wyprawa na eBay i za jedyne €100 (+€20 przesyłka) Netra T1 jest moja.

Do najcichszych komputerów to ona raczej nie należy. Na razie zostaje w
biurze.

Niestety jak na razie nie udało mi się jej uruchomić. To znaczy, włączyć
zasilanie to tak, ale skomunikować się — już nie za bardzo, ze względu na
dziwny port serial z gniazdem RJ45. Gdyby Sun zrobił swój port serial
kompatybilny z Cisco, po prostu pożyczyłbym przewtyczkę od sieciowców. Ale
nie, Sun musi mieć _wszystko inaczej_.

Adapter najwyraźniej muszę sobie sam zlutować [według diagramu][diagram].
Dobrze że chociaż diagram opublikowali.

[diagram]:
http://docs.sun.com/source/820-3012-10/A_signal-pin.html#50397208_marker-1001697

Fani Solarisa mówią o nim, że to jest _prawdziwy_ Unix. A SPARC to _prawdziwy_
komputerowy hardware. Jeżeli chodzi im o to, że zanim cokolwiek się da na tym
sprzęcie i sofcie zrobić, człowiek żałuje że się urodził, to zdecydowanie się
zgadzam.

----
**Komentarze**

* deviant (2008-05-14 10:34:03): <p>Mozesz spokojnie uzyc kabelka od routerow
  Cisco. Mam takowy (moge podac numer kabla jak bedziesz potrzebowal), sprawuje
  sie dobrze. Bedziesz mial kabel, to albo minicom albo windowsowy hypertrm.
  Potem logon na <span class="caps">ALOM</span>, poweron i lecisz ;) Polecam
  zapoznac sie z opcjami typu boot, np. boot cdrom. Milej zabawy ;)</p>
* Bonjoure (2008-05-14 10:36:57): <p>Wygląda bardzo fajnie! Szkoda faktycznie,
  że zanim się człowiek nacieszy, to musi koszmar przebyć np. z lutownicą i
  poszukiwaniem rozwiązań. Niemniej jednak faktycznie <span
  class="caps">SPARC</span> brzmi fantastycznie, zwłaszcza że pieniądze
  niewielkie (stosunkowo). Do czego zamierzasz zastosować to cudo?</p>
* GiM (2008-05-14 11:58:47): <p>też się ostatnio rozglądałem na ebayu za
  sparcami. ceny niskie.<br /> z różnych powodów póki co musi jeszcze
  poczekać</p>
* lordmac (2008-05-14 14:41:36): <p>Tak jak napisal deviant &#8211; standardowy
  kabel serialowy dziala na Sun&#8217;ach.<br /> Parametry transmisji przez
  serial tez sa standardowe : 9600 8N1, <br /> Hardware flow control: <span
  class="caps">YES</span>, software flow control: NO <br /> Emulacje terminala
  najlepiej ustawic na <span class="caps">DEC</span> VT100</p>
* lordmac (2008-05-14 14:45:28): <p>To pochwal sie jeszcze co tam masz w srodku
  w tym suniku :)</p>
* Automaciej (2008-05-14 23:10:01): <p>deviant, lordmac: Przewtyczka Cisco
  niestety nie działa z tym modelem. Netra ma inaczej zmapowane piny. Nawet
  sprawdziłem multimetrem jak są zmapowane piny w przewtyczce Cisco żeby mieć
  pewność że są zmapowane inaczej niż to co podaje Sun.</p>    <p>W suniku tylko
  tyle, żeby ruszył Solaris 10. Procesor 400MHz, 512MB <span
  class="caps">RAM</span> i 18GB <span class="caps">HDD</span>. (Solaris 10 na
  dzieńdobry używa 160MB <span class="caps">RAM</span> na jeden proces javy. Mój
  kolega się śmiał że to pewnie pół kernela napisane w javie. Bardzo się nie
  pomylił, bo to jest proces który zajmuje się startowaniem i zatrzymywaniem
  usług systemowych, odpowiednik skryptów w <code>/etc/init.d/</code>.)</p>
  <p>Zastosowanie na razie edukacyjne. Poinstaluję tam system, pobawię się, a
  jak mnie wnerwi to wyrzucę przez okno albo podpalę, sfilmuję i wrzucę na
  YouTube. ;-)</p>    <p>A jeżeli mnie nie wnerwi, to postawię po IPv6 publiczny
  serwer FTP z możliwością anonimowego zapisu.</p>
* deviant (2008-05-15 09:08:44): <p>Maciej &#8211; albo cos z nia jest nie tak
  albo z tym kabelkiem cisco ktory probowales. Mowisz, ze <span
  class="caps">SMF</span> duzo zasobow zre? ;)</p>
* lordmac (2008-05-15 10:11:24): <p><span class="caps">SMF</span> to nic ;)
  &#8211; on sie tylko laduje do pamieci i tyle &#8230;. zeby ci przypadkiem
  przez mysl nie przeszlo uzywanie graficznej konsoli administracyjnej <span
  class="caps">SMC</span> zrobionej w Javie &#8230;. a fuj<br /> Niestety masz
  troche malo ramu , ale polecam pobawienie sie virtualnymi contenerami.<br />
  No i zawsze mozesz sobie zainstalowac OpenSolaris&#8217;a</p>  <p>No i
  niezapomnij o pkg-get&#8217;cie ktory bardzo ulatwia instalacje paczek
  (http://www.sunfreeware.com/pkg-get.html)</p>
* automaciej (2008-05-19 20:13:37): <p>JumpStart<br /><br />Nie, to nie jest
  odkurzacz. Odkurzacz ma rurę. Tak, dźwięk wydaje podobny.<br />Moja Netra T1
  jest maszyną nieco autystyczną. Porozumiewa się ze światem przez port
  szeregowy, USB, SCSI i dwie sieciówki. Nie ma karty graficznej, ani
  klawiatury. O [...]</p>
* WwW (2008-11-09 20:04:45): <p>A juz trzymałem spust myszki na opcji <span
  class="caps">KUP</span> <span class="caps">TERAZ</span> na allegro, ale teraz
  sie powstrzymam chyba :)</p>
* ksx4system (2010-06-16 02:14:15): <p>LOL, wczoraj kupiłem Netrę X1 i
  prawdopodobnie dziś rozpocznę walke ;-) tak, kabelek mam oczywiście Cisco,
  potwornie drogi jak na 1,8m skrętki z nietypową wtyczką na 2 końcu :-/</p>
* subwoofer (2011-06-08 08:44:24): <p>Zarzadzanie usługami jest napisane w javie
  żeby sie skalowało :) <br /> Czyli mona latwo exportowac dane o uslugach z
  jednej bazy do innej....na linuxie nie da sie chyba tak z miejsca, jezeli
  przyjdzie duzy server to rozwiazanie java + baza danych sie lepiej sprawdzi.
  <br /> Netre tez mam przez kabel cisco podlaczone i jest oki, a wiec pozycz od
  sieciowcow :)<br /> Polecam nauczyc sie Openboota...</p>  <p>Pozdrawiam :)</p>
