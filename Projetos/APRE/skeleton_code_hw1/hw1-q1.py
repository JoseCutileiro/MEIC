#!/usr/bin/env python

# Deep Learning Homework 1

import argparse

import numpy as np
import matplotlib.pyplot as plt

import utils


class LinearModel(object):
    def __init__(self, n_classes, n_features, **kwargs):
        self.W = np.zeros((n_classes, n_features))

    def update_weight(self, x_i, y_i, **kwargs):
        raise NotImplementedError

    def train_epoch(self, X, y, **kwargs):
        for x_i, y_i in zip(X, y):
            self.update_weight(x_i, y_i, **kwargs)

    def predict(self, X):
        """X (n_examples x n_features)"""
        scores = np.dot(self.W, X.T)  # (n_classes x n_examples)
        predicted_labels = scores.argmax(axis=0)  # (n_examples)
        return predicted_labels

    def evaluate(self, X, y):
        """
        X (n_examples x n_features):
        y (n_examples): gold labels
        """
        y_hat = self.predict(X)
        n_correct = (y == y_hat).sum()
        n_possible = y.shape[0]
        return n_correct / n_possible


class Perceptron(LinearModel):
    def update_weight(self, x_i, y_i, **kwargs):
        """
        x_i (n_features): a single training example
        y_i (scalar): the gold label for that example
        other arguments are ignored
        """
        scores = np.dot(self.W, x_i)  # Compute scores for each class
        predicted_label = np.argmax(scores)  # Predicted label based on highest score
        
        # Update weights if prediction is incorrect
        if predicted_label != y_i:
            self.W[y_i] += x_i  # Increase weights for the correct class
            self.W[predicted_label] -= x_i  # Decrease weights for the incorrect class


class LogisticRegression(LinearModel):
    def update_weight(self, x_i, y_i, learning_rate=0.001):
        """
        x_i (n_features): a single training example
        y_i: the gold label for that example
        learning_rate (float): keep it at the default value for your plots
        """
        # Q1.1b

        label_scores = self.W.dot(x_i)[:,None]
        
        y_one_hot = np.zeros((np.size(self.W,0),1))
        y_one_hot[y_i] = 1
        
        label_propabilities = np.exp(label_scores) / np.sum(np.exp(label_scores))
        
        self.W += learning_rate * (y_one_hot - label_propabilities) * x_i[None,:]



class MLP(object):
    # Q3.2b. This MLP skeleton code allows the MLP to be used in place of the
    # linear models with no changes to the training loop or evaluation code
    # in main().
    def __init__(self, n_classes, n_features, hidden_size):
        # Initialize an MLP with a single hidden layer.
        print("n_classes: ", n_classes)
        units = [n_features, hidden_size, n_classes]
        W1 = np.random.normal(0.1, 0.1, (units[1], units[0]))
        b1 = np.zeros(units[1])
        W2 = np.random.normal(0.1, 0.1, (units[2], units[1]))
        b2 = np.zeros(units[2])
        self.W = [W1, W2]
        self.b = [b1, b2]

    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=0))  # Log-sum-exp trick
        return exp_x / np.sum(exp_x, axis=0)
    
    def relu(self, x):
        return np.maximum(0, x)
        
    def forward(self, x, weights, biases):
        num_layers = len(weights)
        hiddens = []
        g = self.relu
        # compute hidden layers
        for i in range(num_layers):
                h = x if i == 0 else hiddens[i-1]
                z = weights[i].dot(h) + biases[i]
                if i < num_layers-1:  # Assuming the output layer has no activation.
                    hiddens.append(g(z))
                else:
                    hiddens.append(z)

        #compute output
        output = hiddens[-1]
        return output, hiddens
    
    def backward(self, x, y, output, hiddens, weights):
        num_layers = len(weights)
        probs = self.softmax(output)
        grad_z = probs - y  

        grad_weights = []
        grad_biases = []

        # Backpropagate gradient computations 
        for i in range(num_layers-1, -1, -1):
            
            # Gradient of hidden parameters.
            h = x if i == 0 else hiddens[i-1]
            grad_weights.append(grad_z[:, None].dot(h[:, None].T))
            grad_biases.append(grad_z)
            
            # Gradient of hidden layer below.
            grad_h = weights[i].T.dot(grad_z)

            # Gradient of hidden layer below before activation.
            grad_z = grad_h * (h > 0)   # Grad of loss wrt z3.

        # Making gradient vectors have the correct order
        grad_weights.reverse()
        grad_biases.reverse()
        return grad_weights, grad_biases
    
    def cross_entropy_loss(self, output, y):
        # Compute cross-entropy loss
        probs = self.softmax(output)
        loss = -y.dot(np.log(probs))
        return loss

    def predict(self, X):
        # Compute the forward pass of the network. At prediction time, there is
        # no need to save the values of hidden nodes, whereas this is required
        # at training time.
        predicted_labels = []
        for x in X:
            # Compute forward pass and get the class with the highest probability
            output = self.forward(x, self.W, self.b)[0]
            y_hat = np.argmax(output)
            predicted_labels.append(y_hat)
        predicted_labels = np.array(predicted_labels)
        return predicted_labels

    def evaluate(self, X, y):
        """
        X (n_examples x n_features)
        y (n_examples): gold labels
        """
        # Identical to LinearModel.evaluate()
        y_hat = self.predict(X)
        n_correct = np.sum(y_hat == y)  # Directly compare predicted labels with true labels
        n_possible = y.shape[0]
        return n_correct / n_possible

    def train_epoch(self, X, y, learning_rate=0.001):
        """
        Dont forget to return the loss of the epoch.
        """
        # Comoute forward pass
        total_loss = 0
        for x_i, y_i in zip(X, y):
            y_i_one_hot = np.eye(self.W[-1].shape[0])[y_i]
            output, hiddens = self.forward(x_i, self.W, self.b)
            loss = self.cross_entropy_loss(output, y_i_one_hot)
            total_loss += loss
            # Compute backpropagation
            grad_weights, grad_biases = self.backward(x_i, y_i_one_hot, output, hiddens, self.W)
            
            # Update weights
            
            for i in range(len(self.W)):
                self.W[i] -= learning_rate*grad_weights[i]
                self.b[i] -= learning_rate*grad_biases[i]
        return total_loss


def plot(epochs, train_accs, val_accs):
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.plot(epochs, train_accs, label='train')
    plt.plot(epochs, val_accs, label='validation')
    plt.legend()
    plt.savefig("plot_results.png")
    plt.show()

def plot_loss(epochs, loss):
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.plot(epochs, loss, label='train')
    plt.legend()
    plt.savefig("plot_loss_results.png")
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('model',
                        choices=['perceptron', 'logistic_regression', 'mlp'],
                        help="Which model should the script run?")
    parser.add_argument('-epochs', default=20, type=int,
                        help="""Number of epochs to train for. You should not
                        need to change this value for your plots.""")
    parser.add_argument('-hidden_size', type=int, default=200,
                        help="""Number of units in hidden layers (needed only
                        for MLP, not perceptron or logistic regression)""")
    parser.add_argument('-learning_rate', type=float, default=0.001,
                        help="""Learning rate for parameter updates (needed for
                        logistic regression and MLP, but not perceptron)""")
    opt = parser.parse_args()

    utils.configure_seed(seed=42)

    add_bias = opt.model != "mlp"
    data = utils.load_oct_data(bias=add_bias)
    train_X, train_y = data["train"]
    dev_X, dev_y = data["dev"]
    test_X, test_y = data["test"]
    n_classes = np.unique(train_y).size
    n_feats = train_X.shape[1]

    # initialize the model
    if opt.model == 'perceptron':
        model = Perceptron(n_classes, n_feats)
    elif opt.model == 'logistic_regression':
        model = LogisticRegression(n_classes, n_feats)
    else:
        model = MLP(n_classes, n_feats, 200)
    epochs = np.arange(1, opt.epochs + 1)
    train_loss = []
    valid_accs = []
    train_accs = []
    
    for i in epochs:
        print('Training epoch {}'.format(i))
        train_order = np.random.permutation(train_X.shape[0])
        train_X = train_X[train_order]
        train_y = train_y[train_order]
        if opt.model == 'mlp':
            loss = model.train_epoch(
                train_X,
                train_y,
                learning_rate=opt.learning_rate
            )
        else:
            model.train_epoch(
                train_X,
                train_y,
                learning_rate=opt.learning_rate
            )
        
        train_accs.append(model.evaluate(train_X, train_y))
        valid_accs.append(model.evaluate(dev_X, dev_y))
        if opt.model == 'mlp':
            print('loss: {} | train acc: {} | val acc: {}'.format(
                loss, train_accs[-1], valid_accs[-1],
            ))
            train_loss.append(loss)
        else:
            print('train acc: {:.4f} | val acc: {:.4f}'.format(
                 train_accs[-1], valid_accs[-1],
            ))
    print('Final test acc: {:.4f}'.format(
        model.evaluate(test_X, test_y)
        ))

    # plot
    plot(epochs, train_accs, valid_accs)
    if opt.model == 'mlp':
        plot_loss(epochs, train_loss)


if __name__ == '__main__':
    main()
