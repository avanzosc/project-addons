# Copyright 2026 AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Merge duplicated task stages once, right after installing the module."""
    _logger.info("Merging duplicated task stages after module installation.")
    env["project.task.type"]._merge_duplicate_stages_by_name()
