# Handling requests with client certificate

This example shows how to use HTTP requests which need to pass client
certificate with the passphrase.

The included Robot Framework user library `ExtendedHTTPLibrary.py` provides
one extra keyword `Create Pkcs12 Session` which will create `RPA.HTTP` / `RequestsLibrary`
compatible session.

After this session has been created following keywords can be used to utilize created session:

    - GET On Session
    - PUT On Session
    - POST On Session
    - DELETE On Session
    - PATCH On Session
    - HEAD On Session
    - OPTIONS On Session

## Learning materials

- [All docs related to Robot Framework](https://robocorp.com/docs/languages-and-frameworks/robot-framework)
