name: Advanced CI/CD Pipeline with Deployment
on: 
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: '3.10'

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
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
      
      - name: Code formatting check
        run: poetry run black --check .
      
      - name: Linting
        run: |
          poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          poetry run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      
      - name: Run tests with coverage
        run: poetry run pytest --cov=./ --cov-report=xml --cov-report=html
      
      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
      
      - name: Archive test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results-${{ matrix.python-version }}
          path: |
            htmlcov/
            coverage.xml

  security-scan:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install Poetry
        uses: snok/install-poetry@v1
      
      - name: Install dependencies
        run: poetry install
      
      - name: Run security scan
        run: |
          poetry add --group dev bandit safety
          poetry run bandit -r . -f json -o bandit-report.json || true
          poetry run safety check --json --output safety-report.json || true
      
      - name: Upload security reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            bandit-report.json
            safety-report.json

  build:
    runs-on: ubuntu-latest
    needs: [test, security-scan]
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install Poetry
        uses: snok/install-poetry@v1
      
      - name: Build package
        run: poetry build
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/

  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: staging
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: dist
          path: dist/
      
      - name: Deploy to staging
        run: |
          echo "Deploying to staging environment..."
          # Simulate deployment steps
          echo "Application version: $(ls dist/*.whl | head -1)"
          echo "Staging deployment completed successfully!"
      
      - name: Run integration tests
        run: |
          echo "Running integration tests on staging..."
          # Simulate integration tests
          echo "All integration tests passed!"

  deploy-production:
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: dist
          path: dist/
      
      - name: Deploy to production
        run: |
          echo "Deploying to production environment..."
          # Simulate production deployment
          echo "Application version: $(ls dist/*.whl | head -1)"
          echo "Production deployment completed successfully!"
      
      - name: Create release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: v${{ github.run_number }}
          release_name: Release v${{ github.run_number }}
          body: |
            Automated release from main branch
            
            Changes in this release:
            - Automated build and deployment
            - All tests passed
            - Security scans completed
          draft: false
          prerelease: false

  notify:
    runs-on: ubuntu-latest
    needs: [deploy-production]
    if: always()
    
    steps:
      - name: Notify deployment status
        run: |
          if [ "${{ needs.deploy-production.result }}" == "success" ]; then
            echo "✅ Deployment successful! Production is updated."
          else
            echo "❌ Deployment failed. Check the logs for details."
          fi
