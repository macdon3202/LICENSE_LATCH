"""Live replay, invalid-input rollback and missing-source audit."""
from __future__ import annotations
import json
import os
from pathlib import Path
import time
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet
from run_studionet_e2e import RPC, EXPLORER, load_wallet, plain, read, signals

ADDRESS = "0x029c5325891c737a8e04a6702aFE284BeD1d672b"


def send(client, account, args, expect_error=False):
    tx = str(client.write_contract(address=ADDRESS, function_name="assess_upgrade", account=account, args=args, value=0))
    print(json.dumps({"submitted": tx}), flush=True)
    for _ in range(200):
        info = plain(client.get_transaction(tx))
        status, consensus, execution = signals(info)
        if status == "FINALIZED":
            success = consensus in {"MAJORITY_AGREE", "AGREE", "ACCEPTED"} and execution == "SUCCESS"
            if success == expect_error:
                raise AssertionError({"tx": tx, "expect_error": expect_error, "consensus": consensus, "execution": execution})
            return {"tx": tx, "explorer": f"{EXPLORER}/tx/{tx}", "status": status, "consensus": consensus, "execution": execution}
        time.sleep(3)
    raise TimeoutError(tx)


def main():
    load_wallet()
    account = create_account(os.environ["SERVICE_LEDGER_KEY_A"])
    client = create_client(chain=studionet, account=account, endpoint=RPC)
    proof = {"contract": ADDRESS, "transactions": [], "readbacks": {}}

    # Exact replay must fail and preserve the full config and assessment.
    before_config = read(client, ADDRESS, account, "get_config", [])
    before_one = read(client, ADDRESS, account, "get_assessment", [1])
    proof["transactions"].append(send(client, account, ["ethers", "6.14.0", "6.15.0", "PERMISSIVE_STANDARD"], expect_error=True))
    assert read(client, ADDRESS, account, "get_config", []) == before_config
    assert read(client, ADDRESS, account, "get_assessment", [1]) == before_one
    proof["readbacks"]["replay_no_mutation"] = before_one

    # Same-version input fails before any external fetch and cannot increment.
    before_same = read(client, ADDRESS, account, "get_config", [])
    proof["transactions"].append(send(client, account, ["ethers", "6.15.0", "6.15.0", "PERMISSIVE_STANDARD"], expect_error=True))
    assert read(client, ADDRESS, account, "get_config", []) == before_same
    proof["readbacks"]["same_version_count_unchanged"] = before_same["assessment_count"]

    # A syntactically valid nonexistent version persists a fail-closed audit
    # result; it must never be converted into a negative licensing accusation.
    missing_version = "0.0.0-license-latch-missing"
    proof["transactions"].append(send(client, account, ["ethers", "6.14.0", missing_version, "PERMISSIVE_STANDARD"]))
    missing_id = int(read(client, ADDRESS, account, "get_config", [])["assessment_count"])
    missing = read(client, ADDRESS, account, "get_assessment", [missing_id])
    assert missing["state"] == "UNRESOLVED" and missing["reason"] == "SOURCE_NOT_VERIFIED"
    proof["readbacks"]["missing_source"] = missing
    proof["result"] = "PASS"
    out = Path(__file__).resolve().parents[1] / "docs" / "studionet-adversarial.json"
    out.write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(proof, indent=2))


if __name__ == "__main__":
    main()
