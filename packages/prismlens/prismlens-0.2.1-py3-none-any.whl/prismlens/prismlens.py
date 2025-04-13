"""Control script for the Prism service."""

from __future__ import annotations

import subprocess
import sys
import time

from polykit.log import PolyLog

from prismlens.prismlens_config import PrismAction, PrismConfig, PrismInstance

logger = PolyLog.get_logger(level="info")


class PrismLens:
    """Control class for Prism's environment and Docker stack."""

    def __init__(self, config: PrismConfig):
        self.config = config

    def build_image(self, instance: PrismInstance) -> bool:
        """Build the Docker image."""
        logger.info("Building the Docker image for %s...", instance)

        git_commit_hash = self._fetch_git_commit_hash()
        command = f"GIT_COMMIT_HASH={git_commit_hash} docker compose build"

        try:
            result = subprocess.call(command, shell=True, cwd=str(instance.path))
            if result == 0:
                logger.info("Docker image for %s built successfully.", instance)
                return True
            logger.error("Failed to build Docker image for %s. Exit code: %d", instance, result)
            return False
        except Exception as e:
            logger.error(
                "An error occurred while building the Docker image for %s: %s", instance, str(e)
            )
            return False

    def _fetch_git_commit_hash(self) -> str:
        """Fetch the current Git commit hash."""
        success, output = self.run("git rev-parse HEAD")
        return output.strip() if success else "unknown"

    def start_prism(self, instance: PrismInstance, stop_first: bool = True) -> None:
        """Start the Prism service."""
        if stop_first:
            self.stop_and_remove_containers(instance)

        logger.info("Starting %s...", instance.container)

        try:
            command = "docker compose up -d"
            logger.debug("Running command in %s: %s", instance.path, command)
            subprocess.call(command, shell=True, cwd=str(instance.path))
        except KeyboardInterrupt:
            logger.error("Start process interrupted.")

    def stop_and_remove_containers(self, instance: PrismInstance) -> None:
        """Stop and remove Docker containers."""
        logger.info("Stopping and removing %s...", instance.container)

        # First try the normal docker compose down
        self.docker_compose_command("down", instance)

        # Verify containers are actually gone
        self._verify_container_removal(instance)

        logger.info("%s stopped and removed.", instance.container)

    def _verify_container_removal(self, instance: PrismInstance, max_attempts: int = 5) -> None:
        """Verify that containers are properly removed, with retries if needed.

        Args:
            instance: The instance whose containers should be removed.
            max_attempts: Maximum number of verification attempts.
        """
        containers_to_check = [instance.container]
        if instance == PrismInstance.PROD:
            containers_to_check.extend(["prism-db", "prism-redis"])

        for container in containers_to_check:
            for attempt in range(max_attempts):
                check_cmd = f"docker ps -a --filter name=^/{container}$ --format '{{{{.Names}}}}'"
                success, output = self.run(check_cmd)

                if not success or not output.strip():
                    break  # Container is gone, move to next one

                if attempt == max_attempts - 1:  # Last attempt, force remove
                    logger.warning(
                        "Container %s still exists after %d checks, forcing removal...",
                        container,
                        max_attempts,
                    )
                    self.run(f"docker rm -f {container}")

                    success, output = self.run(check_cmd)
                    if success and output.strip():
                        logger.error("Failed to remove container %s even with force", container)
                else:  # Wait for Docker to finish processing previous command
                    logger.debug(
                        "Container %s still exists, waiting for removal (attempt %d/%d)...",
                        container,
                        attempt + 1,
                        max_attempts,
                    )

                    # Check if the container is in the process of stopping
                    status_cmd = f"docker inspect --format='{{{{.State.Status}}}}' {container} 2>/dev/null || echo 'removed'"
                    _, status = self.run(status_cmd)

                    if status.strip() == "removing" or status.strip() == "exited":
                        # Container is in the process of being removed or is stopped
                        logger.debug("Container %s is in state: %s", container, status.strip())
                    else:
                        # Container is not being removed, try to stop it first
                        logger.debug("Attempting to stop container %s", container)
                        self.run(f"docker stop {container}")

    def restart_single_instance(self, instance: PrismInstance) -> None:
        """Handle restart for a single instance."""
        logger.info("Restarting %s instance...", instance)

        # Stop and remove containers
        self.stop_and_remove_containers(instance)

        if instance == PrismInstance.PROD:  # Only check nginx for prod instance
            self.check_nginx()

        # Start without stopping again
        self.start_prism(instance, stop_first=False)

        logger.info("%s instance restart completed.", instance.capitalize())

    def check_nginx(self) -> None:
        """Check if both Nginx containers are running."""
        command = 'docker ps --filter "name=nginx" --format "{{.Names}}"'
        _, output = self.run(command)
        running_containers = set(output.splitlines())

        missing = []  # Check if containers with these names exist (using 'in' for partial matches)
        if all("nginx-proxy" not in container for container in running_containers):
            missing.append("nginx-proxy")
        if not any(
            "nginx" in container and "proxy" not in container for container in running_containers
        ):
            missing.append("nginx")

        if missing:
            logger.error("Required nginx containers not running: %s", ", ".join(missing))
            sys.exit(1)

    def ensure_prod_running(self) -> None:
        """Ensure prod instance is running, start if not."""
        command = ["docker", "ps", "--filter", "name=prism", "--format", "{{.Status}}"]
        _, output = self.run(command)
        if "Up" not in output:
            logger.info("Prod instance not running, starting...")
            self.start_prism(PrismInstance.PROD)

    def handle_start(self) -> None:
        """Handle 'start' action."""
        if self.config.on_all:
            self.check_nginx()
            self.start_prism(PrismInstance.PROD)
            self.start_prism(PrismInstance.DEV)
            self.follow_logs(PrismInstance.DEV)
        elif self.config.instance == PrismInstance.DEV:
            self.ensure_prod_running()
            self.start_prism(PrismInstance.DEV)
            self.follow_logs(PrismInstance.DEV)
        else:
            self.check_nginx()
            self.start_prism(PrismInstance.PROD)
            self.follow_logs(PrismInstance.PROD)

    def handle_restart(self) -> None:
        """Handle 'restart' action."""
        if self.config.on_all:
            if not self.build_image(PrismInstance.PROD) or not self.build_image(PrismInstance.DEV):
                logger.error("Image build failed. Exiting...")
                sys.exit(1)
        elif not self.build_image(self.config.instance):
            logger.error("Image build failed. Exiting...")
            sys.exit(1)

        if self.config.on_all:
            self.handle_all()
        else:
            self.stop_and_remove_containers(self.config.instance)
            if self.config.instance == PrismInstance.DEV:
                self.start_prism(PrismInstance.DEV)
            else:
                self.check_nginx()
                self.start_prism(PrismInstance.PROD)
            self.follow_logs(self.config.instance)

    def handle_stop(self) -> None:
        """Handle 'stop' action."""
        if self.config.on_all:  # Stop dev first, then prod
            self.stop_and_remove_containers(PrismInstance.DEV)
            self.stop_and_remove_containers(PrismInstance.PROD)
        elif self.config.instance == PrismInstance.DEV:
            self.stop_and_remove_containers(PrismInstance.DEV)
            self.follow_logs(PrismInstance.PROD)
        else:
            self.stop_and_remove_containers(PrismInstance.PROD)

    def handle_all(self) -> None:
        """Handle 'restart' action for both instances, ensuring proper order."""
        logger.info("Restarting all instances...")

        # First, stop both instances (dev first, then prod)
        self.stop_and_remove_containers(PrismInstance.DEV)
        self.stop_and_remove_containers(PrismInstance.PROD)

        # Then start prod and wait for it to be ready
        if PrismInstance.PROD == PrismInstance.PROD:  # Only check nginx for prod
            self.check_nginx()

        logger.info("Starting prod instance first...")
        self.start_prism(PrismInstance.PROD, stop_first=False)

        # Wait for prod services to be ready
        self._wait_for_prod_services()

        # Then start dev
        logger.info("Starting dev instance...")
        self.start_prism(PrismInstance.DEV, stop_first=False)

        logger.info("All instances restarted successfully!")

        # Follow logs after both restarts are complete
        self.follow_logs(self.config.instance)

    def _wait_for_prod_services(self, max_attempts: int = 10) -> None:
        """Wait for prod services to be ready.

        Args:
            max_attempts: Maximum number of attempts to check service readiness
        """
        logger.info("Waiting for prod services to be ready...")

        containers = ["prismbot", "prism-db", "prism-redis"]

        for attempt in range(max_attempts):
            all_ready = True

            for container in containers:  # Check if container is running and healthy
                cmd = f"docker inspect --format='{{{{.State.Status}}}}' {container} 2>/dev/null || echo 'not_found'"
                _, status = self.run(cmd)

                if status.strip() != "running":
                    all_ready = False
                    logger.debug(
                        "Container %s is not ready yet (status: %s)", container, status.strip()
                    )
                    break

            if all_ready:
                logger.info("All prod services are ready.")
                return

            logger.debug("Waiting for prod services (attempt %d/%d)...", attempt + 1, max_attempts)
            time.sleep(2)  # Short wait between checks

        logger.warning("Timed out waiting for prod services to be ready, continuing anyway")

    def follow_logs(self, instance: PrismInstance) -> None:
        """Follow the logs of the specified instance."""
        try:
            subprocess.call(["docker", "logs", "-f", instance.container])
        except KeyboardInterrupt:
            logger.info("Ending log stream.")
            sys.exit(0)

    @staticmethod
    def run(
        command: str | list[str],
        show_output: bool = False,
        cwd: str | None = None,
    ) -> tuple[bool, str]:
        """Execute a shell command and optionally print the output."""
        try:
            with subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd
            ) as process:
                output, _ = process.communicate()
                decoded_output = output.decode("utf-8").strip()

                if show_output:
                    print(decoded_output)

                return process.returncode == 0, decoded_output
        except subprocess.CalledProcessError as e:
            if show_output:
                print(e.output.decode("utf-8").strip())
            return False, e.output.decode("utf-8").strip()

    @staticmethod
    def docker_compose_command(action: str, instance: PrismInstance) -> bool:
        """Run a Docker Compose command.

        Args:
            action: The Docker Compose action (up, down, etc.).
            instance: The Prism instance to operate on.
        """
        command = f"docker compose {action}"

        if action == "up":
            command += " -d"

        logger.debug("Running command in %s: %s", instance.path, command)
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(instance.path),
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                logger.error(
                    "Docker Compose command failed with exit code %d\nOutput: %s\nError: %s",
                    result.returncode,
                    result.stdout.strip(),
                    result.stderr.strip(),
                )
                return False

            return True
        except Exception as e:
            logger.error("Docker Compose command failed: %s", str(e))
            return False


def parse_args() -> PrismConfig:
    """Parse command-line arguments in a flexible, command-style way."""
    args = {arg.lower() for arg in sys.argv[1:]}
    return PrismConfig.from_args(args, logger)


def main() -> None:
    """Perform the requested action."""
    # Check if both prod and dev paths exist
    if not PrismInstance.PROD.path.exists() or not PrismInstance.DEV.path.exists():
        logger.error("Required paths for prod and dev instances not found.")
        sys.exit(1)

    config = parse_args()
    prism = PrismLens(config)

    if config.action is PrismAction.START:
        prism.handle_start()
    elif config.action is PrismAction.RESTART:
        prism.handle_restart()
    elif config.action is PrismAction.STOP:
        prism.handle_stop()
    else:
        prism.follow_logs(config.instance)


if __name__ == "__main__":
    main()
