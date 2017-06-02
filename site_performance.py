import argparse
import pycurl
import socket
import site_result_time
from io import BytesIO

global site
global ip
global dns_lookup
global tcp_connection_time
global http_response_code
global redirect_count
global load_content_time
site_list = ['google.com', 'yahoo.com', 'amazon.com', 'cnn.com', 'msn.com', 'ebay.com']
buffer = BytesIO()
curl = pycurl.Curl()
multi_curl = pycurl.CurlMulti()


def get_all_information(timeout, is_json_output, user_agent, parallel):
    print("Test information about sites")

    if user_agent:
        curl.setopt(curl.USERAGENT, user_agent)
        print(user_agent + " - user agent")

    for site in site_list:
        curl.setopt(curl.URL, "https://www." + site + "/")
        curl.setopt(curl.WRITEDATA, buffer)
        curl.perform()
        multi_curl.timeout()

        print("***** " + site.upper() + " *****")
        ip = socket.gethostbyname(site)
        dns_lookup = curl.getinfo(curl.NAMELOOKUP_TIME)
        tcp_connection_time = curl.getinfo(curl.CONNECT_TIME)
        http_response_code = curl.getinfo(curl.HTTP_CODE)
        redirect_count = curl.getinfo(curl.REDIRECT_COUNT)
        if http_response_code == 200:
            load_content_time = curl.getinfo(curl.TOTAL_TIME)

        print("IP address: " + ip)
        print('DNS resolution time for the domain: %f' % dns_lookup)
        print('TCP connection time: %f' % tcp_connection_time)
        print('The HTTP response code: %i' % http_response_code)
        print('The number of redirects: %i' % redirect_count)

        if http_response_code == 200:
            print('Get content time: %f' % load_content_time)
        else:
            print("HTTP response Code isn't 200! Content didn't load.")
        print('*** END ***')

        if is_json_output:
            site_result_time.SiteResult.__init__(site, ip, dns_lookup, tcp_connection_time, http_response_code, redirect_count, load_content_time)

    pass


def write2file():
    site_result_time.SiteResult.__init__(site, ip, dns_lookup, tcp_connection_time, http_response_code, redirect_count, load_content_time)


def write2TestFile():
    site_result_time.SiteResult.__init__(site_result_time, "google.com", "192.168.0.1", 0.0008, 0.005, 200, 2, 5.35)
    site_result_time.SiteResult.write_json_file(site_result_time)


def str2bool(v):
    if v.lower() in ('yes', 'true', 'y', 't', '1'):
        return True
    elif v.lower() in ('no', 'false', 'n', 'f', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected: 'yes'/'no', 'true'/'false', '1'/'2'")


def create_parser():
    parser = argparse.ArgumentParser(
        description='Test response time for some parameters'
    )

    parser.add_argument(
        '-W', '--wright', type=str2bool, required=True,
        help='Is need to write test result to json file? - enter boolean value.'
    )

    parser.add_argument(
        '-A', '--agent', type=str, required=False,
        help='Specify the user agent the requests are made from. If needed.'
    )

    parser.add_argument(
        '-T', '--timeout', type=float, required=True,
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
    #get_all_information(args.timeout, args.wright, args.agent, args.parallel)
    write2TestFile()


if __name__ == '__main__':
    main()
