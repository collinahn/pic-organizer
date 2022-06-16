from dataclasses import dataclass
from dataclasses import field

from utils.metaclasses import MetaSingleton

@dataclass
class BaseFolder:
    path: str = field(default_factory='')


@dataclass
class GlobalBaseFolder(BaseFolder, metaclass=MetaSingleton):
    ...

if __name__ == '__main__':

    base = BaseFolder('.')
    print(base.path)

    base = BaseFolder('..1')

    print(base.path)

    base = GlobalBaseFolder(base.path)
    base = GlobalBaseFolder('123')
    print(base)

