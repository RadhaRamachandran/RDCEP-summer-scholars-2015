__author__ = 'Ben'
from mechanize import Browser

br = Browser()
br.open("http://311request.cityofchicago.org/reports/new?service_id=4fd3b656e750846c53000004")
br.select_form(nr=0)
# Browser passes through unknown attributes (including methods)
# to the selected HTMLForm (from ClientForm).
br[""] = ["mozzarella", "caerphilly"]  # (the method here is __setitem__)
response = br.submit()  # submit current form