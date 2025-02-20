#!/usr/bin/env python3

import os
import subprocess
import sys
import argparse
import logging
import textwrap
import traceback

description = """
    Performance Analyse Tools
    If the usage above is too long to read, please add the argument in `positional arguments` below to use subcommand.
"""
class MyFormatter(argparse.RawTextHelpFormatter,
                  argparse.ArgumentDefaultsHelpFormatter):
    pass

help_text_example = textwrap.dedent("""
Example:
    # (a) analyse one xml generated by gtest
    python3 analysis_suite.py --log_path=output.xml

    # (b) analyse one xml generated by gtest without database
    python3 analysis_suite.py --log_path=output.xml --use_db=0

    # (c) analyse one folder of xmls generated by gtest repeat mode
    python3 analysis_suite.py --log_path=xml_folder_path

    # (d) compare two xml generated by gtest
    python3 analysis_suite.py --log_path=output.xml --compare_path=baseline.xml

    # (e) compare two xml and generate images which contain cases' comparison info
    python3 analysis_suite.py --log_path=output.xml --compare_path=baseline.xml --generate_pic 1

    # (f) compare two xml folder of xmls generated by gtest repeat mode
    python3 analysis_suite.py --log_path=xml_folder_path --compare_path=baseline_folder_path

    # (g) tpi: compare two xml. when no comparison is needed, --compare_path can be ignored
    python3 analysis_suite.py --log_path=output.xml --compare_path=baseline.xml --tpi 1

    # (h) simple_tpi : compare two xml. when no comparison is needed, --compare_path can be ignored
    python3 analysis_suite.py --log_path=output.xml --compare_path=baseline.xml --tpi 1 --simple_tpi 1 --frameworks pt1.13

    # (i) simple_tpi : do not parse pt/pb files(no `input`, `output`, `params` field in `cases` Table)
    python3 analysis_suite.py --log_path=new.xml --compare_path=baseline.xml --need_case_info False

    # (j) filter: select operators in `operator_summary` and `operator_summary(cri)` based on json file
    python3 gtest_analyser.py --log_path=conv.xml --json_file op_list.json

    # (k) filter: deselect operators in `operator_summary` and `operator_summary(cri)` based on json file
    python3 gtest_analyser.py --log_path=conv.xml --json_file op_list.json --is_pro 0

    see more details in http://wiki.cambricon.com/pages/viewpage.action?pageId=137672096

""")

def run(args):
    logging.info("run analysis_suite start")

    if "h5" == args.subcommand:
        from h5_creator import run as run_h5_creator
        run_h5_creator(args)
    elif "so" == args.subcommand:
        from so_analyser import run as run_so_analyser
        run_so_analyser(args)
    elif "gtest" == args.subcommand:
        from gtest_analyser import run as run_gtest_analyser
        run_gtest_analyser(args)
        """
    elif "compile_time" == args.subcommand:
        from analyse_compile_time import run as run_compile_time_analyse
        run_compile_time_analyse(args)
    elif "pt2excel" == args.subcommand:
        from prototxt_to_excel import run as run_pt2excel
        run_pt2excel(args)
        """
    elif None == args.subcommand: # 伺候老命令
        from h5_creator import run as run_h5_creator
        from so_analyser import run as run_so_analyser
        from gtest_analyser import run as run_gtest_analyser

        run_h5_creator(args)
        run_so_analyser(args)
        run_gtest_analyser(args)
    else:
        logging.error("error on reading subcommands.")

    logging.info("run analysis_suite end")

if __name__ == "__main__":
    # assure `saved in analysis_suite/cfg/mlu_op_test_pb2.py` exists
    from analysis_suite.utils.ptpb_helper import proto_helper
    proto_helper.check_mluops_proto()

    # initialize arguments parser
    from analysis_suite.args_parser.gtest_log_to_xlsx_parser import Gtest_Log_to_Xlsx_Parser
    parser = Gtest_Log_to_Xlsx_Parser(
        argparse.ArgumentParser(
            description=description,
            formatter_class=MyFormatter,
            epilog=help_text_example
        )
    )

    # parse arguments
    args = parser.parse_args()

    # initialize `logging` module
    from analysis_suite.utils import logger_helper
    logger_helper.logger_init(args)

    logging.debug(args)

    # run the main logic
    try:
        run(args)
    except Exception as e:
        print(e)
        traceback.print_exc()
        sys.exit(1)
