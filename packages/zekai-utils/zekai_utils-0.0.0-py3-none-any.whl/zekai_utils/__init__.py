import os
import pickle
import pandas as pd
import json
import torch
import torch.nn as nn
import numpy as np
import yaml
from PIL import Image, ImageSequence
import cv2
import csv
import imageio
import safetensors
from loguru import logger
import glob
import subprocess
import copy
import random
from multiprocessing import Pool
from tqdm import tqdm
import re
from datetime import datetime
import uuid
import pathlib
from safetensors import safe_open
from safetensors.torch import save_file
import sys
from colorama import Fore, Style

def loguru_format(record):
    level = record["level"].name
    if level == "WARNING": color = Fore.RED
    else: color = Fore.GREEN
    return f"{Style.BRIGHT}{color}[{record['level'].name}]: {record['message']}\n{Style.RESET_ALL}"

logger.remove()
logger.add(sys.stderr, format=loguru_format)


def file2data(path):
    ext = path.split('.')[-1]
    if ext in ["txt", "html"]:
        with open(path, encoding='utf-8') as f:
            data = [e for e in f.read().split('\n') if e]
    elif ext == "json":
        with open(path) as f:
            data = json.load(f)
    elif ext == "jsonl":
        with open(path, 'rb') as f:
            data = [json.loads(e) for e in f.readlines()]
    elif ext == "yaml":
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
    elif ext == "csv":
        data = pd.read_csv(path)
    elif ext == 'xlsx':
        data = pd.read_excel(path)
    elif ext == "pkl":
        with open(path, 'rb') as f:
            data = pickle.load(f)
    elif ext in ['pth', 'ckpt', 'pt']:
        data = torch.load(path, map_location='cpu')
    elif ext in ["npy", "npz"]:
        data = np.load(path)
    elif ext == "safetensors":
        data = {}
        with safetensors.safe_open(path, framework="pt", device="cpu") as f:
            for key in f.keys():
                data[key] = f.get_tensor(key)
    elif ext == 'parquet':
        data = pd.read_parquet(path)
    elif ext in ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif', 'webp']:
        with Image.open(path) as img:
            data = np.array(img)
    elif ext == "gif":
        gif = Image.open(path)
        lst = []
        for frame in ImageSequence.Iterator(gif):
            frame_arr = np.array(frame.convert('RGB'))
            lst.append(frame_arr)
        data = np.stack(lst)
    elif ext in ['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv']:
        frames = []
        cap = cv2.VideoCapture(path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
        cap.release()
        data = np.array(frames)
    else:
        raise ValueError(f'Unsupported {path} with ext: {ext}')
    return data

def data2file(data, path):
    ext = path.split('.')[-1]
    if ext == "html":
        with open(path, 'w') as f:
            f.write(data)    
    if ext == "txt":
        if isinstance(data, list): pass
        elif isinstance(data, str): data = [data]
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(map(str, data)))
    elif ext == "json":
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    elif ext == "jsonl":
        with open(path, 'w', encoding='utf-8') as f:
            for entry in data:
                json.dump(entry, f, ensure_ascii=False)
                f.write('\n')
    elif ext == "yaml":
        with open(path, 'w') as f:
            yaml.safe_dump(data, f)
    elif ext == "csv":
        with open(path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)
    elif ext == 'xlsx':
        pd.DataFrame(data).to_excel(path, index=False)
    elif ext == "pkl":
        with open(path, 'wb') as f:
            pickle.dump(data, f)
    elif ext in ['pth', 'ckpt', 'pt']:
        torch.save(data, path)
    elif ext in ["npy", "npz"]:
        np.save(path, data)
    elif ext == "safetensors":
        save_file(data, path)
    elif ext == 'parquet':
        data.to_parquet(path, index=False)
    elif ext in ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif', 'webp']:
        img = Image.fromarray(data.astype(np.uint8))
        img.save(path)
    elif ext == "gif":
        imageio.mimsave(path, data, format='GIF', duration=0.1)
    elif ext in ['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv']:
        imageio.mimsave(path, data, format=pathlib.Path(path).suffix, fps=16, codec='libx264')
    else:
        raise ValueError(f'Unsupported {path} with ext: {ext}')
    return data

def list_folder(folder, pattern=''):
    search_pattern = os.path.join(folder, pattern) if pattern else os.path.join(folder, '*')
    matching_files = glob.glob(search_pattern)
    matching_files = sorted(matching_files)
    return matching_files

def ensure_folder(folder):
    os.makedirs(folder, exist_ok=True)

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    try: 
        return result.stdout
    except:
        print(f"Error {cmd}: {result.stderr}")

def easy_args(arg_dict):
    class EasyArgs:
        def __init__(self, arg_dict):
            for key, value in arg_dict.items():
                setattr(self, key, value)
    return EasyArgs(arg_dict)

def syncpoint(msg):
    try:
        torch.distributed.barrier()
        logger.info(f"Sync point [ {msg} ]")
    except:
        pass

def dist_info():
    world_size = int(os.environ.get("WORLD_SIZE", -1))
    rank = int(os.environ.get("RANK", -1))
    return rank, world_size

def dist_shard(x):
    rank, world_size = dist_info()
    if world_size == -1:
        return x
    else:
        assigned = copy.deepcopy(x[rank::world_size])
        return assigned

def count_params(model, mode='all'):
    if mode == 'all':
        num = sum(p.numel() for p in model.parameters())
    elif mode == 'freeze':
        num = sum(p.numel() for p in model.parameters() if not p.requires_grad)
    elif mode == 'unfreeze':
        num = sum(p.numel() for p in model.parameters() if  p.requires_grad)
    return f"{round(num/1e6,3)} M"

def set_seed(seed=0):
    random.seed(seed)
    os.environ['PYHTONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False

def mp_wrapper(func, n=-1):
    def wrapper(lst_x):
        local_n = n  
        if local_n == -1:
            local_n = os.cpu_count()
        if local_n > len(lst_x):
            local_n = len(lst_x)
        with Pool(processes=local_n) as pool:
            results = list(tqdm(pool.imap(func, lst_x), total=len(lst_x), desc="Processing"))
        return results
    return wrapper

def dist_run(func, args):
    args = dist_shard(args)
    for arg in tqdm(args):
        func(arg)

def extract_pattern(x, pattern):
    # r"(.*?)" must be raw string!
    matches = re.findall(pattern, x)
    return matches

def load_sd(model, path):
    state_dict = torch.load(path, map_location='cpu')
    model.load_state_dict(state_dict, strict=True)
    return model

def get_timestr():
    now = datetime.now()
    time_str = now.strftime("%Y%m%d%H%M%S")
    return time_str

def get_uuid():
    unique_id = uuid.uuid4()
    return str(unique_id)

def log_rank0(msg):
    rank, world_size = dist_info()
    if rank == 0: logger.info(msg)

def warn_rank0(msg):
    rank, world_size = dist_info()
    if rank == 0: logger.warning(msg)

if __name__ == '__main__':
    pass