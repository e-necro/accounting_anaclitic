откуда начало идей спизжено: https://testdriven.io/blog/developing-a-single-page-app-with-fastapi-and-vuejs/

### npm run serve (см решение ниже)
с чего-то переводит на http://localhost:8082/#/, который не работает, поскольку у меня привязка 
к http://localhost:8080/#/
С какого???

### итог
накасипорил, потому и порт не тот был.
У меня уже в Dockerfile фронта запущен `npm run serve` и нехер его у себя снова запускать! Это первая ошибка.
Ошибка два: в docker-compose.yml не надо прицеплять `node_modules` если он уже прикручен в Dockerfile. Все собирается, все запущено!

# TODO: выяснить как работает этот image. В смысле он висит в оперативке или все же жрет мой диск этим node.js


<!--  -->


# frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Run your unit tests
```
npm run test:unit
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
