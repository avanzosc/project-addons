# Copyright 2021 Afredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestProjectTaskEvent(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task = cls.env.ref("project.project_task_1")
        meeting_vals = {
            "name": cls.task.name,
            "start": fields.Datetime.now(),
            "stop": fields.Datetime.now(),
            "task_id": cls.task.id,
        }
        cls.meeting = cls.env["calendar.event"].create(meeting_vals)

    def test_project_task_event(self):
        self.assertEqual(self.task.count_calendar_event, 1)
        result = self.task.action_to_calendar_event()
        context = result.get("context")
        self.assertEqual(result.get("res_model"), "calendar.event")
        self.assertEqual(context.get("default_name"), self.task.name)
        domain = [("id", "in", [self.meeting.id])]
        self.assertEqual(result.get("domain"), domain)
