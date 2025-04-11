import torch
import numpy as np
from tqdm import tqdm
from sklearn.metrics import f1_score
from torch.nn import CrossEntropyLoss
from torch.optim import LBFGS
from .model import PadeKAN


def fit(model, dataset, steps=100, loss_fn=None, lr=1., batch=-1):
    optimizer = LBFGS(model.parameters(), lr=lr, history_size=10, line_search_fn="strong_wolfe",
                      tolerance_grad=1e-32, tolerance_change=1e-32)

    results = {"train_loss": [], "test_loss": []}
    pbar = tqdm(range(steps), desc="description", ncols=100)

    if batch == -1 or batch > dataset["train_input"].shape[0]:
        batch_size = dataset["train_input"].shape[0]
        batch_size_test = dataset["test_input"].shape[0]
    else:
        batch_size = batch
        batch_size_test = batch

    global train_loss

    def closure():
        global train_loss
        optimizer.zero_grad()
        pred = model(dataset['train_input'][train_id])
        train_loss = loss_fn(pred, dataset['train_label'][train_id])
        train_loss.backward()
        return train_loss

    for _ in pbar:
        train_id = np.random.choice(dataset['train_input'].shape[0], batch_size, replace=False)
        test_id = np.random.choice(dataset['test_input'].shape[0], batch_size_test, replace=False)

        optimizer.step(closure)
        test_loss = loss_fn(model(dataset['test_input'][test_id]), dataset['test_label'][test_id])

        results['train_loss'].append(torch.sqrt(train_loss).cpu().detach().numpy())
        results['test_loss'].append(torch.sqrt(test_loss).cpu().detach().numpy())

        pbar.set_description(f"| train_loss: {results['train_loss'][-1]:.2e} | test_loss: {results['test_loss'][-1]:.2e} ")

    return results


def objective(trial, dataset, input_shape, output_shape, device,
              EPOCHS=100, MAX_DEPTH=10, MAX_NEURONS=50):

    depth = trial.suggest_int("depth", 1, MAX_DEPTH)
    width = [trial.suggest_int(f"neurons_layer_{i}", 5, MAX_NEURONS, step=5) for i in range(depth)]
    orders1 = [trial.suggest_int(f"orders1_layer_{i}", 2, 6) for i in range(depth)]
    orders2 = [trial.suggest_int(f"orders2_layer_{i}", 2, 6) for i in range(depth)]

    width = [input_shape] + width + [output_shape]
    model = PadeKAN(width, orders1, orders2).to(device)

    fit(model, dataset, steps=EPOCHS, loss_fn=CrossEntropyLoss())

    X_valid = dataset["test_input"]
    y_valid = dataset["test_label"]

    y_score = model(X_valid).cpu()
    y_pred = (y_score > 0.5).int()

    return f1_score(y_valid.cpu(), y_pred, average="macro")
