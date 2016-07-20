.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
Account Fiscal Year Closing
===========================

Generalization of l10n_es_fiscal_year_closing (
https://github.com/OCA/l10n-spain/tree/8.0/l10n_es_fiscal_year_closing )
Fiscal Year Closing Wizard

Replaces the default OpenERP end of year wizards (from account module)
with a more advanced all-in-one wizard that will let the users:
- Check for unbalanced moves, moves with invalid dates
or period or draft moves on the fiscal year to be closed.
- Create the Loss and Profit entry.
- Create the Net Loss and Profit entry.
- Create the Closing entry.
- Create the Opening entry.

It is stateful, saving all the info about the fiscal year closing, so the
user can cancel and undo the operations easily.

Usage
=====

To use this module, you need to:

#. Run "Close Fiscal Year" wizard from
    Account - Periodic Processing - End Period

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/122/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/l10n-italy/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Borja López Soilán (Pexego) - borja@kami.es
* Lorenzo Battistini - lorenzo.battistini@agilebg.com

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.