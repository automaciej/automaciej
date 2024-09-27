---
aliases:
- /2015/10/co-trzeba-potrafic-zeby-byc-klientem-rwe/
date: 2015-10-01 17:03:45
draft: false
tags:
- życie
title: Co trzeba potrafić, żeby być klientem RWE

---

W lutym RWE przysłało informację że się zmienił sposób logowania. Przysłali nowe
hasło i napisali żeby użyć takiego samego Numeru Klienta jak poprzednio.  (Numer
klienta? Ale ja nie wiem jaki mam numer klienta! Czy to jest to samo co „numer
handlowy partnera”? Bo ten akurat znam. Skoro już wymyślają dziwne nazwy
numerów, mogliby chociaż używać ich konsekwentnie) W haśle tymczasowym jest
podejrzany string “&amp;amp;”. <!--more--> Czyżby spaprali escaping podczas
formatowania emaila? Spróbowałem zalogować się powyższym numerem i hasłem
skopiowanym z emaila. Złe hasło. Spróbowałem z hasłem gdzie zamiast „&amp;amp;”
podstawiłem „&amp;”. Tak też się nie udało. Kliknąłem więc na opcję odzyskiwania
hasła. Napisali że wygenerowali nowe hasło, ale email z hasłem nigdy do mnie nie
dotarł. Na stronie piszą żeby w razie kłopotów do nich dzwonić. Dzwonić?! Jak ja
nie znoszę dzwonić! Nie ma żadnego adresu email pod który można by zgłosić
problem, ani formularza zgłoszeniowego.

W końcu zadzwoniłem. Poprosiłem o zresetowanie hasła, i przysłali mi mailem
hasło tymczasowe. Spróbowałem go użyć. Po zatwierdzeniu formularza logowania
wylądowałem na stronie z kolejnym formularzem, tym razem do zmiany hasła
tymczasowego na hasło właściwe. Wypełniłem go, kliknąłem „zapisz”, i… nic.
Strona ani drgnęła.

pomyślałem że problem może tkwić w zepsutym walidatorze formularza po stronie
przeglądarki. Strona mówiła mi że muszę wypełnić pole „użytkownik”, pomimo że
było już wypełnione. Usunięcie treści z niego i wypełnienie od nowa w niczym
nie pomogło. W związku z tym otworzyłem konsolę programisty, znalazłem
formularz, dopisałem do tagu form dodatkowy atrybut: id=”kittens”, a potem w
konsoli napisałem magiczne zaklęcie znalezione na stack overflow:

    
    
    form = document.getElementById("kittens");
    form.submit();
    

W ten sposób wysłałem formularz, omijając walidację po stronie klienta. Serwer
przyjął i przetworzył formularz: zalogowałem się!

Czyli, aby być klientem RWE trzeba spełnić pewne wymagania. Należy do nich
znajomość HTML, Javascriptu oraz konsoli deweloperskiej w przeglądarce.

----
**Komentarze**

* Cichy (2015-10-01 19:36:00): <p>Nareszcie jakaś firma, która stawia na
  inteligentnych klientów:-).</p>
