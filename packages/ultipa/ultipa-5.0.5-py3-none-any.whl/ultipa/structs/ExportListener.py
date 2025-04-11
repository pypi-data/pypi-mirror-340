from abc import abstractmethod

from ultipa import BaseModel


class ExportListener():
    @abstractmethod
    def onReady(self):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def onError(self):
        pass

    @abstractmethod
    def onComplete(self):
        pass
