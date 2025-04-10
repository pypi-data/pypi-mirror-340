import os
import time
import shutil
import pytest
import random
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient

from raic.foundry.client.environment import EnvironmentEnum
import raic.foundry.shared.azure
from raic.foundry.client.context import login_if_not_already
from raic.foundry.datasources import Datasource
from raic.foundry.inference import InferenceRun

# Get the directory of the current script
root_dir = Path(os.path.abspath(__file__)).parent.parent.absolute()

def test_new(setUp):
    test_name, _, data_source, _ = setUp

    try:
        # Act
        run = InferenceRun.new(name=f'Integration Test {test_name}', data_source=data_source)

        while not run.is_complete():
            print("Waiting for inference run to complete...")
            time.sleep(10)

        data_frame = run.fetch_predictions_as_dataframe()
        print(data_frame)

        # Assert
        assert len(data_frame) > 0
    finally:
        if 'run' in locals() and run is not None:
            # Cleanup Inference Run
            run.delete()        

def test_new_classification_only(setUp):
    test_name, _, data_source, _ = setUp

    try:
        # Act
        run = InferenceRun.new(name=f'Integration Test {test_name}', data_source=data_source, universal_detector=None)

        while not run.is_complete():
            print("Waiting for inference run to complete...")
            time.sleep(10)

        data_frame = run.fetch_predictions_as_dataframe()
        print(data_frame)

        # Assert
        assert len(data_frame) > 0
    finally:
        if 'run' in locals() and run is not None:
            # Cleanup Inference Run
            run.delete()

def test_results_as_dataframe(setUp):
    test_name, _, data_source, _ = setUp

    # Arrange
    run = InferenceRun.from_existing('Whales - 11JUL')

    # Act
    data_frame = run.fetch_predictions_as_dataframe()
    print(data_frame)

    # Assert
    assert len(data_frame) > 0
 
def test_crop_download(setUp):
    test_name, _, data_source, output_directory = setUp

    # Arrange
    run = InferenceRun.from_existing('0030c086-30cc-4c7c-830b-e430dd311e99')

    # Act
    count = 0
    for downloaded_image_path in run.stream_crop_images(output_directory):
        print(downloaded_image_path)
        count=count+1

    # Assert
    assert count > 0 

@pytest.fixture
def setUp(request: pytest.FixtureRequest):
    test_name = request.node.name
    workspace_directory = os.path.join(str(root_dir), ".ignore")
    datasources_directory = os.path.join(str(root_dir), ".ignore/datasources")
    output_directory = Path(workspace_directory, 'test', test_name)

    # Clear previous run output
    if output_directory.is_dir():
        print(f'Cleaning up any previous runs of {test_name} before starting...')
        shutil.rmtree(str(output_directory))

    output_directory.mkdir(parents=True, exist_ok=True)

    # Ensure logged in
    login_if_not_already(environment=EnvironmentEnum.Prod)

    input_path = _load_test_imagery_from_scus(datasources_directory, 'foundry-test-geotiff', 'test_geotiff')
    data_source_name = f'Integration Test {test_name}_datasource_{random.randint(1, 100)}'
    data_source = Datasource.new_from_local_folder(data_source_name, input_path)
    print(f'Setup for {test_name} complete')

    yield test_name, workspace_directory, data_source, output_directory

    # Tear Down
    if data_source is not None:
        # Cleanup Data Source
        data_source.delete()


def _load_test_imagery_from_scus(datasources_directory, data_source_container, destination_folder):
    imagery_datasource_folder = os.path.join(datasources_directory, destination_folder)
    account_url = "https://devstraicscussynth.blob.core.windows.net"

    if os.path.exists(imagery_datasource_folder):
        print(f'Imagery folder {imagery_datasource_folder} already exists')
    else:
        print(f'Creating service client for {account_url}...')
        secretClient = SecretClient("https://dev-kv-raic-scus-synth.vault.azure.net", AzureCliCredential())
        connection_string = secretClient.get_secret('BlobStorage--DefaultBlobStorage--ProviderOptions--ConnectionString').value
        assert connection_string is not None

        service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = service_client.get_container_client(data_source_container)

        print(f'Retrieving list of files in datasource container {data_source_container}...')
        blob_list = container_client.list_blobs()
        blob_list = [blob.name for blob in blob_list]

        print(f'There are {len(blob_list)} files in this datasource.  Let\'s download them')
        for blob_name in blob_list:
            _download_blob(container_client, blob_name, imagery_datasource_folder)

    return imagery_datasource_folder


def _download_blob(container_client, blob_name, imagery_datasource_folder):
    blob_client = container_client.get_blob_client(blob_name)
    local_file_path = os.path.join(imagery_datasource_folder, blob_name)

    if not os.path.exists(os.path.dirname(local_file_path)):
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

    print(f'Downloading {local_file_path}...')
    with open(local_file_path, "wb") as local_file:
        download_stream = blob_client.download_blob(max_concurrency=4)
        download_stream.readinto(local_file)


def _assert_blob_exists(data_source, blob_name):
    container_url = data_source.get_blob_storage_container_url()
    assert raic.foundry.shared.azure.blob_exists(container_url, blob_name) == True, f'Blob {blob_name} not found in data source {data_source._record['name']} ({data_source.datasource_id})'


def _remove_files_except(directory, keep_files):
    if os.path.isfile(directory):
        directory = os.path.dirname(directory)

    for file_or_folder_name in os.listdir(directory):
        filepath = os.path.join(directory, file_or_folder_name)

        if os.path.isfile(filepath) and file_or_folder_name not in keep_files:
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath)

