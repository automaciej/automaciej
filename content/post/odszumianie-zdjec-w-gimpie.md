+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2005-08-21T01:23:04"
draft = false
title = "Odszumianie zdjęć w Gimpie"
+++
Filtr „Selective Gaussian Blur” bardzo dobrze nadaje się do odszumiania
fotografii cyfrowych. Przynajmniej dla moich amatorskich celów. Brakowało mi
tylko prostej instrukcji, jak ustawić parametry? Dzisiaj to wypracowałem.

  1. Wczytujemy zdjęcie.
  2. Idziemy do: filtry → rozmycie → selektywne rozmycie Gaussa. Pokazuje się
     okienko dialogowe.
  3. Przewijając paskami znajdujemy fragment zdjęcia z dobrze widocznym szumem
     (czyli lekką kaszką).
  4. Ustawiamy „Maksymalna delta” na 255 a „promień rozmycia” na zero.
  5. Obserwując kaszkę, powiększamy powoli „promień rozmycia”, aż kaszka
     zniknie. Kaszka zamienia się najpierw w plamki, a zwiększając promień
     rozmycia można się ich również pozbyć. Jednak nie należy ustawiać zbyt
     dużych wartości. Idea jest taka żeby znaleźć najmniejszą satysfakcjonującą
     wartość promienia.
  6. Kiedy promień jest ustawiony, zmieniamy „Maksymalna delta” na zero. Kaszka
     znów się pojawia. Teraz podnosimy „deltę” powoli do góry i obserwujemy
     kaszkę. Kiedy kaszka zniknie, możemy wcisnąć OK i nasze zdjęcie zostanie
     odszumione.

UPDATE: Specjalizowane programy do odszumiania dają nieco lepsze efekty,
szczególnie jeżeli chodzi o szum powodujący przebarwienia; zgaduję że jest to
osiągane poprzez odszumianie kanałów HSV zamiast RGB. W Gimpie nie udało mi
się tego osiągnąć.

# Komentarze

* ignis (2007-08-17 15:03:30): <p>no niestety ja tez sie bawie w odszumianie w
  gimpie, bo gimp wariuje jesli dostaje informacje z nowszych aparatow :(</p>
  <p>a cinepaint testowales moze? podobno lepiej sobie radzi.</p>
* command\_dos (2009-07-15 07:01:54): <p>tutaj napisałem coś o pewnym
  plugin'ie:<br /> http://command-dos.comxa.com/2009/07/odszumianie-zdjec-w-
  gimpie/<br /> szybko, łatwo i przyjemnie ;)</p>
* Czesław (2012-03-17 22:26:22): <p>command\_dos można usunąć error404</p>
