import torch
import torch.nn as nn

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_stacked_layers, prediction_priors):
        super().__init__()
        self.hidden_size = hidden_size
        self.input_size = input_size
        self.num_stacked_layers = num_stacked_layers

        # Updated layers from the provided model
        self.prefc1 = nn.Linear(prediction_priors * input_size, hidden_size // 4)
        self.prefc2 = nn.Linear(hidden_size // 4, hidden_size // 2)
        self.prefc3 = nn.Linear(hidden_size // 2, hidden_size)
        self.fc = nn.Linear(hidden_size, 3)
        self.fcfinal1 = nn.Linear(5 + 3, 16)
        self.fcfinal2 = nn.Linear(16, 1)

        self.relu = nn.LeakyReLU(0.1)
        self.sigm = nn.Sigmoid()

    def forward(self, x, x1):
        batch_size = x.size(0)
        x = torch.reshape(x, (batch_size, 1, -1))
        x1 = x1.float()

        out = self.prefc1(x)
        out = self.relu(out)
        out = self.prefc2(out)
        out = self.relu(out)
        out = self.prefc3(out)
        out = self.relu(out)
        out = torch.squeeze(out, 1)

        out = self.fc(out)
        out = self.relu(out)
        out = self.fcfinal1(torch.cat((out, x1), 1))
        out = self.relu(out)
        out = self.fcfinal2(out)
        return out


class MeanBiasError(nn.Module):
    def __init__(self):
        super(MeanBiasError, self).__init__()

    def forward(self, y_pred, y_true):
        return torch.mean(y_pred - y_true)


def train(model, dataloader, num_epochs, learning_rate):
    lr = learning_rate
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    model.train(True)
    rloss = 0.0

    for epoch in range(1, num_epochs + 1):
        for batch_index, batch in enumerate(dataloader):
            x_batch, y_batch, x1_batch = batch[0], batch[1], batch[2]
            output = model(x_batch, x1_batch)
            loss = loss_function(output, y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            rloss += loss
            if batch_index % 100 == 99:
                avg_loss = rloss / 100
                # print(f'avg_loss: {avg_loss}')
                rloss = 0.0
    return model


def infer(model, x, x1, eval=True):
    if eval:
        x = torch.tensor(x).float().unsqueeze(0)
    else:
        x = torch.tensor(x).float()
    x1 = torch.tensor(x1).float().unsqueeze(0)
    model.train(False)
    out = model(x, x1).detach()
    return out