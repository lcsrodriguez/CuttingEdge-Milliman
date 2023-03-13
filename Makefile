# General Makefile

# Enable the test webserver to vizualize the documentation
on:
	mkdocs serve 

# Build/Release the documentation source (html)
build:
	mkdocs build 