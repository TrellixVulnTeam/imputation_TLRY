
import torch
import torch.nn as nn

class Conv_AE(nn.Module):
    def __init__(self):
        super(Conv_AE ,self).__init__()

        self.Encoder = nn.Sequential(
            nn.Conv1d(1 ,8 ,10 ,3),
            nn.BatchNorm1d(16),
            nn.Tanh(),
            nn.Conv1d(8 ,16 ,10 ,2),
            nn.BatchNorm1d(32),
            nn.Tanh(),
            nn.Conv1d(16 ,32 ,10 ,2),
            nn.BatchNorm1d(64),
            nn.Tanh(),
            nn.Conv1d(32 ,64 ,10 ,2),
            nn.BatchNorm1d(128),
            nn.Tanh(),
            nn.Conv1d(64 ,128 ,10 ,2)
        )

        self.Decoder = nn.Sequential(
            nn.ConvTranspose1d(128 ,64 ,10 ,1),
            nn.BatchNorm1d(128),
            nn.Tanh(),
            nn.ConvTranspose1d(64 ,32 ,10 ,1),
            nn.BatchNorm1d(64),
            nn.Tanh(),
            nn.ConvTranspose1d(32 ,16 ,10 ,1),
            nn.BatchNorm1d(32),
            nn.Tanh(),
            nn.ConvTranspose1d(16 ,8 ,10 ,4 ,output_padding=1),
            nn.BatchNorm1d(16),
            nn.Tanh(),
            nn.ConvTranspose1d(8 ,1 ,10 ,5),
            nn.Tanh()
        )

        self.linear1 = nn.Linear(720,720)


    def encoder(self,x):
        # x = torch.cat([x, mask], dim=1)
        # x = self.linear1(x).view(-1, 1, 720)
        x = self.linear1(x)
        x = x.view(-1,1,720)
        return self.Encoder(x)

    def decoder(self,x):
        x=self.Decoder(x).view(-1, 720)
        x= torch.clamp(x,min=0)
        # x = torch.cat([x,mask],dim=1)
        # x = self.linear1(x)
        return x

    def forward(self ,x):
        x = x.view(-1,1,720)
        encode = self.encoder(x)
        decode = self.decoder(encode)
        return decode.view(-1,720)
