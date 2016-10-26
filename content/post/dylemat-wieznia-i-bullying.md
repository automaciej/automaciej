+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2007-05-12T16:06:43"
title = "Dylemat więźnia i bullying"
tags = [ "dywagacje" ]
+++
[Dylemat więźnia](http://pl.wikipedia.org/wiki/Dylemat_wi%C4%99%C5%BAnia) jest
jednym z klasycznych problemów teorii gier. Jest interesującą abstrakcją całej
klasy sytuacji, gdzie dwie strony mogą wybierać pomiędzy kooperatywnym i
niekooperatywnym zachowaniem. Jest to też gra, w której można osiągnąć wynik
zysk-zysk oraz strata-strata. Dylemat więźnia nie ma zastosowania do sytuacji
typu targowanie się, gdzie zysk jednej strony oznacza stratę drugiej; opisuje
on raczej sytuację w której gracze tworzą zespół i pracują razem.

Jednym z głównym elementów dylematu więźnia są cztery poziomy wypłat,
ustawione w taki sposób, że największy zysk osiąga się „wrabiając” drugą
stronę.

![Dylemat więźnia, wypłaty](http://media.blizinski.pl/images/blog/pd-01-decisions-payoffs.png)

W grze są cztery możliwości.

![Dylemat więźnia, strategie i wypłaty](http://media.blizinski.pl/images/blog/pd-02-combinations.png)

Jeżeli obydwaj gracze kooperują, wygrywają: zysk―zysk. Jeżeli jeden zdradzi,
zyskuje jeszcze więcej: duży zysk―duża strata. Jeżeli obydwaj zdradzą (zagrają
niekooperatywnie), obydwaj tracą: strata-strata.

Wpadłem niedawno na pomysł rozszerzenia dylematu więźnia w taki sposób, żeby
zamodelować bullying, a potem szukać najefektywniejszych strategii. Główne
elementy rozszerzenia modelu byłyby nastepujące:

  * Jest wielu graczy.
  * Każdy gracz gra wielokrotnie z wieloma innymi graczami; w każdej grze biorą
    udział dwaj gracze.
  * Gracze mogą obserwować gry w których nie biorą udziału
  * Obserwacja może być myląca, na przykład zdrada może być widziana jako
    kooperacja.
  * Jeżeli gracz zdradzi i informacja o tym wydostanie się na zewnątrz, gracz
    może zostać „ukarany” przez pozostałych graczy, tak jak na przykład
    w strategii _wet za wet_.

Bullying byłby wtedy, kiedy jeden z graczy zdradza (atakuje?), wygrywa dużo
(duży zysk―duża strata) i ukrywa to przez środowiskiem. W następnej turze
zdradzony gracz, jeżeli stosuje strategię _wet za wet_, powinien się bronić
czyli grać niekooperatywnie. Niestety, jeżeli tak zrobi, zostanie przez
środowisko uznany za atakującego (czyli tego który zdradził pierwszy) i
ukarany. To powoduje że gracz, pomimo że został zdradzony, nie może się bronić
― w następnej turze musi grać kooperatywnie, co powoduje że jest się podatny
na kolejny atak i znowu poniesie dużą stratę. Jeżeli prawda o tym że bully
zdradza, nigdy nie wyjdzie na światło dzienne, może on pozostać bezkarny na
nieskończoną liczbę tur.

Nie jestem pewien jak powinny wyglądać szczegóły tego modelu, na przykład jak
zamodelować przekłamanie? Czy powinno ono być losowe czy deterministyczne? Czy
gracze powinni całkowicie kontrolować to co przedostaje się do środowiska, czy
tylko częściowo?

Dobry model powinien być tak prosty jak to możliwe, przy jednoczesnym, dobrym
odzwierciedleniu istoty problemu i głównych cech, takie jak obecność
środowiska i przekłamania.

# Komentarze

* mamaT (2007-05-14 14:37:28): <p>ja bym to nazwała dylematem małżonka :-)</p>
* Luscynd (2007-05-15 19:48:19): <p>Chyba stosunkowo łatwo można by zamodelować
  świat widziany oczami bully&#8217;ego, bo jest on wyjątkowo czarno biały i
  hierarchiczny. Ludzie dzielą się na wyraźne kategorie:</p>  <p>1. Ludzie
  których bully potrzebuje &#8211; poplecznicy. Dzielą się na 2 podkategorie:
  <ul> <li>popierają bully&#8217;ego bo mają wspólny interes, a środki są dla
  nich nieistotne</li> <li>naiwni, (za) dobrzy ludzie, którzy wierzą że bully
  poprawi się gdy będzie dobrze traktowany. Można ich poznać po tym że lubią
  używać eufemizmów ;-)</li> </ul></p>  <p>2. Ludzie których bully szanuje
  (stosunkowo niewielka grupa): <ul> <li>są to ludzie którzy mu imponują i
  jednocześnie nie wchodzą w drogę (najczęściej są wyżej w hierarchii)</li>
  </ul></p>  <p>3. Ludzie których bully nie szanuje (najliczniejsza grupa) Można
  podzielić ich zgrubsza na 3 podkategorie: <ul> <li>ofiary które się
  podporządkowują (ukryta wrogość ze strony bully&#8217;ego)</li> <li>inni bully
  o sprzecznych interesach (otwarta wrogość)</li> <li>potencjalne lub byłe
  ofiary które nie chcą się podporządkować (otwarta wrogość; są najbardziej
  niebezpieczni ponieważ mogliby zdemaskować bully&#8217;ego, a więc należy ich
  natychmiast wyeliminować)</li> </ul></p>
