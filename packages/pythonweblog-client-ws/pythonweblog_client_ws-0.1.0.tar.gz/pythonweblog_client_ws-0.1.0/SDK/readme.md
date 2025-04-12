# SDK LogSQL

## Visão Geral

Este SDK fornece implementações para interagir com o serviço LogSQL utilizando tanto requisições REST quanto comunicação via WebSocket.

## Módulos

- **SDK_REST**: Contém métodos e classes para integração via HTTP.
- **SDK_WS**: Contém classes e handlers para comunicação via WebSocket, incluindo gestão e autenticação de conexões.

## Utilização

### REST
Importe os componentes do módulo REST:
```python
from SDK.SDK_REST.main import LogSQLClient, LogSQLHandler, LogType, setup_rest_logger
```

### WebSocket
Importe os componentes do módulo WebSocket:
```python
from SDK.SDK_WS.main import LogSQLWSClient, LogSQLWSHandler, setup_ws_logger
```

Configure o logger ou o cliente conforme a necessidade:
```python
# Exemplo para WebSocket:
logger = setup_ws_logger(
    name="seu_logger",
    server_url="http://localhost:1234",
    username="seu_usuario",
    password="sua_senha",
    level=logging.DEBUG
)
```

## Considerações Finais

O SDK foi desenvolvido para facilitar a integração com o serviço LogSQL, permitindo tanto operações síncronas quanto assíncronas.
