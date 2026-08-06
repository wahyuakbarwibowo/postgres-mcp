from server import BLOCKED


def test_guard():
    assert BLOCKED.search("TRUNCATE users")
    assert BLOCKED.search("drop table users")
    assert BLOCKED.search("DROP DATABASE prod")
    assert BLOCKED.search("alter table t drop column c")
    assert not BLOCKED.search("SELECT * FROM users")
    assert not BLOCKED.search("DELETE FROM users WHERE id=1")
    assert not BLOCKED.search("select dropped_at from audit")


if __name__ == "__main__":
    test_guard()
    print("ok")
