import datetime
import inspect
import json
import os
import pathlib
import time
import warnings

_DELAY = 604800 # 1 week


def _get_tdx_path(endpoint: str | pathlib.Path) -> pathlib.Path:
    return pathlib.Path(os.path.join(os.path.expanduser("~"), ".TyraDex")) / endpoint


class TDXFile:
    @classmethod
    def create(cls, endpoint, data):
        path = _get_tdx_path(endpoint + '.tdx')
        if path.exists():
            os.remove(path)
        tdx = cls(path)
        tdx._data = data
        tdx._limit = int(time.time()) + _DELAY
        tdx.save()
        return tdx

    @classmethod
    def get(cls, endpoint):
        path = _get_tdx_path(endpoint)
        return cls(path)

    def __init__(self, path: str | pathlib.Path):
        self._path = pathlib.Path(str(path) + ('' if str(path).endswith('.tdx') else '.tdx'))
        if not self._path.parent.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)

        self._endpoint: str = str(self._path).removeprefix(str(_get_tdx_path('')))[1:].removesuffix('.tdx')
        self._limit: int = 0
        self._data = {}

        self.load()

    def __repr__(self):
        return (
            "<data:{data}, limit: {limit}, endpoint: {endpoint}>"
            .format(
                data=str(self._data).replace('\n', ' '),
                limit=self._limit,
                endpoint=self._endpoint
            )
        )

    def __str__(self):
        return json.dumps(self._data, ensure_ascii=False, indent=4)

    @property
    def exists(self):
        return self._path.exists()

    @property
    def is_valid(self):
        return self._limit > time.time()

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def limit(self):
        return datetime.datetime.fromtimestamp(int(self._limit))

    @property
    def data(self):
        if self._limit < time.time():
            stacks = [s.function for s in inspect.stack()]
            if 'create' not in stacks:
                sl = 2
                if stacks[1] == "save":
                    sl = 3
                    if stacks[2] == '__init__':
                        sl = 4
                warnings.warn('Data is out of date.', UserWarning, stacklevel=sl)
        return self._data

    def update(self, data):
        if isinstance(data, dict) or isinstance(data, list):
            self._data = data
            self._limit = int(time.time()) + _DELAY
            self.save()
        else:
            try:
                self.update(list(iter(data)))
            except TypeError:
                raise TypeError("Data must be iterable.")

    def load(self):
        if self._path.exists():
            with open(self._path, "r", encoding='utf-8') as f:
                data = ""
                for line in f.readlines():
                    if line.startswith("$") or line.isspace() or line == "\n":
                        pass
                    else:
                        data += line

                try:
                    self._endpoint = data.splitlines()[0]
                except TypeError:
                    raise TypeError("Critical error, the endpoint is bad.")

                try:
                    self._limit = int(data.splitlines()[1])
                    if self._limit < time.time():
                        if inspect.stack()[1].function != "__init__":
                            warnings.warn('The data is out of date.', UserWarning, stacklevel=2)
                except (ValueError, TypeError):
                    warnings.warn('Limit must be an int. The data will be considered outdated.', RuntimeWarning, stacklevel=2)
                    self._limit = 0

                try:
                    self._data = json.loads('\n'.join(data.splitlines()[2:]))
                except (json.decoder.JSONDecodeError, TypeError):
                    self._limit = 0
                    self._data = {}

    def save(self):
        with open(self._path, "w", encoding='utf-8') as f:
            f.write(
                "{endpoint}\n{limit}\n{data}"
                .format(
                    endpoint=self._endpoint,
                    limit=self._limit,
                    data=json.dumps(self.data, ensure_ascii=False, indent=4)
                )
            )