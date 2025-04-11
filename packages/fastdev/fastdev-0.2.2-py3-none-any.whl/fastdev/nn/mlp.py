from typing import List, Optional, Type

import torch
import torch.nn as nn


class MLP(nn.Module):
    """A flexible MLP"""

    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        hidden_dims: List[int],
        activation_layer: Optional[Type[nn.Module]] = nn.ReLU,
        activation_on_output: bool = False,
        residual_on_output: bool = False,
        residual_on_hidden: bool = False,
        use_normalization: bool = False,
        normalization_layer: Optional[Type[nn.Module]] = nn.LayerNorm,
    ) -> None:
        super().__init__()
        self.dims = [input_dim] + hidden_dims + [output_dim]
        self.residual_on_hidden = residual_on_hidden
        self.residual_on_output = residual_on_output

        layers = []
        for i in range(len(self.dims) - 1):
            block = [nn.Linear(self.dims[i], self.dims[i + 1])]
            if use_normalization:
                block.append(normalization_layer(self.dims[i + 1]))  # type: ignore
            # Only add activation if it's not the last layer (or if activation_on_output is True).
            if i < len(self.dims) - 2 or activation_on_output:
                if activation_layer is not None:
                    block.append(activation_layer(inplace=True))  # type: ignore
            layers.append(nn.Sequential(*block))
        self.layers = nn.ModuleList(layers)

        # Set up optional output skip connection
        if residual_on_output:
            self.skip_output = nn.Linear(input_dim, output_dim) if input_dim != output_dim else nn.Identity()
        else:
            self.skip_output = None  # type: ignore

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        original_shape = x.shape

        if x.ndim > 2:  # Flatten to 2D if needed (B, ..., D) => (B*..., D)
            x = x.reshape(-1, x.shape[-1])

        x_in = x  # Keep a copy of the original input for output residual
        for i, layer in enumerate(self.layers):
            out = layer(x)
            # Optional residual on hidden layers if matching dims
            if self.residual_on_hidden and self.dims[i] == self.dims[i + 1]:
                out += x
            x = out

        if self.skip_output is not None:  # Optional residual on output
            x += self.skip_output(x_in)

        if x.shape[-1] != original_shape[-1]:  # Reshape back to the original leading dimensions if output_dim changed
            x = x.reshape(original_shape[:-1] + (self.dims[-1],))

        return x


if __name__ == "__main__":
    mlp = MLP(
        input_dim=16,
        output_dim=32,
        hidden_dims=[32, 32],
        activation_layer=nn.SiLU,
        residual_on_hidden=True,
        residual_on_output=True,
        use_normalization=True,
        normalization_layer=nn.BatchNorm1d,
    )
    x = torch.randn(4, 16)
    print(mlp(x).shape)
