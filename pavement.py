from paver.easy import *
from paver.setuputils import setup
import threading, os, platform
import json

setup(
    name = "behave-browserstack",
    version = "0.1.0",
    author = "BrowserStack",
    author_email = "support@browserstack.com",
    description = ("Behave Integration with BrowserStack"),
    license = "MIT",
    keywords = "example selenium browserstack",
    url = "https://github.com/browserstack/lettuce-browserstack",
    packages=['features']
)

def run_behave_test(config, feature, task_id=0):

    sh('pytest --driver BrowserStack --variables capabilities{}.json'.format(task_id))




def run_behave_test_parallel(config, feature, task_id=0):

    ###pytest --driver BrowserStack --capability browserName Firefox --capability os Windows --capability os_version 10 --capability build 'Pytest Sample'

    with open('capabilities_parallel.json') as json_file:
        data = json.load(json_file)

    cap = data["capabilities" + str(task_id)]

    print(cap)

    cap_list = []

    cap_string = ""
    
    for key, value in cap.items():
        cap_list.append("--capability " + str(key) + " '" + str(value) + "'")

    for i in cap_list:
        cap_string = cap_string + i + " "
        
    print cap_list
    print cap_string

    # sh('pytest --driver BrowserStack --variables capabilities{}.json'.format(task_id))

    sh('pytest --driver BrowserStack ' + cap_string)



@task
@consume_nargs(1)
def run(args):
    # """Run single, local and parallel test using different config."""
    # if args[0] in ('single', 'local'):
    #     run_behave_test(args[0], args[0])
    # else:

    ####
    jobs = []
    for i in range(1,4):
        # print('hiii')
        p = threading.Thread(target=run_behave_test_parallel,args=(args[0], "single",i))
        jobs.append(p)
        p.start()

    for th in jobs:
        th.join()

    ####

    # run_behave_test_parallel()



@task
def test():
    """Run all tests"""
    sh("paver run single")
    sh("paver run local")
    sh("paver run parallel")
