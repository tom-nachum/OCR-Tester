import csv
import subprocess
import os
import time
import datetime
import sys
from pathlib import Path

ENCODING = "UTF-8"
TXT = ".txt"

# Input.csv cols:
TEST_NUMBER = "\ufeffTest number"
PATH = "Path"
FILE_NAME = "File name"
ING_DESC = "Image description"
TEXT = "Text"
COMMENTS = "Comments"
LANGUAGE = "Language"
BLACK = "tessedit_char_blacklist="
UN_BLACK = "tessedit_char_unblacklist="
WHITE = "tessedit_char_whitelist="
SEP = "page_separator="
INPUT_HEADER = [TEST_NUMBER, PATH, FILE_NAME, ING_DESC, TEXT, COMMENTS,
                LANGUAGE, BLACK, UN_BLACK, WHITE, SEP]
EMPTY_CONFIG = 'None'
EMPTY_LANG = ''

# testResults.csv:
RESULTS_CSV = "testResults_artuim.csv"
# extra cols in testResults.csv:
PASS_FAIL = "Pass/Fail"
TESSERACT_OUTPUT = "Tesseract Output"
COMMAND = "Command"
OUTPUT_HEADER = [PASS_FAIL, TESSERACT_OUTPUT, COMMAND]

# Tesseract run config:
TESSERACT = "Tesseract"
PATH_OF_OUTPUT_TXT = "output"
CONFIG = "-c"
LANG = "-l"


def add_config_parameters(row):
    config = []
    black, un_black, white, sep = row[BLACK], row[UN_BLACK], row[WHITE], row[SEP]
    if black != EMPTY_CONFIG:
        config += [CONFIG, BLACK + black]
    if un_black != EMPTY_CONFIG:
        config += [CONFIG, UN_BLACK + un_black]
    if white != EMPTY_CONFIG:
        config += [CONFIG, WHITE + white]
    if sep != EMPTY_CONFIG:
        config += [CONFIG, SEP + sep]
    return config


def run_tesseract(row):
    file_name, path, language = row[FILE_NAME], row[PATH], row[LANGUAGE]
    input_image_name = os.path.join(path, file_name)
    test_num = row[TEST_NUMBER]
    output_txt_name = PATH_OF_OUTPUT_TXT + f"/test_{test_num}"
    command_op = [TESSERACT, input_image_name, output_txt_name]
    if language != EMPTY_LANG:
        command_op += [LANG, language]
    command_op += add_config_parameters(row)
    subprocess.run(command_op)
    command = " ".join(command_op)
    return output_txt_name, command


def analyze(txt_file_name, expected_txt, tess_command):
    output_file = open(txt_file_name + TXT, encoding=ENCODING)
    if SEP in tess_command:
        output_text = "".join(output_file.readlines())
    else:
        output_text = "".join(output_file.readlines()[:-1])
    output_file.close()
    result = "Pass" if expected_txt == output_text else "Fail"
    return result, output_text


def print_results(test_num, test_command, result):
    command_col = " " * (len(test_command) - len("Command"))
    header = f"Test# | Command {command_col}| Result"
    test_col = ' ' * (len("Test#") - len(test_num))
    test = f"{test_num}{test_col} | {test_command} | {result}"
    print(header)
    print(test)


def run_automation():
    input_csv_name = sys.argv[1]
    input_csv = open(input_csv_name, encoding=ENCODING)
    test_results_csv = open(RESULTS_CSV, 'w', newline='', encoding=ENCODING)
    results_writer = csv.writer(test_results_csv)
    results_writer.writerow(INPUT_HEADER + [PASS_FAIL])
    Path(os.path.curdir + "/output").mkdir(parents=True, exist_ok=True)
    for row in csv.DictReader(input_csv):
        output_text_name, command = run_tesseract(row)
        test_result, out_txt = analyze(output_text_name, row[TEXT], command)
        print_results(row[TEST_NUMBER], command, test_result)
        results_writer.writerow(list(row.values()) + [test_result])
    input_csv.close()
    test_results_csv.close()


def calc_time(start_time, end_time):
    total_seconds = end_time - start_time
    print("\nTime of automation:")
    print(str(datetime.timedelta(seconds=total_seconds)))


if __name__ == '__main__':
    start = time.time()
    run_automation()
    end = time.time()
    calc_time(start, end)
