import numpy as np


class RawDecoder():
    def __init__(self, n_output_channels) -> None:
        self.n_output_channels = n_output_channels

    def decode(self, clip):
        return clip[:, :self.n_output_channels]


class UHJDecoder(RawDecoder):
    def __init__(self, n_output_channels, channel_format='ACN') -> None:
        super().__init__(n_output_channels)
        self.channel_format = channel_format

    def decode(self, clip):
        # clip = clip[:, :4]
        clip = np.fft.fft(clip.T)

        if self.channel_format == 'ACN': W, Y, _, X = clip
        elif self.channel_format == 'FuMa': W, X, Y, _ = clip

        S = 0.9396926*W + 0.1855740*X
        D = 1j * (-0.3420201*W + 0.5098604*X) + 0.6554516*Y

        L = np.fft.ifft(((S + D)/2.0))
        R = np.fft.ifft(((S - D)/2.0))

        L = np.expand_dims(np.real(L), 1)
        R = np.expand_dims(np.real(R), 1)

        clip = np.concatenate((L, R), 1)

        # passing through super makes sure output channel count is correct
        return super().decode(clip)
