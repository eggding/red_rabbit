namespace cpp ff  
namespace as3 ff  
namespace py ff  
// ���ﶨ����һ���ṹ�壬û�ж��巽������Ӧ�����ɵĴ�����gen-cpp�е�shared_types.h�У�������һ��class��SharedStruct,  
// ��û�п�������������������read��write���������������������л�������л��ķ���.  
// ���ˣ����е�i32��Thrift IDL�ж���ı������ͣ���Ӧ��c++�����е�int32_t  
// thrift-0.9.0.exe -gen as3 -o as3
// thrift-0.9.0.exe -gen py -o py
struct chat_msg_t {      
  1: list<i32> key  
  2: string value  
}


