from abc import ABCMeta, abstractmethod


class Renderer:
    __metaclass__ = ABCMeta

    def set_engine(self, engine):
        self._engine = engine

    @abstractmethod
    def _render(self):
        ...

    @abstractmethod
    def clear_lines(self, range):
        ...
