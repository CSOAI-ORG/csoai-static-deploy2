# LAMBDA-GRPO: one-line fix to GRPO loss (+12% reasoning)
# Paper: arxiv:2509.21154
def lambda_grpo_loss(old_logps, new_logps, rewards, ref_logps, beta=0.1, lmb=0.5):
    import torch, torch.nn.functional as F
    ratios = (new_logps - old_logps).exp()
    advantages = (rewards - ref_logps * beta)
    surr1 = ratios * advantages
    surr2 = ratios.clamp(1 - 0.2, 1 + 0.2) * advantages
    base_loss = -torch.min(surr1, surr2).mean()
    step_credit = (advantages > 0).float() * lmb
    return base_loss + -(step_credit * new_logps).mean()
