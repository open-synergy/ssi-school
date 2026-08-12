# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


class CommonTestMixin:  # pylint: disable=too-few-public-methods
    """Provide the shared billing fixtures reused across test classes.

    The mixin builds one income account, one service product and one
    pricelist so that unrelated test classes do not each invent their
    own billing master data.

    Usage::

        class TestMyCase(CommonTestMixin, YamlTransactionCase):
            @classmethod
            def setUpClass(cls):
                super().setUpClass()
                # cls.product, cls.account and cls.pricelist are ready
    """

    @classmethod
    def setUpClass(cls):  # pylint: disable=invalid-name
        """Create the shared income account, product and pricelist.

        The records are exposed as ``cls.account``, ``cls.product`` and
        ``cls.pricelist`` so that every test class mixing this in starts
        from the same billing master data.
        """
        super().setUpClass()

        cls.account_type_income = cls.env.ref("account.data_account_type_revenue")

        cls.account = cls.env["account.account"].create(
            {
                "name": "School Fee Income",
                "code": "COMMON4200",
                "user_type_id": cls.account_type_income.id,
            }
        )

        cls.product = cls.env["product.product"].create(
            {
                "name": "School Fee",
                "type": "service",
                "list_price": 1_000_000.0,
            }
        )

        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Standard School Pricelist",
                "currency_id": cls.env.company.currency_id.id,
            }
        )
