# In a Python file named event_organization.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EventFormOrganization(models.Model):
    _name = 'event.form.organization'
    _description = 'Event Reservation'

    name = fields.Char(string='Event Name', required=True)
    content = fields.Text(string='Event Content')
    begin_date = fields.Date(string='Begin Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    room_id = fields.Many2one('classroom', string='Classroom')

    @api.onchange('begin_date', 'end_date', 'room_id')
    def _check_classroom_availability(self):
        if self.begin_date and self.end_date and self.room_id:
            events = self.env['event.form.organization'].search([
                ('room_id', '=', self.room_id.id),
                ('id', '!=', self._origin.id) if self._origin else (1, '=', 1),
                '|',
                '&', ('begin_date', '<=', self.begin_date), ('end_date', '>=', self.begin_date),
                '&', ('begin_date', '<=', self.end_date), ('end_date', '>=', self.end_date)
            ])
            if events:
                raise ValidationError("The classroom is not available for the selected date range.")
