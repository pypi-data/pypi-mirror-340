import jax.numpy as jnp
from flax import nnx
from jaxtyping import Array, Float, Int


class AttentionBlock(nnx.Module):
    """
    LayerNorm1 -> Attention -> Dropout -> Residual -> LayerNorm2 -> FeedForward -> Dropout -> Residual
    """

    def __init__(
        self,
        rng_seed: Int,
        embed_dim: Int,
        hidden_dim: Int,
        qkv_dim: Int,
        num_heads: Int,
        dropout_rate: Float = 0.0,
    ):
        self.attention = nnx.MultiHeadAttention(
            num_heads=num_heads,
            in_features=embed_dim,
            qkv_features=qkv_dim,
            out_features=embed_dim,
            decode=False,
            dropout_rate=dropout_rate,
            rngs=nnx.Rngs(rng_seed),
        )
        self.layer_norm1 = nnx.LayerNorm(
            num_features=embed_dim, rngs=nnx.Rngs(rng_seed + 1)
        )
        self.layer_norm2 = nnx.LayerNorm(
            num_features=embed_dim, rngs=nnx.Rngs(rng_seed + 2)
        )
        self.dropout = nnx.Dropout(dropout_rate, rngs=nnx.Rngs(rng_seed + 3))
        self.linear_block = nnx.Sequential(
            nnx.Linear(embed_dim, hidden_dim, rngs=nnx.Rngs(rng_seed + 4)),
            nnx.gelu,
            nnx.Dropout(dropout_rate, rngs=nnx.Rngs(rng_seed + 5)),
            nnx.Linear(hidden_dim, embed_dim, rngs=nnx.Rngs(rng_seed + 6)),
        )

    def __call__(self, x: Float[Array, "n_token n_embed"]) -> Float[Array, "n_token n_embed"]:
        norm_x = self.layer_norm1(x)
        attention_x = self.attention(norm_x)
        x = x + self.dropout(attention_x)
        linear_out = self.layer_norm2(x)
        return x + self.dropout(self.linear_block(linear_out))


class VisionTransformer(nnx.Module):

    """
    I ommit the class token for generality. It can easily be added back by adding an extra token to the input.
    """

    def __init__(
        self,
        rng_seed: int,
        embed_dim: Int,  # Dimensionality of input and attention feature vectors
        hidden_dim: int,  # Dimensionality of hidden layer in feed-forward network
        num_heads: int,  # Number of heads to use in the Multi-Head Attention block
        num_channels: int,  # Number of channels of the input (3 for RGB)
        num_layers: int,  # Number of layers to use in the Transformer
        patch_size: int,  # Number of pixels that the patches have per dimension
        num_patches: int,  # Maximum number of patches an image can have
        dropout_prob: float = 0.0,  # Amount of dropout to apply in the feed-forward network
    ):
        self.patch_size = patch_size
        self.num_patches = num_patches

        self.linear_projector = nnx.Linear(
            patch_size * patch_size * num_channels, embed_dim, rngs=nnx.Rngs(rng_seed)
        )
        self.attention_blocks = nnx.Sequential(*[
            AttentionBlock(rng_seed + i + 1, embed_dim, hidden_dim, embed_dim, num_heads)
            for i in range(num_layers)
        ])
        self.dropout_block = nnx.Dropout(dropout_prob, rngs=nnx.Rngs(rng_seed + num_layers + 1))
        self.positional_embedding = nnx.Embed(num_embeddings=num_patches, features=embed_dim, rngs=nnx.Rngs(rng_seed + num_layers + 2))

    def __call__(
        self, images: Int[Array, "C H W"], inference: bool = False
    ) -> Float[Array, " C"]:
        x = self.image_to_patch(images)
        x = nnx.vmap(self.linear_projector)(x)
        x = x + self.positional_embedding(jnp.arange(x.shape[0]))
        x = self.dropout_block(x)
        x = self.attention_blocks(x)
        return x

    def image_to_patch(
        self, image: Int[Array, " C H W"]
    ) -> Int[Array, "H*W/P/P P*P*C"]:
        C, H, W = image.shape
        x = image.reshape(C, H//self.patch_size, self.patch_size, W//self.patch_size, self.patch_size)
        x = x.transpose(1, 3, 0, 2, 4)
        return x.reshape(-1, C*self.patch_size*self.patch_size)