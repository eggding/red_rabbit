#include "rpc/ffrpc_ops.h"

void register_broker_client_req()
{
    register_broker_client_t::in_t msg;
    msg.binder_broker_node_id = 0
    msg.service_name          = m_service_name;
}