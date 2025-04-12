# SDK LogSQL

## Overview
Este SDK agora fornece integração via WebSockets para interação com o serviço LogSQL.

## Módulo

- **SDK_WS**: Contém classes e handlers para comunicação WebSocket, incluindo gerenciamento de conexão e autenticação.

## Uso

### WebSocket
```python
from SDK.SDK_WS.main import LogSQLWSClient, LogSQLWSHandler, setup_ws_logger
logger = setup_ws_logger(
    name="your_logger",
    username="your_user",
    password="your_password",
    level=logging.DEBUG
)
```

## Final Considerations
Este SDK foi desenvolvido para facilitar a integração com o serviço LogSQL por meio de comunicação assíncrona usando WebSockets.

# LogSQL

## Description

This project provides a simple way to log and manage SQL queries. It ensures safer data handling and helps developers track query execution.

## Features

• Easy to integrate into existing projects  
• Real-time logging  
• Configurable output options  

## Installation

1. Clone the repository  
2. Run the setup script  
3. Configure the logging options  

## Usage

Call the logger function in your SQL-related scripts, passing your query string. The query is automatically recorded.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss future improvements.

## License

MIT
`