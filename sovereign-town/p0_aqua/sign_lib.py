#!/usr/bin/env python3
"""
Ed25519 attestation for Sovereign Town episodes (the proofof.ai signing primitive).

Asymmetric: episodes are signed with a private key, verifiable by ANYONE holding only the public
key — no server, no shared secret (EU AI Act Art-12 record-keeping / Art-14 oversight evidence).
Honest: real Ed25519 if `cryptography` is present; else raises (never fabricates a signature).

Security note:
  The private key is stored in `.town_priv.key` (gitignored). When the environment variable
  `SOV_TOWN_KEY_PASSWORD` is set, the key is encrypted at rest using Fernet derived from the
  password via PBKDF2-HMAC-SHA256. Without a password the key is stored as raw base64 and a
  warning is logged.
"""
import os, base64, json, logging
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

OUT = os.path.dirname(os.path.abspath(__file__))
PRIV = os.path.join(OUT, ".town_priv.key")     # gitignored
BAK  = os.path.join(OUT, ".town_priv.key.bak") # gitignored on-disk backup (survives a wiped PRIV)
PUB  = os.path.join(OUT, "town_pub.key")        # publishable verifier key

logger = logging.getLogger(__name__)


def _truthy(v) -> bool:
    return str(v).strip().lower() in ("1", "true", "yes", "on")


def _raw(k, kind):
    if kind == "priv":
        return k.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw,
                               serialization.NoEncryption())
    return k.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)


def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def _is_encrypted(blob: str) -> bool:
    try:
        data = json.loads(blob)
        return isinstance(data, dict) and "salt" in data and "token" in data
    except (json.JSONDecodeError, ValueError):
        return False


def _decrypt(blob: str, password: str) -> bytes:
    data = json.loads(blob)
    salt = base64.b64decode(data["salt"])
    token = base64.b64decode(data["token"])
    return Fernet(_derive_key(password, salt)).decrypt(token)


def _encrypt(raw: bytes, password: str) -> str:
    salt = os.urandom(16)
    token = Fernet(_derive_key(password, salt)).encrypt(raw)
    return json.dumps({
        "salt": base64.b64encode(salt).decode(),
        "token": base64.b64encode(token).decode(),
    })


def _decode_blob(blob: str, password: str | None) -> bytes:
    """Return the raw private-key bytes from an on-disk blob (encrypted or plaintext)."""
    if _is_encrypted(blob):
        if not password:
            raise RuntimeError("Private key is encrypted but SOV_TOWN_KEY_PASSWORD is not set")
        return _decrypt(blob, password)
    return base64.b64decode(blob)


def _write_priv(path: str, raw: bytes, password: str | None) -> None:
    with open(path, "w") as f:
        f.write(_encrypt(raw, password) if password else base64.b64encode(raw).decode())
    os.chmod(path, 0o600)


def load_or_create_key(password: str | None = None, allow_rotate: bool | None = None):
    """Load an existing Ed25519 keypair, or generate one only when it is safe to do so.

    Key-continuity guarantees (an attestation key must never silently change — a new key
    orphans every previously signed cycle, exactly the gap seen in ledger cycles 1-30):

      * If `.town_priv.key` is missing but the `.town_priv.key.bak` backup exists, the key is
        transparently restored from the backup (the common "file got wiped on redeploy" case).
      * If BOTH the private key and its backup are gone but a published `town_pub.key` already
        exists, this RAISES instead of minting a new identity — restore the key from your secret
        store, or set `SOV_TOWN_ALLOW_ROTATE=1` to deliberately start a new identity.
      * The published `town_pub.key` is never silently overwritten: if the loaded private key
        does not match an existing `town_pub.key`, this RAISES (unless rotation is allowed).
      * A 0600 `.town_priv.key.bak` is refreshed on every successful load/create.

    If `SOV_TOWN_KEY_PASSWORD` is set, the private key is encrypted at rest; an existing
    plaintext key is re-encrypted the first time a password is supplied.
    """
    if password is None:
        password = os.environ.get("SOV_TOWN_KEY_PASSWORD")
    if allow_rotate is None:
        allow_rotate = _truthy(os.environ.get("SOV_TOWN_ALLOW_ROTATE", ""))

    src = PRIV if os.path.exists(PRIV) else (BAK if os.path.exists(BAK) else None)

    if src is not None:
        with open(src, "r") as f:
            blob = f.read().strip()
        raw = _decode_blob(blob, password)
        priv = Ed25519PrivateKey.from_private_bytes(raw)
        if src == BAK:
            logger.warning("Private key %s was missing — restored from backup %s",
                           os.path.basename(PRIV), os.path.basename(BAK))
            _write_priv(PRIV, raw, password)
        elif not _is_encrypted(blob) and password:
            _write_priv(PRIV, raw, password)      # re-encrypt plaintext now a password exists
            logger.info("Re-encrypted plaintext private key with SOV_TOWN_KEY_PASSWORD")
        elif not _is_encrypted(blob):
            logger.warning("Ed25519 private key is stored unencrypted. Set "
                           "SOV_TOWN_KEY_PASSWORD to encrypt it at rest.")
    elif os.path.exists(PUB) and not allow_rotate:
        raise RuntimeError(
            f"Refusing to rotate the town signing key: a published identity exists "
            f"({os.path.basename(PUB)}) but both {os.path.basename(PRIV)} and its backup are "
            f"missing. Generating a new key would orphan every previously signed cycle. "
            f"Restore the private key from your secret store, or set SOV_TOWN_ALLOW_ROTATE=1 "
            f"to deliberately begin a new identity.")
    else:
        if not password:
            logger.warning("Generating a new unencrypted Ed25519 private key. Set "
                           "SOV_TOWN_KEY_PASSWORD to encrypt it at rest.")
        priv = Ed25519PrivateKey.generate()
        raw = _raw(priv, "priv")
        _write_priv(PRIV, raw, password)

    pub_b64 = base64.b64encode(_raw(priv.public_key(), "pub")).decode()
    if os.path.exists(PUB):
        existing = open(PUB).read().strip()
        if existing and existing != pub_b64 and not allow_rotate:
            raise RuntimeError(
                f"Loaded private key does not match the published {os.path.basename(PUB)}. "
                f"Refusing to overwrite the public verifier key (prior signatures would stop "
                f"verifying). Set SOV_TOWN_ALLOW_ROTATE=1 to intentionally publish a new key.")
        if existing != pub_b64:
            logger.warning("Rotating published %s (SOV_TOWN_ALLOW_ROTATE set)", os.path.basename(PUB))
    with open(PUB, "w") as f:
        f.write(pub_b64)
    try:
        os.chmod(PUB, 0o644)
    except OSError:
        pass

    _write_priv(BAK, _raw(priv, "priv"), password)    # refresh on-disk backup
    return priv, pub_b64


def sign(priv, message: str) -> str:
    return base64.b64encode(priv.sign(message.encode())).decode()


def verify(pub_b64: str, message: str, sig_b64: str) -> bool:
    try:
        Ed25519PublicKey.from_public_bytes(base64.b64decode(pub_b64)).verify(
            base64.b64decode(sig_b64), message.encode())
        return True
    except Exception:
        return False
