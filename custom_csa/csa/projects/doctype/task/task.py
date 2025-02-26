import frappe


@frappe.whitelist()
def get_children(doctype, parent, task=None, project=None, status=None, is_root=False):

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

    tasks = frappe.get_list(
        doctype,
        fields=["name as value", "subject as title", "is_group as expandable"],
        filters=filters,
        order_by="name",
    )

    return tasks