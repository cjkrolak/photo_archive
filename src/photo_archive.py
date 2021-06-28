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
end_string = ".jpg"  # file type
number_of_files = 50000  # maximum number of files to archive in one run,
#                          used to prevent infinite loops
minimum_file_age = 60 * 60 * 24 * 7  # 7 days in seconds,
#                                       files newer than this won't be archived


def main():
    """
    Iterate over folders, archiving any file within these folders that meets
    the file age and file extension criteria.
    """
    archive_count = file_count = 0  # initialize counters
    start_time = time.time()

    # iterate through folders
    for path in paths:
        print("archiving files in folder '%s'..." % path)
        # iterate through files
        for entry in os.scandir(path):
            # iterate through each file
            if entry.path.endswith(end_string) and entry.is_file():
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
                if not file_should_be_archived(file_time):
                    print(
                        "%s: skipping file: %s, not old enough to archive"
                        % (file_count, full_path)
                    )
                    continue
                else:
                    archive_count += 1
                    print("%s: archiving file: %s" % (file_count, full_path))

                # create folders if needed
                target_path = path + "\\" + str(year)
                create_folder_if_necesary(target_path)  # year folder
                target_path = path + "\\" + str(year) + "\\" + str(month)
                create_folder_if_necesary(target_path)  # month sub-folder

                # move file
                file_name = full_path.strip(path)
                new_full_path = target_path + "\\" + file_name
                os.rename(full_path, new_full_path)

                # exit at max number of files to prevent infinite loop
                if file_count >= number_of_files:
                    print(
                        "reached maximum file scan count of %s,"
                        " aborting run" % file_count
                    )
                    break

    # final message
    stop_time = time.time()
    elapsed_time_min = (stop_time - start_time) / 60
    print(
        "%s of %s files archived in %.1f minutes"
        % (archive_count, file_count, elapsed_time_min)
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
    if file_timestamp < now - minimum_file_age:
        return True
    else:
        return False


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
        print("created new folder: %s" % target_path)
    else:
        pass


if __name__ == "__main__":
    # execute only if run as a script
    main()
    print("archiving script is done")
