"""
This module provides the OECDAPI_Databuilder class, which is responsible for
constructing queries to the OECD API, fetching data in chunks to avoid rate limits,
and merging the data into CSV files and a consolidated pandas DataFrame.
"""

import logging
import time
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from tqdm import tqdm

from .utils import create_retry_session  # Retry session helper

# Set up logging configuration.
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DATA_DIR = Path.cwd() / "datasets" / "OECD"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class OECDAPI_Databuilder:
    def __init__(
        self,
        config: Dict[str, Dict[str, str]],
        start: str,
        end: str,
        freq: str = "Q",
        response_format: str = "csv",
        dbpath: str = str(DATA_DIR),
        base_url: Optional[str] = None,
        request_interval: float = 5.0,
    ) -> None:
        """
        Initialize the OECDAPI_Databuilder instance.

        :param config: Dictionary of indicator configurations.
        :param start: Start time period (e.g., "2019-Q1").
        :param end: End time period (e.g., "2020-Q3").
        :param freq: Data frequency: "Q" for quarterly, "M" for monthly, "Y" for yearly.
        :param response_format: Expected response format: "csv", "json", or "xml".
        :param dbpath: Path where CSV files will be stored.
        :param base_url: Base URL for the OECD API.
        :param request_interval: Delay (in seconds) between API requests.
        """
        self.config = config
        self.start = start
        self.end = end
        self.freq = freq.upper()
        self.response_format = response_format.lower()
        self.base_url = base_url
        self.indicators = list(self.config.keys())
        self.dbpath = Path(dbpath)
        self.request_interval = request_interval

        # Ensure the storage directory exists.
        self.dbpath.mkdir(parents=True, exist_ok=True)

        # Validate required parameters.
        if not self.start or not self.end:
            raise ValueError("Both start and end periods must be provided.")

        # Collect the union of all REF_AREA values from the configuration.
        countries_set = set()
        for conf in self.config.values():
            ref_area = conf.get("REF_AREA", "")
            if ref_area:
                countries_set.update(ref_area.split("+"))
        self.countries = sorted(list(countries_set))
        logger.info(f"Combined countries from configuration: {self.countries}")

        # Use a session with retries to reuse connections.
        self.session = create_retry_session()

    def _build_time_chunks(
        self, period_range: pd.PeriodIndex, chunk_size: int
    ) -> List[Tuple[str, str]]:
        """
        Build a list of time chunk tuples (start, end) for the given period_range.

        :param period_range: Pandas PeriodIndex generated from start to end.
        :param chunk_size: Number of periods in each time chunk.
        :return: List of (chunk_start, chunk_end) tuples.
        """
        time_chunks = []
        for i in range(0, len(period_range), chunk_size):
            chunk = period_range[i : i + chunk_size]
            if self.freq == "Q":
                chunk_start = f"{chunk[0].year}-Q{chunk[0].quarter}"
                chunk_end = f"{chunk[-1].year}-Q{chunk[-1].quarter}"
            elif self.freq == "Y":
                chunk_start = str(chunk[0])
                chunk_end = str(chunk[-1])
            elif self.freq == "M":
                chunk_start = chunk[0].strftime("%Y-%m")
                chunk_end = chunk[-1].strftime("%Y-%m")
            else:
                raise ValueError(f"Unsupported frequency: {self.freq}")
            time_chunks.append((chunk_start, chunk_end))
        return time_chunks

    def _get_headers(self) -> Dict[str, str]:
        """
        Construct and return the HTTP headers for the API request based on response_format.
        """
        headers = {}
        if self.response_format == "csv":
            headers["Accept"] = "application/vnd.sdmx.data+csv; charset=utf-8"
        elif self.response_format == "json":
            headers["Accept"] = "application/vnd.sdmx.data+json; charset=utf-8; version=2"
        elif self.response_format == "xml":
            headers["Accept"] = "application/vnd.sdmx.genericdata+xml; charset=utf-8; version=2.1"
        else:
            raise ValueError("response_format must be one of: csv, json, xml")
        return headers

    def _parse_response(self, resp_text: str) -> pd.DataFrame:
        """
        Parse the API response text into a pandas DataFrame.

        :param resp_text: Raw API response text.
        :return: DataFrame parsed from response.
        """
        if self.response_format == "csv":
            return pd.read_csv(StringIO(resp_text))
        elif self.response_format == "json":
            return pd.read_json(StringIO(resp_text))
        elif self.response_format == "xml":
            # pd.read_xml uses lxml under the hood.
            return pd.read_xml(StringIO(resp_text))
        else:
            raise ValueError("Unsupported response_format")

    def fetch_data(self, chunk_size: Optional[int] = None) -> "OECDAPI_Databuilder":
        """
        Fetch data from the OECD API in chunks to avoid timeouts and rate-limit issues.
        Saves the concatenated results for each indicator as a CSV file.

        :param chunk_size: Number of periods to include in each API request.
                           If None, a default value of 100 will be used.
        :return: self
        """
        period_range = pd.period_range(start=self.start, end=self.end, freq=self.freq)

        if chunk_size is None:
            chunk_size = 100  # Default chunk size

        for indicator, conf in self.config.items():
            filter_order = list(conf.keys())
            all_chunks: List[pd.DataFrame] = []
            time_chunks = self._build_time_chunks(period_range, chunk_size)

            logger.info(f"For indicator '{indicator}', processing time chunks: {time_chunks}")

            filter_values = [conf.get(key, "") for key in filter_order]
            filter_url = ".".join(filter_values)
            if not self.base_url:
                raise ValueError("Base URL must be provided for the OECD API.")
            full_url = f"{self.base_url}{filter_url}"
            logger.info(f"Fetching data for '{indicator}' using URL: {full_url}")

            headers = self._get_headers()

            for chunk_start, chunk_end in tqdm(time_chunks, desc=f"Downloading {indicator} Data"):
                query_url = (
                    f"{full_url}?startPeriod={chunk_start}&endPeriod={chunk_end}"
                    "&dimensionAtObservation=TIME_PERIOD"
                )
                try:
                    resp = self.session.get(query_url, headers=headers)
                    resp.raise_for_status()
                    chunk_df = self._parse_response(resp.text)

                    expected_cols = {"REF_AREA", "TIME_PERIOD", "OBS_VALUE"}
                    if expected_cols.issubset(chunk_df.columns):
                        chunk_df = chunk_df[["REF_AREA", "TIME_PERIOD", "OBS_VALUE"]]
                    else:
                        logger.warning(
                            f"Unexpected columns in the response for {query_url}: {chunk_df.columns.tolist()}"
                        )

                    all_chunks.append(chunk_df)
                    logger.info(
                        f"Chunk {chunk_start} to {chunk_end}: {chunk_df.shape[0]} rows fetched."
                    )
                except Exception as error:
                    logger.error(
                        f"Error fetching chunk {chunk_start} to {chunk_end} for '{indicator}': {error}"
                    )
                time.sleep(self.request_interval)

            if all_chunks:
                indicator_df = pd.concat(all_chunks, ignore_index=True)
            else:
                indicator_df = pd.DataFrame(columns=["REF_AREA", "TIME_PERIOD", "OBS_VALUE"])

            csv_filename = self.dbpath / f"{indicator}.csv"
            indicator_df.to_csv(csv_filename, index=False)
            logger.info(f"Data for indicator '{indicator}' saved to {csv_filename}")
        return self

    def _convert_date(self, date_str: str) -> Any:
        """
        Convert a date string into a datetime object based on the frequency.
        Supported formats:
          - Quarterly: "YYYY-Qn"
          - Monthly: "YYYY-MM"
          - Yearly: "YYYY"
        :param date_str: Date string from the data.
        :return: Corresponding datetime object or the original string on failure.
        """
        try:
            if self.freq == "Q":
                return pd.Period(date_str, freq="Q").start_time
            elif self.freq == "M":
                return pd.Period(date_str, freq="M").start_time
            elif self.freq == "Y":
                return pd.Period(date_str, freq="A").start_time
            else:
                logger.warning(f"Unsupported frequency '{self.freq}' for date conversion.")
                return date_str
        except Exception as error:
            logger.error(f"Error converting date string '{date_str}': {error}")
            return date_str

    def create_dataframe(self) -> pd.DataFrame:
        """
        Merge CSV data for all indicators into a single DataFrame.
        For each indicator, the CSV file is expected to have the columns:
            'REF_AREA', 'TIME_PERIOD', 'OBS_VALUE'
        The merging process:
          - Renames 'TIME_PERIOD' to 'date' and 'REF_AREA' to 'country'
          - Merges on ['date', 'country'] using an outer join
          - Converts date strings using _convert_date
          - Ensures that indicator values are numeric
        :return: Merged pandas DataFrame.
        :raises: ValueError if no CSV files are found.
        """
        if not self.indicators:
            raise ValueError("No indicators found. Check your configuration.")

        merged_df: Optional[pd.DataFrame] = None
        for indicator in self.indicators:
            csv_file = self.dbpath / f"{indicator}.csv"
            try:
                df = pd.read_csv(csv_file)
            except Exception as error:
                logger.error(f"File not found or unable to read {csv_file}: {error}")
                continue

            df = df.rename(
                columns={
                    "TIME_PERIOD": "date",
                    "REF_AREA": "country",
                    "OBS_VALUE": indicator,
                }
            )
            if merged_df is None:
                merged_df = df
            else:
                merged_df = pd.merge(merged_df, df, on=["date", "country"], how="outer")

        if merged_df is None:
            raise ValueError("No data was loaded from any CSV file.")

        merged_df["date"] = merged_df["date"].apply(self._convert_date)
        merged_df["country"] = merged_df["country"].astype(str)
        for col in merged_df.columns:
            if col not in ["date", "country"]:
                merged_df[col] = pd.to_numeric(merged_df[col], errors="coerce")

        merged_df = merged_df.sort_values(by=["date", "country"]).reset_index(drop=True)
        return merged_df
