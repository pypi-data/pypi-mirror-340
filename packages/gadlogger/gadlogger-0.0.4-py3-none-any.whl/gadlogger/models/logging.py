import dataclasses
import hashlib
import json
import sys
import types
import typing


@dataclasses.dataclass
class Logger:
    name: str
    level: int
    module: typing.Optional[types.ModuleType] = None
    stream: typing.Optional[typing.TextIO] = sys.stdout
    kwargs: typing.Dict = dataclasses.field(default_factory=dict)

    @property
    def id(self) -> str:
        return hashlib.md5(
            json.dumps(
                {
                    "name": self.name,
                    "level": self.level,
                    "stream": str(self.stream),
                    "module": str(self.module),
                    "kwargs": {k: v.__name__ if callable(v) else v for k, v in (self.kwargs or {}).items()},
                },
                sort_keys=True,
                ensure_ascii=False,
            ).encode("utf-8")
        ).hexdigest()
