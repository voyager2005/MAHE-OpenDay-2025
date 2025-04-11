import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Initialize weights and biases
        self.w1 = np.random.randn(hidden_size, input_size)
        self.b1 = np.random.randn(hidden_size, 1)
        self.w2 = np.random.randn(output_size, hidden_size)
        self.b2 = np.random.randn(output_size, 1)

    def activate(self, x):
        # Sigmoid activation
        return 1 / (1 + np.exp(-x))

    def forward(self, inputs):
        # Feedforward pass
        inputs = np.array(inputs).reshape(-1, 1)  # column vector
        z1 = np.dot(self.w1, inputs) + self.b1
        a1 = self.activate(z1)
        z2 = np.dot(self.w2, a1) + self.b2
        a2 = self.activate(z2)
        return a2.flatten()

    def mutate(self, rate=0.1):
        # Randomly adjust weights for evolution
        def mutate_matrix(mat):
            mutation = np.random.randn(*mat.shape) * rate
            return mat + mutation

        self.w1 = mutate_matrix(self.w1)
        self.b1 = mutate_matrix(self.b1)
        self.w2 = mutate_matrix(self.w2)
        self.b2 = mutate_matrix(self.b2)

    def clone(self):
        # Make a copy of the brain
        clone = NeuralNetwork(self.w1.shape[1], self.w1.shape[0], self.w2.shape[0])
        clone.w1 = np.copy(self.w1)
        clone.b1 = np.copy(self.b1)
        clone.w2 = np.copy(self.w2)
        clone.b2 = np.copy(self.b2)
        return clone
