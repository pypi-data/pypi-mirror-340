from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class NetworkInterface:
    """Represents a network interface information."""
    name: str
    ip_address: str
    mac_address: str
    is_active: bool


@dataclass
class HardwareInfo:
    """Represents the collected hardware information."""
    system_info: Dict[str, str]  # OS, hostname, etc.
    cpu_info: Dict[str, str]  # CPU model, cores, etc.
    memory_info: Dict[str, str]  # Total memory, available, etc.
    disk_info: Dict[str, str]  # Disk size, free space, etc.
    network_interfaces: List[NetworkInterface]
    machine_id: Optional[str]  # Unique machine identifier


class HardwareCollector:
    """Interface for hardware information collection."""
    
    def collect(self) -> HardwareInfo:
        """Collect hardware information from the system.
        
        Returns:
            HardwareInfo: The collected hardware information.
            
        Raises:
            HardwareCollectionError: If there's an error collecting the information.
        """
        raise NotImplementedError() 