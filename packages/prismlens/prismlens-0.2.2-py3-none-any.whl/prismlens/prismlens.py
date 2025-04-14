"""Control script for Prism and related services."""

from __future__ import annotations

import subprocess
import sys
import time

from polykit.log import PolyLog

from prismlens.config import PrismAction, PrismConfig, PrismInstance

logger = PolyLog.get_logger(level="info")

PROD_CONTAINERS = ["prismbot", "prism-db", "prism-redis"]
PROD_SERVICES = ["prism-db", "prism-redis"]
NGINX_CONTAINER = "nginx"


class PrismLens:
    """Control class for Prism's environment and Docker stack."""

    def __init__(self, config: PrismConfig):
        self.config = config

    def handle_start(self) -> None:
        """Handle 'start' action."""
        if self.config.on_all:
            self.verify_nginx()
            self.start_prism(PrismInstance.PROD)
            self.start_prism(PrismInstance.DEV)
            self._restart_nginx()
            self.follow_logs(PrismInstance.DEV)
        elif self.config.instance == PrismInstance.DEV:
            self._ensure_prod_running()
            self.start_prism(PrismInstance.DEV)
            self.follow_logs(PrismInstance.DEV)
        else:
            self.verify_nginx()
            self.start_prism(PrismInstance.PROD)
            self._restart_nginx()
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

        # Check Nginx if we're dealing with prod
        if self.config.instance == PrismInstance.PROD or self.config.on_all:
            self.verify_nginx()

        if self.config.on_all:
            self.handle_all()
        else:
            self.stop_and_remove_containers(self.config.instance)
            self.start_prism(self.config.instance, stop_first=False)
            if self.config.instance == PrismInstance.PROD:
                self._restart_nginx()
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

        # Stop both instances (dev first, then prod)
        self.stop_and_remove_containers(PrismInstance.DEV)
        self.stop_and_remove_containers(PrismInstance.PROD)

        # Start prod and wait for it to be ready
        logger.info("Starting prod instance first...")
        self.start_prism(PrismInstance.PROD, stop_first=False)

        # Wait for prod services to be ready
        self.wait_for_prod_services()

        # Restart Nginx after prod services are started
        self._restart_nginx()

        # Start dev
        logger.info("Starting dev instance...")
        self.start_prism(PrismInstance.DEV, stop_first=False)

        logger.info("All instances restarted successfully!")

        # Follow logs after both restarts are complete
        self.follow_logs(self.config.instance)

    def follow_logs(self, instance: PrismInstance) -> None:
        """Follow the logs of the specified instance."""
        try:
            subprocess.call(["docker", "logs", "-f", instance.container])
        except KeyboardInterrupt:
            logger.info("Ending log stream.")
            sys.exit(0)

    def verify_nginx(self) -> None:
        """Verify that Nginx is running and configured correctly."""
        # Check if Nginx container is running
        command = f'docker ps --filter "name={NGINX_CONTAINER}" --format "{{{{.Names}}"'
        _, output = self.run(command)
        running_containers = output.splitlines()

        if not any("nginx" in container for container in running_containers):
            logger.error("%s container is not running.", NGINX_CONTAINER)
            sys.exit(1)

        # Check if Nginx configuration is valid
        command = f"docker exec {NGINX_CONTAINER} nginx -t"
        success, output = self.run(command)

        if success and "syntax is ok" in output and "test is successful" in output:
            logger.info("Nginx configuration is valid.")
        else:
            logger.error("Nginx configuration check failed:\n%s", output)
            sys.exit(1)

    def _restart_nginx(self) -> None:
        logger.info("Restarting %s...", NGINX_CONTAINER)
        success, output = self.run(f"docker restart {NGINX_CONTAINER}")

        if not success:
            logger.warning("Failed to restart %s: %s", NGINX_CONTAINER, output)

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
        self.run_docker_compose("down", instance)

        # Verify containers are actually gone
        self._verify_container_removal(instance)

        logger.info("%s stopped and removed.", instance.container)

    def _verify_container_removal(self, instance: PrismInstance, max_attempts: int = 5) -> None:
        """Verify that containers are properly removed, with retries if needed."""
        containers_to_check = [instance.container]
        if instance == PrismInstance.PROD:
            containers_to_check.extend(PROD_SERVICES)

        for container in containers_to_check:
            self._ensure_container_removed(container, max_attempts)

    def _ensure_container_removed(self, container: str, max_attempts: int = 5) -> None:
        """Ensure a specific container is removed, with retries if needed."""
        for attempt in range(max_attempts):
            # Check if container exists
            check_cmd = f"docker ps -a --filter name=^/{container}$ --format '{{{{.Names}}}}'"
            success, output = self.run(check_cmd)

            if not success or not output.strip():
                return  # Container is gone, so we're done here

            # Last attempt - force remove
            if attempt == max_attempts - 1:
                logger.warning(
                    "Container %s still exists after %d checks, forcing removal...",
                    container,
                    max_attempts,
                )
                self.run(f"docker rm -f {container}")

                # Final check after force removal
                success, output = self.run(check_cmd)
                if success and output.strip():
                    logger.error("Failed to remove container %s even when forced.", container)
                return

            # Container exists but we have more attempts, so check its status
            logger.debug(
                "Container %s still exists, waiting for removal (attempt %d/%d)...",
                container,
                attempt + 1,
                max_attempts,
            )

            # Check container status
            status_cmd = f"docker inspect --format='{{{{.State.Status}}}}' {container} 2>/dev/null || echo 'removed'"
            _, status = self.run(status_cmd)
            status = status.strip()

            if status in {"removing", "exited"}:  # Container being removed
                logger.debug("Container %s is in state: %s", container, status)

            else:  # Container is not being removed, try to stop it
                logger.debug("Attempting to stop container %s.", container)
                self.run(f"docker stop {container}")

            # Wait before next attempt
            time.sleep(1)

    def _ensure_prod_running(self) -> None:
        """Ensure the prod instance is running before proceeding."""
        prod = PrismInstance.PROD
        command = ["docker", "ps", "--filter", f"name={prod.container}", "--format", "{{.Status}}"]
        _, output = self.run(command)
        if "Up" not in output:
            logger.info("Prod instance not running, starting...")
            self.start_prism(prod)

    def wait_for_prod_services(self, max_attempts: int = 10) -> None:
        """Ensure that prod services are available before proceeding."""
        logger.info("Waiting for prod services to be ready...")

        for attempt in range(max_attempts):
            all_ready = True

            for container in PROD_CONTAINERS:  # Check if container is running and healthy
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

        logger.warning("Timed out waiting for prod services to be ready, continuing anyway.")

    def build_image(self, instance: PrismInstance) -> bool:
        """Build the Docker image for Prism."""
        logger.info("Building the Docker image for %s...", instance)

        commit_hash = self._get_commit_hash()
        command = f"GIT_COMMIT_HASH={commit_hash} docker compose build"

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

    def _get_commit_hash(self) -> str:
        success, output = self.run("git rev-parse HEAD")
        return output.strip() if success else "unknown"

    @staticmethod
    def run(
        command: str | list[str], show_output: bool = False, cwd: str | None = None
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
    def run_docker_compose(action: str, instance: PrismInstance) -> bool:
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


def main() -> None:
    """Perform the requested action."""
    # Check if both prod and dev paths exist
    if not PrismInstance.PROD.path.exists() or not PrismInstance.DEV.path.exists():
        logger.error("Required paths for prod and dev instances not found.")
        sys.exit(1)

    args = {arg.lower() for arg in sys.argv[1:]}
    config = PrismConfig.from_args(args, logger)
    prism = PrismLens(config)

    if config.action is PrismAction.START:
        prism.handle_start()
    elif config.action is PrismAction.RESTART:
        prism.handle_restart()
    elif config.action is PrismAction.STOP:
        prism.handle_stop()
    else:
        prism.follow_logs(config.instance)
