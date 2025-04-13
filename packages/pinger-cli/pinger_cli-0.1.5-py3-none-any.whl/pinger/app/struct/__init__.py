import subprocess
import platform
import shutil
import base64
import boto3


class App:
    _compose = None

    @classmethod
    def compose(cls, setting=None):
        if cls._compose is None:
            if setting is None:
                cls._compose = "docker-compose"
            else:
                cls._compose = setting
        return cls._compose

    _docker = None

    @classmethod
    def docker(cls, setting=None):
        if cls._docker is None:
            if setting is None:
                cls._docker = "docker"
            else:
                cls._docker = setting
        return cls._docker

    _name = None

    @classmethod
    def name(cls, setting=None):
        if cls._name is None:
            if not setting is None:
                cls._name = setting
        return cls._name

    @classmethod
    def sh(cls, command: str):
        """Run a shell command with error checking."""
        subprocess.run(command, shell=True, check=True)

    @classmethod
    def install_poetry(cls):
        """Install Poetry non-interactively if it's not present."""
        if shutil.which("poetry"):
            print("Poetry is already installed.")
            return

        print("Poetry not found. Installing Poetry...")
        if platform.system() == "Windows":
            powershell_cmd = (
                "(Invoke-WebRequest -Uri https://install.python-poetry.org "
                "-UseBasicParsing | python -)"
            )
            cls.sh(f'powershell -Command "{powershell_cmd}"')
        else:
            cls.sh("curl -sSL https://install.python-poetry.org | python3 -")

        print("Poetry installed successfully!")

    @classmethod
    def poetry_install(cls):
        """Run 'poetry install' non-interactively."""
        if not shutil.which("poetry"):
            print("Poetry is not installed. Please install it first.")
            raise RuntimeError("Poetry not found.")

        print("Installing project dependencies with Poetry...")
        cls.sh("poetry install --no-interaction")
        print("Poetry dependencies installed successfully!")

    @classmethod
    def get_system(cls) -> str:
        """Returns the correct Nix system identifier for the current OS."""
        sys_name = platform.system()
        if sys_name == "Darwin":
            return "x86_64-darwin"
        elif sys_name == "Linux":
            return "x86_64-linux"
        else:
            raise RuntimeError(f"Unsupported system: {sys_name}")

    @classmethod
    def get_ecr_repo_uri(cls, repo_name: str, profile_name: str) -> str:
        """Fetch the ECR repository URI given a repo name and AWS profile."""
        session = boto3.Session(profile_name=profile_name)
        ecr_client = session.client("ecr")
        response = ecr_client.describe_repositories(repositoryNames=[repo_name])
        return response["repositories"][0]["repositoryUri"]

    @classmethod
    def ecr_login(cls, registry_uri: str, profile_name: str):
        """Login to ECR using a registry URI and AWS profile."""
        session = boto3.Session(profile_name=profile_name)
        ecr = session.client("ecr")
        token = ecr.get_authorization_token()
        auth_token = token["authorizationData"][0]["authorizationToken"]
        password = base64.b64decode(auth_token).decode("utf-8").split(":")[1]
        cls.sh(
            f"{cls.docker()} login --username AWS --password {password} {registry_uri}"
        )

    @classmethod
    def git_hash(cls) -> str:
        """Returns the short Git commit hash."""
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode("utf-8")
            .strip()
        )

    @classmethod
    def shell(cls):
        """
        Drop into a bash shell in the 'main' container, only creating + starting it if necessary.
        """
        # Check if the 'main' container is already up
        try:
            ps_output = (
                subprocess.check_output(f"{cls.compose()} ps -q main", shell=True)
                .decode()
                .strip()
            )
        except subprocess.CalledProcessError:
            ps_output = ""

        if not ps_output:
            cls.start()

        # Now exec into the container
        cls.sh(f"{cls.docker()} exec main bash")

    @classmethod
    def ci(cls, env: str, ecr_repo_name: str):
        """Build/push Docker image to ECR for given AWS profile (env)."""
        print(f"Running CI for environment/profile: {env}")
        repo_uri = cls.get_ecr_repo_uri(ecr_repo_name, profile_name=env)
        cls.sh(f"{cls.docker()} build -t {cls.name()}:latest .")
        cls.ecr_login(registry_uri=repo_uri.split("/")[0], profile_name=env)

        commit = cls.git_hash()
        cls.sh(f"{cls.docker()} tag {cls.name()}:latest {repo_uri}:latest")
        cls.sh(f"{cls.docker()} tag {cls.name()}:latest {repo_uri}:{commit}")

        cls.sh(f"{cls.docker()} push {repo_uri}:latest")
        cls.sh(f"{cls.docker()} push {repo_uri}:{commit}")

    @classmethod
    def cd(cls, env: str, region: str):
        """Deploy the latest ECS task definition in an environment's service."""
        print(f"Running CD for environment: {env}")
        session = boto3.Session(profile_name=env)
        ecs = session.client("ecs", region_name=region)

        cluster_name = f"{env}-{cls.name()}-cluster"
        service_name = f"{env}-{cls.name()}-service"

        service_desc = ecs.describe_services(
            cluster=cluster_name, services=[service_name]
        )
        current_td = service_desc["services"][0]["taskDefinition"]
        family_name = current_td.split("/")[-1].split(":")[0]

        task_defs = ecs.list_task_definitions(
            familyPrefix=family_name, sort="DESC", maxResults=1
        )
        latest_task_def = task_defs["taskDefinitionArns"][0]

        print(f"Latest task definition: {latest_task_def}")
        ecs.update_service(
            cluster=cluster_name,
            service=service_name,
            taskDefinition=latest_task_def,
            forceNewDeployment=True,
        )

        print("Waiting for ECS deployment to stabilize...")
        waiter = ecs.get_waiter("services_stable")
        waiter.wait(cluster=cluster_name, services=[service_name])
        print("Deployment successful!")

    @classmethod
    def start(cls):
        """Start local Docker Compose for development."""
        cls.sh(f"{cls.docker()} build -t f{cls.name()}:latest .")
        cls.sh(f"{cls.compose()} up -d")

    @classmethod
    def scale(cls, env: str, cluster: str, service: str, count: int, region: str):
        """
        Scale an ECS service to the specified number of tasks, then wait for stability.

        :param env: The AWS profile/environment
        :param cluster: The ECS cluster name.
        :param service: The ECS service name.
        :param count: The desired number of tasks.
        """
        print(
            f"Scaling ECS service '{service}' in cluster '{cluster}' to {count} tasks for env '{env}'..."
        )
        session = boto3.Session(profile_name=env)
        ecs = session.client("ecs", region_name=region)

        ecs.update_service(
            cluster=cluster,
            service=service,
            desiredCount=count,
        )

        print("Waiting for ECS deployment to stabilize...")
        waiter = ecs.get_waiter("services_stable")
        waiter.wait(cluster=cluster, services=[service])
        print("Scaling to", count, "tasks successful!")

    @classmethod
    def restart(cls):
        """Restart local Docker Compose containers."""
        print("Restarting local Docker Compose containers...")
        cls.sh(f"{cls.compose()} restart")
        print("Restarted successfully!")
