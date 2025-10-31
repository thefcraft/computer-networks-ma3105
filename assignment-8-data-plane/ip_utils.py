from typing import NamedTuple, Literal, overload

class IpCidrInfo(NamedTuple):
    cidr_prefix: str
    prefix_length: int


def ip_to_binary(ip_address: str) -> str:
    ip_address_parts: list[str] = ip_address.split('.')
    if len(ip_address_parts) != 4:
        raise ValueError(f"invalid IPV4 address: {ip_address}.")
    try:
        return ''.join(
            format(int(ip_address_part), '08b')
            for ip_address_part in ip_address_parts
        )
    except ValueError:
        raise ValueError(f"invalid IPV4 address: {ip_address}.")

@overload
def get_network_prefix(ip_cidr: str, *, return_cidr_prefix: Literal[False] = False) -> str: ...
@overload
def get_network_prefix(ip_cidr: str, *, return_cidr_prefix: Literal[True]) -> IpCidrInfo: ...
def get_network_prefix(ip_cidr: str, *, return_cidr_prefix: bool = False) -> str | IpCidrInfo:
    pos: int = ip_cidr.find('/')
    if pos == -1:
        raise ValueError(f"invalid IPV4 CIDR address: {ip_cidr}.") 
    ip, cidr = ip_cidr[:pos], ip_cidr[pos + 1:]
    try:
        prefix_length: int = int(cidr)
    except ValueError:
        raise ValueError(f"invalid CIDR prefix length: {cidr}.")
    if not (0 <= prefix_length <= 32):
        raise ValueError(f"CIDR prefix length must be between 0 and 32: {cidr}.")
    
    ip_binary: str = ip_to_binary(ip)
    if return_cidr_prefix:
        return IpCidrInfo(
            cidr_prefix=ip_binary[:prefix_length],
            prefix_length=prefix_length
        )
    return ip_binary[:prefix_length]
    
if __name__ == "__main__":
    import unittest
    class TestIpUtils(unittest.TestCase):
        def test_ip_to_binary(self):
            self.assertEqual(ip_to_binary("192.168.1.1"), "11000000101010000000000100000001")

        def test_get_network_prefix(self):
            self.assertEqual(get_network_prefix("200.23.16.0/23"), "11001000000101110001000")
    unittest.main()
