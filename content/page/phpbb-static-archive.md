+++
# vim:set nosmartindent nocindent ft=markdown:
date = "2016-05-05T15:19:06+01:00"
draft = true
title = "phpBB static archive"
tags = ["phpbb"]
menu = ["main"]
language = "en"
+++
I looked online for instructions on how to create a static phpBB archive of
a retired forum, and didn't find much, apart from other people asking the same
thing. Here's what I did.

## General options

There's a couple of possible approaches. One of the criteria is future
maintenance cost. I'm assuming that the reason that you want a static archive is
that you want it to not require maintenance, or require as little as possible.

* Lock the forum and let phpBB continue to run.
   * Pros:
      * There's little to do, so it's quick.
   * Cons:
      * High mantenance. It's not static. You're still running PHP, so you have
        to keep on upgrading your PHP installation and your phpBB installation,
        or your forum archive will get hacked.
* Write your own exporter: Query the database with SQL and write the output the
  way you want it.
   * Pros:
      * Low maintenance of the resulting site. 
      * High level of control of how the output is structured.
   * Cons:
      * Writing the exporter is time consuming.
      * The output will most likely look different from the original forum, so
        people used to the forum who are browsing it will be likely confused
        about the navigation.
      * You need to put in additional work to preserve the old URLs.
   * Comment: Also… you could even generate a set of Markdown files to be fed as
     input to a static website generator such as hugo. This would give you a lot
     of things for free, including nice URLs and a sitemap.
* Download the whole forum using wget or httrack.
   * Pros:
      * The result looks the same as the original.
   * Cons:
      * Out of the box, it does not work! It requires tweaks as discussed below.
      * Lots of content duplication. If there are different URLs with the same
        content, they will exist as separate files on disk.

## Here's what I did

I'm intentionally not trying to write the whole thing in a form of a script,
even though it was tempting. I expect different phpBB installations to vary, and
the chance that my script would work with somebody else's forum is slim. So
instead I'll write up what I did step by step, and people can follow this howto
and make alterations as they see fit.

Note: I'm using Apache and I'm quoting Apache specific configuration lines.

### Mirroring the forum

I downloaded the database and the forum snapshot to a local computer to start
a local instance. It's a hassle but it makes things quicker. Once it was ready,
I created a mirror on disk:

    wget --mirror -k -p <Forum URL>

After downloading it turned out that I had 127 thousand files on disk, which
takes up 5GB of space as shown by `du -sh <directory>`. I mean I've seen larger
in my career, but I expected a smaller size from a generally text-based static
forum archive.

I've put result of wget's work on a test server to see how it works.

### Question marks

During testing it turned out that the "?" in the URL is treated as a special
character. For example, when the browser requests this:

    GET /style.php?id=1 HTTP/1.1

…the WWW server is looking for a file on disk named style.php, fails to find
it, and returns a HTTP 404 error.

    HTTP 404: style.php not found

But in our case we want the server to serve the file named "style.php?id=1"!

```
$ ls -l style.php*
-rw-rw-r-- 1 maciej maciej 71445 Apr 24 15:58 style.php?id=1&lang=pl
-rw-rw-r-- 1 maciej maciej 71445 Apr 24 16:24 style.php?id=1&lang=pl&sid=2231c9b38ea28f9aa9e9bdd2a8452846
```

By the way, did you noticed the file with sid? Ugh. Anyway…

With help from StackOverflow I've found these magic lines that I added to
`.htaccess`:

    RewriteCond %{ENV:REDIRECT_STATUS} !200 
    RewriteCond %{QUERY_STRING} !^$ 
    RewriteRule ^(.*)$ %{REQUEST_URI}\%3F%{QUERY_STRING} [noescape,last,qsdiscard]

I don't fully understand what it does, but it seems to work. As far as I could
understand &mdash; when the query string is not empty ("?foo=bar" in the URL),
the request is rewritten in such a way that we're putting it together again
using REQUEST\_URI and QUERY\_STRING, and we're connecting them with "%3F" which
is an urlencoded question mark. When this is done, Apache understands that we
mean a "?" on disk, and not a url/query string combination. We also have to add
"qsdiscard" to prevent Apache from appending the query string again onto the
URL. In a way, Apache is trying to do the right thing: keeping the file part and
the query string part of the URL meaningful and separate. But in this case we
want to do something opposite: treat the "?" literally as a part of file name.

By the way, the solution I found on StackOverflow was slightly different and
didn't work for me verbatim.

### Done-ish? Probably not

OK, so this is the rudimentary version of the archive. It has a number of
disadvantages, but it meets the main criteria: we have static files and the
content is there, you can browse it.

What are the problems?

1.  The login form and the search box are is still there, which is confusing for
    people, they will try to log in and wonder why it's broken.

    Addressed below.

1.  A number of URLs won't work. There is a number of reasons for this, one of
    them is the parameter ordering. The web server isn't interpreting the query
    strings any more, so these two are different now:

        viewtopic.php?f=1&t=2
        viewtopic.php?t=2&f=1

    In the PHP world they were interpreted and became part of the URL parameter
    namespace regardless of the order, but now Apache is just looking for files
    on disk, and it just looks for files named exactly as specified in the URL.
    So some URLs that used to work, especially if somebody linked to your forum
    from the outside, will not work.

    Not addressed as of 2016-05-05.

1.  URLs are ugly. I know that search engines can deal with this sort of stuff,
    and they can do things like filtering out the "sid" parameter from the URL.
    But still, I keep on thinking that the forum URLs should be more like:
   
        /forum/1/4/i-like-fluffy-kittens/

    Not addressed as of 2016-05-05.

1.  No sitemap.

    Not addressed as of 2016-05-05.

1.  Not mobile friendly. This isn't a problem with the archiving process per se,
    but it is a feature I would expect in a good archive.

    Not addressed as of 2016-05-05.

### Login form and the search box.

The next thing I noticed is that there still is a login form in the HTML. It is
confusing for people because there's nothing indicating that there's nothing to
log into. I wanted to remove the form, but it was duplicated across 127 thousand
files!

First I tested it on one file:

    sed -i -e '/<div id="search-box">$/,+9d' viewtopic.php?…

And then ran across all files:

    find . -name '*.php*' -exec sed -i -e '/<div id="search-box">$/,+9d' {} \;

This took a fair bit of time, but was successful. I actually don't know how much
because I went out for a small hike.

### Let's make it smaller

The reason why the forum occupies a large amount of disk space is that a small
file still occupies a full block on disk, so there's a sort of file count tax
that you have to pay when storing files on disk. But there's something that you
can do. I realized that the forum archive is static, so I can use a read-only
file system, and there are read-only file system which pack files efficiently.
After a quick look around, [SquashFS](https://en.wikipedia.org/wiki/SquashFS)
turned up as the best pick, with efficient file packing, compression, and
support in the Linux kernel. The whole packed forum shrinked from 5G to 517MB.
I mounted it using the loopback device on the web server (added it to
/etc/fstab), and voila! Almost 10× reduction in size. My web server only has 20G
of disk space, so saving 4.5G is significant.

### Unresolved problems

At the time of writing there's a number of problems I haven't addressed in my
forum archive.  If I manage to, I'll update this page with new information.

The resulting forum archive is available at https://www.atopowe.pl/forum/.
