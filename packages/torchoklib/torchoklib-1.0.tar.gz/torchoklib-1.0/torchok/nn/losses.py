import numpy as np
import torchok
from torchok import Tensor
from torchok import nn


class MSELoss(nn.Module):
    def __init__(self):
        super().__init__()

    def __call__(self, pred, y):
        loss  = (pred  -  y) **  2
        return loss
    
class L1Loss(nn.Module):
    def __init__(self):
        super().__init__()

    def __call__(self, pred, y):
        loss  = (pred - y).abs()
        return loss


class CrossEntropyLoss(nn.Module):
    def __init__(self):
        super().__init__()

    def __call__(self, pred, y):
        loss  = - 1 * y * pred.log()
        return loss
    
class CEWithLogitsLoss(nn.Module):
    def __init__(self):
        super().__init__()

    def __call__(self, pred, y):
        pred_probs = pred.softmax()
        loss  = - 1 * y * pred_probs.log()
        return loss
