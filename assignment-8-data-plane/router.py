from typing import NamedTuple, Literal
from ip_utils import IpCidrInfo, get_network_prefix, ip_to_binary

class Route(NamedTuple):
    ip_cidr: str
    link_name: str

class Router:
    def __init__(self, routes: list[Route | tuple[str, str]]) -> None:
        self.routes: list[Route] = [
            Route(
                ip_cidr=route[0],
                link_name=route[1]
            ) if not isinstance(route, Route) else route
            for route in routes
        ]
        self.forwarding_table: list[tuple[IpCidrInfo, str]] = self.build_forwarding_table(self.routes)

    @staticmethod
    def build_forwarding_table(routes: list[Route]) -> list[tuple[IpCidrInfo, str]]:
        return sorted(
            (
                (
                    get_network_prefix(route.ip_cidr, return_cidr_prefix=True), 
                    route.link_name
                )
                for route in routes
            ),
            key=lambda x: x[0].prefix_length,
            reverse=True # Longest prefix first
        )
    
    def route_packet(self, dest_ip: str) -> str | Literal["Default Gateway"]:
        binary_dest_ip = ip_to_binary(dest_ip)
        for ip_cidr_info, link_name in self.forwarding_table:
            if binary_dest_ip[:ip_cidr_info.prefix_length] == ip_cidr_info.cidr_prefix:
                return link_name
        return "Default Gateway"
    
if __name__ == "__main__":
    import unittest
    class TestRouter(unittest.TestCase):
        def setUp(self):
            # Initialize the router with the specified routes
            self.router = Router([
                ("223.1.1.0/24", "Link 0"),
                ("223.1.2.0/24", "Link 1"),
                ("223.1.3.0/24", "Link 2"),
                ("223.1.0.0/16", "Link 4 (ISP)")
            ])
        def test_route_packet_exact_match(self):
            self.assertEqual(self.router.route_packet("223.1.1.100"), "Link 0")
            self.assertEqual(self.router.route_packet("223.1.2.5"), "Link 1")
            self.assertEqual(self.router.route_packet("223.1.250.1"), "Link 4 (ISP)")
        def test_route_packet_with_no_matching_prefix(self):
            self.assertEqual(self.router.route_packet("198.51.100.1"), "Default Gateway")
    unittest.main()