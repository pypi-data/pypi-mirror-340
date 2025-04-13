# In order to use the PYPI token variable in this script
# it must first be exported in the parent bash process 
# e.g.: export PYPI_TOKEN && ./publish.sh
uv build && uv publish --username __token__ --password ${PYPI_TOKEN}
