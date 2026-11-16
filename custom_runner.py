
import os
import shutil
import argparse
from behave.__main__ import main as behave_main


def clean_and_create_folder(folder_path):
    """Deletes a folder if it exists and recreates it."""
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)


if __name__ == "__main__":

    # Define paths
    allure_results_folder = "reports/allure-results"
    screenshot_folder = "screenshots"

    # 1. Perform pre-test setup
    print("Cleaning up old reports and screenshots...")
    clean_and_create_folder(allure_results_folder)
    clean_and_create_folder(screenshot_folder)

    # 2. Set up command-line argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tags",
        help="Behave tags to filter scenarios",
        default=""
    )
    args = parser.parse_args()

    # 3. Get tags from Jenkins environment variable OR command-line argument
    tags_to_run = os.getenv("BEHAVE_TAGS", args.tags)

    # 4. Define Behave arguments
    behave_args = []

    if tags_to_run:
        behave_args.extend(["--tags", tags_to_run])

    behave_args.extend([
        "--format", "allure_behave.formatter:AllureFormatter",
        "--outfile", "reports/allure-results"
    ])

    # 5. Run Behave tests
    print(f"Running Behave tests with tags: {tags_to_run or 'All scenarios'}")
    behave_main(behave_args)

    # 6. Post-test actions
    print("Test execution finished. To see the report, run: allure serve reports/allure-results")
