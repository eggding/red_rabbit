
#ifndef _FF_BROKER_BRIDGE_H_
#define _FF_BROKER_BRIDGE_H_



namespace ff
{
class ffbroker_t;
class ffbroker_bridge_t
{
public:
    ffbroker_bridge_t();
    ~ffbroker_bridge_t();
    ffbroker_t& get_ffbroker()              { return *m_ffbroker; }
    void        set_ffbroker(ffbroker_t* p) { m_ffbroker = p; }
    
    //! 处理broker bridge 转发给broker master的消息
    int handle_bridge_to_broker_route_msg(bridge_route_to_broker_t::in_t& msg_, socket_ptr_t sock_);
    
    //! 处理broker master 注册到broker bridge
    int handle_broker_register_bridge(register_bridge_broker_t::in_t& msg_, socket_ptr_t sock_);
    
    //! [3] bridge的处理函数，从broker master转发到另外的broker master
    int bridge_handle_broker_to_broker_msg(bridge_route_to_broker_t::in_t& msg_, socket_ptr_t sock_);
    
    //! 处理bridge 同步消息
    int handle_bridge_sync_data(register_bridge_broker_t::out_t& msg_, socket_ptr_t sock_);
private:
    ffbroker_t*     m_ffbroker;
};

};

#endif

