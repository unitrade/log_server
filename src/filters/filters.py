class FilterBase:
    def __init__(self):
        self.level = "DEFAULT"

    def evaluate(self, record: dict) -> bool:
        if self.level in str(record.values()):
            return True
        return False


class FilterRange(FilterBase):
    def __init__(self, start_date=None, end_date=None):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        # {"filter_type": "FilterRange", "startDate": "2021-04-27", "endDate": "2021-04-28"}

    def evaluate(self, record: dict) -> bool:
        if self.start_date in str(record.values()):
            return True
        return False


class FilterInfo(FilterBase):
    def __init__(self):
        super().__init__()
        self.level = "INFO"


class FilterDebug(FilterBase):
    def __init__(self):
        super().__init__()
        self.level = "DEBUG"


class FilterWarning(FilterBase):
    def __init__(self):
        super().__init__()
        self.level = "WARNING"


class FilterError(FilterBase):
    def __init__(self):
        super().__init__()
        self.level = "ERROR"


class FilterDecorator(FilterBase):
    def __init__(self, list_filters: list):
        super().__init__()
        self.list_filters = list_filters

    def evaluate(self, record: dict) -> bool:
        for item in self.list_filters:
            if item.level not in str(record.values()):
                return False
        return True
