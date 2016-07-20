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

{
    "name": "Fiscal Year Closing",
    "version": "8.0.1.0.0",
    "category": "Generic Modules/Accounting",
    "website": "https://odoo-community.org/",
    "author": "Odoo Italian Community,Pexego, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/fyc_workflow.xml",
        "views/wizard_populate_mapping.xml",
        "views/wizard_run.xml",
        "views/fyc_view.xml",
        "views/hide_account_wizards.xml",
    ],
}
