# -*- coding: utf-8 -*-
# Copyright 2009 Zikzakmedia S.L. (
#               http://zikzakmedia.com) All Rights Reserved.
#           Jordi Esteve <jesteve@zikzakmedia.com>
# Copyright 2008 ACYSOS S.L. (http://acysos.com) All Rights Reserved.
#           Pedro Tarrafeta <pedro@acysos.com>
# Copyright 2011 Associazione Odoo Italia (<http://www.odoo-italia.org>).
# Copyright 2012 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright 2012 Domsense srl (<http://www.domsense.com>)
# Copyright 2016 Apulia Software srl (<http://www.apuliasoftware.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""
Fiscal Year Closing
"""
__author__ = "Borja López Soilán (Pexego)"

from openerp import models, fields, api, _
from datetime import datetime
from openerp.exceptions import Warning as UserError
from openerp import netsvc


#-------------------------------------------------------------------------------
# Predeclaration of the FYC object
#-------------------------------------------------------------------------------
class fiscal_year_closing_init(models.Model):
    """
    Fiscal Year Closing Wizard
    """

    _name = "account_fiscal_year_closing.fyc"
    _description = "Fiscal Year Closing Wizard"

    name = fields.Char(string='Description', size=60, required=True)



#-------------------------------------------------------------------------------
# Account mapping objects (to be used on the fyc configuration)
#-------------------------------------------------------------------------------

class fiscal_year_closing_lp_account_mapping(models.Model):
    """
    Loss & Profit Account Mapping
    """

    _name = "account_fiscal_year_closing.fyc_lp_account_map"
    _description = "SFYC Loss & Profit Account Mapping"

    name = fields.Char(sting='Description', size=60)
    fyc_id = fields.Many2one(
        'account_fiscal_year_closing.fyc', string='Fiscal Year Closing',
        ondelete='cascade', required=True, select=1)
    source_account_id = fields.Many2one(
        'account.account', string='Source account',
        required=True, ondelete='cascade')
    dest_account_id = fields.Many2one(
        'account.account', string='Dest account',
        required=False, ondelete='cascade')


class fiscal_year_closing_nlp_account_mapping(models.Model):
    """
    Net Loss & Profit Account Mapping
    """

    _name = "account_fiscal_year_closing.fyc_nlp_account_map"
    _description = "SFYC Net Loss & Profit Account Mapping"

    name = fields.Char(sting='Description', size=60)
    fyc_id = fields.Many2one(
        'account_fiscal_year_closing.fyc', string='Fiscal Year Closing',
        ondelete='cascade', required=True, select=1)
    source_account_id = fields.Many2one(
        'account.account', string='Source account',
        required=True, ondelete='cascade')
    dest_account_id = fields.Many2one(
        'account.account', string='Dest account',
        required=False, ondelete='cascade')


class fiscal_year_closing_c_account_mapping(models.Model):
    """
    Closing Account Mapping
    """

    _name = "account_fiscal_year_closing.fyc_c_account_map"
    _description = "SFYC Closing Account Mapping"

    name = fields.Char(sting='Description', size=60)
    fyc_id = fields.Many2one(
        'account_fiscal_year_closing.fyc', string='Fiscal Year Closing',
        ondelete='cascade', required=True, select=1)
    source_account_id = fields.Many2one(
        'account.account', string='Source account',
        required=True, ondelete='cascade')
    dest_account_id = fields.Many2one(
        'account.account', string='Dest account',
        required=False, ondelete='cascade')


#-------------------------------------------------------------------------------
# Fiscal Year Closing Wizard
#-------------------------------------------------------------------------------
class fiscal_year_closing(models.Model):
    """
    Fiscal Year Closing Wizard
    """

    _inherit = "account_fiscal_year_closing.fyc"

    # ---- Default values

    def _get_closing_name(self):
        return _('{year} Fiscal Year Closing'.format(
            year=datetime.now().year - 1))

    def _get_closing_fiscalyear_id(self):
        """
        Gets the last (previous) fiscal year
        """
        company = self.env.user.company_id
        str_date = '%s-06-01' % (datetime.now().year - 1)
        fiscalyear = self.env['account.fiscalyear'].search(
            [('company_id', '=', company.id),
             ('date_start', '<=', str_date),
             ('date_stop', '>=', str_date)])
        if not fiscalyear:
            fiscalyear = self.env['account.fiscalyear'].search(
                [('company_id', '=', False),
                 ('date_start', '<=', str_date),
                 ('date_stop', '>=', str_date)])
        return fiscalyear and fiscalyear[0].id

    def _get_opening_fiscalyear_id(self):
        """
        Gets the current fiscal year
        """
        company = self.env.user.company_id
        str_date = '%s-06-01' % datetime.now().year
        fiscalyear = self.env['account.fiscalyear'].search(
            [('company_id', '=', company.id),
             ('date_start', '<=', str_date),
             ('date_stop', '>=', str_date)])
        if not fiscalyear:
            fiscalyear = self.env['account.fiscalyear'].search(
                [('company_id', '=', False),
                 ('date_start', '<=', str_date),
                 ('date_stop', '>=', str_date)])
        return fiscalyear and fiscalyear[0].id

    #
    # Fields -------------------------------------------------------------------
    #

    name = fields.Char(default=_get_closing_name)
    # Company
    company_id = fields.Many2one(
        'res.company', 'Company', ondelete='cascade',
        readonly=True, required=True,
        default=lambda self: self.env['res.company']._company_default_get(
            'account_fiscal_year_closing.fyc'))
    # Fiscal years
    closing_fiscalyear_id = fields.Many2one(
        'account.fiscalyear', string='Fiscal year to close',
        required=True, ondelete='cascade', select=1,
        default=_get_closing_fiscalyear_id)
    opening_fiscalyear_id = fields.Many2one(
        'account.fiscalyear', string='Fiscal year to open',
        required=True, ondelete='cascade', select=2,
        default=_get_opening_fiscalyear_id)
    # Operations (to do), and their account moves (when done)
    create_loss_and_profit = fields.Boolean()
    loss_and_profit_move_id = fields.Many2one(
        'account.move', string='L&P Move', ondelete='set null', readonly=True)
    create_net_loss_and_profit = fields.Boolean()
    net_loss_and_profit_move_id = fields.Many2one(
        'account.move', string='Net L&P Move', 
        ondelete='set null', readonly=True)
    create_closing = fields.Boolean()
    closing_move_id = fields.Many2one(
        'account.move', string='Closing Move', 
        ondelete='set null', readonly=True)
    create_opening = fields.Boolean()
    opening_move_id = fields.Many2one(
        'account.move', string='Opening Move',
        ondelete='set null', readonly=True)
    # Extra operations
    check_invalid_period_moves = fields.Boolean(
        help="Checks that there are no moves, "
             "on the fiscal year that is being closed, "
             "with dates or periods outside that fiscal year.")
    check_draft_moves = fields.Boolean(
        help="Checks that there are no draft moves on the fiscal year "
             "that is being closed. Non-confirmed moves won't be "
             "taken in account on the closing operations.")
    check_unbalanced_moves = fields.Boolean(
        help="Checks that there are no unbalanced moves "
             "on the fiscal year that is being closed.")
    # State
    state = fields.Selection([
        ('new', 'New'),
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('canceled', 'Canceled')], default='new')
    # Loss and Profit options
    lp_description = fields.Char(size=60)
    lp_journal_id = fields.Many2one('account.journal')
    lp_period_id = fields.Many2one('account.period')
    lp_date = fields.Date()
    lp_account_mapping_ids = fields.One2many(
        'account_fiscal_year_closing.fyc_lp_account_map', 'fyc_id')
    # Net Loss and Profit options
    nlp_description = fields.Char(size=60)
    nlp_journal_id = fields.Many2one('account.journal')
    nlp_period_id = fields.Many2one('account.period')
    nlp_date = fields.Date('Date')
    nlp_account_mapping_ids = fields.One2many(
        'account_fiscal_year_closing.fyc_nlp_account_map', 'fyc_id')
    # Closing options
    c_description = fields.Char(size=60)
    c_journal_id = fields.Many2one('account.journal')
    c_period_id = fields.Many2one('account.period')
    c_date = fields.Date('Date')
    c_account_mapping_ids = fields.One2many(
        'account_fiscal_year_closing.fyc_nlp_account_map', 'fyc_id')
    # Opening options
    o_description = fields.Char(size=60)
    o_journal_id = fields.Many2one('account.journal')
    o_period_id = fields.Many2one('account.period')
    o_date = fields.Date('Date')
    o_account_mapping_ids = fields.One2many(
        'account_fiscal_year_closing.fyc_nlp_account_map', 'fyc_id')

    #
    # Workflow actions ---------------------------------------------------------
    #

    def _get_journal_id(self, cr, uid, fyc, context):
        """
        Gets the journal to use.
        (It will search for a 'GRAL' or 'General' journal)
        """
        assert fyc.company_id, "A company should have been selected"
        journal_ids = self.pool.get('account.journal').search(cr, uid, [
                            ('company_id', '=', fyc.company_id.id),
                            ('code', '=', 'GRAL'),
                        ])
        if not journal_ids:
            journal_ids = self.pool.get('account.journal').search(cr, uid, [
                            ('company_id', '=', False),
                            ('code', '=', 'GRAL'),
                        ])
        if not journal_ids:
            journal_ids = self.pool.get('account.journal').search(cr, uid, [
                            ('company_id', '=', fyc.company_id.id),
                            ('name', 'ilike', 'General'),
                        ])
        if not journal_ids:
            journal_ids = self.pool.get('account.journal').search(cr, uid, [
                            ('company_id', '=', False),
                            ('name', 'ilike', 'General'),
                        ])
        return journal_ids and journal_ids[0]

    def _get_lp_period_id(self, cr, uid, fyc, context):
        """
        Gets the period for the L&P entry
        (It searches for a "PG%" special period on the previous fiscal year)
        """
        period_ids = self.pool.get('account.period').search(cr, uid, [
                            ('fiscalyear_id', '=', fyc.closing_fiscalyear_id.id),
                            ('special', '=', True),
                            ('date_start', '=', fyc.closing_fiscalyear_id.date_stop),
                            ('code', 'ilike', 'PG'),
                        ])
        if not period_ids:
            period_ids = self.pool.get('account.period').search(cr, uid, [
                                ('fiscalyear_id', '=', fyc.closing_fiscalyear_id.id),
                                ('special', '=', True),
                                ('date_start', '=', fyc.closing_fiscalyear_id.date_stop),
                            ])
        return period_ids and period_ids[0]

    def _get_c_period_id(self, cr, uid, fyc, context):
        """
        Gets the period for the Closing entry
        (It searches for a "C%" special period on the previous fiscal year)
        """
        period_ids = self.pool.get('account.period').search(cr, uid, [
                            ('fiscalyear_id', '=', fyc.closing_fiscalyear_id.id),
                            ('special', '=', True),
                            ('date_start', '=', fyc.closing_fiscalyear_id.date_stop),
                            ('code', 'ilike', 'C'),
                        ])

        if not period_ids:
            period_ids = self.pool.get('account.period').search(cr, uid, [
                                ('fiscalyear_id', '=', fyc.closing_fiscalyear_id.id),
                                ('special', '=', True),
                                ('date_start', '=', fyc.closing_fiscalyear_id.date_stop),
                            ])
        return period_ids and period_ids[0]

    def _get_o_period_id(self, cr, uid, fyc, context):
        """
        Gets the period for the Opening entry
        (It searches for a "A%" special period on the previous fiscal year)
        """
        period_ids = self.pool.get('account.period').search(cr, uid, [
                            ('fiscalyear_id', '=', fyc.opening_fiscalyear_id.id),
                            ('special', '=', True),
                            ('date_stop', '=', fyc.opening_fiscalyear_id.date_start),
                            ('code', 'ilike', 'A'),
                        ])
        if not period_ids:
            period_ids = self.pool.get('account.period').search(cr, uid, [
                                ('fiscalyear_id', '=', fyc.opening_fiscalyear_id.id),
                                ('special', '=', True),
                                ('date_stop', '=', fyc.opening_fiscalyear_id.date_start),
                            ])
        return period_ids and period_ids[0]


    def _get_account_mappings(self, cr, uid, fyc, mapping, context):
        """
        Transforms the mapping dictionary on a list of mapping lines.
        """
        account_mappings = []
        for source, dest, description in mapping:
            #
            # Find the source account
            #
            account_ids = self.pool.get('account.account').search(cr, uid, [
                            ('company_id', '=', fyc.company_id.id),
                            ('code', '=like', source),
                        ])
            source_account_id = account_ids and account_ids[0] or None

            #
            # Find the dest account
            #
            account_ids = self.pool.get('account.account').search(cr, uid, [
                            ('company_id', '=', fyc.company_id.id),
                            ('code', '=like', dest),
                            ('type', '!=', 'view'),
                        ])
            dest_account_id = account_ids and account_ids[0] or None

            #
            # Use a default description if not provided
            #
            if not description:
                if source_account_id:
                    description = self.pool.get('account.account').read(cr, uid, source_account_id, ['name'])['name']

            #
            # If the mapping is valid for this chart of accounts
            #
            if source_account_id:
                #
                # Make sure that the dest account is valid
                #
                if dest_account_id:
                    # Add the line to the result
                    account_mappings.append({
                            'name': description,
                            'source_account_id': source_account_id,
                            'dest_account_id': dest_account_id,
                        })
                else:
                    # Add the line to the result
                    account_mappings.append({
                            'name': _('No destination account %s found for account %s.') % (dest, source),
                            'source_account_id': source_account_id,
                            'dest_account_id': None,
                        })

        return [(0, 0, acc_map) for acc_map in account_mappings]



    def action_draft(self, cr, uid, ids, context=None):
        """
        Called when the user clicks the confirm button.
        """
        if context is None:
            context = {}
        #
        # Make sure the lang is defined on the context
        #
        user = self.pool.get('res.users').browse(cr, uid, uid, context)

        for fyc in self.browse(cr, uid, ids, context):
            #
            # Check for duplicated entries
            #
            fyc_ids = self.search(cr, uid, [('name', '=', fyc.name)])
            if len(fyc_ids) > 1:
                raise UserError(_('There is already a fiscal year closing with this name.'))
            
            assert fyc.closing_fiscalyear_id and fyc.closing_fiscalyear_id.id
            fyc_ids = self.search(cr, uid, [('closing_fiscalyear_id', '=', fyc.closing_fiscalyear_id.id)])
            if len(fyc_ids) > 1:
                raise UserError(_('There is already a fiscal year closing for the fiscal year to close.'))

            assert fyc.opening_fiscalyear_id and fyc.opening_fiscalyear_id.id
            fyc_ids = self.search(cr, uid, [('opening_fiscalyear_id', '=', fyc.opening_fiscalyear_id.id)])
            if len(fyc_ids) > 1:
                raise UserError(_('There is already a fiscal year closing for the fiscal year to open.'))

            #
            # Check whether the default values of the fyc object have to be computed
            # or they have already been computed (restarted workflow)
            #
            if fyc.c_account_mapping_ids:
                # Fyc wizard reverted to 'new' after canceled

                self.write(cr, uid, [fyc.id], { 'state': 'draft' })
            else:
                # New fyc wizard object

                vals = {
                    #
                    # Perform all the operations by default
                    #
                    'create_loss_and_profit': True,
                    'create_net_loss_and_profit': False,
                    'create_closing': True,
                    'create_opening': True,

                    'check_invalid_period_moves': True,
                    'check_draft_moves': True,
                    'check_unbalanced_moves': True,

                    #
                    # L&P options
                    #
                    'lp_description': _("Loss & Profit"),
                    'lp_journal_id': self._get_journal_id(cr, uid, fyc, context),
                    'lp_period_id': self._get_lp_period_id(cr, uid, fyc, context),
                    'lp_date': fyc.closing_fiscalyear_id.date_stop,
#                    'lp_account_mapping_ids': self._get_account_mappings(cr, uid, fyc, _LP_ACCOUNT_MAPPING, context),

                    #
                    # Net L&P options
                    #
                    'nlp_description': _("Net Loss & Profit"),
                    'nlp_journal_id': self._get_journal_id(cr, uid, fyc, context),
                    'nlp_period_id': self._get_lp_period_id(cr, uid, fyc, context),
                    'nlp_date': fyc.closing_fiscalyear_id.date_stop,
#                    'nlp_account_mapping_ids': self._get_account_mappings(cr, uid, fyc, _NLP_ACCOUNT_MAPPING, context),

                    #
                    # Closing options
                    #
                    'c_description': _("Fiscal Year Closing"),
                    'c_journal_id': self._get_journal_id(cr, uid, fyc, context),
                    'c_period_id': self._get_c_period_id(cr, uid, fyc, context),
                    'c_date': fyc.closing_fiscalyear_id.date_stop,
#                    'c_account_mapping_ids': self._get_account_mappings(cr, uid, fyc, _C_ACCOUNT_MAPPING, context),

                    #
                    # Opening options
                    #
                    'o_description': _("Fiscal Year Opening"),
                    'o_journal_id': self._get_journal_id(cr, uid, fyc, context),
                    'o_period_id': self._get_o_period_id(cr, uid, fyc, context),
                    'o_date': fyc.opening_fiscalyear_id.date_start,

                    # *** New state ***
                    'state': 'draft',
                }
                self.write(cr, uid, [fyc.id], vals)
        return True


    def action_run(self, cr, uid, ids, context=None):
        """
        Called when the create entries button is used.
        """
        # Note: Just change the state, everything else is done on the run wizard
        #       *before* this action is called.
        self.write(cr, uid, ids, {'state': 'in_progress'})
        return True


    def action_confirm(self, cr, uid, ids, context=None):
        """
        Called when the user clicks the confirm button.
        """
        if context is None:
            context = {}
        #
        # Make sure the lang is defined on the context
        #
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        context['lang'] = context.get('lang') or user.lang

        for fyc in self.browse(cr, uid, ids, context):
            #
            # Require the L&P, closing, and opening moves to exist (NL&P is optional)
            #
            if not fyc.loss_and_profit_move_id:
                raise UserError(_("The Loss & Profit move is required"))
            if not fyc.closing_move_id:
                raise UserError(_("The Closing move is required"))
            if not fyc.opening_move_id:
                raise UserError(_("The Opening move is required"))

            ''' needed ?
            
            #
            # Calculate the moves to check
            #
            moves = []
            moves.append(fyc.loss_and_profit_move_id)
            if fyc.net_loss_and_profit_move_id:
                moves.append(fyc.net_loss_and_profit_move_id)
            moves.append(fyc.closing_move_id)
            moves.append(fyc.opening_move_id)

            #
            # Check and reconcile each of the moves
            #
            for move in moves:
                netsvc.Logger().notifyChannel('fyc', netsvc.LOG_DEBUG, "Checking %s" % move.ref)
                #
                # Check if it has been confirmed
                #
                if move.state == 'draft':
                    raise UserError(_("Some moves are in draft state!"), _("You have to review and confirm each of the moves before continuing"))
                #
                # Check the balance
                #
                amount = 0
                for line in move.line_id:
                    amount += (line.debit - line.credit)
                if abs(amount) > 0.5 * 10 ** -int(self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')):
                    raise (_("Some moves are unbalanced!"), _("All the moves should be balanced before continuing"))

                #
                # Reconcile the move
                #
                # Note: We will reconcile all the lines, even the 'not reconcile' ones,
                #       to prevent future problems (the user may change the
                #       reconcile option of an account in the future)
                #
                netsvc.Logger().notifyChannel('fyc', netsvc.LOG_DEBUG, "Reconcile %s" % move.ref)
                tmp_context = context.copy()
                tmp_context['fy_closing'] = True # Fiscal year closing = reconcile everything
                line_ids = [line.id for line in move.line_id]
                self.pool.get('account.move.line').reconcile(cr, uid, line_ids, context=tmp_context)

            #
            # Close the fiscal year and it's periods
            #
            # Note: We can not just do a write, cause it would raise a
            #       "You can not modify/delete a journal with entries for this period!"
            #       so we have to do it on SQL level :(
            #       This is based on the "account.fiscalyear.close.state" wizard.
            #
            netsvc.Logger().notifyChannel('fyc', netsvc.LOG_DEBUG, "Closing fiscal year")
            query = """
                    UPDATE account_journal_period
                    SET state = 'done'
                    WHERE period_id IN (SELECT id FROM account_period WHERE fiscalyear_id = %d)
                    """
            cr.execute(query % fyc.closing_fiscalyear_id.id)
            query = """
                    UPDATE account_period
                    SET state = 'done'
                    WHERE fiscalyear_id = %d
                    """
            cr.execute(query % fyc.closing_fiscalyear_id.id)
            query = """
                    UPDATE account_fiscalyear
                    SET state = 'done'
                    WHERE id = %d
                    """
            cr.execute(query % fyc.closing_fiscalyear_id.id)
            
            '''

        # Done
        self.write(cr, uid, ids, {'state': 'done'})
        return True


    def action_cancel(self, cr, uid, ids, context=None):
        """
        Called when the user clicks the cancel button.
        """
        if context is None:
            context = {}
        #
        # Make sure the lang is defined on the context
        #
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        context['lang'] = context.get('lang') or user.lang

        #
        # Uncheck all the operations
        #
        self.pool.get('account_fiscal_year_closing.fyc').write(cr, uid, ids, {
                    'create_loss_and_profit': False,
                    'create_net_loss_and_profit': False,
                    'create_closing': False,
                    'create_opening': False,
                    'check_invalid_period_moves': False,
                    'check_draft_moves': False,
                    'check_unbalanced_moves': False,
                }, context=context)

        ''' needed? 

        #
        # Open the fiscal year and it's periods
        #
        # Note: We can not just do a write, cause it would raise a
        #       "You can not modify/delete a journal with entries for this period!"
        #       so we have to do it on SQL level :(
        #       This is based on the "account.fiscalyear.close.state" wizard.
        #
        # TODO check this for 6.1
        
        for fyc in self.browse(cr, uid, ids, context):
            query = """
                    UPDATE account_journal_period
                    SET state = 'draft'
                    WHERE period_id IN (SELECT id FROM account_period WHERE fiscalyear_id = %d)
                    """
            cr.execute(query % fyc.closing_fiscalyear_id.id)
            query = """
                    UPDATE account_period
                    SET state = 'draft'
                    WHERE fiscalyear_id = %d
                    """
            cr.execute(query % fyc.closing_fiscalyear_id.id)
            query = """
                    UPDATE account_fiscalyear
                    SET state = 'draft'
                    WHERE id = %d
                    """
            cr.execute(query % fyc.closing_fiscalyear_id.id)

        '''

        for fyc in self.browse(cr, uid, ids, context):
            if fyc.loss_and_profit_move_id:
                fyc.loss_and_profit_move_id.unlink()
            if fyc.net_loss_and_profit_move_id:
                fyc.net_loss_and_profit_move_id.unlink()
            if fyc.closing_move_id:
                fyc.closing_move_id.unlink()
            if fyc.opening_move_id:
                fyc.opening_move_id.unlink()

        # Canceled
        self.write(cr, uid, ids, {'state': 'canceled'})
        return True


    def action_recover(self, cr, uid, ids, context=None):
        """
        Called when the user clicks the draft button to create
        a new workflow instance.
        """
        self.write(cr, uid, ids, {'state': 'new'})
        wf_service = netsvc.LocalService("workflow")
        for item_id in ids:
            wf_service.trg_delete(
                uid, 'account_fiscal_year_closing.fyc', item_id, cr)
            wf_service.trg_create(
                uid, 'account_fiscal_year_closing.fyc', item_id, cr)
            wf_service.trg_validate(
                uid, 'account_fiscal_year_closing.fyc', item_id, 'draft', cr)
        return True
