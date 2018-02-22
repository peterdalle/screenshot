# Screenshot

Create a screenshot of a full web page, not only the visible part of the web page that is above the fold (browser viewport). This is achieved by automatically opening and scrolling through a web page to force dynamic images to load. Then a screenshot is saved to a PNG file.

PNG files can become quite large, like 30 MB or so for the front page of a news site.

## Install

1. Install dependencies [Selenium](https://www.seleniumhq.org/) (the actual thing that does all the work) and [python-slugify](https://pypi.python.org/pypi/python-slugify) (converts URLs into file names, e.g. `www.google.com` into `www-google-com`):

```bash
pip install selenium
pip install python-slugify
```

2. Download a [web driver](https://www.seleniumhq.org/docs/03_webdriver.jsp). I recommend firefox over chrome due to compatability.

3. Make sure Python can find the web driver by modifying your PATH environment variable. This is described in the [Selenium installation guide](http://selenium-python.readthedocs.io/installation.html).

4. Download Screenshot:

```bash
$ git clone git@github.com:peterdalle/screenshot.git
```

## Usage

Provide a URL or domain name as argument:

```bash
$ python screenshot.py google.com
```

A file like `2018-01-12_18-02_http-google-com.png` is then saved in your current directory, with current date and time stamp (yyyy-mm-dd_hh-mm).

Provide multiple URLs or domin names as arguments:

```bash
$ python screenshot.py google.com bbc.com svt.se "https://example.net/search?q=test&p=3"
```

Note that the `&` character in URLs have a special meaning in the terminal/command prompt, so don't forget to enclose those URLs in `"` quotes.

You can also provide a file name (`urls.txt`) with one URL or domain name per line:

```bash
$ python screenshot.py urls.txt
```

## Settings

Change the behavior of the program in the [`settings` class](/screenshot.py#L10). Each setting is documented there.

The most important setting is probably `headless = True` which means that a browser is opened in the background without opening a visible browser window.

## Known issues

### Memory hog

Selenium seem to have a problem closing the web driver, resulting in lots of web drivers left running and clogging down memory resources. You may need to kill the running processes now and then, especially if you screenshot with crontab.
