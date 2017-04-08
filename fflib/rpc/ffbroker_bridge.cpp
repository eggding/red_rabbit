#include "rpc/ffbroker.h"
#include "rpc/ffbroker_bridge.h"
#include "base/log.h"

using namespace ff;

ffbroker_bridge_t::ffbroker_bridge_t():
    m_ffbroker(NULL)
{
    
}
ffbroker_bridge_t::~ffbroker_bridge_t()
{
    
}

//! [4]
//! 处理broker bridge 转发给broker master的消息
int ffbroker_bridge_t::handle_bridge_to_broker_route_msg(bridge_route_to_broker_t::in_t& msg_, socket_ptr_t sock_)
{
    //! 需要转发给broker client
    broker_route_t::in_t dest_msg;
    dest_msg.from_node_id = msg_.from_node_id;//! 来自哪个节点
    
    dest_msg.dest_node_id = msg_.dest_node_id;//! 需要转发到哪个节点上
    
    //! 记录所有服务/接口信息
    if (dest_msg.dest_node_id == 0 && msg_.service_name.empty() == false)//! 说明是调用消息
    {
        map<uint32_t, ffbroker_t::broker_client_info_t>::iterator it = get_ffbroker().m_broker_client_info.begin();//! node id -> service
        for (; it != get_ffbroker().m_broker_client_info.end(); ++it)
        {
            if (it->second.service_name == msg_.service_name)
            {
                dest_msg.dest_node_id = it->first;
                break;
            }
        }
    }

    dest_msg.msg_id = get_ffbroker().m_msg2id[msg_.msg_name];//! 调用的是哪个接口
    dest_msg.callback_id = msg_.callback_id;
    dest_msg.body = msg_.body;
    
    uint32_t bridge_node_id = sock_->get_data<ffbroker_t::session_data_t>()->get_node_id();
    dest_msg.bridge_route_id = get_ffbroker().m_broker_bridge_info[bridge_node_id].broker_group_id[msg_.from_broker_group_name];
    LOGINFO((BROKER, "ffbroker_t::handle_bridge_to_broker_route_msg begin dest node id[%u], bridge_node_id[%u], dest_msg.bridge_route_id[%u]",
             msg_.dest_node_id, bridge_node_id, dest_msg.bridge_route_id));
    return get_ffbroker().route_msg_to_broker_client(dest_msg);
}



//! 处理broker master 注册到broker bridge
int ffbroker_bridge_t::handle_broker_register_bridge(register_bridge_broker_t::in_t& msg_, socket_ptr_t sock_)
{
    ffbroker_t::session_data_t* psession = new ffbroker_t::session_data_t(get_ffbroker().alloc_id());
    sock_->set_data(psession);
    get_ffbroker().m_broker_group_info[msg_.broker_group].sock = sock_;
    
    register_bridge_broker_t::out_t out_msg;
    map<string/*group name*/, ffbroker_t::broker_group_info_t>::iterator it = get_ffbroker().m_broker_group_info.begin();
    for (; it != get_ffbroker().m_broker_group_info.end(); ++it)
    {
        out_msg.broker_group.insert(it->first);
    }
    for (it = get_ffbroker().m_broker_group_info.begin(); it != get_ffbroker().m_broker_group_info.end(); ++it)
    {
        msg_sender_t::send(it->second.sock, BRIDGE_SYNC_DATA, out_msg);
    }
    LOGINFO((BROKER, "ffbroker_t::handle_broker_register_bridge end ok broker group[%s]", msg_.broker_group));
    return 0;
}

//! [3] bridge的处理函数，从broker master转发到另外的broker master
int ffbroker_bridge_t::bridge_handle_broker_to_broker_msg(bridge_route_to_broker_t::in_t& msg_, socket_ptr_t sock_)
{
    map<string/*group name*/, ffbroker_t::broker_group_info_t>::iterator it = get_ffbroker().m_broker_group_info.find(msg_.dest_broker_group_name);
    if (it == get_ffbroker().m_broker_group_info.end())
    {
        return -1;
    }
    
    msg_sender_t::send(it->second.sock, BRIDGE_TO_BROKER_ROUTE_MSG, msg_);
    LOGINFO((BROKER, "ffbroker_t::bridge_handle_broker_to_broker_msg end ok dest node id[%u]", msg_.dest_node_id));
    return 0;
}

int ffbroker_bridge_t::handle_bridge_sync_data(register_bridge_broker_t::out_t& msg_, socket_ptr_t sock_)
{
    if (NULL == sock_->get_data<ffbroker_t::session_data_t>())
    {
        return 0;
    }
    uint32_t node_id = sock_->get_data<ffbroker_t::session_data_t>()->get_node_id();
    for (set<string>::iterator it = msg_.broker_group.begin(); it != msg_.broker_group.end(); ++it)
    {
        get_ffbroker().m_broker_bridge_info[node_id].broker_group_id[*it] = get_ffbroker().alloc_id();
        LOGINFO((BROKER, "ffbroker_t::handle_bridge_sync_data broker group [%s]", *it));
    }

    return 0;
}

