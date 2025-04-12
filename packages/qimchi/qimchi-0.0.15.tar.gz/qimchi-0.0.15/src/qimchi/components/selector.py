from pathlib import Path

from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

# Local imports
import qimchi.components.data as data
from qimchi.components.data import (
    __all__ as DATASET_TYPES,
)  # NOTE: __all__ is a list of all the public names in the module
from qimchi.components.utils import read_data
from qimchi.state import _state, DATA_REFRESH_INTERVAL
from qimchi.logger import logger


def data_selector() -> html.Div:
    """
    Generator for the data selector component.

    Returns:
        dash.html.Div: The data selector component

    """
    return html.Div(
        [
            html.Div(
                [
                    # NOTE: "upload-ticker" is used for two purposes:
                    # 1. For live measurements - updating datasets from disk
                    # 2. To conditionally refresh data_selector dropdowns
                    dcc.Interval(
                        id="upload-ticker",
                        interval=DATA_REFRESH_INTERVAL,
                        n_intervals=0,
                    ),
                    # Store to keep track of whether the data selector is set
                    dcc.Store(
                        id="is-data-selector-set",
                        data=False,
                        storage_type="memory",
                    ),
                    html.Div(
                        dcc.Input(
                            className="input",
                            type="text",
                            placeholder="Dataset Path",
                            id="dataset-path",
                            persistence=True,
                            persistence_type="local",
                        ),
                        className="column is-5 mb-0 pb-0",
                    ),
                    html.Div(
                        dcc.Dropdown(
                            options=DATASET_TYPES,
                            placeholder="Dataset type",
                            id="dataset-type",
                            persistence=True,
                            persistence_type="local",
                        ),
                        className="column is-2 mb-0 pb-0",
                    ),
                    html.Div(
                        html.Button(
                            "Submit",
                            id="submit",
                            n_clicks=0,
                            className="button is-warning",
                        ),
                        className="column is-2 mb-0 pb-0",
                    ),
                    html.Div(
                        className="column is-12 m-1 pt-0 mt-0",
                        id="data-options",
                    ),
                    dcc.Store("load-signal", data=0),
                ],
                className="columns is-full is-multiline ml-1 mr-1 is-flex is-vcentered",
                id="selector",
            ),
        ]
    )


@callback(
    Output("data-options", "children"),
    State("data-options", "children"),
    Input("dataset-type", "value"),
    Input("dataset-path", "value"),
    Input("submit", "n_clicks"),
    prevent_initial_call=True,
)
def update_options(
    sel_contents: None | html.Div, dataset_type: str, dataset_path: str, _
) -> html.Div:
    """
    Updates the options for the data selector.

    Args:
        sel_contents (None | html.Div): The current contents of the data selector
        dataset_type (str): The type of the dataset
        dataset_path (str): The path to the dataset

    Returns:
        dash.html.Div: The updated data selector component

    """
    if dataset_type is not None and dataset_path is not None:
        try:
            dataset_path = Path(dataset_path)
            logger.debug(f"Dataset Type: {dataset_type}")
            logger.debug(f"Dataset Path: {dataset_path}")

            # Import `dataset_type` class from data module and instantiate it
            data_cls = getattr(data, dataset_type)(path=dataset_path)
            logger.debug(f"Dataset Class: {data_cls}")

            # Update the state
            _state.dataset_path = dataset_path
            _state.dataset_type = dataset_type
            _state.save_state()

            return data_cls.selector()
        except AttributeError:
            # CONCERN: API: XarrayData is being handled differently from XarrayDataFolder
            logger.error("AttributeError from update_options()")
            return sel_contents
    return sel_contents


@callback(
    Output("submit", "n_clicks"),
    State("submit", "n_clicks"),
    State("dataset-path", "value"),
    State("dataset-type", "value"),
    State("is-data-selector-set", "data"),
    Input("upload-ticker", "n_intervals"),
)
def refresh(
    n_clicks: int, dataset_path: str, dataset_type: str, is_ds_set: bool, _
) -> int:
    """
    Conditionally refreshes the submit button, auto-submitting the data path
    and options to refresh the data selector dropdowns.

    Args:
        n_clicks (int): The current number of clicks
        dataset_path (str): The path to the dataset
        dataset_type (str): The type of the dataset
        is_ds_set (bool): Whether the data selector is set

    Returns:
        int: The number of clicks

    Raises:
        PreventUpdate: If `dataset_path` or `dataset_type` is not set, or if `is_ds_set` is True

    """
    logger.debug(
        f"Refresh | n_clicks: {n_clicks} | dataset_path: {dataset_path} | data_type: {dataset_type} | is_ds_set: {is_ds_set}"
    )
    if not dataset_path or not dataset_type or is_ds_set:
        logger.debug(
            "Refresh | No data path or type set; or data_selector is set. Not refreshing."
        )
        raise PreventUpdate
    logger.debug("Refresh | Refreshing data selector.")
    return n_clicks


@callback(
    Output("dependent-dropdown", "options"),
    Input("load-signal", "data"),
)
def update_dependents(sig: int | None) -> list:
    """
    Updates the dependent dropdown options.

    Args:
        sig (int | None): Signal to indicate that data has been updated

    Returns:
        list: The dependent dropdown options generated from the data

    Raises:
        PreventUpdate: If `sig` is None or 0

    """
    if sig in [None, 0]:
        raise PreventUpdate
    data = read_data(src="update_dependents")
    return list(data.data_vars.keys())


@callback(
    Output("independent-dropdown", "options"),
    Input("load-signal", "data"),
    Input("dependent-dropdown", "value"),
)
def update_independents(sig: int | None, dependents: list):
    """
    Updates the independent dropdown options.

    Args:
        sig (int): Signal to indicate that data has been updated
        dependents (list): List of dependent variables

    Returns:
        list: The independent dropdown options generated from the data

    Raises:
        PreventUpdate: If `sig` is None or 0, or `dependents` is None

    """
    if sig in [None, 0] or dependents is None:
        raise PreventUpdate
    data = read_data(src="update_independents")
    return list(data[dependents].coords)
