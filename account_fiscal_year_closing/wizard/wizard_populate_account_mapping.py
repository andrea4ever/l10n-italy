# -*- coding: utf-8 -*-
# Copyright 2016 Apulia Software srl (<http://www.apuliasoftware.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, fields, api

USER_TYPE = {
    'lp': ('income', 'expense'),
    'nlp': ('asset', 'liabilty'),
}

MODEL_TYPE = {
    'lp': 'account_fiscal_year_closing.fyc_lp_account_map',
    'nlp': 'account_fiscal_year_closing.fyc_nlp_account_map'
}


class PopulateAccountMapping(models.TransientModel):

    _name = 'populate.account.mapping'

    mapping_type = fields.Selection(
        [('lp', 'Loss & Profit'),
         ('nlp', 'Net Loss & Profit'), ('c', 'Closing')], required=True,
        default='lp')
    dest_account_id = fields.Many2one('account.account', required=True)

    @api.multi
    def populate_mapping(self):
        self.ensure_one()
        user_type = self.env['account.account.type'].search([
            ('report_type', 'in', USER_TYPE[self.mapping_type])])
        accounts = self.env['account.account'].search([
            ('type', 'in', ('other', 'receivable', 'payable', 'liquidity')),
            ('user_type', 'in', ([t.id for t in user_type]))
        ])
        for account in accounts:
            self.env[MODEL_TYPE[self.mapping_type]].create({
                'fyc_id': self._context['active_id'],
                'source_account_id': account.id,
                'dest_account_id': self.dest_account_id.id,
            })
