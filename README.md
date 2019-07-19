# ConfigHelper

## 数据类型
* INT                       int32
* LONG                      int64
* FLOAT                     float，该类型支持不是很好，基本等于没有
* BOOL                      bool
* STR                       string
* ARRAY[:Type]              repeated, 数组类型；子类型若不填写则会自动推导，建议写上
* MAP[:KeyType, ValueType]  map<Type1, Type>，字典类型，子类型若不填写则会自动推导，但建议写上
* JSON:Type                 自定义结构类型，需要提供该Json的描述文件

## 配置文件
* Config.json
    * JSON_PATH: json文件所有的路径，在该路径下的文件分为两类：
        1. JsonDesc.json 该文件为json类型的自定义结构类型的描述文件，明声了该结构的成员
        2. JsonType_JsonFileName.json JsonType为在描述文件中声明过的结构，JsonFileName则是该结构的实例名称
    * EXCEL_PATH: Excel文件的读取路径
    * OUT_PATH: 最后输出的proto文件的路径
    * PROTO_SAVE_PATH: 根据excel/json生成的proto文件的存放路径，该proto文件是用来确定根据json及excel字段生成的
    * BINARY_SAVE_PATH: 二进制文件生成路径
    * LOG_PATH： 无用
    * PYTHON_PROTO_MODULE_PATH: 生成的python的proto文件的所在位置；这里面会利用python的反射将数据写进二进制文件中，因此需要标名该文件的位置
    * SPAWN_CSHARP_COMMAND: 该指令用来生成C# 的proto文件
    * SPAWN_PYTHON_COMMAND: 该指令用来生成python的proto文件
    * OTHER_OUT_PATH: 暂时无用
    
## 其它
* ExtendTools是工作中为了解决一些特殊文件而存在的
