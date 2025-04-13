import subprocess
import os
import shutil
import sys
import time
from typing import Optional

# This will store the build process
build_process = None


def clean_dist_folder(dist_dir: str = "dist"):
    """Clean the distribution folder before building."""
    if os.path.exists(dist_dir):
        print(f"Cleaning {dist_dir} directory...")
        try:
            shutil.rmtree(dist_dir)
            os.makedirs(dist_dir)
            print(f"Successfully cleaned {dist_dir} directory.")
        except Exception as e:
            print(f"Error cleaning {dist_dir} directory: {str(e)}")
            sys.exit(1)
    else:
        os.makedirs(dist_dir)
        print(f"Created {dist_dir} directory.")


def run_build_process(prod: bool = True):
    """Run the Parcel build process."""
    global build_process

    build_command = (
        ["npm.cmd", "run", "build"] if prod else ["npm.cmd", "run", "build:dev"]
    )

    try:
        print(
            f"Starting build process with {'production' if prod else 'development'} mode..."
        )
        build_process = subprocess.Popen(
            build_command,
            cwd=os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Stream output in real-time
        while True:
            output = build_process.stdout.readline()
            if output == b"" and build_process.poll() is not None:
                break
            if output:
                print(output.decode("utf-8").strip())

        # Check for errors
        if build_process.returncode != 0:
            stderr = build_process.stderr.read().decode("utf-8")
            print(f"Build process failed with error code {build_process.returncode}")
            print(f"Error: {stderr}")
            return False

        print("Build completed successfully!")
        return True

    except Exception as e:
        print(f"Error running build process: {str(e)}")
        return False


def copy_server_files(server_dir: str = "server", dist_dir: str = "dist"):
    """Copy server files to the distribution folder."""
    if os.path.exists(server_dir):
        try:
            # Create server directory in dist if it doesn't exist
            dist_server_dir = os.path.join(dist_dir, "server")
            if not os.path.exists(dist_server_dir):
                os.makedirs(dist_server_dir)

            # Copy server files, excluding __pycache__ folders
            for root, dirs, files in os.walk(server_dir):
                if "__pycache__" in root:
                    continue

                # Create corresponding directory in dist
                rel_path = os.path.relpath(root, server_dir)
                target_dir = os.path.join(dist_server_dir, rel_path)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                # Copy files
                for file in files:
                    if file.endswith(".py"):
                        src_file = os.path.join(root, file)
                        dst_file = os.path.join(target_dir, file)
                        shutil.copy2(src_file, dst_file)

            print("Server files copied successfully.")
            return True
        except Exception as e:
            print(f"Error copying server files: {str(e)}")
            return False
    else:
        print(f"Server directory '{server_dir}' not found.")
        return False


def copy_static_assets(static_dir: str = "static", dist_dir: str = "dist"):
    """Copy static assets to the distribution folder."""
    if os.path.exists(static_dir):
        try:
            # Create static directory in dist if it doesn't exist
            dist_static_dir = os.path.join(dist_dir, "static")
            if os.path.exists(dist_static_dir):
                shutil.rmtree(dist_static_dir)

            # Copy all static assets
            shutil.copytree(static_dir, dist_static_dir)
            print("Static assets copied successfully.")
            return True
        except Exception as e:
            print(f"Error copying static assets: {str(e)}")
            return False
    else:
        print(f"Static directory '{static_dir}' not found. Skipping.")
        return True  # Not critical, so return True


def create_package_json(dist_dir: str = "dist"):
    """Create a minimal package.json for production deployment."""
    try:
        # Read the original package.json to get name and version
        with open("package.json", "r") as f:
            import json

            pkg_data = json.load(f)

        # Create a minimal package.json for production
        prod_pkg = {
            "name": pkg_data.get("name", "carpenter-app"),
            "version": pkg_data.get("version", "1.0.0"),
            "private": True,
            "scripts": {"start": "node server/index.js"},
            "dependencies": {
                # Add only production dependencies needed to run the server
                "express": pkg_data.get("dependencies", {}).get("express", "^4.18.2"),
                "starlette": pkg_data.get("dependencies", {}).get(
                    "starlette", "^0.28.0"
                ),
            },
        }

        # Write the production package.json
        with open(os.path.join(dist_dir, "package.json"), "w") as f:
            json.dump(prod_pkg, f, indent=2)

        print("Created production package.json")
        return True
    except Exception as e:
        print(f"Error creating package.json: {str(e)}")
        return False


def build(prod: bool = True, dist_dir: str = "dist"):
    """Build the project for production or development."""
    start_time = time.time()
    print(f"Starting {'production' if prod else 'development'} build...")

    # Step 1: Clean the dist folder
    clean_dist_folder(dist_dir)

    # Step 2: Run the build process
    if not run_build_process(prod):
        print("Build failed. Exiting.")
        return False

    # Step 3: Copy server files
    if not copy_server_files(server_dir="carpenter", dist_dir=dist_dir):
        print("Failed to copy server files. Build may be incomplete.")

    # Step 4: Copy static assets
    copy_static_assets(dist_dir=dist_dir)

    # Step 5: Create production package.json
    if prod:
        create_package_json(dist_dir)

    # Done!
    elapsed_time = time.time() - start_time
    print(f"Build completed in {elapsed_time:.2f} seconds.")
    print(f"Output directory: {os.path.abspath(dist_dir)}")
    return True
