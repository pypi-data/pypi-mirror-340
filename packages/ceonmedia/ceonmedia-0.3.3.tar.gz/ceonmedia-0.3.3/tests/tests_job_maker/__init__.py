import pytest

# we want to have pytest assert introspection in the helpers
# Otherwise, only asserts directly inside the currently
# running .py test file will print debug info
# pytest.register_assert_rewrite("ceonmedia.core.tests.serialization")
# pytest.register_assert_rewrite("ceonmedia.core.tests.instantiation")
