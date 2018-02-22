import datetime, time
import sys
import urllib
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from slugify import slugify
from html.parser import HTMLParser

class settings:
	driver = "firefox"               # "firefox" or "chrome". Firefox is recommended since Chrome doesn't seen to work all the time.
	headless = True                  # True = run browser in the background without opening a browser window, False = open ordinary browser window (useful for debugging).
	screenshot_path = ""             # Path where to save screenshots.
	screenshot_fullpage = True       # True = take screenshot of full page by scrolling, False = take screenshot only of what is visible in the viewport.
	sleep_seconds = 0.5              # Delay this many seconds between scrolling.
	viewport_width = 1200            # Width of the viewport (e.g., basically browser window width)
	viewport_height = 800            # Height of the viewport (e.g., basically browser window width)
	html_parse = True                # True = parse the HTML and save to a file.
	html_path = ""                   # Path where to save HTML pages.
	html_language = "sv"             # Assumed language of the HTML page.

def processarguments(cli_args):
	""" Determine whether the arguments is a file name or a URL. """
	if len(cli_args) == 2:
		try_filename = cli_args[1]
		if isfile(try_filename):
			# Read URLs from file.
			print("Opening {0}...".format(try_filename))
			urls = readurlsfromfile(try_filename)
			counturls(urls)
			capture(urls)
			sys.exit()

	# Read URLs from input arguments.
	urls = []
	for url in list(set(cli_args)):
		if url != sys.argv[0]:
			urls.append(expandurl(url))
	counturls(urls)
	capture(urls)

def counturls(urls):
	""" Count the number of URLs found and print on screen. """
	if len(urls) == 0:
		print("Found no URLs.")
		sys.exit()
	elif len(urls) == 1:
		print("Found {0} URL.".format(len(urls)))
	else:
		print("Found {0} URLs.".format(len(urls)))

def capture(urls):
	""" Capture screenshot. """
	# Start browser.
	if settings.driver == "chrome":
		options = webdriver.ChromeOptions()
		#options.add_argument('window-size=1200x600')
		if settings.headless:
			print("Starting headless Chrome...")
			options.add_argument("headless")
		else:
			print("Starting Chrome...")
		browser = webdriver.Chrome(chrome_options = options)
	elif settings.driver == "firefox":
		options = webdriver.FirefoxOptions()
		#options.add_argument('window-size=1200x600')
		if settings.headless:
			print("Starting headless Firefox...")
			options.add_argument("--headless")
		else:
			print("Starting Firefox...")
		browser = webdriver.Firefox(firefox_options = options)
	else:
		raise BaseException("Driver {0} not found.".format(settings.driver))

	# Capture each URL.
	for url in urls:
		now = datetime.datetime.now()
		screenshot_filename = "{0}{1:%Y-%m-%d_%H-%M}_{2}.png".format(settings.screenshot_path, now, slugify(url))
		html_filename = "{0}{1:%Y-%m-%d_%H-%M}_{2}.html".format(settings.html_path, now, slugify(url))
		text_filename = "{0}{1:%Y-%m-%d_%H-%M}_{2}.txt".format(settings.html_path, now, slugify(url))
		print("Get {0}".format(url))

		# The heart of the program, screenshot web page.
		try:
			browser.get(url)
			if settings.screenshot_fullpage:
				# Take screenshot of full web page (not just the browser viewport).
				pageheight = browser.execute_script("return document.body.scrollHeight;")
				browser.set_window_size(settings.viewport_width, pageheight + 300)

				# Scroll through page in order to load all images.
				print("Scrolling page", end=" ")
				for i in range(int(pageheight / settings.viewport_height)):
					browser.execute_script("window.scrollTo(0, {0})".format(i * settings.viewport_height))
					time.sleep(settings.sleep_seconds)
					print(str(i + 1), end=" ", flush=True)
				print()

				# Scroll to bottom and to top again just to make sure whole web page is covered.
				browser.execute_script("window.scrollTo(0, 0)")
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
			else:
				# Take screenshot of visible part of web page (browser viewport).
				browser.set_window_size(settings.viewport_width, settings.viewport_height)

			print("Saving {0}...".format(screenshot_filename))
			browser.save_screenshot(screenshot_filename)

			if settings.html_parse:
				print("Saving {0}...".format(html_filename))
				print("Saving {0}...".format(text_filename))
				parsehtml(browser.page_source, html_filename, text_filename)
		except WebDriverException as e:
			print("Web driver error: {0}".format(e))

	print("Quit browser...")
	browser.quit()
	print("Finished.")

def parsehtml(html, html_filename, text_filename):
	""" Save the HTML to file and text to file. """
	f = open(text_filename, "w", encoding="utf-8")
	f.write(striphtml(html))
	f.close()

	f = open(html_filename, "w", encoding="utf-8")
	f.write(html)
	f.close()

class MLStripper(HTMLParser):
	""" Strip tags from HTML, leaving only the text. """
	def __init__(self):
		super().__init__()
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def striphtml(html):
	""" Helper function to strip tags from HTML, leaving only the text. """
	s = MLStripper()
	s.feed(html)
	return(s.get_data())

def expandurl(url):
	""" Expand short URL to full URL, e.g. example.net into http://example.net. """
	url = url.lower()
	if url.startswith("www"):
		url = "http://" + url
	elif not url.startswith("http://") and not url.startswith("https://"):
		url = "http://" + url
	if isurl(url):
		return(url)
	else:
		print("Couldn't recognize URL: {0}".format(url))
		sys.exit()

def isurl(url):
	""" Check whether the URL is valid. """
	return(urllib.parse.urlparse(url).scheme != "")

def isfile(filename):
	""" Check whether file exists. """
	try:
		myfile = Path(filename)
		if myfile.is_file():
			return(True)
	except OSError:
		return(False)
	return(False)

def readurlsfromfile(filename):
	""" Read lines from file. """
	file = open(filename, "r", encoding="utf8")
	lines = file.readlines()
	file.close()
	urls = []
	for url in lines:
		urls.append(expandurl(url))
	return(urls)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		processarguments(sys.argv)
	else:
		print("Please supply at least one URL.")
		print('Example: python {0} "http://example.net/"'.format(sys.argv[0]))
		sys.exit()
