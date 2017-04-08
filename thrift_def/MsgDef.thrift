namespace cpp ff  
namespace as3 ff  
namespace py  msg_def
// thrift-0.9.0.exe -gen as3 -o as3
// thrift-0.9.0.exe -gen py -o py

struct chat_msg_t {      
  1: list<i32> key  
  2: string value  
}

struct account_t {      
  1: string nick_name = ""   
  2: string password = ""
  3: bool  register_flag = false //! ¿¿¿¿¿  
  4: string email = ""
}

