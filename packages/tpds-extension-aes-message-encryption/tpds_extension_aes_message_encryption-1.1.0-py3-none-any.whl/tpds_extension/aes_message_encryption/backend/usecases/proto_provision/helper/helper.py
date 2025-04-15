# This file is governed by the terms outlined in the LICENSE file located in the root directory of
#  this repository. Please refer to the LICENSE file for comprehensive information.

import os
from tpds.flash_program import FlashProgram
from tpds.tp_utils.tp_settings import TPSettings
from tpds.api.api.hw.api_board import get_details
from tpds.proto_boards import get_board_path


def check_board_status(board, logger):
    """Check the board status and program the factory hex if not programmed

    Args:
        board (_type_): Board information to check the status
        logger (_type_): Logger object to capture the logs
    """
    logger.log("Checking Board Status... ")
    assert board, "No board selected"
    kit_parser = FlashProgram(board, get_details(board))
    logger.log(kit_parser.check_board_status())
    assert kit_parser.is_board_connected(), "Check the Kit parser board connections"
    factory_hex = os.path.join(get_board_path(board), f"{board}.hex")
    if not kit_parser.is_factory_programmed():
        assert factory_hex, "Factory hex is unavailable to program"
        logger.log("Programming factory hex...")
        path = os.path.join(
            TPSettings().get_tpds_core_path(),
            "assets",
            "Factory_Program.X",
            factory_hex,
        )
        logger.log(f"Programming {path} file")
        kit_parser.load_hex_image(path)
    logger.log("Board Status OK")
