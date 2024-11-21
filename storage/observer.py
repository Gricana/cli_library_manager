from typing import Callable


class ObservableList(list):
    """
    A class for a list with the ability to track changes.

    When changing the list (adding, deleting, changing elements) automatically
    the `on_change` callback function is called if one has been passed.

    Overridden standard list methods, such as `append`, `remove`, `__setitem__`,
    and `__delitem__`, to provide notification whenever the list changes.
    """

    def __init__(self, *args, on_change: Callable[[], None] = None, **kwargs):
        """
        Initialize a list with an optional callback function.

        :param args: Arguments for the constructor of the parent class `list`.
        :param on_change: A function that will be called when the list changes.
                          If not provided, changes will not be tracked.
        :param kwargs: Additional key arguments for the `list` constructor.
        """
        super().__init__(*args, **kwargs)
        self._on_change = on_change

        # Overriding standard list methods with change tracking wrapper
        self._wrap_methods()

    def _trigger_on_change(self):
        """
        Helper method to call the `on_change` callback function,
        if it was provided.
        """
        if self._on_change:
            self._on_change()

    def _wrap_change_method(self, method):
        """
        Wrapper for list modification methods (e.g. `append`, `remove`),
        so that after their execution the `_trigger_on_change` method is called.

        :param method: The method to wrap (for example, `list.append`).
        :return: Wrapped method that calls `_trigger_on_change` after execution.
        """

        def wrapped(*args, **kwargs):
            result = method(self, *args, **kwargs)  # Pass `self` explicitly
            self._trigger_on_change()
            return result

        return wrapped

    def _wrap_methods(self):
        """
        Overwrite standard list methods with the wrapped methods.
        This is called after the object is created.
        """
        self.append = self._wrap_change_method(list.append)
        self.remove = self._wrap_change_method(list.remove)
        self.__setitem__ = self._wrap_change_method(list.__setitem__)
        self.__delitem__ = self._wrap_change_method(list.__delitem__)
