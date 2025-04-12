import torch
import torch.nn as nn
from .layer import ChebyKANLayer  # you’ll need to create/import this


class ChebyshevKAN(nn.Module):
    def __init__(self, layers=None, orders=None):
        super(ChebyshevKAN, self).__init__()
        self._layers = layers
        self._orders = orders
        self.layers = nn.ModuleList()

        if layers and orders:
            for i in range(len(layers) - 2):
                self.layers.append(ChebyKANLayer(layers[i], layers[i + 1], orders[i]))
            self.layers.append(nn.Linear(layers[-2], layers[-1]))

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
