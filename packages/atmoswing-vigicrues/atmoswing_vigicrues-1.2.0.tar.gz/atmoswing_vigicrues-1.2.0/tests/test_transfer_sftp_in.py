import os
import shutil
import tempfile
import types
from datetime import datetime

import pytest

import atmoswing_vigicrues as asv

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# Needs a running docker container (see files/sftp-docker-instructions.txt)
RUN_SFTP = False


@pytest.fixture
def options_no_variables():
    with tempfile.TemporaryDirectory() as tmp_dir:
        options_full = asv.Options(
            types.SimpleNamespace(
                config_file=DIR_PATH + '/files/config_cep_download.yaml'
            ))

        action_options = options_full.config['pre_actions'][0]['with']
        action_options['local_dir'] = tmp_dir

    return action_options


@pytest.fixture
def options_with_variables():
    with tempfile.TemporaryDirectory() as tmp_dir:
        options_full = asv.Options(
            types.SimpleNamespace(
                config_file=DIR_PATH + '/files/config_cep_download_with_variables.yaml'
            ))

        action_options = options_full.config['pre_actions'][0]['with']
        action_options['local_dir'] = tmp_dir

    return action_options


@pytest.fixture
def options_arpege():
    with tempfile.TemporaryDirectory() as tmp_dir:
        options_full = asv.Options(
            types.SimpleNamespace(
                config_file=DIR_PATH + '/files/config_arpege_download.yaml'
            ))

        action_options = options_full.config['pre_actions'][0]['with']
        action_options['local_dir'] = tmp_dir

    return action_options


def count_files_recursively(options):
    nb_files = sum([len(files) for r, d, files in os.walk(options['local_dir'])])
    return nb_files


def test_download_cep_no_variables_succeeds(options_no_variables):
    action = asv.TransferSftpIn('Get CEP data over SFTP', options_no_variables)
    date = datetime(2023, 4, 13, 12)
    if RUN_SFTP:
        assert action.run(date)
        assert count_files_recursively(options_no_variables) == 6
        shutil.rmtree(options_no_variables['local_dir'])


def test_download_cep_with_variables_succeeds(options_with_variables):
    action = asv.TransferSftpIn('Get CEP data over SFTP', options_with_variables)
    date = datetime(2023, 4, 13, 12)
    if RUN_SFTP:
        assert action.run(date)
        assert count_files_recursively(options_with_variables) == 4
        shutil.rmtree(options_with_variables['local_dir'])


def test_do_not_download_if_exists(options_with_variables, capsys):
    action = asv.TransferSftpIn('Get CEP data over SFTP', options_with_variables)
    date = datetime(2023, 4, 13, 12)
    if RUN_SFTP:
        assert action.run(date)
        assert count_files_recursively(options_with_variables) == 4
        assert action.run(date)
        captured = capsys.readouterr()
        assert captured.out == "  -> Fichiers déjà présents localement.\n"
        shutil.rmtree(options_with_variables['local_dir'])


def test_download_arpege_succeeds(options_arpege):
    action = asv.TransferSftpIn('Get ARPEGE data over SFTP', options_arpege)
    date = datetime(2023, 4, 17, 00)
    if RUN_SFTP:
        assert action.run(date)
        assert count_files_recursively(options_arpege) == 3
        shutil.rmtree(options_arpege['local_dir'])
