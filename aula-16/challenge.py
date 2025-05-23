#!/usr/bin/env python3
"""
Advanced CI/CD Deployment Automation System
Challenge: Create a comprehensive deployment automation system with rollback capabilities
"""

import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib


class DeploymentStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class HealthCheck:
    """Health check configuration"""
    endpoint: str
    expected_status: int = 200
    timeout: int = 30
    retries: int = 3

    def check(self) -> bool:
        """Simulate health check"""
        # In a real implementation, this would make HTTP requests
        print(f"Checking health at {self.endpoint}")
        time.sleep(0.1)  # Simulate network delay
        return True  # Simplified for demo


@dataclass
class DeploymentConfig:
    """Deployment configuration"""
    application_name: str
    version: str
    environment: Environment
    artifact_url: str
    health_checks: List[HealthCheck]
    rollback_enabled: bool = True
    blue_green: bool = False
    canary_percentage: Optional[int] = None


@dataclass
class DeploymentRecord:
    """Record of a deployment"""
    id: str
    config: DeploymentConfig
    status: DeploymentStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    logs: List[str] = None
    error_message: Optional[str] = None

    def __post_init__(self):
        if self.logs is None:
            self.logs = []

    def add_log(self, message: str):
        """Add a log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(f"[{timestamp}] {message}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "application_name": self.config.application_name,
            "version": self.config.version,
            "environment": self.config.environment.value,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "logs": self.logs,
            "error_message": self.error_message
        }


class DeploymentManager:
    """Manages application deployments with rollback capabilities"""
    
    def __init__(self):
        self.deployments: Dict[str, DeploymentRecord] = {}
        self.environment_versions: Dict[Environment, Dict[str, str]] = {
            env: {} for env in Environment
        }
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger("deployment_manager")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger

    def _generate_deployment_id(self, config: DeploymentConfig) -> str:
        """Generate a unique deployment ID"""
        data = f"{config.application_name}-{config.version}-{config.environment.value}-{datetime.now().isoformat()}"
        return hashlib.md5(data.encode()).hexdigest()[:8]

    def deploy(self, config: DeploymentConfig) -> str:
        """Deploy an application"""
        deployment_id = self._generate_deployment_id(config)
        
        record = DeploymentRecord(
            id=deployment_id,
            config=config,
            status=DeploymentStatus.PENDING,
            start_time=datetime.now()
        )
        
        self.deployments[deployment_id] = record
        record.add_log(f"Starting deployment of {config.application_name} v{config.version}")
        
        try:
            # Update status to in progress
            record.status = DeploymentStatus.IN_PROGRESS
            record.add_log("Deployment in progress...")
            
            # Simulate deployment steps
            self._execute_deployment(record)
            
            # Run health checks
            self._run_health_checks(record)
            
            # Update environment version tracking
            self.environment_versions[config.environment][config.application_name] = config.version
            
            # Mark as successful
            record.status = DeploymentStatus.SUCCESS
            record.end_time = datetime.now()
            record.add_log("Deployment completed successfully")
            
            self.logger.info(f"Deployment {deployment_id} completed successfully")
            
        except Exception as e:
            record.status = DeploymentStatus.FAILED
            record.end_time = datetime.now()
            record.error_message = str(e)
            record.add_log(f"Deployment failed: {e}")
            
            self.logger.error(f"Deployment {deployment_id} failed: {e}")
            
            # Auto-rollback if enabled
            if config.rollback_enabled:
                self._auto_rollback(record)
        
        return deployment_id

    def _execute_deployment(self, record: DeploymentRecord):
        """Execute the deployment steps"""
        config = record.config
        
        # Simulate deployment based on strategy
        if config.blue_green:
            record.add_log("Executing blue-green deployment")
            time.sleep(0.2)  # Simulate blue environment setup
            record.add_log("Blue environment ready, switching traffic")
            time.sleep(0.1)  # Simulate traffic switch
            
        elif config.canary_percentage:
            record.add_log(f"Starting canary deployment with {config.canary_percentage}% traffic")
            time.sleep(0.1)  # Simulate canary deployment
            record.add_log("Canary deployment successful, rolling out to 100%")
            time.sleep(0.1)  # Simulate full rollout
            
        else:
            record.add_log("Executing rolling deployment")
            time.sleep(0.2)  # Simulate rolling deployment
        
        record.add_log("Application deployed successfully")

    def _run_health_checks(self, record: DeploymentRecord):
        """Run health checks after deployment"""
        config = record.config
        record.add_log("Running health checks...")
        
        for i, health_check in enumerate(config.health_checks):
            record.add_log(f"Health check {i+1}: {health_check.endpoint}")
            
            if not health_check.check():
                raise Exception(f"Health check failed for {health_check.endpoint}")
            
            record.add_log(f"Health check {i+1} passed")
        
        record.add_log("All health checks passed")

    def _auto_rollback(self, record: DeploymentRecord):
        """Automatically rollback a failed deployment"""
        config = record.config
        
        # Find previous successful version
        previous_version = self._get_previous_version(config.application_name, config.environment)
        
        if previous_version:
            record.add_log(f"Auto-rolling back to version {previous_version}")
            
            # Create rollback config
            rollback_config = DeploymentConfig(
                application_name=config.application_name,
                version=previous_version,
                environment=config.environment,
                artifact_url=f"rollback://{previous_version}",
                health_checks=config.health_checks,
                rollback_enabled=False  # Prevent recursive rollbacks
            )
            
            # Execute rollback
            rollback_id = self.deploy(rollback_config)
            record.add_log(f"Rollback deployment: {rollback_id}")
            record.status = DeploymentStatus.ROLLED_BACK
        else:
            record.add_log("No previous version found for rollback")

    def _get_previous_version(self, app_name: str, environment: Environment) -> Optional[str]:
        """Get the previous successful version for an application in an environment"""
        # Find the last successful deployment
        successful_deployments = [
            d for d in self.deployments.values()
            if (d.config.application_name == app_name and 
                d.config.environment == environment and 
                d.status == DeploymentStatus.SUCCESS)
        ]
        
        if successful_deployments:
            # Sort by start time and get the latest
            latest = sorted(successful_deployments, key=lambda x: x.start_time)[-1]
            return latest.config.version
        
        return None

    def rollback(self, app_name: str, environment: Environment, target_version: Optional[str] = None) -> str:
        """Manually rollback an application to a previous version"""
        if target_version is None:
            target_version = self._get_previous_version(app_name, environment)
        
        if not target_version:
            raise ValueError("No target version found for rollback")
        
        # Create rollback deployment config
        config = DeploymentConfig(
            application_name=app_name,
            version=target_version,
            environment=environment,
            artifact_url=f"rollback://{target_version}",
            health_checks=[HealthCheck(endpoint=f"http://{app_name}/health")],
            rollback_enabled=False
        )
        
        return self.deploy(config)

    def get_deployment_status(self, deployment_id: str) -> Optional[DeploymentRecord]:
        """Get the status of a deployment"""
        return self.deployments.get(deployment_id)

    def list_deployments(self, app_name: Optional[str] = None, environment: Optional[Environment] = None) -> List[DeploymentRecord]:
        """List deployments with optional filtering"""
        deployments = list(self.deployments.values())
        
        if app_name:
            deployments = [d for d in deployments if d.config.application_name == app_name]
        
        if environment:
            deployments = [d for d in deployments if d.config.environment == environment]
        
        return sorted(deployments, key=lambda x: x.start_time, reverse=True)

    def get_environment_status(self) -> Dict[str, Any]:
        """Get the current status of all environments"""
        return {
            env.value: versions for env, versions in self.environment_versions.items()
        }

    def export_deployment_history(self) -> str:
        """Export deployment history as JSON"""
        history = {
            "deployments": [d.to_dict() for d in self.deployments.values()],
            "environment_versions": {
                env.value: versions for env, versions in self.environment_versions.items()
            },
            "exported_at": datetime.now().isoformat()
        }
        return json.dumps(history, indent=2)


def main():
    """Demonstrate the deployment automation system"""
    manager = DeploymentManager()
    
    print("🚀 Advanced CI/CD Deployment Automation System")
    print("=" * 60)
    
    # Deploy version 1.0.0 to staging
    staging_config = DeploymentConfig(
        application_name="web-app",
        version="1.0.0",
        environment=Environment.STAGING,
        artifact_url="s3://artifacts/web-app-1.0.0.tar.gz",
        health_checks=[
            HealthCheck(endpoint="http://staging.web-app.com/health"),
            HealthCheck(endpoint="http://staging.web-app.com/api/status")
        ]
    )
    
    deployment_id = manager.deploy(staging_config)
    print(f"Staging deployment started: {deployment_id}")
    
    # Deploy version 1.0.0 to production with blue-green
    prod_config = DeploymentConfig(
        application_name="web-app",
        version="1.0.0",
        environment=Environment.PRODUCTION,
        artifact_url="s3://artifacts/web-app-1.0.0.tar.gz",
        health_checks=[
            HealthCheck(endpoint="http://web-app.com/health"),
            HealthCheck(endpoint="http://web-app.com/api/status")
        ],
        blue_green=True
    )
    
    prod_deployment_id = manager.deploy(prod_config)
    print(f"Production deployment started: {prod_deployment_id}")
    
    # Deploy version 1.1.0 with canary
    canary_config = DeploymentConfig(
        application_name="web-app",
        version="1.1.0",
        environment=Environment.PRODUCTION,
        artifact_url="s3://artifacts/web-app-1.1.0.tar.gz",
        health_checks=[
            HealthCheck(endpoint="http://web-app.com/health"),
        ],
        canary_percentage=10
    )
    
    canary_deployment_id = manager.deploy(canary_config)
    print(f"Canary deployment started: {canary_deployment_id}")
    
    # Show deployment status
    print("\n📊 Deployment Status:")
    print("-" * 30)
    for deployment in manager.list_deployments():
        status_emoji = {
            DeploymentStatus.SUCCESS: "✅",
            DeploymentStatus.FAILED: "❌",
            DeploymentStatus.IN_PROGRESS: "⏳",
            DeploymentStatus.PENDING: "⏸️",
            DeploymentStatus.ROLLED_BACK: "🔄"
        }
        emoji = status_emoji.get(deployment.status, "❓")
        print(f"{emoji} {deployment.config.application_name} v{deployment.config.version} "
              f"({deployment.config.environment.value}) - {deployment.status.value}")
    
    # Show environment status
    print("\n🌍 Environment Status:")
    print("-" * 25)
    env_status = manager.get_environment_status()
    for env, apps in env_status.items():
        print(f"{env.title()}:")
        for app, version in apps.items():
            print(f"  └─ {app}: v{version}")
    
    # Demonstrate rollback
    print("\n🔄 Testing Rollback:")
    print("-" * 20)
    try:
        rollback_id = manager.rollback("web-app", Environment.PRODUCTION)
        print(f"Rollback initiated: {rollback_id}")
    except Exception as e:
        print(f"Rollback failed: {e}")
    
    # Export deployment history
    print("\n📁 Exporting Deployment History...")
    history = manager.export_deployment_history()
    with open("/tmp/deployment_history.json", "w") as f:
        f.write(history)
    print("History exported to /tmp/deployment_history.json")


if __name__ == "__main__":
    main()
