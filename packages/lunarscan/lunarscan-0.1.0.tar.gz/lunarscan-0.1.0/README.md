# LunarScan - Networking Tools Made Simple

**LunarScan** is a Python module designed to simplify network scanning and IP geolocation tasks. With a few lines of code, you can scan for open ports, resolve IP addresses, and retrieve geolocation information about a target.

## Installation

To use **LunarScan**, simply import the module in your Python project:

```python
import lunarscan
```

Alternatively, import specific functions:

```python
from lunarscan import scan, geoscan, get_ip
```

## Functions

### `scan(target, start_port, end_port)`

Scans a target IP or hostname for open ports within a specified range.

**Arguments**:
- `target` (str): The IP address or hostname of the target.
- `start_port` (int): The starting port number.
- `end_port` (int): The ending port number.

**Returns**:
- `list[int]`: A list of open ports.

**Example**:
```python
open_ports = lunarscan.scan("192.168.1.1", 20, 100)
print(open_ports)
```

### `geoscan(target)`

Retrieves geolocation information for a given target IP. Prints details such as the continent, country, region, city, and geographical coordinates.

**Arguments**:
- `target` (str): The IP address or hostname to geolocate.

**Output**:
- Prints geolocation details to the console.

**Example**:
```python
lunarscan.geoscan("example.com")
```

### `get_ip(target)`

Resolves a target domain to its corresponding IP address.

**Arguments**:
- `target` (str): The domain name (e.g., `"google.com"`).

**Returns**:
- `str | None`: The resolved IP address, or `None` if the resolution fails.

**Example**:
```python
ip = lunarscan.get_ip("github.com")
print(ip)
```

## Notes

- The `geoscan` function uses the `ip-api.com` service to fetch geolocation data. Ensure you have internet access.
- Port scanning in the `scan` function has a timeout of 1 second per port for performance.
- Future versions may include multithreading, banner grabbing, and CLI support.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.