Zodiac Sign Based Authentication Middleware for Swift (OpenStack) based on 
Swauth (https://github.com/gholt/swauth).


## Installation
Zodiacauth requires Swauth so begin by installing Swauth.

Install zodiacauth by downloading the source or using a package manager such as 
pip.

`pip install -e https://leetrout@github.com/leetrout/swift-zodiacauth.git#egg=zodiacauth`


## Configuration
Add `zodiacauth` to your proxy-server.conf (/etc/swift/proxy-server.conf) 
pipeline and provide a filter configuration.

Zodiacauth is based on Swauth so you need to provide the `super_admin_key` in 
your zodiacauth filter.

Zodiacauth requires an access control list (ACL) in JSON format and you must 
provide a path to that file as well.

    [filter:zodiacauth]
    use = egg:zodiacauth#zodiacauth
    zodiac_acl_path = /tmp/acl.json
    super_admin_key = zodiacauthkey

Once you have configured zodiacauth you can easily add users using the Swauth
tools:

    swift-init proxy reload

    swauth-prep -K swauthkey

    swauth-add-user -A http://127.0.0.1:8080/auth/ -K swauthkey -a test tester testing

    swift -A http://127.0.0.1:8080/auth/v1.0 -U test:tester -K testing stat -v

## Access Control List
The ACL is an external file in JSON format that specifies a combination if 
zodiac signs of the containers and objects when they were created and a zodiac 
sign of the access date along with a list of remote addresses.

    [
        [
            "sign of container/object creation date", 
            "sign of current date when access request is made",
            ["0.0.0.0", "1.1.1.1"]
        ]
    ]

For example, to allow access to objects and containers created on Friday, 
November 25th and accessed on Friday, November 25th from 127.0.0.1:

    [
        ["sagittarius", "sagittarius", ["127.0.0.1"]]
    ]

