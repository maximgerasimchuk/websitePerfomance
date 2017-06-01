import argparse
import pycurl
import socket
from io import BytesIO

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
        # body = buffer.getvalue()
        # print(body)
    #     it print body of HTML page

    pass


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
    get_all_information(args.timeout, args.wright, args.agent, args.parallel)


if __name__ == '__main__':
    main()
