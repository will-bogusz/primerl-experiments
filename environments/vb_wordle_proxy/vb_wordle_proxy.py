import verifiers as vf


def load_environment(**kwargs) -> vf.Environment:
    """
    Proxy loader that returns the canonical Wordle environment.

    Accepts all keyword args and forwards them to the underlying env.
    This lets us publish a namespaced clone while relying on the
    official implementation for behavior and rubric.
    """
    # The upstream env id used by verifiers/vf-eval is "wordle".
    # This requires the "wordle" package to be available at runtime.
    return vf.load_environment("wordle", **kwargs)
