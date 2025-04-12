import contextvars

request_id_ctx_var = contextvars.ContextVar("request_id", default=None)
tenant_id_ctx_var = contextvars.ContextVar("tenant_id", default=None)


def set_request_context(request_id: str, tenant_id: str):
    request_id_ctx_var.set(request_id)
    tenant_id_ctx_var.set(tenant_id)


def get_request_id():
    return request_id_ctx_var.get()


def get_tenant_id():
    return tenant_id_ctx_var.get()
