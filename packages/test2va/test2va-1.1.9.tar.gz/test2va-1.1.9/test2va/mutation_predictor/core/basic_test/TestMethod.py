class TestMethod:
    def __init__(self, method_name: str = "", has_before_method: bool = False, before_method_str: str = "", method_str: str = ""):
        self._method_name = method_name
        self._has_before_method = has_before_method
        self._before_method_str = before_method_str
        self._method_str = method_str

    # Getter and Setter for method_name
    def get_method_name(self) -> str:
        return self._method_name

    def set_method_name(self, method_name: str) -> None:
        self._method_name = method_name

    # Getter and Setter for has_before_method
    def get_has_before_method(self) -> bool:
        return self._has_before_method

    def set_has_before_method(self, has_before_method: bool) -> None:
        self._has_before_method = has_before_method

    # Getter and Setter for before_method_str
    def get_before_method_str(self) -> str:
        return self._before_method_str

    def set_before_method_str(self, before_method_str: str) -> None:
        self._before_method_str = before_method_str

    # Getter and Setter for method_str
    def get_method_str(self) -> str:
        return self._method_str

    def set_method_str(self, method_str: str) -> None:
        self._method_str = method_str