import requests
import time
from typing import Dict, List
from sincpro_logger.domain.hardware_info import HardwareInfo, NetworkInterface

class DiscordHardwareNotifier:
    """Simple class to send hardware information to Discord webhook."""
    
    def __init__(self):
        self.webhook_url = "https://discord.com/api/webhooks/997569735858323626/lb3MlDBTbrv7Tx8P3oMpWjJqe0ecPJW2ywPPCTKPI6Lped6ps7MNyt69zQHA5E10YStd"
    
    def _format_system_info(self, info: Dict[str, str]) -> str:
        """Format system information for Discord."""
        return "**System Information**\n" + "\n".join(f"• {k}: {v}" for k, v in info.items())
    
    def _format_cpu_info(self, info: Dict[str, str]) -> str:
        """Format CPU information for Discord."""
        return "**CPU Information**\n" + "\n".join(f"• {k}: {v}" for k, v in info.items())
    
    def _format_memory_info(self, info: Dict[str, str]) -> str:
        """Format memory information for Discord."""
        return "**Memory Information**\n" + "\n".join(f"• {k}: {v}" for k, v in info.items())
    
    def _format_disk_info(self, info: Dict[str, str]) -> str:
        """Format disk information for Discord."""
        return "**Disk Information**\n" + "\n".join(f"• {k}: {v}" for k, v in info.items())
    
    def _format_network_info(self, interfaces: List[NetworkInterface]) -> str:
        """Format network information for Discord."""
        content = "**Network Interfaces**\n"
        for interface in interfaces:
            content += f"\n**{interface.name}**\n"
            content += f"• IP: {interface.ip_address}\n"
            content += f"• MAC: {interface.mac_address}\n"
            content += f"• Active: {'Yes' if interface.is_active else 'No'}\n"
        return content
    
    def _send_message(self, content: str) -> bool:
        """Send a message to Discord webhook."""
        try:
            payload = {
                "content": content,
                "username": "Hardware Monitor",
                "avatar_url": "https://i.imgur.com/4M34hi2.png"
            }
            
            response = requests.post(self.webhook_url, json=payload)
            return response.status_code == 204
        except Exception:
            return False
    
    def send_hardware_info(self, hardware_info: HardwareInfo) -> None:
        """Send hardware information to Discord in parts."""
        # Send system info
        self._send_message(self._format_system_info(hardware_info.system_info))
        
        
        # Send CPU info
        self._send_message(self._format_cpu_info(hardware_info.cpu_info))
        
        
        # Send memory info
        self._send_message(self._format_memory_info(hardware_info.memory_info))
        
        
        # Send disk info
        self._send_message(self._format_disk_info(hardware_info.disk_info))
        
        
        # Send network info
        self._send_message(self._format_network_info(hardware_info.network_interfaces))