from . import models


def _post_install_put_product_standard_price_in_tasks(env):
    cond = [("sale_line_product_id", "!=", False)]
    tasks = env["project.task"].search(cond)
    for task in tasks:
        task.product_standard_price = task.sale_line_product_id.standard_price
