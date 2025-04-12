from saved_instance import SimpleStorage, simple_storage


def test_simple_storage_factory():
    ss: SimpleStorage = simple_storage()
    print(ss.get("is_on"))