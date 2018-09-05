Maciej Bliziński's home page
============================

Running hugo
------------

* Requires [golang](http://golang.org/); if you're installing hugo from github,
  it is likely going to be the latest version of Go.
* Installing hugo (if not from the distribution's packages):

        mkdir -p ~/src/go
        export GOPATH=~/src/go
        export GOLANG=~/src/go
        go get -u -v github.com/spf13/hugo
        alias hugo ~/src/go/bin/hugo

Styles
------

Download Bootstrap, and copy it into the static directory:

    unzip ~/Downloads/bootstrap-3.3.7-dist.zip 
    cd bootstrap-3.3.7-dist/
    cp -r css fonts js ~/src/automaciej-hugo/static/

Updating and testing the website
-------------------

        hugo -D -F server

  * -D for drafts
  * -F for future content

* Creating a new page or post:

        hugo new post/<name>/index.md

* Testing and deploying

        ./util/deploy.sh test
        ./util/deploy.sh deploy
