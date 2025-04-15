import sys

import ibis
import pyarrow as pa
import pyarrow.parquet as pq

from composable_dataloader.format import Format
from composable_dataloader.logger import logger


def read_table(
    uri: str,
    account_name: str,
    format: Format = Format.PARQUET,
):
    """
    Read data from cloud storage in Parquet or Delta format.

    Supports both Parquet and Delta formats, authenticating with Azure credentials.

    Args:
        uri: Storage location URI
        account_name: Azure storage account name
        format: Data format (PARQUET or DELTA)

    Returns:
        Ibis table representing the data

    Raises:
        ValueError: If an unsupported format is specified
    """
    con = ibis.duckdb.connect()
    con.raw_sql(
        f"""
            CREATE SECRET azure_secrets (
            TYPE azure,
            PROVIDER credential_chain,
            CHAIN 'managed_identity;cli',
            ACCOUNT_NAME '{account_name}'
        );
        """
    )

    if format == Format.DELTA:
        return con.read_delta(uri)
    elif format == Format.PARQUET:
        return con.read_parquet(f"{uri}/*.parquet")
    else:
        raise ValueError(f"Unsupported format: {format}. Supported formats are 'delta' and 'parquet'.")


def write_dataframe_to_stdout(df: ibis.Table) -> None:
    """Write Ibis table to stdout as Parquet binary."""

    # Convert to PyArrow and write as Parquet
    buf = pa.BufferOutputStream()
    pq.write_table(df.to_pyarrow(), buf, compression="snappy")

    # Stream binary data to stdout
    buf_bytes = buf.getvalue().to_pybytes()
    logger.info(f"Streaming {len(buf_bytes)} bytes to stdout")
    sys.stdout.buffer.write(buf_bytes)
