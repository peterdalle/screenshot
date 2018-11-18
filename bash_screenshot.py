#!/usr/bin/env python
from slugify import slugify		# pip install python-slugify
import subprocess
import datetime
import sys

# Main function.
def main(url):
	filename = create_filename(url, datetime.datetime.now(), path="./")
	run_bash(url, filename)

# Create filenames with date and url like "2018-01-01-18-40_http-www-example-net.png".
def create_filename(url, time, path):
	return("{0}{1:%Y-%m-%d-%H-%M}_{2}.jpg".format(path, time, slugify(url)))

# Run Bash command to create screenshot.
def run_bash(url, filename):
	bash_cmd = 'xvfb-run --auto-servernum --server-num=1 --server-args="-screen 0 1024x8048x16" cutycapt --url="{}" --out="{}"'.format(url, filename)
	subprocess.call(bash_cmd, shell=True)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		print("Usage: python {} [url]".format(sys.argv[0]))
