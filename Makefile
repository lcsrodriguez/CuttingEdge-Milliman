# General Makefile for auto. doc generation
INIT_FILE=src/__init__.py

# Enable the test webserver to vizualize the documentation
on:
	@echo "Enabling test server to see documentation"
	@mkdocs serve 

# Build/Release the documentation source (html)
build:
	@echo "Building the documentation source"
	@mkdocs build 

# Build the UML graphs (packages & classes graphs)
graph:
	@echo "Building the UML graphs"
	@echo "# Init file. Keep empty" >> $(INIT_FILE)
	@pyreverse -Abo png src/ --output-directory uml/
	@pyreverse -Abo png src/ --output-directory docs/img/uml/
	@rm $(INIT_FILE)