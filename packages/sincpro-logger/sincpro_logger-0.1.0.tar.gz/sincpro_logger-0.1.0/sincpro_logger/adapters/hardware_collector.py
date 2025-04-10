import os
import platform
import socket
import sys
import uuid
from typing import Dict, List, Optional

from sincpro_logger.domain.hardware_info import (
    HardwareCollector,
    HardwareInfo,
    NetworkInterface,
)


class BaseHardwareCollector(HardwareCollector):
    """Base implementation of the hardware collector focusing on system metadata."""

    def collect(self) -> HardwareInfo:
        """Collect basic system metadata."""
        return HardwareInfo(
            system_info=self._collect_system_info(),
            cpu_info={},  # No longer needed
            memory_info={},  # No longer needed
            disk_info={},  # No longer needed
            network_interfaces=self._collect_network_interfaces(),
            machine_id=self._get_machine_id(),
        )

    def _collect_system_info(self) -> Dict[str, str]:
        """Collect basic system information."""
        system_info = {
            "os": self._safe_get_os(),
            "os_version": self._safe_get_os_version(),
            "os_release": self._safe_get_os_release(),
            "hostname": self._safe_get_hostname(),
            "architecture": self._safe_get_architecture(),
            "python_version": self._safe_get_python_version(),
            "python_path": self._safe_get_python_path(),
            "working_directory": self._safe_get_working_directory(),
            "module_path": self._safe_get_module_path(),
            "user": self._safe_get_user(),
            "environment": self._safe_get_environment(),
            "containerized": self._safe_get_containerized(),
        }

        # Add Kubernetes information if running in a pod
        k8s_info = self._get_kubernetes_info()
        if k8s_info:
            system_info.update(k8s_info)

        return system_info

    def _safe_get_os(self) -> str:
        """Safely get OS name."""
        try:
            return platform.system() or "unknown"
        except Exception:
            return "unknown"

    def _safe_get_os_version(self) -> str:
        """Safely get OS version."""
        try:
            return platform.version() or "unknown"
        except Exception:
            return "unknown"

    def _safe_get_os_release(self) -> str:
        """Safely get OS release."""
        try:
            return platform.release() or "unknown"
        except Exception:
            return "unknown"

    def _safe_get_hostname(self) -> str:
        """Safely get hostname."""
        try:
            return socket.gethostname() or "unknown"
        except Exception:
            return "unknown"

    def _safe_get_architecture(self) -> str:
        """Safely get architecture."""
        try:
            return platform.machine() or "unknown"
        except Exception:
            return "unknown"

    def _safe_get_python_version(self) -> str:
        """Safely get Python version."""
        try:
            return sys.version or "unknown"
        except Exception:
            return "unknown"

    def _safe_get_python_path(self) -> str:
        """Safely get Python path."""
        try:
            return sys.executable or "unknown"
        except Exception:
            return "unknown"

    def _safe_get_working_directory(self) -> str:
        """Safely get working directory."""
        try:
            return os.getcwd() or "unknown"
        except Exception:
            return "unknown"

    def _safe_get_module_path(self) -> str:
        """Safely get module path."""
        try:
            return os.path.dirname(os.path.abspath(__file__)) or "unknown"
        except Exception:
            return "unknown"

    def _safe_get_user(self) -> str:
        """Safely get user."""
        try:
            return os.getenv("USER", os.getenv("USERNAME", "unknown")) or "unknown"
        except Exception:
            return "unknown"

    def _safe_get_environment(self) -> str:
        """Safely get environment."""
        try:
            return os.getenv("ENVIRONMENT", "unknown") or "unknown"
        except Exception:
            return "unknown"

    def _safe_get_containerized(self) -> str:
        """Safely get containerized status."""
        try:
            return str(os.path.exists("/.dockerenv"))
        except Exception:
            return "false"

    def _get_kubernetes_info(self) -> Dict[str, str]:
        """Get Kubernetes pod information if running in a pod."""
        k8s_info = {}
        
        try:
            # Check if running in Kubernetes
            if os.path.exists("/var/run/secrets/kubernetes.io"):
                k8s_info["kubernetes"] = "true"
                
                # Get pod name from environment variable
                pod_name = os.getenv("POD_NAME", os.getenv("HOSTNAME", ""))
                if pod_name:
                    k8s_info["pod_name"] = pod_name
                
                # Get namespace from environment variable or file
                namespace = os.getenv("POD_NAMESPACE", "")
                if not namespace and os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/namespace"):
                    try:
                        with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
                            namespace = f.read().strip()
                    except Exception:
                        pass
                if namespace:
                    k8s_info["namespace"] = namespace
                
                # Get node name
                node_name = os.getenv("NODE_NAME", "")
                if node_name:
                    k8s_info["node_name"] = node_name
                
                # Get service account
                if os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/token"):
                    k8s_info["service_account"] = "true"
                
                # Get pod IP
                pod_ip = os.getenv("POD_IP", "")
                if pod_ip:
                    k8s_info["pod_ip"] = pod_ip
        except Exception:
            pass

        return k8s_info

    def _collect_network_interfaces(self) -> List[NetworkInterface]:
        """Collect basic network interface information."""
        interfaces = []
        try:
            hostname = self._safe_get_hostname()
            ip_address = "unknown"
            
            try:
                ip_address = socket.gethostbyname(hostname)
            except Exception:
                pass
            
            # Try to get pod IP in Kubernetes
            pod_ip = os.getenv("POD_IP", "")
            if pod_ip:
                ip_address = pod_ip
            
            interfaces.append(
                NetworkInterface(
                    name="default",
                    ip_address=ip_address,
                    mac_address="00:00:00:00:00:00",
                    is_active=True,
                )
            )
        except Exception:
            # Add a default interface even if everything fails
            interfaces.append(
                NetworkInterface(
                    name="default",
                    ip_address="unknown",
                    mac_address="00:00:00:00:00:00",
                    is_active=True,
                )
            )

        return interfaces

    def _get_machine_id(self) -> str:
        """Get a unique machine identifier."""
        # Try different methods to get a unique ID
        methods = [
            self._get_machine_id_from_kubernetes,
            self._get_machine_id_from_systemd,
            self._get_machine_id_from_docker,
        ]
        
        for method in methods:
            try:
                machine_id = method()
                if machine_id:
                    return machine_id
            except Exception:
                continue
        
        # If all methods fail, generate a UUID
        return str(uuid.uuid4())

    def _get_machine_id_from_kubernetes(self) -> Optional[str]:
        """Get machine ID from Kubernetes pod."""
        try:
            # In Kubernetes, we can use the pod name as a unique identifier
            pod_name = os.getenv("POD_NAME", os.getenv("HOSTNAME", ""))
            if pod_name:
                return f"k8s-{pod_name}"
        except Exception:
            pass
        return None

    def _get_machine_id_from_systemd(self) -> Optional[str]:
        """Get machine ID from systemd (Linux)."""
        try:
            with open("/etc/machine-id", "r") as f:
                return f.read().strip()
        except Exception:
            return None

    def _get_machine_id_from_docker(self) -> Optional[str]:
        """Get machine ID from Docker environment."""
        try:
            # Check if we're running in Docker
            if os.path.exists("/.dockerenv"):
                # Try to get container ID from cgroup
                with open("/proc/1/cgroup", "r") as f:
                    for line in f:
                        if "docker" in line or "kubepods" in line:
                            # Extract container ID
                            parts = line.strip().split("/")
                            if len(parts) > 2:
                                return parts[-1]
        except Exception:
            pass
        return None


def get_hardware_collector() -> HardwareCollector:
    """Factory function to get the hardware collector."""
    return BaseHardwareCollector() 