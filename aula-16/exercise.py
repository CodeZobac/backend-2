name: Multi-Version CI Pipeline
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          version: latest
          virtualenvs-create: true
          virtualenvs-in-project: true
      
      - name: Load cached venv
        id: cached-poetry-dependencies
        uses: actions/cache@v3
        with:
          path: .venv
          key: venv-${{ runner.os }}-${{ matrix.python-version }}-${{ hashFiles('**/poetry.lock') }}
      
      - name: Install dependencies
        if: steps.cached-poetry-dependencies.outputs.cache-hit != 'true'
        run: poetry install --no-interaction --no-root
      
      - name: Install project
        run: poetry install --no-interaction
      
      - name: Run linting
        run: |
          poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          poetry run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      
      - name: Run tests with coverage
        run: |
          poetry run pytest --cov=./ --cov-report=xml
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
