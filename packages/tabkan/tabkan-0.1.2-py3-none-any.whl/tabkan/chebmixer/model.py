import torch
import torch.nn as nn


class ChebyKANLayer(nn.Module):
    def __init__(self, input_dim, output_dim, degree):
        super().__init__()
        self.inputdim = input_dim
        self.outdim = output_dim
        self.degree = degree
        self.cheby_coeffs = nn.Parameter(torch.empty(input_dim, output_dim, degree + 1))
        nn.init.normal_(self.cheby_coeffs, mean=0.0, std=1 / (input_dim * (degree + 1)))

    def forward(self, x):
        x = x.reshape(-1, self.inputdim)
        x = torch.tanh(x)
        cheby = torch.ones(x.shape[0], self.inputdim, self.degree + 1, device=x.device)
        if self.degree > 0:
            cheby[:, :, 1] = x
        for i in range(2, self.degree + 1):
            cheby[:, :, i] = 2 * x * cheby[:, :, i - 1] - cheby[:, :, i - 2]
        y = torch.einsum('bid,iod->bo', cheby, self.cheby_coeffs)
        return y.view(-1, self.outdim)


class fKAN(nn.Module):
    def __init__(self, layers, orders):
        super().__init__()
        self.layers = nn.ModuleList()
        for i in range(len(layers) - 2):
            self.layers.append(ChebyKANLayer(layers[i], layers[i + 1], orders[i]))
        self.layers.append(nn.Linear(layers[-2], layers[-1]))

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x


class MixerLayerKAN(nn.Module):
    def __init__(self, num_tokens, token_dim, channel_dim, token_order=3, channel_order=3):
        super().__init__()
        self.norm1 = nn.LayerNorm(channel_dim)
        self.token_mixing = fKAN([num_tokens, token_dim, num_tokens], orders=[token_order])
        self.norm2 = nn.LayerNorm(channel_dim)
        self.channel_mixing = fKAN([channel_dim, channel_dim * 2, channel_dim], orders=[channel_order, channel_order])

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
