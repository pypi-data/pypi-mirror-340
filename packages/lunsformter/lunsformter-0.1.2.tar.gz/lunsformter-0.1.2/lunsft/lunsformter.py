import torch
import torch.nn as nn
import torch.nn.functional as F

class OptitationLayer(nn.Module):
    """
    Optimized attention-like layer (Optitation Layer) using PyTorch.
    Uses efficient local windowed attention for linear speed.
    """
    def __init__(self, dim, low_rank_dim=None, window_size=8, device="cpu"):
        super().__init__()
        self.dim = dim
        self.low_rank_dim = low_rank_dim or max(8, dim // 4)
        self.window_size = window_size
        self.Wq = nn.Parameter(torch.randn(dim, self.low_rank_dim) / dim**0.5)
        self.Wk = nn.Parameter(torch.randn(dim, self.low_rank_dim) / dim**0.5)
        self.Wv = nn.Parameter(torch.randn(dim, self.low_rank_dim) / dim**0.5)
        self.Wo = nn.Parameter(torch.randn(self.low_rank_dim, dim) / self.low_rank_dim**0.5)
        self.bq = nn.Parameter(torch.zeros(self.low_rank_dim))
        self.bk = nn.Parameter(torch.zeros(self.low_rank_dim))
        self.bv = nn.Parameter(torch.zeros(self.low_rank_dim))
        self.bo = nn.Parameter(torch.zeros(dim))
        self.device = device

    def forward(self, x):
        # x: (seq_len, dim)
        Q = x @ self.Wq + self.bq
        K = x @ self.Wk + self.bk
        V = x @ self.Wv + self.bv
        seq_len = x.shape[0]
        window = self.window_size
        out = torch.zeros_like(x)
        for i in range(seq_len):
            start = max(0, i - window)
            Qi = Q[i:i+1]  # (1, low_rank_dim)
            Ki = K[start:i+1]  # (w, low_rank_dim)
            Vi = V[start:i+1]  # (w, low_rank_dim)
            attn_scores = Qi @ Ki.T / (self.low_rank_dim ** 0.5)  # (1, w)
            attn_weights = torch.softmax(attn_scores, dim=-1)
            attn_out = attn_weights @ Vi  # (1, low_rank_dim)
            out[i] = attn_out @ self.Wo + self.bo
        return out

class Lunsformter(nn.Module):
    def __init__(self, vocab_size=50, seq_len=10, dim=64, hidden_dim=128, num_layers=2, chunk_size=5, use_optitation=True, device="cpu"):
        super().__init__()
        self.vocab_size = vocab_size
        self.seq_len = seq_len
        self.dim = dim
        self.chunk_size = chunk_size
        self.use_optitation = use_optitation
        self.device = device

        self.embeddings = nn.Parameter(torch.randn(vocab_size, dim) * 0.01)
        self.positional = nn.Parameter(torch.randn(seq_len, dim) * 0.01)

        self.layers = nn.ModuleList()
        self.optitation_layers = nn.ModuleList()
        for _ in range(num_layers):
            W_g = nn.Parameter(torch.randn(dim, dim) / dim**0.5)
            b_g = nn.Parameter(torch.zeros(dim))
            W_s = nn.Parameter(torch.randn(dim, hidden_dim) / dim**0.5)
            b_s = nn.Parameter(torch.zeros(hidden_dim))
            W_o = nn.Parameter(torch.randn(hidden_dim, dim) / hidden_dim**0.5)
            b_o = nn.Parameter(torch.zeros(dim))
            self.layers.append(nn.ParameterList([W_g, b_g, W_s, b_s, W_o, b_o]))
            self.optitation_layers.append(OptitationLayer(dim, device=device))

        self.output_W = nn.Parameter(torch.randn(dim, vocab_size) / dim**0.5)
        self.output_b = nn.Parameter(torch.zeros(vocab_size))

    def _lensed_gate(self, x, W_g, b_g):
        gate = torch.sigmoid(x @ W_g + b_g)
        return x * gate

    def _context_sculpt(self, x, W_s, b_s, W_o, b_o):
        sculpted = torch.tanh(x @ W_s + b_s)
        out = sculpted @ W_o + b_o
        return out

    def _chunk_link_update(self, x):
        seq_len, dim = x.shape
        rem = seq_len % self.chunk_size
        if rem != 0:
            pad_len = self.chunk_size - rem
            pad = torch.zeros((pad_len, dim), dtype=x.dtype, device=x.device)
            x_padded = torch.cat([x, pad], dim=0)
        else:
            x_padded = x

        chunks = x_padded.view(-1, self.chunk_size, self.dim)

        new_chunks = []
        for i, c in enumerate(chunks):
            neighbor_sum = c.clone()
            if i > 0:
                neighbor_sum += chunks[i-1] * 0.5
            if i < len(chunks) - 1:
                neighbor_sum += chunks[i+1] * 0.5
            updated = neighbor_sum / (1 + 0.5 * (i > 0) + 0.5 * (i < len(chunks) -1))
            new_chunks.append(updated)

        updated_x = torch.cat(new_chunks, dim=0)
        return updated_x[:seq_len]

    def forward(self, idx_seq):
        idx_seq = torch.as_tensor(idx_seq, dtype=torch.long, device=self.device)
        seq_len_in = idx_seq.shape[0]
        if seq_len_in > self.positional.shape[0]:
            extra_needed = seq_len_in - self.positional.shape[0]
            extra_pos = torch.randn(extra_needed, self.dim, device=self.device) * 0.01
            pos_embeds = torch.cat([self.positional, extra_pos], dim=0)
        else:
            pos_embeds = self.positional

        x = self.embeddings[idx_seq] + pos_embeds[:seq_len_in]

        for pos in range(1, x.shape[0]):
            decay = 0.8 ** pos
            x[pos] += decay * x[0]

        for i, layer in enumerate(self.layers):
            W_g, b_g, W_s, b_s, W_o, b_o = layer
            residual = x
            x = self._lensed_gate(x, W_g, b_g)
            x = self._context_sculpt(x, W_s, b_s, W_o, b_o)
            x += residual
            if self.use_optitation:
                x = x + self.optitation_layers[i](x)
            x = self._chunk_link_update(x)

        logits = x @ self.output_W + self.output_b
        return logits

    def generate(self, prefix, max_tokens=20, temperature=1.0, return_scores=False):
        device = self.device
        idx_seq = torch.tensor(prefix, dtype=torch.long, device=device)
        prob_scores = []
        for _ in range(max_tokens):
            logits = self.forward(idx_seq[-self.seq_len:])
            logits = logits[-1] / max(temperature, 1e-8)
            probs = torch.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, 1).item()
            prob_scores.append(probs[next_token].item())
            idx_seq = torch.cat([idx_seq, torch.tensor([next_token], device=device)])
        idx_seq_np = idx_seq.cpu().numpy()
        if return_scores:
            return idx_seq_np, prob_scores
        else:
            return idx_seq_np

    def insideout_generate(self, prefix, max_tokens=20, num_candidates=5, penalize_repeats=True, verbose=False, temperature=1.0, return_scores=False):
        device = self.device
        idx_seq = torch.tensor(prefix, dtype=torch.long, device=device)

        logits = self.forward(idx_seq[-self.seq_len:])
        logits = logits[-1] / max(temperature, 1e-8)
        start_probs = torch.softmax(logits, dim=-1)
        top_tokens = torch.topk(start_probs, num_candidates).indices.cpu().numpy()

        if verbose:
            print(f"[InsideOut] Top {num_candidates} initial tokens to try: {top_tokens}")

        best_seq = None
        best_score = -float("inf")
        best_scores_list = None

        for candidate_idx, start in enumerate(top_tokens):
            candidate_seq = torch.cat([idx_seq, torch.tensor([start], device=device)])
            scores = [start_probs[start].item()]

            if verbose:
                print(f"\n[InsideOut] Candidate {candidate_idx +1}/{len(top_tokens)} starting token {start}")

            for step in range(max_tokens - 1):
                logits_cand = self.forward(candidate_seq[-self.seq_len:])
                logits_cand = logits_cand[-1] / max(temperature, 1e-8)
                next_probs = torch.softmax(logits_cand, dim=-1)
                next_token = torch.multinomial(next_probs, 1).item()

                repeat_penalty = 0.5 if penalize_repeats and next_token in candidate_seq.cpu().numpy() else 1.0
                prob_score = next_probs[next_token].item() * repeat_penalty
                scores.append(prob_score)

                candidate_seq = torch.cat([candidate_seq, torch.tensor([next_token], device=device)])

                if verbose:
                    print(f"  Step {step +1}/{max_tokens-1} token: {next_token}, prob_score: {prob_score:.4f}")

            avg_score = sum(scores) / len(scores)
            if verbose:
                print(f"  Candidate avg score: {avg_score:.4f}")

            if avg_score > best_score:
                best_score = avg_score
                best_seq = candidate_seq
                best_scores_list = list(scores)
                if verbose:
                    print(f"  --> New best sequence found with score {best_score:.4f}")

        if verbose:
            print(f"\n[InsideOut] Best overall avg score: {best_score:.4f}")

        best_seq_np = best_seq.cpu().numpy() if best_seq is not None else None
        if return_scores:
            return best_seq_np, best_scores_list
        else:
            return best_seq_np

if __name__ == "__main__":
    model = Lunsformter()
    prefix = [1, 2, 3]

    generated = model.generate(prefix, max_tokens=10)
    print("Generated Token IDs (standard generate):", generated)

    print("\nStarting verbose insideout_generate...")
    insideout_verbose = model.insideout_generate(prefix, max_tokens=10, num_candidates=3, verbose=True)
    print("InsideOut Generated Token IDs (verbose):", insideout_verbose)

    print("\nInsideout_generate without verbose...")
    insideout_silent = model.insideout_generate(prefix, max_tokens=10, num_candidates=3, verbose=False)
    print("InsideOut Generated Token IDs (silent):", insideout_silent)
