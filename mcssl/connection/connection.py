from abc import ABC, abstractmethod

class Connection(ABC):
    @abstractmethod
    def wrap_socket(self,client_socket):
        pass


