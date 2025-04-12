# Publish to test-pypi
# poetry publish -r test-pypi
uv build && uv publish --username __token__ --password ${PYPI_TOKEN}
