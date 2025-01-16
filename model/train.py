from utils import *
from data.loader import loader
from model.rbm import RBM


class RBMTrainer:
    def __init__(self, v_size=15, v0_size=12, h_size=6, lr=0.01):
        self.a, self.b, self.J = initialize_weights(v_size, h_size)
        self.v_size = v_size
        self.v0_size = v0_size
        self.h_size = h_size
        self.lr = lr

    def train_rbm(self, file_path, epochs=2000):
        # Load the dataset
        features, labels = loader(file_path)

        # Initialize the RBM instance with current parameters
        rbm = RBM(self.a, self.b, self.J, self.v_size, self.v0_size, self.h_size)

        # Training loop
        for i in range(epochs):
            for feature, label in zip(features, labels):
                v_true = np.concatenate((label, feature), axis=0)
                prob = activation_prob(v_true, self.J.T, self.b, T=1)
                v, h = rbm.contrastive_divergence_step(v_true)

                # Update parameters
                self.a += self.lr * (v_true - v)
                self.b += self.lr * (prob - h)
                self.J += self.lr * (np.outer(v_true, prob) - np.outer(v, h))

            # Update the RBM instance with the new parameters
            rbm.update_parameters(self.a, self.b, self.J)

            # Calculate and print accuracy
            if (i + 1) % 100 == 0 or i == epochs - 1:
                print(f'Epoch: {i + 1}')

        return self.a, self.b, self.J
