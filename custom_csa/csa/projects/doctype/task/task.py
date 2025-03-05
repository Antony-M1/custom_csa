import frappe


@frappe.whitelist()
def get_children(doctype, parent, task=None, project=None, status=None, exp_start_date=None, exp_end_date=None, is_root=False):

    filters = [["docstatus", "<", "2"]]

    if task:
        filters.append(["parent_task", "=", task])
    elif parent and not is_root:
        # via expand child
        filters.append(["parent_task", "=", parent])
    else:
        filters.append(['ifnull(`parent_task`, "")', "=", ""])

    if project:
        filters.append(["project", "=", project])
    
    if status:
        filters.append(["status", "=", status])

    if exp_start_date:
        filters.append(["exp_start_date", ">=", exp_start_date])
    if exp_end_date:
        filters.append(["exp_end_date", "<=", exp_end_date])

    tasks = frappe.get_list(
        doctype,
        fields=["name as value", "subject as title", "is_group as expandable"],
        filters=filters,
        order_by="name",
    )

    return tasks