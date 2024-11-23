#!/usr/bin/env python3

"""
script to automatically archive photograph files into folders by year and month
to prevent folders from getting to large.

Python 3.x script syntax
"""
import datetime
import os
import time

# globals
# paths is a list of folders to perform archiving on.
paths = [
    "s:\\ftp\\aleeracam",
    "s:\\ftp\\bigsandycam",
    "s:\\ftp\\bigsandylake",
    "s:\\ftp\\bigsandylake2_ftp\\FI9805W_C4D655303E56\\snap",
    "s:\\ftp\\bigsandyloft_ftp\\FI9821P_C4D6553D93AE\\snap",
    "s:\\ftp\\meishkacam",
]
END_STRING = ".jpg"  # file type
NUMBER_OF_FILES = 50000  # maximum number of files to archive in one run,
#                          used to prevent infinite loops
MINIMUM_FILE_AGE = 60 * 60 * 24 * 7  # 7 days in seconds,
#                                       files newer than this won't be archived


def main():
    """
    Iterate over folders, archiving any file within these folders that meets
    the file age and file extension criteria.
    """
    # pylint: disable=too-many-locals
    archive_count = file_count = 0  # initialize counters
    start_time = time.time()

    # iterate through folders
    for path in paths:
        print(f"archiving files in folder '{path}'...")
        # iterate through files
        for entry in os.scandir(path):
            # iterate through each file
            if entry.path.endswith(END_STRING) and entry.is_file():
                full_path = entry.path

                # parse the file date for month and year
                file_time = os.path.getmtime(full_path)
                file_date = datetime.datetime.fromtimestamp(file_time)
                month = file_date.strftime("%m")
                year = file_date.strftime("%Y")
                # print("%s: file: %s, date: %s, month=%s, year=%s" %
                #      (file_count, full_path, file_date, month, year))
                file_count += 1

                # check file age
                days_old = (time.time() - file_time) / 60 / 60 / 24
                if not file_should_be_archived(file_time):
                    print(
                        f"{file_count}: skipping file: {full_path}, not old enough to archive "
                        f"({days_old:.1f} days old)"
                    )
                    continue
                archive_count += 1

                # create folders if needed
                subfolder = "\\" + str(year)
                target_path = path + "\\" + subfolder
                create_folder_if_necesary(target_path)  # year folder
                subfolder = subfolder + "\\" + str(month)
                target_path = path + subfolder
                create_folder_if_necesary(target_path)  # month sub-folder

                # create new filename
                file_name = full_path.strip(path)
                new_full_path = target_path + "\\" + file_name

                # move file
                print(
                    f"{file_count}: archiving file: {full_path} -> {subfolder}, "
                    f"({days_old:.1f} days old)"
                )
                os.rename(full_path, new_full_path)

                # exit at max number of files to prevent infinite loop
                if file_count >= NUMBER_OF_FILES:
                    print(
                        f"reached maximum file scan count of {file_count}, aborting run"
                    )
                    break

    # final message
    stop_time = time.time()
    elapsed_time_min = (stop_time - start_time) / 60
    print(
        f"{archive_count} of {file_count} files archived in {elapsed_time_min:.1f} minutes"
    )


def file_should_be_archived(file_timestamp):
    """
    Return True if file is old enough to be archived

    inputs:
        file_timestamp(float): datetime value of file
    returns:
        (bool) True if file exceeds limit
    """
    now = time.time()
    return file_timestamp < now - MINIMUM_FILE_AGE


def create_folder_if_necesary(target_path):
    """
    Create the target folder if it doesn't already exist

    inputs:
        target_path(str): target folder to create
    returns:
        None
    """
    if not os.path.isdir(target_path):
        os.mkdir(target_path)
        print(f"created new folder: {target_path}")
    else:
        pass


if __name__ == "__main__":
    # execute only if run as a script
    main()
    print("archiving script is done")
