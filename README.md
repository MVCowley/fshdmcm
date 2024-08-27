# `fshdmcm`

## Running the app

`fshdmcm` is a `shiny` app written to support a bioRxiv preprint: [Quantifying anti-DUX4 therapy for facioscapulohumeral muscular dystrophy](https://www.biorxiv.org/content/10.1101/2024.08.14.607973v1).
This work aims to explore the comparative efficacy of different anti-DUX4 therapeutic strategies for FSHD.
While reading the manuscript, use the app to further interrogate the model space and test any parameter combinations you find interesting.
The app can be accessed [here](https://mcowley.shinyapps.io/fshdmcm/).
A desktop browser is recommended.

If you would like to run the app locally, clone the repository, create a new virtual environment, and then install the required python packages with:

```python3
pip install -r requirements.txt
```

Then run the app with:

```python3
shiny run --launch-browser app.py
```

Tested with Python 3.9.19.

## Development

As this is a shiny app, it is not a directly installable python package.
To run the tests, using the same virtual environment as the app, install pytest via:

```shell
pip install pytest
```

Then from the `fshdmcm` directory run:

```shell
python -m pytest tests
```

## How to collaborate

To report a bug or request support please post an issue [here](https://github.com/MVCowley/fshdmcm/issues) outlining the problem faced and including error messages and logs where possible.

To propose a pull request, please create an issue first to discuss your proposed changes. We use [Black](https://github.com/psf/black) formatting, with a line length of 80.

For any commerical inquiries or other requests, contact us [here](m.cowley@ucl.ac.uk).
