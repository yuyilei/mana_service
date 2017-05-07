# mana_service

> 华师匣子管理API

## 环境配置(container.env)

```
ADMIN=admin
ADMINPWD=adminpwd
```

## 部署

**单独部署**:

```shell
$ docker-compose stop && docker-compose build && dockder-compose up -d &&
docker-compose ps
```

## 测试

+ 配置```container.test.env```

```shell
$./start_test.sh && docker-compose -f docker-compose.test.yml logs --tail="100" mana_api_test
```
