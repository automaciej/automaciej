Maciej Bliziński's home page
============================

* Requires [golang](http://golang.org/) 1.3+, installed using
[godeb](http://blog.labix.org/2013/06/15/in-flight-deb-packages-of-go).
* Installing hugo, assuming `~/bin` is in `$PATH`:

        export GOPATH=~/go
        export GOLANG=~/go
        go get -u -v github.com/spf13/hugo
        cp ~/go/bin/hugo ~/bin

* Testing the website:

        hugo -w -D -F --theme=purehugo server

  * -D for drafts
  * -F for future content

* Creating a new page:

        hugo new page/<name>.md

* Deploying

        ./deploy.sh

## Images

    convert -size 440x440 hellotalk-inbox.jpg \
      -resize 440x440 -adaptive-sharpen 3x9 \
      +profile '*' hellotalk-inbox-440.jpg
