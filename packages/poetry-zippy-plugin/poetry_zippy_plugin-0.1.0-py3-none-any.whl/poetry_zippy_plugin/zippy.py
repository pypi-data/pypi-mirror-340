"""
Poetry Target Dependencies Plugin

A Poetry plugin that installs packages and their dependencies to a target directory,
similar to `pip install --target <folder>`. Useful for AWS Lambda deployments.

The plugin handles dependency resolution using Poetry's lock file, ensuring all
dependencies (including transitive ones) are installed correctly. It supports:
- Installing to a target directory
- Copying source files with pattern-based exclusions
- Creating ZIP archives for deployment
- Platform-specific wheel selection
- Python version compatibility
- Dependency group management (--only, --with, --without)
"""

from pathlib import Path
import shutil
from typing import Dict, Set
import os
import fnmatch
import tempfile
import collections

from cleo.events.console_events import COMMAND
from cleo.events.event import Event
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from cleo.helpers import option

from poetry.console.commands.group_command import GroupCommand
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.repositories.lockfile_repository import LockfileRepository
from poetry.core.packages.package import Package


class ZippyCommand(GroupCommand):
    name = "zippy"
    description = "Install the project dependencies to a target directory and optionally create a ZIP package"

    help = """
The <info>zippy</info> command installs all dependencies to a specific target directory.

This is useful for preparing deployments where all dependencies need to be in a single directory,
such as AWS Lambda functions. The command supports:
- Installing dependencies to a target directory
- Copying source files with pattern-based exclusions
- Creating ZIP archives for deployment
- Platform-specific wheel selection
- Python version compatibility
- Dependency group management

<info>poetry zippy --target ./lambda_dependencies</info>
"""

    options = [
        option("target", "t", "The target directory where dependencies will be installed.", flag=False),
        option("source", "s", "The source directory to copy into the target directory.", flag=False),
        option("exclude", "e", "Comma-separated patterns to exclude when copying source files.", flag=False),
        option("zip", "z", "Path to the ZIP file to create from the target directory.", flag=False),
        option("only", None, description="The dependency groups to consider (comma-separated).", flag=False),
        option("with", None, description="The optional dependency groups to include (comma-separated).", flag=False),
        option("without", None, description="The dependency groups to skip (comma-separated).", flag=False),
        option("platform", None, "Only use wheels compatible with this platform tag.", flag=False),
        option("implementation", None, "Only use wheels compatible with this Python implementation.", flag=False),
        option(
            "python-version",
            None,
            "The Python interpreter version to use for wheel and 'Requires-Python' compatibility checks.",
            flag=False,
        ),
        option("pip", None, "Additional arguments to pass directly to pip install.", flag=False),
    ]

    @property
    def activated_groups(self) -> Set[str]:
        """
        Safely determines the set of activated groups based on command options.

        This method handles the complex logic of determining which dependency groups
        should be included based on the --only, --with, and --without options.

        Returns:
            Set[str]: A set of group names that should be included in the installation.

        The logic follows these rules:
        1. If --only is specified, only those groups are included
        2. Otherwise, starts with 'main' and 'dev' (if not excluded)
        3. Adds groups from --with
        4. Removes groups from --without
        5. Ensures 'main' is present unless explicitly excluded by --only
        """
        # We need the Poetry object to access group definitions
        poetry_package = self.poetry.package

        # Determine base groups (usually main + dev, unless --no-dev is handled elsewhere or poetry version is old)
        # For simplicity and broad compatibility, let's default to ['main'] and add 'dev' if requested or not excluded.
        # Note: GroupCommand logic might be more complex in newer Poetry versions regarding defaults.
        # This simplified logic focuses on correctly parsing the --only, --with, --without flags.

        groups_to_parse: Dict[str, Set[str]] = {}
        for key in {"only", "with", "without"}:
            # Safely get option value, ensuring it's a string (even if empty)
            option_value = self.option(key)  # Get raw value (could be None)
            raw_groups_str = option_value if isinstance(option_value, str) else ""

            # Split and strip, handling empty strings correctly
            groups_to_parse[key] = {
                group.strip()
                for group in raw_groups_str.split(",")
                if group.strip()  # Avoid empty strings resulting from ",," or trailing ","
            }

        only = groups_to_parse["only"]
        _with = groups_to_parse["with"]
        without = groups_to_parse["without"]

        # Logic adapted from older Poetry versions / GroupCommand concept:
        # Start with all known groups
        all_groups = set(poetry_package.dependency_group_names(include_optional=True))

        # Filter by "only" if provided
        if only:
            activated = only.intersection(all_groups)
        # Ensure 'main' is included if 'only' is used without explicitly mentioning it?
        # This behavior varies; let's stick to explicit 'only' for now.
        # If 'main' is not in 'only', it won't be included.
        else:
            # Start with default groups (main + dev conceptually)
            activated = set()
            if "main" in all_groups:
                activated.add("main")
            # Check if 'dev' group exists (newer poetry versions)
            # Using try-except as group definition access might vary
            try:
                if poetry_package.dev_requires:  # Simple check if dev dependencies exist
                    if "dev" in all_groups:
                        activated.add("dev")
            except AttributeError:
                # Older poetry might not have dev_requires; dev might be in optional_groups
                if "dev" in all_groups:  # Add if it exists, regardless of optional status initially
                    activated.add("dev")

            # Add groups from "with"
            activated.update(_with.intersection(all_groups))

            # Remove groups from "without"
            activated.difference_update(without)

        # Ensure main is always present unless 'only' excludes it?
        # Let's enforce 'main' inclusion if 'activated' is currently empty and 'only' was not used.
        if not only and not activated and "main" in all_groups:
            activated.add("main")

        # Filter out any groups that don't actually exist (e.g., if 'dev' was assumed but not defined)
        return activated.intersection(all_groups)

    def handle(self) -> int:
        """
        Main command handler that orchestrates the installation process.

        The process follows these steps:
        1. Validates and sets up target directory
        2. Resolves dependencies using Poetry's lock file
        3. Installs each package to the target directory
        4. Copies source files (if specified)
        5. Creates ZIP file (if requested)
        6. Cleans up temporary directories

        Returns:
            int: 0 on success, 1 on failure
        """

        # Target/Zip/Temp Dir Setup...
        target_dir = self.option("target")
        zip_path = self.option("zip")

        # Ensure lock file exists before proceeding
        if not self.poetry.locker.is_locked():
            self.line_error("<error>poetry.lock not found. Please run 'poetry lock' first.</error>")
            return 1

        if not target_dir and not zip_path:
            self.line_error("<error>Either target directory (--target) or ZIP file (--zip) is required.</error>")
            return 1

        # If only zip is specified, create a temporary directory
        using_temp_dir = False

        if not target_dir and zip_path:
            target_dir = tempfile.mkdtemp(prefix="poetry_zippy_")
            using_temp_dir = True
            self.line(f"<info>Using temporary directory: {target_dir}</info>")

        target_path = Path(target_dir)

        if target_path.exists():
            if not target_path.is_dir():
                self.line_error(f"<error>{target_dir} exists and is not a directory.</error>")
                return 1

            # Clean directory if it exists
            # Check if the directory is non-empty before asking for confirmation
            if any(target_path.iterdir()) and self.confirm(
                f"Target directory {target_dir} is not empty. Clear it before proceeding?"
            ):
                try:
                    shutil.rmtree(target_path)
                    target_path.mkdir(parents=True)
                except Exception as e:
                    self.line_error(f"<error>Failed to clear directory: {e}</error>")
                    return 1
        else:
            # Create the directory if it doesn't exist
            try:
                target_path.mkdir(parents=True)
            except Exception as e:
                self.line_error(f"<error>Failed to create directory: {e}</error>")
                return 1

        self.line(f"<info>Installing dependencies to: {target_dir}</info>")

        # Get Poetry project
        poetry = self.poetry

        # 1. Get activated groups (uses the @property defined above)
        activated_groups = self.activated_groups
        # Type check remains useful
        if not isinstance(activated_groups, set):
            self.line_error(
                f"<error>Internal error: Expected self.activated_groups to be a set, but got {type(activated_groups)}</error>"
            )
            return 1
        self.line(f"<info>Processing dependencies for groups: {', '.join(activated_groups) or '[default]'}</info>")

        # 2. Get locked repository
        locked_repository: LockfileRepository = self.poetry.locker.locked_repository()

        # 3. Identify root dependencies and initial packages
        packages_to_install_set: set[Package] = set()
        queue = collections.deque()  # Queue for BFS traversal

        for group_name in activated_groups:
            try:
                # Get the DependencyGroup object for the current group name
                # This object holds the dependencies as defined in pyproject.toml for this group
                dependency_group = self.poetry.package.dependency_group(group_name)

                # Check if dependencies exist before iterating
                if dependency_group.dependencies:
                    for dependency in dependency_group.dependencies:
                        # Find the initial packages in the lock file for these direct dependencies
                        found_packages = locked_repository.find_packages(dependency)
                        for package in found_packages:
                            if package != poetry.package:  # Skip root project
                                if package not in packages_to_install_set:
                                    packages_to_install_set.add(package)
                                    queue.append(package)  # Add to queue for traversal
            except ValueError:
                # Handle cases where a group specified (e.g., via --with) doesn't exist
                # `dependency_group()` raises ValueError for unknown groups.
                self.line(f"<warning>Skipping non-existent group specified: {group_name}</warning>")

        self.line(
            f"<info>Found {len(packages_to_install_set)} direct dependencies for selected groups. Resolving transitive dependencies...</info>"
        )

        # 4. Graph Traversal (BFS)
        processed_packages_count = 0  # For richer logging if needed
        while queue:
            current_package: Package = queue.popleft()
            processed_packages_count += 1

            # Check if requirements exist before iterating
            if current_package.requires:
                for requirement in current_package.requires:
                    # Find the package(s) in the lock file satisfying this sub-dependency
                    found_packages = locked_repository.find_packages(requirement)
                    for resolved_sub_package in found_packages:
                        if resolved_sub_package != poetry.package:  # Skip root project
                            if resolved_sub_package not in packages_to_install_set:
                                packages_to_install_set.add(resolved_sub_package)
                                queue.append(resolved_sub_package)  # Add new package to traversal queue
                                processed_packages_count += 1  # Increment count when adding new package

        # 5. Convert set to sorted list
        packages_to_install = sorted(list(packages_to_install_set), key=lambda p: p.name)

        if not packages_to_install:
            # Message updated slightly
            self.line(
                f"<warning>No packages (including transitive) identified for installation for activated groups: {', '.join(activated_groups) or '[default]'}</warning>"
            )
            if not self.option("source") and not self.option("zip"):
                self.line("<info>No source copy or zip requested. Exiting.</info>")
                if using_temp_dir:
                    try:
                        shutil.rmtree(target_path)
                        self.line("<info>Cleaned up temporary directory</info>")
                    except Exception as e:
                        self.line_error(
                            f"<error>Warning: Failed to clean up temporary directory {target_dir}: {e}</error>"
                        )
                    return 0

        # Message updated slightly
        self.line(f"<info>Found {len(packages_to_install)} total packages (including transitive) to install.</info>")

        # Set up pip command for each package
        import subprocess
        import sys

        for package in packages_to_install:
            # Skip the root project package itself
            if package == poetry.package:
                continue

            self.line(f"Installing <c1>{package.name}</c1> (<c2>{package.version}</c2>)")

            # Use pip to install the package to the target directory
            pip_cmd = [
                sys.executable,
                "-m",
                "pip",
                "install",
                f"{package.name}=={package.version}",
                "--target",
                str(target_path),
                "--no-deps",  # We'll handle deps through Poetry's resolver
            ]

            # Add platform-specific options if provided
            if self.option("platform"):
                pip_cmd.extend(["--platform", self.option("platform")])
            if self.option("implementation"):
                pip_cmd.extend(["--implementation", self.option("implementation")])
            if self.option("python-version"):
                pip_cmd.extend(["--python-version", self.option("python-version")])

            # Add any additional pip arguments if provided
            if self.option("pip"):
                pip_cmd.extend(self.option("pip").split())

            try:
                subprocess.check_call(pip_cmd, stdout=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                self.line_error(f"<error>Failed to install {package.name}: {e}</error>")
                return 1

        # Handle source directory copying if specified
        source_dir = self.option("source")
        if source_dir:
            source_path = Path(source_dir)
            if not source_path.exists() or not source_path.is_dir():
                self.line_error(f"<error>Source directory {source_dir} does not exist or is not a directory.</error>")
                return 1

            self.line(f"<info>Copying source files from {source_dir} to {target_dir}...</info>")

            # Get exclude patterns if specified
            exclude_patterns = []
            if self.option("exclude"):
                exclude_patterns = self.option("exclude").split(",")
                self.line(f"<info>Excluding patterns: {', '.join(exclude_patterns)}</info>")

            # Always exclude common Python cache directories and files
            default_excludes = ["__pycache__/", "*.pyc", "*.pyo", "*.pyd", ".git/", ".pytest_cache/", ".coverage"]
            exclude_patterns.extend(default_excludes)

            def should_exclude(path):
                rel_path = os.path.relpath(path, source_path)
                for pattern in exclude_patterns:
                    if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                        return True
                return False

            # Copy files while respecting exclude patterns
            copied_files = 0
            for root, dirs, files in os.walk(source_path):
                # Filter out excluded directories to prevent walking into them
                dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]

                for file in files:
                    src_file = os.path.join(root, file)
                    if should_exclude(src_file):
                        continue

                    # Compute relative path to preserve directory structure
                    rel_path = os.path.relpath(src_file, source_path)
                    dst_file = target_path / rel_path

                    # Create parent directories if they don't exist
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)

                    # Copy the file
                    shutil.copy2(src_file, dst_file)
                    copied_files += 1

            self.line(f"<info>Copied {copied_files} files from {source_dir} to {target_dir}</info>")

        # Create ZIP file if requested
        if zip_path:
            self.line(f"<info>Creating ZIP file at {zip_path}...</info>")

            try:
                import zipfile

                # Ensure parent directory exists
                zip_file_path = Path(zip_path)
                zip_file_path.parent.mkdir(parents=True, exist_ok=True)

                # Create ZIP file
                with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                    # Walk through the target directory
                    for root, dirs, files in os.walk(target_path):
                        for file in files:
                            file_path = os.path.join(root, file)

                            # Calculate relative path for ZIP file
                            rel_path = os.path.relpath(file_path, target_path)

                            # Add file to ZIP
                            zipf.write(file_path, rel_path)

                self.line(f"<fg=green>Successfully created ZIP file: {zip_path}</>")
            except Exception as e:
                self.line_error(f"<error>Failed to create ZIP file: {e}</error>")
                return 1

        # Clean up temporary directory if we created one
        if using_temp_dir:
            try:
                shutil.rmtree(target_path)
                self.line("<info>Cleaned up temporary directory</info>")
            except Exception as e:
                self.line_error(f"<error>Warning: Failed to clean up temporary directory {target_dir}: {e}</error>")
        else:
            self.line(f"\n<fg=green>Successfully installed all dependencies to {target_dir}!</>")

        return 0


class ZippyPlugin(ApplicationPlugin):
    """
    Poetry plugin that adds a command to install dependencies to a target directory.

    This plugin registers the 'zippy' command with Poetry, making it available
    as a subcommand of the poetry CLI. The command supports installing dependencies
    to a target directory and creating deployment packages.
    """

    def activate(self, application: Application) -> None:
        """Activate the plugin."""
        application.command_loader.register_factory("zippy", lambda: ZippyCommand())

        # Optional: Add event listener for help command to show the new command
        # in the list of available commands
        dispatcher = application.event_dispatcher
        assert isinstance(dispatcher, EventDispatcher)

        dispatcher.add_listener(COMMAND, self.on_command)

    def on_command(self, event: Event, event_name: str, dispatcher: EventDispatcher) -> None:
        """Event handler for console commands."""
        pass  # We don't need to do anything here, but it's required for the event listener
