import pytest
from returns.io import IOFailure, IOSuccess
from returns.pipeline import flow, is_successful
from returns.pointfree import alt, apply, bind, lash, map_
from returns.unsafe import unsafe_perform_io


def test_flow():
    # Lambda function deals with IOResult as parameter and return.
    flow_result = flow(
        IOSuccess(1),
        lambda x: IOSuccess(unsafe_perform_io(x.unwrap()) + 1)
        if is_successful(x)
        else x,
    )
    assert flow_result == IOSuccess(2)

    flow_result = flow(
        IOFailure(1),
        lambda x: IOSuccess(unsafe_perform_io(x.unwrap()) + 1)
        if is_successful(x)
        else x,
    )
    assert flow_result == IOFailure(1)

    # When function receives a pure value and returns a Result, we use bind
    flow_result = flow(
        IOSuccess(1),
        bind(lambda x: IOSuccess(x + 1)),
    )
    assert flow_result == IOSuccess(2)

    flow_result = flow(
        IOFailure(1),
        bind(lambda x: IOSuccess(x + 1)),
    )
    assert flow_result == IOFailure(1)

    # Checking flow in case of failure at different points
    flow_result = flow(
        IOSuccess(1),
        bind(lambda x: IOSuccess(x + 1)),
        bind(lambda x: IOSuccess(x + 1)),
    )
    assert flow_result == IOSuccess(3)

    flow_result = flow(
        IOFailure(1),
        bind(lambda x: IOSuccess(x + 1)),
        bind(lambda x: IOSuccess(x + 1)),
    )
    assert flow_result == IOFailure(1)

    flow_result = flow(
        IOSuccess(1),
        bind(lambda x: IOFailure(0)),
        bind(lambda x: IOSuccess(x + 1)),
    )
    assert flow_result == IOFailure(0)

    flow_result = flow(
        IOSuccess(1),
        bind(lambda x: IOSuccess(x + 1)),
        bind(lambda x: IOFailure(0)),
    )
    assert flow_result == IOFailure(0)


def test_recovery_flow():
    # Recovering from a failure
    flow_result = flow(
        IOSuccess(1),
        lash(lambda x: IOSuccess(x - 1)),
        bind(lambda x: IOSuccess(x + 1)),
        bind(lambda x: IOSuccess(x + 1)),
    )
    assert flow_result == IOSuccess(3)

    flow_result = flow(
        IOFailure(1),
        lash(lambda x: IOSuccess(x - 1)),
        bind(lambda x: IOSuccess(x + 1)),
        bind(lambda x: IOSuccess(x + 1)),
    )
    assert flow_result == IOSuccess(2)


def test_flow_mixing_pure_and_results():
    # This works in success pipes but is not right to handle failures
    # "bind" receives a Result and pass pure value to the function, and returns the function value
    flow_result = flow(
        IOSuccess(1),
        bind(lambda x: x + 1),
        lambda x: x + 1,
    )
    assert flow_result == 3

    # But this error happens when the pipe starts with a Failure
    with pytest.raises(TypeError):
        # TypeError: unsupported operand type(s) for +: 'IOFailure' and 'int'
        flow_result = flow(
            IOFailure(1),
            bind(lambda x: x + 1),
            lambda x: x + 1,
        )
        # Because 3rd step is expecting a clean value not a Result, that was passwd by "bind"

    # Here doesn't throw error because failure is skipped by bind and apply
    flow_result = flow(
        IOFailure(0),
        bind(lambda x: x + 1),
        apply(lambda x: x + 1),
    )
    assert flow_result == IOFailure(0)

    # but "apply" was used wrongly, it works in the following way, converts "Container[a -> b]" to: "Container[a] -> Container[b]"
    with pytest.raises(AttributeError):
        # AttributeError: 'int' object has no attribute 'apply'
        flow_result = flow(
            IOSuccess(0),
            bind(lambda x: x + 1),
            apply(lambda x: x + 1),
        )

    # The right way is using "map_" to wrap the pure function, that works for success and failure.
    # From documentation: https://returns.readthedocs.io/en/latest/pages/result.html
    # map vs bind
    # We use the map method when we’re working with pure functions, a function is pure if it doesn’t produce any side-effect (e.g. Exceptions).
    # On the other hand, we use the bind method if a function returns a Result instance which translates its potential side-effect into a raw value.
    flow_result = flow(
        IOSuccess(1),
        map_(lambda x: x + 1),
        bind(lambda x: IOSuccess(x + 1)),
    )
    assert flow_result == IOSuccess(3)

    flow_result = flow(
        IOFailure(0),
        map_(lambda x: x + 1),
        bind(lambda x: IOSuccess(x + 1)),
    )
    assert flow_result == IOFailure(0)

    # This way also work using "apply" but it is weird to read.
    flow_result = flow(
        IOSuccess(1),
        apply(IOSuccess(lambda x: x + 1)),
        bind(lambda x: IOSuccess(x + 1)),
    )
    assert flow_result == IOSuccess(3)

    flow_result = flow(
        IOFailure(0),
        apply(IOSuccess(lambda x: x + 1)),
        bind(lambda x: IOSuccess(x + 1)),
    )
    assert flow_result == IOFailure(0)
