class ServerMessageError(Exception):
    """服务器消息库的基类异常"""
    pass

class ServerConnectionError(ServerMessageError):
    """服务器连接异常"""
    pass

class MessageSendError(ServerMessageError):
    """消息发送异常"""
    pass