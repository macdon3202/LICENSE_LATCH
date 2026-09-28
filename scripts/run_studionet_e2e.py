"""Run one real npm snapshot-pair assessment and record exact evidence."""
from __future__ import annotations
import json
import os
from pathlib import Path
import time
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

RPC = "https://studio.genlayer.com/api"
EXPLORER = "https://explorer-studio.genlayer.com"


def load_wallet():
    path = Path(__file__).resolve().parents[2] / "secrets" / "genlayer-test-wallets.env"
    for raw in path.read_text(encoding="utf-8").splitlines():
        if "=" in raw and not raw.lstrip().startswith("#"):
            key, value = raw.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\"").strip("<>"))


def plain(value):
    if isinstance(value, dict): return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [plain(v) for v in value]
    return value if isinstance(value, (str, int, float, bool)) or value is None else str(value)


def read(client, address, account, method, args):
    last = None
    for attempt in range(8):
        try: return plain(client.read_contract(address=address, function_name=method, args=args, account=account))
        except Exception as error:
            last = error
            time.sleep(2 + attempt)
    raise last


def signals(info):
    status = str(info.get("status_name") or info.get("status") or "UNKNOWN").upper()
    consensus = str(info.get("result_name") or info.get("consensus_result_name") or info.get("consensus_result") or "UNKNOWN").upper()
    data = info.get("consensus_data") if isinstance(info.get("consensus_data"), dict) else {}
    receipts = data.get("leader_receipt") or data.get("validators") or []
    if isinstance(receipts, dict): receipts = [receipts]
    leader = next((r for r in receipts if isinstance(r, dict) and str(r.get("mode", "")).lower() == "leader"), {})
    execution = str(leader.get("execution_result") or info.get("execution_result") or "UNKNOWN").upper()
    return status, consensus, execution


def main():
    load_wallet()
    address = os.environ.get("LICENSE_LATCH_ADDRESS", "")
    name = os.environ.get("LICENSE_LATCH_PACKAGE", "")
    old = os.environ.get("LICENSE_LATCH_OLD", "")
    new = os.environ.get("LICENSE_LATCH_NEW", "")
    policy = os.environ.get("LICENSE_LATCH_POLICY", "")
    if not all((address, name, old, new, policy)):
        raise SystemExit("Set address, package, old/new versions and policy after reviewing real registry resources")
    account = create_account(os.environ["SERVICE_LEDGER_KEY_A"])
    client = create_client(chain=studionet, account=account, endpoint=RPC)
    before = read(client, address, account, "get_config", [])
    tx = str(client.write_contract(address=address, function_name="assess_upgrade", account=account, args=[name, old, new, policy], value=0))
    print(json.dumps({"submitted": tx}), flush=True)
    receipt = None
    for _ in range(200):
        info = plain(client.get_transaction(tx))
        status, consensus, execution = signals(info)
        if status == "FINALIZED":
            if consensus not in {"MAJORITY_AGREE", "AGREE", "ACCEPTED"} or execution != "SUCCESS":
                raise AssertionError((status, consensus, execution, tx))
            receipt = {"tx": tx, "explorer": f"{EXPLORER}/tx/{tx}", "status": status, "consensus": consensus, "execution": execution}
            break
        time.sleep(3)
    if receipt is None: raise TimeoutError(tx)
    assessment_id = int(read(client, address, account, "get_config", [])["assessment_count"])
    final = read(client, address, account, "get_assessment", [assessment_id])
    print(json.dumps({"contract": address, "before": before, "assessment_id": assessment_id, "fixture": {"package": name, "old": old, "new": new, "policy": policy}, "transaction": receipt, "final": final}, indent=2))


if __name__ == "__main__": main()
