# Livekit Voice Technical Agent

A demo of LiveKit's framework for building agents using Cartesia Sonic-3 for voice assistance and Cerebras high-throughput, low-latency AI inference

[Read LiveKit docs on Cerebras](https://docs.livekit.io/agents/integrations/cerebras/).

You can follow the tutorial [here](https://inference-docs.cerebras.ai/cookbook/agents/sales-agent-cerebras-livekit).

## Prerequisites

- Python3
- [LiveKit CLI](https://docs.livekit.io/reference/developer-tools/livekit-cli/)


## Start Development

Activate venv:

```bash
cd livekit-worker
source venv/bin/active
```

## Installing Packages

Make sure you have activated the venv. Then install with pip and update requirements.txt:

```bash
pip install package-name
pip freeze > requirements.txt
```

## Start Worker Agent

```bash
python main.py dev
```

## Create Demo Room

```bash
lk token create \
  --api-key LIVEKIT_API_KEY \
  --api-secret LIVEKIT_API_SECRET \
  --join --room test_room --identity test_user \
  --valid-for 1h
```

## Confirm Room Creation

```bash
lk room list --url LIVEKIT_URL \
  --api-key LIVEKIT_API_KEY \
  --api-secret LIVEKIT_API_SECRET
```

A successful room creation will return a token.

## Enter Demo Room

Go to [LiveKit Meet](https://meet.livekit.io/?tab=custom).

Enter the address WS address from LiveKit cloud account.
Enter the token returned after creating a room.
