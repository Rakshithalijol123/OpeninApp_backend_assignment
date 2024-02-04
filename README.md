# Used Backend Technology: FastAPI
**FastAPI** is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints.

# Why FastAPI?
 - **Pythonic Development:**  If your team is more familiar with Python or has experience with other Python frameworks, FastAPI provides a Pythonic development experience. It leverages Python's type hints and async/await syntax for clear and expressive code.
 - **Asynchronous Programming:** Built on top of Starlette, FastAPI supports asynchronous programming out of the box. This is advantageous for handling a large number of concurrent requests efficiently, making it suitable for real-time applications.
 - **Performance:** FastAPI is designed to be high-performance, and it benefits from Python's async capabilities. If your project involves heavy computation or IO-bound tasks, FastAPI's asynchronous features can be advantageous.
 - **Automatic API Documentation:** FastAPI automatically generates interactive API documentation using Swagger UI and ReDoc. This can be beneficial for both development and documentation purposes.
 - **Security Features:** FastAPI comes with built-in security features, including automatic validation of OAuth2, API key authentication, and support for JSON Web Tokens (JWT).

# Advantages of FastAPI over other Backend Technologies?

 - **Performance:** FastAPI, built on top of Starlette and Pydantic, is designed to be high-performance and asynchronous by default. It leverages Python's async and await syntax to handle a large number of concurrent requests efficiently. Node.js is also known for its non-blocking, event-driven architecture, providing good performance.

 - **Type Safety:** FastAPI utilizes Python type hints, allowing for better code readability and enabling tools like Pydantic to perform automatic data validation and serialization. This can result in fewer runtime errors and improved code maintainability.

 - **Automatic API Documentation:** FastAPI automatically generates interactive API documentation based on the OpenAPI standard. This makes it easier for developers to understand, test, and explore the API without the need for external documentation tools. Node.js requires additional tools or libraries for generating API documentation.

 - **Python Ecosystem:** If your team is already familiar with Python or your project relies on existing Python libraries, FastAPI provides a seamless integration with the Python ecosystem. You can leverage a wide range of existing Python modules and tools.

 - **Security Features:** FastAPI comes with built-in security features, including automatic validation of OAuth2, API key authentication, and support for JSON Web Tokens (JWT). It simplifies the implementation of secure authentication and authorization mechanisms.

 - **Compatibility with OpenAPI:** FastAPI is fully compatible with the OpenAPI standard, allowing for easy integration with other tools and services that follow the same standard. This promotes interoperability and collaboration within the broader API ecosystem.

 - **Rapid Development:** FastAPI is designed to minimize boilerplate code, making it easy to create APIs quickly. With automatic data validation and serialization, developers can focus on business logic rather than repetitive tasks.

 - **Active Development and Community:** FastAPI has an active and growing community of developers. The framework is actively maintained, and new features and improvements are regularly introduced. A strong community can provide support, share knowledge, and contribute to the ecosystem.


# Flow

- Create a virtual environment
- pip install -r requirement.txt

# To run the server

python run.py

# To open FastAPI Swagger UI

localhost/docs

# JWT auth credentials

 * USERNAME : "547353cb38f248482ee2d404ab38ad5a16bd073bd023efe0fcad693e6936eb4c"
 * PASSWORD : "d8ae0c4a2cac77d554136dae65a4e36cb63e990dbd5b9bfc22ca2b7d0dc50a7d"

# New Updates

- oAuth2 authentication is added
- Get required username and password from config file
- create app based endpoints then add them in main using
  from src.apps.credentials.views import router as credentials_router
  app.include_router(credentials_router, prefix="/credentials",
  dependencies=[Depends(validate_token)])`
