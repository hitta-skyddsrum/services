{
    "staging": {
        "app_function": "run.app",
        "aws_region": "eu-west-1",
        "s3_bucket": "hitta-skyddsrum-microservices",
        "domain": "stageapi.hittaskyddsrum.se",
        "cors": true,
        "route53_enabled": true,
	"project_name": "hitta-skyddsrum-services",
        "lets_encrypt_key": "s3://hitta-skyddsrum-https-certificate/account.key",
        "runtime": "python2.7",
        "environment_variables": {
          "MYSQL_DATABASE_USER": "$MYSQL_DATABASE_USER",
          "MYSQL_DATABASE_PASSWORD": "$MYSQL_DATABASE_PASSWORD",
          "MYSQL_DATABASE_DB": "$MYSQL_DATABASE_DB",
          "MYSQL_DATABASE_HOST": "$MYSQL_DATABASE_HOST"
        }
    },
    "prod": {
        "extends": "staging",
        "domain": "api.hittaskyddsrum.se",
        "s3_bucket": "hitta-skyddsrum-microservices-prod"
    }
}
