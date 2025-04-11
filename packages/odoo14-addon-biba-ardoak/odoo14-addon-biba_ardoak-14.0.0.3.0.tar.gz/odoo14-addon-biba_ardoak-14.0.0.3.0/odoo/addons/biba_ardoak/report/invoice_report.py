from odoo import fields, models, api


class InvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    partner_type = fields.Many2one("partner.type", string="Partner Type", readonly=True)
    partner_zone = fields.Many2one("partner.zone", string="Partner Zone", readonly=True)

    _depends = {
        'res.partner': ['partner_zone', 'partner_type'],
    }

    @property
    def _table_query(self):
        return '{} {} {} {}'.format(self._select(), self._from(), self._where(), self._group_by())

    @api.model
    def _from(self):
        res = super()._from()
        res += """
        left join partner_type p_type on (partner.partner_type=p_type.id)
        left join partner_zone p_z on (partner.partner_zone=p_z.id)
        """
        return res

    @api.model
    def _group_by(self):
        res = """
        GROUP BY
        p_type.id
        , p_z.id
        , line.id
        , move.state
        , move.move_type
        , move.partner_id
        , move.invoice_user_id
        , move.fiscal_position_id
        , move.payment_state
        , move.invoice_date
        , move.invoice_date_due
        , uom_template.id
        , template.categ_id
        , uom_line.factor
        , currency_table.rate
        , partner.country_id
        , commercial_partner.country_id
        , move.payment_mode_id
        , move.team_id
        """
        return res

    @api.model
    def _select(self):
        res = super()._select()
        return "{} {}".format(res, ", p_type.id as partner_type, p_z.id as partner_zone")
