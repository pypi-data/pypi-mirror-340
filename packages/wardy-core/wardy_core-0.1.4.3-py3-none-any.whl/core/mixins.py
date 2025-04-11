"""Useful mixins."""


class SimpleRepr:
    """Mixin to make a standard-looking __repr__.

    Displays as  Class(a='1', b=2) and suppresses _ attributes
    """

    def __repr__(self) -> str:
        """Create a simple, standard repr.

        Returns:
            str: repr of form Class(a='1', b=2) and suppresses _ attributes
        """
        return (
            self.__class__.__name__
            + "("
            + ", ".join(
                [
                    f"{var_name}={repr(var_value)}"
                    for var_name, var_value in self.__dict__.items()
                    if not var_name.startswith("_")
                ]
            )
            + ")"
        )
