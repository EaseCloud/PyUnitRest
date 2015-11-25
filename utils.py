import os
import unittest
import config


class RestTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        print('正在备份数据库...')

        # 先 touch 锁定文件
        assert not os.path.exists('.lock'), '测试未完成，数据库已被锁定，如有错误，请手动删除 .lock 文件'
        open('.lock', 'w').close()

        os.system(
            'mysqldump %s -u%s -p%s --add-drop-database --add-drop-table >tmp/_db_production.sql 2>>tmp/.error'
            % (config.DB_NAME, config.DB_USER, config.DB_PASS)
        )
        os.system(
            'mysqldump %s -u%s -p%s -d --add-drop-database --add-drop-table >tmp/_db_init.sql 2>>tmp/.error'
            % (config.DB_NAME, config.DB_USER, config.DB_PASS)
        )

        print('正在创建测试数据库...')

        os.system(
            'mysql -u%s -p%s -D%s <tmp/_db_init.sql 2>>tmp/.error'
            % (config.DB_NAME, config.DB_USER, config.DB_PASS)
        )

    @classmethod
    def tearDownClass(cls):

        print('\n正在还原数据库...')

        os.system(
            'mysql -u%s -p%s -D%s <tmp/_db_production.sql 2>>tmp/.error'
            % (config.DB_NAME, config.DB_USER, config.DB_PASS)
        )
        os.remove('.lock')

