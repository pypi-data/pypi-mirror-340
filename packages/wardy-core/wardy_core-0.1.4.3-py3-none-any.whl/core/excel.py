"""Excel functionality."""
from __future__ import annotations

import logging
from dataclasses import astuple, fields, is_dataclass
from pathlib import Path
from typing import Sequence

import xlsxwriter
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

logger = logging.getLogger()


def new_workbook(filename: str | Path) -> Workbook:
    """Create a new Excel Workbook.

    Args:
        filename (str | Path): Fully-qualified filename to use

    Returns:
        Workbook: object controlling workbook
    """
    logger.debug("Creating workbook at %s", filename)
    return xlsxwriter.Workbook(filename)


def new_worksheet(
    sheetname: str = None,
    *,
    filename: str | Path | None = None,
    workbook: Workbook = None,
) -> tuple[Workbook, Worksheet]:
    """Create a new Excel worksheet.

    Args:
        sheetname (str, optional): Specify sheet name. Defaults to None.
        filename (str | Path, optional): Create whole new workbook. Defaults to None.
        workbook (Workbook, optional): Existing workbook to add sheet to.

    Raises:
        TypeError: Missing filename and workbook

    Returns:
        Tuple[Workbook, Worksheet]: workbook created or passed in, new worksheet
    """
    if workbook is None:
        if filename is None:
            raise TypeError("Must supply workbook or filename")
        workbook = new_workbook(filename)

    logger.debug("Creating worksheet %s in %s, file %s", sheetname, workbook, filename)
    return workbook, workbook.add_worksheet(sheetname)


def new_table(
    excel_data: Sequence,
    *,
    headings: list[str] = None,
    filename: str | Path | None = None,
    workbook: Workbook = None,
    sheetname: str = None,
    worksheet: Worksheet = None,
) -> None:
    """Create an Excel workbook with a table, based on supplied data.

    Args:
        excel_data (Sequence): rows of dataclass (columns)
        headings (List[str]): heading names to use. Default is to inspect data
        filename (str | Path, optional): Create whole new workbook. Defaults to None.
        workbook (Workbook, optional): Already existing workbook to use
        sheetname (str, optional): Name for new sheet to contain table.
            Defaults to Excel-generated
        worksheet (Worksheet, optional): Already existing worksheet to use.

    Raises:
        ValueError: data supplied is incorrect or empty
        TypeError: Missing filename, workbook and worksheet
    """
    if not excel_data:
        raise ValueError("No data supplied")
    if not is_dataclass(excel_data[0]):
        raise TypeError("excel_data must contain dataclasses")

    if worksheet is None:
        workbook, worksheet = new_worksheet(
            sheetname, filename=filename, workbook=workbook
        )

    if not headings:
        headings = [field.name for field in fields(excel_data[0])]

    excel_columns = tuple({"header": header} for header in headings)
    excel_table = tuple(astuple(row) for row in excel_data)

    worksheet.add_table(
        0,
        0,
        len(excel_table),
        len(headings) - 1,
        {"data": excel_table, "columns": excel_columns},
    )

    if filename and workbook:
        workbook.close()
