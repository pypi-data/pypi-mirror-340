# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _
from lino.core import actions
from lino.utils.html import E
from lino.modlib.memo.mixins import body_subject_to_elems

from lino_xl.lib.accounting.choicelists import VoucherTypes
from lino_xl.lib.accounting.ui import PartnerVouchers, ByJournal, PrintableByJournal
from lino_xl.lib.accounting.roles import LedgerStaff, LedgerUser
from lino_xl.lib.invoicing.ui import InvoicingsByGenerator

has_payment_methods = dd.get_plugin_setting('accounting', 'has_payment_methods',
                                            False)


class PaperTypes(dd.Table):
    model = 'trading.PaperType'
    required_roles = dd.login_required(LedgerStaff)
    column_names = 'name template *'


class TradingVouchers(PartnerVouchers):
    pass


# class MakeCopy(dd.Action):
#     button_text = u"\u2042"  # ASTERISM (⁂)

#     label = _("Make copy")
#     show_in_workflow = True
#     show_in_toolbar = False
#     copy_item_fields = set('product total_incl unit_price qty'.split())

#     parameters = dict(
#         partner=dd.ForeignKey('contacts.Partner'),
#         product=dd.ForeignKey('products.Product', blank=True),
#         subject=models.CharField(
#             _("Subject"), max_length=200, blank=True),
#         your_ref=models.CharField(
#             _("Your ref"), max_length=200, blank=True),
#         entry_date=models.DateField(_("Entry date")),
#         total_incl=dd.PriceField(_("Total incl VAT"), blank=True),
#     )
#     params_layout = """
#     entry_date partner
#     your_ref
#     subject
#     product total_incl
#     """

#     def action_param_defaults(self, ar, obj, **kw):
#         kw = super(MakeCopy, self).action_param_defaults(ar, obj, **kw)
#         kw.update(your_ref=obj.your_ref)
#         kw.update(subject=obj.subject)
#         kw.update(entry_date=obj.entry_date)
#         kw.update(partner=obj.partner)
#         # qs = obj.items.all()
#         # if qs.count():
#         #     kw.update(product=qs[0].product)
#         # kw.update(total_incl=obj.total_incl)
#         return kw

#     def run_from_ui(self, ar, **kw):
#         VoucherStates = rt.models.accounting.VoucherStates
#         obj = ar.selected_rows[0]
#         pv = ar.action_param_values
#         kw = dict(
#             journal=obj.journal,
#             user=ar.get_user(),
#             partner=pv.partner, entry_date=pv.entry_date,
#             subject=pv.subject,
#             your_ref=pv.your_ref)

#         new = obj.__class__(**kw)
#         new.fill_defaults()
#         new.full_clean()
#         new.save()
#         if pv.total_incl:
#             if not pv.product:
#                 qs = obj.items.all()
#                 if qs.count():
#                     pv.product = qs[0].product
#             item = new.add_voucher_item(
#                 total_incl=pv.total_incl, product=pv.product)
#             item.total_incl_changed(ar)
#             item.full_clean()
#             item.save()
#         else:
#             for olditem in obj.items.all():
#                 # ikw = dict()
#                 # for k in self.copy_item_fields:
#                 #     ikw[k] = getattr(olditem, k)
#                 ikw = { k: getattr(olditem, k)
#                         for k in self.copy_item_fields}
#                 item = new.add_voucher_item(**ikw)
#                 item.total_incl_changed(ar)
#                 item.full_clean()
#                 item.save()

#         new.full_clean()
#         new.register_voucher(ar)
#         new.state = VoucherStates.registered
#         new.save()
#         ar.goto_instance(new)
#         ar.success()


class InvoiceDetail(dd.DetailLayout):
    main = "general more accounting"

    general = dd.Panel("""
    panel1:20 panel2:30 panel3:25 totals:20
    ItemsByInvoice
    """,
                       label=_("General"))

    more = dd.Panel("""
    id user language #project #item_vat
    intro
    """,
                    label=_("More"))

    accounting = dd.Panel("""
    #voucher_date journal accounting_period number #narration match
    vat.MovementsByVoucher
    """ + "storage.MovementsByVoucher\n" if dd.is_installed("storage") else "",
                          label=_("Ledger"))

    totals = dd.Panel("""
    total_base
    total_vat
    total_incl
    workflow_buttons
    """)

    panel1 = dd.Panel("""
    entry_date
    payment_method
    payment_term
    due_date:20
    """)

    panel2 = dd.Panel("""
    partner
    vat_regime
    subject
    your_ref
    """)

    panel3 = dd.Panel("""
    invoicing_min_date
    invoicing_max_date
    paper_type
    printed
    """)  # sales_remark


class Invoices(TradingVouchers):
    model = 'trading.VatProductInvoice'
    required_roles = dd.login_required(LedgerUser)
    order_by = ["-id"]
    # order_by = ["journal", "accounting_period__year", "number"]
    column_names = "id entry_date partner total_incl user *"
    detail_layout = 'trading.InvoiceDetail'
    insert_layout = dd.InsertLayout("""
    journal
    partner entry_date
    subject
    """,
                                    window_size=(40, 'auto'))
    # parameters = dict(
    #     state=VoucherStates.field(blank=True),
    #     **TradingVouchers.parameters)

    # start_at_bottom = True

    # @classmethod
    # def get_request_queryset(cls, ar):
    #     qs = super(Invoices, cls).get_request_queryset(ar)
    #     pv = ar.param_values
    #     if pv.state:
    #         qs = qs.filter(state=pv.state)
    #     return qs


class InvoicesByJournal(Invoices, ByJournal):
    quick_search_fields = "partner subject"
    order_by = ["accounting_period__year", "number"]
    # start_at_bottom = True
    insert_layout = """
    partner entry_date
    subject
    """
    params_panel_hidden = True
    params_layout = "partner start_period end_period #year state cleared "
    column_names = "number_with_year entry_date #due_date " \
        "invoicing_min_date invoicing_max_date " \
        "partner " \
        "subject:10 total_incl " \
        "workflow_buttons *"


VoucherTypes.add_item_lazy(InvoicesByJournal)

if has_payment_methods:

    class CashInvoiceDetail(InvoiceDetail):
        main = "sales_tab general more accounting"

        sales_tab = dd.Panel("""
        partner payment_method total_incl
        cash_received cash_to_return balance_to_pay
        ItemsByInvoice
        """,
                             label=_("Sales"))

        panel3 = dd.Panel("""
        match
        # payment_method
        paper_type
        printed
        """)  # sales_remark

    class CashInvoices(Invoices):
        model = 'trading.CashInvoice'

    class CashInvoicesByJournal(CashInvoices, ByJournal):
        column_names = "number_with_year entry_date " \
            "partner " \
            "total_incl payment_method cash_received cash_returned " \
            "workflow_buttons *"
        insert_layout = """
        partner
        user
        """
        detail_layout = 'trading.CashInvoiceDetail'

    VoucherTypes.add_item_lazy(CashInvoicesByJournal)


class PrintableInvoicesByJournal(PrintableByJournal, Invoices):
    label = _("Sales invoice journal")


class DueInvoices(Invoices):
    label = _("Due invoices")
    order_by = ["due_date"]

    column_names = "due_date journal__ref number " \
        "partner " \
        "total_incl balance_before balance_to_pay *"

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        kw.update(cleared=dd.YesNo.no)
        return kw


class InvoiceItemDetail(dd.DetailLayout):
    main = """
    seqno product discount
    unit_price qty total_base total_vat total_incl
    title #peppol_vat_category:5
    invoiceable_type:15 invoiceable_id:15 invoiceable:50
    description"""

    window_size = (80, 20)


class InvoiceItems(dd.Table):
    """Shows all sales invoice items."""
    model = 'trading.InvoiceItem'
    required_roles = dd.login_required(LedgerStaff)
    auto_fit_column_widths = True
    # hidden_columns = "seqno description total_base total_vat"

    detail_layout = 'trading.InvoiceItemDetail'

    insert_layout = """
    product discount qty
    title
    """

    stay_in_grid = True


class ItemsByInvoice(InvoiceItems):
    label = _("Content")
    master_key = 'voucher'
    order_by = ["seqno"]
    required_roles = dd.login_required(LedgerUser)
    # column_names = "product title discount unit_price qty item_total *"
    if dd.plugins.vat.item_vat:
        column_names = "product title discount unit_price qty total_incl invoiceable *"
    else:
        column_names = "product title discount unit_price qty total_base invoiceable *"


"""
The following two classes are used by the `trading.print_items_table` plugin
setting.
"""


class ItemsByInvoicePrint(ItemsByInvoice):
    # column_names = "description_print unit_price qty item_total"
    if dd.plugins.vat.item_vat:
        column_names = "description_print unit_price qty total_incl"
    else:
        column_names = "description_print unit_price qty total_base"
    include_qty_in_description = False

    @dd.displayfield(_("Description"))
    def description_print(cls, self, ar):
        title = self.title or str(self.product)
        elems = body_subject_to_elems(ar, title, self.description)
        # dd.logger.info("20160511a %s", cls)
        if cls.include_qty_in_description:
            if self.qty is not None and self.qty != 1:
                elems += [
                    " ",
                    _("({qty}*{unit_price}/{unit})").format(
                        qty=self.quantity,
                        unit=self.product.delivery_unit,
                        unit_price=self.unit_price)
                ]
        e = E.div(*elems)
        # dd.logger.info("20160704d %s", tostring(e))
        return e


class ItemsByInvoicePrintNoQtyColumn(ItemsByInvoicePrint):
    if dd.plugins.vat.item_vat:
        column_names = "description_print total_incl"
    else:
        column_names = "description_print total_base"
    include_qty_in_description = True
    hide_sums = True


# 20220512 VatProductInvoice.print_items_table = ItemsByInvoicePrint


class InvoiceItemsByProduct(InvoiceItems):
    master_key = 'product'
    column_names = "voucher voucher__partner qty title \
description:20x1 discount unit_price total_incl total_base total_vat"

    editable = False
    # auto_fit_column_widths = True


class InvoiceItemsByGenerator(InvoicingsByGenerator):
    model = 'trading.InvoiceItem'
    column_names = "voucher qty title description:20x1 #discount " \
                   "unit_price total_incl #total_base #total_vat *"


class SignAction(actions.Action):
    label = "Sign"

    def run_from_ui(self, ar):

        def ok(ar):
            for row in ar.selected_rows:
                row.instance.user = ar.get_user()
                row.instance.save()
            ar.success(refresh=True)

        ar.confirm(
            ok,
            _("Going to sign %d documents as user %s. Are you sure?") %
            (len(ar.selected_rows), ar.get_user()))


class DocumentsToSign(Invoices):
    use_as_default_table = False
    filter = dict(user__isnull=True)
    # can_add = perms.never
    column_names = "number:4 #order entry_date " \
        "partner:10 " \
        "subject:10 total_incl total_base total_vat "
    # actions = Invoices.actions + [ SignAction() ]


class InvoicesByPartner(Invoices):
    # model = 'trading.VatProductInvoice'
    order_by = ["-entry_date", '-id']
    master_key = 'partner'
    column_names = "entry_date detail_link total_incl "\
                   "workflow_buttons *"
    # column_names = "entry_date journal__ref number total_incl "\
    #                "workflow_buttons *"


# class SalesByPerson(TradingVouchers):
# column_names = "journal:4 number:4 date:8 " \
# "total_incl total_base total_vat *"
# order_by = ["date"]
# master_key = 'person'


class ProductDetailMixin(dd.DetailLayout):
    sales = dd.Panel("""
    trading.InvoiceItemsByProduct
    """,
                     label=dd.plugins.trading.verbose_name)
