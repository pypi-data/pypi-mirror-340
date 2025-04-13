#!/usr/bin/env python3

"""Control script for the Prism service."""

from __future__ import annotations

import subprocess
import sys
from threading import Thread

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

    def start_prism(self, instance: PrismInstance) -> None:
        """Start the Prism service."""
        logger.info("Starting %s...", instance.container)

        try:
            self.docker_compose_command("up", instance)
        except KeyboardInterrupt:
            logger.error("Start process interrupted.")

    def stop_and_remove_containers(self, instance: PrismInstance) -> None:
        """Stop and remove Docker containers."""
        logger.info("Stopping and removing %s...", instance.container)
        self.docker_compose_command("down", instance)
        logger.info("%s stopped and removed.", instance.container)

    def restart_single_instance(self, instance: PrismInstance) -> None:
        """Handle restart for a single instance."""
        logger.info("Restarting %s instance...", instance)
        self.stop_and_remove_containers(instance)

        if instance == PrismInstance.PROD:  # Only check nginx for prod instance
            self.check_nginx()

        self.start_prism(instance)
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
        """Handle 'restart' action for both instances using threads."""
        # Create threads for both instances
        prod_thread = Thread(target=self.restart_single_instance, args=(PrismInstance.PROD,))
        dev_thread = Thread(target=self.restart_single_instance, args=(PrismInstance.DEV,))

        # Start both threads
        prod_thread.start()
        dev_thread.start()

        # Wait for both threads to complete
        prod_thread.join()
        dev_thread.join()

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
    def docker_compose_command(action: str, instance: PrismInstance) -> None:
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
            subprocess.call(command, shell=True, cwd=str(instance.path))
        except Exception as e:
            logger.error("Docker Compose command failed: %s", str(e))


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
