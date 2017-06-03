import argparse
import pycurl
import socket
import yaml
import site_result_time
from io import BytesIO

buffer = BytesIO()
curl = pycurl.Curl()


def get_all_information(timeout, is_json_output, user_agent, parallel):
    site_list = get_site_list()

    curl.setopt(curl.WRITEDATA, buffer)
    curl.setopt(curl.FOLLOWLOCATION, True)

    if user_agent:
        curl.setopt(curl.USERAGENT, user_agent)
    if timeout:
        curl.setopt(curl.TIMEOUT, timeout)
    result_list = []

    for site in site_list:
        curl.setopt(curl.URL, "https://www." + site + "/")
        try:
            curl.perform()
        except Exception as exc:
            print("Exception: ", exc.args)
            pass

        http_response_code = curl.getinfo(curl.HTTP_CODE)
        ip = socket.gethostbyname(site)
        dns_lookup = curl.getinfo(curl.NAMELOOKUP_TIME)
        tcp_connection_time = curl.getinfo(curl.CONNECT_TIME)
        redirect_count = curl.getinfo(curl.REDIRECT_COUNT)

        if http_response_code == 200:
            load_content_time = curl.getinfo(curl.TOTAL_TIME)
        else:
            load_content_time = 0

        print("Test result for site: ", site)
        data = {
            site: {
                "ip_address": ip,
                "dns_lookup_time": dns_lookup,
                "tcp_connection_time": tcp_connection_time,
                "status_code": http_response_code,
                "redirect_count": redirect_count,
                "load_content_time": load_content_time
            }
        }
        print(data)
        result = site_result_time.SiteResult(site, ip, dns_lookup, tcp_connection_time,
                                             http_response_code, redirect_count, load_content_time)
        result_list.append(result)

    curl.close()

    if is_json_output:
        result.write_json_file(result_list)

    pass


def str2bool(v):
    if v.lower() in ('yes', 'true', 'y', 't', '1'):
        return True
    elif v.lower() in ('no', 'false', 'n', 'f', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected: 'yes'/'no', 'true'/'false', '1'/'2'")


def get_user_agent(agent):
    if str.lower(agent) in ["safari", "chrome", "android", "opera_mini"]:
        with open("site_time_config.yml", 'r') as f:
            doc = yaml.load(f)
            return doc["user_agent"][str.lower(agent)]
    else:
        return agent


def get_site_list():
    with open("site_time_config.yml", 'r') as f:
        doc = yaml.load(f)
        return doc["site_list"]


def create_parser():
    parser = argparse.ArgumentParser(
        description='Test response time for some parameters'
    )

    parser.add_argument(
        '-W', '--wright', type=str2bool, required=True,
        help='Is need to write test result to json file? - enter boolean value.'
    )

    parser.add_argument(
        '-A', '--agent', type=get_user_agent, required=True,
        help='Specify the user agent the requests are made from. If needed.'
    )

    parser.add_argument(
        '-T', '--timeout', type=int, required=True,
        help='Enter the timeout in seconds.'
    )

    parser.add_argument(
        '-P', '--parallel', type=int, required=False,
        help='Enter the count of threads if you want to to specify the concurrency. Default is 1 thread.'
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    get_all_information(args.timeout, args.wright, args.agent, args.parallel)


if __name__ == '__main__':
    main()
