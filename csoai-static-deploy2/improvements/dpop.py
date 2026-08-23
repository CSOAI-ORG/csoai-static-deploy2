# DPOP: better than DPO/SimPO (+5.3%)
# Paper: arxiv:2606.12505
def dpop_loss(policy_chosen, policy_rejected, ref_chosen, ref_rejected, beta=0.1, pw=0.5):
    import torch.nn.functional as F
    logratios = (policy_chosen - policy_rejected) - (ref_chosen - ref_rejected)
    dpo_loss = -F.logsigmoid(beta * logratios).mean()
    penalty = F.relu(policy_rejected - policy_chosen).mean()
    return dpo_loss + pw * penalty
