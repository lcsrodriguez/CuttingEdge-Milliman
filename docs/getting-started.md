# Getting started

## Clone & Run the project

1. Clone the repository:
```bash
git clone git@github.com:lcsrodriguez/CuttingEdge-Milliman.git
cd CuttingEdge-Milliman/
```

!!! note
    One can also download the repository by clicking on the green button **Code** > **Download ZIP**.

2. Verify the requirements to execute the Jupyter Notebook
```bash
python3 --version
pip3 -V
pip3 install -r requirements.txt
```

3. Run the Jupyter-Notebook 
```bash
jupyter-notebook main.ipynb
```

4. Check and handle the figures stored in `out/`:
```bash
ls out/
cd out/
```

## Build the documentation

1. Install these additional requirements
```bash
pip3 install mkdocs "mkdocstrings[python]" mkdocs-material
```

2. Convert the Jupyter Notebook file (`.ipynb` extension) into a Python script file (`.py`)
```bash
jupyter nbconvert --to script main.ipynb --output out/main
cat out/main.py
```

3. Perform the needed updates in the code

4. Run the following command to release the last version of the documentation 
```bash
mdkocs build
```

!!! danger "Warning"
    One can retrive the built version of the documentation in `site/` which is programmed to never be pushed onto the online Git repo.