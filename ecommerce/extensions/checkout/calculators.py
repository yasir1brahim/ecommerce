from oscar.core import prices
import logging

class OrderTotalCalculator(object):
    """
    Calculator class for calculating the order total.
    """

    def __init__(self, request=None):
        # We store a reference to the request as the total may
        # depend on the user or the other checkout data in the session.
        # Further, it is very likely that it will as shipping method
        # always changes the order total.
        self.request = request

    def calculate(self, basket, shipping_charge, **kwargs):
        excl_tax = basket.total_excl_tax + shipping_charge.excl_tax
        if basket.is_tax_known and shipping_charge.is_tax_known:
            incl_tax = basket.total_incl_tax + shipping_charge.incl_tax
            incl_tax = round(incl_tax, 2)
        else:
            incl_tax = None
            incl_tax = basket.total_incl_tax
        return prices.Price(
            currency=basket.currency,
            excl_tax=excl_tax, incl_tax=incl_tax)
