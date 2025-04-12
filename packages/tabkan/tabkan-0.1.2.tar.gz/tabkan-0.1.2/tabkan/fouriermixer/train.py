import torch
import torch.nn as nn
import torch.optim as optim
from tabkan.utils import create_data_loaders, train_model
from tabkan.fouriermixer import FourierKANMixer


def fit(X_train, y_train, X_valid, y_valid, params, device='cuda'):
    model = FourierKANMixer(
        num_features=X_train.shape[1],
        num_classes=y_train.max().item() + 1 if y_train.ndim == 1 else y_train.shape[1],
        num_layers=params.get('num_layers', 4),
        token_dim=params.get('token_dim', 64),
        channel_dim=params.get('channel_dim', 128),
        token_order=params.get('token_order', 3),
        channel_order=params.get('channel_order', 3)
    ).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=params.get('lr', 1e-3))

    train_loader, valid_loader = create_data_loaders(
        X_train, y_train, X_valid, y_valid,
        batch_size=params.get('batch_size', 32)
    )

    train_model(
        model, train_loader, valid_loader,
        criterion, optimizer, device,
        num_epochs=params.get('epochs', 50)
    )

    return model
