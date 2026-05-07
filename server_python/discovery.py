import socket
import platform
from zeroconf import IPVersion, ServiceInfo, Zeroconf

class DiscoveryService: 
    def __init__(self, port: int):
        self.zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
        self.port = port
        self.type = "_filebridge._tcp.local."
        self.name = f"FileBridge-{socket.gethostname()}.{self.type}"

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip

    def register(self):
        info = ServiceInfo(
            self.type,
            self.name,
            addresses=[socket.inet_aton(self.get_ip())],
            port=self.port,
            properties={
                'ver': '1.0',
                'os': platform.system(),
                'host': self.hostname
            },
            server=f"{self.hostname}.local.",
        )
        self.zeroconf.register_service(info)
        print("Advertising: {self.name} on {self.get_ip()}")
    
    def unregister(self):
        self.zeroconf.unregister_all_services()
        self.zeroconf.close()

