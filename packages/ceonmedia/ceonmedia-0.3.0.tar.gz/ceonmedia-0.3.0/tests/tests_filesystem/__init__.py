import pytest

# we want to have pytest assert introspection in the helpers
# Otherwise, only asserts directly inside the currently
# running .py test file will print debug info
# pytest.register_assert_rewrite("ceonstock.tests.serialization")
# pytest.register_assert_rewrite("ceonstock.tests.instantiation")
# pytest.register_assert_rewrite("ceonstock.tests.json_tests")
