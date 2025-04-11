from odoo import fields, models
from odoo.tools import float_compare, float_round


class AccountMove(models.Model):
    _inherit = "account.move"

    # Fields used on account invoice reports pivot view
    partner_type = fields.Many2one("partner.type", string="Partner Type", readonly=True)
    partner_zone = fields.Many2one("partner.zone", string="Partner Zone", readonly=True)
