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

def iterate_predictions():
    run = InferenceRun.from_existing('8be65be9-de9a-48a7-a2c4-c2c0f6615ae3')

    for prediction in run.iterate_predictions():
        print(prediction)

    df = run.fetch_predictions_as_dataframe()
    print(df)

def vectorize_and_image():
    image_path = Path('samples/image24-12-17_06-00-00-94.jpg')

    model = VectorizerModel.from_existing('baseline')
    result = raic.foundry.results.embedding.create_embedding(image_path, model)
    print(result)

if __name__ == "__main__":
    raic.foundry.client.context.login_if_not_already(environment=EnvironmentEnum.Dev)

    #create_data_source()
    #create_inference_run_classification_only()
    #create_inference_run()
    #iterate_predictions()
    vectorize_and_image()

    print("Done")


    