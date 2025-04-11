import logging
from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import scoped_session, sessionmaker

# 类型变量定义
T = TypeVar("T", bound="Base")  # type: ignore

# 初始化基类
Base = declarative_base()


# 数据库配置
class DatabaseConfig:
    def __init__(
        self,
        dialect: str = "mysql",
        driver: str = "pymysql",
        username: str = "root",
        password: str = "password",
        host: str = "localhost",
        port: int = 3306,
        database: str = "my_database",
        pool_size: int = 5,
        pool_recycle: int = 3600,
    ):
        self.dialect = dialect
        self.driver = driver
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.pool_size = pool_size  # 最大空闲连接数
        self.pool_recycle = pool_recycle  # 连接的最大存活时间


# 数据库操作
class Database:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine = None
        self.session_factory = None
        self.current_session = None  # 用于事务管理

        # 配置日志信息
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def connect(self) -> None:
        """创建数据库连接"""
        try:
            connection_url = (
                f"{self.config.dialect}+{self.config.driver}://"
                f"{self.config.username}:{self.config.password}@"
                f"{self.config.host}:{self.config.port}/"
                f"{self.config.database}"
            )

            self.engine = create_engine(
                url=connection_url,
                pool_size=self.config.pool_size,
                pool_recycle=self.config.pool_recycle,
                echo=False,  # 在生产环境中设置为False
            )

            self.session_factory = scoped_session(
                sessionmaker(
                    bind=self.engine,
                    autocommit=False,
                    autoflush=False
                )
            )
            self.logger.info("Database connection established successfully!")
        except Exception as e:
            self.logger.error(f"Database connection failed: {str(e)}.")
            raise

    def register_models(self) -> None:
        """注册所有新模型"""
        try:
            Base.metadata.create_all(self.engine)
            self.logger.info("Models registered successfully!")
        except Exception as e:
            self.logger.error(f"Models resigtration failed: {str(e)}.")
            raise

    def get_session(self) -> Session:
        """获取新的数据库会话"""
        if not self.session_factory:
            raise RuntimeError("Database not connected.")
        return self.session_factory()

    # -------------------- 基本CRUD操作 --------------------
    def create(self, obj: T) -> T:
        """创建新记录"""
        session = self.get_session()
        try:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            self.logger.debug(f"Created new record: {obj}!")
            return obj
        except Exception as e:
            session.rollback()
            self.logger.error(f"Create operation failed: {str(e)}.")
            raise
        finally:
            session.close()

    def get_by_id(self, model: Type[T], obj_id: int) -> Optional[T]:
        """通过id获取单个记录"""
        session = self.get_session()
        try:
            result = session.query(model).get(obj_id)
            self.logger.debug(f"Retrieved record by ID {obj_id}: {result}!")
            return result
        except Exception as e:
            self.logger.error(f"Get by ID failed: {str(e)}.")
            raise
        finally:
            session.close()

    def get_all(self, model: Type[T]) -> List[T]:
        """获取所有记录"""
        session = self.get_session()
        try:
            results = session.query(model).all
            self.logger.debug(f"Retrieved all records: {len(results)} found!")
            return results
        except Exception as e:
            self.logger.error(f"Get all failed: {str(e)}.")
        finally:
            session.close()

    def update(self, obj: T) -> T:
        """更新现有记录"""
        session = self.get_session()
        try:
            session.merge(obj)
            session.commit()
            session.refresh(obj)
            self.logger.debug(f"Update record: {obj}!")
            return obj
        except Exception as e:
            session.rollback()
            self.logger.error(f"Update failed: {str(e)}.")
            raise
        finally:
            session.close()

    def delete(self, obj: T) -> None:
        """删除记录"""
        session = self.get_session()
        try:
            session.delete(obj)
            session.commit()
            self.logger.debug(f"Delete record: {obj}!")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Delete failed: {str(e)}")
            raise
        finally:
            session.close()

    # -------------------- 高级操作 --------------------
    def filter_by(self, model: Type[T], **filters: Any) -> List[T]:
        """条件查询"""
        session = self.get_session()
        try:
            results = session.query(model).filter_by(**filters).all()
            self.logger.debug(f"Filtered query found {len(results)} records!")
            return results
        except Exception as e:
            self.logger.error(f"Filtered query failed: {str(e)}.")
            raise
        finally:
            session.close()

    def paginate(
        self, model: Type[T], page: int = 1, per_page: int = 10, **filters: Any
    ) -> Dict[str, Any]:
        """分页查询"""
        session = self.get_session()
        try:
            query = session.query(model)
            if filters:
                query = query.filter_by(**filters)

            total = query.count()
            results = query.offset((page - 1) * per_page).limit(per_page).all()

            self.logger.debug(f"Paginated query: page {page}, results {len(results)}!")

            return {"total": total, "page": page, "per_page": per_page, "data": results}
        except Exception as e:
            self.logger.error(f"Paginated failed: {str(e)}.")
        finally:
            session.close()

    # -------------------- 事务管理 --------------------
    def begin_transaction(self) -> None:
        """开启事务"""
        if self.current_session is None:
            self.current_session = self.get_session()
            self.logger.debug("Transaction started!")

    def commit_transaction(self) -> None:
        """提交事务"""
        if self.current_session:
            try:
                self.current_session.commit()
                self.logger.debug("Transaction committed!")
            except Exception as e:
                self.current_session.rollback()
                self.logger.error(f"Transaction commit failed: {str(e)}.")
                raise
            finally:
                self.current_session.close()
                self.current_session = None

    def rollback_transaction(self) -> None:
        """回滚事务"""
        if self.current_session:
            self.current_session.rollback()
            self.current_session.close()
            self.current_session = None
            self.logger.debug("Transaction rolled back.")

    def __enter__(self):
        """支持上下文管理"""
        self.begin_transaction()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理退出处理"""
        if exc_type:
            self.rollback_transaction()
        else:
            self.commit_transaction()

    def close(self) -> None:
        """关闭数据库连接"""
        if self.engine:
            self.engine.dispose()
            self.logger.info("Database connetion closed!")
