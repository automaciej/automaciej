+++
date = "2007-06-07T02:26:20"
draft = false
title = "Bazaar, Git i Subversion: zmiana nazwy katalogu"
aliases = [ "/2007/06/bazaar-git-i-subversion-zmiana-nazwy-katalogu/",]

+++

Chyba każdy kto uczył się zarządzać kodem, zaczynał od CVS a potem przenosił się
na coś innego. Przeważnie na Subversion, które z założenia jest rozwijane jako
[zamiennik](http://subversion.tigris.org/faq.html#why) i ulepszenie CVS.  Dla
programistów żądnych przygód lub po prostu bardziej wymagających, mamy Git,
Bazaar, Monotone, Mercurial, Darcs... i [wiele
innych](http://en.wikipedia.org/wiki/Comparison_of_revision_control_software).

Mark Shuttleworth napisał [ciekawą
rzecz](http://www.markshuttleworth.com/archives/123): mianowicie, że zmiana nazw
plików i katalogów to jedna z najważniejszych operacji potrzebnych przy
zarządzaniu kodem. Podał tam przykład zmiany nazwy katalogu w jednej gałęzi
z jednoczesnym dodaniem pliku do tego katalogu w drugiej gałęzi. Z czystej
ciekawości napisałem test, który sprawdza zachowanie trzech programów, które
znam: Bazaar, Git i Subversion. Scenariusz jest następujący:

1\. Utworzony jest projekt z jednym katalogiem i jednym plikiem w tym
katalogu.

    
    
    
    `-- project
        `-- dir-a
            `-- foo.txt
    
    

2\. Programista A tworzy gałąź, w której zmienia nazwę katalogu.

    
    
    
    `-- project
        `-- dir-b
            `-- foo.txt
    
    

3\. Jednocześnie, programista B modyfikuje ten plik i dodaje nowy, w czasie
kiedy katalog jest jeszcze pod starą nazwą.

    
    
    
    `-- project
        `-- dir-a
            |-- bar.txt
            `-- foo.txt
    
    

4\. Programista C tworzy nową gałąź, po czym dołącza do niej zmiany z gałęzi
A, a następnie zmiany z gałęzi B. Po takim połączeniu, oczekiwałbym że projekt
będzie zawierał jeden katalog z dwoma plikami.

    
    
    
    `-- project
        `-- dir-b
            |-- bar.txt
            `-- foo.txt
    
    

Z trzech programów które przetestowałem, tylko Bazaar zachował się w ten
sposób. Git utworzył dwa katalogi (dir-a i dir-b), a Subversion zignorowało
plik bar.txt i w ogóle nie umieściło go w złączeniu.

Test który napisałem, odnosi się tylko do trzech programów. Jeżeli napiszesz
ten sam test do swojego systemu zarządzania kodem, chętnie zobaczę wyniki!
Tymczasem, dla tych którzy chcą sami zobaczyć jak to działa, przygotowałem do
pobrania archiwum ze skryptami:

(niestety, kod już nie jest dostępny)

Testy są w postaci skryptów w bashu i były testowane pod Linuksem. Załączony
jest też plik README (po angielsku).

_Uaktualnienie: (2007-06-08), a_

Dennis Lambe dodał test dla Darcs. Z przyjemnością stwierdziłem, że Darcs
obsługuje zmiany nazw katalogów prawidłowo: po połączeniu zmian z obydwu
gałęzi mamy jeden katalog z dwoma plikami. Dołączyłem ten test do archiwum
powyżej.

_Uaktualnienie: (2007-06-08), b_

Usunąłem wszystkie trzyliterowe skróty z artykułu żeby uniknąć dyskusji o nich
i trzymać się tematu.

----
**Komentarze**

* Uzytkownik (2007-06-07 11:46:51): Najdardziej lubię bazaar &#8211; co
  z tego, jak jest on praktycznie nieużywany i niewspierany przez
  cokolwiek&#8230;
* hirman (2007-06-08 00:30:03): Tak naprawdę to żadne z opisanych przez
  Ciebie narzędzi nie należy do grupy SCM, są to
  narzędzia typu VCS. Do pierwszej grupy można
  zaliczyć np. Traca, który bazuje na Subversion.
* Automaciej (2007-06-08 01:57:24): @hirman: Podasz jakieś źródła? Szukałem
  na Wikipedii potwierdzenia tego co mówisz, ale nie
  znalazłem.
* hirman (2007-06-08 20:02:12): Polecam bardzo dobrą książkę &#8222;Version
  Control with Subversion&#8221; (http://svnbook.red-bean.com/). W szczególności
  wstęp do części &#8222;What is Subversion?&#8221;.  Na stronach
  głównych wszyscy używają pojęć version control system bądź revision control
  system.  Generalnie chodzi o to że żadne z wymienionych narzędzi nie
  posiada informacji na temat tego co przechowuje. Operuje na czystych danych.
  Może to być kod ale równie dobrze przepisy na wypieki, tygodniowy plan zajęć
  czy źródła książki.  Trudno znaleźć system spełniający kryteria dla
  SCM. Poszukałem trochę i znalazłem:  
 &#8212;
  system SOS firmy ClioSoft dla projektantów
  sprzętu  
 &#8212; Daversy do zarządzania zmianami w bazach danych  

  &#8212; IntelliJ Renamer dla języka Java (nie jestem jednak do końca pewien
  czy potrafi wersjonować kod).  
 Pełna lista (SCM
  i VCS) http://scm.tigris.org/  Przy okazji
  poszukiwań okazało się że Trac to inny SCM &#8211;
  Software Configuration Management :)
* Automaciej (2007-06-09 23:26:47): Dzisiaj zauważyłem że rozmawiano o tej sprawie na IRC,
  #git. Krótko, i niczym się to nie zakończyło, ale przynajmniej ktoś to
  zauważył. Szkoda że „context” był taki twardogłowy.
