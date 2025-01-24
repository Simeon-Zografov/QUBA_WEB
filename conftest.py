def pytest_collection_modifyitems(config, items):
    for item in items[:]:
        if "only_chrome" in item.keywords:
            # Retrieve the parameter for the test
            params = item.callspec.params if hasattr(item, "callspec") else {}
            if params.get("driver") != "chrome":
                items.remove(item)
