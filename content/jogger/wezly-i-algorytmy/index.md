---
aliases:
- /2018/09/wezly-i-algorytmy/
date: '2018-09-07T08:18:50-03:00'
description: Węzły żeglarskie mają coś wspólnego z algorytmami w informatyce.
draft: false
tags:
- informatyka
title: Węzły i algorytmy

---
Algorytm w informatyce posiada swoją podstawową strukturę, z której wprost
wynika jego skuteczność lub nieskuteczność. Jeżeli ta struktura jest
niewłaściwa, to żadna ilość poprawek, zmian i łat naokoło nie rozwiąże problemu.
Wystarczy natomiast użyć algorytmu o właściwej strukturze, i problem zostanie
rozwiązany.

<!--more-->

Bawiąc się kawałkiem sznurka i ćwicząc węzeł ratowniczy, zauważyłem że węzły
żeglarskie mają podobną cechę. Węzeł żeglarski nie musi być skomplikowany, żeby
być skuteczny. Musi mieć za to właściwą strukturę. Jeżeli nie ma tej struktury,
to żadna ilość supłania naokoło nie rozwiąże problemu. Prawidłowy węzeł
natomiast sprawdzi się niezależnie od tego, czy jest prosty czy skomplikowany.

Na przykład, węzeł ratowniczy tworzy pętlę, która się nie zaciska.


[ratowniczy]: /2018/08/wezly-zeglarskie/wezel-ratowniczy-wiazanie.gif

[ratowniczy-webm]: /2018/08/wezly-zeglarskie/wezel-ratowniczy-wiazanie.webm

<video width="200" height="113" controls autoplay loop>
<source src="wezel-ratowniczy-wiazanie.webm" type="video/webm"/>
(Twoja przeglądarka nie wyświetla filmów.)
</video>

<small>
_Sposób wiązania węzła który tu pokazuję jest amatorski, ale pokazuje w jaki
sposób węzeł jest zrobiony. Szybkie wiązanie tego węzła można zobaczyć na
YouTube pod hasłem {{< yt-search "węzeł ratowniczy na sobie" >}}._
</small>

W ten sposób możemy się opasać liną, zawiązać ten węzeł, i to pozwoli na
przykład załodze statku wyciągnąć nas z wody. Swoją drogą, wiązanie węzła
ratowniczego na sobie, w wodzie, wydaje mi się trudne. Wyobrażam sobie że
kandydaci na marynarzy ćwiczą ten węzeł tak długo, aż wiązanie go staje się dla
nich całkowicie automatyczne.

Algorytmy mają podobną charakterystykę. Każdy algorytm ma swoją podstawową
strukturę, która może składać się na przykład z pętli &ndash; nawet słownictwo
tutaj się pokrywa &ndash; i jakichś instrukcji warunkowych, określającej na
przykład moment wyjścia z tej pętli.

W zastosowaniach praktycznych algorytm najczęściej trzeba uzbroić tak żeby
radził sobie ze skrzeczącą rzeczywistością, ale żadna ilość łatania naokoło nie
pomoże, jeżeli podstawowa struktura algorytmu jest nieprawidłowa.

Estetyka też zdaje się iść w parze z funkcjonalnością, zarówno w węzłach jak
w algorytmach.  Skuteczny węzeł dobrze wygląda.  Skuteczny algorytm również
wygląda dobrze. (Co to znaczy, „jak wygląda algorytm”? Odpowiedziałbym że
zarówno kod, jak i wizualizacja działania, będą dawały wrażenie uporządkowania
i kontroli.)

Dlaczego skuteczne algorytmy są również proste? I dlaczego skuteczne węzły są
proste? Oraz… co to znaczy, skuteczne?

Skuteczność jest subiektywna, bo oznacza tyle, że algorytm robi to, czego od
niego oczekujemy my, ludzie. I my oceniamy, czy te oczekiwania zostały
spełnione, czy nie. Obiektywnie, implementacja algorytmu jest tylko kawałkiem
materii który coś robi, i nie jest to ani dobre, ani złe, ani ładne, ni
brzydkie, szybkie, wolne, prawidłowe czy nieprawidłowe.

Jeżeli oczekujemy od algorytmu że na przykład znajdzie nam element z listy
uporządkowanej od elementu najmniejszego do największego, to w pewnym sensie
porządek zawiera się już w naszym oczekiwaniu: określiliśmy, w jakiej sytuacji
algorytm będzie działać, i co chcemy dostać w wyniku.

Podobnie węzeł. Jeżeli oczekujemy od węzła, że będziemy mogli się nim opasać,
i że pętla się nie zaciśnie wokół naszych bioder, a jednocześnie pozwoli nam
umieścić na linie ciężar naszego ciała, to też jest to uporządkowane
oczekiwanie. Gdyby oczekiwanie było skomplikowane, węzeł też prawdopodobnie
musiałby być skomplikowany.

Można istniejący węzeł skomplikować. Można wziąć węzeł ratowniczy i zamiast
jednej pętelki zrobić dwie, albo wykonywać jakieś inne drobne modyfikacje. Ale
to nie zmieni faktu że jest to wciąż węzeł ratowniczy, i jest być może tylko
odrobinę mocniejszy. Odrobinę -- bo jego podstawowa siła bierze się z jego
podstawowej struktury, z tego że im mocniej obciążamy pętlę, tym mocniej jest
ona trzymana, tym większa siła działa przeciwko wyśliźnięciu się liny z węzła.

Podobnie algorytm. Jeżeli działa i jest efektywny, to dlatego że ma odpowiednią
podstawową strukturę, a nie dlatego że zrobiliśmy jakieś drobne modyfikacje.
Szybkość algorytmu sortowania tablicy, na przykład mergesort, bierze się z tego,
że liczba przebiegów programu przez całą tablicę jest relatywnie niewielka.
Dzięki temu, kiedy podwoimy wielkość danych wejściowych, czas potrzebny na
wykonanie algorytmu wzrośnie też z grubsza dwukrotnie, z niewielką tylko
zakładką; a nie na przykład czterokrotnie. Żadna drobna modyfikacja,
optymalizacja, czy pamięć podręczna, tego w zauważalny sposób nie zmieni.
