#!/usr/bin/env python3
"""
CI/CD Pipeline Configuration Builder
Exercise: Create a simple CI/CD pipeline configuration builder
"""

import yaml
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional


@dataclass
class Step:
    """Represents a single step in a CI/CD job"""
    name: str
    run: Optional[str] = None
    uses: Optional[str] = None
    with_params: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"name": self.name}
        if self.run:
            result["run"] = self.run
        if self.uses:
            result["uses"] = self.uses
        if self.with_params:
            result["with"] = self.with_params
        return result


@dataclass
class Job:
    """Represents a CI/CD job"""
    name: str
    runs_on: str = "ubuntu-latest"
    steps: List[Step] = None
    strategy: Optional[Dict[str, Any]] = None
    needs: Optional[List[str]] = None

    def __post_init__(self):
        if self.steps is None:
            self.steps = []

    def add_step(self, step: Step):
        """Add a step to the job"""
        self.steps.append(step)

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "runs-on": self.runs_on,
            "steps": [step.to_dict() for step in self.steps]
        }
        if self.strategy:
            result["strategy"] = self.strategy
        if self.needs:
            result["needs"] = self.needs
        return result


class PipelineBuilder:
    """Builds CI/CD pipeline configurations"""
    
    def __init__(self, name: str):
        self.name = name
        self.triggers = []
        self.jobs = {}
        self.env_vars = {}

    def add_trigger(self, trigger: str, branches: List[str] = None):
        """Add a trigger to the pipeline"""
        if branches:
            self.triggers.append({trigger: {"branches": branches}})
        else:
            self.triggers.append(trigger)

    def add_job(self, job: Job):
        """Add a job to the pipeline"""
        self.jobs[job.name] = job

    def add_env_var(self, key: str, value: str):
        """Add an environment variable"""
        self.env_vars[key] = value

    def create_python_test_job(self, python_versions: List[str] = None) -> Job:
        """Create a standard Python testing job"""
        if python_versions is None:
            python_versions = ['3.8', '3.9', '3.10', '3.11']

        job = Job(
            name="test",
            strategy={
                "matrix": {
                    "python-version": python_versions
                }
            }
        )

        # Add standard Python CI steps
        job.add_step(Step(name="Checkout code", uses="actions/checkout@v4"))
        job.add_step(Step(
            name="Set up Python ${{ matrix.python-version }}",
            uses="actions/setup-python@v4",
            with_params={"python-version": "${{ matrix.python-version }}"}
        ))
        job.add_step(Step(
            name="Install dependencies",
            run="pip install -r requirements.txt"
        ))
        job.add_step(Step(
            name="Run tests",
            run="python -m pytest"
        ))

        return job

    def generate_yaml(self) -> str:
        """Generate the YAML configuration"""
        config = {
            "name": self.name,
            "on": self.triggers,
            "jobs": {name: job.to_dict() for name, job in self.jobs.items()}
        }

        if self.env_vars:
            config["env"] = self.env_vars

        return yaml.dump(config, default_flow_style=False, sort_keys=False)


def main():
    """Demonstrate the pipeline builder"""
    # Create a simple CI pipeline
    pipeline = PipelineBuilder("Simple CI Pipeline")
    
    # Add triggers
    pipeline.add_trigger("push")
    pipeline.add_trigger("pull_request")
    
    # Add environment variables
    pipeline.add_env_var("PYTHON_VERSION", "3.10")
    
    # Create and add a test job
    test_job = pipeline.create_python_test_job()
    pipeline.add_job(test_job)
    
    # Generate and print the YAML
    yaml_config = pipeline.generate_yaml()
    print("Generated CI/CD Pipeline Configuration:")
    print("=" * 50)
    print(yaml_config)
    
    # Create a more complex pipeline with multiple jobs
    complex_pipeline = PipelineBuilder("Complex CI/CD Pipeline")
    complex_pipeline.add_trigger("push", ["main", "develop"])
    complex_pipeline.add_trigger("pull_request", ["main"])
    
    # Test job
    test_job = complex_pipeline.create_python_test_job()
    complex_pipeline.add_job(test_job)
    
    # Build job
    build_job = Job(name="build", needs=["test"])
    build_job.add_step(Step(name="Checkout code", uses="actions/checkout@v4"))
    build_job.add_step(Step(name="Build package", run="python setup.py sdist bdist_wheel"))
    complex_pipeline.add_job(build_job)
    
    # Deploy job
    deploy_job = Job(name="deploy", needs=["build"])
    deploy_job.add_step(Step(name="Deploy to staging", run="echo 'Deploying to staging'"))
    complex_pipeline.add_job(deploy_job)
    
    print("\nComplex Pipeline Configuration:")
    print("=" * 50)
    print(complex_pipeline.generate_yaml())


if __name__ == "__main__":
    main()
