import json
import io
import datetime


class SiteResult:
    def __init__(self, name, ip, dns_lookup_time, tcp_connection_time, status_code,
                 redirect_count, load_content_time):
        self.site_name = name
        self.ip = ip
        self.dns_lookup_time = dns_lookup_time
        self.tcp_connection_time = tcp_connection_time
        self.status_code = status_code
        self.redirect_count = redirect_count
        self.load_content_time = load_content_time

    @staticmethod
    def write_json_file(result_list, json_data=[]):
        for self in result_list:
            data = {
                self.site_name: [
                    {
                        "ip_address": self.ip,
                        "dns_lookup_time": self.dns_lookup_time,
                        "tcp_connection_time": self.tcp_connection_time,
                        "status_code": self.status_code,
                        "redirect_count": self.redirect_count,
                        "load_content_time": self.load_content_time
                    }
                ]
            }
            json_data.append(data)

        with io.open('result/test_result_' + str(datetime.datetime.now()) + '.json', 'w') as outfile:
            json.dump(json_data, outfile)
