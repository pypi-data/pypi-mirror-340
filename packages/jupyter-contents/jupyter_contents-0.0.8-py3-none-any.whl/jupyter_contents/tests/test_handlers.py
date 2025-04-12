import json

from ..__version__ import __version__


async def test_config(jp_fetch):
    # When
    response = await jp_fetch("jupyter_contents", "config")
    # Then
    assert response.code == 200
    payload = json.loads(response.body)
    assert payload == {
        "extension": "jupyter_contents",
        "version": __version__
    }
