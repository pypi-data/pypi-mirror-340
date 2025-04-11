import time
from pathlib import Path
import raic.foundry.client.context
from raic.foundry.datasources import Datasource
from raic.foundry.models import UniversalDetector, VectorizerModel, PredictionModel
from raic.foundry.inference import InferenceRun
import raic.foundry.results.embedding
from raic.foundry.client.environment import EnvironmentEnum


def create_data_source():
    data_source = Datasource.new_from_local_folder(name='CM Test Data Source', local_path='./samples')
    print(data_source)

def create_inference_run():
    data_source = Datasource.from_existing('Brewers Demo')
    universal_detector = UniversalDetector.from_existing('baseline', version='latest')
    vectorizer_model = VectorizerModel.from_existing('baseline', version='latest')
    run = InferenceRun.new(
        name='CM Inference Run', 
        data_source=data_source, 
        universal_detector=universal_detector,
        vectorizer_model=vectorizer_model
    )
    
    print(run)

    while not run.is_complete():
        print("Waiting for run to complete...")
        time.sleep(30)

def create_inference_run_classification_only():
    data_source = Datasource.from_existing('Manufacturing Defect 2 Unzipped')
    run = InferenceRun.new(
        name='CM Classification Only', 
        data_source=data_source, 
        universal_detector=None
    )
    
    print(run)

    while not run.is_complete():
        print("Waiting for run to complete...")
        time.sleep(30)

def wait_and_return_dataframe():
    run = InferenceRun.from_existing('28961b03-f846-4b39-ac07-4ec5a73bf513')
    df = run.wait_and_return_dataframe()
    print(df)

def iterate_predictions():
    run = InferenceRun.from_existing('28961b03-f846-4b39-ac07-4ec5a73bf513')

    for prediction in run.iterate_predictions():
        print(prediction)

    df = run.fetch_predictions_as_dataframe()
    print(df)

def vectorize_and_image():
    image_path = Path('samples/image24-12-17_06-00-00-94.jpg')

    model = VectorizerModel.from_existing('baseline')
    result = raic.foundry.results.embedding.create_embedding(image_path, model)
    print(result)


def corey():
    from raic.foundry.datasources import Datasource
    from raic.foundry.models import VectorizerModel
    from raic.foundry.inference import InferenceRun

    # Look up existing data source record
    data_source = Datasource.from_existing('NAIP NY_2021 Example 1')

    # Look up the vectorizer model
    vectorizer_model = VectorizerModel.from_existing('baseline', version='latest')

    # Start new inference run
    run = InferenceRun.new(name='CM Test', data_source=data_source, universal_detector=None, vectorizer_model=vectorizer_model)
    print(f'Inference run {run.id} started')

    data_frame = run.wait_and_return_dataframe()
    data_frame.to_csv('cm_test.csv', index=False)


def corey2():
    # Start new inference run
    run = InferenceRun.from_existing(identifier='32706070-a7d6-4526-b112-f82efc8cb936')
    print(f'Inference run {run.id} found')

    data_frame = run.wait_and_return_dataframe()
    data_frame.to_csv('cm_test.csv', index=False)

if __name__ == "__main__":
    raic.foundry.client.context.login_if_not_already(environment=EnvironmentEnum.Prod)
    #create_data_source()
    #create_inference_run_classification_only()
    #create_inference_run()
    #wait_and_return_dataframe()
    #iterate_predictions()
    #vectorize_and_image()
    #corey()
    corey2()

    print("Done")


    