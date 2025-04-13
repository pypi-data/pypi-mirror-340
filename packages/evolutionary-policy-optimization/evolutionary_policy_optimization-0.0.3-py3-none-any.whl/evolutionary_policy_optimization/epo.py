from __future__ import annotations

import torch
from torch import nn, cat
import torch.nn.functional as F

import torch.nn.functional as F
from torch.nn import Linear, Module, ModuleList

from einops import rearrange, repeat

# helpers

def exists(v):
    return v is not None

def default(v, d):
    return v if exists(v) else d

def identity(t):
    return t

def xnor(x, y):
    return not (x ^ y)

def l2norm(t):
    return F.normalize(t, p = 2, dim = -1)

# tensor helpers

def log(t, eps = 1e-20):
    return t.clamp(min = eps).log()

def calc_entropy(logits):
    prob = logits.softmax(dim = -1)
    return -prob * log(prob)

def gather_log_prob(
    logits, # Float[b l]
    indices # Int[b]
): # Float[b]
    indices = rearrange(indices, '... -> ... 1')
    log_probs = logits.log_softmax(dim = -1)
    log_prob = log_probs.gather(-1, indices)
    return rearrange(log_prob, '... 1 -> ...')

# reinforcement learning related - ppo

def actor_loss(
    logits,         # Float[b l]
    old_log_probs,  # Float[b]
    actions,        # Int[b]
    advantages,     # Float[b]
    eps_clip = 0.2,
    entropy_weight = .01,
):
    log_probs = gather_log_prob(logits, actions)

    entropy = calc_entropy(logits)

    ratio = (log_probs - old_log_probs).exp()

    clipped_ratio = ratio.clamp(min = 1. - eps_clip, max = 1. + eps_clip)

    # classic clipped surrogate loss from ppo

    actor_loss = -torch.min(clipped_ratio * advantage, ratio * advantage)

    # add entropy loss for exploration

    entropy_aux_loss = -entropy_weight * entropy

    return actor_loss + entropy_aux_loss

def critic_loss(
    pred_values,  # Float[b]
    advantages,   # Float[b]
    old_values    # Float[b]
):
    discounted_values = advantages + old_values
    return F.mse_loss(pred_values, discounted_values)

# evolution related functions

def crossover_latents(
    parent1, parent2,
    weight = None,
    random = False,
    l2norm_output = False
):
    assert parent1.shape == parent2.shape

    if random:
        assert not exists(weight)
        weight = torch.randn_like(parent1).sigmoid()
    else:
        weight = default(weight, 0.5) # they do a simple averaging for the latents as crossover, but allow for random interpolation, as well extend this work for tournament selection, where same set of parents may be re-selected

    child = torch.lerp(parent1, parent2, weight)

    if not l2norm_output:
        return child

    return l2norm(child)

def mutation(
    latents,
    mutation_strength = 1.,
    l2norm_output = False
):
    mutations = torch.randn_like(latents)

    mutated = latents + mutations * mutation_strength

    if not l2norm_output:
        return mutated

    return l2norm(mutated)

# simple MLP networks, but with latent variables
# the latent variables are the "genes" with the rest of the network as the scaffold for "gene expression" - as suggested in the paper

class MLP(Module):
    def __init__(
        self,
        dims: tuple[int, ...],
        dim_latent = 0,
    ):
        super().__init__()
        assert len(dims) >= 2, 'must have at least two dimensions'

        # add the latent to the first dim

        first_dim, *rest_dims = dims
        first_dim += dim_latent
        dims = (first_dim, *rest_dims)

        self.dim_latent = dim_latent
        self.needs_latent = dim_latent > 0

        self.encode_latent = nn.Sequential(
            Linear(dim_latent, dim_latent),
            nn.SiLU()
        ) if self.needs_latent else None

        # pairs of dimension

        dim_pairs = tuple(zip(dims[:-1], dims[1:]))

        # modules across layers

        layers = ModuleList([Linear(dim_in, dim_out) for dim_in, dim_out in dim_pairs])

        self.layers = layers

    def forward(
        self,
        x,
        latent = None
    ):
        assert xnor(self.needs_latent, exists(latent))

        if exists(latent):
            # start with naive concatenative conditioning
            # but will also offer some alternatives once a spark is seen (film, adaptive linear from stylegan, etc)

            batch = x.shape[0]

            latent = self.encode_latent(latent)
            latent = repeat(latent, 'd -> b d', b = batch)

            x = cat((x, latent), dim = -1)

        # layers

        for ind, layer in enumerate(self.layers, start = 1):
            is_last = ind == len(self.layers)

            x = layer(x)

            if not is_last:
                x = F.silu(x)

        return x

# classes

class LatentGenePool(Module):
    def __init__(
        self,
        num_latents,                     # same as gene pool size
        dim_latent,                      # gene dimension
        crossover_random = True,         # random interp from parent1 to parent2 for crossover, set to `False` for averaging (0.5 constant value)
        l2norm_latent = False,           # whether to enforce latents on hypersphere,
        frac_tournaments = 0.25,         # fraction of genes to participate in tournament - the lower the value, the more chance a less fit gene could be selected
        frac_natural_selected = 0.25,    # number of least fit genes to remove from the pool
        frac_elitism = 0.1,              # frac of population to preserve from being noised
        mutation_strength = 1.,          # factor to multiply to gaussian noise as mutation to latents
        net: MLP | Module | dict | None = None,
    ):
        super().__init__()

        maybe_l2norm = l2norm if l2norm_latent else identity

        latents = torch.randn(num_latents, dim_latent)

        if l2norm_latent:
            latents = maybe_l2norm(latents, dim = -1)

        self.num_latents = num_latents
        self.latents = nn.Parameter(latents, requires_grad = False)

        self.maybe_l2norm = maybe_l2norm

        # some derived values

        assert 0. < frac_tournaments < 1.
        assert 0. < frac_natural_selected < 1.
        assert 0. <= frac_elitism < 1.
        assert (frac_natural_selected + frac_elitism) < 1.

        self.dim_latent = dim_latent
        self.num_latents = num_latents
        self.num_natural_selected = int(frac_natural_selected * num_latents)

        self.num_tournament_participants = int(frac_tournaments * self.num_natural_selected)
        self.crossover_random  = crossover_random

        self.mutation_strength = mutation_strength
        self.num_elites = int(frac_elitism * num_latents)
        self.has_elites = self.num_elites > 0

        # network for the latent / gene

        if isinstance(net, dict):
            net = MLP(**net)

        assert net.dim_latent == dim_latent, f'the latent dimension set on the MLP {net.dim_latent} must be what was passed into the latent gene pool module ({dim_latent})'
        self.net = net

    @torch.no_grad()
    # non-gradient optimization, at least, not on the individual level (taken care of by rl component)
    def genetic_algorithm_step(
        self,
        fitness, # Float['p'],
        inplace = True
    ):
        """
        p - population
        g - gene dimension
        """
        assert self.num_latents > 1

        genes = self.latents # the latents are the genes

        pop_size = genes.shape[0]
        assert pop_size == fitness.shape[0]

        # 1. natural selection is simple in silico
        # you sort the population by the fitness and slice off the least fit end

        sorted_indices = fitness.sort().indices
        natural_selected_indices = sorted_indices[-self.num_natural_selected:]
        genes, fitness = genes[natural_selected_indices], fitness[natural_selected_indices]

        # 2. for finding pairs of parents to replete gene pool, we will go with the popular tournament strategy

        batch_randperm = torch.randn((pop_size - self.num_natural_selected, self.num_tournament_participants)).argsort(dim = -1)

        participants = genes[batch_randperm]
        participant_fitness = fitness[batch_randperm]

        tournament_winner_indices = participant_fitness.topk(2, dim = -1).indices

        tournament_winner_indices = repeat(tournament_winner_indices, '... -> ... g', g = self.dim_latent)

        parents = participants.gather(-2, tournament_winner_indices)

        # 3. do a crossover of the parents - in their case they went for a simple averaging, but since we are doing tournament style and the same pair of parents may be re-selected, lets make it random interpolation

        parent1, parent2 = parents.unbind(dim = 1)
        children = crossover_latents(parent1, parent2, random = self.crossover_random)

        # append children to gene pool

        genes = cat((children, genes))

        # 4. they use the elitism strategy to protect best performing genes from being changed

        if self.has_elites:
            genes, elites = genes[:-self.num_elites], genes[-self.num_elites:]

        # 5. mutate with gaussian noise - todo: add drawing the mutation rate from exponential distribution, from the fast genetic algorithms paper from 2017

        genes = mutation(genes, mutation_strength = self.mutation_strength)

        # add back the elites

        if self.has_elites:
            genes = cat((genes, elites))

        genes = self.maybe_l2norm(genes)

        if not inplace:
            return genes

        # store the genes for the next interaction with environment for new fitness values (a function of reward and other to be researched measures)

        self.latents.copy_(genes)

    def forward(
        self,
        *args,
        latent_id: int | None = None,
        **kwargs,
    ):

        assert exists(self.net)

        # if only 1 latent, assume doing ablation and get lone gene

        if not exists(latent_id) and self.num_latents == 1:
            latent_id = 0

        assert 0 <= latent_id < self.num_latents

        # fetch latent

        latent = self.latents[latent_id]

        return self.net(
            *args,
            latent = latent,
            **kwargs
        )
