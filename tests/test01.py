import json
import unittest
from urllib.parse import *
from urllib.request import urlopen
from urllib.error import *

from config import API_ROOT
from utils import RestTestCase


class TestBaseUser(RestTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_creation(self):

        response = urlopen(API_ROOT+'/create/user_01')

        # 响应码应当为 200
        self.assertEqual(response.status, 200)

        headers = response.getheaders()
        content = response.read().decode()
        result = json.loads(content)

        # 1. 用户创建的结果
        # 1.1. 返回用户名称正确
        self.assertEqual(result['username'], 'user_01')
        # 1.2. 新建用户的状态应该为正常（1）
        self.assertEqual(result['status'], 1)
        # 1.3. 返回数据的字段包含如下
        self.assertSetEqual(
            set(result.keys()),
            {'username', 'password', 'status', 'remark'}
        )

    def test_02_duplicate_user_creation(self):

        # 2. 再次创建应该要卡住，因为用户名重复
        with self.assertRaises(HTTPError):
            response = urlopen(API_ROOT+'/create/user_01')


