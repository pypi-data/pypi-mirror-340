from pathlib import Path
from typing import Any, List

import dash
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

# Local imports
from ..base import Data, Database
from qimchi.state import _state
from qimchi.logger import logger
from qimchi.components.utils import read_data


def _update_options_fn(
    src: str,
    condition_list: List[str | Path | Any],
    check_file: bool = False,
    default_return: List[str] | None = [],
) -> List[str] | str | None:
    """
    Helper function to update options based on the condition list.

    Args:
        src: Source of the update.
        condition_list (List[str | Path | Any]): List of parameters to compare with None.
            Ordering matters, as the path is constructed from the first item to the second last item.
            The last item is always assumed to be `dataset_type`
        check_file (bool, optional): Check if the path is a file, by default False (checks for directory)
        default_return (List | None, optional): Default return item if the condition is not satisfied, by default []

    Returns:
        List[str] | str | None: List of strings (options) or empty list or None

    """
    logger.debug(f"_update_options_fn | src: {src}")

    # NOTE: This only checks for truthy (i.e., "" is False, but Path("") is True). Should work here though.
    if all(condition_list):
        # Assuming either strings or Paths
        path = Path(*condition_list[:-1])

        if not path.is_dir():
            logger.debug(f"Path {path} is not a directory.")
            return default_return
        # Unfiltered options
        options: List[str] = [p.name for p in path.iterdir()]
        # Filter for only files or directories
        options = [
            opt
            for opt in options
            if (
                # TODOLATER: Some redundancy here
                (path / opt).is_dir() and (path / opt).suffix == ".zarr"
                if check_file
                else (path / opt).is_dir()
            )
        ]
        logger.debug(f"_update_options_fn | src: {src} | options: {options}")
        return options

    logger.debug(f"_update_options_fn | src: {src} | default_return: {default_return}")
    return default_return


def _should_update_data(path: Path, sig_curr: int, origin: str) -> bool:
    """
    Conditionally update the data store with the Zarr file content.

    Args:
        path (Path): Path to the dataset
        sig_curr (int): The current signal

    Returns:
        bool: Whether the data has been updated

    """
    if path.is_dir() and path.suffix == ".zarr":
        curr_mod_time = path.stat().st_mtime
        if str(path) == str(_state.measurement_path):
            if curr_mod_time != _state.measurement_last_fmt:
                logger.warning(
                    f"_should_update_data | {origin}: DATA UPDATED ON DISK!! AT {path}."
                )
                _state.measurement_last_fmt = curr_mod_time
                _state.save_state()
                return True

            # If the data has not been loaded even once, load it (e.g., for the first time on page load)
            if sig_curr in [None, 0]:
                logger.warning(
                    f"_should_update_data | {origin}: DATA BEING LOADED FROM {path}"
                )
                return True
            # If the data has been loaded, do not update
            else:
                return False

        else:
            # If the path has changed, update the state
            logger.warning(
                f"_should_update_data | {origin}: DATA PATH MODIFIED!! AT {path}."
            )
            _state.measurement_path = path
            _state.measurement_last_fmt = curr_mod_time
            _state.save_state()

            if origin == "XarrayData":
                # To update the wafer_id etc. in the state
                data = read_data(src="_should_update_data")
                metadata = data.attrs
                device_type = metadata.get("Device Type", "")
                wafer_id = metadata.get("Wafer ID", "")
                sample_name = metadata.get("Sample Name", "")
                meas_id = metadata.get("Measurement ID", "")

                # Update the state
                _state.device_type = device_type
                _state.wafer_id = wafer_id
                _state.device_id = sample_name
                _state.measurement = meas_id
                _state.save_state()

            logger.warning(
                f"_should_update_data | {origin}: DATA LOADED FROM MODIFIED {path}"
            )
            return True


class XarrayDataFolder(Database):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    @callback(
        Input("measurement", "value"),
        Input("measurement-type", "value"),
        Input("device-id", "value"),
        Input("device-type", "value"),
        Input("wafer-id", "value"),
    )
    def update_state_dropdown_vals(
        measurement: str,
        measurement_type: str,
        device_id: str,
        device_type: str,
        wafer_id: str,
    ) -> None:
        """
        Update the state with the wafer id, device type, device id, measurement type, and measurement.

        """
        _state.wafer_id = wafer_id if wafer_id else _state.wafer_id
        _state.device_type = device_type if device_type else _state.device_type
        _state.device_id = device_id if device_id else _state.device_id
        _state.measurement_type = (
            measurement_type if measurement_type else _state.measurement_type
        )
        _state.measurement = measurement if measurement else _state.measurement
        _state.save_state()

    @staticmethod
    @callback(
        Output("is-data-selector-set", "data"),
        Output("wafer-id", "options"),
        State("wafer-id", "options"),
        Input("dataset-path", "value"),
        Input("dataset-type", "value"),
        Input("submit", "n_clicks"),
        prevent_initial_call=True,
    )
    def update_wafer_id(
        wafer_options: List[str],
        dataset_path: str | Path,
        dataset_type: str,
        *_,
    ) -> List[str]:
        """
        Update the wafer ID options based on the dataset path and type.
        Also sets the `is-data-selector-set` flag to True.
        This function is triggered by the submit button and updates the wafer ID options in the dropdown.
        This in turn triggers other dropdowns sequentially.

        Args:
            wafer_options (List[str]): Current wafer ID options
            dataset_path (str | Path): Path to the dataset
            dataset_type (str): Type of the dataset

        Returns:
            bool: Whether the data selector is set
            List[str]: Updated wafer ID

        """
        input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        logger.debug(f"update_wafer_id || Input ID: {input_id}")
        logger.debug(
            f"update_wafer_id | Dataset Path: {dataset_path} | Dataset Type: {dataset_type}"
        )
        logger.debug(f"update_wafer_id || Wafer Options: {wafer_options}")

        key = "wafer_id"
        opts = _update_options_fn(
            key,
            [dataset_path, dataset_type],
            default_return=wafer_options,
        )

        return bool(opts), opts

    @staticmethod
    @callback(
        Output("device-type", "options"),
        State("device-type", "options"),
        Input("wafer-id", "value"),
        Input("dataset-path", "value"),
        Input("dataset-type", "value"),
        Input("submit", "n_clicks"),
        prevent_initial_call=True,
    )
    def update_device_type(
        device_type_options: List[str],
        wafer_id: str,
        dataset_path: str | Path,
        dataset_type: str,
        *_,
    ) -> List[str] | None:
        input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        logger.debug(f"update_device_type || Input ID: {input_id}")

        key = "device_type"

        return _update_options_fn(
            key,
            [dataset_path, wafer_id, dataset_type],
        )

    @staticmethod
    @callback(
        Output("device-id", "options"),
        State("device-id", "options"),
        Input("device-type", "value"),
        Input("wafer-id", "value"),
        Input("dataset-path", "value"),
        Input("dataset-type", "value"),
        Input("submit", "n_clicks"),
        prevent_initial_call=True,
    )
    def update_device_id(
        device_id_options: List[str],
        device_type: str,
        wafer_id: str,
        dataset_path: str | Path,
        dataset_type: str,
        *_,
    ) -> List[str] | None:
        input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        logger.debug(f"update_device_id || Input ID: {input_id}")

        key = "device_id"

        return _update_options_fn(
            key,
            [dataset_path, wafer_id, device_type, dataset_type],
        )

    @staticmethod
    @callback(
        Output("measurement-type", "options"),
        State("measurement-type", "options"),
        Input("device-id", "value"),
        Input("device-type", "value"),
        Input("wafer-id", "value"),
        Input("dataset-path", "value"),
        Input("dataset-type", "value"),
        Input("submit", "n_clicks"),
        prevent_initial_call=True,
    )
    def update_measurement_type(
        measurement_type_options: List[str],
        device_id: str,
        device_type: str,
        wafer_id: str,
        dataset_path: str | Path,
        dataset_type: str,
        *_,
    ) -> List[str] | None:
        input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        logger.debug(f"update_measurement_type || Input ID: {input_id}")

        key = "measurement_type"

        return _update_options_fn(
            key,
            [dataset_path, wafer_id, device_type, device_id, dataset_type],
        )

    @staticmethod
    @callback(
        Output("measurement", "options"),
        State("measurement", "options"),
        Input("measurement-type", "value"),
        Input("device-id", "value"),
        Input("device-type", "value"),
        Input("wafer-id", "value"),
        Input("dataset-path", "value"),
        Input("dataset-type", "value"),
        Input("submit", "n_clicks"),
        Input("upload-ticker", "n_intervals"),
        prevent_initial_call=True,
    )
    def update_measurement(
        measurement_options: List[str],
        measurement_type: str,
        device_id: str,
        device_type: str,
        wafer_id: str,
        dataset_path: str | Path,
        dataset_type: str,
        *_,
    ) -> List[str] | None:
        input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        logger.debug(f"update_measurement || Input ID: {input_id}")

        key = "measurement"
        options = _update_options_fn(
            key,
            [
                dataset_path,
                wafer_id,
                device_type,
                device_id,
                measurement_type,
                dataset_type,
            ],
            check_file=True,  # Checks if the path is a measurement file
        )
        options.sort(key=lambda x: int(x.split("-")[0]))

        # If measurement_options is None, return new options
        if not measurement_options:
            return options

        # Else, if the input_id is "upload-ticker", check if the options are the same
        if input_id == "upload-ticker":
            # If same, PreventUpdate
            if set(measurement_options) == set(options):
                logger.debug(
                    "update_measurement | Measurement options are the same. Preventing update."
                )
                raise PreventUpdate
            # If not the same, return the updated options
            else:
                logger.debug(
                    "update_measurement | Measurement options are different. Updating measurement options."
                )
                return options
        return options

    @staticmethod
    @callback(
        Output(
            "load-signal",
            "data",
            allow_duplicate=True,
        ),
        State("load-signal", "data"),
        Input(
            "measurement",
            "value",
        ),
        State("measurement-type", "value"),
        State("device-id", "value"),
        State("device-type", "value"),
        State("wafer-id", "value"),
        State("dataset-path", "value"),
        Input("upload-ticker", "n_intervals"),
        prevent_initial_call=True,
    )
    def update_data(
        sig_curr: int,
        measurement: str,
        measurement_type: str,
        device_id: str,
        device_type: str,
        wafer_id: str,
        dataset_path: str | Path,
        *_,
    ) -> dict:
        """
        Update the data store with the Zarr file content.

        Args:
            sig_curr (int): The current signal value
            measurement (str): Measurement name
            measurement_type (str): Measurement type
            device_id (str): Device ID
            device_type (str): Device type
            wafer_id (str): Wafer ID
            dataset_path (str | Path): Path to the dataset

        Returns:
            dict: The updated data store

        Raises:
            PreventUpdate: If the path is not a file or not a Zarr file

        """
        input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        logger.debug(f"update_data | Input ID: {input_id}")
        logger.debug(
            f"update_data | Measurement: {measurement} | Measurement Type: {measurement_type} | Device ID: {device_id} | Device Type: {device_type} | Wafer ID: {wafer_id} | Dataset Path: {dataset_path}"
        )

        if all(
            [
                measurement,
                measurement_type,
                device_id,
                device_type,
                wafer_id,
                dataset_path,
            ]
        ):
            measurement_path = Path(
                dataset_path,
                wafer_id,
                device_type,
                device_id,
                measurement_type,
                measurement,
            )
            path = measurement_path
            if _should_update_data(path, sig_curr, "XarrayDataFolder"):
                return sig_curr + 1 if sig_curr is not None else 1
            else:
                raise PreventUpdate

    @staticmethod
    @callback(
        Output("measurement", "value"),
        Input("prev-mmnt-button", "n_clicks"),
        Input("next-mmnt-button", "n_clicks"),
        Input("measurement", "value"),
        State("measurement", "options"),
    )
    def update_selected_measurement(
        _prev_clicks: int, _next_clicks: int, curr_mmnt: str, mmnt_options: list
    ) -> int:
        """
        Updates selected measurement based on button clicks or dropdown selection.

        Args:
            _prev_clicks (int): Number of clicks on the previous button
            _next_clicks (int): Number of clicks on the next button
            curr_mmnt (str): Current selected measurement
            mmnt_options (list): List of measurement options

        Returns:
            str: New selected measurement

        Raises:
            PreventUpdate: If the options are not available

        """
        input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        logger.debug(f"update_selected_measurement | Input ID: {input_id}")
        logger.debug(
            f"update_selected_measurement | {dash.callback_context.triggered[0]=}"  # '.'
        )

        # BUG: Upstream bug. See https://github.com/plotly/dash/issues/1523
        if not input_id:
            logger.debug("update_selected_measurement | No button clicked")

            old_mmnt = _state.measurement
            # NOTE: Assuming this is None only on reload
            logger.debug(
                f"update_selected_measurement | No button clicked | Options not available: Returning old measurement: {old_mmnt}"
            )

            if old_mmnt:
                return old_mmnt
            else:
                raise PreventUpdate

        if not mmnt_options:
            old_mmnt = _state.measurement
            # NOTE: Assuming this is None only on reload
            logger.debug(
                f"Options not available: Returning old measurement: {old_mmnt}"
            )
            return old_mmnt

        # Identify which button was pressed
        triggered_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

        # If no measurement is selected, do not update
        if not curr_mmnt:
            logger.debug(
                "update_selected_measurement | No current measurement selected"
            )
            raise PreventUpdate

        curr_idx = mmnt_options.index(curr_mmnt)
        if triggered_id == "prev-mmnt-button":
            new_index = (curr_idx - 1) % len(mmnt_options)  # Cycle left
        elif triggered_id == "next-mmnt-button":
            new_index = (curr_idx + 1) % len(mmnt_options)  # Cycle right
        else:
            new_index = curr_idx  # No change

        logger.debug(f"New index: {new_index}")
        logger.debug(f"New option: {mmnt_options[new_index]}")

        return mmnt_options[new_index]

    def options(self):
        """
        Dropdowns in the selector.

        Returns:
            dash.html.Div: Div element containing the dropdowns for the selector

        """
        return html.Div(
            [
                html.Div("Sample Information:", className="column is-1"),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="wafer-id",
                            placeholder="Wafer ID",
                            searchable=True,
                            persistence=True,
                            persistence_type="local",
                        ),
                    ],
                    className="column is-2",
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="device-type",
                            placeholder="Device Type",
                            searchable=True,
                            persistence=True,
                            persistence_type="local",
                        ),
                    ],
                    className="column is-2",
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="device-id",
                            placeholder="Device ID",
                            searchable=True,
                            persistence=True,
                            persistence_type="local",
                        ),
                    ],
                    className="column is-2",
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="measurement-type",
                            placeholder="Measurement Type",
                            searchable=True,
                            persistence=True,
                            persistence_type="local",
                        ),
                    ],
                    className="column is-2",
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="measurement",
                            placeholder="Measurement",
                            searchable=True,
                            # NOTE: Persistence handled server-side
                        )
                    ],
                    className="column",
                ),
                html.Button(
                    html.I(className="fa-solid fa-arrow-left button"),
                    id="prev-mmnt-button",
                    n_clicks=0,
                ),
                html.Button(
                    html.I(className="fa-solid fa-arrow-right button"),
                    id="next-mmnt-button",
                    n_clicks=0,
                ),
            ],
            className="columns is-full is-multiline is-flex is-vcentered",
        )


class XarrayData(Data):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    @callback(
        Output(
            "load-signal",
            "data",
            allow_duplicate=True,
        ),
        State("load-signal", "data"),
        Input("dataset-path", "value"),
        Input("upload-ticker", "n_intervals"),
        prevent_initial_call=True,
    )
    def update_data(sig_curr: int, path: str, *_):
        """
        Update the data store with the Zarr file content.

        Args:
            sig_curr (int): The current signal value
            path (str): Path to the Zarr file

        Returns:
            dict: The updated data store

        Raises:
            PreventUpdate: If the path is not a file or not a Zarr file

        """
        if path in ["", None]:
            raise PreventUpdate

        path = Path(path)
        if _should_update_data(path, sig_curr, "XarrayData"):
            return sig_curr + 1 if sig_curr is not None else 1
        else:
            raise PreventUpdate
