import torch
import torch.jit
import huggingface_hub
import os
from enum import Enum
from pathlib import Path

class MODELS():
    MSCONV3Ds = 'MSCONV3D'

class WEIGHTS(Enum):
    TUCHRI = 'TUC-HRI'
    TUCHRI_CS = 'TUC-HRI-CS'

#__example__ from rsp.ml.model import publish_model
#__example__
#__example__ model = torch.nn.Sequential(
#__example__     torch.nn.Linear(10, 10),
#__example__     torch.nn.ReLU(),
#__example__     torch.nn.Linear(10, 10)
#__example__ )
#__example__ publish_model(
#__example__     user_id='SchulzR97',
#__example__     model_id='MSCONV3D', 
#__example__     weights_id='TUC-HRI-CS',
#__example__     model=model,
#__example__     input_shape=(1, 30, 3, 400, 400),
#__example__     hf_token=None
#__example__ )
def publish_model(
        user_id:str,
        model_id:str,
        weights_id:str,
        model:torch.nn.Module,
        input_shape:tuple,
        hf_token:str = None
):
    """
    Publishes a PyTorch model to HuggingFace.
    
    Parameters
    ----------
    user_id : str
        HuggingFace username
    model_id : str
        Model name
    weights_id : str
        Weights name
    model : torch.nn.Module
        PyTorch model to publish
    input_shape : tuple
        Input shape of the model
    hf_token : str, optional
        HuggingFace token, by default None. If None, it will be read from the cache directory or prompted from the user
    """
    cache_dir = Path('.cache')
    repo_dir = cache_dir.joinpath(model_id)
    repo_dir.mkdir(exist_ok=True, parents=True)

    if hf_token is None:
        token_file = cache_dir.joinpath('token.txt')
        if token_file.exists():
            with open(token_file, 'r') as f:
                hf_token = f.read().strip()
        else:
            hf_token = input('Please enter your HuggingFace token: ')
            with open(token_file, 'w') as f:
                f.write(hf_token)
    huggingface_hub.login(token=hf_token)

    repo = huggingface_hub.Repository(local_dir=repo_dir, clone_from=f'{user_id}/{model_id}')
    repo.git_pull()

    model_path = repo_dir.joinpath(f'{weights_id}.pth')
    scripted_model = torch.jit.trace(model, torch.rand(input_shape, dtype=torch.float32))
    scripted_model.save(model_path)

    repo.push_to_hub()

#__example__ from rsp.ml.model import load_model
#__example__
#__example__ model = load_model(
#__example__     user_id='SchulzR97',
#__example__     model_id='MSCONV3D',
#__example__     weights_id='TUC-HRI-CS'
#__example__ )
def load_model(
        user_id:str,
        model_id:str,
        weights_id:str
    ) -> torch.nn.Module:
    """
    Loads a PyTorch model from HuggingFace.

    Parameters
    ----------
    user_id : str
        HuggingFace username
    model_id : str
        Model name
    weights_id : str
    """

    api = huggingface_hub.HfApi()
    model_path = api.hf_hub_download(f'{user_id}/{model_id}', filename=f'{weights_id}.pth')

    model = torch.jit.load(model_path)

    return model

#__example__ #import rsp.ml.model as model
#__example__
#__example__ model_weight_files = model.list_model_weights()
def list_model_weights():
    """
    Lists all available weight files.

    Returns
    -------
    List[Tuple(str, str)]
        List of (MODEL:str, WEIGHT:str)
    """
    weight_files = []
    username = 'SchulzR97'
    for model in huggingface_hub.list_models(author=username):
        for file in huggingface_hub.list_repo_files(model.id):
            appendix = file.split('.')[-1]
            if appendix not in ['bin', 'pt', 'pth']:
                continue
            model_id = model.id.replace(f'{username}/', '')
            weight_id = file
            weight_files.append((model_id, weight_id))
            print(weight_files[-1])
    return weight_files

if __name__ == '__main__':
    # load_model
    model = load_model(
        user_id='SchulzR97',
        model_id='MSCONV3D',
        weights_id='TUC-HRI-CS'
    )
    pass

    # publish_model
    model = torch.nn.Sequential(
        torch.nn.Linear(10, 10),
        torch.nn.ReLU(),
        torch.nn.Linear(10, 10)
    )
    publish_model(
        user_id='SchulzR97',
        model_id='MSCONV3D', 
        weights_id='TUC-HRI-CS',
        model=model,
        hf_token=None
    )

    list_model_weights()

    model = load_model(MODELS.TUCARC3D, WEIGHTS.TUCAR)