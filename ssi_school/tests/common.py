# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


class CommonTestMixin:
    """Mixin yang menyediakan fixture bersama (product, account, pricelist)
    yang dapat digunakan ulang di berbagai kelas unit test.

    Cara penggunaan::

        class TestMyCase(CommonTestMixin, SavepointCase):
            @classmethod
            def setUpClass(cls):
                super().setUpClass()
                # cls.product, cls.account, cls.pricelist sudah tersedia
    """

    @classmethod
    def setUpClass(cls):
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
