PyUnitRest
==========

Python unit test framework for general RESTful api

缘起：[使用 Python 的 unittest 类库进行 RESTful 单元测试](https://www.huangwenchao.com.cn/2015/03/python-unittest.html)

## 题记

现在要做一个 RESTful 的系统，然后定义了一套 RESTful 的 HTTP 接口。这个时候需要引入一个有效的机制来进行逻辑的设计。

为什么要做单元测试？

1. 对于一些给定的业务逻辑，以及边界条件，都需要进行反复的测试，以确保逻辑无误；
2. 这些测试用例仅仅通过逻辑计划，在编码之前就可以确定，可以提前进行，而且是稳定的；
3. 测试用例一旦完成，只需要设定好能够充分验证业务逻辑以及各类边界条件的测试用例，就可以一直（主要在开发环节，运维时候少一点）反复地跑，这样能够以最小的人工努力实现代码实现逻辑的稳定。

多了不说了，反正单元测试是利国利民的好事，也是业务解耦的好办法，要养成这个习惯！

## 单元测试的基本步骤

1. 初始化环境
  + 这一步主要是确立一个基本稳定的环境
  + 例如把数据库的内容清空，或者向其写入一些固定的基础数据
2. 执行测试用例
  + 每个测试用例可以看成是一个函数，然后在这个函数中执行一系列的操作
  + 在尽量多可能的地方设置断言，断言正确的逻辑结果
  + 于是如果有一个断言失败，测试用例就会失败
3. 清理工作
  + 完成一系列的测试用例之后可以执行一个固定的清理工作，以恢复环境

## 方案

由于这次是 RESTful 开发，业务之间的解耦规划比较理想，因此单元测试只针对在 HTTP 层面进行测试，那么理论上可以选择任何语言进行测试，那么选取什么方案呢？

最终还是选择了 Python 下面的 unittest 类库进行测试：

[https://docs.python.org/3/library/unittest.html](https://docs.python.org/3/library/unittest.html)

unittest 是 python 核心的类库，这样可以充分利用到 python 语言的便捷性。要知道，在 python 里面用 urllib 的借口收发 HTTP 请求简直就是小菜一碟！

## Python - UnitTest 介绍

### 快速例子

先援引一下官方文档的一个测试例子，不需要任何额外的安装：

```python
import random
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = list(range(10))

    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, list(range(10)))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

if __name__ == '__main__':
    unittest.main()
```

直接拿这个代码一跑，一切就搞定了！

### 基本概念

那么我们叙述一下基本的概念，着重阅读 [26.3.4. Organizing test code](https://docs.python.org/3/library/unittest.html#organizing-test-code) 这个小节。

#### 1. TestCase 类

从 `unittest.TestCase` 派生出若干个类，用于承载测试用例；

```python
class TestCase01(unittest.TestCase):

    # 测试方法放在这里面
    def test_01(self):
        # 这个用例的测试代码
        pass

    # 可以定义多个
    def test_02(self):
        pass
```

##### 1.1. test*(self) 测试方法

在这个类里面任何以 test 开头的方法都会被测试运行。

*！！！注意，测试方法的执行顺序是按照测试方法名的字典序执行的*

如果在一个测试方法里面出现了“断言错误”，那么这个测试点就被报告为“失败（Failure）”，如果抛出了其他错误，则会被报告为“错误(Error)”。

注意，断言错误的产生通过 unittest 模块的 `assert???()` 系列方法，或者通过 assert 语句产生，这些一般是主动的业务逻辑校验。

那么“错误”的情况就在于非业务逻辑的问题，这些都应当被分别正确地报告。

##### 1.2. setUp(self) 方法

测试类可以实现 `setUp` 方法，如果 `setUp()` 方法里面抛出了异常，那么那么框架会认为测试出了问题，这个类里面的用例就不会执行。

##### 1.3. tearDown(self) 方法

如果 `setUp()` 跑成功了，`tearDown` 就会在全部测试方法跑完的时候运行，不管中间有没有错误或者失败。

> 注意，每个 test 方法执行前后会执行一套 setUp - tearDown 方法，如果希望是对整个测试类进行初始化和清理，那么应当实现对应的 setUpClass 和 tearDownClass 方法（这两个方法需要 @classmethod）。

#### 测试固件 *Test Fixture* 与测试套件 *Test Suite*

上述的一个测试环境（测试类）就叫做一个 *Fixture*，这里窃译之为“测试固件”。

那么最后，当 `unittest.main()` 执行的时候，框架会自动收集所有实现的测试用例并执行之。

然后还有一个“测试套件”类 `TestSuite`，大致的使用方法如下：

```python
def suite():
    suite = unittest.TestSuite()
    suite.addTest(WidgetTestCase('test_default_size'))
    suite.addTest(WidgetTestCase('test_resize'))
    return suite
```

文档建议把测试用例分组放在不同的模块里面 *感觉他可能针对那些直接把测试跟逻辑实现放在一起的做法*：

例如 `test_widget_01.py` 这个样子，有如下几点好处：

1. 可以从命令行单独测试一个模块
2. 便于使测试代码与发布代码分离
3. 这样可以把测试代码固定起来，修改功能实现的时候一般而言都不应该改测试代码（大多是情况下是实现出了问题，不是测试出了问题）
4. 更便于重构测试代码
5. 反正如果有 C 实现的内容都要抽出来，这种情况下你想不想都要这么搞
6. 如果测试策略改变，无需修改实现

简而言之，测试代码跟实现代码分开放，这是很容易做到也是收益很高的解耦。

## 实务

后面的话我们就直接用 unittest 模块写测试了，不过后面有几点树需要注意的：

1. 在一个测试类跑测试之前，应当在 `setUpClass()` 方法重置数据库，以获得一个统一的初始环境；
2. 在一个测试类跑完测试后，应当在 `setUpClass()` 方法将数据库恢复原状；

于是我们通过 `os.system()` 方法直接调用命令行，对数据库进行备份、恢复的方法来实现这些功能即可。

然后，下面把我做的一个样例附上，具体的写法，大致如此：

```python
## settings.py

TEST_DOMAIN = 'localhost'
PATH_MYSQL = 'D:\\upupw\\MySQL\\bin'

DB_USER = 'root'
DB_PASSWORD = 'root'
DB_DATABASE = 'test'
```

```python
## test.py
import json
import os
import unittest
from urllib.parse import *
from urllib.request import urlopen
from urllib.error import *

from settings import *


def db_dump():
    #print('正在备份数据库...')
    assert not os.path.exists('.lock'), '测试未完成，数据库已被锁定，如有错误，请手动删除 .lock 文件'
    open('.lock', 'w').close()
    os.system(
        '%s\\mysqldump %s -u%s -p%s --add-drop-database --add-drop-table >_db_production.sql 2>null'
        % (PATH_MYSQL, DB_DATABASE, DB_USER, DB_PASSWORD)
    )
    os.system(
        '%s\\mysqldump %s -u%s -p%s -d --add-drop-database --add-drop-table >_db_init.sql 2>null'
        % (PATH_MYSQL, DB_DATABASE, DB_USER, DB_PASSWORD)
    )

def db_init():
    #print('正在创建测试数据库...')
    os.system(
        '%s\\mysql -u%s -p%s -D%s <_db_init.sql 2>null'
        % (PATH_MYSQL, DB_USER, DB_PASSWORD, DB_DATABASE)
    )


def db_recover():
    #print('正在还原数据库')
    os.system(
        '%s\\mysql -u%s -p%s -D%s <_db_production.sql 2>null'
        % (PATH_MYSQL, DB_USER, DB_PASSWORD, DB_DATABASE)
    )
    os.remove('.lock')


class TestBaseUser(unittest.TestCase):
    
    def setUp(self):
        #print('  * 初始化')
        pass
        
    def tearDown(self):
        #print('  * 清理')
        pass

    def test_01_creation(self):
        # print('http://%s/create/user01' % TEST_DOMAIN)

        response = urlopen('http://%s/create/user_01' % TEST_DOMAIN)

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
            response = urlopen('http://%s/create/user_01' % TEST_DOMAIN)
        

    @classmethod
    def setUpClass(cls):
        db_dump()
        db_init()

    @classmethod
    def tearDownClass(cls):
        db_recover()


if __name__ == '__main__':
    unittest.main()

```