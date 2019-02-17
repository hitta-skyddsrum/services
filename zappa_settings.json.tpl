{
    "_default": {
        "app_function": "run.app",
        "aws_region": "eu-west-1",
        "cors": true,
        "route53_enabled": true,
        "project_name": "hitta-skyddsrum-services",
        "lets_encrypt_key": "s3://hitta-skyddsrum-https-certificate/account.key",
        "runtime": "python3.6",
        "environment_variables": {
          "MYSQL_DATABASE_USER": "$MYSQL_DATABASE_USER",
          "MYSQL_DATABASE_PASSWORD": "$MYSQL_DATABASE_PASSWORD",
          "MYSQL_DATABASE_DB": "$MYSQL_DATABASE_DB",
          "MYSQL_DATABASE_HOST": "$MYSQL_DATABASE_HOST"
        },
        "s3_bucket": "hitta-skyddsrum-services-zappa",
        "tags": {
          "project": "hitta-skyddsrum",
          "stage": "$ZAPPA_STAGE"
        }
    },
    "$ZAPPA_STAGE": {
        "extends": "_default",
        "domain": "$ZAPPA_DOMAIN",
        "role_name": "$ZAPPA_ROLE_NAME"
    }
}
