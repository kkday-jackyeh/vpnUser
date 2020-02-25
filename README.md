# Auto generate VPN user

---

## Prerequisites

1. Python 3

---

## Getting Started

1. Modify .env

```shell
    $ cp env.template .env
```

2. fill in .env

3. create user.txt

```shell
$ vim user.txt
# username1
# username2
# username3
# username4
```

4. Run program to create user

```shell
    $ python3 index.py
```

5. Get user info in result.txt

```shell
    $ more result.txt
```
