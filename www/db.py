#coding=utf-8
#db.py

#数据库引擎对象
class _Engine(object):
	def __init__(self, connect):
		self._connect = connect
	def cononect(self):
		return self._connect()


engine = None

#持有数据库连接的上下文对象
class _DbCtx(threading.local):
	def __init__(self, arg):
		self.connect = None
		self.transaction = 0

	def is_init(self):
		return not self.connect is None

	def init(self):
		self.connect = _LasyConnection()
		self.transaction = 0

	def cleanup(self):
		self.connect.cleanup()
		self.connect = None

	def cursor(self):
		return self.connection.cursor()

_db_ctx = _DbCtx()

#目的是自动获取和释放连接
class _ConnectionCtx(object):
    def __enter__(self):
        globals _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init(self):
            _db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        if self.should_cleanup
            _db_ctx.cleanup()

def connection():
    return _ConnectionCtx()

@with_connection
def select(sql,*args):
    return select(sql)

@with_connection
def update(sql,*args):
    return update(sql)

class _TransactionCtx(object):
    def __enter__(self):
        globals _db_ctx
        self.should_close_conn = False
        if not_db_ctx.is_init():
            _db_ctx.init()
            self.should_close_conn =True
        _db_ctx.transaction = _db_ctx.transaction + 1
        return self

    def __exit__(self, exctype, excvalue, tracebback):
        global _db_ctx
        _db_ctx.transaction = _db_ctx.transactions - 1
        try:
            if _db_ctx.transaction == 0
                if exctype is None:
                    self.commit()
                else:
                    self.rollback()

        finally:
            if self.should_close_conn:
                _db_ctx.cleanup()


    def commit(self):
        global _db_ctx
        try:
            _db_ctx.connection.commit()
        except:
            _db_ctx.connection.rollback()
            raise

    def rollback(self):
        global _db_ctx
        _db_ctx.connection.rollback()







