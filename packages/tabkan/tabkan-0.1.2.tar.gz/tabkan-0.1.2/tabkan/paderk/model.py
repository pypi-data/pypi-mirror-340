import torch
import torch.nn as nn
from rkan.torch import PadeRKAN


class PadeKAN(nn.Module):
    def __init__(self, layers=None, orders1=None, orders2=None):
        super(PadeKAN, self).__init__()
        self._layers = layers
        self._orders1 = orders1
        self._orders2 = orders2
        self.layers = nn.ModuleList()

        if layers and orders1 and orders2:
            for i in range(len(layers) - 1):
                self.layers.append(nn.Linear(layers[i], layers[i + 1]))
                if i < len(layers) - 2:
                    self.layers.append(PadeRKAN(orders1[i], orders2[i]))

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

    def fit(self, dataset, steps=100, loss_fn=None, lr=1., batch=-1):
        from .train import fit
        return fit(self, dataset, steps, loss_fn, lr, batch)

    def tune(self, dataset, input_shape, output_shape, device, trials=50,
             EPOCHS=100, MAX_DEPTH=10, MAX_NEURONS=50):
        import optuna
        from .train import objective

        study = optuna.create_study(direction="maximize")

        study.optimize(
            lambda trial: objective(
                trial=trial,
                dataset=dataset,
                input_shape=input_shape,
                output_shape=output_shape,
                device=device,
                EPOCHS=EPOCHS,
                MAX_DEPTH=MAX_DEPTH,
                MAX_NEURONS=MAX_NEURONS
            ),
            n_trials=trials
        )

        return study.best_params
