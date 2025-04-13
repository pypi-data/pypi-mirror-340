# Fr1997 python私有包

## 介绍
    私人包，所有方法需要配置参数，没有配置参数无法使用

### 项目代码打包成一个可执行文件

```sh
python setup.py build
```

### 将源文件进行打包操作

```sh
python setup.py sdist
```

### （本地）安装包

```sh
pip install dist/Fr1997v011-4.0.1.tar.gz
```

### 下载包

```sh
pip install Fr1997v011
```

### 清空pip缓存

```sh
pip cache purge
```

### 升级包

```sh
pip install --upgrade Fr1997v011
```

### 上传pypi  (pip install twine)
 
```sh
twine upload dist/*      
```
      

### 卸载包

```sh
pip uninstall Fr1997v011
```

pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple Fr1997v011==1.1.2


####
`
    配置文件
        所有配置在这个地方读取 
        使用内存缓存机制 memcache
        没有读取到内存中的配置，这个包相当于不能用
    pip3 cache purge
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple Fr1997v011==3.2.6

    pip3 install --upgrade Fr1997v011
    pip3 install redis
    pip3 install pymysql
    pip3 install elasticsearch
    pip3 install python-memcached
    pip3 install PyExecJS
    pip3 install -U cos-python-sdk-v5
    pip3 install pypinyin
    pip3 install django
    pip3 install lxml
    
    pip38 install --upgrade Fr1997v011
    pip38 install redis
    pip38 install pymysql
    pip38 install elasticsearch
    pip38 install python-memcached
    pip38 install PyExecJS
    pip38 install -U cos-python-sdk-v5
    pip38 install pypinyin
    pip38 install django
    pip38 install lxml
`


