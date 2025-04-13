import socket
import json
from .exceptions import ServerConnectionError, MessageSendError

class MessageClient:
    """
    服务器消息发布客户端
    
    示例用法:
    >>> client = MessageClient(host='example.com', port=8080)
    >>> client.connect()
    >>> client.send_message({'type': 'alert', 'content': '系统警告'})
    >>> client.disconnect()
    """
    
    def __init__(self, host='localhost', port=8080, timeout=10):
        """
        初始化客户端
        
        :param host: 服务器地址
        :param port: 服务器端口
        :param timeout: 连接超时时间(秒)
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self._socket = None
        self._connected = False
    
    def connect(self):
        """连接到服务器"""
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(self.timeout)
            self._socket.connect((self.host, self.port))
            self._connected = True
        except (socket.timeout, ConnectionRefusedError) as e:
            raise ServerConnectionError(f"无法连接到服务器 {self.host}:{self.port}") from e
    
    def send_message(self, message):
        """
        发送消息到服务器
        
        :param message: 要发送的消息(dict格式)
        :raises MessageSendError: 当消息发送失败时抛出
        """
        if not self._connected:
            raise MessageSendError("未连接到服务器")
        
        try:
            # 将消息转换为JSON格式并发送
            message_str = json.dumps(message) + '\n'
            self._socket.sendall(message_str.encode('utf-8'))
        except (socket.error, TypeError, ValueError) as e:
            raise MessageSendError("消息发送失败") from e
    
    def disconnect(self):
        """断开与服务器的连接"""
        if self._socket:
            try:
                self._socket.close()
            finally:
                self._socket = None
        self._connected = False
    
    def __enter__(self):
        """支持上下文管理协议"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持上下文管理协议"""
        self.disconnect()
    
    @property
    def is_connected(self):
        """返回当前连接状态"""
        return self._connected