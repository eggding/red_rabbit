namespace cpp ff  
namespace as3 ff  
namespace py ff  
// 这里定义了一个结构体，没有定义方法，对应于生成的代码在gen-cpp中的shared_types.h中，其中有一个class叫SharedStruct,  
// 有没有看到其中有两个方法叫read和write，这就是用来对其进行序列化与把序列化的方法.  
// 对了，其中的i32是Thrift IDL中定义的变量类型，对应于c++语言中的int32_t  
// thrift-0.9.0.exe -gen as3 -o as3
// thrift-0.9.0.exe -gen py -o py
struct chat_msg_t {      
  1: list<i32> key  
  2: string value  
}


