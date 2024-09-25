+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2007-08-15T16:54:31"
draft = false
title = "Oprogramowanie naukowe kontra minus ha"
+++

Pracuję z oprogramowaniem naukowym jakieś pół roku i [nie
powiem](http://automatthias.wordpress.com/2007/07/22/scientists-share-your-source-code/)
żeby mnie zdziwiło to co zobaczyłem:

    maciej@pm:~$ impute -h
    Segmentation fault
    
Program z którym miałem nieprzyjemność pracować, jest już odrobinę lepszy.

    maciej@l2cu27:~> hapmixmap -h
    Usage: 
       hapmixmap 
    or hapmixmap -f [extra options]
    Consult the manual for details of user options.
    
    This is a list of all valid options:
    ----------------------------------------
    allelefreqoutputfile ( outputfile )
    allelefreqprecisionposteriormeanfile ( outputfile )
    allelefreqprecisionprior ( dvector )
    (...)

Ale i tak jest prawie nieużywalny. Zamiast użyć jakiejś ogólnie dostępnej
biblioteki do parsowania opcji takiej jak getopt albo Boost::program_options,
ma jakiś własny robaczywy kawałek kodu którego jedynym zadaniem jest chyba
utrudnianie życia użytkownikom.

----
**Komentarze**

* D4rky (2007-08-15 17:13:58): <p>do czego uzywasz tego typu rzeczy?</p>
* Automaciej (2007-08-15 17:33:02): <p>Do analizy danych genetycznych, przy czym
  moja rola jest wyłącznie narzędziowa, zapuszczam analizy, zbieram wyniki i
  dostarczam profesorowi w strawnej formie. A programy są tak pokręcone że
  potrzeba inżyniera żeby w ogóle z nich korzystać.</p>
* Piotr W. (2007-08-21 00:22:17): <p>Boost jest bardzo niechlujny i niestety
  wielu programistów używa tego szajsu :( dlatego nie ma się co dziwić, że ktoś
  tworzy coś swojego &#8211; choć nie zawsze mu to wychodzi.</p>
* Automaciej (2007-08-21 01:37:18): <p>Wierz mi, Boost jest o <em>wiele</em>
  porządniejszy niż to z czym tu mamy do czynienia. A programista, który jest w
  stanie napisać coś lepszego niż Boost powinien wiedzieć, co jest nie tak w
  Boost i wiedzieć dlaczego jego kod jest lepszy. Ja na przykład nie wiem co
  jest nieporządnego w Boost i uważam że używanie np. wzorca klasy smart pointer
  zaoszczędziłoby masę segfaultów i dziesiątek godzin debugowania. Podobnie z
  parsowaniem parametrów command-line i konfiguracji. Swoją drogą, jeżeli znasz
  jakieś konkretne materiały przeciwko Boost, podaj linki.</p>
