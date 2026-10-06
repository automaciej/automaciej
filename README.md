Hi!

I'm an ex-Google SRE, on a career break as of 2026. I'm currently pursuing my
own music projects.

https://blizin.ski

## Before committing

Run the site expectations test; it builds the site and checks head tags,
structured data, feeds, links, and the /bio/ releases list:

```bash
python3 util/test_site_expectations.py
```

All tests must pass before `git commit`. When a feature once went missing and
had to be restored, add a test for it in `util/test_site_expectations.py`.
