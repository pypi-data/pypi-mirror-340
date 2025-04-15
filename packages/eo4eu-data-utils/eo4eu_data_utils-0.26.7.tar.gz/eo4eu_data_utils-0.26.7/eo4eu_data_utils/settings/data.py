def recover_soft_fail(data, e: Exception):
    return data.but(
        passed = [],
        failed = data.failed + data.passed
    )


def recover_raise_exc(data, e: Exception):
    raise e


def recover_continue(data, e: Exception):
    return data
