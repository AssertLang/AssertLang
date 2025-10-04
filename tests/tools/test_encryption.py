from tools.encryption.adapters import adapter_py


def test_encryption_hash():
    res = adapter_py.handle({"op": "hash", "alg": "sha256", "data": "abc"})
    assert res["ok"] is True
    assert (
        res["data"]["result"] == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )
