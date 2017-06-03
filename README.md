Command-line test tool that gets the content for a list of websites and reports the performance of each website

for run tests use command bellow:
usage: site_performance.py [-h] -W WRIGHT -A AGENT -T TIMEOUT [-P PARALLEL]

optional arguments:
  -h, --help            show this help message and exit
  -W WRIGHT, --wright WRIGHT
                        Is need to write test result to json file? - enter
                        boolean value.
  -A AGENT, --agent AGENT
                        Specify the user agent the requests are made from. If
                        needed.
  -T TIMEOUT, --timeout TIMEOUT
                        Enter the timeout in seconds.
  -P PARALLEL, --parallel PARALLEL
                        Enter the count of threads if you want to to specify
                        the concurrency. Default is 1 thread.