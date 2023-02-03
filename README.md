# Brief Box Back-end Serverless Services


## Authentication

- Token Type: [JSON Web Token](https://jwt.io)
- Token Expiration: 24 hours
- Code Format: 999 999 (space insensitive)

**Authentication Sequence Diagram**

```mermaid
sequenceDiagram
    participant A as Web/Mobile App
    participant B1 as Code endpoint
    participant B2 as Challenge endpoint
    participant B3 as Token endpoint
    participant C as Server database
    actor D as Contact (SMS/e-mail)
    participant E as Local cache
    autonumber
    A->>+B1: Generate Code with Contact and UUID
    B1-)C: Put Code, Contact, UUID and TTL
    activate C
    B1-)-D: Send Code
    activate D
    A-->D: Check Code
    deactivate D
    A->>+B2: Validade Code with Contact and UUID
    B2->C: Get Code with Contact and UUID
    B2-)C: Put Challenge with Contact, UUID and Code
    B2--)-A: Return Challenge
    A->>+B3: Request Token with Contact, UUID, Code and Challenge
    B3->C: Get Challenge with Contact, UUID and Code
    B3->C: Delete Contact, UUID, Code and Challenge
    deactivate C
    B3--)-A: Return Token
    A-)E: Put Token
    activate E
    deactivate E
```

**Backend Service Sequence Diagram**

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

To create a virtualenv:

```
$ python3 -m venv .venv
$ .venv/bin/pip install -r requirements.txt
```

Useful commands:

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
