#include "rpc/ffgate.h"
#include "net/net_factory.h"
#include "base/log.h"
#include "net/socket_op.h"

using namespace ff;

#define FFGATE                   "FFGATE"

ffgate_t::ffgate_t()
{
    
}
ffgate_t::~ffgate_t()
{
    
}

int ffgate_t::open(arg_helper_t& arg_helper)
{
    LOGTRACE((FFGATE, "ffgate_t::open begin broker<%s>", arg_helper.get_option_value("-broker")));
    if (false == arg_helper.is_enable_option("-gate"))
    {
        LOGERROR((FFGATE, "ffgate_t::open failed without -gate argmuent"));
        return -1;
    }
    m_gate_name = arg_helper.get_option_value("-gate");
    m_ffrpc = new ffrpc_t(m_gate_name);
    
    m_ffrpc->reg(&ffgate_t::change_session_logic, this);
    m_ffrpc->reg(&ffgate_t::close_session, this);
    m_ffrpc->reg(&ffgate_t::route_msg_to_session, this);
    m_ffrpc->reg(&ffgate_t::broadcast_msg_to_session, this);
    
    cout << arg_helper.get_option_value("-broker") << endl;
    if (m_ffrpc->open(arg_helper.get_option_value("-broker")))
    {
        LOGERROR((FFGATE, "ffgate_t::open failed check -broker argmuent"));
        return -1;
    }
    
    if (NULL == net_factory_t::gateway_listen(arg_helper, this))
    {
        LOGERROR((FFGATE, "ffgate_t::open failed without -gate_listen"));
        return -1;
    }
    
    LOGTRACE((FFGATE, "ffgate_t::open end ok"));
    return 0;
}
int ffgate_t::close()
{
    if (m_ffrpc)
    {
        m_ffrpc->close();
    }
    return 0;
}

//! 处理连接断开
int ffgate_t::handle_broken(socket_ptr_t sock_)
{
    m_ffrpc->get_tq().produce(task_binder_t::gen(&ffgate_t::handle_broken_impl, this, sock_));
    return 0;
}
//! 处理消息
int ffgate_t::handle_msg(const message_t& msg_, socket_ptr_t sock_)
{
    m_ffrpc->get_tq().produce(task_binder_t::gen(&ffgate_t::handle_msg_impl, this, msg_, sock_));
    return 0;
}

//! 处理连接断开
int ffgate_t::handle_broken_impl(socket_ptr_t sock_)
{
    LOGTRACE((FFGATE, "ffgate_t::broken begin"));
    session_data_t* session_data = sock_->get_data<session_data_t>();
    if (NULL == session_data)
    {
        sock_->safe_delete();
        return 0;
    }
    
    if (false == session_data->is_valid())
    {
        //! 还未通过验证
        m_wait_verify_set.erase(sock_);
    }
    else
    {
        client_info_t& client_info = m_client_set[session_data->id()];
        if (client_info.sock == sock_)
        {
            session_offline_t::in_t msg;
            msg.session_id  = session_data->id();
            msg.online_time = session_data->online_time;
            m_ffrpc->call(DEFAULT_LOGIC_SERVICE, msg);
            m_client_set.erase(session_data->id());
        }
    }
    LOGTRACE((FFGATE, "ffgate_t::broken session_id[%ld]", session_data->id()));
    delete session_data;
    sock_->set_data(NULL);
    sock_->safe_delete();
    return 0;
}
//! 处理消息
int ffgate_t::handle_msg_impl(const message_t& msg_, socket_ptr_t sock_)
{
    session_data_t* session_data = sock_->get_data<session_data_t>();
    if (NULL == session_data)//! 还未验证sessionid
    {
        return verify_session_id(msg_, sock_);
    }
    else if (false == session_data->is_valid())
    {
        //! sessionid再未验证之前，client是不能发送消息的
        sock_->close();
        return 0;
    }
    else
    {
        return route_logic_msg(msg_, sock_);
    }
    return 0;
}

//! 验证sessionid
int ffgate_t::verify_session_id(const message_t& msg_, socket_ptr_t sock_)
{
    string ip = socket_op_t::getpeername(sock_->socket());
    LOGTRACE((FFGATE, "ffgate_t::verify_session_id session_key len=%u, ip[%s]", msg_.get_body().size(), ip));
    if (ip.empty())
    {
        sock_->close();
        return -1;
    }
    session_data_t* session_data = new session_data_t();
    sock_->set_data(session_data);
    //! 还未通过验证
    m_wait_verify_set.insert(sock_);

    session_verify_t::in_t msg;
    msg.session_key = msg_.get_body();
    msg.online_time = session_data->online_time;
    msg.gate_name   = m_gate_name;
    msg.ip          = ip;
    m_ffrpc->call(DEFAULT_LOGIC_SERVICE, msg, ffrpc_ops_t::gen_callback(&ffgate_t::verify_session_callback, this, sock_));
    LOGTRACE((FFGATE, "ffgate_t::verify_session_id end ok"));
    return 0;
}
//! 验证sessionid 的回调函数
int ffgate_t::verify_session_callback(ffreq_t<session_verify_t::out_t>& req_, socket_ptr_t sock_)
{
    LOGINFO((FFGATE, "ffgate_t::verify_session_callback session_id[%ld], err[%s]", req_.arg.session_id, req_.arg.err));
    set<socket_ptr_t>::iterator it = m_wait_verify_set.find(sock_);
    if (it == m_wait_verify_set.end())
    {
        //! 连接已经断开
        return 0;
    }
    m_wait_verify_set.erase(it);
    
    if (false == req_.arg.err.empty() || req_.arg.session_id == 0)
    {

        if (false == req_.arg.extra_data.empty())
        {
            msg_sender_t::send(sock_, 0, req_.arg.extra_data);
        }
        LOGTRACE((FFGATE, "ffgate_t::close connection"));
        sock_->close();
        return 0;
    }
    session_data_t* session_data = sock_->get_data<session_data_t>();
    session_data->set_id(req_.arg.session_id);
    client_info_t& client_info = m_client_set[session_data->id()];
    if (client_info.sock)
    {
        client_info.sock->close();
        LOGINFO((FFGATE, "ffgate_t::verify_session_callback reconnect, close old session_id[%ld]", req_.arg.session_id));
    }
    client_info.sock = sock_;

    if (false == req_.arg.extra_data.empty())
    {
        msg_sender_t::send(client_info.sock, 0, req_.arg.extra_data);
    }
    session_enter_scene_t::in_t enter_msg;
    enter_msg.session_id = session_data->id();
    enter_msg.from_gate = m_gate_name;
    //enter_msg.from_scene = "";
    enter_msg.to_scene = DEFAULT_LOGIC_SERVICE;
    //enter_msg.extra_data = "";
    m_ffrpc->call(DEFAULT_LOGIC_SERVICE, enter_msg, ffrpc_ops_t::gen_callback(&ffgate_t::enter_scene_callback, this, session_data->id()));
    LOGTRACE((FFGATE, "ffgate_t::verify_session_callback end ok"));
    return 0;
}

//! enter scene 回调函数
int ffgate_t::enter_scene_callback(ffreq_t<session_enter_scene_t::out_t>& req_, const userid_t& session_id_)
{
    LOGTRACE((FFGATE, "ffgate_t::enter_scene_callback session_id[%ld]", session_id_));
    LOGTRACE((FFGATE, "ffgate_t::enter_scene_callback end ok"));
    return 0;
}

//! 逻辑处理,转发消息到logic service
int ffgate_t::route_logic_msg(const message_t& msg_, socket_ptr_t sock_)
{
    session_data_t* session_data = sock_->get_data<session_data_t>();
    LOGTRACE((FFGATE, "ffgate_t::route_logic_msg session_id[%ld]", session_data->id()));
    
    client_info_t& client_info   = m_client_set[session_data->id()];
    if (client_info.request_queue.size() == MAX_MSG_QUEUE_SIZE)
    {
        //!  消息队列超限，关闭sock
        sock_->close();
        return 0;
    }
    
    route_logic_msg_t::in_t msg;
    msg.session_id = session_data->id();
    msg.cmd        = msg_.get_cmd();
    msg.body       = msg_.get_body();
    if (client_info.request_queue.empty())
    {
        m_ffrpc->call(client_info.alloc_logic_service, msg,
                      ffrpc_ops_t::gen_callback(&ffgate_t::route_logic_msg_callback, this, session_data->id(), sock_));
    }
    else
    {
        client_info.request_queue.push(msg);
    }
    LOGTRACE((FFGATE, "ffgate_t::route_logic_msg end ok alloc_logic_service[%s]", client_info.alloc_logic_service));
    return 0;
}

//! 逻辑处理,转发消息到logic service
int ffgate_t::route_logic_msg_callback(ffreq_t<route_logic_msg_t::out_t>& req_, const userid_t& session_id_, socket_ptr_t sock_)
{
    LOGTRACE((FFGATE, "ffgate_t::route_logic_msg_callback session_id[%ld]", session_id_));
    map<userid_t/*sessionid*/, client_info_t>::iterator it = m_client_set.find(session_id_);
    if (it == m_client_set.end() || it->second.sock != sock_)
    {
        return 0;
    }
    client_info_t& client_info = it->second;
    if (client_info.request_queue.empty())
    {
        return 0;
    }
    
    m_ffrpc->call(client_info.alloc_logic_service, client_info.request_queue.front(),
                  ffrpc_ops_t::gen_callback(&ffgate_t::route_logic_msg_callback, this, session_id_, sock_));
    
    client_info.request_queue.pop();
    LOGTRACE((FFGATE, "ffgate_t::route_logic_msg_callback end ok queue_size[%d],alloc_logic_service[%s]",
                client_info.request_queue.size(), client_info.alloc_logic_service));
    return 0;
}

//! 改变处理client 逻辑的对应的节点
int ffgate_t::change_session_logic(ffreq_t<gate_change_logic_node_t::in_t, gate_change_logic_node_t::out_t>& req_)
{
    LOGTRACE((FFGATE, "ffgate_t::change_session_logic session_id[%ld]", req_.arg.session_id));
    map<userid_t/*sessionid*/, client_info_t>::iterator it = m_client_set.find(req_.arg.session_id);
    if (it == m_client_set.end())
    {
        return 0;
    }
    
    session_enter_scene_t::in_t enter_msg;
    enter_msg.from_scene = it->second.alloc_logic_service;
    
    it->second.alloc_logic_service = req_.arg.alloc_logic_service;
    gate_change_logic_node_t::out_t out;
    req_.response(out);
    
    enter_msg.session_id = req_.arg.session_id;
    enter_msg.from_gate = m_gate_name;
    
    enter_msg.to_scene = req_.arg.alloc_logic_service;
    enter_msg.extra_data = req_.arg.extra_data;
    m_ffrpc->call(req_.arg.alloc_logic_service, enter_msg, ffrpc_ops_t::gen_callback(&ffgate_t::enter_scene_callback, this, req_.arg.session_id));
    
    LOGTRACE((FFGATE, "ffgate_t::change_session_logic end ok"));
    return 0;
}

//! 关闭某个session socket
int ffgate_t::close_session(ffreq_t<gate_close_session_t::in_t, gate_close_session_t::out_t>& req_)
{
    LOGTRACE((FFGATE, "ffgate_t::close_session session_id[%ld]", req_.arg.session_id));
    
    map<userid_t/*sessionid*/, client_info_t>::iterator it = m_client_set.find(req_.arg.session_id);
    if (it == m_client_set.end())
    {
        return 0;
    }
    it->second.sock->close();
    gate_close_session_t::out_t out;
    req_.response(out);
    LOGTRACE((FFGATE, "ffgate_t::gate_close_session_t end ok"));
    return 0;
}

//! 转发消息给client
int ffgate_t::route_msg_to_session(ffreq_t<gate_route_msg_to_session_t::in_t, gate_route_msg_to_session_t::out_t>& req_)
{
    LOGTRACE((FFGATE, "ffgate_t::route_msg_to_session begin num[%d]", req_.arg.session_id.size()));
    
    for (size_t i = 0; i < req_.arg.session_id.size(); ++i)
    {
        userid_t& session_id = req_.arg.session_id[i];
        LOGTRACE((FFGATE, "ffgate_t::route_msg_to_session session_id[%ld]", session_id));

        map<userid_t/*sessionid*/, client_info_t>::iterator it = m_client_set.find(session_id);
        if (it == m_client_set.end())
        {
            continue;
        }

        msg_sender_t::send(it->second.sock, req_.arg.cmd, req_.arg.body);
    }
    gate_route_msg_to_session_t::out_t out;
    req_.response(out);
    LOGTRACE((FFGATE, "ffgate_t::route_msg_to_session end ok"));
    return 0;
}

//! 广播消息给所有的client
int ffgate_t::broadcast_msg_to_session(ffreq_t<gate_broadcast_msg_to_session_t::in_t, gate_broadcast_msg_to_session_t::out_t>& req_)
{
    LOGTRACE((FFGATE, "ffgate_t::broadcast_msg_to_session begin"));
    
    map<userid_t/*sessionid*/, client_info_t>::iterator it = m_client_set.begin();
    for (; it != m_client_set.end(); ++it)
    {
        msg_sender_t::send(it->second.sock, req_.arg.cmd, req_.arg.body);
    }
    
    gate_broadcast_msg_to_session_t::out_t out;
    req_.response(out);
    LOGTRACE((FFGATE, "ffgate_t::broadcast_msg_to_session end ok"));
    return 0;
}
