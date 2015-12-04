# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2012 OpenERP - Team de Localización Argentina.
# https://launchpad.net/~openerp-l10n-ar-localization
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api
from openerp.exceptions import Warning


class sale_order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    @api.v7
    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        """
        """
        if context is None:
            context = {}
        invoice_vals = super(sale_order, self)._prepare_invoice(
            cr, uid, order, lines, context)

        partner_obj = self.pool.get('res.partner')
        partner_id = invoice_vals['partner_id']
        company_id = invoice_vals['company_id']

        journal_ids = partner_obj.prefered_journals(
            cr, uid, [partner_id], 'out_invoice',
            {'company_id': company_id}
        )

        if not journal_ids or not journal_ids[partner_id]:
            raise Warning('Please define sales journal for this company:'
                          ' "%s" (id:%d).' %
                          (order.company_id.name, order.company_id.id))

        invoice_vals['journal_id'] = journal_ids[partner_id][0]
        return invoice_vals

sale_order()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
