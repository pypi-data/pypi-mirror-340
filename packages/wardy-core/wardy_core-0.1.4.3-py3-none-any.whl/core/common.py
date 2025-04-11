"""Generally helpful functions with multiple use cases."""

from typing import List, Set, Union


def comma_separated_to_set(in_data: Union[str, List[str]]) -> Set[str]:
    """Take a list or comma-separated string and separate.

    This is useful for argparse with nargs option. Users may supply a
    comma-separated string instead of space delimted.

    Args:
        in_data (Union[str, List[str]]): list items or comma-separated

    Raises:
        TypeError: didn't pass a string or list

    Returns:
        Set[str]: individual items
    """
    split_up_items = set()

    if isinstance(in_data, str):
        in_list = [in_data]
    elif isinstance(in_data, list):
        in_list = in_data
    else:
        raise TypeError(f"data '{in_data}' needs to be a string or list")

    for list_item in in_list:
        if "," in list_item:
            split_up_items.update(list_item.split(","))
        else:
            split_up_items.add(list_item)

    return split_up_items
