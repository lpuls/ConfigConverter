# ConfigHelper

## 数据类型
* INT                       int32
* LONG                      int64
* FLOAT                     float，该类型支持不是很好，基本等于没有
* BOOL                      bool
* STR                       string
* ARRAY[:Type]              repeated, 数组类型
* MAP[:KeyType, ValueType]  map<Type1, Type>，字典类型
* Type                      自定义结构类型，需要提供该Json的描述文件或着是Excel中定义的枚举

## 配置文件
* Config.json
    * package_name      包名，放在CS文件中就表示命名空间
    * excel_path        要读取的Excel文件的地址（有读取Excel文件为数据源时才有效）
    * json_path         要读取的Json文件包在的地址（有读取Json文件为数据源时才有效）
    * json_desc_path    在Json中定义的描述文件，用于声明一个结构（有读取Json文件为数据源时才有效）
    * binary_path       保存二进制文件的地址（使用写二进制文件功能才有效）
    * cs_path           保存CS文件的地址（使用写二进制文件功能才有效）
    * py_path           保存python文件的地址（使用写二进制文件功能才有效）
    * python_name       写成二进制文件时，要通过返射获取实例的python文件名（使用写二进制文件功能才有效）
    * proto_path        保存生成的proto文件的地址（使用写二进制文件功能才有效）
    * csv_path          保存生成的csv文件的地址（使用写csv文件功能才有效）
    
## 其它
* ExtendTools是工作中为了解决一些特殊文件而存在的

## 使用
* Excel
    * 数据：前三行分别为：类型，描述，字段名称
    * 枚举：前三行如数据；第一列为枚举名称，第二列为枚举值，第三列为枚潜描述

* Json
    * 需要在Config.json_desc_path列表中添加描述文件的地址
    * 按照描述文件定义的格式往里面写入数据，就如同普通的Json文件一样
