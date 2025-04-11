import torch
import torch.nn as nn
import math


class NaiveFourierKANLayer(nn.Module):
    def __init__(self, inputdim, outdim, gridsize, addbias=True, smooth_initialization=False):
        super().__init__()
        self.gridsize = gridsize
        self.addbias = addbias
        self.inputdim = inputdim
        self.outdim = outdim

        grid_norm_factor = (torch.arange(gridsize) + 1) ** 2 if smooth_initialization else math.sqrt(gridsize)
        self.fouriercoeffs = nn.Parameter(
            torch.randn(2, outdim, inputdim, gridsize) / (math.sqrt(inputdim) * grid_norm_factor)
        )
        if self.addbias:
            self.bias = nn.Parameter(torch.zeros(1, outdim))

    def forward(self, x):
        xshp = x.shape
        outshape = xshp[:-1] + (self.outdim,)
        x = x.view(-1, self.inputdim)
        k = torch.arange(1, self.gridsize + 1, device=x.device).view(1, 1, 1, self.gridsize)
        xr = x.view(x.shape[0], 1, x.shape[1], 1)
        c = torch.cos(k * xr)
        s = torch.sin(k * xr)
        y = torch.sum(c * self.fouriercoeffs[0:1], (-2, -1))
        y += torch.sum(s * self.fouriercoeffs[1:2], (-2, -1))
        if self.addbias:
            y += self.bias
        return y.view(outshape)


class fKAN(nn.Module):
    def __init__(self, layers, gridsizes):
        super().__init__()
        self.layers = nn.ModuleList()
        for i in range(len(layers) - 2):
            self.layers.append(NaiveFourierKANLayer(layers[i], layers[i + 1], gridsize=gridsizes[i]))
        self.layers.append(nn.Linear(layers[-2], layers[-1]))

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x


class MixerLayerKAN(nn.Module):
    def __init__(self, num_tokens, token_dim, channel_dim, token_order=3, channel_order=3):
        super().__init__()
        self.norm1 = nn.LayerNorm(channel_dim)
        self.token_mixing = fKAN([num_tokens, token_dim, num_tokens], gridsizes=[token_order])
        self.norm2 = nn.LayerNorm(channel_dim)
        self.channel_mixing = fKAN([channel_dim, channel_dim * 2, channel_dim], gridsizes=[channel_order, channel_order])

    def forward(self, x):
        y = self.norm1(x)
        y = y.transpose(1, 2)
        B, C, T = y.shape
        y = y.reshape(B * C, T)
        y = self.token_mixing(y)
        y = y.reshape(B, C, T).transpose(1, 2)
        x = x + y

        y = self.norm2(x)
        B, T, C = y.shape
        y = y.reshape(B * T, C)
        y = self.channel_mixing(y)
        y = y.reshape(B, T, C)
        x = x + y
        return x


class KANMixer(nn.Module):
    def __init__(self, num_features, num_classes, num_layers=4, token_dim=64, channel_dim=128,
                 token_order=3, channel_order=3):
        super().__init__()
        self.embedding = nn.Linear(1, channel_dim)
        self.mixer_layers = nn.Sequential(*[
            MixerLayerKAN(num_features, token_dim, channel_dim, token_order, channel_order)
            for _ in range(num_layers)
        ])
        self.norm = nn.LayerNorm(channel_dim)
        self.fc = nn.Linear(channel_dim, num_classes)

    def forward(self, x):
        x = x.unsqueeze(-1)
        x = self.embedding(x)
        x = self.mixer_layers(x)
        x = self.norm(x)
        x = x.mean(dim=1)
        return self.fc(x)
