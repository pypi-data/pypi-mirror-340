import socket
import requests

def scan(target, start_port, end_port):
    open_ports = []
    print(f"Scanning {target} for open ports between {start_port} and {end_port}. . .")

    for port in range(start_port, end_port + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)

            result = sock.connect_ex((target, port))

            if result == 0:
                open_ports.append(port)
            sock.close()
        except socket.error:
            pass

    return open_ports


def geoscan(target):
    try:
        ip_address = socket.gethostbyname(target)
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,message,continent,country,regionName,city,lat,lon,query")
        data = response.json()

        if data['status'] == 'fail':
            print(f"Geolocation failed: {data.get('message', 'Unknown error')}")
            return

        continent = data.get("continent", "Unknown")
        country = data.get("country", "Unknown")
        state = data.get("regionName", "Unknown")
        city = data.get("city", "Unknown")
        lat = data.get("lat", 0.0)
        lon = data.get("lon", 0.0)

        def to_dms(degree, is_lat=True):
            direction = ''
            if is_lat:
                direction = 'N' if degree >= 0 else 'S'
            else:
                direction = 'E' if degree >= 0 else 'W'

            abs_degree = abs(degree)
            d = int(abs_degree)
            m = int((abs_degree - d) * 60)
            s = round((abs_degree - d - m/60) * 3600, 3)
            return f"{degree:.6f} / {direction} {d}° {m}' {s}''"

        lat_dms = to_dms(lat, is_lat=True)
        lon_dms = to_dms(lon, is_lat=False)

        print(f"Region: {continent}")
        print(f"Country: {country}")
        print(f"State: {state}")
        print(f"City: {city}")
        print(f"Coordinates: {lat_dms}  - {lon_dms}")
        print(f"Scanned IP: {ip_address}")

    except Exception as e:
        print(f"Error during geolocation: {e}")

def get_ip(target):
    try:
        return socket.gethostbyname(target)
    except socket.error:
        return None
