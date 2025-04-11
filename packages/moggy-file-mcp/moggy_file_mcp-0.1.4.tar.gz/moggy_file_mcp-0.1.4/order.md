### test.pypi

pypi-AgENdGVzdC5weXBpLm9yZwIkODU2MDJhZDYtMDE1Ni00MzJkLWEyNGEtMzMxYjJlNmVkNjkwAAIqWzMsIjAwZjMzNGMxLTJhYjMtNGE5YS1hYmQxLTJkMWYxMmRjYmY5ZCJdAAAGIG3PmXWcGGid7JP61_NSaoIDgq2HD6y_wV02Dl80QFZj


pypi-AgEIcHlwaS5vcmcCJDZmZGVjMjEwLWUxZjctNGQ3Yy05ZGIyLTU3NjRkZDIxZWY1MwACKlszLCI3MWNiZmI1Yy03YzExLTRkYjgtYjA3Ny0xNGYyNWYwNThhNWMiXQAABiC6HCvlXFVf8CYECYr4ilTJ-VUtPrJF7UzBZKcF2bgwgA

### test.pypi

twine upload dist/*
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

testpypi: pip install --index-url https://test.pypi.org/simple/ moggy-file-mcp
pypi: pip install --index-url https://pypi.org/simple/ moggy-file-mcp




