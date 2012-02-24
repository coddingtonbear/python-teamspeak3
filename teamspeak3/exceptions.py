from socket import error

class TeamspeakConnectionError(error):
    pass

class TeamspeakConnectionLost(TeamspeakConnectionError):
    pass

class TeamspeakConnectionFailed(TeamspeakConnectionError):
    pass
