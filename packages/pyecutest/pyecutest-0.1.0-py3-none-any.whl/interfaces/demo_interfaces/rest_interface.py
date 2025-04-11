from typing import Dict, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Resource:
    id: str
    data: Dict[str, Any]

class RestInterface(ABC):
    """A simple REST-like interface demo"""
    
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Resource:
        """Create a new resource"""
        pass
    
    @abstractmethod
    def read(self, resource_id: str) -> Optional[Resource]:
        """Read a resource by ID"""
        pass
    
    @abstractmethod
    def update(self, resource_id: str, data: Dict[str, Any]) -> Optional[Resource]:
        """Update a resource"""
        pass
    
    @abstractmethod
    def delete(self, resource_id: str) -> bool:
        """Delete a resource"""
        pass

class DemoRestInterface(RestInterface):
    """A concrete implementation of the REST interface for demo purposes"""
    
    def __init__(self):
        self._resources: Dict[str, Resource] = {}
    
    def create(self, data: Dict[str, Any]) -> Resource:
        import uuid
        resource_id = str(uuid.uuid4())
        resource = Resource(id=resource_id, data=data)
        self._resources[resource_id] = resource
        return resource
    
    def read(self, resource_id: str) -> Optional[Resource]:
        return self._resources.get(resource_id)
    
    def update(self, resource_id: str, data: Dict[str, Any]) -> Optional[Resource]:
        if resource_id not in self._resources:
            return None
        resource = Resource(id=resource_id, data=data)
        self._resources[resource_id] = resource
        return resource
    
    def delete(self, resource_id: str) -> bool:
        if resource_id in self._resources:
            del self._resources[resource_id]
            return True
        return False 