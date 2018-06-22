+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2007-08-19T14:10:00"
draft = false
title = "Czy można umysłem generować liczby losowe?"
+++
Wiele sztuczek takich, jak te które demonstruje Derren Brown, opiera się na
tym, że prosi się jakąś osobę o wybranie jakiejś liczby, przy czym
[brzmi](http://en.wikipedia.org/wiki/Derren_Brown#Russian_Roulette) to na
przykład tak:

> Choose _one_ of those numbers, keep them to yourself, choose _one_, it doesn't
> matter which _one_ it is, settle on a number, are you thinking of _one_ now...

Nic dziwnego, że osoba do której mówił, wybrała liczbę 1.

Wymyślanie liczby losowej jest, mam wrażenie, czynnością dla człowieka bardzo
nienaturalną. Nasz umysł pracuje zawsze w przeciwnym kierunku, stara się
doszukiwać związków i w miarę możliwości eliminować losowość. Liczba losowa to
liczba „bez sensu”, oderwana od wszystkiego naokoło. Praca „bez sensu” to
ostatnia rzecz jaką nasz umysł chciałby wyprodukować. Nie wiem jak wy, ale ja,
poproszony o wymyślenie liczby losowej, zawsze wpadam w panikę: Liczba? Ale
jaka? Byle jaka? Jak to byle jaka? Skąd mam ją wziąć? Wymyślić? Ale jak? Skąd
będę wiedział że jest losowa?

[![Dilbertowy generator liczb losowych](http://www.etoan.com/random-number-generation/dilbert2001182781025.gif)](http://www.etoan.com/random-number-generation/dilbert2001182781025.gif)

Gdybyśmy chcieli naprawdę wybrać liczbę losową, moglibyśmy na przykład kilka
razy [rzucić monetą](http://www.random.org/coins/), a wyniki potraktować jako
bity. Gdyby wylosowana liczba wyszła poza interesujący nas zakres, eksperyment
można by powtórzyć.

A co jeżeli nie mamy monety? Czy można wymyślić jakiś sposób generowania „w
głowie” liczb losowych lub przynajmniej bardzo mało podatnych na sugestię, bez
użycia rekwizytów takich jak moneta?

Komputery przy generowaniu liczb losowych często używają zewnętrznej entropii,
takiej jak ruch sieciowy, dostęp do dysku czy poruszenia myszą. Czy mamy takie
bodźce zmysłowe, których możemy użyć do generowania liczb losowych, a którymi
byłoby trudno manipulować? Na przykład, wybierać zera i jedynki na podstawie
czegoś, co widzimy, słyszymy lub czujemy. (Bodźców smakowych czy węchowych
byłoby chyba trudniej użyć.)

Albo może inny sposób, może użyć czegoś podobnego do techniki sugerowanej
przez `man passwd`:

> Inna metoda konstrukcji hasła polega na wyborze łatwego do zapamiętania zdania
> (np. z literatury) i wyborze pierwszej bądź ostatniej litery każdego wyrazu.
> Przykładem tego jest:  
  
      Ask not for whom the bell tolls.  
co daje  
      An4wtbt,  
albo też  
      A czy znasz Ty, bracie młody  
co daje  
      A3zTbm.

Wygenerowane ciągi już bardziej przypominają liczby losowe niż jedynka
zasugerowana przez Derrena Browna. Pozostaje kwestia zamiany liter na bity
albo cyfry.

Macie jakieś inne pomysły?

# Komentarze

* 9gods (2007-08-20 10:29:32): <p>Przeprowadzano eksperymenty (na
  uniwersytetach), w których komputer non stop generował losowe cyfry a
  uczestnikom kazano koncentrować się na jednej z nich. I próbki wykazywały, że
  wybrana cyfra występowała o jakiś znaczący procent (większy niż błąd
  statystyczny) częściej niż inne.</p>
* 9gods (2007-08-20 11:43:18): <p>Kiedy prosisz człowieka o wybranie losowo
  jakieś cyfry, będzie oczywiście ona z czymś związana: albo będzie to ulubiona,
  albo ostatnio usłyszana czy może taka, która wydaje mu się najmniej
  prawdopodobna. I tu można stwierdzić, że nie do końca jest ona losowa. Ale
  proces wybierania sposobu wybierania :) można już nazwać losowym, bo często
  nawet dla tej osoby jest on niewiadomy.</p>  <p>Cyfr jest niewiele i zawsze
  przy pytaniu o nie jest duża szansa, że ktoś wykorzysta schemat, który był już
  raz przez niego użyty. Jednak przy większych liczbach możemy już mówić o
  losowości.</p>  <p>Co zaś się tyczy twojej paniki to powstaje ona dla tego, że
  chcesz intelektualizować, zamiast losować :) Po prostu wyrzuć z siebie ciąg
  przypadkowych liczb nie próbując ich oceniać.</p>
* Automaciej (2007-08-21 08:48:43): <p>„Po prostu wyrzuć z siebie ciąg
  przypadkowych liczb nie próbując ich oceniać.”<br /> Dokładnie w ten sposób
  ulega się sugestii i manipulacji.</p>
* Alaxafel (2008-01-16 15:28:45): <p>Umysłem to średnio, ale zawsze można
  spojrzeć na zegarek i wziąć ostatnią cyfrę sekundnika &#8211; jeśli potrzebna
  jest jedna liczba losowa to mamy gwarancję że ona jest losowa, bo kto bez
  uprzedniego sprawdzenia powie która jest aktualnie sekunda?</p>
