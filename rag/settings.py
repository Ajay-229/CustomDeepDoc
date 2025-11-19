import logging
from common.misc_utils import pip_install_torch

PARALLEL_DEVICES = 0
try:
    pip_install_torch()
    import torch.cuda
    PARALLEL_DEVICES = torch.cuda.device_count()
    logging.info(f"found {PARALLEL_DEVICES} gpus")
except Exception:
    logging.info("can't import package 'torch'")