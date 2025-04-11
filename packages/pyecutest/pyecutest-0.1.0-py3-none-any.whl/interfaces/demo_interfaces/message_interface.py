from typing import Dict, Any, Callable, List
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum

class MessageType(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

@dataclass
class Message:
    type: MessageType
    content: str
    metadata: Dict[str, Any]

class MessageHandler(ABC):
    """A simple message-based interface demo"""
    
    @abstractmethod
    def publish(self, message: Message) -> None:
        """Publish a message to all subscribers"""
        pass
    
    @abstractmethod
    def subscribe(self, callback: Callable[[Message], None]) -> None:
        """Subscribe to receive messages"""
        pass
    
    @abstractmethod
    def unsubscribe(self, callback: Callable[[Message], None]) -> None:
        """Unsubscribe from receiving messages"""
        pass

class DemoMessageHandler(MessageHandler):
    """A concrete implementation of the message handler for demo purposes"""
    
    def __init__(self):
        self._subscribers: List[Callable[[Message], None]] = []
    
    def publish(self, message: Message) -> None:
        for subscriber in self._subscribers:
            subscriber(message)
    
    def subscribe(self, callback: Callable[[Message], None]) -> None:
        if callback not in self._subscribers:
            self._subscribers.append(callback)
    
    def unsubscribe(self, callback: Callable[[Message], None]) -> None:
        if callback in self._subscribers:
            self._subscribers.remove(callback) 