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

* deviant (2008-05-14 10:34:03): Mozesz spokojnie uzyc kabelka od routerow
  Cisco. Mam takowy (moge podac numer kabla jak bedziesz potrzebowal), sprawuje
  sie dobrze. Bedziesz mial kabel, to albo minicom albo windowsowy hypertrm.
  Potem logon na ALOM, poweron i lecisz ;) Polecam
  zapoznac sie z opcjami typu boot, np. boot cdrom. Milej zabawy ;)
* Bonjoure (2008-05-14 10:36:57): Wygląda bardzo fajnie! Szkoda faktycznie,
  że zanim się człowiek nacieszy, to musi koszmar przebyć np. z lutownicą i
  poszukiwaniem rozwiązań. Niemniej jednak faktycznie SPARC brzmi fantastycznie, zwłaszcza że pieniądze
  niewielkie (stosunkowo). Do czego zamierzasz zastosować to cudo?
* GiM (2008-05-14 11:58:47): też się ostatnio rozglądałem na ebayu za
  sparcami. ceny niskie.  
 z różnych powodów póki co musi jeszcze
  poczekać
* lordmac (2008-05-14 14:41:36): Tak jak napisal deviant &#8211; standardowy
  kabel serialowy dziala na Sun&#8217;ach.  
 Parametry transmisji przez
  serial tez sa standardowe : 9600 8N1,   
 Hardware flow control: YES, software flow control: NO   
 Emulacje terminala
  najlepiej ustawic na DEC VT100
* lordmac (2008-05-14 14:45:28): To pochwal sie jeszcze co tam masz w srodku
  w tym suniku :)
* Automaciej (2008-05-14 23:10:01): deviant, lordmac: Przewtyczka Cisco
  niestety nie działa z tym modelem. Netra ma inaczej zmapowane piny. Nawet
  sprawdziłem multimetrem jak są zmapowane piny w przewtyczce Cisco żeby mieć
  pewność że są zmapowane inaczej niż to co podaje Sun.    W suniku tylko
  tyle, żeby ruszył Solaris 10. Procesor 400MHz, 512MB RAM i 18GB HDD. (Solaris 10 na
  dzieńdobry używa 160MB RAM na jeden proces javy. Mój
  kolega się śmiał że to pewnie pół kernela napisane w javie. Bardzo się nie
  pomylił, bo to jest proces który zajmuje się startowaniem i zatrzymywaniem
  usług systemowych, odpowiednik skryptów w `/etc/init.d/`.)
  Zastosowanie na razie edukacyjne. Poinstaluję tam system, pobawię się, a
  jak mnie wnerwi to wyrzucę przez okno albo podpalę, sfilmuję i wrzucę na
  YouTube. ;-)    A jeżeli mnie nie wnerwi, to postawię po IPv6 publiczny
  serwer FTP z możliwością anonimowego zapisu.
* deviant (2008-05-15 09:08:44): Maciej &#8211; albo cos z nia jest nie tak
  albo z tym kabelkiem cisco ktory probowales. Mowisz, ze SMF duzo zasobow zre? ;)
* lordmac (2008-05-15 10:11:24): SMF to nic ;)
  &#8211; on sie tylko laduje do pamieci i tyle &#8230;. zeby ci przypadkiem
  przez mysl nie przeszlo uzywanie graficznej konsoli administracyjnej SMC zrobionej w Javie &#8230;. a fuj  
 Niestety masz
  troche malo ramu , ale polecam pobawienie sie virtualnymi contenerami.  

  No i zawsze mozesz sobie zainstalowac OpenSolaris&#8217;a  No i
  niezapomnij o pkg-get&#8217;cie ktory bardzo ulatwia instalacje paczek
  (http://www.sunfreeware.com/pkg-get.html)
* automaciej (2008-05-19 20:13:37): JumpStart  
  
Nie, to nie jest
  odkurzacz. Odkurzacz ma rurę. Tak, dźwięk wydaje podobny.  
Moja Netra T1
  jest maszyną nieco autystyczną. Porozumiewa się ze światem przez port
  szeregowy, USB, SCSI i dwie sieciówki. Nie ma karty graficznej, ani
  klawiatury. O [...]
* WwW (2008-11-09 20:04:45): A juz trzymałem spust myszki na opcji KUP TERAZ na allegro, ale teraz
  sie powstrzymam chyba :)
* ksx4system (2010-06-16 02:14:15): LOL, wczoraj kupiłem Netrę X1 i
  prawdopodobnie dziś rozpocznę walke ;-) tak, kabelek mam oczywiście Cisco,
  potwornie drogi jak na 1,8m skrętki z nietypową wtyczką na 2 końcu :-/
* subwoofer (2011-06-08 08:44:24): Zarzadzanie usługami jest napisane w javie
  żeby sie skalowało :)   
 Czyli mona latwo exportowac dane o uslugach z
  jednej bazy do innej....na linuxie nie da sie chyba tak z miejsca, jezeli
  przyjdzie duzy server to rozwiazanie java + baza danych sie lepiej sprawdzi.
    
 Netre tez mam przez kabel cisco podlaczone i jest oki, a wiec pozycz od
  sieciowcow :)  
 Polecam nauczyc sie Openboota...  Pozdrawiam :)
