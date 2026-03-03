import torch


def detect_device():
    if torch.cuda.is_available():
        return "gpu"
    return "cpu"


def route(requirement_device: str):
    if requirement_device == "cpu":
        return "cpu"

    if requirement_device == "gpu":
        return "gpu" if torch.cuda.is_available() else "cpu"

    if requirement_device == "auto":
        return detect_device()

    return "cpu"
