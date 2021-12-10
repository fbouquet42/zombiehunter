from abc import ABCMeta, abstractmethod

class   AutomaticDefault(metaclass=ABCMeta):

    @abstractmethod
    def _loading(self):
        pass

    @abstractmethod
    def update(self, monster):
        pass
