# Brief Box Backend Serverless Services

## Authentication

- Token Type: [JSON Web Token](https://jwt.io)
- Token Expiration: 1 hour or 1 year (if remember flag)
- Code Format: 999999

Authentication Sequence Diagram:

```mermaid
sequenceDiagram
    participant A as Web/Mobile App
    participant B1 as Code endpoint
    participant B2 as Token endpoint
    participant C as Server database
    actor D as Contact (SMS/e-mail)
    participant E as Local cache
    autonumber
    A->>+B1: Generate Code with Contact
    B1-)C: Put Code, Contact and TTL
    activate C
    B1-)-D: Send Code
    activate D
    A-->D: Check Code
    deactivate D
    A->>+B2: Request Token with Contact and Code
    B2->C: Delete Contact and Code
    deactivate C
    B2--)-A: Return Token
    A-)E: Put Token
    activate E
    deactivate E
```

Backend Service Sequence Diagram:

```mermaid
sequenceDiagram
    participant A as Web/Mobile App
    participant E as Local cache
    participant F as Backend services
    activate E
    A->E: Get Token
    A->>F: Call Service with Token
    activate F
    alt Valid Token
        F-)A: 200 {Service Response Boby)
    else Invalid Token
        F-)A: 401 {Error Unauthorized}
    end
    deactivate F
    deactivate E
```


## Development

To install CDK:

```
$ nvm use 18.12.1
$ npm install -g aws-cdk@2.63.0
```

To create Python Virtual Environment:

```
$ pyenv install 3.10.3
$ pyenv exec python -m venv .venv
$ .venv/bin/pip install -r requirements.txt
```

Useful commands:

 * `cdk diff`         compare deployed stack with current state
 * `cdk deploy`       deploy this stack to your default AWS account/region
 * `.venv/bin/pytest` run python local tests
 * `.venv/bin/behave` run behaviour feature tests
 * `.venv/bin/behave --no-capture --no-capture-stderr` run behaviour feature tests with logs
