+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2008-03-08T17:04:49"
draft = false
title = "Jak rozpoznać krzaczenie się polskich znaków"
+++
_UPDATE: [Napraw swój pokrzaczony tekst.](http://krzaki.blizinski.pl/)_

Jak wyglądają pokrzaczone polskie znaki, to chyba widział każdy, kto używał
komputera dłużej niż od wczoraj. Ale krzaczenie się było zazwyczaj tylko
informacją, że coś jest nie tak. Tylko nieliczni potrafili, zobaczywszy na
przykład „Pchn±æ w tê ³ód¼ je¿a i o¶m skrzyñ fig.”, powiedzieć „A, to jest
iso-8859-2 interpretowane jako iso-8859-1.”

Dzisiaj usiadłem i napisałem
[skrypt](http://code.blizinski.pl/shell/encoding.sh.html), który przegląda
najpopularniejsze kodowania i pokazuje, jak wygląda każda kombinacja
interpretacji polskich znaków.

W ostatniej kolumnie widać, czy podczas przetwarzania nie wystąpiły jakieś
błędy, na przykład napis w kodowaniu iso-8859-2 nie jest poprawnym napisem w
utf-8.

Prawdziwe | Wzięte za | Wygląda tak... | ok?  
---|---|---|---  
utf-8 | utf-8 | Pchnąć w tę łódź jeża i ośm skrzyń fig. | ok  
utf-8 | iso-8859-2 | PchnÄ?Ä? w tÄ? Ĺ?ĂłdĹş jeĹźa i oĹ?m skrzyĹ? fig. | ok  
utf-8 | iso-8859-1 | PchnÄ?Ä? w tÄ? Å?Ã³dÅº jeÅ¼a i oÅ?m skrzyÅ? fig. | ok  
utf-8 | cp1250 | PchnÄ…Ä‡ w tÄ™ Ĺ‚ĂłdĹş jeĹĽa i oĹ›m skrzyĹ„ fig. | ok  
iso-8859-2 | utf-8 | Pchn w t d jea i om skrzy fig. | ERR  
iso-8859-2 | iso-8859-2 | Pchnąć w tę łódź jeża i ośm skrzyń fig. | ok  
iso-8859-2 | iso-8859-1 | Pchn±æ w tê ³ód¼ je¿a i o¶m skrzyñ fig. | ok  
iso-8859-2 | cp1250 | Pchn±ć w tę łódĽ jeża i o¶m skrzyń fig. | ok  
cp1250 | utf-8 | Pchn w t d jea i om skrzy fig. | ERR  
cp1250 | iso-8859-2 | Pchnšć w tę łód? jeża i o?m skrzyń fig. | ok  
cp1250 | iso-8859-1 | Pchn¹æ w tê ³ód? je¿a i o?m skrzyñ fig. | ok  
cp1250 | cp1250 | Pchnąć w tę łódź jeża i ośm skrzyń fig. | ok  
  
Miejmy nadzieję że dzięki unicode takie problemy będą stopniowo odchodziły w
niepamięć, ale założę się że mamy przed sobą jeszcze niejedną migrację MySQL
albo inną niewyraźną operację która może zamienić nasze narodowe znaki w
bezkształtną papkę.

Ten skrypt pokazuje tylko jeden etap krzaczenia. Prawdziwa przygoda zaczyna
się, kiedy mamy polskie znaki pokrzaczone nie jedno-, ale dwukrotnie!

# Komentarze

* Crash (2008-03-08 17:07:55): <p>iso-8859-1iso-8859-1Pchn w t ód jea i om skrzy
  fig.ERR</p>  <p>Innymi słowy: albo moja przeglądarka nie interpretuje
  iso-8859-1, albo tekst w *-1 interpretowany jako tekst w *-1 nie wyświetla
  polskich znaków.</p>
* Automaciej (2008-03-08 17:09:11): <p>Crash: W zasadzie, to tych wierszy nie
  powinno być w tabelce, bo ten napis nie może być przedstawiony w iso-8859-1.
  Usunę je.</p>
* kuku (2008-03-08 17:48:30): <p>czasem też można zobaczyć 4 literki w
  kwadraciku<br /> a ja ostatnio walczyłem ze zmianą nazw w cyrylicy na unicode
  &#8211; wyglądało to mniej wiecej tak:(wejsciowego kodowania nie znałem)</p>
  <p>for i in `convmv &#8212;list`; do convmv &#8212;qfrom -f $i -t UTF8 14\ -\
  Ò‰êö’å\ Ž’ƒŒö©ê\ ã\ èƒåŒØêåŒØ.mp3 ;done   </p>  <p>a potem tylko trzeba było
  wybrać odpowiednie (najłądniejsze &#8211; znaczy się ;)</p>
* Mike (2008-03-08 19:08:20): <p>Z tym MySQL&#8217;em to faktycznie jaja sa.
  Mialem jedna konwersje ze starego na nowego SQL&#8217;a i musialem szybko
  wydumac jak zrobic gladkie przejscie. Udalo sie, ale chwilami bylo ciezko.</p>
* BTM (2008-03-08 19:46:49): <p>Ej no, co to za Microsoftowy tekst? Co się stało
  z &#8222;Zażółć gęślą jaźń&#8221; ? :P</p>
* Automaciej (2008-03-08 20:04:06): <p>BTM: Zażółć gęślą jaźń ma za mało liter
  bez akcentów, jak się pokrzaczy, to już tak strasznie, że w ogóle nie widać,
  jakie to były słowa. Nie upieram się, jestem otwarty na propozycje. :-)</p>
* Joanna (Typoagrafka) (2008-03-08 21:12:43): <p>— Tylko nieliczni potrafili
  <strong>powiedzieć</strong> zobaczywszy na przykład „Pchn±æ w tê ³ód¼ je¿a i
  o¶m skrzyñ fig.”, <strong>powiedzieć</strong> „A, to jest iso-8859-2
  interpretowane jako iso-8859-1.”</p>  <p>— Bardzo ciekawy artykuł i
  spostrzeżenie, Maćku! Dzięki! A skrypt na pewno wypróbuję w wolnej chwili!</p>
* Joanna (Typoagrafka) (2008-03-08 21:16:17): <p>PS: „Pchnąć w tę łódź jeża lub
  ośm skrzyń fig” nie ma nic wspólnego z Microsoftem. To zdanie, które zawiera
  <strong>każdą</strong> literę polskiego alfabetu dokładnie raz i dlatego jest
  szczególnej wartości do tego celu idealne. Istnieje jeszcze kilka takich zdań.
  Patrz <a href="http://pl.wikipedia.org/wiki/Pangram" rel="nofollow"
  >Pangram@Wikipedia</a></p>
* btm (2008-03-08 21:33:08): <p>Joanno, wiem, co to Pangram. A z Microsoftem ma
  więcej wspólnego niż Ci się wydaje &#8211; wystarczy pogooglać (+ dodać słowo
  &#8222;office&#8221;, bodaj w Word&#8217;dzie jest) Tymniemniej, o wiele
  częściej stosuje się gęślą jaźń bo jest szybsze do wpisania i takoż zawiera
  wszystki polskie znaki diakrytyczne :)</p>
* Joanna (Typoagrafka) (2008-03-08 23:41:50): <p>To, że Microsoft wbudował w
  Worda trick który wypisuje ten pangram ileśtam razy z automatu nie robi z
  niego jeszcze &#8222;microsoftowego tekstu&#8221;, bez przesady. Mogę sobie
  napisać program, który mi to zrobi w dowolnym edytorze, to jeszcze nie znaczy,
  że to będzie &#8222;asiowy tekst&#8221;. Tylko o to mi chodzi. Ale nie
  zaśmiecajmy Gospodarzowi komentarzy. Microsoftem. :P</p>
* R@V (2008-03-09 21:57:53): <p>Niestety, tak to bywa, że tzw WebMajsterzy nie
  wiedzą o co chodzi z kodowaniem bazy danych i klienta bazy danych&#8230;</p>
  <p>Wielokrotnie widziałem jak np utf-8 było wrzucane do pól zdefiniowanych
  jako iso8859-1. co powodowało spore problemy z ewentualnym importem.</p>
  <p>Oczywiście jak ktoś chce to się uda, zrobić wszystko i tak.<br /> W
  przypadku &#8211; mysql+php &#8211; mysqli\_client\_encoding(); &#8211;
  postgres+php &#8211; pg\_client\_encoding();</p>  <p>gdy zakładamy bazę &#8211;
  mysql &#8211; set names [kodowanie] i dodatkowo zakładając tabele musi być
  ustawioene odpowiednie collation. \_ci(case insensitive) \_bi(case sensitive)
  &#8211; postgres &#8211; -E [kodowanie]</p>  <p>a na stronie to chyba nawet
  dzieci wiedzą, że w meta to się ustawia a dodatkowo wysyła się w
  nagłówkach.</p>  <p>korzystając z tak niewielkiej ilości informacji można już
  sporo zdziałać i spowodować, że kodowanie nie będzie bolączką...</p>
  <p>Pozdrawiam</p>
* automaciej (2008-03-13 19:32:31): <p>Napraw swój pokrzaczony tekst<br /><br
  />Niedawno poszła plotka, że napisałem skrypt który rozpoznaje pokrzaczone
  polskie literki. Postanowiłem nadgonić plotkę i naprawdę go napisałem.<br
  />Tym razem jest to dostępny on-line skrypt, do którego można wkleić
  pokrzaczony polski tekst,[...]</p>
* ,./,/.ij8890980i (2011-03-29 11:48:28): <p>jebane huje</p>
* Kurt (2011-12-11 15:41:32): <p>Ciekawe c o to za kretyn wpisał się powyżej.
  Najwyraźniej miał pokrzaczone kodowanie we łbie.</p>
* Pozycjonowanie stron (2013-03-12 15:11:35): <p>Można wykryć kodowanie za
  pomocą mb<em>detect</em>encoding</p>
