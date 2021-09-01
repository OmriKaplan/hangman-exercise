# Copyright (c) 2021 Lightricks. All rights reserved.
from abc import ABC, abstractmethod


# An abstract class - Server
class Server(ABC):

    @abstractmethod
    def initialize_server(self):
        pass

    @abstractmethod
    def send_to_server(self, token, message):
        pass

    @abstractmethod
    def get_from_server(self, req_type):
        pass


# Inheritances of Server
class HTTPServer(Server):

    def initialize_server(self):
        pass

    def send_to_server(self, token, message):
        pass

    def get_from_server(self, req_type):
        pass


class DummyServer(Server):

    def initialize_server(self):
        return "_________F__", "dfdfsg"

    def send_to_server(self, token, message):
        return "_________F__", "dfgdg", True

    def get_from_server(self, req_type):
        if req_type == 0:
            return 'h', 'dfsdf'
        elif req_type == 1:
            return ' dummy solution ', 'dfsdf'
        else:
            return 'illegal request', 'dfsdf'
