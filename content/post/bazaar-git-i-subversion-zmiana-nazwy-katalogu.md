+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2007-06-07T02:26:20"
draft = false
title = "Bazaar, Git i Subversion: zmiana nazwy katalogu"
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

* Uzytkownik (2007-06-07 11:46:51): <p>Najdardziej lubię bazaar &#8211; co
  z tego, jak jest on praktycznie nieużywany i niewspierany przez
  cokolwiek&#8230;</p>
* hirman (2007-06-08 00:30:03): <p>Tak naprawdę to żadne z opisanych przez
  Ciebie narzędzi nie należy do grupy <span class="caps">SCM</span>, są to
  narzędzia typu <span class="caps">VCS</span>. Do pierwszej grupy można
  zaliczyć np. Traca, który bazuje na Subversion.</p>
* Automaciej (2007-06-08 01:57:24): <p>@hirman: Podasz jakieś źródła? Szukałem
  na Wikipedii potwierdzenia tego co mówisz, ale <a
  href="http://en.wikipedia.org/wiki/Revision_control" rel="nofollow" >nie
  znalazłem</a>.</p>
* hirman (2007-06-08 20:02:12): <p>Polecam bardzo dobrą książkę &#8222;Version
  Control with Subversion&#8221; (http://svnbook.red-bean.com/). W szczególności
  wstęp do części &#8222;What is Subversion?&#8221;.</p>  <p>Na stronach
  głównych wszyscy używają pojęć version control system bądź revision control
  system.</p>  <p>Generalnie chodzi o to że żadne z wymienionych narzędzi nie
  posiada informacji na temat tego co przechowuje. Operuje na czystych danych.
  Może to być kod ale równie dobrze przepisy na wypieki, tygodniowy plan zajęć
  czy źródła książki.</p>  <p>Trudno znaleźć system spełniający kryteria dla
  <span class="caps">SCM</span>. Poszukałem trochę i znalazłem:<br /> &#8212;
  system <span class="caps">SOS</span> firmy ClioSoft dla projektantów
  sprzętu<br /> &#8212; Daversy do zarządzania zmianami w bazach danych<br />
  &#8212; IntelliJ Renamer dla języka Java (nie jestem jednak do końca pewien
  czy potrafi wersjonować kod).<br /> Pełna lista (<span class="caps">SCM</span>
  i <span class="caps">VCS</span>) http://scm.tigris.org/</p>  <p>Przy okazji
  poszukiwań okazało się że Trac to inny <span class="caps">SCM</span> &#8211;
  Software Configuration Management :)</p>
* Automaciej (2007-06-09 23:26:47): <p>Dzisiaj zauważyłem że <a
  href="http://colabti.de/irclogger/irclogger_log/git?date=2007-06-09,Sat&amp;amp;sel=229#l387"
  rel="nofollow" >rozmawiano</a> o tej sprawie na <span class="caps">IRC</span>,
  #git. Krótko, i niczym się to nie zakończyło, ale przynajmniej ktoś to
  zauważył. Szkoda że „context” był taki twardogłowy.</p>
