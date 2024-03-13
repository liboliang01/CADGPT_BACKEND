from django.shortcuts import render
import time

# Create your views here.
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import torch

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import create_pan_cameras, decode_latent_images, gif_widget
from shap_e.util.notebooks import decode_latent_mesh


@api_view(['GET'])
def index(request):
    return Response("Hello, world. You're at the polls index.")

@api_view(['GET'])
def get_model(request):
    return FileResponse(open(r"./backend/models/example.obj", "rb"))

@api_view(['GET'])
def get_model_shap_e(request):
    message = request.GET.get('message',default='a shark')
    print(message)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    xm = load_model('transmitter', device=device)
    model = load_model('text300M', device=device)
    diffusion = diffusion_from_config(load_config('diffusion'))
    
    batch_size = 1
    guidance_scale = 15.0
    prompt = message

    latents = sample_latents(
        batch_size=batch_size,
        model=model,
        diffusion=diffusion,
        guidance_scale=guidance_scale,
        model_kwargs=dict(texts=[prompt] * batch_size),
        progress=True,
        clip_denoised=True,
        use_fp16=False,
        use_karras=True,
        karras_steps=64,
        sigma_min=1e-3,
        sigma_max=160,
        s_churn=0,
    )
    
    timestamp = int(time.time())
    output_dir = os.path.join(os.getcwd(),'output')
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    for i, latent in enumerate(latents):
        output_path = os.path.join(output_dir, f'{timestamp}_mesh_{i}.obj')
        t = decode_latent_mesh(xm, latent).tri_mesh()
        with open(output_path, 'w') as f:
            t.write_obj(f)
    output_path = os.path.join(output_dir, f'{timestamp}_mesh_0.obj')
    return FileResponse(open(output_path, "rb"))