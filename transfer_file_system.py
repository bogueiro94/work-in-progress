#Python transfer file system

import os
import shutil
import logging
import argparse
from apscheduler.schedulers.blocking import BlockingScheduler

def sync_folders(source_folder, target_folder):
    # Configure logging
    logging.basicConfig(filename='sync_log2.txt', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s')

    # Get a list of files and directories in the source folder
    source_contents = os.listdir(source_folder)

    # Get a list of files and directories in the target folder
    target_contents = os.listdir(target_folder)

    # Sync based on last modified time
    for item in source_contents:
        source_item = os.path.join(source_folder, item)
        target_item = os.path.join(target_folder, item)

        if os.path.exists(target_item):
            if os.path.isdir(source_item):
                sync_folders(source_item, target_item)
            elif os.path.getmtime(source_item) > os.path.getmtime(target_item):
                shutil.copy2(source_item, target_item)
                logging.info(f"File copied: {target_item}")
        else:
            if os.path.isdir(source_item):
                shutil.copytree(source_item, target_item)
                logging.info(f"Folder created: {target_item}")
            else:
                shutil.copy2(source_item, target_item)
                logging.info(f"File copied: {target_item}")

    # Remove files and directories from the target folder
    for item in target_contents:
        target_item = os.path.join(target_folder, item)
        if item not in source_contents:
            if os.path.isdir(target_item):
                shutil.rmtree(target_item)
                logging.info(f"Folder removed: {target_item}")
            else:
                os.remove(target_item)
                logging.info(f"File removed: {target_item}")

if __name__ == "__main__":
    # Create an ArgumentParser object to handle command line arguments
    parser = argparse.ArgumentParser(description="Folder synchronization tool")
    # Add command line arguments for source folder, target folder, and synchronization interval
    parser.add_argument("source", help="Path to source folder")
    parser.add_argument("target", help="Path to target folder")
    parser.add_argument("sync_interval", type=float, default=0.1, help="Interval between syncs in seconds")
    
    # Parse the command line arguments
    args = parser.parse_args()
    
    # Create a BlockingScheduler object to schedule synchronization jobs
    scheduler = BlockingScheduler()
    scheduler.add_job(lambda: sync_folders(args.source, args.target), 'interval', seconds=args.sync_interval)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
