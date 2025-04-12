import os
import shutil
import tempfile
import types
from datetime import datetime, timedelta, timezone

import pytest

import atmoswing_vigicrues as asv

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# With too many requests to the server, the test may fail due to banning.
RUN_REQUESTS = False


@pytest.fixture
def options():
    with tempfile.TemporaryDirectory() as tmp_dir:
        options_full = asv.Options(
            types.SimpleNamespace(
                config_file=DIR_PATH + '/files/config_gfs_download.yaml'
            ))

        action_options = options_full.config['pre_actions'][0]['with']
        action_options['output_dir'] = tmp_dir

    return action_options


def count_files_recursively(options):
    nb_files = sum([len(files) for r, d, files in os.walk(options['output_dir'])])
    return nb_files


def test_download_gfs_fails_if_files_not_found(options):
    if not RUN_REQUESTS:
        return
    action = asv.DownloadGfsData('Download GFS data', options)
    date = datetime.now(timezone.utc)
    date = date.replace(date.year + 1)
    assert action.download(date) is False
    shutil.rmtree(options['output_dir'])


def test_download_gfs_025_succeeds(options):
    if not RUN_REQUESTS:
        return
    options['resolution'] = 0.25
    action = asv.DownloadGfsData('Download GFS data', options)
    date = datetime.now(timezone.utc) - timedelta(days=1)
    assert action.download(date)
    assert count_files_recursively(options) == 3 * 4 * 2
    shutil.rmtree(options['output_dir'])


def test_download_gfs_050_succeeds(options):
    if not RUN_REQUESTS:
        return
    options['resolution'] = 0.50
    action = asv.DownloadGfsData('Download GFS data', options)
    date = datetime.now(timezone.utc) - timedelta(days=1)
    assert action.download(date)
    assert count_files_recursively(options) == 3 * 4 * 2
    shutil.rmtree(options['output_dir'])


def test_download_gfs_100_succeeds(options):
    if not RUN_REQUESTS:
        return
    options['resolution'] = 1
    action = asv.DownloadGfsData('Download GFS data', options)
    date = datetime.now(timezone.utc) - timedelta(days=1)
    assert action.download(date)
    assert count_files_recursively(options) == 3 * 4 * 2
    shutil.rmtree(options['output_dir'])


def test_download_gfs_default_succeeds(options):
    if not RUN_REQUESTS:
        return
    action = asv.DownloadGfsData('Download GFS data', options)
    date = datetime.now(timezone.utc) - timedelta(days=1)
    assert action.download(date)
    assert count_files_recursively(options) == 3 * 4 * 2
    shutil.rmtree(options['output_dir'])


def test_download_gfs_with_surface_var(options):
    if not RUN_REQUESTS:
        return
    options['levels'] = [500, 1000, 'surface']
    action = asv.DownloadGfsData('Download GFS data', options)
    date = datetime.now(timezone.utc) - timedelta(days=1)
    assert action.run(date)
    assert count_files_recursively(options) == 3 * 4 * 2
    shutil.rmtree(options['output_dir'])


def test_download_gfs_entire_atmosphere_var(options):
    if not RUN_REQUESTS:
        return
    options['levels'] = ['entire_atmosphere']
    options['variables'] = ['pwat']
    action = asv.DownloadGfsData('Download GFS data', options)
    date = datetime.now(timezone.utc) - timedelta(days=1)
    assert action.run(date)
    assert count_files_recursively(options) == 3 * 4
    shutil.rmtree(options['output_dir'])
