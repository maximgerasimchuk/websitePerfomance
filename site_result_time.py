import json
import io


class SiteResult:
    def __init__(self, name, ip, dns_lookup, tcp_connection_time, http_response_code, redirect_count, load_content_time):
        self.name = name
        self.ip = ip
        self.dns_lookup_time = dns_lookup
        self.tcp_connection_time = tcp_connection_time
        self.status_code = http_response_code
        self.redirect_count = redirect_count
        self.load_content_time = load_content_time

    def write_json_file(self):
        data = {}
        data[{
            "site": [{
                "name": self.name,
                "ip_address": self.ip,
                "dns_lookup_time": self.dns_lookup_time,
                "tcp_connection_time": self.tcp_connection_time,
                "status_code": self.status_code,
                "redirect_count": self.redirect_count,
                "load_content_time": self.load_content_time
            }]
        }]
        print(json.dump(data))
        with io.open('siteResult.json', 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=False)