import vierror as vie
import viconfig as vic
import vidbcontrol as vidbc
from fastapi import Query, Path, Body, Form

class Field:
    def __init__(self, name=None, title=None, description=None, type=None, tag=None, verify=None):
        self.name = name
        self.title = title
        self.description = description
        self.type = type
        self.tag = tag
        self.verify = verify if verify is not None else []

    def v_value(self, value):
        new_value = value
        for v in self.verify:
            new_value = v(new_value, self.name)
        return new_value

    def options(self):
        opts = {}
        if self.name:
            opts["name"] = self.name
        if self.title:
            opts["title"] = self.title
        if self.description:
            opts["description"] = self.description
        if self.type:
            vie.MError("Field.Options.Type", "Type 不能为空")
            opts["type"] = self.type
        if self.tag:
            opts["tag"] = self.tag
        return opts
    
    def __call__(self, *args, **kwds):
        options = self.options().update({
            "default": None
        })
        del options["type"]
        del options["name"]
        if self.type == "query":
            return Query(**options)
        elif self.type == "path":
            return Path(**options)
        elif self.type == "body":
            return Body(**options)
        elif self.type == "form":
            return Form(**options)
        elif self.type is None:
            return None
        else:
            raise vie.MError("Field.Type", "Type 必须为 query, path, body, form")
        

class DBOrm:
    def __init__(self, table: str, schema: str, config: vic.Config):
        self.table = table
        self.schema = schema
        self.config = config
        self.conn = self.connect(config)

    def connect(self, config: vic.Config):
        """
        连接数据库
        """
        return vidbc.PDBConn(**{
            "user": config.get("database", "user"),
            "password": config.get("database", "password"),
            "host": config.get("database", "host"),
            "port": config.get("database", "port"),
            "database": config.get("database", "name"),
        })
    
    def create_table(self, sql: str):
        """
        创建表
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        cur.close()
    
    def c_sql(self, type: str, sql_dict: dict):
        """
        生成 SQL 语句和参数
        """
        if type == "select":
            sql, params = vidbc.Query(self.table, self.schema).select(**sql_dict)
        elif type == "insert":
            sql, params = vidbc.Query(self.table, self.schema).insert(**sql_dict)
        elif type == "update":
            sql, params = vidbc.Query(self.table, self.schema).update(**sql_dict)
        elif type == "delete":
            sql, params = vidbc.Query(self.table, self.schema).delete(**sql_dict)
        elif type == "insert_mul":
            sql, params = vidbc.Query(self.table, self.schema).insert_mul(**sql_dict)
        else:
            raise vie.MError("DBOrm.CSQL", "Type 必须为 select, insert, update, delete, insert_mul")
        return sql, params
    
    def query_res(self, sql_dict: dict, to_json=False):
        sql, params = self.c_sql(sql_dict)
        cur = self.conn.cursor()
        cur.execute(sql, params)
        res = cur.fetchall()
        if to_json:
            res = [dict(zip([column[0] for column in cur.description], row)) for row in res]
        cur.close()
        return res
    
    def query_com(self, sql_dict: dict):
        sql, params = self.c_sql(sql_dict)
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        cur.close()

    def callback(self, func: str, params: dict):
        raise vie.MError("DBOrm.Callback", "暂不支持此功能")

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()




class BaseRouter:
    def __init__(self, path=None, method=None, title=None, description=None, tags=None, fields=None):
        """
        Root 根节点（/）
        """
        self.path = path
        self.method = method
        self.title = title
        self.description = description
        self.tags = tags
        self.fields: dict[Field] = fields if fields is not None else {}

    def options(self):
        """
        获取路由选项
        returns: dict
            {
                "path": self.path, # 路径
                "method": self.method, # 方法
                "title": self.title, # 标题
                "description": self.description, # 描述
                "tags": self.tags, # 标签
                "router": self.router() # 路由函数
            }
        """
        opts = {}
        if self.path:
            raise vie.MError("RouterClass.Options.Path", "Path 不能为空")
        if self.method:
            raise vie.MError("RouterClass.Options.Method", "Method 不能为空")
        if self.title:
            opts["title"] = self.title
        if self.description:
            opts["description"] = self.description
        if self.tags:
            opts["tags"] = self.tags
        router_func = self.router()
        if callable(router_func):
            opts["router"] = router_func
        else:
            raise vie.MError("RouterClass.Options.Router", "Router 必须为可调用的函数")
        return opts
    
    def router(self):
        """
        路由函数(此函数必须在集成类中实现)
        returns: function
            路由函数
        """
        raise vie.MError("RouterClass.Router", "Router 必须在集成类中实现")
        def router_func():
            pass
        return router_func
    
    def add_fields(self, fields: list[Field]):
        """
        添加字段
        """
        for field in fields:
            if field.name in self.fields:
                raise vie.MError("RouterClass.AddFields", "字段 %s 已经存在" % field.name)
            self.fields[field.name] = field
    
    def get_field(self, name: str):
        """
        获取字段
        """
        if name not in self.fields:
            raise vie.MError("RouterClass.GetField", "字段 %s 不存在" % name)
        return self.fields[name]

    def model_verify(self, info: dict):
        """
        数据验证
        """
        for key in self.fields:
            info[key] = self.get_field(key).v_value(info[key])
        return info
    
    def c_table(self):
        raise vie.MError("BaseRouter.c_table", "c_table 必须在集成类中实现, 并返回创建表的sql语句")
        sql = ""
        return sql

    
    def db_model(self, config: vic.Config):
        """
        数据库模型
        """
        return DBOrm("user", "public", config)
