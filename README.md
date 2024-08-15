# fshdmcm

## Running the app

This repository holds code for a shiny app supporting a manuscript in preparation.
Further details will be added shortly once the preprint is available.
The app can be accessed [here](https://mcowley.shinyapps.io/fshdmcm/).

If you would like to run the app locally, clone the repository, and then install the required python packages with:

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
To run the tests, first install pytest into the environment you installed the requirements, via:

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
