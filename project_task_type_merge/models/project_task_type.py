# Copyright 2026 AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import logging

from odoo import Command, _, api, models

_logger = logging.getLogger(__name__)


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    def action_merge_duplicate_stages(self):
        """Run the merge and return a notification with the outcome.

        Thin wrapper around :meth:`_merge_duplicate_stages_by_name` used by
        the manual server action. Building the notification here (instead of
        inside the action's ``code`` field) keeps its title and message
        translatable, since terms in server-action code are not exported.
        """
        result = self._merge_duplicate_stages_by_name()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Task Stages Merged"),
                "message": _(
                    "%(groups)s group(s) merged, %(stages)s stage(s) deleted.",
                    groups=result["merged_groups"],
                    stages=result["deleted_stages"],
                ),
                "type": "success",
                "sticky": False,
            },
        }

    @api.model
    def _merge_duplicate_stages_by_name(self):
        """Merge project task stages sharing the same name.

        For every group of project stages (``user_id`` not set) with an
        identical name, a single canonical stage is kept: all its tasks are
        moved to it, every related project is gathered on it and the remaining
        duplicates are deleted. Archived stages are merged too; when a group
        mixes active and archived stages, an active one is kept as canonical
        so that tasks are never moved onto a hidden stage. Personal stages
        (``user_id`` set) are never touched.

        It is used both by the module ``post_init_hook`` and by the manual
        server action, so the clean up can be relaunched at any time.
        """
        # active_test=False so archived stages/projects are taken into account.
        Stage = self.env["project.task.type"].with_context(active_test=False).sudo()
        Task = self.env["project.task"].with_context(active_test=False).sudo()
        stages = Stage.search([("user_id", "=", False)], order="id asc")

        # Group the project stages (archived ones included) by their (stripped)
        # stored name. The name is translatable, so duplicates are grouped by
        # the value shown in the current language, which matches the columns
        # created per project.
        groups = {}
        for stage in stages:
            name = (stage.name or "").strip()
            if not name:
                continue
            groups.setdefault(name, Stage.browse())
            groups[name] |= stage

        merged_groups = 0
        deleted_stages = 0
        for name, group in groups.items():
            if len(group) < 2:
                continue
            # Prefer the lowest-id active stage as canonical (records are
            # ordered by id asc) so tasks are not moved onto an archived stage;
            # fall back to the lowest-id one when the whole group is archived.
            active_stages = group.filtered("active")
            canonical = (active_stages or group)[0]
            duplicates = group - canonical
            # A savepoint per group keeps a single failure from aborting the
            # whole merge while leaving no half-merged data behind.
            try:
                with self.env.cr.savepoint():
                    # Keep the canonical stage available in every project that
                    # was linked to any of the merged stages (archived projects
                    # included, since Stage runs with active_test=False).
                    projects = group.project_ids
                    canonical.project_ids = [Command.set(projects.ids)]
                    # Move every task (archived ones included) to the canonical
                    # stage before deleting the duplicates (ondelete='restrict').
                    tasks = Task.search([("stage_id", "in", duplicates.ids)])
                    tasks.write({"stage_id": canonical.id})
                    duplicates.unlink()
                merged_groups += 1
                deleted_stages += len(duplicates)
            except Exception:  # noqa: BLE001
                _logger.exception(
                    "Could not merge duplicated task stages named '%s'.", name
                )

        _logger.info(
            "Duplicated task stages merge finished: %s group(s) merged, "
            "%s stage(s) deleted.",
            merged_groups,
            deleted_stages,
        )
        return {"merged_groups": merged_groups, "deleted_stages": deleted_stages}
