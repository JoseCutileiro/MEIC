#!/usr/bin/env python

# Deep Learning Homework 1

import argparse

import torch
from torch.utils.data import DataLoader
import torch.nn as nn
from matplotlib import pyplot as plt
import torch.nn.functional as F

import utils


# Q2.1
class LogisticRegression(nn.Module):

    def __init__(self, n_classes, n_features, **kwargs):
        """
        n_classes (int)
        n_features (int)

        The __init__ should be used to declare what kind of layers and other
        parameters the module has. For example, a logistic regression module
        has a weight matrix and bias vector. For an idea of how to use
        pytorch to make weights and biases, have a look at
        https://pytorch.org/docs/stable/nn.html
        """
        super(LogisticRegression, self).__init__()
        self.layer = nn.Linear(n_features, n_classes)

    def forward(self, x, **kwargs):
        """
        x (batch_size x n_features): a batch of training examples

        Every subclass of nn.Module needs to have a forward() method. forward()
        describes how the module computes the forward pass. In a log-lineear
        model like this, for example, forward() needs to compute the logits
        y = Wx + b, and return y (you don't need to worry about taking the
        softmax of y because nn.CrossEntropyLoss does that for you).

        One nice thing about pytorch is that you only need to define the
        forward pass -- this is enough for it to figure out how to do the
        backward pass.
        """
        logits = self.layer(x)
        return logits



# Q2.2
class FeedforwardNetwork(nn.Module):
    def __init__(
            self, n_classes, n_features, hidden_size, layers,
            activation_type, dropout):
        super().__init__()
        self.hidden_layers = nn.ModuleList()
        self.dropout = nn.Dropout(dropout)
        
        # Input layer
        self.hidden_layers.append(nn.Linear(n_features, hidden_size))
        
        # Hidden layers
        for _ in range(layers - 1):
            self.hidden_layers.append(nn.Linear(hidden_size, hidden_size))
        
        # Output layer
        self.output_layer = nn.Linear(hidden_size, n_classes)
        
        self.activation = F.relu

    def forward(self, x):
        for layer in self.hidden_layers:
            x = self.dropout(self.activation(layer(x)))
        x = self.output_layer(x)
        return x


def train_batch(X, y, model, optimizer, criterion, **kwargs):
    """
    X (n_examples x n_features)
    y (n_examples): gold labels
    model: a PyTorch defined model
    optimizer: optimizer used in gradient step
    criterion: loss function

    To train a batch, the model needs to predict outputs for X, compute the
    loss between these predictions and the "gold" labels y using the criterion,
    and compute the gradient of the loss with respect to the model parameters.

    Check out https://pytorch.org/docs/stable/optim.html for examples of how
    to use an optimizer object to update the parameters.

    This function should return the loss (tip: call loss.item()) to get the
    loss as a numerical value that is not part of the computation graph.
    """
    optimizer.zero_grad()  # Clear gradients from the previous iteration

    outputs = model(X)
    loss = criterion(outputs, y)
    loss.backward()  # Compute gradients
    optimizer.step()  # Update weights using optimizer

    return loss.item()


def predict(model, X):
    """X (n_examples x n_features)"""
    scores = model(X)  # (n_examples x n_classes)
    predicted_labels = scores.argmax(dim=-1)  # (n_examples)
    return predicted_labels


@torch.no_grad()
def evaluate(model, X, y, criterion):
    """
    X (n_examples x n_features)
    y (n_examples): gold labels
    """
    model.eval()
    logits = model(X)
    loss = criterion(logits, y)
    loss = loss.item()
    y_hat = logits.argmax(dim=-1)
    n_correct = (y == y_hat).sum().item()
    n_possible = float(y.shape[0])
    model.train()
    return loss, n_correct / n_possible


def plot(epochs, plottables, name='', ylim=None):
    """Plot the plottables over the epochs.
    
    Plottables is a dictionary mapping labels to lists of values.
    """
    plt.clf()
    plt.xlabel('Epoch')
    for label, plottable in plottables.items():
        plt.plot(epochs, plottable, label=label)
    plt.legend()
    if ylim:
        plt.ylim(ylim)
    plt.savefig('%s.pdf' % (name), bbox_inches='tight')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('model',
                        choices=['logistic_regression', 'mlp'],
                        help="Which model should the script run?")
    parser.add_argument('-epochs', default=20, type=int,
                        help="""Number of epochs to train for. You should not
                        need to change this value for your plots.""")
    parser.add_argument('-batch_size', default=1, type=int,
                        help="Size of training batch.")
    parser.add_argument('-learning_rate', type=float, default=0.01)
    parser.add_argument('-l2_decay', type=float, default=0)
    parser.add_argument('-hidden_size', type=int, default=100)
    parser.add_argument('-layers', type=int, default=1)
    parser.add_argument('-dropout', type=float, default=0.3)
    parser.add_argument('-activation',
                        choices=['tanh', 'relu'], default='relu')
    parser.add_argument('-optimizer',
                        choices=['sgd', 'adam'], default='sgd')
    opt = parser.parse_args()

    utils.configure_seed(seed=42)

    data = utils.load_oct_data()
    dataset = utils.ClassificationDataset(data)
    train_dataloader = DataLoader(
        dataset, batch_size=opt.batch_size, shuffle=True, generator=torch.Generator().manual_seed(42))

    dev_X, dev_y = dataset.dev_X, dataset.dev_y
    test_X, test_y = dataset.test_X, dataset.test_y

    n_classes = torch.unique(dataset.y).shape[0]  # 10
    n_feats = dataset.X.shape[1]

    # initialize the model
    if opt.model == 'logistic_regression':
        model = LogisticRegression(n_classes, n_feats)
    else:
        model = FeedforwardNetwork(
            n_classes,
            n_feats,
            opt.hidden_size,
            opt.layers,
            opt.activation,
            opt.dropout
        )

    # get an optimizer
    optims = {"adam": torch.optim.Adam, "sgd": torch.optim.SGD}

    optim_cls = optims[opt.optimizer]
    optimizer = optim_cls(
        model.parameters(),
        lr=opt.learning_rate,
        weight_decay=opt.l2_decay)

    # get a loss criterion
    criterion = nn.CrossEntropyLoss()

    # training loop
    epochs = torch.arange(1, opt.epochs + 1)
    train_losses = []
    valid_losses = []
    valid_accs = []
    for ii in epochs:
        print('Training epoch {}'.format(ii))
        epoch_train_losses = []
        for X_batch, y_batch in train_dataloader:
            loss = train_batch(
                X_batch, y_batch, model, optimizer, criterion)
            epoch_train_losses.append(loss)

        epoch_train_loss = torch.tensor(epoch_train_losses).mean().item()
        val_loss, val_acc = evaluate(model, dev_X, dev_y, criterion)

        print('Training loss: %.4f' % epoch_train_loss)
        print('Valid acc: %.4f' % val_acc)

        train_losses.append(epoch_train_loss)
        valid_losses.append(val_loss)
        valid_accs.append(val_acc)

    _, test_acc = evaluate(model, test_X, test_y, criterion)
    print('Final Test acc: %.4f' % (test_acc))
    # plot
    if opt.model == "logistic_regression":
        config = (
            f"batch-{opt.batch_size}-lr-{opt.learning_rate}-epochs-{opt.epochs}-"
            f"l2-{opt.l2_decay}-opt-{opt.optimizer}"
        )
    else:
        config = (
            f"batch-{opt.batch_size}-lr-{opt.learning_rate}-epochs-{opt.epochs}-"
            f"hidden-{opt.hidden_size}-dropout-{opt.dropout}-l2-{opt.l2_decay}-"
            f"layers-{opt.layers}-act-{opt.activation}-opt-{opt.optimizer}"
        )

    losses = {
        "Train Loss": train_losses,
        "Valid Loss": valid_losses,
    }
    # Choose ylim based on model since logistic regression has higher loss
    if opt.model == "logistic_regression":
        ylim = (0.93, 1.1)
    elif opt.model == "mlp":
        ylim = (min(valid_losses)-0.1, max(valid_losses)+0.1)
    else:
        raise ValueError(f"Unknown model {opt.model}")
    plot(epochs, losses, name=f'{opt.model}-training-loss-{config}', ylim=ylim)
    accuracy = { "Valid Accuracy": valid_accs }
    
    min_y = min(valid_accs) - 0.02
    max_y = max(valid_accs) + 0.02
    plot(epochs, accuracy, name=f'{opt.model}-validation-accuracy-{config}', ylim=(min_y, max_y))


if __name__ == '__main__':
    main()