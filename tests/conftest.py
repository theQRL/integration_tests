import pytest
import subprocess
import os
import helpers.runtest_nodes_synchronize
import multiprocessing


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true",
                     default=False, help="run slow tests")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture(scope="session", autouse=True)
def set_up(request):

    print('\n*****************************')
    print('*****************************')
    print('\nSetting up Integration Test environment\n')
    print('*****************************')
    print('*****************************')

    sync_event = multiprocessing.Event()
    w1 = multiprocessing.Process(
        name='nodes',
        target=helpers.runtest_nodes_synchronize.wait_for_sync,
        args=(sync_event,),
    )
    w1.start()
    synced = False
    while w1.is_alive():
     #process is still alive
     #we are still waiting for the sync event
     if sync_event.is_set():
      synced = True
      break
    #check that we could sync
    if synced == False:
        raise Exception('CouldNotSync!')
    yield

    w1.terminate()
    current_path = os.path.dirname(__file__)
    subprocess.call([current_path + '/helpers/reset_net.sh'])

    print('*****************************')
    print('*****************************')
    print('\nTearing Down Integration Test Environment\n')
    print('*****************************')
    print('*****************************')
